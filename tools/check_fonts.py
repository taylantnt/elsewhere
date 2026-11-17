#!/usr/bin/env python3
"""Report characters the game's fonts cannot draw.

The game composes its typeface with a Ren'Py FontGroup: kanji come from Kiwi
Maru, everything else from mini-wakuwaku-maru (see game/gui.rpy). Both fonts
accept a character they have no glyph for, and Ren'Py then draws nothing at
all -- the character is simply missing from the line.

This walks every .rpy file and checks each non-ASCII character against the font
that would draw it. A character that produces no ink is reported with a
file:line. Line comments are skipped, because nothing on them reaches a screen.

A screen can opt out of the game font with `font "DejaVuSans.ttf"` or
`text_font "DejaVuSans.ttf"` (and a style can do the same). Those elements are
skipped, since they are drawn by a font that does have the glyph.

Usage:
    python3 tools/check_fonts.py            # check the whole game
    python3 tools/check_fonts.py FILE...    # check specific files

It exits non-zero when it finds something, so it can be wired into a check.

The usual fix is a substitution, not a new font. The dialogue font is shared by
every line in the game, so prose has to use characters that font actually has.
"""

import os
import re
import sys
import unicodedata

from PIL import ImageFont

GAME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "game")
GUI = os.path.join(GAME, "gui.rpy")

# FontGroup.add(font, start, end) -- literal u"\uXXXX" bounds are what gui.rpy
# uses, so a small regex is enough to read the real configuration instead of
# duplicating it here.
ADD_RE = re.compile(
    r'game_font\.add\(\s*(?P<font>\w+)\s*,\s*'
    r'(?P<start>None|u"[^"]*"|"[^"]*")\s*,\s*'
    r'(?P<end>None|u"[^"]*"|"[^"]*")\s*\)')
FONT_RE = re.compile(r'^\s*(?P<name>\w+_font)\s*=\s*"(?P<path>[^"]+)"', re.M)

# Any element that pins its own font is not using the FontGroup. Ren'Py spells
# the button version `text_font`, so the prefix is part of the match.
OVERRIDE_RE = re.compile(r'(?:^|[\s_])(?:text_)?font\s+"([^"]+)"')

# Text that is passed to a screen as data cannot be traced to the displayable
# that draws it, so a line may say so itself.
PINNED_RE = re.compile(r'#\s*check_fonts:\s*pinned')
STYLE_REF_RE = re.compile(r'\bstyle\s+"?([\w.]+)"?')
STYLE_DEF_RE = re.compile(r'^\s*style\s+([\w.]+)\s*:')


def read_font_group():
    """Return [(start, end, font path)] plus the default font path."""
    text = open(GUI, encoding="utf-8").read()
    fonts = {name: path for name, path in FONT_RE.findall(text)}
    rules = []
    default = None
    for match in ADD_RE.finditer(text):
        font = fonts[match.group("font")]
        start, end = match.group("start"), match.group("end")
        if start == "None":
            default = font
            continue
        # Bounds are written as literal \uXXXX escapes in gui.rpy.
        start = start.strip('u"').encode().decode("unicode_escape")
        end = end.strip('u"').encode().decode("unicode_escape")
        rules.append((ord(start), ord(end), font))
    if default is None:
        raise SystemExit("could not find the FontGroup default in " + GUI)
    return rules, default


def font_for(codepoint, rules, default):
    for start, end, path in rules:
        if start <= codepoint <= end:
            return path
    return default


def indent_of(line):
    return len(line) - len(line.lstrip())


def block_span(lines, index):
    """Line numbers (0-based) of the statement that owns `index`.

    Ren'Py blocks are indentation, so the owner is the nearest line above with
    less indentation, and its body runs until the indentation drops back.
    """
    header = index
    if lines[index].rstrip().endswith(":"):
        body_indent = indent_of(lines[index]) + 1
    else:
        body_indent = indent_of(lines[index])
        for probe in range(index - 1, -1, -1):
            if not lines[probe].strip():
                continue
            if indent_of(lines[probe]) < body_indent:
                header = probe
                body_indent = indent_of(lines[probe]) + 1
                break
    end = index
    for probe in range(header + 1, len(lines)):
        if lines[probe].strip() and indent_of(lines[probe]) < body_indent:
            break
        end = probe
    return header, end


def collect_style_fonts(lines):
    """Map style name -> True when that style pins its own font."""
    fonts = {}
    for index, line in enumerate(lines):
        match = STYLE_DEF_RE.match(line)
        if not match:
            continue
        _header, end = block_span(lines, index)
        fonts[match.group(1)] = any(
            OVERRIDE_RE.search(lines[probe])
            for probe in range(index, end + 1))
    return fonts


def collect_pinned(lines):
    """Line numbers covered by a `# check_fonts: pinned` marker.

    The marker covers the statement that follows it, so a long data table can
    explain itself once instead of on every row.
    """
    pinned = set()
    for index, line in enumerate(lines):
        if not PINNED_RE.search(line):
            continue
        for probe in range(index + 1, len(lines)):
            if not lines[probe].strip() or lines[probe].lstrip().startswith("#"):
                continue
            start, end = block_span(lines, probe)
            pinned.update(range(start, end + 1))
            break
    return pinned


def uses_own_font(lines, index, style_fonts):
    """True when the element on this line is drawn with a pinned font."""
    header, end = block_span(lines, index)
    for probe in range(header, end + 1):
        if OVERRIDE_RE.search(lines[probe]):
            return True
    for probe in range(header, end + 1):
        for style in STYLE_REF_RE.findall(lines[probe]):
            if style_fonts.get(style):
                return True
    return False


def iter_rpy(paths):
    if paths:
        for path in paths:
            yield path
        return
    for root, _dirs, files in os.walk(GAME):
        for name in sorted(files):
            if name.endswith(".rpy"):
                yield os.path.join(root, name)


def main(argv):
    rules, default = read_font_group()
    handles = {}

    def handle(path):
        if path not in handles:
            handles[path] = ImageFont.truetype(os.path.join(GAME, path), 64)
        return handles[path]

    problems = []
    for path in iter_rpy(argv):
        with open(path, encoding="utf-8-sig") as source:
            lines = source.read().splitlines()
        style_fonts = collect_style_fonts(lines)
        pinned = collect_pinned(lines)
        for index, line in enumerate(lines):
            if line.lstrip().startswith("#"):
                continue
            blank = []
            for char in line:
                codepoint = ord(char)
                if codepoint < 128:
                    continue
                # Whitespace and invisible format characters take no ink on
                # purpose.
                if char.isspace() or unicodedata.category(char) == "Cf":
                    continue
                font_path = font_for(codepoint, rules, default)
                if any(handle(font_path).getmask(char, mode="L")):
                    continue
                blank.append((char, font_path))
            if not blank:
                continue
            if index in pinned:
                continue
            if uses_own_font(lines, index, style_fonts):
                continue
            for char, font_path in dict(blank).items():
                problems.append((path, index + 1, char, font_path))

    if not problems:
        print("All characters have glyphs in the game font.")
        return 0

    print("%d character(s) render blank:\n" % len(problems))
    for path, number, char, font_path in problems:
        print("  %s:%d  %r U+%04X  (missing from %s)"
              % (os.path.relpath(path, GAME) if path.startswith(GAME) else path,
                 number, char, ord(char), os.path.basename(font_path)))
    print("\nSubstitute a character the font has, or draw the element with a")
    print("font that has it (see DejaVuSans.ttf overrides in game/screens.rpy).")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
