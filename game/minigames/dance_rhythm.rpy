################################################################################
## NEON STEP: FOUR-LANE RHYTHM MINIGAME
################################################################################
##
## A 128 BPM synthwave track drives a four-lane note highway. The chart spans
## the whole track and is generated per difficulty against the audio clock, so
## arrows land on the beat rather than on a frame timer. The section map below
## is tuned to neon_step.mp3 (97 bars, ~182.8 s) -- change DANCE_TOTAL_BARS and
## DANCE_SECTIONS together if the music is swapped again.
##
## Keyboard: ← ↓ ↑ → or D F J K. Touch: tap the lane pads.
## Story use: call minigame_dance
## Test: jump test_dance
##

default persistent.dance_best_score = 0
default persistent.dance_best_accuracy = 0.0
default persistent.dance_best_grade = "N/A"

init python:
    import math
    import random

    DANCE_BPM = 128
    # Beat period measured from neon_step.mp3 via spectral-flux onset analysis
    # (127.99 BPM). Do not "round" this back to 60/128 -- the 0.005% difference
    # drifts ~20 ms over the full track.
    DANCE_BEAT = 0.46880
    DANCE_BAR = DANCE_BEAT * 4.0
    # Time of the first downbeat, measured from the track's onset envelope.
    # The old 0.10 guess put every note ~64 ms ahead of the music.
    DANCE_BEAT_OFFSET = 0.036
    # Audio output latency of renpy.music.get_pos, in seconds. get_pos reports
    # the position sent to the audio device, which runs ahead of what the
    # player hears by the mixer buffer. If notes still feel early vs the song,
    # raise this (try 0.04-0.08); if they feel late, lower it.
    DANCE_AUDIO_LAG = 0.0
    DANCE_TOTAL_BARS = 97      # ~182.8 s at 128 BPM
    DANCE_MUSIC = "audio/Music/neon_step.mp3"

    DANCE_LANE_COLORS = ["#53c8ff", "#7dff9f", "#ffd166", "#ff6f9f"]
    DANCE_LANE_GLYPHS = ["←", "↓", "↑", "→"]
    DANCE_LANE_KEYS = ["LEFT / D", "DOWN / F", "UP / J", "RIGHT / K"]

    DANCE_LANE_W = 150
    DANCE_LANE_GAP = 8
    DANCE_LANE_X = [16 + index * (DANCE_LANE_W + DANCE_LANE_GAP) for index in range(4)]
    DANCE_PLAY_W = 656
    DANCE_PLAY_H = 568
    DANCE_HIT_Y = 468
    DANCE_SCROLL = 420.0

    # Judgement windows, in seconds either side of the beat.
    DANCE_PERFECT = 0.055
    DANCE_GREAT = 0.105
    DANCE_GOOD = 0.16
    DANCE_MISS_WINDOW = 0.19

    DANCE_SCORES = {"PERFECT": 350, "GREAT": 220, "GOOD": 110}
    DANCE_GRADE_COLORS = {
        "PERFECT": "#ffe58a",
        "GREAT": "#8dffb0",
        "GOOD": "#7cc9ff",
        "MISS": "#ff7f97",
    }
    DANCE_GRADES = [
        (99.0, "S+", "#ffe38a"),
        (95.0, "S", "#7ef0ff"),
        (90.0, "A", "#8dffa8"),
        (82.0, "B", "#6fb9ff"),
        (70.0, "C", "#ffc46b"),
        (55.0, "D", "#ff8fa8"),
    ]
    DANCE_GRADE_LETTERS = tuple(letter for _threshold, letter, _color in DANCE_GRADES)

    def dance_best_grade_text():
        """Grade of the best scoring run, tolerating old/blank persistent values."""
        value = persistent.dance_best_grade
        if value in DANCE_GRADE_LETTERS:
            return value
        return "N/A"

    # ---------------------------------------------------------------- charts
    #
    # Each bar is a list of (beat offset, lane or lanes). Lanes are
    # left / down / up / right. Double entries are chords.

    DANCE_VERSE_BARS = [
        [(0, 0), (1, 2), (2, 1), (3, 3)],
        [(0, 3), (1, 1), (2, 0), (3, 2)],
        [(0, 1), (1, 3), (1.5, 2), (2, 0), (3, 2)],
        [(0, 2), (0.5, 1), (1, 3), (2, 0), (2.5, 2), (3, 1)],
    ]

    DANCE_BUILD_BARS = [
        [(index * 0.5, lane) for index, lane in enumerate((0, 1, 2, 3, 2, 1, 0, 1))],
        [(index * 0.5, lane) for index, lane in enumerate((3, 2, 1, 0, 1, 2, 3, 2))],
        [(0, (0, 3)), (0.5, 2), (1, 1), (1.5, 3), (2, (1, 2)), (2.5, 0), (3, 3), (3.5, 1)],
        [(0, 0), (0.5, 1), (1, 2), (1.5, 3), (2, 2), (2.5, 1),
         (3.0, 0), (3.25, 1), (3.5, 2), (3.75, 3)],
    ]

    DANCE_CHORUS_BARS = [
        [(0, 0), (0.5, 2), (1, 1), (1.5, 3), (2, 0), (2.5, 2), (3, 1), (3.5, 3)],
        [(0, 3), (0.5, 1), (1, 2), (1.5, 0), (2, 3), (2.5, 1), (3, 2), (3.5, 0)],
        [(0, 1), (0.5, 2), (1, (0, 3)), (2, 1), (2.5, 2), (3, (0, 3)), (3.5, 1)],
        [(0, (0, 3)), (1, 1), (1.5, 2), (2, (0, 3)), (3, 1), (3.5, 2), (3.75, 3)],
    ]

    DANCE_BREAK_BARS = [
        [(0, 2), (1, 0), (2, 3), (3, 1)],
        [(0, 0), (1, 3), (2, 1), (3, 2)],
        [(0, 1), (2, 0), (3, 2)],
        [(0, 3), (1, 1), (2, 2), (2.5, 3), (3, 0)],
    ]

    # The intro rides the quiet sparkle arp before the first drop. Bars 0-1 are
    # left open as a lead-in, so notes begin at bar 2.
    DANCE_INTRO_BARS = [
        [(0, 0), (2, 2)],
        [(0, 3), (2, 1)],
        [(0, 1), (2, 3)],
        [(0, 2), (2, 0)],
    ]

    # The outro rides the final crash out instead of stopping at the last chorus.
    DANCE_OUTRO_BARS = [
        [(0, 2), (2, 0)],
        [(0, 1), (2, (0, 3))],
        [(0, 2), (1.5, 1), (3, 3)],
        [(0, (0, 3)), (2, (1, 2))],
    ]

    # Section map for neon_step.mp3, derived from the track's energy layout:
    #   intro 0-7 | drop 8-23 | verse 24-39 | break 40-47 | build 48-55
    #   | drop II 56-87 | outro 88-96
    # Each entry is (first_bar, end_bar_exclusive, HUD label, pattern key).
    DANCE_SECTIONS = [
        (0, 8, "INTRO", "intro"),
        (8, 24, "DROP", "chorus"),
        (24, 40, "VERSE", "verse"),
        (40, 48, "BREAK", "break"),
        (48, 56, "BUILD", "build"),
        (56, 88, "DROP II", "chorus"),
        (88, DANCE_TOTAL_BARS, "OUTRO", "outro"),
    ]

    DANCE_PATTERNS = {
        "intro": DANCE_INTRO_BARS,
        "verse": DANCE_VERSE_BARS,
        "build": DANCE_BUILD_BARS,
        "chorus": DANCE_CHORUS_BARS,
        "break": DANCE_BREAK_BARS,
        "outro": DANCE_OUTRO_BARS,
    }

    def make_dance_chart(difficulty="normal"):
        notes = []

        def add_note(bar, beat, lanes):
            time = (bar * 4.0 + beat) * DANCE_BEAT + DANCE_BEAT_OFFSET
            if isinstance(lanes, int):
                lanes = (lanes,)
            if difficulty == "easy" and len(lanes) > 1:
                lanes = lanes[:1]
            for lane in lanes:
                notes.append({
                    "time": time,
                    "lane": lane,
                    "judged": False,
                    "result": None,
                    "hit_offset": 0.0,
                })

        def add_bar(bar, pattern):
            for beat, lanes in pattern:
                if difficulty == "easy" and abs(beat - round(beat)) > 0.001:
                    continue
                add_note(bar, beat, lanes)

        for start, end, _label, kind in DANCE_SECTIONS:
            pattern = DANCE_PATTERNS[kind]
            for offset, bar in enumerate(range(start, end)):
                if bar < 2:
                    continue
                add_bar(bar, pattern[offset % len(pattern)])
                if difficulty == "hard":
                    if kind in ("chorus", "build"):
                        add_note(bar, 3.75, (bar + 2) % 4)
                    elif kind == "verse":
                        add_note(bar, 3.25, (bar * 3) % 4)

        unique = {}
        for note in notes:
            unique[(round(note["time"], 4), note["lane"])] = note
        return sorted(unique.values(), key=lambda note: (note["time"], note["lane"]))

    # ---------------------------------------------------------------- engine

    class DanceRhythmEngine(object):
        DIFFICULTY_LABELS = {
            "easy": ("EASY", "Quarter notes / brighter timing"),
            "normal": ("NORMAL", "Eighth notes / chords"),
            "hard": ("HARD", "Sixteenths / faster scroll"),
        }

        def __init__(self):
            self.phase = "ready"
            self.difficulty = "normal"
            self.notes = []
            self.chart_end = 66.0
            self.elapsed = 0.0
            self.use_audio_clock = True
            self.fallback = 0.0
            self.clock_offset = 0.0
            self.speed_mult = 1.0

            self.score = 0
            self.combo = 0
            self.best_combo = 0
            self.perfect = 0
            self.great = 0
            self.good = 0
            self.misses = 0
            self.fever = False
            self.new_record = False
            self.finalized = False
            self.pause_elapsed = 0.0
            self.next_beep = 0

            self.lane_flash = [0.0, 0.0, 0.0, 0.0]
            self.lane_hold = [0.0, 0.0, 0.0, 0.0]
            self.bursts = []
            self.sparks = []
            self.popups = []
            self.combo_pulse = 0.0
            self.shake_timer = 0.0
            self.shake_amount = 0.0

        # ---------------------------------------------------------- lifecycle

        def start_run(self, difficulty):
            self.difficulty = difficulty
            self.speed_mult = {"easy": 0.86, "normal": 1.0, "hard": 1.16}.get(difficulty, 1.0)
            self.notes = make_dance_chart(difficulty)
            self.chart_end = max(note["time"] for note in self.notes) + 1.2

            self.phase = "playing"
            self.elapsed = 0.0
            self.fallback = 0.0
            self.clock_offset = 0.0
            self.next_beep = 0
            self.finalized = False
            self.new_record = False

            self.score = 0
            self.combo = 0
            self.best_combo = 0
            self.perfect = 0
            self.great = 0
            self.good = 0
            self.misses = 0
            self.fever = False

            self.lane_flash = [0.0, 0.0, 0.0, 0.0]
            self.lane_hold = [0.0, 0.0, 0.0, 0.0]
            self.bursts = []
            self.sparks = []
            self.popups = []
            self.combo_pulse = 0.0
            self.shake_timer = 0.0
            self.shake_amount = 0.0

        def pause(self):
            if self.phase != "playing":
                return
            self.phase = "paused"
            self.pause_elapsed = self.elapsed
            renpy.music.set_pause(True, channel="dance_music")
            renpy.music.set_volume(0.3, channel="dance_music")

        def resume(self):
            if self.phase != "paused":
                return
            position = renpy.music.get_pos(channel="dance_music")
            if position is not None:
                self.clock_offset = position - self.pause_elapsed - DANCE_AUDIO_LAG
            renpy.music.set_volume(0.8, channel="dance_music")
            renpy.music.set_pause(False, channel="dance_music")
            self.fallback = 0.0
            self.phase = "playing"

        def finalize(self):
            if self.finalized:
                return
            self.finalized = True
            self.phase = "results"
            renpy.music.stop(channel="dance_music", fadeout=1.2)

            best = persistent.dance_best_score or 0
            if self.score > best:
                self.new_record = True
                persistent.dance_best_score = self.score
                persistent.dance_best_grade = self.grade()[0]
            if self.accuracy > (persistent.dance_best_accuracy or 0.0):
                persistent.dance_best_accuracy = self.accuracy

        # ------------------------------------------------------------ ticking

        def sync_clock(self, dt):
            self.fallback += dt
            position = None
            if self.use_audio_clock:
                position = renpy.music.get_pos(channel="dance_music")
            if position is None:
                if self.fallback > 0.3:
                    self.elapsed += dt
            else:
                self.fallback = 0.0
                self.elapsed = max(0.0, position - self.clock_offset - DANCE_AUDIO_LAG)

        def update_count_in(self):
            while self.next_beep < 4 and self.elapsed >= self.next_beep * DANCE_BEAT + DANCE_BEAT_OFFSET:
                if self.next_beep > 0:
                    renpy.sound.play("audio/SFX/dance_select.wav", channel="dance_sfx4")
                self.next_beep += 1

        def update_notes(self):
            for note in self.notes:
                if not note["judged"] and self.elapsed > note["time"] + DANCE_MISS_WINDOW:
                    note["judged"] = True
                    note["result"] = "MISS"
                    self.misses += 1
                    self.combo = 0
                    self.fever = False
                    self.shake_timer = 0.16
                    self.shake_amount = 4.0
                    self.popup("MISS", DANCE_GRADE_COLORS["MISS"], note["lane"])
                    renpy.sound.play("audio/SFX/dance_miss.wav", channel="dance_sfx4")

        def tick(self, dt):
            dt = max(0.0, min(dt, 0.08))
            self.update_effects(dt)
            if self.phase != "playing":
                return
            self.sync_clock(dt)
            self.update_count_in()
            self.update_notes()
            if self.elapsed >= self.chart_end:
                self.finalize()

        def update_effects(self, dt):
            for burst in self.bursts:
                burst["life"] -= dt
            self.bursts = [burst for burst in self.bursts if burst["life"] > 0.0]

            for spark in self.sparks:
                spark["life"] -= dt
                spark["x"] += spark["vx"] * dt
                spark["y"] += spark["vy"] * dt
                spark["vy"] += 340.0 * dt
                spark["vx"] *= 0.97
            self.sparks = [spark for spark in self.sparks if spark["life"] > 0.0]

            for popup in self.popups:
                popup["life"] -= dt
            self.popups = [popup for popup in self.popups if popup["life"] > 0.0]

            for index in range(4):
                self.lane_flash[index] = max(0.0, self.lane_flash[index] - dt)
                self.lane_hold[index] = max(0.0, self.lane_hold[index] - dt)

            self.combo_pulse = max(0.0, self.combo_pulse - dt * 3.2)
            self.shake_timer = max(0.0, self.shake_timer - dt)

        # -------------------------------------------------------------- input

        def press(self, lane):
            if self.phase != "playing":
                return
            self.lane_flash[lane] = 0.22
            self.lane_hold[lane] = 0.16

            candidates = [
                note for note in self.notes
                if not note["judged"] and note["lane"] == lane
                and abs(note["time"] - self.elapsed) <= DANCE_GOOD
            ]
            if not candidates:
                return

            note = min(candidates, key=lambda item: abs(item["time"] - self.elapsed))
            difference = abs(note["time"] - self.elapsed)
            note["judged"] = True
            note["hit_offset"] = note["time"] - self.elapsed

            if difference <= DANCE_PERFECT:
                result = "PERFECT"
                self.perfect += 1
            elif difference <= DANCE_GREAT:
                result = "GREAT"
                self.great += 1
            else:
                result = "GOOD"
                self.good += 1
            note["result"] = result

            self.combo += 1
            self.best_combo = max(self.best_combo, self.combo)
            self.combo_pulse = 1.0

            if self.combo >= 25 and not self.fever:
                self.fever = True
                renpy.sound.play("audio/SFX/dance_fever.wav", channel="dance_sfx4")
                self.popup("FEVER!", "#ffd76a", None, size=1.5)

            multiplier = 1.0 + min(self.combo, 100) * 0.01
            if self.fever:
                multiplier *= 1.5
            self.score += int(round(DANCE_SCORES[result] * multiplier))

            self.popup(result, DANCE_GRADE_COLORS[result], lane)
            self.add_hit_effects(lane, result)

        def add_hit_effects(self, lane, result):
            center_x = DANCE_LANE_X[lane] + DANCE_LANE_W / 2.0
            self.bursts.append({
                "x": center_x,
                "y": DANCE_HIT_Y,
                "life": 0.42,
                "duration": 0.42,
                "color": DANCE_LANE_COLORS[lane],
            })
            count = 10 if result == "PERFECT" else 7
            for _ in range(count):
                angle = random.uniform(-2.6, -0.5)
                speed = random.uniform(70.0, 210.0)
                self.sparks.append({
                    "x": center_x + random.uniform(-18.0, 18.0),
                    "y": DANCE_HIT_Y - random.uniform(0.0, 12.0),
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "life": 0.42,
                    "duration": 0.42,
                    "angle": random.uniform(0.0, 360.0),
                    "color": DANCE_LANE_COLORS[lane],
                })

        def popup(self, text, color, lane=None, size=1.0):
            self.popups.append({
                "text": text,
                "color": color,
                "lane": lane,
                "life": 0.55,
                "duration": 0.55,
                "size": size,
            })

        # -------------------------------------------------------------- stats

        @property
        def accuracy(self):
            total = self.perfect + self.great + self.good + self.misses
            if not total:
                return 0.0
            points = self.perfect * 1.0 + self.great * 0.72 + self.good * 0.42
            return 100.0 * points / total

        @property
        def passed(self):
            return self.accuracy >= 70.0

        @property
        def fever_gauge(self):
            if self.fever:
                return 1.0
            return min(1.0, self.combo / 25.0)

        @property
        def score_text(self):
            return "{:,}".format(self.score)

        @property
        def difficulty_label(self):
            return self.DIFFICULTY_LABELS.get(self.difficulty, ("NORMAL", ""))[0]

        def grade(self):
            accuracy = self.accuracy
            for threshold, letter, color in DANCE_GRADES:
                if accuracy >= threshold:
                    return letter, color
            return "F", "#8899aa"

        def section_label(self):
            bar = int(self.elapsed // DANCE_BAR)
            for start, end, label, _kind in DANCE_SECTIONS:
                if bar < end:
                    return label
            return "OUTRO"


init python:
    renpy.music.register_channel("dance_music", mixer="music", loop=False)
    renpy.music.register_channel("dance_sfx4", mixer="sfx", loop=False)
    renpy.music.set_volume(0.8, channel="dance_sfx4")
    renpy.music.set_volume(0.8, channel="dance_music")


init python:
    def dance_start_run(engine, difficulty):
        engine.start_run(difficulty)
        renpy.music.set_pause(False, channel="dance_music")
        renpy.music.set_volume(0.8, channel="dance_music")
        renpy.music.stop(channel="dance_music")
        renpy.music.play(DANCE_MUSIC, channel="dance_music", loop=False)
        renpy.sound.play("audio/SFX/dance_start.wav", channel="dance_sfx4")


transform dance_beam(xpos_value, angle, tint, alpha_value):
    anchor (0.5, 0.0)
    xpos xpos_value
    ypos -40
    xysize (gui.scale(900), gui.scale(900))
    rotate angle
    alpha alpha_value
    matrixcolor TintMatrix(tint)


screen dance_rhythm(engine):
    modal True
    zorder 130

    $ lane_x = DANCE_LANE_X
    $ beat_phase = ((engine.elapsed - DANCE_BEAT_OFFSET) % DANCE_BEAT) / DANCE_BEAT
    $ beat_pulse = max(0.0, 1.0 - beat_phase * 2.4)
    $ scroll = DANCE_SCROLL * engine.speed_mult
    $ progress = min(1.0, engine.elapsed / max(0.1, engine.chart_end))
    $ accuracy_text = "%.1f" % engine.accuracy
    $ combo_color = "#ffd76a" if engine.fever else "#eaf6ff"
    $ fever_color = "#ff9fcf" if engine.fever else "#7fdcff"
    $ shake_x = int(math.sin(engine.elapsed * 97.0) * engine.shake_amount) if engine.shake_timer > 0.0 else 0
    $ shake_y = int(math.cos(engine.elapsed * 83.0) * engine.shake_amount * 0.6) if engine.shake_timer > 0.0 else 0
    $ elapsed_text = "%d:%02d" % (int(engine.elapsed) // 60, int(engine.elapsed) % 60)
    $ total_text = "%d:%02d" % (int(engine.chart_end) // 60, int(engine.chart_end) % 60)
    $ best_score_text = "{:,}".format(persistent.dance_best_score or 0)
    $ best_grade_text = dance_best_grade_text()

    add "images/dance/bg_neon_club.png" xysize (config.screen_width, config.screen_height)
    add "images/dance/beam.png" at dance_beam(
        gui.scale(400), -22 + math.sin(engine.elapsed * 0.24) * 9, "#4fc7ff", 0.10 + 0.04 * beat_pulse)
    add "images/dance/beam.png" at dance_beam(
        gui.scale(880), 22 + math.cos(engine.elapsed * 0.27) * 9, "#ff5fa8", 0.10 + 0.04 * beat_pulse)
    add "images/dance/floor_glow.png" xpos 0 ypos gui.scale(600) xysize (config.screen_width, gui.scale(120))
    add "images/dance/vignette.png" xysize (config.screen_width, config.screen_height)

    # ------------------------------------------------------------ top strip
    fixed:
        xpos gui.scale(24)
        ypos gui.scale(10)
        xysize (gui.scale(520), gui.scale(52))

        text "NEON STEP" size gui.scale(30) bold True color "#eef7ff" kerning gui.scale(1)
        text "ELSEWHERE RHYTHM CLUB  /  128 BPM  /  ORIGINAL MIX" size gui.scale(9) color "#86a3bd" kerning gui.scale(2) ypos gui.scale(40)

    hbox:
        xalign 1.0
        xoffset -gui.scale(24)
        ypos gui.scale(18)
        spacing gui.scale(10)

        frame:
            background Solid("#0d2233")
            padding (gui.scale(14), gui.scale(5))
            text engine.difficulty_label size gui.scale(10) bold True color "#7fd6ff" kerning gui.scale(2)

        frame:
            background Solid("#25102f")
            padding (gui.scale(14), gui.scale(5))
            text engine.section_label() size gui.scale(10) bold True color "#ff9fcf" kerning gui.scale(2)

    fixed:
        xpos gui.scale(24)
        ypos gui.scale(66)
        xysize (gui.scale(1232), gui.scale(4))

        add Solid("#132030") xysize (gui.scale(1232), gui.scale(4))
        add Solid("#53c8ff") xysize (max(1, int(gui.scale(1232) * progress)), gui.scale(4))
        add "images/dance/glow.png" xpos int(gui.scale(1232) * progress) - gui.scale(20) ypos gui.scale(-18) xysize (gui.scale(40), gui.scale(40)) alpha 0.5 matrixcolor TintMatrix("#8fe4ff")

        for mark in [start for start, _end, _label, _kind in DANCE_SECTIONS[1:]]:
            add Solid("#061019") xpos int(gui.scale(1232) * ((mark * DANCE_BAR) / max(0.1, engine.chart_end))) ypos 0 xsize gui.scale(1) ysize gui.scale(4)

    # ----------------------------------------------------------- left panel
    frame:
        background Frame("images/dance/hud_panel.png", gui.scale(26), gui.scale(26))
        xpos gui.scale(20)
        ypos gui.scale(90)
        xysize (gui.scale(276), gui.scale(566))
        padding (gui.scale(22), gui.scale(18))

        vbox:
            xfill True
            spacing gui.scale(2)

            text "COMBO" size gui.scale(10) bold True color "#7c93ad" kerning gui.scale(3)
            text "[engine.combo]" size gui.scale(60) bold True color combo_color at Transform(zoom=1.0 + 0.16 * engine.combo_pulse)
            text "BEST  [engine.best_combo]" size gui.scale(10) color "#8ca7bd"

            null height gui.scale(8)
            add Solid("#1d3348") xysize (gui.scale(232), gui.scale(1))
            null height gui.scale(6)

            text "ACCURACY" size gui.scale(10) bold True color "#7c93ad" kerning gui.scale(3)
            hbox:
                spacing gui.scale(2)
                text accuracy_text size gui.scale(30) bold True color "#eaf6ff"
                text "%" size gui.scale(13) color "#86a3bd" yalign 0.85

            fixed:
                xysize (gui.scale(232), gui.scale(6))
                add Solid("#12202f") xysize (gui.scale(232), gui.scale(6))
                add Solid("#7dff9f") xysize (max(1, int(gui.scale(232) * engine.accuracy / 100.0)), gui.scale(6))

            null height gui.scale(10)
            add Solid("#1d3348") xysize (gui.scale(232), gui.scale(1))
            null height gui.scale(6)

            text "JUDGEMENTS" size gui.scale(10) bold True color "#7c93ad" kerning gui.scale(3)
            for judge_label, judge_color, judge_count in (
                ("PERFECT", DANCE_GRADE_COLORS["PERFECT"], engine.perfect),
                ("GREAT", DANCE_GRADE_COLORS["GREAT"], engine.great),
                ("GOOD", DANCE_GRADE_COLORS["GOOD"], engine.good),
                ("MISS", DANCE_GRADE_COLORS["MISS"], engine.misses),
            ):
                fixed:
                    xysize (gui.scale(232), gui.scale(17))
                    add Solid(judge_color) xysize (gui.scale(7), gui.scale(7)) yalign 0.5
                    text judge_label xpos gui.scale(15) yalign 0.5 size gui.scale(10) color "#9db4c8" kerning gui.scale(1)
                    text str(judge_count) xalign 1.0 yalign 0.5 size gui.scale(11) bold True color "#d5e8f8"

            null height gui.scale(10)
            add Solid("#1d3348") xysize (gui.scale(232), gui.scale(1))
            null height gui.scale(6)

            hbox:
                xfill True
                text "RANK" size gui.scale(10) bold True color "#7c93ad" kerning gui.scale(3) yalign 0.5
                $ live_letter, live_color = engine.grade()
                text live_letter xalign 1.0 size gui.scale(16) bold True color live_color

            null height gui.scale(4)
            text engine.DIFFICULTY_LABELS.get(engine.difficulty, ("NORMAL", ""))[1] size gui.scale(8) color "#8199b0"

            null height gui.scale(12)
            add Solid("#1d3348") xysize (gui.scale(232), gui.scale(1))
            null height gui.scale(6)

            text "NOW PLAYING" size gui.scale(10) bold True color "#7c93ad" kerning gui.scale(3)
            fixed:
                xysize (gui.scale(232), gui.scale(54))
                for bar in range(14):
                    $ bar_height = int(gui.scale(7 + 34 * abs(math.sin(engine.elapsed * 2.2 + bar * 0.73)) * (0.35 + 0.65 * beat_pulse)))
                    add Solid("#4fc7ff" if bar % 2 == 0 else "#7dff9f") xpos gui.scale(bar * 16) ypos gui.scale(54) - bar_height xsize gui.scale(11) ysize bar_height alpha 0.62

    # ---------------------------------------------------------- right panel
    frame:
        background Frame("images/dance/hud_panel.png", gui.scale(26), gui.scale(26))
        xpos gui.scale(984)
        ypos gui.scale(90)
        xysize (gui.scale(276), gui.scale(566))
        padding (gui.scale(22), gui.scale(18))

        vbox:
            xfill True
            spacing gui.scale(2)

            text "SCORE" size gui.scale(10) bold True color "#7c93ad" kerning gui.scale(3)
            text engine.score_text size gui.scale(34) bold True color "#eaf6ff"

            null height gui.scale(8)
            add Solid("#1d3348") xysize (gui.scale(232), gui.scale(1))
            null height gui.scale(6)

            text "FEVER" size gui.scale(10) bold True color "#7c93ad" kerning gui.scale(3)
            hbox:
                spacing gui.scale(8)
                text ("ACTIVE" if engine.fever else "CHARGE") size gui.scale(13) bold True color fever_color
                text ("x1.5 SCORE" if engine.fever else "[engine.combo] / 25") size gui.scale(9) color "#8ca7bd" yalign 0.75

            fixed:
                xysize (gui.scale(232), gui.scale(10))
                add Solid("#1a1124") xysize (gui.scale(232), gui.scale(10))
                add Solid("#ff6f9f") xysize (max(1, int(gui.scale(232) * engine.fever_gauge)), gui.scale(10))
                if engine.fever:
                    add "images/dance/glow.png" xpos 0 ypos gui.scale(-10) xysize (gui.scale(232), gui.scale(30)) alpha (0.22 + 0.14 * beat_pulse) matrixcolor TintMatrix("#ff8fc4")

            null height gui.scale(10)
            add Solid("#1d3348") xysize (gui.scale(232), gui.scale(1))
            null height gui.scale(6)

            text "RUN" size gui.scale(10) bold True color "#7c93ad" kerning gui.scale(3)
            fixed:
                xysize (gui.scale(232), gui.scale(17))
                text "HIT NOTES" size gui.scale(10) color "#9db4c8" yalign 0.5
                $ hit_total = engine.perfect + engine.great + engine.good
                text "[hit_total] / [engine.notes.__len__()]" xalign 1.0 yalign 0.5 size gui.scale(10) bold True color "#d5e8f8"
            fixed:
                xysize (gui.scale(232), gui.scale(17))
                text "MAX COMBO" size gui.scale(10) color "#9db4c8" yalign 0.5
                text "[engine.best_combo]" xalign 1.0 yalign 0.5 size gui.scale(10) bold True color "#d5e8f8"
            fixed:
                xysize (gui.scale(232), gui.scale(17))
                text "PERFECT" size gui.scale(10) color "#9db4c8" yalign 0.5
                text "[engine.perfect]" xalign 1.0 yalign 0.5 size gui.scale(10) bold True color DANCE_GRADE_COLORS["PERFECT"]

            null height gui.scale(10)
            add Solid("#1d3348") xysize (gui.scale(232), gui.scale(1))
            null height gui.scale(6)

            text "GUIDE" size gui.scale(10) bold True color "#7c93ad" kerning gui.scale(3)
            for guide_index in range(4):
                hbox:
                    spacing gui.scale(8)
                    add Solid(DANCE_LANE_COLORS[guide_index]) xysize (gui.scale(7), gui.scale(7)) yalign 0.5
                    text DANCE_LANE_KEYS[guide_index] size gui.scale(9) color "#9db4c8"

            null height gui.scale(12)
            add Solid("#1d3348") xysize (gui.scale(232), gui.scale(1))
            null height gui.scale(6)

            text "SET TIME" size gui.scale(10) bold True color "#7c93ad" kerning gui.scale(3)
            hbox:
                spacing gui.scale(4)
                text elapsed_text size gui.scale(16) bold True color "#eaf6ff"
                text "/ [total_text]" size gui.scale(10) color "#8199b0" yalign 0.8
            text "AUDIO-SYNCED CHART  /  128 BPM" size gui.scale(8) color "#6d8298"

            null height gui.scale(10)
            add Solid("#1d3348") xysize (gui.scale(232), gui.scale(1))
            null height gui.scale(6)

            text "PERSONAL BEST" size gui.scale(10) bold True color "#7c93ad" kerning gui.scale(3)
            hbox:
                spacing gui.scale(8)
                text best_grade_text size gui.scale(18) bold True color "#ffd76a"
                text best_score_text size gui.scale(12) bold True color "#eaf6ff" yalign 0.8
            text "BEAT THE RECORD TO SET A NEW RANK" size gui.scale(8) color "#6d8298"

    # ------------------------------------------------------------ playfield
    fixed:
        xpos gui.scale(312) + shake_x
        ypos gui.scale(90) + shake_y
        xysize (gui.scale(656), gui.scale(568))

        add Solid("#040911f2") xysize (gui.scale(656), gui.scale(568))

        for lane in range(4):
            $ lane_left = lane_x[lane]
            $ lane_color = DANCE_LANE_COLORS[lane]
            add "images/dance/lane_panel.png":
                xpos gui.scale(lane_left)
                ypos 0
                xysize (gui.scale(150), gui.scale(568))
                alpha 0.34
                matrixcolor TintMatrix(lane_color)
            add "images/dance/glow.png":
                xpos gui.scale(lane_left - 20)
                ypos gui.scale(300)
                xysize (gui.scale(190), gui.scale(268))
                alpha (0.05 + 0.14 * (engine.lane_flash[lane] / 0.22))
                matrixcolor TintMatrix(lane_color)

        for lane in range(1, 4):
            add Solid("#0b1d2d") xpos gui.scale(lane_x[lane] - 4) ypos 0 xsize gui.scale(2) ysize gui.scale(568)

        add Solid("#0d1b2a") xpos gui.scale(0) ypos 0 xsize gui.scale(2) ysize gui.scale(568)
        add Solid("#0d1b2a") xpos gui.scale(654) ypos 0 xsize gui.scale(2) ysize gui.scale(568)

        $ first_beat = int(math.floor(engine.elapsed / DANCE_BEAT)) - 1
        for beat_index in range(24):
            $ beat_time = (first_beat + beat_index) * DANCE_BEAT + DANCE_BEAT_OFFSET
            $ beat_y = DANCE_HIT_Y - (beat_time - engine.elapsed) * scroll
            if -4 <= beat_y <= DANCE_HIT_Y:
                if (first_beat + beat_index) % 4 == 0:
                    add Solid("#7fc8ff2e") xpos gui.scale(8) ypos gui.scale(beat_y) xsize gui.scale(640) ysize gui.scale(1)
                else:
                    add Solid("#7fc8ff14") xpos gui.scale(8) ypos gui.scale(beat_y) xsize gui.scale(640) ysize gui.scale(1)

        if engine.fever:
            add Solid("#ff4fa0") xysize (gui.scale(656), gui.scale(568)) alpha (0.045 + 0.05 * beat_pulse)
            text "FEVER" size gui.scale(74) bold True color "#ff8fc4" kerning gui.scale(14) xalign 0.5 ypos gui.scale(160) at Transform(alpha=0.06 + 0.04 * beat_pulse)

        # notes
        for note in engine.notes:
            if not note["judged"]:
                $ note_y = DANCE_HIT_Y - (note["time"] - engine.elapsed) * scroll
                if -64 <= note_y <= DANCE_HIT_Y + 6:
                    $ note_center = lane_x[note["lane"]] + 75
                    $ note_color = DANCE_LANE_COLORS[note["lane"]]
                    $ note_alpha = min(1.0, max(0.0, (note_y + 64) / 88.0))
                    add "images/dance/note_trail.png":
                        xpos gui.scale(note_center - 9)
                        ypos gui.scale(note_y - 108)
                        xysize (gui.scale(18), gui.scale(96))
                        alpha (0.6 * note_alpha)
                        matrixcolor TintMatrix(note_color)
                    add "images/dance/glow.png":
                        xpos gui.scale(note_center - 60)
                        ypos gui.scale(note_y - 60)
                        xysize (gui.scale(120), gui.scale(120))
                        alpha (0.3 * note_alpha)
                        matrixcolor TintMatrix(note_color)
                    add "images/dance/note_gem.png":
                        xpos gui.scale(note_center - 32)
                        ypos gui.scale(note_y - 32)
                        xysize (gui.scale(64), gui.scale(64))
                        alpha note_alpha
                        matrixcolor TintMatrix(note_color)
                    text DANCE_LANE_GLYPHS[note["lane"]] size gui.scale(22) bold True color "#071018" xpos gui.scale(note_center) xanchor 0.5 ypos gui.scale(note_y) yanchor 0.5 at Transform(alpha=0.9 * note_alpha)

        # receptors
        for lane in range(4):
            $ lane_left = lane_x[lane]
            $ lane_color = DANCE_LANE_COLORS[lane]
            $ flash = engine.lane_flash[lane] / 0.22
            $ ring_scale = 1.0 + 0.05 * beat_pulse + 0.13 * flash
            $ ring_size = int(gui.scale(146) * ring_scale)
            add "images/dance/receptor_ring.png":
                xpos gui.scale(lane_left + 75) - ring_size / 2
                ypos gui.scale(DANCE_HIT_Y) - ring_size / 2
                xysize (ring_size, ring_size)
                alpha (0.5 + 0.3 * beat_pulse + 0.35 * flash)
                matrixcolor TintMatrix(lane_color)
            add "images/dance/glow.png":
                xpos gui.scale(lane_left - 14)
                ypos gui.scale(DANCE_HIT_Y - 54)
                xysize (gui.scale(178), gui.scale(108))
                alpha (0.1 + 0.3 * flash)
                matrixcolor TintMatrix(lane_color)
            add "images/dance/receptor_pad.png":
                xpos gui.scale(lane_left + 5)
                ypos gui.scale(DANCE_HIT_Y - 18)
                xysize (gui.scale(140), gui.scale(48))
                alpha (0.62 + 0.38 * flash)
                matrixcolor TintMatrix(lane_color)
            text DANCE_LANE_GLYPHS[lane] size gui.scale(22) bold True color "#06101a" xpos gui.scale(lane_left + 75) xanchor 0.5 ypos gui.scale(DANCE_HIT_Y + 6) yanchor 0.5

            button:
                xpos gui.scale(lane_left + 5)
                ypos gui.scale(DANCE_HIT_Y - 18)
                xysize (gui.scale(140), gui.scale(48))
                action Function(engine.press, lane)
                sensitive (engine.phase == "playing")
                background None
                hover_background Solid(lane_color + "26")
                padding (0, 0)

            text DANCE_LANE_KEYS[lane] size gui.scale(9) bold True color lane_color xpos gui.scale(lane_left + 75) xanchor 0.5 ypos gui.scale(DANCE_HIT_Y + 56) at Transform(alpha=0.75)

        # hit bursts + sparks
        for burst in engine.bursts:
            $ burst_progress = 1.0 - burst["life"] / burst["duration"]
            $ burst_size = int(gui.scale(40 + 150 * burst_progress))
            add "images/dance/burst.png":
                xpos gui.scale(burst["x"]) - burst_size / 2
                ypos gui.scale(burst["y"]) - burst_size / 2
                xysize (burst_size, burst_size)
                alpha max(0.0, 1.0 - burst_progress)
                matrixcolor TintMatrix(burst["color"])

        for spark in engine.sparks:
            $ spark_alpha = max(0.0, spark["life"] / spark["duration"])
            add "images/dance/spark.png":
                xpos gui.scale(spark["x"]) - gui.scale(9)
                ypos gui.scale(spark["y"]) - gui.scale(9)
                xysize (gui.scale(18), gui.scale(18))
                alpha spark_alpha
                at Transform(rotate=spark["angle"])
                matrixcolor TintMatrix(spark["color"])

        # judgements
        for popup in engine.popups:
            $ popup_progress = 1.0 - popup["life"] / popup["duration"]
            $ popup_alpha = max(0.0, popup["life"] / popup["duration"])
            $ popup_font = int(gui.scale(26 * popup["size"]) * (1.0 + 0.1 * (1.0 - popup_alpha)))
            if popup["lane"] is None:
                text popup["text"] size popup_font bold True color popup["color"] xalign 0.5 ypos gui.scale(250 - 34 * popup_progress) at Transform(alpha=popup_alpha) outlines [(gui.scale(2), "#04101c", 0, gui.scale(1))]
            else:
                text popup["text"] size popup_font bold True color popup["color"] xpos gui.scale(lane_x[popup["lane"]] + 75) xanchor 0.5 ypos gui.scale(DANCE_HIT_Y - 96 - 34 * popup_progress) at Transform(alpha=popup_alpha) outlines [(gui.scale(2), "#04101c", 0, gui.scale(1))]

        if engine.phase == "playing" and engine.elapsed < 3.4:
            $ ready_alpha = min(1.0, max(0.0, (3.4 - engine.elapsed) / 1.4))
            text "GET READY" size gui.scale(30) bold True color "#dff2ff" kerning gui.scale(9) xalign 0.5 ypos gui.scale(196) at Transform(alpha=ready_alpha)
            text "FIND THE BEAT" size gui.scale(10) color "#8fb4cc" kerning gui.scale(4) xalign 0.5 ypos gui.scale(236) at Transform(alpha=ready_alpha)

    # -------------------------------------------------------------- bottom
    text "← ↓ ↑ →   /   D F J K     /     TAP THE LANE PADS     /     ESC PAUSE" size gui.scale(10) bold True color "#7b93a9" kerning gui.scale(2) xalign 0.5 ypos gui.scale(670)

    # --------------------------------------------------------------- ready
    if engine.phase == "ready":
        $ best_text = "{:,}".format(persistent.dance_best_score or 0)
        $ best_grade = dance_best_grade_text()
        $ best_accuracy = "%.1f" % (persistent.dance_best_accuracy or 0.0)

        add Solid("#04070fcc")

        frame:
            background Frame("images/dance/dialog_panel.png", gui.scale(26), gui.scale(26))
            xalign 0.5
            yalign 0.5
            xysize (gui.scale(800), gui.scale(400))
            padding (gui.scale(42), gui.scale(30))

            vbox:
                xfill True
                spacing gui.scale(8)

                text "NEON STEP" size gui.scale(46) bold True color "#eef7ff" kerning gui.scale(2) xalign 0.5
                text "ELSEWHERE RHYTHM CLUB  /  128 BPM  /  ORIGINAL SYNTHWAVE MIX" size gui.scale(9) color "#8fb0c9" kerning gui.scale(3) xalign 0.5

                null height gui.scale(6)
                text "SELECT DIFFICULTY" size gui.scale(10) bold True color "#7c93ad" kerning gui.scale(4) xalign 0.5
                null height gui.scale(2)

                hbox:
                    xalign 0.5
                    spacing gui.scale(12)
                    for diff_key, diff_name, diff_desc, diff_color in (
                        ("easy", "EASY", "Quarter notes\nrelaxed scroll", "#7dff9f"),
                        ("normal", "NORMAL", "Eighth notes\nchords and lifts", "#53c8ff"),
                        ("hard", "HARD", "Sixteenths\nfast scroll", "#ff6f9f"),
                    ):
                        button:
                            xsize gui.scale(224)
                            action Function(dance_start_run, engine, diff_key)
                            background Solid("#0c1a26")
                            hover_background Solid("#16374d")
                            padding (gui.scale(16), gui.scale(14))

                            vbox:
                                spacing gui.scale(4)
                                text diff_name size gui.scale(18) bold True color diff_color kerning gui.scale(2) xalign 0.5
                                text diff_desc size gui.scale(9) color "#93aec5" text_align 0.5 xalign 0.5

                null height gui.scale(10)

                hbox:
                    xalign 0.5
                    spacing gui.scale(18)
                    text "BEST  [best_text]" size gui.scale(11) bold True color "#ffd76a"
                    text "RANK  [best_grade]" size gui.scale(11) bold True color "#8dffb0"
                    text "ACCURACY  [best_accuracy]%" size gui.scale(11) color "#a9c2d6"

                null height gui.scale(4)
                text "HIT EACH GEM AS IT CROSSES THE RECEPTOR.  CHORDS NEED BOTH LANES." size gui.scale(9) color "#7b93a9" kerning gui.scale(2) xalign 0.5
                text "ESC TO LEAVE THE SET" size gui.scale(8) color "#5f748a" xalign 0.5

    # -------------------------------------------------------------- paused
    elif engine.phase == "paused":
        add Solid("#04070fbb")

        frame:
            background Frame("images/dance/dialog_panel.png", gui.scale(26), gui.scale(26))
            xalign 0.5
            yalign 0.5
            xysize (gui.scale(500), gui.scale(305))
            padding (gui.scale(40), gui.scale(30))

            vbox:
                xfill True
                spacing gui.scale(12)
                text "PAUSED" size gui.scale(34) bold True color "#eef7ff" kerning gui.scale(6) xalign 0.5
                text "NEON STEP / [engine.difficulty_label]" size gui.scale(10) color "#8fb0c9" kerning gui.scale(2) xalign 0.5

                null height gui.scale(4)

                textbutton "RESUME":
                    xalign 0.5
                    action Function(engine.resume)
                    background Solid("#22628f")
                    hover_background Solid("#3188c4")
                    padding (gui.scale(28), gui.scale(10))
                    text_size gui.scale(12)
                    text_bold True
                    text_color "#ffffff"

                textbutton "RESTART":
                    xalign 0.5
                    action Function(dance_start_run, engine, engine.difficulty)
                    background Solid("#23303d")
                    hover_background Solid("#35485a")
                    padding (gui.scale(28), gui.scale(10))
                    text_size gui.scale(12)
                    text_bold True
                    text_color "#dfeaf4"

                textbutton "LEAVE THE SET":
                    xalign 0.5
                    action Return(False)
                    background Solid("#2a1820")
                    hover_background Solid("#4d2735")
                    padding (gui.scale(28), gui.scale(10))
                    text_size gui.scale(12)
                    text_bold True
                    text_color "#ffb3c3"

    # ------------------------------------------------------------- results
    elif engine.phase == "results":
        $ result_letter, result_color = engine.grade()
        $ result_accuracy = "%.2f" % engine.accuracy
        $ result_score = "{:,}".format(engine.score)

        add Solid("#04070fe0")

        frame:
            background Frame("images/dance/dialog_panel.png", gui.scale(26), gui.scale(26))
            xalign 0.5
            yalign 0.5
            xysize (gui.scale(760), gui.scale(470))
            padding (gui.scale(42), gui.scale(26))

            vbox:
                xfill True
                spacing gui.scale(4)

                text "SET COMPLETE" size gui.scale(12) bold True color "#7c93ad" kerning gui.scale(6) xalign 0.5
                text "NEON STEP  /  [engine.difficulty_label]" size gui.scale(24) bold True color "#eef7ff" kerning gui.scale(2) xalign 0.5

                null height gui.scale(2)

                hbox:
                    xalign 0.5
                    fixed:
                        xysize (gui.scale(240), gui.scale(176))
                        add "images/dance/glow.png" xysize (gui.scale(240), gui.scale(240)) alpha (0.24 + 0.05 * beat_pulse) matrixcolor TintMatrix(result_color)
                        text result_letter size gui.scale(124) bold True color result_color xalign 0.5 yalign 0.5 at Transform(zoom=1.0 + 0.02 * beat_pulse) outlines [(gui.scale(3), "#04070f", 0, gui.scale(2))]

                text "ACCURACY  [result_accuracy]%" size gui.scale(13) bold True color "#cfe6f6" xalign 0.5

                null height gui.scale(4)

                hbox:
                    xalign 0.5
                    spacing gui.scale(26)

                    vbox:
                        spacing gui.scale(2)
                        text "SCORE" size gui.scale(9) bold True color "#7c93ad" kerning gui.scale(3) xalign 0.5
                        text result_score size gui.scale(24) bold True color "#eef7ff" xalign 0.5
                    vbox:
                        spacing gui.scale(2)
                        text "MAX COMBO" size gui.scale(9) bold True color "#7c93ad" kerning gui.scale(3) xalign 0.5
                        text "[engine.best_combo]" size gui.scale(24) bold True color "#ffd76a" xalign 0.5
                    vbox:
                        spacing gui.scale(2)
                        text "FEVER" size gui.scale(9) bold True color "#7c93ad" kerning gui.scale(3) xalign 0.5
                        text ("YES" if engine.best_combo >= 25 else "NO") size gui.scale(24) bold True color ("#ff9fcf" if engine.best_combo >= 25 else "#8199b0") xalign 0.5

                null height gui.scale(4)

                hbox:
                    xalign 0.5
                    spacing gui.scale(20)
                    for judge_label, judge_color, judge_count in (
                        ("PERFECT", DANCE_GRADE_COLORS["PERFECT"], engine.perfect),
                        ("GREAT", DANCE_GRADE_COLORS["GREAT"], engine.great),
                        ("GOOD", DANCE_GRADE_COLORS["GOOD"], engine.good),
                        ("MISS", DANCE_GRADE_COLORS["MISS"], engine.misses),
                    ):
                        hbox:
                            spacing gui.scale(6)
                            add Solid(judge_color) xysize (gui.scale(7), gui.scale(7)) yalign 0.5
                            text judge_label size gui.scale(9) color "#9db4c8"
                            text str(judge_count) size gui.scale(9) bold True color judge_color

                if engine.new_record:
                    text "NEW PERSONAL BEST" size gui.scale(10) bold True color "#ffd76a" kerning gui.scale(3) xalign 0.5

                null height gui.scale(6)

                hbox:
                    xalign 0.5
                    spacing gui.scale(12)

                    textbutton "PLAY AGAIN":
                        action Function(dance_start_run, engine, engine.difficulty)
                        background Solid("#22628f")
                        hover_background Solid("#3188c4")
                        padding (gui.scale(28), gui.scale(11))
                        text_size gui.scale(12)
                        text_bold True
                        text_color "#ffffff"

                    textbutton "FINISH":
                        action Return(engine.passed)
                        background Solid("#20303d")
                        hover_background Solid("#334858")
                        padding (gui.scale(28), gui.scale(11))
                        text_size gui.scale(12)
                        text_bold True
                        text_color "#dfeaf4"

    # ---------------------------------------------------------------- keys
    if engine.phase == "playing":
        key "K_ESCAPE" action Function(engine.pause)
        key "K_LEFT" action Function(engine.press, 0)
        key "K_DOWN" action Function(engine.press, 1)
        key "K_UP" action Function(engine.press, 2)
        key "K_RIGHT" action Function(engine.press, 3)
        key "K_d" action Function(engine.press, 0)
        key "K_f" action Function(engine.press, 1)
        key "K_j" action Function(engine.press, 2)
        key "K_k" action Function(engine.press, 3)
    elif engine.phase == "paused":
        key "K_ESCAPE" action Function(engine.resume)
    else:
        key "K_ESCAPE" action Return(False)

    timer 0.016 repeat True action Function(engine.tick, 0.016)


label minigame_dance:
    window hide
    $ _dance_engine = DanceRhythmEngine()
    call screen dance_rhythm(_dance_engine)
    $ _dance_result = _return
    stop dance_music fadeout 0.6
    return _dance_result


label test_dance:
    scene black with Dissolve(0.4)
    "Neon Step: pick a difficulty, then hit each gem as it crosses the receptor. Hold the beat and the fever builds."
    call minigame_dance from _call_minigame_dance
    if _return:
        "You finish the set in rhythm. The floor lights flare as the last chord rings out."
    else:
        "The set ends early, but the beat is still waiting."
    return
