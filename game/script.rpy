# --- CORE SYSTEMS: LANGUAGE & PROGRESSION ---

# Define custom text tags for the language system
init python:
    # 1. JAPANESE FONT
    # The typeface itself is assembled in gui.rpy as `game_font`, a FontGroup that
    # takes romaji and kana from mini-wakuwaku-maru and kanji from Kiwi Maru. That
    # is needed because mini-wakuwaku-maru's kanji outlines are empty, which is why
    # every kanji used to render as a silent gap in an otherwise fine line.
    #
    # gui.rpy points gui.text_font / gui.name_text_font / gui.interface_text_font
    # at that group, and the standard screens read those. The style.* assignments
    # below are a fallback for any text drawn outside the standard styles.
    style.default.font = game_font
    style.say_dialogue.font = game_font
    style.say_label.font = game_font
    style.button_text.font = game_font
    style.menu_choice.font = game_font
    style.input.font = game_font

    # 2. Typewriter Sound Effect
    #
    # type.wav is a single 2 millisecond click followed by roughly 1.5 seconds of
    # digital silence. Looping it as-is therefore makes one click per line and then
    # nothing, which is the "it only plays once" bug.
    #
    # type_click.wav is that same click padded out to exactly one 30cps character
    # period (1/30 of a second = 1470 frames). Looping it while the line types fires
    # one click per character, which is the buruburuburuburu you asked for. It is
    # matched to preferences.text_cps = 30, which label start sets.
    #
    # It gets a channel of its own for two reasons. It runs for the whole length
    # of every line, so it must not be cut off by - or cut off - any other sound;
    # and it sits under the music rather than at the level of a door closing, so
    # its volume wants to be one number in one place instead of something every
    # scene has to remember.
    #
    # TYPEWRITER_VOLUME is that number. 1.0 is the file exactly as recorded.
    renpy.music.register_channel("typing", mixer="sfx", loop=True)
    TYPEWRITER_VOLUME = 0.35

    def type_sound(event, interact=True, **kwargs):
        if not interact:
            return
        if event == "show_done":
            renpy.music.play("audio/SFX/type_click.wav", channel="typing",
                             relative_volume=TYPEWRITER_VOLUME)
        elif event == "slow_done":
            renpy.music.stop(channel="typing")

    # A separate channel for looping place ambience, so the murmur of a room can
    # sit underneath the music track instead of fighting it for one channel.
    renpy.music.register_channel("ambient", mixer="sfx", loop=True)

    # And a channel for one-shot interface sounds: money changing hands, the
    # ticket gate snapping shut. They need their own channel because the music
    # and ambience channels are both busy, and because the typewriter click loops
    # on `typing` and would be cut off by - and would cut off - anything else.
    renpy.music.register_channel("sfx", mixer="sfx", loop=False)

    def play_sfx(path):
        renpy.sound.play(path, channel="sfx")

    # 3. The room's own ambience
    #
    # His room is the one place the player returns to, so it gets its own track
    # and the track changes with the time of day. Call this on the line after the
    # room's `scene` statement:
    #
    #     scene bg_room_night with stair_fade
    #     $ room_ambient(True)
    #
    # It is a default, not a rule. "Unless specified" works by simply not calling
    # it: if a particular visit wants different music, play that track yourself
    # instead of calling this. To silence the room on purpose, call this and then
    # `stop music`, the same way the arrival scene already does before the dream.
    def room_ambient(night=False, fadein=2.0):
        track = "audio/Music/room_night.mp3" if night else "audio/Music/room_day.mp3"
        renpy.music.play(track, channel="music", fadein=fadein)

    # 4. The street outside the house, at night
    #
    # Nearly every route home ends on this background, so the track lives here
    # instead of being repeated at each one. Call it on the line after the scene:
    #
    #     scene bg_home_exterior_night with walk_fade
    #     $ night_street()
    def night_street(fadein=1.5):
        renpy.music.play("audio/SFX/night.mp3", channel="music", fadein=fadein)

    def language_tag(tag, argument, contents):
        fluency = store.japanese_fluency
        if fluency >= 5:
            return [(renpy.TEXT_TAG, "color=#87cefa"), (renpy.TEXT_TEXT, contents[0][1]), (renpy.TEXT_TAG, "/color")]
        else:
            return []
    config.custom_text_tags["jp"] = language_tag

    # Set default typewriter speed for brand-new saves.
    config.default_text_cps = 30

# --- PLACEHOLDER ART ---
# Repaint these with your real backgrounds whenever you are ready. They exist so
# the scenes never error out (or show the grey "missing image" box) in the meantime.
#
# While a background is still missing, the placeholder prints the name of the art
# it is waiting for in the middle of the screen, so it is obvious at a glance
# which location we are standing in and which background still needs to be drawn.
#
# To swap a real background in, just replace the placeholder_bg(...) call with:
#     image bg_taxi_stand = Transform("images/backgrounds/taxi_stand.png", ...)
# and nothing else in the script has to move.
init python:
    def placeholder_bg(color, label):
        return Fixed(
            Solid(color),
            Text(
                label,
                xalign=0.5,
                yalign=0.45,
                size=58,
                color="#ffffff40",
                outlines=[],
                text_align=0.5,
            ),
            xysize=(config.screen_width, config.screen_height),
        )

    # The same trick for a face that has not been drawn yet. Scheduled on the same
    # 256x384 canvas as every real portrait, so the day the art arrives it drops
    # into the same slot the box is standing in and nothing else has to move.
    def placeholder_portrait(color, label):
        return Fixed(
            Solid(color),
            Text(
                label,
                xalign=0.5,
                yalign=0.5,
                size=26,
                color="#ffffff40",
                outlines=[],
                text_align=0.5,
            ),
            xysize=(256, 384),
        )

    # The two helpers below mean a background or a portrait can be dropped into
    # images/ and used with no code change at all. Until the file exists they
    # quietly draw the placeholder instead of the grey "missing image" box, so
    # unfinished art can never break the build.
    #
    #   backgrounds:  images/backgrounds/<name>.png
    #   portraits:    images/characters/<name>.png
    #
    # Usage is the same call either way, and the file - not the code - decides
    # whether you get the art or the placeholder:
    #
    #     image bg_kitchen_night = bg_or_placeholder("bg_kitchen_night", "#1C1B18", "KITCHEN AT NIGHT")
    #     image side clerk = At(portrait_or_placeholder("clerk", "#4a4038", "STUDENT\nRELATIONS"), portrait_idle)
    def bg_or_placeholder(name, color, label):
        path = "images/backgrounds/%s.png" % (name,)
        if renpy.loadable(path):
            return Transform(path, xysize=(config.screen_width, config.screen_height), fit="cover")
        return placeholder_bg(color, label)

    def portrait_or_placeholder(name, color, label):
        path = "images/characters/%s.png" % (name,)
        if renpy.loadable(path):
            return Transform(path, xysize=(256, 384), fit="contain")
        return placeholder_portrait(color, label)

# A click during a fade used to cut it in half. Ren'Py lets the player dismiss a
# transition while it is still playing, so a walk_fade became a hard cut for
# anyone who clicked as the screen started to go dark. Turning that off makes a
# transition run to the length it was written to, which is the whole point of
# fading rather than cutting.
#
# It also covers the timed beat pauses (the one under the stair climb, and so on).
# Every pause in this script has a delay, so none of them wait on a click and none
# of them can be stranded by this.
#
# Deliberate skipping is untouched: holding Ctrl still runs forward and drops
# transitions to hard cuts, which is how a replay should behave.
#
# Set at init rather than in the script so it is part of the clean store, and
# therefore holds after a load as well as on a new game.
init python:
    _dismiss_pause = False

    # A locked dialogue option stays on the page and goes grey instead of being
    # hidden until it is earned. A greyed line tells the player that there is a
    # way of answering here that he is not yet capable of, which is the entire
    # point of gating a choice; a line that is simply absent teaches nothing.
    #
    # The gate is the option's condition, and Ren'Py already marks a false one
    # insensitive, so all this does is stop it from being filtered out first.
    #
    # Story gates that are meant to be discoveries are written so they still read
    # correctly when they appear early. There is one of those at the moment, the
    # veteran assistant at the airport, and his label already handles the case
    # where the player walks up to him with nothing in his hands.
    config.menu_include_disabled = True

    # Right-click opens the game menu by default, and in a game that asks the
    # player to read rather than to click, an accidental right-click throws them
    # out of the scene. Only the mouse binding comes off; Escape still opens the
    # menu, so saving and quitting are untouched.
    config.keymap["game_menu"] = [key for key in config.keymap["game_menu"]
                                  if not key.startswith("mouseup")]

# A slow fade that reads as "walked there, and time passed". Every change of
# location below uses this instead of a hard cut.
define walk_fade = Fade(1.2, 0.3, 1.2)

# The same walk as walk_fade, stretched out a little, for the climb up to his room.
# Stairs take longer than a doorway does, and the fade is meant to move at the speed
# of the footsteps playing under it.
define stair_fade = Fade(1.6, 0.6, 1.6)

# The gate slamming shut should land harder than the built-in hpunch, which is a
# quarter of a second and gone before you feel it. Same side-to-side shake, but
# slower per swing and held for over a second, so the impact has time to land.
define gate_shake = Move((22, 0), (-22, 0), .18, bounce=True, repeat=True, delay=1.1)

# airport.png is only 626x417, so it is scaled up and centre-cropped to fill the
# 1280x720 screen rather than stretched out of shape. It has real art, so it gets
# no placeholder label.
image bg_airport = Transform("images/backgrounds/bg_airport.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_station = Transform("images/backgrounds/bg_station.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_platform = Transform("images/backgrounds/bg_platform.png", xysize=(config.screen_width, config.screen_height), fit="cover")
# The house and his bedroom each come in two lights: the night he arrives in, and
# the morning he wakes up to. They are the same rooms either way, so they are named
# by time of day rather than by room. Pick whichever matches the hour of the scene.
image bg_home_night = Transform("images/backgrounds/bg_home_inside_night.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_home_day = Transform("images/backgrounds/bg_home_inside_day.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_room_night = Transform("images/backgrounds/bg_room_night.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_room_day = Transform("images/backgrounds/bg_room_day.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_train_interior = Transform("images/backgrounds/bg_train_interior.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_home_exterior_night = Transform("images/backgrounds/bg_home_exterior_night.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_home_exterior_day = Transform("images/backgrounds/bg_home_exterior_day.png", xysize=(config.screen_width, config.screen_height), fit="cover")

# The kitchen on the first morning, which is where Act Five happens. Real art, so
# it gets no placeholder label.
image bg_kitchen = Transform("images/backgrounds/bg_kitchen_day.png", xysize=(config.screen_width, config.screen_height), fit="cover")

# The taxi stand and the back of the cab. Real art, so they get no placeholder
# label. The file names differ slightly from the image names (bg_taxistand.png,
# bg_taxi_inside.png), so the scene statements carry on using bg_taxi_stand and
# bg_taxi_interior untouched.
image bg_taxi_stand = Transform("images/backgrounds/bg_taxistand.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_taxi_interior = Transform("images/backgrounds/bg_taxi_inside.png", xysize=(config.screen_width, config.screen_height), fit="cover")
# The same cab seen once he wakes up at the destination: darker, the meter still
# lit, the street outside unfamiliar. Only used for the last beat of the ride.
image bg_taxi_interior_final = Transform("images/backgrounds/bg_taxi_inside_final.png", xysize=(config.screen_width, config.screen_height), fit="cover")

# The university gate on the first morning. There is a bg_campus.png sitting in
# images/backgrounds that may be the right shot for the courtyards beyond the
# gate; until that is decided the ground inside uses a placeholder.
image bg_school_gate = Transform("images/backgrounds/bg_school_gate.png", xysize=(config.screen_width, config.screen_height), fit="cover")

# The department's second floor is the last one still being drawn. Name the file
# bg_department_hall.png, drop it in images/backgrounds/, and it appears here on
# its own; until then the placeholder prints the room we are standing in.
image bg_campus_interior = Transform("images/backgrounds/bg_campus.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_department_hall = bg_or_placeholder("bg_department_hall", "#3a3630", "OUR DEPARTMENT\nSECOND FLOOR")
image bg_student_relations = Transform("images/backgrounds/bg_student_relations.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_lecture_hall = Transform("images/backgrounds/bg_lecture_hall.png", xysize=(config.screen_width, config.screen_height), fit="cover")

# The two rooms the first free afternoon can end in. The ramen shop has art now
# (it lives at images/backgrounds/bg_ramen_shop.png, which is why the scene name
# and the file name differ slightly). The club room is still being drawn, so it
# keeps printing its own name until bg_photo_club.png arrives.
image bg_ramen_shop = bg_or_placeholder("bg_ramen_shop", "#2b2118", "RAMEN SHOP\nLATE")
image bg_ramen = bg_or_placeholder("bg_ramen", "#2b2118", "RAMEN\nLATE")
# The same counter a few minutes later, with the bowl finished. Every route through
# the shop ends on this shot, right before he pays.
image bg_ramen_empty = bg_or_placeholder("bg_ramen_empty", "#2b2118", "EMPTY BOWL\nLATE")
image bg_photo_club = bg_or_placeholder("bg_photo_club", "#2f3230", "PHOTOGRAPHY CLUB\nCIRCLE - CLUB ROOM")

# The river path Hikari runs. Real art, so no placeholder label.
image bg_river = bg_or_placeholder("bg_river", "#1a2230", "RIVER PATH\nEVENING")

# The narrow street he ends up in when he takes the wrong turn out of the school
# gate, and walks deeper into the evening until he finds the ramen shop doorway.
# The art is already low and warm, so nothing darkens it; the dialogue is what
# moves the light down.
image bg_alley = bg_or_placeholder("bg_alley", "#2a2320", "SIDE STREET\nDUSK")

image bg_train = Solid("#1C1B18")
# The hospital is not a place he visits; it is a single white frame that cuts into
# the scene for a fifth of a second. Drop bg_hospital.png into images/backgrounds/
# and it becomes that frame; until then it stays the flat white it has always been.
image hospital_flash = bg_or_placeholder("bg_hospital", "#d9e6ee", "HOSPITAL")

# The pamphlet the assistant hands over at the airport, held up in front of him
# while he tries to read it. The original is 1920x1408, so it is scaled down to
# sit inside the 1280x720 screen instead of swallowing it whole.
image pamphlet = Transform("images/ui/pamphlet.png", xysize=(720, 528))

# --- VARIABLES ---
default japanese_fluency = 0
default sister_affection = 0
default sim_affection = 0
default orson_affection = 0
default chef_affection = 0
default aya_affection = 0
default hana_affection = 0

# Airport state
default talked_to_security = False
default talked_to_man1 = False
default talked_to_npc2 = False
default has_pamphlet = False

# Two officers share the post at the terminal doors, so this ticks over every
# time he walks up. Even answers come from the man, odd ones from the woman.
default security_index = 0

# The journey home. travel_method records the choice made outside the terminal,
# and boarded_shinkansen is True only if he caught the express rather than the
# local. Between them they decide which version of the homecoming he gets.
default travel_method = None
default boarded_shinkansen = False
default arrived_late = False

# Both of these tick forward every time he looks, so the information boards
# scroll to a new notice each visit and the plants get progressively stranger.
default board_message_index = 0
default plant_index = 0

# --- MONEY & INVENTORY ---
# Money is the everyday resource: train fares, a bowl of ramen, a book from the
# reading club stall. Items are plain strings, listed in the Bag screen.
default money = 0
default inventory = []

# --- THE PLAYER ---
# The name asked for before the story starts, and the name the family and Hikari
# use when they talk to him. Kept to twelve characters so it never pushes the
# name box or the dialogue around.
default player_name = ""

# False until the first yen leaves his hand. The hint below only ever runs once
# per playthrough, so it is the very first payment that explains the wallet.
default money_hint_shown = False

# Same idea for the first item: the very first thing he puts in the bag explains
# the bag. Right now that is the pamphlet from the airport assistant.
default pamphlet_hint_shown = False

# The first time the day is his to spend. It runs the once-only card explaining
# what the free afternoons are for, right after he has picked one and the game has
# actually taken him there, so the explanation arrives with something to look at.
default after_school_hint_shown = False

# Which shape of afternoon he picked on the first day. Set by the menu in
# `first_class` and read immediately afterwards; declared here so it rolls back
# with everything else. The name is never shown to the player.
default first_day_activity = ""

# True once the river run has happened once. The run is not a confidant slot in
# locations.rpy yet, so this is the only thing that records it for now.
default first_run_started = False

# How many times he has been out to the river with her. The run is a recurring
# activity rather than one of the seven-visit chains in locations.rpy, so it
# keeps its own count here; WIRE reads this one through the contact entry in
# wire.rpy rather than from confidant_visits, which does not have a slot for her.
default hikari_visits = 0

# --- CHARACTER ATTRIBUTES ---
# The three-pillar progression system. Values live in save data, while the
# definitions and thresholds live in one place below so scene code only has to
# ask for a named reward.
#
# These are deliberately floats. A single answer in a conversation nudges an
# attribute by half a point, and it is the accumulation of those small answers
# that eventually moves a rank. Whole numbers would force every small answer to
# be either worthless or a full step, which is the thing this system exists to
# avoid.
default character_attributes = {
    "insight": 0.0,
    "grace": 0.0,
    "nerve": 0.0,
}
default attribute_reward_flags = []

# False until the very first point lands. That first gain is the one time the
# game stops and says what these three pillars actually are, and it never
# explains them again.
default attribute_hint_shown = False

# What he has actually said to people. A conversation that can be walked up to
# twice is a conversation a player can farm twice, so once he has answered
# somebody, that answer is what comes back the next time he talks to them. The
# key is the person, the value is which answer he gave them.
default remembered_choices = {}

# What the people who matter are holding against him. This is the memory, not the
# reward: the attribute system says what he is becoming, this says what he did.
default character_memories = {}

# How those people are named on screen. The memory keys are lowercase ids, but
# the notice is a sentence about a person, so it needs the name rather than the id.
default memory_names = {
    "hikari": "Hikari",
    "clerk": "the clerk",
    "professor": "the professor",
}

# The orb cluster in the corner. It stays off until the story proper begins, so
# the disclaimer cards at the start are not wearing a progress bar, and it
# switches on the moment he is actually in the world.
default show_attribute_hud = False

init python:
    # Every change to the wallet goes through these, so a scene never has to
    # worry about clamping or about going into the red.
    def give_money(amount):
        store.money += amount

    def can_afford(amount):
        return store.money >= amount

    def spend_money(amount):
        """Pay if you can. Returns True and deducts, or False and changes nothing."""
        if store.money < amount:
            return False
        store.money -= amount
        # Every yen that leaves his hand makes the same small sound.
        play_sfx("audio/SFX/money.wav")
        # The first time money actually moves, the game stops and says where the
        # money comes from. Once only, and never on a payment that did not happen.
        if not store.money_hint_shown:
            store.money_hint_shown = True
            renpy.call_screen("hint_card", eyebrow="A NOTE ON MONEY", body=store.hint_text_money)
        return True

    def add_item(item):
        if item not in store.inventory:
            store.inventory.append(item)
            # The first thing he ever picks up gets explained, once, right before
            # the "picked up" toast so the toast is not talking over the card.
            if item == "pamphlet" and not store.pamphlet_hint_shown:
                store.pamphlet_hint_shown = True
                renpy.call_screen("hint_card", eyebrow="A NOTE ON YOUR BAG", body=store.hint_text_bag)
            renpy.notify(_("Picked up: %s") % item_name(item))

    def remove_item(item):
        if item in store.inventory:
            store.inventory.remove(item)

    def has_item(item):
        return item in store.inventory

    def buy_item(price, item):
        """Hand over the money, then pocket the thing. False if he is short."""
        if not spend_money(price):
            return False
        add_item(item)
        return True

    # The definitions, colours, and pacing all live here so there is only one
    # source of truth for the character-attribute system.
    #
    # One colour each, and they are deliberately far apart on the wheel so the
    # corner of the screen can be read at a glance without a label: blue for the
    # one that thinks, green for the one that connects, red for the one that acts.
    attribute_defs = {
        "insight": {
            "name": "Insight",
            "blurb": "The power to understand.",
            "color": "#5fb8ff",
            "color_soft": "#5fb8ff55",
        },
        "grace": {
            "name": "Grace",
            "blurb": "The power to connect.",
            "color": "#77d98b",
            "color_soft": "#77d98b55",
        },
        "nerve": {
            "name": "Nerve",
            "blurb": "The power to act.",
            "color": "#ff6b6b",
            "color_soft": "#ff6b6b55",
        },
    }

    # The order the three are always drawn in. The HUD, the gain card, and the
    # Attributes page all walk this list, so the three of them can never end up
    # disagreeing about which orb is which.
    attribute_order = ["insight", "grace", "nerve"]

    # The little "[Grace]" that prefixes a locked dialogue option, so a closed
    # door says which key opens it instead of just refusing. Written once here so
    # the three of them can never drift apart from the definitions above.
    #
    # These are used as "[tag_grace] Tell her ..." and not as a literal string, and
    # that is the whole reason there is only one bracket here. Bracket escaping
    # happens inside the substitution pass: writing [[ in the *source* of a
    # caption yields a literal [, but this value is inserted *by* substitution, and
    # substitution does not run a second time over what it just inserted. The text
    # tokenizer that runs afterwards only knows about {} tags, so a [[ arriving
    # this way would be printed as [[. One bracket, substituted in, is correct.
    attribute_tag = {}
    for _attribute_id in attribute_order:
        attribute_tag[_attribute_id] = "{color=%s}[%s]{/color}" % (
            attribute_defs[_attribute_id]["color"],
            attribute_defs[_attribute_id]["name"],
        )

    tag_insight = attribute_tag["insight"]
    tag_grace = attribute_tag["grace"]
    tag_nerve = attribute_tag["nerve"]

    # Ranks are a five-step ladder and every step costs more than the last one,
    # so the early game moves quickly and the later game means something. These
    # are cumulative totals, not points-per-rank: rank 2 begins at 2.0 total.
    #
    # Everything is measured in halves. A single line of dialogue is worth half
    # a point at most, so it is the *accumulation* of answers that moves the
    # ladder rather than any one clever reply.
    attribute_rank_thresholds = [0.0, 2.0, 5.0, 9.5, 15.0]
    attribute_rank_names = [
        "Developing",
        "Emerging",
        "Capable",
        "Accomplished",
        "Exceptional",
    ]

    # Every reward in the game is one of these three sizes. Scene code names the
    # size rather than a number, so the whole economy can be retuned here
    # without touching a single line of dialogue.
    #
    #   small  — an aside, or one answer in a passing conversation
    #   medium — a real choice in a conversation that has a subject
    #   large  — a set-piece decision that changes the shape of the day
    attribute_reward_sizes = {
        "small": 0.5,
        "medium": 1.0,
        "large": 2.0,
    }

    def attribute_name(attribute_id):
        return attribute_defs.get(attribute_id, {}).get("name", attribute_id.title())

    def attribute_blurb(attribute_id):
        return attribute_defs.get(attribute_id, {}).get("blurb", "")

    def attribute_color(attribute_id):
        return attribute_defs.get(attribute_id, {}).get("color", "#ffffff")

    def attribute_color_alpha(attribute_id, alpha):
        """The attribute's colour with its opacity baked in.

        The orbs, the ticker, and the progress bars all arrive as one finished
        colour string rather than a colour plus an `alpha` property, because a
        screen displayable that has to combine the two is the kind of thing
        that silently does nothing on one Ren'Py version and works on the next.
        """
        base = attribute_color(attribute_id).lstrip("#")[:6]
        alpha = max(0.0, min(1.0, float(alpha)))
        return "#%s%02x" % (base, int(round(alpha * 255)))

    def format_points(value):
        """Points as the player should read them: 1, not 1.0. 0.5 stays 0.5."""
        value = float(value)
        if abs(value - round(value)) < 0.001:
            return str(int(round(value)))
        return "%.1f" % value

    def attribute_total(attribute_id):
        return max(0.0, float(store.character_attributes.get(attribute_id, 0.0)))

    def attribute_total_text(attribute_id):
        return format_points(attribute_total(attribute_id))

    def attribute_rank(attribute_id):
        total = attribute_total(attribute_id)
        rank = 1

        for i, threshold in enumerate(attribute_rank_thresholds, start=1):
            if total >= threshold:
                rank = i

        return min(rank, len(attribute_rank_names))

    def attribute_rank_name(attribute_id):
        return attribute_rank_names[attribute_rank(attribute_id) - 1]

    def attribute_progress(attribute_id):
        """How far this attribute has come, 0.0 to 1.0, over the whole ladder.

        This is what the orbs are filled with, and it is deliberately measured
        against the *final* threshold rather than the current rank. An orb that
        starts almost transparent therefore keeps getting more solid with every
        answer, instead of emptying itself again the moment a rank is reached,
        which is what made the first version of this read as a reset.
        """
        top = attribute_rank_thresholds[-1]
        if top <= 0:
            return 1.0
        return min(1.0, max(0.0, attribute_total(attribute_id) / top))

    def attribute_orb_alpha(attribute_id):
        """An orb's opacity, from barely-there to solid."""
        return 0.16 + 0.84 * attribute_progress(attribute_id)

    def attribute_rank_floor(attribute_id):
        """The running total at which the current rank began."""
        return attribute_rank_thresholds[attribute_rank(attribute_id) - 1]

    def attribute_rank_ceiling(attribute_id):
        """The running total that would end the current rank, or None at the top."""
        rank = attribute_rank(attribute_id)
        if rank >= len(attribute_rank_thresholds):
            return None
        return attribute_rank_thresholds[rank]

    def attribute_rank_progress(attribute_id):
        """How far through the current rank he is, 0.0 to 1.0.

        Separate from attribute_progress(): this one is the bar on the
        Attributes page, which should empty itself at every rank so each step of
        the ladder can be watched filling. The orbs use the other one, because
        they are meant to only ever get more solid.
        """
        ceiling = attribute_rank_ceiling(attribute_id)
        floor_value = attribute_rank_floor(attribute_id)

        if ceiling is None or ceiling <= floor_value:
            return 1.0

        span = ceiling - floor_value
        return max(0.0, min(1.0, (attribute_total(attribute_id) - floor_value) / span))

    def attribute_rank_span(attribute_id):
        """How many points the current rank is worth, for the "3 / 4.5" readout."""
        ceiling = attribute_rank_ceiling(attribute_id)
        if ceiling is None:
            return 0.0
        return ceiling - attribute_rank_floor(attribute_id)

    def attribute_rank_earned(attribute_id):
        """How many points he has put into the current rank, for the same readout."""
        return attribute_total(attribute_id) - attribute_rank_floor(attribute_id)

    def attribute_rank_next_text(attribute_id):
        """The line under the bar on the Attributes page."""
        ceiling = attribute_rank_ceiling(attribute_id)

        if ceiling is None:
            return "Everything this pillar has to give."

        next_rank = attribute_rank(attribute_id) + 1

        return "%s of %s to %s" % (
            format_points(attribute_rank_earned(attribute_id)),
            format_points(attribute_rank_span(attribute_id)),
            attribute_rank_names[next_rank - 1],
        )

    def has_attribute(attribute_id, minimum_rank):
        """Whether a gated choice is open to him yet.

        Gates are always by *rank*, never by raw points, so a locked line means
        "he has not become that person yet" rather than "you are half a point
        short". That is the difference between a door and a toll booth.

        Ranks are 1-based and start at 1, so 2 is the first number that can
        actually close anything: a gate of 1 is true from the first line of the
        game and is always a bug. Rank 2 is 2.0 points in that attribute.
        """
        return attribute_rank(attribute_id) >= minimum_rank

    def attribute_reward_value(amount):
        """A named size, or a raw number of points. Names are preferred."""
        if isinstance(amount, str):
            return float(attribute_reward_sizes.get(amount, attribute_reward_sizes["small"]))
        return float(amount)

    def add_attribute_points(attribute_id, amount="small", show="auto"):
        """Raise an attribute, and make sure the player sees that it happened.

        Every gain shows something, including the small ones. Which of the two
        things it shows is decided here so no scene ever has to think about it:

          show="auto"  — the quiet ticker, or the full card on a rank up
          show="card"  — the full card, for a set-piece decision
          show=False   — nothing at all, for bookkeeping that is not a reward

        A rank up always takes the full card whatever the size, because that is
        the moment the ladder actually moved and it should feel like it.
        """
        if attribute_id not in attribute_defs:
            raise Exception("Unknown attribute id: %r" % (attribute_id,))

        points = attribute_reward_value(amount)
        if points <= 0:
            return attribute_total(attribute_id)

        before_rank = attribute_rank(attribute_id)
        store.character_attributes[attribute_id] = attribute_total(attribute_id) + points
        after_rank = attribute_rank(attribute_id)
        rank_up = after_rank > before_rank

        if show is False:
            return attribute_total(attribute_id)

        if rank_up or show == "card":
            # Let the choice breathe for a moment before the card takes over, so
            # the reward reads as a follow-through rather than a cut.
            renpy.pause(0.45, hard=True)
            # The riser opens the animation and runs for 1.70s, which is exactly
            # as long as the stat takes to travel out of the middle. The landing
            # sound is fired by the screen itself, on a timer, so the two stay in
            # step no matter how the motion is retimed.
            play_sfx("audio/SFX/attribute_rise.wav")
            renpy.call_screen("attribute_gain_card", attribute_id=attribute_id,
                              amount=points, rank_up=rank_up)
            # The card has already returned, so the screen is clear again.
            show_attribute_gain_intro()
        else:
            # The common case is a half point in the middle of a conversation,
            # and that must not cost the player a click or a pause. It is a
            # chip that rides over the next couple of lines and hides itself.
            show_attribute_tick(attribute_id, points)
            # The chip takes itself away after 2.10s. Only the one time the
            # explanation is coming is it worth waiting that out, so the card
            # never dims the screen on top of the chip it is meant to follow.
            if not store.attribute_hint_shown:
                renpy.pause(2.10, hard=True)
            show_attribute_gain_intro()

        return attribute_total(attribute_id)

    def show_attribute_gain_intro():
        """The one and only explanation of what the three pillars are.

        It is called after the gain that triggered it has finished playing, so
        it never talks over its own animation. A full card has already returned
        by the time it runs, and the chip has been given its whole 2.10s.

        It is deliberately vague. It names the three pillars and says they come
        from real decisions, and then stops. The line he cannot answer yet, and
        the person who remembers what he said, are better discovered than
        explained, so neither is mentioned here.
        """
        if store.attribute_hint_shown:
            return

        store.attribute_hint_shown = True
        renpy.call_screen("hint_card", eyebrow="A NOTE ON WHO YOU ARE BECOMING",
                          body=store.hint_text_attribute)

    def show_attribute_tick(attribute_id, points):
        """Flash the small "Grace +0.5" chip and step out of the way.

        This is what a half point in the middle of a conversation looks like. It
        must not cost the player a click or a beat, so it is a screen that shows
        itself, waits, and hides itself again.

        The hide-then-show is the same trick renpy.notify uses: a second gain
        replaces the chip on screen instead of stacking a second one on top of
        it, and re-showing is also what replays the entrance animation.
        """
        renpy.hide_screen("attribute_tick")
        renpy.show_screen("attribute_tick", attribute_id=attribute_id, points=points)

    def reward_attributes_once(flag, rewards, show="card"):
        """Apply a one-time reward definition so a major choice cannot double-pay.

        Anything sitting inside a hub the player can walk back into has to go
        through here, or the same conversation can be farmed for a rank.
        """
        if flag in store.attribute_reward_flags:
            return False

        store.attribute_reward_flags.append(flag)

        for attribute_id, amount in rewards:
            add_attribute_points(attribute_id, amount=amount, show=show)

        return True

    def remembered_choice(person):
        """Which answer he already gave this person, or None if they are new."""
        return store.remembered_choices.get(person)

    def remember_choice(person, answer):
        """Latch an answer so walking back up to the same person replays it.

        Without this, any conversation the player can start twice is a slot
        machine: take answer A for the point, walk away, come back, take answer B
        for another. A person he has already spoken to is not a menu that
        re-rolls, so the answer is written down and played back instead.
        """
        store.remembered_choices[person] = answer

    def remember(who, note):
        """Log something he said that an important character will hold onto.

        The attribute system records what he is becoming; this records what he
        did, in the words of the person who will bring it up again later.
        """
        store.character_memories.setdefault(who, []).append(note)
        # Same hide-then-show trick as the tick chip: a second memory replaces the
        # first on screen and replays the entrance instead of stacking.
        renpy.hide_screen("memory_notice")
        renpy.show_screen("memory_notice",
                          who=store.memory_names.get(who, who.capitalize()))


# --- ITEMS ---
# `inventory` holds item ids. This table holds everything else the Bag needs to
# draw one: what it is called, its picture, the line of description, and whether
# it can actually be used for anything. Items waiting on art fall back to a plain
# placeholder, the same way the unfinished backgrounds do, so the Bag never shows
# a broken box.
init python:
    item_data = {

        "phone": {
            "name": "Phone",
            "icon": "images/ui/phone.png",
            "desc": "This cannot be used at the moment.",
            "usable": False,
        },

        "pamphlet": {
            "name": "Pamphlet",
            "icon": "images/ui/pamphlet.png",
            "desc": "A folded map covered in arrows and kanji. I can't read it, but other people can. Open it to take a closer look.",
            "usable": True,
            "use_label": "Open",
        },

        "ticket_320": {
            "name": "320 Yen Ticket",
            "icon": "images/ui/ticket.png",
            "desc": "I purchased the wrong ticket, so this cannot be used.",
            "usable": False,
        },

        "ticket_800": {
            "name": "800 Yen Ticket",
            "icon": "images/ui/ticket.png",
            "desc": "I purchased the wrong ticket, so this cannot be used.",
            "usable": False,
        },

        "student_card": {
            "name": "Student Card",
            "icon": "images/ui/student_card.png",
            "desc": "My student card. I should always have this with me. I heard I can even get discounts with it.",
            "usable": False,
        },

    }

    def item_name(item):
        return item_data.get(item, {}).get("name", item)

    def item_desc(item):
        return item_data.get(item, {}).get("desc", "")

    def item_usable(item):
        return item_data.get(item, {}).get("usable", False)

    def item_use_label(item):
        """What the Bag's action button says. "Open" for a pamphlet, "Use" by default."""
        return item_data.get(item, {}).get("use_label", "Use")

    def item_icon(item, size):
        """The item's picture, or a soft placeholder until its art exists."""
        path = item_data.get(item, {}).get("icon")

        if path and renpy.loadable(path):
            return Transform(path, xysize=(size, size), fit="contain")

        return Fixed(
            Solid("#ffffff10"),
            Text(item_name(item), xalign=0.5, yalign=0.5,
                 size=max(11, int(size / 4)), color="#ffffff55", outlines=[]),
            xysize=(size, size),
        )

# --- THINGS THAT CHANGE THE MORE YOU LOOK AT THEM ---
# The boards scroll to a different notice every time he walks past, and the
# plants get steadily stranger the more of them he inspects, which is the
# easter egg you asked for. Both lists are read by label check_boards and
# label look_plants, and both are indexed by a counter that lives in the
# defaults above.
init python:
    board_messages = [
        "Please check your flight departure time carefully. Gates close 30 minutes before departure.",
        "All passengers must present valid identification and boarding passes at security checkpoints.",
        "Baggage restrictions apply. Check with your airline for specific weight and size limits.",
        "Flight delays may occur due to weather conditions. Monitor departure boards for updates.",
        "Duty-free shopping is available after security. Remember liquid restrictions for carry-on items.",
        "Emergency exits are located throughout the terminal. Familiarize yourself with the nearest exit.",
        "Free WiFi is available throughout the airport. Connect to 'Airport_Guest' network.",
    ]

    plant_dialogues = [
        "Oh what a great plant!",
        "Oh, another plant!",
        "These plants are quite nice...",
        "I don't have time to look at plants all day.",
        "Why am I looking at plants?",
        "Maybe I'll get a plant when I have my own place. Wonder if my host family would allow that?",
        "Same as the last one.",
        "Really? Another plant?",
        "PLANTSSS!",
        "PLAAAAAAAAANTTTTSSSS!!!",
    ]

# --- CHARACTERS ---
# Added character_callback for typewriter sound
# The name in this box is the one the player typed at the start of the game, so
# every line he says is labelled with his own name. dynamic=True tells Ren'Py to
# re-read [player_name] each time instead of resolving it once at boot.
define mc = Character("[player_name]", dynamic=True, callback=type_sound)
define hikari = Character("Hikari", color="#ffb6c1", callback=type_sound, image="sister")
define orson = Character("Orson", color="#a9a9a9", callback=type_sound)
define chef = Character("Chef", color="#deb887", callback=type_sound, image="chef")
define sim = Character("Sim", color="#add8e6", callback=type_sound, image="sim")
define aya = Character("Aya", color="#dda0dd", callback=type_sound)
define hana = Character("Hana", color="#98fb98", callback=type_sound)

# Generic NPCs
#
# The two people in the terminal he can actually talk to. They used to share a
# single "Stranger" name box, which made the one warm person in the building read
# as the same man who had just told him to move. They are two different people,
# so they get two different boxes and two different pictures.
define timid_man = Character("Timid Man", callback=type_sound, image="timid_man")
define cheerful_woman = Character("Cheerful Woman", callback=type_sound, image="cheerful_woman")

# Two officers work the same post at the terminal doors. They share the job
# title in the name box and are told apart by the picture: security.png is the
# man, security2.png is the woman.
define security = Character("Security", callback=type_sound, image="security")
define security2 = Character("Security", callback=type_sound, image="security2")

# The driver who takes him home if he picks the taxi.
define taxi_driver = Character("Taxi Driver", callback=type_sound, image="taxi_driver")

# The host family. Only the parents are awake on the night he arrives, so they are
# named by role here and introduce themselves properly at the door. Hikari is
# already asleep, so she has no lines in this scene.
define mother = Character("Mother", color="#e8c8a0", callback=type_sound, image="mother")
define father = Character("Father", color="#c8c4b4", callback=type_sound, image="father")

# The two airport staff. image="name" is what puts their picture beside the
# dialogue box while they are the one talking; the picture itself is the
# "image side name" below. Add image= to any other character to do the same.
define assistant = Character("Assistant", callback=type_sound, image="assistant")
define veteran = Character("Veteran Assistant", callback=type_sound, image="veteran")

# The university. The professor is the first person in Japan to tell him a rule
# he did not know existed, and the clerk is the first adult here who was told he
# was coming before he arrived. Both of those are the point of their scenes.
define professor = Character("Professor", color="#c9c4b0", callback=type_sound, image="professor")
define clerk = Character("Student Relations", color="#b8c6bd", callback=type_sound, image="clerk")

# --- PORTRAITS ---
# The picture in the left gutter belongs to whoever is talking. Two things are
# automatic here:
#
#   1. Every portrait breathes. A slow bob on a loop, so nobody sits there like a
#      cardboard cutout.
#   2. While a character is actually speaking, Ren'Py swaps to the "talking"
#      version of their portrait if one exists, and back to the plain one the
#      moment they stop. That swap is config.speaking_attribute below. It needs no
#      per-line code, so it covers every character at once, including ones you add
#      later.
#
# Right now nobody owns a talking picture, so everyone just gets the breathing.
# Characters with no "side" image at all (the narrator, the MC) show nothing,
# which is why anything you have not drawn yet is safe to leave out.
#
# The source files are 1024x1536, so they are scaled down to sit beside the text.
#
# The bob is read off the game clock rather than eased by ATL. ATL counts from the
# moment its displayable is built, and Ren'Py rebuilds the side image on every line
# of dialogue, so an ease pair snapped back to the top each time a new line opened.
# Reading the clock instead means the phase survives those rebuilds, and nobody
# visibly jumps mid-sentence.
init python:
    import math

    def portrait_breathe(trans, st, at):
        # 0 -> 4px -> 0 over 3.2s, the same shape the old ease pair drew.
        trans.yoffset = 2.0 - 2.0 * math.cos(renpy.get_game_runtime() * math.pi / 1.6)
        return 0

    def portrait_chatter(trans, st, at):
        # The same idea at speaking speed: 0 -> 6px -> 0 in about a fifth of a second.
        trans.yoffset = 3.0 - 3.0 * math.cos(renpy.get_game_runtime() * math.pi / 0.11)
        return 0

transform portrait_idle:
    subpixel True
    function portrait_breathe

# A quicker, shallower version of the same motion, used while speaking.
transform portrait_talk:
    subpixel True
    function portrait_chatter

# The assistant is the first character in the game with a second drawing: the same
# girl, caught out, looking away because she cannot find the English for what she
# has to say. Which of the two is on screen is read from a flag every time the
# picture is built, so it needs no new machinery and no other character has to
# change. Set assistant_shy to True before she speaks and back to False when she
# has recovered.
default assistant_shy = False

image side assistant = At(ConditionSwitch(
    "assistant_shy",
    Transform("images/characters/assistant_shy.png", xysize=(256, 384), fit="contain"),
    True,
    Transform("images/characters/assistant.png", xysize=(256, 384), fit="contain"),
), portrait_idle)
image side veteran = At(Transform("images/characters/veteran.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side security = At(Transform("images/characters/security.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side security2 = At(Transform("images/characters/security2.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side mother = At(Transform("images/characters/mother.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side father = At(Transform("images/characters/father.png", xysize=(256, 384), fit="contain"), portrait_idle)

# Hikari. She is asleep on the night he arrives and awake on the morning after,
# which makes the kitchen her first appearance on screen, so this is the first
# time her picture is needed.
#
# She has a second drawing for the evenings she runs: the same girl in what she
# actually runs in. Which one is on screen is read from a flag every time the
# picture is built, the same way the assistant's shy drawing works, so it needs
# no per-line attribute syntax and no other change. Set hikari_run to True when
# she changes and back to False once she is back in the house.
default hikari_run = False

image side sister = At(ConditionSwitch(
    "hikari_run",
    Transform("images/characters/sister_run.png", xysize=(256, 384), fit="contain"),
    True,
    Transform("images/characters/sister.png", xysize=(256, 384), fit="contain"),
), portrait_idle)
image side taxi_driver = At(Transform("images/characters/taxidriver.png", xysize=(256, 384), fit="contain"), portrait_idle)

# The professor already has a portrait on disk, so he uses it.
image side professor = At(Transform("images/characters/teacher.png", xysize=(256, 384), fit="contain"), portrait_idle)

# The two people whose stories the first free afternoon can open: the ramen chef
# near home, and Sim, who runs the photography club, Circle. Both portraits are already
# on disk, so unlike the three below they need no placeholder.
image side chef = At(Transform("images/characters/chef.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side sim = At(Transform("images/characters/sim.png", xysize=(256, 384), fit="contain"), portrait_idle)

# These three are drawn but not yet delivered. Drop the named file into
# images/characters/ and the picture replaces the label here with no other change:
#   clerk.png, timid_man.png, cheerful_woman.png
image side clerk = At(portrait_or_placeholder("clerk", "#4a4038", "STUDENT\nRELATIONS"), portrait_idle)
image side timid_man = At(portrait_or_placeholder("timid_man", "#4b4a44", "TIMID MAN"), portrait_idle)
image side cheerful_woman = At(portrait_or_placeholder("cheerful_woman", "#6b5a4a", "CHEERFUL\nWOMAN"), portrait_idle)

# --- PORTRAITS THAT STAY, AND PORTRAITS THAT LEAVE ---
#
# The say screen draws the speaker's portrait itself, and only for as long as that
# person is the one talking. The instant somebody else has a line the picture is
# gone in a single frame, and there is nothing left on screen to fade.
#
# So every name with a "side" picture above also has a "_standing" twin: the same
# drawing, in the same place on the screen, except it is an ordinary displayable
# instead of part of the say screen. Swapping one for the other changes nothing
# you can see, and it buys you show and hide, which take transitions.
#
# To have somebody leave in the middle of a scene:
#
#     father "You still have school tomorrow."
#     show father_standing                  # takes over from the say screen
#     mc "(He goes to bed.)"
#     hide father_standing with dissolve    # he fades out
#
# To have somebody arrive before they speak, show them with a transition:
#
#     show mother_standing with dissolve
#
# The assistant and the sister keep their ConditionSwitch, so their standing twin
# follows the shy and the running drawings on its own. Nothing else per character.
transform standing:
    xalign 0.5
    ypos config.screen_height
    yanchor 1.0
    zoom 1.8

init python:
    for _standing_tag in (
        "assistant", "veteran", "security", "security2", "mother", "father",
        "sister", "taxi_driver", "professor", "chef", "sim",
        "clerk", "timid_man", "cheerful_woman",
    ):
        renpy.image(_standing_tag + "_standing", At("side " + _standing_tag, standing))
    del _standing_tag

define config.speaking_attribute = "talking"

# --- HOW TO GIVE SOMEONE A MOUTH ---
# Nothing above needs touching. To upgrade one character:
#
#   1. In images/characters/, save a second copy of their portrait with the mouth
#      open, named after the first: assistant.png -> assistant_talk.png. Same
#      canvas size, same head position. Only the mouth should move.
#
#   2. Add a single line here, naming that character:
#
#          image side assistant talking = At(Transform("images/characters/assistant_talk.png", xysize=(256, 384), fit="contain"), portrait_talk)
#
#      From then on he bobs faster while he talks and sits still when he stops.
#      veteran, chef, orson, sim, aya and so on each need their own line, and each
#      one is independent, so you can add them as slowly as you like.
#
#   3. If you would rather the mouth visibly open and close instead of just
#      bobbing, swap that line for this loop, which alternates the two pictures
#      roughly four times a second:
#
#          image side assistant talking:
#              Transform("images/characters/assistant.png", xysize=(256, 384), fit="contain")
#              pause 0.12
#              Transform("images/characters/assistant_talk.png", xysize=(256, 384), fit="contain")
#              pause 0.12
#              repeat

# Dream characters
define robed_figure = Character("Robed Figure", color="#000000", callback=type_sound)

# "doctor" is kept for the day the room finally speaks to him as a person. Until
# then, the voices that bleed into the dream are deliberately written as plain
# narration: no name, no portrait, so they arrive as sentences he overhears
# rather than as somebody talking to him.
define doctor = Character("Doctor", color="#ff4444", callback=type_sound)

# Narration (a bare "quoted line") goes through the built-in narrator, so it needs
# the click as well. Declaring it here stops 00definitions.rpy from replacing it.
define narrator = Character(None, kind=adv, what_style="say_thought", callback=type_sound)

# --- SCREENS: PHOTO MODE PREVIEW ---
# This is a basic skeleton for the photo mode you requested
screen photo_mode(bg_image):
    add bg_image
    
    # Simple camera frame overlay
    add "images/ui/camera_frame.png" align (0.5, 0.5)
    
    # Zoom/Pan controls could be added here
    textbutton "Take Photo" action Return(True) align (0.9, 0.9)
    textbutton "Exit" action Return(False) align (0.1, 0.9)

## The notice ##################################################################
##
## Two cards that run once, before the story does, on a black field that belongs
## to no scene in the game. Neither has a button, and both are modal, so there is
## nothing on screen to click: the card fades itself in, holds, and fades itself
## out, and only then does the screen hand control back. The two that follow are
## the parts the player does have to answer.

define notice_text_fiction = "Everything in this game is a work of fiction.\n\nAny resemblance to real people, living or dead, is coincidental. No character here is meant to represent anyone in real life."

define notice_text_choice = "Be mindful of your choices.\n\nEvery choice you make changes what happens next. Some of them cannot be taken back, and some of them will be remembered."

define notice_text_accept = "By continuing, you accept that this is a story.\n\nAnd that the story is listening."

# Each card fades itself up, holds long enough to be read, and fades itself back
# down. The timing lives in the transform, so the screen only has to wait out the
# total, which is 4.8 seconds. Change one and change the other to match.
transform notice_card:
    alpha 0.0
    linear 1.0 alpha 1.0
    pause 2.8
    linear 1.0 alpha 0.0

style notice_label is default:
    size gui.scale(13)
    color "#7d766a"
    kerning gui.scale(7)
    text_align 0.5

style notice_body is default:
    size gui.scale(22)
    color "#e6e1d8"
    text_align 0.5
    line_spacing gui.scale(11)
    kerning gui.scale(0.5)

style notice_meta is default:
    size gui.scale(12)
    color "#5a544b"
    kerning gui.scale(3)
    text_align 0.5

# Text only, no plate behind it: on black, colour is what tells the player where
# the cursor is, the same way it does on the menus. The label's own styling lives
# in the matching _text style, which is what a button's text looks for.
style notice_button is button:
    background None
    hover_background None
    padding (gui.scale(18), gui.scale(10))

style notice_button_text is button_text:
    size gui.scale(15)
    kerning gui.scale(5)
    idle_color "#8a8377"
    hover_color "#f4efe6"

screen notice_page(eyebrow, body, page):
    modal True

    # There is no button on this card, so there is nothing to click. When the
    # fade-out in notice_card finishes, the timer fires and the screen returns on
    # its own. The two numbers must stay in step with each other.
    timer 4.800 action Return()

    add Solid("#000000")

    vbox:
        at notice_card
        xalign 0.5
        yalign 0.5
        spacing gui.scale(26)

        text eyebrow style "notice_label" xalign 0.5
        add Solid("#3a352e") xysize (gui.scale(420), 1) xalign 0.5
        text body style "notice_body" xalign 0.5 xmaximum gui.scale(660)
        text page style "notice_meta" xalign 0.5

screen notice_confirm(question):
    modal True
    add Solid("#000000")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing gui.scale(30)

        text "BEFORE YOU BEGIN" style "notice_label" xalign 0.5
        add Solid("#3a352e") xysize (gui.scale(420), 1) xalign 0.5
        text question style "notice_body" xalign 0.5 xmaximum gui.scale(660)
        textbutton "I accept" action Return(True) style "notice_button" xalign 0.5

screen notice_name():
    modal True
    add Solid("#000000")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing gui.scale(28)

        text "ONE LAST THING" style "notice_label" xalign 0.5
        add Solid("#3a352e") xysize (gui.scale(420), 1) xalign 0.5
        text "What should they call you?" style "notice_body" xalign 0.5

        input:
            value VariableInputValue("player_name", returnable=True)
            length 12
            exclude "{}[]"
            size gui.scale(30)
            pixel_width gui.scale(360)
            xalign 0.5

        # Both branches draw the same two rows, so the layout never shifts as the
        # player types. Only the hint wording changes, and whether Begin responds.
        if player_name.strip():
            text "up to twelve characters" style "notice_meta" xalign 0.5
            textbutton "Begin" action Return(True) style "notice_button" xalign 0.5
        else:
            text "type a name to begin" style "notice_meta" xalign 0.5
            textbutton "Begin" action Return(True) style "notice_button" xalign 0.5 sensitive False

# The one-time hints. They are all drawn by the same card, so the only thing each
# caller supplies is the wording, and none of them ever runs twice.
define hint_text_money = "Make sure to check your cash in your bag, so you know you have enough for the things you need."

define hint_text_bag = "Make sure to check the items in your bag. It might be useful."

# The first point he ever earns. It names the three pillars and says where they
# come from, and deliberately says nothing about where they lead: the locked
# answer and the person who remembers are better met as surprises than explained
# here. Everything past this sentence is left for the player to find.
define hint_text_attribute = "Something you chose just left a mark on you. You are becoming three things at once: Insight, Grace and Nerve.\n\nThey only move when a decision actually costs you something, not every time.\n\nYou cannot see where they are taking you yet. Some doors open only for the person you have grown into, and some people will remember how you answered."

# The first afternoon he is allowed to spend. It names the thing he has just been
# handed and says what it is for, without listing where he can go: the places are
# meant to be found, and the ones that matter will announce themselves with a
# mark of their own. Called from the after-school fork, once, after the game has
# already taken him somewhere.
define hint_text_after_school = "The lectures are done, and the rest of the day is yours. This is what an afternoon in Japan looks like for you now.\n\nYou get one of them a day. You spend it on a person, a place, or a way home, and the day ends either way.\n\nNobody will tell you which one to pick. The ones with something waiting for you will let you know. Where you go is how you get to know this city, and the people in it get to know you back."


# A note that stops the game for a beat: the scene dims, a short card fades up
# over it, and both fade away again once Okay is pressed. Not called from the
# script itself: spend_money() and add_item() call it, each guarded so it only
# ever fires once.
#
# Swapping the "at" transform on a screen displayable makes Ren'Py rebuild it,
# which restarts the ATL from the first frame, so the out-fade always plays from
# the solid state. The timer at the bottom must outlast the longest out-fade.
transform hint_dim_in:
    alpha 0.0
    linear 0.5 alpha 0.55

transform hint_dim_out:
    alpha 0.55
    linear 0.4 alpha 0.0

transform hint_card_in:
    alpha 0.0
    yoffset gui.scale(14)
    linear 0.5 alpha 1.0 yoffset 0

transform hint_card_out:
    alpha 1.0
    yoffset 0
    linear 0.4 alpha 0.0 yoffset gui.scale(-8)

screen hint_card(eyebrow, body):
    modal True

    default hiding = False

    # A translucent black, not an opaque one: the room is still back there,
    # just quieter for a moment.
    if hiding:
        add Solid("#000000") at hint_dim_out
    else:
        add Solid("#000000") at hint_dim_in

    frame:
        at (hint_card_out if hiding else hint_card_in)
        background Solid("#1c1b18e6")
        padding (gui.scale(46), gui.scale(38))
        xalign 0.5
        yalign 0.5

        vbox:
            spacing gui.scale(24)
            xalign 0.5

            text eyebrow style "notice_label" xalign 0.5
            add Solid("#3a352e") xysize (gui.scale(360), 1) xalign 0.5
            text body style "notice_body" xalign 0.5 xmaximum gui.scale(520)
            textbutton "Okay" action SetScreenVariable("hiding", True) style "notice_button" xalign 0.5 sensitive (not hiding)

    if hiding:
        timer 0.420 action Return()

# The attribute gain screen slows the motion down and gives the earned stat a
# cleaner route: it appears in the middle, then glides into its own orb and
# stays there, breathing in the correct place.
transform attribute_gain_cluster_in:
    alpha 0.0
    yoffset gui.scale(12)
    linear 0.28 alpha 1.0
    ease 0.52 yoffset 0

transform attribute_gain_cluster_out:
    alpha 1.0
    yoffset 0
    ease 0.44 alpha 0.0 yoffset gui.scale(-10)

transform attribute_gain_title_in:
    alpha 0.0
    xoffset gui.scale(-48)
    pause 1.12
    ease 0.52 alpha 1.0 xoffset 0

transform attribute_gain_bar_in:
    alpha 0.0
    yoffset gui.scale(12)
    pause 1.38
    ease 0.44 alpha 1.0 yoffset 0

transform attribute_gain_orb_idle:
    alpha 0.70
    zoom 1.0
    block:
        linear 1.85 alpha 0.84 zoom 1.015
        linear 1.85 alpha 0.68 zoom 0.992
        repeat

transform attribute_gain_target_glow:
    alpha 0.10
    zoom 0.96
    pause 1.08
    block:
        linear 1.25 alpha 0.34 zoom 1.05
        linear 1.25 alpha 0.12 zoom 0.98
        repeat

transform attribute_gain_focus_to_grace:
    alpha 0.0
    zoom 0.68
    linear 0.26 alpha 1.0 zoom 1.06
    ease 0.22 zoom 1.0
    pause 0.48
    ease 0.82 xoffset gui.scale(-34) yoffset gui.scale(-104) zoom 0.82
    block:
        linear 1.75 zoom 0.85
        linear 1.75 zoom 0.81
        repeat

transform attribute_gain_focus_to_insight:
    alpha 0.0
    zoom 0.68
    linear 0.26 alpha 1.0 zoom 1.06
    ease 0.22 zoom 1.0
    pause 0.48
    ease 0.82 xoffset gui.scale(-236) yoffset gui.scale(78) zoom 0.80
    block:
        linear 1.75 zoom 0.83
        linear 1.75 zoom 0.79
        repeat

transform attribute_gain_focus_to_nerve:
    alpha 0.0
    zoom 0.68
    linear 0.26 alpha 1.0 zoom 1.06
    ease 0.22 zoom 1.0
    pause 0.48
    ease 0.82 xoffset gui.scale(182) yoffset gui.scale(78) zoom 0.80
    block:
        linear 1.75 zoom 0.83
        linear 1.75 zoom 0.79
        repeat

transform attribute_gain_focus_flash:
    alpha 0.78
    block:
        linear 0.82 alpha 1.0
        linear 0.82 alpha 0.76
        repeat

style attribute_gain_title is default:
    size gui.scale(50)
    color "#eef8ff"
    italic True
    kerning gui.scale(1)

style attribute_gain_title_pop is default:
    size gui.scale(70)
    color "#ffffff"
    italic True
    kerning gui.scale(1)

style attribute_gain_name is default:
    size gui.scale(34)
    color "#f4efe6"
    italic True
    kerning gui.scale(1)
    text_align 0.5

style attribute_gain_amount is default:
    size gui.scale(104)
    color "#ffffff"
    italic True
    text_align 0.5

style attribute_gain_plus is default:
    size gui.scale(23)
    color "#f4efe6"
    kerning gui.scale(2)
    text_align 0.5

style attribute_gain_rank is default:
    size gui.scale(18)
    color "#ebe5da"
    kerning gui.scale(3)
    text_align 0.5

style attribute_gain_mini is default:
    size gui.scale(23)
    color "#dcd6cb"
    italic True
    text_align 0.5

screen attribute_gain_card(attribute_id, amount, rank_up=False):
    modal True

    default hiding = False

    # `rank_up` is True when this gain pushed the attribute over a threshold, and
    # all it changes is the headline and the weight of the moment. Passing it in
    # rather than working it out here keeps the card a view of a decision that has
    # already been made, which is what section 9.7 of the spec asks for.
    $ current_total = attribute_total_text(attribute_id)
    $ amount_text = format_points(amount)
    $ current_rank = attribute_rank(attribute_id)
    $ current_rank_name = attribute_rank_name(attribute_id)
    $ current_name = attribute_name(attribute_id)
    $ current_blurb = attribute_blurb(attribute_id)
    $ active_color = attribute_defs[attribute_id]["color"]
    $ active_soft = attribute_defs[attribute_id]["color_soft"]
    $ headline = "RANK" if rank_up else "ATTRIBUTE"

    if hiding:
        add Solid("#000000") at hint_dim_out
    else:
        add Solid("#000000") at hint_dim_in

    fixed:
        at (attribute_gain_cluster_out if hiding else attribute_gain_cluster_in)
        xalign 0.5
        yalign 0.5
        xmaximum gui.scale(1040)
        ymaximum gui.scale(600)

        # Rings and the core triangle.
        text "○" xpos gui.scale(290) ypos gui.scale(4) size gui.scale(386) color "#ffffff10"
        text "○" xpos gui.scale(108) ypos gui.scale(190) size gui.scale(336) color "#ffffff0c"
        text "○" xpos gui.scale(520) ypos gui.scale(190) size gui.scale(336) color "#ffffff0c"

        text "●" xpos gui.scale(332) ypos gui.scale(42) size gui.scale(308) color attribute_defs["grace"]["color_soft"] at attribute_gain_orb_idle
        text "●" xpos gui.scale(138) ypos gui.scale(232) size gui.scale(292) color attribute_defs["insight"]["color_soft"] at attribute_gain_orb_idle
        text "●" xpos gui.scale(550) ypos gui.scale(232) size gui.scale(292) color attribute_defs["nerve"]["color_soft"] at attribute_gain_orb_idle
        text "△" xpos gui.scale(426) ypos gui.scale(212) size gui.scale(136) color "#f7fbffcc"

        if attribute_id == "grace":
            text "●" xpos gui.scale(332) ypos gui.scale(42) size gui.scale(308) color active_soft at attribute_gain_target_glow
        elif attribute_id == "insight":
            text "●" xpos gui.scale(138) ypos gui.scale(232) size gui.scale(292) color active_soft at attribute_gain_target_glow
        else:
            text "●" xpos gui.scale(550) ypos gui.scale(232) size gui.scale(292) color active_soft at attribute_gain_target_glow

        # Start in the middle, then ease into the corresponding orb.
        if attribute_id == "grace":
            fixed:
                xalign 0.5
                yalign 0.5
                xmaximum gui.scale(260)
                ymaximum gui.scale(180)
                at attribute_gain_focus_to_grace

                vbox:
                    xalign 0.5
                    yalign 0.5
                    spacing gui.scale(-8)

                    text current_name style "attribute_gain_name" xalign 0.5 color active_color at attribute_gain_focus_flash
                    text "[current_total]" style "attribute_gain_amount" xalign 0.5 color active_color at attribute_gain_focus_flash
                    text "+[amount_text]" style "attribute_gain_plus" xalign 0.5

        elif attribute_id == "insight":
            fixed:
                xalign 0.5
                yalign 0.5
                xmaximum gui.scale(260)
                ymaximum gui.scale(180)
                at attribute_gain_focus_to_insight

                vbox:
                    xalign 0.5
                    yalign 0.5
                    spacing gui.scale(-8)

                    text current_name style "attribute_gain_name" xalign 0.5 color active_color at attribute_gain_focus_flash
                    text "[current_total]" style "attribute_gain_amount" xalign 0.5 color active_color at attribute_gain_focus_flash
                    text "+[amount_text]" style "attribute_gain_plus" xalign 0.5

        else:
            fixed:
                xalign 0.5
                yalign 0.5
                xmaximum gui.scale(260)
                ymaximum gui.scale(180)
                at attribute_gain_focus_to_nerve

                vbox:
                    xalign 0.5
                    yalign 0.5
                    spacing gui.scale(-8)

                    text current_name style "attribute_gain_name" xalign 0.5 color active_color at attribute_gain_focus_flash
                    text "[current_total]" style "attribute_gain_amount" xalign 0.5 color active_color at attribute_gain_focus_flash
                    text "+[amount_text]" style "attribute_gain_plus" xalign 0.5

        # The title waits until the move has already started.
        vbox:
            at attribute_gain_title_in
            xpos gui.scale(30)
            ypos gui.scale(82)
            spacing gui.scale(-18)

            text headline style "attribute_gain_title"
            text "UP!" style "attribute_gain_title_pop" color active_color

        frame:
            at attribute_gain_bar_in
            background Solid("#000000dc")
            padding (gui.scale(22), gui.scale(11))
            xalign 0.5
            ypos gui.scale(462)

            text current_blurb style "notice_body" color "#eef8ff" size gui.scale(20) xalign 0.5

        frame:
            at attribute_gain_bar_in
            background Solid("#000000ee")
            padding (gui.scale(24), gui.scale(8))
            xalign 0.5
            ypos gui.scale(516)

            text "RANK [current_rank]  [current_rank_name.upper()]" style "attribute_gain_rank" xalign 0.5

        # Keep the trio readable, but do not duplicate the moving stat text.
        if attribute_id != "grace":
            text "Grace [attribute_total_text(\"grace\")]" xpos gui.scale(408) ypos gui.scale(162) xsize gui.scale(170) style "attribute_gain_mini" color "#f4efe6"

        if attribute_id != "insight":
            text "Insight [attribute_total_text(\"insight\")]" xpos gui.scale(198) ypos gui.scale(356) xsize gui.scale(180) style "attribute_gain_mini" color "#f4efe6"

        if attribute_id != "nerve":
            text "Nerve [attribute_total_text(\"nerve\")]" xpos gui.scale(620) ypos gui.scale(356) xsize gui.scale(180) style "attribute_gain_mini" color "#f4efe6"

        textbutton "Okay" action SetScreenVariable("hiding", True) style "notice_button" xalign 0.5 yalign 1.0 yoffset gui.scale(10) sensitive (not hiding)

    # The landing fire is on a timer rather than a second play_sfx call, so it
    # stays locked to the motion: 1.70s is the moment the stat finishes its
    # travel and settles into its orb. Retime the transforms and this beat has to
    # be moved with them.
    timer 1.70 action Play("sfx", "audio/SFX/attribute_land.wav")

    if hiding:
        timer 0.440 action Return()

# --- THE QUIET GAIN, AND THE ORB CLUSTER ---
#
# Two pieces of feedback that run during play rather than stopping it.
#
# The chip is what half a point looks like. It appears over the top of the
# scene, says which attribute moved and by how much, and takes itself away
# again. It borrows the shape of renpy's own notify screen, `on hide` included,
# because that is the one part of the engine that already does exactly this.
#
# The cluster is the three orbs in the corner of the screen: the same three
# circles the gain card draws full size, only small. Each one starts almost
# transparent and grows steadily more solid as that attribute fills, so the
# corner answers "how am I doing" without ever printing a number.

transform attribute_tick_appear:
    on show:
        alpha 0.0
        yoffset gui.scale(-10)
        linear 0.26 alpha 1.0 yoffset 0
    on hide:
        ease 0.40 alpha 0.0 yoffset gui.scale(-8)

screen attribute_tick(attribute_id, points):
    zorder 95

    $ tick_name = attribute_name(attribute_id)
    $ tick_color = attribute_color(attribute_id)
    $ tick_points = "+" + format_points(points)

    frame:
        at attribute_tick_appear

        # Directly under the orbs, not under the dialogue. The number belongs to
        # the corner it just changed, so it reads as that orb's own readout, and
        # it stays clear of the line the player is in the middle of reading.
        xalign 1.0
        yalign 0.0
        xoffset gui.scale(-28)
        yoffset gui.scale(74)

        background Solid("#0e0d0ce0")
        padding (gui.scale(26), gui.scale(8), gui.scale(26), gui.scale(8))

        hbox:
            spacing gui.scale(12)

            text tick_name style "attribute_tick_text" color tick_color
            text tick_points style "attribute_tick_text" color tick_color

    # Long enough to read twice, short enough not to become furniture.
    timer 2.10 action Hide("attribute_tick")

style attribute_tick_text is default:
    size gui.scale(22)
    italic True
    kerning gui.scale(1)

# The other half of a decision: not a number going up, but a person deciding
# something about him. It sits up top, which is where the tick chip used to live,
# so the two never share a corner. A stat move reads next to the orbs; a memory
# reads over the scene.
transform memory_notice_appear:
    on show:
        alpha 0.0
        yoffset gui.scale(-8)
        linear 0.30 alpha 1.0 yoffset 0
    on hide:
        ease 0.45 alpha 0.0 yoffset gui.scale(-6)

screen memory_notice(who):
    zorder 96

    frame:
        at memory_notice_appear

        xalign 0.5
        yalign 0.0
        yoffset gui.scale(88)

        background Solid("#0e0d0cd8")
        padding (gui.scale(24), gui.scale(7), gui.scale(24), gui.scale(7))

        text "([who] will remember that)" style "memory_notice_text"

    timer 2.60 action Hide("memory_notice")

style memory_notice_text is default:
    size gui.scale(21)
    italic True
    color gui.accent_color
    kerning gui.scale(1)

transform attribute_hud_appear:
    alpha 0.0
    linear 0.55 alpha 1.0

# The cluster breathes as a single unit rather than orb by orb, so a glance at
# the corner reads it as one object instead of three competing ones.
transform attribute_hud_breathe:
    block:
        ease 2.40 zoom 1.035
        ease 2.40 zoom 1.0
        repeat

screen attribute_hud():
    zorder 90

    # The game menu suppresses overlay screens on its own, so the only case left
    # to guard is the very start of the game, before he is in the world.
    if show_attribute_hud and not main_menu:

        hbox:
            at attribute_hud_appear

            xalign 1.0
            yalign 0.0
            xoffset gui.scale(-28)
            yoffset gui.scale(24)
            spacing gui.scale(6)

            for orb_id in attribute_order:

                fixed:
                    xsize gui.scale(44)
                    ysize gui.scale(44)
                    at attribute_hud_breathe

                    # The fill first, then its outline on top, so the ring is
                    # never swallowed by a nearly-opaque orb.
                    text "●":
                        xalign 0.5
                        yalign 0.5
                        size gui.scale(36)
                        color attribute_color_alpha(orb_id, attribute_orb_alpha(orb_id))

                    text "○":
                        xalign 0.5
                        yalign 0.5
                        size gui.scale(44)
                        color "#ffffff2b"

# --- START LABEL ---
label start:

    # Before the story, the two notices. Neither can be clicked past: each card
    # fades itself in and out and then returns on its own timer, so a new player
    # reads both whether they mean to or not. They only ever run here, which is
    # to say only on a new game. A loaded save resumes where it was.
    call screen notice_page("DISCLAIMER", notice_text_fiction, "1 / 2")
    call screen notice_page("BEFORE YOU BEGIN", notice_text_choice, "2 / 2")

    # Then the one thing the player has to answer for themselves.
    call screen notice_confirm(notice_text_accept)

    # And the name the rest of the cast will use. It is asked once and then it is
    # his: every line of his own carries it in the name box, and the family use it
    # in the scenes where somebody would actually say a name out loud.
    #
    # The loop exists because an empty name box reads as a bug the first time
    # somebody speaks to him, so this one field is not allowed to stay blank.
    while player_name.strip() == "":
        call screen notice_name()
    $ player_name = player_name.strip()

    # Initializing game state
    $ japanese_fluency = 0

    # Every yen he owns, converted to cash before he boarded. It has to cover the
    # ride to the host family and a first meal, and it is not a lot. The whole
    # wallet mechanic hangs off how thin this is.
    $ money = 30000

    # What he lands with. The phone is in his pocket from the first scene, and it
    # is the first thing in the Bag that turns out to be useless.
    $ inventory = ["phone"]

    # The typewriter effect is driven by the *player preference* text_cps.
    # config.default_text_cps only applies to brand-new installs, so existing
    # saves kept the old "instant text" setting. Forcing it here guarantees the
    # letter-by-letter effect (and the type.wav clicking) on every playthrough.
    $ preferences.text_cps = 30

    # Jump to the prologue
    jump prologue

label prologue:
    # The title theme is still playing when the story begins. Until now the
    # screen went black in a single frame and the dream track replaced the menu
    # track in the same instant, so the first line arrived as a cut. Here the
    # music and the picture go down together over the same two seconds, the black
    # is held for a beat, and the story comes up on the far side of it with its
    # own track already fading in underneath.
    #
    # The three screens before this one are already solid black, so the sound is
    # the only thing the player actually sees change. That is the point: the room
    # goes quiet, holds, and then begins.
    stop music fadeout 2.0
    scene black with Fade(2.0, 1.0, 0.0)
    #DISABLED FOR NOW# play music "audio/Music/dream sequence 1 (short loop).wav" fadein 2.0#
    play music "audio/SFX/airplane.mp3" fadein 2.0
    
    "Whoah that is one long flight."
    "I barely slept for any of it."
    "But I made it. I'm almost here."
    "Tokyo, Japan."
    "I came here thanks to a foreign exchange student program in our university."
    
    
    "I should be more excited. Host family, a new university, a new language, a new life."
    "But right now, everything feels a little... fuzzy."
    "I remember filling out the application. Sending the forms. Waiting for months."
    "I remember being thrilled when I got accepted. My friends said I was brave."
    "But... what exactly made me choose Japan?"
    "I must've had a reason. I know I did."
    "But thinking back now... it's like the memory is just out of reach."
    "Like trying to recall a dream after waking up."
    "Maybe it's just the jet lag. Or the nerves. Or being in a completely new place alone."

    
    # The wallet, established before he has spent a single yen of it.
    "I have thirty thousand yen, in cash, folded into the back of my wallet."
    "That's all of it. But should be enough to get me started with my life."
    "Thirty thousand yen to start a whole new life..."
    "No, It's not enough. It's nowhere near enough."
    "I'll have to figure something out. Maybe find a part time job or something."
    "I have to. I cannot rely on people to take care of me all the time."
    
    # Foreshadowing glitch - the first crack in the simulation
    show hospital_flash onlayer overlay at truecenter:
        alpha 0.0
        linear 0.1 alpha 0.3
        linear 0.1 alpha 0.0
    
    "Initiating..."
    
    "I should focus on what's ahead."
    "A door, and a family I have only ever seen in photographs."
    
    stop music fadeout 1.0
    jump airport_arrival

label airport_arrival:
    # The terminal: a calm track riding over the murmur of the crowd. The ambience
    # is on its own channel so it layers underneath the music, and both loop until
    # he leaves the building (see label end_airport).
    #
    # Both start before the picture does. The prologue went out on black, and the
    # airport comes up out of that black over the same two seconds the sound takes
    # to rise, so the room is already audible by the time it is visible. It used
    # to arrive on one frame, which made the end of the flight read as a cut.
    play music "audio/Music/airportscene.mp3" fadein 2.0
    play ambient "audio/SFX/airport.ogg" fadein 2.0
    scene bg_airport with Fade(0.0, 0.0, 2.0)

    # The cluster comes on here rather than at `start`, because this is the first
    # moment he is actually standing in the world. The two disclaimer cards and
    # the voice on the plane are not the game yet, and three progress orbs over
    # them would be answering a question nobody has asked.
    $ show_attribute_hud = True

    "Finally, Tokyo."
    
    "Alright, I made it all the way here..."
    "But I have no idea where I'm going."
    "Let me check my phone for the Maps app."
    "..."
    "What? No reception?"
    "I guess I can't use my phone right now."
    "Maybe I should ask someone around here for directions."

label airport_exploration:
    menu:
        "Ask the Security Guard":
            jump talk_security
        "Ask the Timid Man":
            jump talk_timid_man
        "Ask the Cheerful Woman":
            jump talk_cheerful_woman
        "Ask the Airport Assistant":
            jump talk_assistant
        "Ask the Veteran Assistant" if has_pamphlet or (talked_to_security and talked_to_man1 and talked_to_npc2):
            jump talk_veteran_assistant
        "Check the Information Boards":
            jump check_boards
        "Look at the Plants":
            jump look_plants

label talk_security:
    # There are two of them on this post and it depends which one is standing
    # there when he walks up, so the shift swaps back and forth. Ask twice and
    # you get told off twice, by two different people, in two different ways.
    if security_index % 2 == 0:
        security "ちょっと、下がってください。"
        mc "(Huh? I'm just trying to ask something...)"
        security "業務中です。話しかけないでください。"
        mc "(Did I do something wrong? I just showed my smartphone to him...)"
        security "……"
        mc "(He didn't even *look* at it... Is this guy part robot or something?)"
    else:
        security2 "……何か？"
        mc "(She looked at me the way you look at a bug on a windshield.)"
        security2 "ここは立入制限区域です。この先は関係者以外通れません。"
        mc "(Restricted area. I'm not trying to go anywhere. I just want the exit.)"
        mc "Excuse me. Which way is—"
        security2 "総合案内所はあちらです。"
        mc "(She pointed without looking. Somewhere behind me. Possibly at the whole building.)"
        security2 "私は持ち場を離れられません。他の人に聞いてください。"
        mc "(I understood about four words of that, and all four were 'go away'.)"
        security2 "それ以上は業務妨害とみなします。"
        mc "(Okay. Okay. I'm going.)"

    $ security_index += 1
    $ talked_to_security = True

    # The guard cannot be won over, so the only thing this fork decides is what
    # kind of person he is about being dismissed. None of the three gets him
    # anywhere and none of them pays: the airport is not a turning point, it is a
    # man walking up to strangers and being brushed off, so the fork is character
    # rather than progress. He is not being graded on results yet.
    #
    # What he does choose is what he says, and he only gets to say it once. The
    # hub lets him walk back here, and on the second visit the answer he already
    # gave is the answer that comes out of his mouth.
    $ prior_answer = remembered_choice("security")

    if prior_answer == "bow":
        jump answer_security_bow
    elif prior_answer == "press":
        jump answer_security_press
    elif prior_answer == "watch":
        jump answer_security_watch

    menu:
        "Apologise.":
            $ remember_choice("security", "bow")
            jump answer_security_bow
        "Point at the address again.":
            $ remember_choice("security", "press")
            jump answer_security_press
        "Watch where everyone else goes.":
            $ remember_choice("security", "watch")
            jump answer_security_watch

label answer_security_bow:
    mc "Sumimasen. Sumimasen."
    mc "(I bowed. I have no idea why I bowed. My body just did it.)"
    mc "(Maybe I should ask someone who isn't radiating pure stress.)"
    jump airport_exploration

label answer_security_press:
    mc "Excuse me. 中野3丁目. Please."
    mc "(They looked at the phone. They looked at me. They looked at the phone again, and then away.)"
    mc "(That was not a no. It was a wall. There is a difference and I just found it.)"
    mc "(Maybe I should ask someone who isn't radiating pure stress.)"
    jump airport_exploration

label answer_security_watch:
    mc "(Nevermind. Everyone in this building is walking somewhere, someone will tell me more than they will.)"
    mc "(Maybe I should ask someone who isn't radiating pure stress.)"
    jump airport_exploration

label talk_timid_man:
    timid_man "話しかけないでくれ！"
    timid_man "忙しくて雑談してる暇はないんだ。"
    mc "(What...? I have no idea what they just said.)"
    $ talked_to_man1 = True

    # Same shape as the guard: three ways to be turned away, no points, and the
    # one he picks is the one he is stuck with if he comes back.
    $ prior_answer = remembered_choice("timid_man")

    if prior_answer == "again":
        jump answer_timid_again
    elif prior_answer == "aside":
        jump answer_timid_aside
    elif prior_answer == "listen":
        jump answer_timid_listen

    menu:
        "Ask again, slower.":
            $ remember_choice("timid_man", "again")
            jump answer_timid_again
        "Step aside.":
            $ remember_choice("timid_man", "aside")
            jump answer_timid_aside
        "Let him go.":
            $ remember_choice("timid_man", "listen")
            jump answer_timid_listen

label answer_timid_again:
    mc "Ah... sorry. Um. Exit?"
    mc "(He said the same thing again. Exactly the same words, at exactly the same speed.)"
    mc "(It is not that he can't understand me. It's that I'm not a question he has time for.)"
    mc "(I guess he doesn't want to talk...)"
    jump airport_exploration

label answer_timid_aside:
    mc "Ah - sorry. Sorry."
    mc "(I guess he doesn't want to talk...)"
    jump airport_exploration

label answer_timid_listen:
    mc "(...いそがしい.)"
    mc "(I know that one. It's on the sign in the arrivals hall. It means busy.)"
    mc "(He isn't angry at me. He's just busy.)"
    mc "(That's the first thing I've properly understood since I landed, and it was a man telling me to move.)"
    mc "(I guess he doesn't want to talk...)"
    jump airport_exploration

label talk_cheerful_woman:
    cheerful_woman "こんにちは！日本へようこそ！"
    cheerful_woman "それでは、失礼いします！幸せになりますように！"
    mc "(Uhh... she said something about... sushi?)"
    mc "(Wait. Did she just recommend a sushi restaurant?)"
    mc "(Or was that a blessing for my sushi-related future?)"

    $ talked_to_npc2 = True

    # She is the one warm face in the terminal, and the fork is only about how
    # much he is willing to give back. No points, and the same answer twice.
    $ prior_answer = remembered_choice("cheerful_woman")

    if prior_answer == "smile":
        jump answer_woman_smile
    elif prior_answer == "echo":
        jump answer_woman_echo

    menu:
        "Smile and bow.":
            $ remember_choice("cheerful_woman", "smile")
            jump answer_woman_smile
        "Try one of her words.":
            $ remember_choice("cheerful_woman", "echo")
            jump answer_woman_echo

label answer_woman_smile:
    mc "(She's the first person in this country who has smiled at me.)"
    cheerful_woman "あら！ がんばってね！"
    jump airport_exploration

label answer_woman_echo:
    mc "Ah... すし?"
    cheerful_woman "え？ ……ああ！ すし！ そうそう！ おいしいよ、すし！"
    mc "(Whatever I just said, it landed. She's laughing, and it isn't at me.)"
    jump airport_exploration

label talk_assistant:
    if not (talked_to_security and talked_to_man1 and talked_to_npc2):
        assistant "いらっしゃいませ～。ようこそ。"
        jump airport_exploration
    
    assistant "いらっしゃいませ～。ようこそ。"
    mc "Hi! Um... Can you help me?"
    # The moment she realises she has to do this in English. She wears the second
    # drawing from here until the address is sorted out, one way or the other.
    $ assistant_shy = True
    assistant "えっ…えいご…すこしだけ…"
    assistant "えいごのスタッフは…いまやすみ…"
    assistant "*muttering to herself* English staff... break time now..."
    mc "...Okay... Umm, I need to find this place."
    assistant "アドレス？うーん… show... me?"
    
    # The pamphlet fork hands him the thing the whole second act runs on, but it
    # is a transaction rather than a turning point, so it pays nothing. It is
    # also the one answer here he has a reason to give twice: if he asks a second
    # time he asks the same way, and the pamphlet is already in his bag.
    $ prior_answer = remembered_choice("assistant")

    if prior_answer == "ask":
        jump answer_assistant_ask
    elif prior_answer == "nevermind":
        jump answer_assistant_nevermind

    menu:
        "Show her the address.":
            $ remember_choice("assistant", "ask")
            jump answer_assistant_ask
        "Never mind.":
            $ remember_choice("assistant", "nevermind")
            jump answer_assistant_nevermind

label answer_assistant_ask:
    mc "*Shows address on phone.* Can you tell me how to go here?"
    # She cannot find the English for it and it starts to show. The second drawing
    # stays up until the pamphlet is in his hands and she has recovered.
    $ assistant_shy = True
    assistant "あー、これはね…でんしゃ？トレイン？"
    assistant "にっぽりえきから。。。えっと。。。ちょっとまってください。"
    assistant "*Takes out a japanese map full of arrows and kanji letters.*"
    $ has_pamphlet = True
    $ add_item("pamphlet")
    mc "Uh... this is... kind of amazing but also terrifying."
    $ assistant_shy = False
    assistant "No problem, Good Luck! がんばってください！"
    mc "...Thanks. I'll try my best."
    jump airport_exploration

label answer_assistant_nevermind:
    mc "Nevermind, thanks anyway."
    $ assistant_shy = False
    jump airport_exploration

label talk_veteran_assistant:
    if not has_pamphlet:
        veteran "Oh dear, are you a bit lost?"
        veteran "If you find a pamphlet lying around, I can try to translate it for you!"
        mc "Pamphlet? I'll go look for one."
        jump airport_exploration

    veteran "Oh dear, are you a bit lost?"
    veteran "What is that in your hand?"
    veteran "Ah... A pamphlet"
    veteran "Let me have a look at that. These things are more puzzle than guide, huh?"
    mc "Yes, totally. I can't make sense of it."
    veteran "Okay then. You're headed to 中野3丁目, right?"
    mc "Yeah, that's the place."
    veteran "You've got two ways to get there. Train is cheaper, but a bit tricky. Taxi's simple, but pricey. Want details?"
    
    menu:
        "Tell me about the train.":
            veteran "Alright, here's the deal. First, buy a ticket before going in. You can't enter the platform without it."
            veteran "Then wait for the express train. Not the local one! Unless you enjoy long rides and sore feet."
            veteran "Follow the signs for the Keisei Line. It'll get you there in about 45 minutes."
            jump taxi_choice
        "No, I'm good. Thanks!":
            jump end_airport

label taxi_choice:
    veteran "Want me to explain the taxi option too, or are you ready to go?"
    menu:
        "Tell me about the taxi.":
            veteran "Just head outside and find the taxi stand. There's usually a line, so be patient."
            veteran "It might cost around ¥18,000, maybe more if traffic's bad. But it's the easiest route."
            veteran "Just show the driver your pamphlet. They'll handle the rest."
            jump end_airport
        "No, I'm good. Thanks!":
            jump end_airport

label check_boards:
    # Each visit scrolls to the next notice on the list, then wraps around, so the
    # board is never showing the same line twice in a row.
    $ board_line = board_messages[board_message_index]
    "The board flickers, then scrolls to the next notice."
    "[board_line]"
    $ board_message_index = (board_message_index + 1) % len(board_messages)
    jump airport_exploration

label look_plants:
    # The first plant is a nice plant. The tenth is a cry for help.
    $ plant_line = plant_dialogues[min(plant_index, len(plant_dialogues) - 1)]
    "[plant_line]"
    $ plant_index += 1
    jump airport_exploration

label end_airport:
    # Reached only from the veteran's branch, so it is the veteran who sees him off.
    veteran "Glad to help! Enjoy your trip, and welcome to Japan!"
    mc "...Thanks. I'll try my best. I hope I can get there."

    # He is out of the terminal, so the crowd and its music go with it.
    stop music fadeout 2.0
    stop ambient fadeout 2.0

    # And the building itself goes with it. A slow fade to black, a held beat, and
    # then the first real decision of the game arrives out of the dark.
    window hide
    scene black with Dissolve(1.5)
    pause 2.0

    jump travel_choice


################################################################################
## ACT TWO: GETTING HOME
################################################################################
##
## Two routes, one destination. He picks outside the terminal, the choice is
## recorded in travel_method, and both routes rejoin at label home_arrival, which
## reads travel_method and boarded_shinkansen to decide what kind of night he has
## had. The taxi is simple and expensive; the train is cheap and a small puzzle.

label travel_choice:
    # Still black from the airport fade, which is deliberate: he is out in the
    # night now, thinking, before we show him anything.
    "Outside, the Tokyo night air hits me all at once."
    "Warmer than I expected. Damp. Full of sounds I don't have names for."
    mc "(Okay. 中野3丁目. Somewhere out there in all of that.)"
    mc "(She said there were two ways. Cheap and confusing, or simple and expensive.)"

    menu:
        "Take the taxi.":
            jump taxi_warning
        "Take the train.":
            $ travel_method = "train"
            # The one award left in the first act, and the only decision in it
            # that changes what the rest of the game is like to play. It carries
            # the whole of the act's progression on its own, which is why it is
            # sized as a set-piece rather than a tick.
            $ reward_attributes_once("travel_route_attribute", [("insight", "large")])
            jump train_station


label taxi_warning:
    mc "(A taxi would take me all the way to the door.)"
    mc "(No transfers. No signs I can't read. No standing on the wrong platform in the dark.)"
    mc "(But eighteen thousand yen. That's more than half of everything I own.)"
    mc "(If I take the train, that money buys me food for a fortnight.)"
    mc "(...but only if I actually get there.)"
    mc "(So. Spend it and arrive safe, or risk getting lost and keep the money.)"

    menu:
        "Take the taxi anyway.":
            $ travel_method = "taxi"
            $ reward_attributes_once("travel_route_attribute", [("nerve", "large")])
            jump taxi_stand
        "Take the train instead.":
            $ travel_method = "train"
            $ reward_attributes_once("travel_route_attribute", [("insight", "large")])
            jump train_station


# --- THE TAXI ---
# The easy route. First-time-foreigner moments, a driver he cannot understand,
# and the tired monologue that puts him to sleep in the back seat.

label taxi_stand:
    scene bg_taxi_stand with walk_fade
    play music "audio/Music/taxi.mp3" fadein 1.5

    "The terminal doors slide open before I even touch them."
    mc "(They just... opened.)"
    mc "(I didn't push anything. I didn't press anything. They just knew I was there.)"
    mc "(Right. This is going to happen to me a lot, isn't it.)"

    "Outside, a row of taxis idles under the lights, engines ticking over."
    "A man in a white shirt and white gloves waves me toward the front of the line."
    mc "(...Gloves. He's wearing white gloves. To drive a car.)"
    mc "(Okay. Show him the pamphlet. That is the entire plan. Show him the pamphlet.)"

    "The taxi glides to a stop in front of me, and the rear door swings open on its own."
    mc "(The door opened. By itself.)"
    mc "(Is he getting out? No. He's still in the driver's seat. He's not even turned around.)"
    mc "(He pulled a lever and the door opened for me. From the front seat.)"
    mc "(That is the most impressive thing I have ever seen a car do.)"
    mc "(...I should get in. There are people behind me. Get in the car.)"

    scene bg_taxi_interior with walk_fade

    "*Climbs in and pulls the door shut.*"
    "The seats are spotless. There is lace over the headrests."
    mc "(Lace. There is lace. In a taxi.)"

    taxi_driver "お客様、どちらまで？"
    mc "(That's my cue.)"
    "*Hands the pamphlet over the seat.*"
    taxi_driver "中野3丁目ですね。かしこまりました。遠いですが、大丈夫でしょうか？"
    mc "(...I understood one word of that and it was 中野.)"
    mc "Ah, um... 中野3丁目... please?"
    taxi_driver "*laughs* Okay, okay. 中野3丁目. No problem."
    mc "(He laughed. I'm choosing to believe that was friendly.)"

    "The meter starts ticking and we pull away from the kerb."
    mc "(No ticket. No button. No card. It just... starts.)"
    mc "(Airport to 中野3丁目. I'd guessed about eighteen thousand for that.)"
    mc "(A confident guess, made by a man who has been awake for twenty hours.)"
    mc "(...Maybe it'll be less. Hopefully it'll be less.)"

    # The first time the game asks him what kind of foreigner he is going to be
    # about it. All three answers are about the same ten seconds of car, and none
    # of them pays: the taxi ride is a texture, not a turning point.
    menu:
        "Try the thank you again.":
            mc "Arigatou... gozaimasu."
            taxi_driver "お。日本語、上手ですね。"
            mc "(I don't know what that was, but it was warm, and he said it to the mirror rather than to me.)"
        "Ask what the meter is doing.":
            mc "Excuse me. The meter. Is it supposed to do that?"
            taxi_driver "Ah. Understand. 高いね。遠いから。"
            mc "(He caught two words of that and gave me four back. It was worth the asking.)"
        "Time the clicks.":
            mc "(Every twenty seconds, almost exactly. I'll know the rhythm of it by the time I get there.)"
            mc "(There is nothing else to do, so I am going to learn this city's arithmetic off a screen on a dashboard.)"

    "The city slides past the window in long wet streaks of light."
    "Buildings I've only seen in photographs. Signs I can't read. Vending machines on every corner, glowing like little aquariums."
    mc "(Vending machines. Everywhere. Every hundred metres, another one.)"
    mc "(Someone on the plane told me you can get hot coffee out of them. In a can. I thought he was joking.)"

    "I look at the little screen on the dashboard, because I cannot help myself."
    "*The meter reads 1,300.*"
    mc "(Thirteen hundred. We have been in this car for four minutes.)"

    "The driver says something and points out of my window. I nod and smile."
    mc "(No idea. I am going to nod and smile my way through this entire year.)"

    "*The meter clicks. I look again.*"
    mc "(Three thousand eight hundred.)"
    mc "(It clicks, and the number goes up. It clicks every twenty seconds or so. I have been timing it. There is nothing else to do.)"
    mc "(And it climbs while we sit at a red light. It goes up while we do absolutely nothing.)"
    mc "(Eighteen thousand. That guess was made before I understood anything about anything.)"

    "Half an hour later the roads get narrow and the lights get fewer."
    "He slows, checks a street sign, turns, and the city goes quiet behind us."
    "*The meter reads 9,200.*"
    mc "(Nine thousand two hundred. I have stopped doing the arithmetic properly and started doing it as a sigh.)"
    mc "(I'm so tired.)"
    mc "(Not sleepy tired. Tired behind the eyes. Tired in the shoulders.)"
    mc "(I've been awake for... I don't know how long. Two planes, three time zones, one whole ocean.)"

    mc "(And at the end of this ride there's a house with a family in it that has never met me.)"
    mc "(What if they don't like me?)"
    mc "(What if I get there and I can't say one useful sentence and we all stand in the hall looking at the floor?)"
    mc "(Should I act like a grown up? Serious. Polite. Careful. No mistakes.)"
    mc "(Or should I just... enjoy this? For once. Actually be in Japan, instead of surviving it.)"
    mc "(...)"
    mc "(I'll decide tomorrow.)"

    "*The meter ticks past 13,400. We are still not there.*"
    mc "(...)"

    mc "(My eyes feel so heavy.)"
    "*Leans head against the window.*"
    "I close my eyes, just for a minute."

    window hide
    scene black with Dissolve(1.5)
    pause 1.5
    scene bg_taxi_interior_final with Dissolve(1.5)

    "I wake up to the indicator ticking, and the car not moving."
    taxi_driver "着きましたよ。中野3丁目。"
    mc "(...中野. That was 中野. I'm awake.)"

    "The meter is still glowing. I finally let myself look at the number."
    "*The meter reads 17,600.*"
    mc "(Seventeen thousand six hundred.)"
    mc "(...Under. It came in under.)"
    mc "(I have never been so relieved to be wrong about a number in my life.)"

    # ¥500 for the first 1.096 km, then ¥100 for every 255 m, so a Tokyo meter
    # only ever lands on ¥500 plus a multiple of ¥100. That is why the fare here
    # is 17,600 and not something convenient like 18,000.
    $ spend_money(17600)
    mc "...Arigatou gozaimasu."
    "He says something cheerful, and the rear door opens by itself again."

    $ arrived_late = False
    $ boarded_shinkansen = False
    window hide
    scene black with Dissolve(2.5)
    stop music fadeout 2.5
    pause 0.5
    jump home_arrival


# --- THE TRAIN ---
# The cheap route, and the puzzle. The gate is the trap, the ticket machine is the
# lock, and the two signs above the platform are the last piece of the riddle.

label train_station:
    scene bg_station with walk_fade
    play music "audio/Music/train.mp3" fadein 1.5
    # The hubbub of the station itself, on its own channel so it sits under the
    # music rather than fighting it. It keeps playing through the platform and
    # stops when he gets on the train.
    play ambient "audio/SFX/stationambiance.mp3" fadein 1.5

    "The station is a wall of sound."
    "Announcements over the top of announcements. Turnstiles beeping. A train somewhere below, more felt than heard."
    "Above me a board of departure times scrolls through columns I can't read fast enough to follow."
    mc "(One thing at a time. The veteran said I need a ticket before I go in.)"
    mc "(And there. There's the gate.)"

    "A row of little metal flaps, opening and closing as people walk through like it's nothing at all."
    mc "(It looks so easy. Everybody else just... walks.)"
    mc "(Is anyone even checking? There's nobody standing there. There's no one at the gate at all.)"
    mc "(...I could just walk through. Ten seconds and I'm on the other side.)"

    # Neither answer pays. Walking through is him acting on his own reading of the
    # room and buying a ticket is him doing what he was told on a landing strip
    # ninety minutes ago, but both are the same ten seconds of turnstile and the
    # turnstile does not remember anything. The fork decides how he meets the
    # station, not who he is becoming.
    menu:
        "Walk straight through.":
            jump train_gate_slam
        "Buy a ticket first.":
            jump train_ticket


label train_gate_slam:
    "I put my head down and step forward like I've done it a thousand times."
    # The buzz of the gate refusing him, and a shake that lasts long enough to
    # actually feel like a wall hitting his legs.
    mc "WHOAH!"
    $ play_sfx("audio/SFX/gate.wav")
    "The flaps snap shut hard, right across my shins, and a buzzer goes off above my head loud enough to turn three heads." with gate_shake
    mc "(That thing almost closed on my legs!)"
    mc "(Okay. Okay. So that's why everybody has a ticket.)"
    mc "(Oh. Right. I need to buy a ticket first.)"
    "Behind me, a man in a station uniform clears his throat. He doesn't say anything. He just looks at me."
    mc "(Yes. Yes, I know. I'm going.)"

    jump train_ticket


label train_ticket:
    "The ticket machines stand in a row along the wall, glowing green in the dim."
    "On the screen: a grid of buttons, and every button is a price."
    mc "(Fares. Prices on buttons. I just need to know which one is mine.)"
    mc "(The pamphlet. There was a number printed next to the station name.)"
    # He holds the pamphlet up in front of him while he tries to read it, then
    # puts it away before the machine menu opens over the top of it.
    show pamphlet at truecenter with dissolve
    "*Squints at the pamphlet. The characters swim a little.*"
    mc "(...800. I think that's 800. It's next to 中野, so it has to be the fare.)"
    mc "(Unless it's the platform number. Or the exit number. Or something I haven't thought of yet.)"
    hide pamphlet with dissolve


label ticket_machine:
    menu:
        "Press the 320 Yen ticket.":
            if has_item("ticket_320"):
                mc "(I already purchased this ticket. It's the wrong one.)"
                jump ticket_machine
            $ buy_item(320, "ticket_320")
            "A ticket drops into the tray with a soft clack."
            mc "(That was satisfying. That was also very cheap.)"
            mc "(...and it goes somewhere that is extremely not 中野.)"
            mc "(Put it down. Try again.)"
            jump ticket_machine

        "Press the 800 Yen ticket.":
            if has_item("ticket_800"):
                mc "(I already purchased this ticket. It's the wrong one.)"
                jump ticket_machine
            $ buy_item(800, "ticket_800")
            "A ticket drops into the tray with a soft clack."
            mc "(800. That's the number from the pamphlet.)"
            mc "(That has to be it. Please let that be it.)"
            "I hold it up against the fare map above the machines. The arrow pointing at 中野 lands on a different row entirely."
            mc "(Not it..)"
            jump ticket_machine

        "Ask the station attendant.":
            "I catch the eye of a woman in a station uniform and hold the pamphlet up."
            mc "Sumimasen... 中野3丁目?"
            "She takes the pamphlet, reads it, and presses the button for me without a word."
            "¥1,300. A ticket slides out."
            mc "(That took her four seconds. It took me four minutes.)"
            mc "Arigatou gozaimasu."
            "She nods, already walking away."
            # The one award on the train route, and it lands on a person rather
            # than a flap of metal. He stopped trying to solve the building by
            # himself and let somebody help him, which is the same thing he will
            # have to keep doing for the next year, and it is the only thing in
            # the first act that moves Grace.
            $ reward_attributes_once("answer_ticket_ask", [("grace", "large")])
            jump train_platform


label train_platform:
    # The only ticket that actually works, and not one he could ever have found
    # on his own. That is the whole point of the scene.
    $ spend_money(1300)
    "I feed the ticket into the gate."
    "It beeps, the flaps swing open, and I walk through like it's nothing."
    mc "(So much easier with a ticket.)"
    mc "(Also, I notice, nobody closed anything on my legs this time.)"

    # Through the gate and up to the platform. A different part of the station,
    # so a different background.
    scene bg_platform with walk_fade

    "The platform opens up in front of me. Two tracks. Two crowds. Trains arriving every few minutes, swallowing people and leaving again."
    "There's a board overhead, and two signs on the posts behind me."
    "One sign lists eight stations."
    "The other lists twenty-three."
    mc "(...Eight, or twenty-three.)"
    mc "(The veteran said the local stops at every single station. So the one with eight has to be the express.)"
    mc "(I can count. That's one skill I definitely brought with me.)"
    mc "(Both of them say 中野. They both go where I'm going. One of them just takes a lot longer to get there.)"

    menu:
        "The sign with eight stations.":
            $ boarded_shinkansen = True
            jump train_board
        "The sign with twenty-three stations.":
            $ boarded_shinkansen = False
            jump train_board


label train_board:
    "A train sighs to a stop in front of me and the doors hiss open."
    "I step in, find a seat by the window, and hold my bag on my lap with both hands."
    "The doors close. The platform slides away."
    stop ambient fadeout 1.5

    scene bg_train_interior with walk_fade
    play music "audio/SFX/traininside.mp3" fadein 2.0

    if boarded_shinkansen:
        "*Looking out of the window as the city blurs past.*"
        mc "Express. Right train, right direction, right carriage. Three things I got right today."
        mc "Watashi namae... no. Watashino namae wa... there. It still works."
        mc "What if they were expecting someone better? Somebody who can actually talk."
        mc "*Takes a deep breath.* No. I worked two years for this seat. Nobody handed it to me."
        mc "*The roofs go by. Then the signs. Then the little gardens squeezed between the houses.*"
        mc "*Yawns.* Eyes. Just for a minute."
    else:
        "*Settling into the seat as the carriage fills up around me.*"
        mc "On the train. On my own. That was the first test, and I got through it."
        mc "This line stops everywhere, so I get to see the parts of it that are not for visitors."
        mc "Watashino namae wa... okay. That one still works too."
        mc "I don't know what the house will be like. I don't know what I will be like in it."
        mc "Everybody at home said I was mad to come alone. Some of them were right."
        mc "*Yawns.* Eyes. Just for a minute."

    # The train takes the long way round from the airport no matter which one he
    # caught, so either route gets him to the house late at night.
    $ arrived_late = True

    # Slow fade. He drops off somewhere in the middle of it, and wakes up at the
    # house in label home_arrival.
    window hide
    scene black with Dissolve(3.0)
    stop music fadeout 3.0
    pause 0.5
    jump home_arrival


################################################################################
## ACT THREE: HOME
################################################################################
##
## Both routes land here, but not in the same state. travel_method decides how he
## talks about the journey, and arrived_late decides whether the house is awake or
## asleep when he rings the bell. The taxi is direct, so he arrives earlier than
## the family expected; the train is the long way round, so he arrives late.

label home_arrival:
    scene bg_home_exterior_night with walk_fade
    $ night_street()
    # Quiet on purpose. After an airport and a train, the smallness of a
    # residential street at night is the point.

    if travel_method == "taxi":
        # The ride and the fare already happened in label taxi_stand, so this is
        # just him standing on the street with the taxi pulling away.
        "*Steps out into a street.*"
        "Barely any pavement, and somebody's bicycle leaning against a wall."
        "The taxi pulls away, and then it's just me and the crickets."
    elif boarded_shinkansen:
        "The walk from the station is short and the neighbourhood lit up by street lights in a cozy way."
        "Low houses one behind the other, each with a tiny garden and some with bicycle leaning against the wall."
        mc "Managed to catch the express and transfer at the right station. Not bad for my first time navigating solo."
    else:
        "The walk from the station takes forever."
        mc "That local stopped at every station between here and the airport. Twice, it felt like."
        mc "It's late. I hope I'm not waking anyone up."


    "I stand in front of a narrow two-storey house with one light on behind the curtains."
    mc "Home, for a year. I'll find out what that means in the morning."
    mc "What was the greeting again. Konnichiwa. That has to work."
    "*Pushes for the doorbell.*"
    # The chime lands at the same moment as the line describing it, so the sound
    # and the text hit together instead of a beat apart.
    $ play_sfx("audio/SFX/doorbell.mp3")
    pause 3.0
    "*The chime is much louder than I expected. It bounces off the houses opposite.*"
    mc "(Oh no. Everyone on this street heard that. I hope I didnt wake up anyone in the house.)"

    if arrived_late:
        # Late arrival, which is the train. Only the mother is still up, and the
        # whole scene is quiet.
        $ play_sfx("audio/SFX/door_open.mp3")
        "The door opens a crack, then all the way, carefully."
        mother "Oh! You made it."
        mother "Thank goodness. We thought you'd got lost somewhere between the airport and here."
        mother "Come in, come in. Quickly. It's cold out, and everyone else is asleep."
        "*She holds the door and waves me in with her whole arm.*"
        mc "Sorry. The train took much longer than I thought, and I..."
        mother "It's alright. Truly. You're here now, that's all that matters."
        mother "Shoes off here. Then straight up the stairs, quietly."
        stop music fadeout 3.0

        scene bg_home_night with walk_fade

        mother "My husband is already asleep, so you'll meet him properly in the morning. I'm Miharu Nagai."
        mc "Ah. Konnichiwa. I'm..."
        mother "I know who you are, [player_name]. We've been waiting months for you."
        mother "Hikari is the one who wrote all those emails. She's asleep too."
        mother "She doesn't even know you've arrived, so she'll get a surprise at breakfast."
        mc "(Hikari. The one who answered every single one of my questions about the university.)"
        mc "(I'll thank her tomorrow. When my brain works.)"
        mother "Come. Your room is at the top of the stairs."
    else:
        # Early arrival, which is the taxi. It went straight to the door, so he is
        # here sooner than the family expected and the whole house is still up.
        "The door opens before I've finished panicking."
        $ play_sfx("audio/SFX/door_open.mp3")
        mother "Oh! You're earlier than I expected!"
        mother "We said an hour, maybe two, with the traffic. Not this early."
        mother "You took a taxi, didn't you. Sensible. I'm so glad you made it. Welcome!"
        mother "Come on in. You must be exhausted."
        "*She has my bag out of my hands before I manage to say anything.*"
        stop music fadeout 3.0

        scene bg_home_night with walk_fade

        mother "Welcome again, [player_name]. I'm Miharu Nagai."
        father "And I'm Tetsuo Nagai. So you finally found our home, [player_name]. Miharu told us you'd be arriving today."
        father "We keep things the proper way in this house. None of that new gadget nonsense."
        father "A good letter, or a proper face-to-face talk, works best."
        mother "Tetsuo still uses the same flip phone he bought ten years ago."
        mother "But don't worry, I'm happy to help you with anything you need."
        mother "Hikari was the one who sent you all those emails. She's resting now, but you'll meet her in the morning."
        father "This is our first time hosting someone from abroad. We'll treat you like family here."
        father "Miharu, why don't you take our guest up before the evening chill sets in?"
        mother "Of course. Please, follow me. Your room is just upstairs."

    # Upstairs now, so the room becomes a place of its own instead of the corner of
    # the house he was still standing in. Shared by both arrival routes.
    #
    # The climb is heard before it is seen: three seconds of feet on the stairs play
    # while he is still down in the hall, and only then does the room arrive.
    #
    # stairs_climb.wav is a cut of the middle of stairs.mp3. The opening of the
    # original sits around -42 dBFS, some 15 dB below every other sound in the game,
    # which is why playing it from the top was inaudible. This cut takes the loudest
    # passage, normalises it to match money/gate/doorbell, and has both the fade in
    # and the fade out baked into the file, so there is nothing to stop at the end
    # and nothing to time. Play it, let it run, change the scene when it is done.
    $ play_sfx("audio/SFX/stairs_climb.wav")
    scene bg_room_night with stair_fade
    pause 3.0
    $ room_ambient(True)

    # The room, and the boxes that arrived before he did.
    "The stairs creak under both of us. She apologises for the creaking, which is somehow more embarrassing than the creaking."
    mother "Well, it's not a lot, but this will be your room for the year."
    mother "Hikari's room is next door, so please try not to make too much noise. She's a light sleeper."
    mother "Oh, and the things you shipped over arrived yesterday. They're still down by the door."
    mother "Would you help your old host mother carry them up?"
    mc "Of course. Let me help."

    # The first thing he ever does for this household, and it is answering the
    # apologising rather than carrying the cardboard. She has been nervous since
    # the doorbell, so the fork is about whether he decides to do anything about
    # that, which is a different question from being polite. It is also the first
    # night, and the first night is not where a person is decided.
    menu:
        "You don't have to apologise.":
            mc "Miharu-san. You don't have to keep saying sorry to me. Not for stairs, and not for boxes."
            mother "..."
            mother "Three days I have been tidying that room, and I have been saying sorry to it the whole time."
            mother "Thank you. That was a kind thing to say to a nervous woman."
        "Are you worried about me being here?":
            mc "Can I ask you something? Are you worried about this? About me being here."
            mother "Every time. There were two students before you and I worried every time."
            mother "You are the first one who has asked me that."
            mc "(I don't know what I expected. I didn't expect it to be true.)"
        "Watch how she carries it.":
            mc "(She takes the top one and holds it with both hands under the base. Not by the flaps.)"
            mc "(That's how you carry somebody else's things. I have been carrying mine by the tape for two countries.)"

    "*We bring the boxes up together. They are heavier than they look, and she apologises the whole way.*"
    if arrived_late:
        mother "Goodnight. Sleep well. We'll talk properly in the morning."
    else:
        mother "Goodnight. And truly, welcome. We'll talk properly in the morning."
    "*The door clicks shut, and then the house is completely silent.*"

    mc "Good thing I sent everything ahead. Thanks to that I only had to carry a small bag."
    mc "I never would have managed the transfers with luggage."
    mc "Right. Unpacking."
    "*Cardboard. Tape. Clothes that smell like my old room. Books I probably won't read.*"

    "Somewhere in the middle of it the room stops looking like a spare room and starts looking like somewhere a person lives."
    mc "Whew. I am tired, but it finally looks like a proper room."
    mc "And honestly, I'm grateful I have one at all."
    mc "I've heard about foreign students sharing bunk beds in rooms half this size."
    if travel_method == "train":
        mc "I slept on the train. So why am I tired again?"
    else:
        mc "I slept in the taxi. So why am I tired again?"
    mc "Maybe I should sleep."
    mc "My first night in Japan."

    window hide
    scene black with Dissolve(2.5)
    stop music fadeout 1.0
    pause 1.0
    jump dream_sequence


################################################################################
## ACT THREE, FIRST BEAT: THE FIRST DREAM
################################################################################
##
## He falls asleep at the end of the first night and the day he just had comes
## back to him in the wrong order, with things in it that were never there.
## Underneath the dream there are two voices in a room he has never been in,
## discussing him in the third person. They are the same white light and the same
## clinical register that cut into him on the plane, so the player has already
## been taught how to read them: this is what is actually happening to him.
##
## The mini-game asks him to sort the real memories of today from the planted
## ones. It is not possible to fail it. It is very possible to be told things he
## should not know.

# The whole picture stutters sideways and then recovers. Slow enough to read as
# damage rather than as movement, and it never settles into a rhythm.
#
# It has two different failures now instead of one. The first is a heavy lateral
# tear that drags the frame and snaps back; the second is a shorter, sharper one
# that arrives sooner. Because they are not the same size or the same distance
# apart, the eye cannot get ahead of it and read it as a loop.
transform glitch_jitter:
    subpixel True
    block:
        xoffset 0 yoffset 0 zoom 1.0
        pause 0.75
        xoffset -26 yoffset 7 zoom 1.012
        pause 0.035
        xoffset 19 yoffset -9
        pause 0.03
        xoffset -12 yoffset 4
        pause 0.045
        xoffset 8 yoffset -3
        pause 0.03
        xoffset -4 yoffset 1
        pause 0.04
        xoffset 0 yoffset 0 zoom 1.0
        pause 0.45
        xoffset 15 yoffset -5
        pause 0.03
        xoffset -21 yoffset 6 zoom 1.008
        pause 0.03
        xoffset 0 yoffset 0 zoom 1.0
        pause 0.62
        repeat


init python:

    def dream_static_bars(count=9, max_alpha=0.32, tears=True):
        """A few bright scan lines, in new places every time they are asked for.

        The static screen calls this on a fast timer, so the interference never
        holds still long enough to read as a pattern. Most of the lines are thin
        and white; a few are tinted, which reads as the picture separating rather
        than just flickering, and now and then the whole frame washes out for a
        single tick.
        """
        width = config.screen_width
        height = config.screen_height
        bars = []

        for _i in range(count):
            thickness = renpy.random.randint(1, 6)
            bars.append(
                Transform(
                    Solid(renpy.random.choice(["#ffffff", "#ffffff", "#bfe9ff", "#ffd9d9"])),
                    xysize=(width, thickness),
                    ypos=renpy.random.randint(0, height - thickness),
                    alpha=renpy.random.uniform(0.07, max_alpha),
                )
            )

        if tears:
            # Sometimes a whole band of interference crosses the frame, which is
            # what makes the static read as damage rather than as texture.
            if renpy.random.random() < 0.38:
                thickness = renpy.random.randint(8, 28)
                bars.append(
                    Transform(
                        Solid("#ffffff"),
                        xysize=(width, thickness),
                        ypos=renpy.random.randint(0, height - thickness),
                        alpha=renpy.random.uniform(0.11, max_alpha),
                    )
                )

            # And rarely, the frame blows out entirely for one tick.
            if renpy.random.random() < 0.07:
                bars.append(Transform(Solid("#ffffff"), alpha=renpy.random.uniform(0.06, 0.13)))

        return bars

    def build_dream_cards(travel_method, boarded_shinkansen):
        """Today, as four memories that happened and two that did not.

        The true cards are written from the route the player actually took, so the
        dream is *his* day rather than a generic one. The false ones are the room's
        own furniture: a face with no name, and a corridor that keeps repeating.
        """
        if travel_method == "taxi":
            real = [
                "The plane doors opening, and the air on the other side of them",
                "A driver who bowed before he opened the door for me",
                "A meter climbing in hundreds, and never once in ones",
                "A bell that rang louder than the whole street",
            ]
        elif boarded_shinkansen:
            real = [
                "The plane doors opening, and the air on the other side of them",
                "A board on the platform that changed while I was reading it",
                "The express, and the country going past sideways",
                "A bell that rang louder than the whole street",
            ]
        else:
            real = [
                "The plane doors opening, and the air on the other side of them",
                "A board on the platform that changed while I was reading it",
                "A local train that stopped at every single station",
                "A bell that rang louder than the whole street",
            ]

        fake = [
            "A woman in white, calling a name that is almost mine",
            "A corridor of doors, and behind every one of them my room",
        ]

        # `order` is the position in the day, not on the board. Both lists above
        # are written in the order things happened, so the number is simply the
        # index, and the label reads these back to know what "right" is. The
        # planted ones have no position in the day, so they get no number.
        cards = []
        for i, text in enumerate(real):
            cards.append({"id": "real%d" % i, "text": text, "real": True, "order": i})
        for i, text in enumerate(fake):
            cards.append({"id": "fake%d" % i, "text": text, "real": False, "order": None})

        # Shuffled once per showing, so the same words do not land in the same
        # squares twice in a row and the player cannot learn the board.
        renpy.random.shuffle(cards)
        return cards


# The interference itself. Drawn on the overlay layer so it crosses the dialogue
# as well as the picture: the voice he is hearing is not coming from the room he
# thinks he is standing in.
screen dream_static():
    layer "overlay"

    default bars = dream_static_bars()
    timer 0.05 repeat True action SetScreenVariable("bars", dream_static_bars())

    for b in bars:
        add b


# How the board answers a touch.
#
# Every card gets this one, and it is a bare named transform rather than a call
# with arguments: a screen rebuilds a displayable whenever its `at` changes, so an
# animated transform built fresh on each render would restart forever instead of
# settling.
#
# Cards lift a little under the cursor, so the board feels like something you are
# handling rather than a form you are filling in.
transform dream_card_hover:
    zoom 1.0
    on idle:
        ease 0.16 zoom 1.0
    on hover:
        ease 0.16 zoom 1.045

# The heading keeps slipping a few pixels, the way the rest of the dream does.
transform dream_title_glitch:
    subpixel True
    block:
        xoffset 0
        pause 2.3
        xoffset -3
        pause 0.04
        xoffset 2
        pause 0.05
        xoffset -1
        pause 0.05
        xoffset 0
        repeat


# The ordering game. The pile is on the right, the day he is rebuilding is on the
# left, and the only thing the label ever hears about is a finished reading.
#
# Moving a card between the two is not a story event, so it does not go through
# the label: the click is handled here and the board changes on the same frame.
# That is what makes taking a card back out of the middle of the order feel like
# moving something on a table instead of asking the game for permission. The label
# owns only what a wrong reading costs, because the count of readings is his and
# not the board's.
#
# Nothing here reveals which cards are his. The old board turned the true ones
# green as they were touched, which handed the player the answer in the first few
# clicks; the whole point of this version is that the board says nothing and the
# order has to be kept in his head.
screen dream_timeline(cards, start_placed, attempts):

    modal True
    zorder 100

    add Solid("#04050a")

    # Interference over the board itself, kept lighter than the full-screen
    # version: it should feel like the picture is unwell, not make the words hard
    # to read.
    default bars = dream_static_bars(3, 0.16, False)
    timer 0.09 repeat True action SetScreenVariable("bars", dream_static_bars(3, 0.16, False))

    # The order being built. It is seeded from what the label handed in, so a
    # reading that came back wrong returns to the board exactly as he left it
    # rather than being wiped and started over.
    default placed = list(start_placed)

    $ card_by_id = {c["id"]: c for c in cards}
    $ pile = [c for c in cards if c["id"] not in placed]
    $ full = len(placed) >= 4

    for b in bars:
        add b

    vbox:
        xalign 0.5
        ypos 28
        spacing 8

        text "PUT THE DAY BACK" at dream_title_glitch:
            xalign 0.5
            size 32
            color "#8fd8ff"
            outlines []

        text "Four of these happened today. Put the four back in the order they happened.":
            xalign 0.5
            size 18
            color "#6b7a8c"
            outlines []

    # How many readings he has left. Three dots, and they go out one at a time.
    hbox:
        xpos 1210
        ypos 42
        xanchor 1.0
        spacing 8

        text "READINGS LEFT" size 16 color "#6b7a8c" outlines []

        for i in range(3):
            text "●" size 19 outlines [] color ("#8fd8ff" if i < attempts else "#232d3a")

    # --- the order he is rebuilding ----------------------------------------
    vbox:
        xpos 70
        ypos 150
        spacing 12

        hbox:
            spacing 16
            text "IN ORDER" size 18 color "#c8a06a" outlines []
            text "[len(placed)] / 4" size 18 color "#5c6b7d" outlines []

        for i in range(4):

            if i < len(placed):

                $ cid = placed[i]
                $ slot_text = card_by_id[cid]["text"]

                # Clicking a placed card takes it back out. Everything under it
                # moves up, because the order is the list itself and the list
                # simply got shorter.
                button:
                    xysize (560, 86)
                    at dream_card_hover
                    background Solid("#1b2330")
                    hover_background Solid("#2b1f28")
                    action [
                        Play("sfx", "audio/SFX/type_click.wav"),
                        SetScreenVariable("placed", placed[:i] + placed[i + 1:]),
                    ]

                    fixed:
                        xysize (560, 86)
                        add Solid("#8fd8ff22", xysize=(56, 86))
                        text str(i + 1) xpos 0 xsize 56 text_align 0.5 yalign 0.5 size 26 color "#8fd8ff" outlines []
                        text slot_text xpos 74 yalign 0.5 xmaximum 430 size 17 line_spacing 3 color "#e8e2d6" outlines []
                        text "x" xpos 532 yalign 0.5 size 18 color "#5c6b7d" outlines []

            else:

                fixed:
                    xysize (560, 86)
                    add Solid("#161d27", xysize=(560, 86))
                    add Solid("#0a0e14", xysize=(556, 82)) xoffset 2 yoffset 2
                    text str(i + 1) xpos 2 xsize 56 text_align 0.5 yalign 0.5 size 26 color "#26313f" outlines []
                    add Solid("#1a2431", xysize=(430, 2)) xpos 84 yalign 0.5

    # --- the pile ----------------------------------------------------------
    vbox:
        xpos 700
        ypos 150
        spacing 8

        text "LOOSE MEMORIES" size 18 color "#c8a06a" outlines []

        for c in pile:

            button:
                xysize (510, 66)
                at dream_card_hover
                background Solid("#11151c")
                hover_background Solid("#1d2531")
                insensitive_background Solid("#0b0e13")
                sensitive (not full)
                action [
                    Play("sfx", "audio/SFX/memory_restore.wav"),
                    SetScreenVariable("placed", placed + [c["id"]]),
                ]

                text c["text"]:
                    xalign 0.5
                    yalign 0.5
                    xmaximum 470
                    text_align 0.5
                    size 17
                    line_spacing 3
                    color "#e8e2d6"
                    outlines []

    # --- the reading -------------------------------------------------------
    button:
        xpos 640
        xanchor 0.5
        ypos 636
        xysize (360, 48)
        background Solid("#14301f" if full else "#0e131a")
        hover_background Solid("#1d4a30")
        sensitive full
        action Return(list(placed))

        text "LOOKS RIGHT":
            xalign 0.5
            yalign 0.5
            size 22
            outlines []
            color ("#c8f0d8" if full else "#39434f")


label dream_sequence:

    # He is asleep. The house is quiet and the dark behind his eyes is not.
    stop music fadeout 2.0
    pause 1.5

    # The dream gets its own bed of sound. It is a loop, so nothing has to be
    # restarted while the sequence plays out.
    play music "audio/Music/dream sequence.wav" fadein 3.0

    # The first thing that is wrong is that the dark is not quiet. Something thin
    # and bright keeps crossing it, like a scan line on a tired television.
    show screen dream_static
    pause 1.4
    hide screen dream_static

    "I'm standing in the airport again."

    scene bg_airport at glitch_jitter with Dissolve(0.35)
    "The same hall. The same sign. The gate I sat at for four hours with a bag between my feet."
    "Only the announcements are arriving before anyone speaks them, and the hall is empty."
    "I walk it end to end. Both times I come out at the same gate."

    # The first slip. Same white light, same clinical voice that cut into him on
    # the plane, so this is the room he is actually lying in.
    show hospital_flash onlayer overlay at truecenter:
        alpha 0.0
        linear 0.1 alpha 0.45
        linear 0.1 alpha 0.0
    "Keep the room at eighteen. He dreams less when it's cold."

    show screen dream_static
    pause 0.6
    hide screen dream_static

    if travel_method == "taxi":

        scene bg_taxi_interior at glitch_jitter with Dissolve(0.3)
        "Then the taxi. Same seat, same smell of cleaner, same driver's shoulders exactly where I left them."
        "The meter is climbing the way it climbed, in hundreds, never in ones."
        "But the road in the windscreen in front of him has no end to it."
        mc "Excuse me. How much further?"
        "He doesn't answer. He doesn't turn around. The meter goes up."

    else:

        scene bg_train_interior at glitch_jitter with Dissolve(0.3)
        "Then the train. Same carriage, same windows, the same handrail I held for an hour."
        "The stations go past in the right order, and then they go past in the right order again."
        mc "Did we already stop here?"
        "Nobody looks up. They are all reading, and none of the pages turn."

    scene bg_home_exterior_night at glitch_jitter with Dissolve(0.35)
    "Then the street. Narrow. Bicycles against the wall. One light on behind the curtains."
    "The bell is still ringing. It has been ringing underneath everything else this whole time."
    hide screen dream_static

    # A second slip, harder than the first, and this time the room answers a
    # question he has not asked yet.
    show hospital_flash onlayer overlay at truecenter:
        alpha 0.0
        linear 0.08 alpha 0.6
        linear 0.08 alpha 0.0
    "Six hours. He has been under six hours."
    "Let him finish the day. The consolidation needs the whole day."

    scene black with Dissolve(0.6)
    "And then the pieces of today come loose and scatter."
    mc "No. Wait."
    mc "I know what today was. I was there for all of it."
    "Everything I did today is lying on the floor of my head, mixed up with things I have never seen."
    "I don't know why it matters that I put it back in the right order."
    "It matters."

    window hide

    # The game. Four of the cards are the day he actually had, in the order he
    # had it, and two are the room's own furniture. He has to put the four true
    # ones back in sequence, and he is given three readings of it.
    #
    # A wrong reading costs a reading and nothing else. What he has worked out
    # comes back to the board with him, because taking the whole thing apart
    # again would hand him the answer instead of making him find it.
    $ dream_cards = build_dream_cards(travel_method, boarded_shinkansen)
    $ dream_order = [c["id"] for c in sorted([c for c in dream_cards if c["real"]], key=lambda c: c["order"])]
    $ dream_placed = []
    $ dream_attempts = 3
    $ dream_solved = False

    while dream_attempts > 0 and not dream_solved:

        call screen dream_timeline(dream_cards, dream_placed, dream_attempts)
        $ dream_placed = _return

        if dream_placed == dream_order:

            $ dream_solved = True

        else:

            $ dream_attempts -= 1

            # The same white light as before, and the room talking over him while
            # he is still looking at the board.
            show hospital_flash onlayer overlay at truecenter:
                alpha 0.0
                linear 0.08 alpha 0.65
                linear 0.08 alpha 0.0

            mc "No. That is not it either."

            if dream_attempts == 2:
                "Out of sequence. He is holding all the pieces and none of the order."
                "Leave him to it. Do not help him."
            elif dream_attempts == 1:
                "Still out. He is arranging the day the way he wants it, not the way it was recorded."
                "One reading left. After that we take the board off him."
            else:
                show screen dream_static
                "That is three. He is not going to find it tonight."
                "Close the sequence. He keeps the day. He does not keep the order."
                hide screen dream_static

    window hide

    if dream_solved:
        "Four of them. All four are mine, and they are back where they go."
        "The airport, the ride, the street, the bell. That was today."
        "That is all of it. That is everything that happened."
    else:
        "I could not make them sit still. Every time I put one down, another one moved."
        "But the four that were mine were in that pile. I know them when I see them."
        "The airport. The ride. The street. The bell."
        "Whatever else was in there was never mine."

    # The reward is not for finishing. It is for finishing first, which is the
    # only reason the readings are counted at all. Insight, because holding a day
    # in the right order is the same muscle as reading a room.
    if dream_solved and dream_attempts == 3:
        $ reward_attributes_once("dream_day_order", [("insight", "medium")], show="card")

    # And the last thing the dream does is answer him, which a dream should not be
    # able to do.
    show hospital_flash onlayer overlay at truecenter:
        alpha 0.0
        linear 0.12 alpha 0.7
        linear 0.12 alpha 0.0
    "Consolidation complete. Bring him up slowly."

    stop music fadeout 3.0
    scene black with Dissolve(1.5)
    pause 1.5

    jump morning_call


################################################################################
## ACT THREE, SECOND BEAT: THE FIRST MORNING
################################################################################

label morning_call:

    # Waking up. The dream lets go of him slowly, the way a hand does once it has
    # decided you can stand on your own.
    #
    # The room in the morning. room_ambient plays room_day.mp3 here by default;
    # this scene is where that track lives, so nothing is overridden.
    scene bg_room_day with Dissolve(2.0)
    $ room_ambient(False)
    "Whoa.. I just had the weirdest dream ever."
    "Something about the airport. A road with no end on it. Two voices talking over me like I wasn't in the room."
    mc "What was that about?"
    mc "It almost looked like a personal nightmare handmade for me."
    "I try to hold onto it and it comes apart like wet paper."
    "It takes me three seconds to remember where I am."
    "Japan. The house. The room with the boxes in it."
    mc "My first morning."


    # And then the house starts moving. This is the first Japanese household he
    # has ever heard wake up.
    "Then the whole house wakes up around me at once."
    "Pans, somewhere below. A radio turned down low. Wood moving."
    "Feet on the stairs, two steps at a time, and then three quick knocks on my door."
    "It slides open before I can answer it."
    hikari "Morning! You're awake. Good, I was about to give up on you."
    "A girl about my age. A blouse, jeans, hair still damp from the shower."
    hikari "I'm Hikari. I sent you the emails. So you're [player_name]."
    mc "(That voice. I have been reading that voice since spring.)"
    mc "Hikari. Right. Sorry, I thought you'd be older."
    hikari "Everyone says that. I write like an old man, apparently. Mom's theory, not mine."
    hikari "Come down when you're decent. There's breakfast, and there are a lot of opinions about it."
    "She is gone before I work out which question to ask first."

    scene bg_kitchen with walk_fade

    "The kitchen smells like toast, green tea, and under both of those something older, like a cupboard that has always been a cupboard."
    "Miharu is at the counter with her sleeves pushed up. Tetsuo is already at the table, and he has not started eating."
    mother "There he is. Sit, sit. It's only rice and soup, but you'll want something warm in you before you go out."
    mc "Thank you. Good morning. Ohayou gozaimasu."
    father "Ohayou."
    mother "Oh, listen to that. Tetsuo, he's been practising."
    father "Hm."
    "There is a folded newspaper beside his bowl. He has not opened it. He looks at me the way you look at a delivery you didn't order."

    if travel_method == "taxi":
        father "Miharu tells me you came from the airport by taxi."
        father "That is the expensive way."
        mc "(He says it like a fact about me, not about the taxi.)"
        father "It is also the correct way, when you land that late and you are carrying things."
        father "Know what things cost here and you will be fine."
    elif boarded_shinkansen:
        father "Miharu tells me you came from the airport by train. And that you found the express."
        father "Most people who arrive here do not find the express on their first day."
        mc "(I think that was a compliment. It was delivered like a customs form.)"
        father "Good. Then you can read a timetable. That will be useful to you here."
    else:
        father "Miharu tells me you came from the airport by train."
        father "Which is the long way, at that hour."
        mc "(He says it like a fact about me, not about the train.)"
        father "It is also the cheaper way. Knowing the difference between the long way and the wrong way is most of living here."

    mother "Tetsuo. He only landed yesterday."
    father "I am being helpful."
    mother "You are not being nice."
    "Hikari puts a bowl down in front of me without being asked and sits opposite, elbows on the table."
    "Tetsuo visibly decides not to mention it."
    hikari "Ignore him. He does this to everybody. He did it to me, and I have lived here my whole life."
    hikari "Okay. University. Same department, same building, which was completely not arranged."
    mc "Was it arranged?"
    hikari "It was arranged."
    hikari "Everyone has been asking about you since April, by the way. There is a pool."
    mc "A pool."
    hikari "On whether you'd actually turn up. I'm not telling you what I bet."

    # The first real conversation in the game he is allowed to steer, and it is
    # with the one person here who has been talking to him for months. He has read
    # her voice since spring and never heard it; this is where the player decides
    # what he does with that. Nothing here pays - it is the first morning, and it
    # is a relationship being started, not a score being kept - but Hikari keeps
    # the answer either way.
    menu:
        "Who starts a pool about a person?":
            mc "Who starts a pool about somebody they've never met?"
            hikari "Mom. April. And she has been losing steadily ever since, which she will not admit."
            mc "(Somewhere between the bet and the rice this stopped being a house I'm staying in.)"
            $ remember("hikari", "asked who started the pool")
        "What did you bet?":
            mc "What did you put on me?"
            hikari "That you'd turn up. And that you'd be shorter."
            mc "That's not a bet. That's an insult with paperwork."
            hikari "It's both. That's the good kind."
            $ remember("hikari", "asked what she bet")
        "Thank you for the emails.":
            mc "Before the food. Thank you. For the emails."
            mc "There were a lot of them, and you answered every one, including the stupid ones."
            hikari "There were no stupid ones."
            mc "(She said that fast. She had it ready. She has had it ready for months.)"
            $ remember("hikari", "thanked her for the emails")

    # Tetsuo's one piece of advice for the year, and it is also the thesis of his
    # character: keep to the routine and nothing bad can happen.
    father "The school will have rules. They will all be written down, and they will all be simple."
    father "Follow them and nothing will happen to you. That is all a school is."
    mc "(He says it like a fact about schools. It lands like a fact about me.)"

    mother "Don't listen to him, dear. The teachers are kind."
    mother "The other students will be curious for a week and then they will be ordinary."
    mother "If anything at all happens, you call me. You still have the number I wrote out for you?"
    mc "I have it."
    mother "You have it. Good."
    mc "(She asks the way people ask when they already know the answer.)"

    hikari "Right. Go and grab your bag. I will be waiting for you here."
    mc "Wait a minute. Are we leaving already?"

    father "I will be at the office until eight."
    father "Hikari. Take him the proper way."
    hikari "I always take the proper way."
    father "You take the short way."
    hikari "Today I'll take the proper way."
    "He nods, once, and picks up his bag."
    father "Your Japanese will improve faster if you use it badly than if you don't use it at all."
    hikari "That was his version of a compliment. Take it, they're rare."
    father "Hikari."
    hikari "I said nothing. Go to work."

    mother "Go on, both of you. Take an umbrella, it's meant to rain this afternoon."
    mother "And eat something before you leave. You as well, Hikari. That was not breakfast."
    hikari "It was toast."
    mother "It was one toast."

    "And then the kitchen is loud and ordinary, and I am standing in the middle of it."
    "A bowl in my hands, and no idea what to do with either."
    hikari "Hey. You okay?"
    mc "Yeah. Just a lot of firsts in one morning."
    hikari "First morning's the worst one. It gets easier by Wednesday. I promise."

    jump leaving_house


################################################################################
## ACT THREE, THIRD BEAT: LEAVING THE HOUSE
################################################################################
##
## The genkan in daylight, and the last thing between the kitchen and the street:
## the screen door. It is the first piece of the house he is trusted to close,
## which is why it gets a scene of its own. Hikari hands him the rule the way she
## hands him everything else, as something everybody already knows.

label leaving_house:

    scene bg_home_day with walk_fade

    # In a Japanese house the shoe rack by the door is a list of who is home, and
    # his own new shoes do not belong on it yet.
    "The hallway is cooler than the kitchen and it smells like the shoe cupboard by the door."
    "Four pairs on the rack, all of them lined up. Mine are the odd ones out, set slightly apart, like they are waiting to be introduced."

    hikari "Yours are the ones that were on a plane yesterday."
    mc "Why does everyone in this house know where my things are?"
    hikari "Because nothing here is allowed to be a surprise. You'll get used to it."

    # Tetsuo leaves first and without ceremony, and the sound he leaves behind is
    # the whole subject of the scene.
    "Behind us, the front door opens. Something slides. The street gets loud for two seconds, and then it doesn't."
    hikari "Hear that?"
    mc "Your dad leaving?"
    hikari "The amado. The screen on the door. He closes it even when he's in a bad mood."
    mc "(I didn't hear anything. It was just the sound of a door closing.)"

    # Two doors, and both of them are honest answers to the same sentence. He can
    # ask, which is him admitting the house is a language he does not speak yet, or
    # he can say the true and slightly embarrassing thing, which costs more. The
    # fork is his first real answer to Hikari and she keeps whichever one he gives.
    menu:
        "How can you hear a difference?":
            mc "How can you tell a mood from a door? It's a door."
            hikari "It's the speed. An angry amado is fast, and a fast one bounces off the frame."
            hikari "You'll hear it in a month. Everybody does. It's the first thing this house teaches you."
            $ remember("hikari", "asked her how she hears a door")
        "I didn't hear anything.":
            mc "...I didn't hear anything. Sorry. It was a door closing."
            hikari "Good. That means you're early."
            mc "(I thought that would land worse than it did. She said it like it was a stage of something I'm going through.)"
            $ remember("hikari", "admitted he did not hear the door")

    # The rule, and the reason for it, because Hikari never gives a rule without a
    # reason. The mosquitoes are not a metaphor.
    hikari "Rule one. You close the screen behind you. Every single time. It isn't about manners."
    mc "Then what is it about?"
    hikari "Mosquitoes. Moths. And one summer I left it open for about ten seconds."
    hikari "A cicada got into my room at two in the morning and screamed until dawn."
    mc "Screamed."
    hikari "It is not a small insect. It's a loud bird that got lost."
    mc "(That is the most serious she has been all morning, and it was about a bug.)"

    # And then he gets it wrong, in the ordinary way that everybody gets it wrong,
    # which is the point: he isn't being tested, he's being taught.
    "I go out first, because that is what you do when somebody is showing you the way out of their own house."
    "The screen slides easily. I pull it shut with one hand on the middle, the way I'd close any other door."
    "It bounces off the frame and hangs there, open by a hand's width."
    hikari "The frame. Not the mesh."
    mc "Sorry."
    hikari "Don't be sorry, just do it. The mesh stretches, and then it's baggy forever, and everybody in the house blames the guest."
    mc "(That was a joke. I'm fairly sure that was a joke.)"
    "I put my fingers on the metal edge instead, and it slides home with a click so small I almost miss it."
    "It sounds exactly like the one Tetsuo made."
    mc "(Okay. That one I'm keeping.)"

    # Miharu gets the last word without ever coming to the door, so her line stays
    # narration and she does not appear out here in the genkan with a portrait.
    "Umbrella! From somewhere back in the house, at the volume of a person who has been waiting all morning to say it twice."
    hikari "It isn't raining, Mom."
    mc "It isn't raining."
    hikari "Take the umbrella."
    mc "(Two people in this house have told me to take an umbrella. I take the umbrella.)"

    jump school_morning


################################################################################
## ACT THREE, FOURTH BEAT: WALKING TO SCHOOL
################################################################################
##
## Out of the house, and the first daylight he has seen in Japan that is not an
## airport or a train window. Hikari talks the whole way, and the reason she
## talks the whole way is the character note.

label school_morning:

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The street looks different in daylight, which is a stupid thing to notice and I notice it anyway."
    "The bicycles are the same. The gutter is the same. Everything is exactly the same and none of it is familiar."
    hikari "You're walking too fast."
    mc "I'm keeping up."
    hikari "You're keeping up at a speed nobody walks at. It's fine. Everyone does it in their first week."
    "She talks the entire way. Which station is ours. Which exit not to take. Which bakery to ignore and which one not to."
    "She does not ask me a single question about myself, and halfway there I understand that this is deliberate."
    mc "(She's filling the silence so I don't have to fill it.)"

    # The journey itself is not shown. The house goes out on black and the ride
    # happens in narration, which is also where the father's phrase from breakfast
    # comes back around: "take him the proper way" is the long one, and Hikari
    # does not take it. The gate then comes up out of that black on the same two
    # seconds the prologue used, so the arrival has weight instead of being a cut.
    scene black with Fade(2.0, 0.6, 0.0)
    stop music fadeout 1.0

    "Then the station, and then the train."

    "(She took me the proper way.)"
    "(That is her father's word for it. He said it this morning like a rule, and I only understood it once we were on the platform.)"
    "(The proper way is the long one, and she does not take it.)"
    "(Two changes. One of them at a station so large I could not tell which floor I was standing on.)"
    "(She crossed the whole thing like a hallway in her own house. I crossed it like a man being carried.)"
    "(She takes the short way. She told me so before we left, and then she took this one anyway.)"
    "(She did not say why, and I did not ask.)"
    "(She says next time she'll show me the fast way.)"
    "(Next time. She said it like it was already a fact about my life here.)"

    scene bg_school_gate with Fade(0.0, 0.0, 2.0)
    play music "audio/Music/school.mp3" fadein 2.0

    "And then there it is."
    "A wall, a gate, a building behind the gate, and a few hundred people my age going through it like water through a grate."
    hikari "So. This is it. That's the school."
    mc "It's big."
    hikari "It's a school. They're all big."

    # The pamphlet he picked up at the airport had a photograph of a school on the
    # back page. Only fires if he actually took one, which is why it is worth
    # having taken it.
    if has_pamphlet:
        "Something at the back of my head moves, very slightly, and does not say why."
        mc "(That photo. The one on the pamphlet from the airport.)"
        mc "(Same gate. Same wall. Same two students standing off to the left, in the same place.)"
        mc "(I'm remembering it wrong. That's all. I only looked at it once.)"
        "I am almost certain I only looked at it once."

    # Still at the gate, and this is where the high school version of the day ends.
    # He is at a university, so the rules he half-remembers do not apply, and Hikari
    # corrects them the way she corrects everything: in passing, without ceremony.
    hikari "Right. Rules. And then I stop being a tour guide and start being your department."
    mc "Those are different jobs?"
    hikari "They are the same job. One of them is just quieter."
    hikari "One. Walk on the left. Everybody walks on the left here, and the stairwell is the one place you find out how much you mean it."
    hikari "Two. You keep your shoes on. This is not high school. They stay on your feet until you get home tonight."
    mc "(There was a whole list in my head of things I was going to do today.)"
    mc "(Taking my shoes off at the door was on it. It is not on it anymore.)"
    hikari "And that is the entire list. Nobody hands you a locker, and nobody tells you where to stand."
    mc "That is less comforting than you think it is."
    hikari "That's because you're still thinking like a student. You are a student here. It's different."
    "She says it the way she said the umbrella on the way out. Like it is obvious."
    "Like she has already decided to be patient with me about it."

    # She has spent the whole walk refusing to ask him anything about himself,
    # which the narration has already pointed out. So the fork is whether he turns
    # the conversation around, admits the wrong list, or asks the question that is
    # actually about the place rather than about him.
    menu:
        "What did you do, your first day?":
            mc "What did you do? Your first day here. You'd have been seventeen."
            hikari "...I walked in the wrong door. Twice. There are two entrances and I used the wrong one for a week."
            hikari "Nobody tells you that either. That's the whole thing about this place."
            mc "(She has been giving me a list of everything she had to learn the hard way. I only just noticed.)"
            $ remember("hikari", "asked what her first day was like")
        "I had a list. It was wrong.":
            mc "I had a list. In my head. On the plane."
            mc "Shoes at the door. Bow to the teacher. Stand up when somebody older walks in."
            hikari "How much of it survived the morning?"
            mc "The bowing. Maybe."
            hikari "That's a better score than most. Come on."
            $ remember("hikari", "admitted the list he brought was wrong")
        "Why does nobody tell you where to stand?":
            mc "If nobody tells you where to stand, how does anybody know where to stand?"
            hikari "They watch. For a week. And then they stop, and by then you're standing in the right place."
            mc "(That is the most useful thing anybody has said to me since I landed, and it wasn't about standing.)"
            $ remember("hikari", "asked how anyone learns where to stand")
    hikari "Ready?"
    mc "No."
    hikari "Honest answer. Come on."
    "I step through."


################################################################################
## ACT THREE, FIFTH BEAT: INSIDE THE GATE
################################################################################
##
## The reveal the whole morning has been walking towards. From the road it is a
## wall with a roof behind it. From the inside it does not stop, and the point of
## the scene is that both of those things are true at the same time.

label campus_grounds:

    scene bg_campus_interior with walk_fade
    
    "And the noise changes."
    "Outside the wall there is a road, and the road is Tokyo. Buses, a crossing signal, a delivery bike, all of it leaning on you at once."
    "Two steps past the gate it is gone. Not quieter. Filtered, like somebody reached over and turned the city down by half."
    mc "(From the street it was one building behind a wall. That is honestly all I could see.)"
    mc "(A wall, a roof, and about four metres of it.)"
    mc "(Inside, it keeps going.)"
    "A courtyard, and then another one behind it, and a covered walkway between the two."
    "Above the walkway a second floor of windows, and above that a third."
    "There are trees along the path, big ones, old enough that somebody planted them on purpose a long time ago and then waited."
    "People cross the courtyard in every direction at once and none of them collide."
    "There is an order to it that I cannot see yet."
    mc "(It's a different world in here. That isn't a figure of speech.)"
    mc "(I watched the city disappear behind a wall in three steps.)"
    hikari "You've stopped walking."
    mc "I'm looking."
    hikari "Everybody does that. First years, exchange students, and once a visiting professor, which was funnier than it sounds."
    hikari "Come on. The good part is the other direction."

    # She has just said that everybody stops here, which makes it the one place on
    # campus where a question about her is not a question about the building.
    menu:
        "What did you see, the first time?":
            mc "What did you see? The first time. You'd have been seventeen."
            hikari "A timetable. Honestly. I was late for something and I never once looked up."
            hikari "I have walked through this since I was seventeen, and you have seen more of it in four minutes than I have in a year."
            mc "(That landed somewhere I was not expecting it to land.)"
            $ remember("hikari", "asked what she saw in the courtyard, years ago")
        "This doesn't feel like a school.":
            mc "This doesn't feel like a school. It feels like it was something else first, and nobody's telling me what."
            hikari "You are going to be a lot of fun at parties."
            mc "(That was a joke. But she looked at the concrete one before she said it.)"
            $ remember("hikari", "said the campus does not feel like a school")
        "Work out the order people cross in.":
            mc "(Left to right, mostly. The ones coming down keep to the rail. Nobody stops in the middle.)"
            mc "(There is a rule here. I can watch it working and I cannot find it written down anywhere.)"

    "She walks fast, which I am starting to understand is just how everyone here walks."
    "She points at things the way a person points at their own house."
    hikari "Library. Open until ten. You will not care about that in September and you will care about it very much in December."
    hikari "That is the cafeteria, and that is the other cafeteria, and there is a reason there are two, and the reason is terrible."
    hikari "Past those, the gym. Nobody uses the gym."
    mc "Then why is there a gym?"
    hikari "Because there was a building here before there was a university. The rest grew around it. Stick close at the crossing."
    mc "(Stone next to glass next to concrete, and the concrete is the oldest of the three.)"
    mc "(Nobody designed this place in one go. It happened to it.)"

    "She turns down a path and the courtyard narrows into a plain grey building with a set of steps and too many doors."
    hikari "And this is ours."
    mc "Ours."
    hikari "You and me. Same department, so same building, so for the next year that door is the one you will get tired of."
    mc "(She says that like it's a good thing. I think it is.)"


################################################################################
## ACT THREE, SIXTH BEAT: THEIR DEPARTMENT
################################################################################
##
## Inside their building, and the first place in Japan that belongs to him rather
## than to a host family or a taxi. Nothing happens here on purpose. It is a room
## he is meant to learn by heart by the time the story is finished with him.

label department_tour:

    scene bg_department_hall with walk_fade

    "Inside, the building is cooler, and it smells like paper and floor wax and, under both of those, chalk."
    "The corridor is longer than the building looked from outside, which is becoming a theme."
    "Posters on both walls. A reading group, a film screening, a room for rent, three rooms for rent."
    "A lost cat that is almost certainly not still lost."
    hikari "Which one is yours?"
    mc "Sorry?"
    hikari "The posters. Everybody picks one on the first day. That is your department. The wall decides it."
    mc "(There is no way to answer that without guessing wrong, so I don't.)"

    # The first door in the game that can be shut, and it is shut by rank rather
    # than by points, so it reads as "he has not become that person yet" instead of
    # "you are half a point short". The other two are open on day one on purpose:
    # they are opinions, and he is entitled to have those before he has earned
    # anything. The locked one is the only one that asks him to have *noticed*
    # something nobody pointed out to him.
    menu:
        "The film one.":
            mc "The film one. Somebody put that up because they wanted other people to see a thing they liked."
            hikari "That is the most accurate sentence anybody has ever said about that poster."
            $ remember("hikari", "picked the film screening poster")
        "The three rooms for rent.":
            mc "There are three of those. Three different flats, three different people who all took the same photograph."
            hikari "Everybody in this building is leaving somewhere, and everybody in this building is arriving somewhere."
            mc "(It is the same wall. That is either the most ordinary thing in Japan or the most frightening, and I can't tell which.)"
            $ remember("hikari", "picked the three rooms for rent")
        "[tag_insight] The lost cat." if has_attribute("insight", 2):
            mc "The cat one. The tape has gone yellow and both bottom corners have curled."
            hikari "...Huh."
            mc "Somebody put that up months ago, and it stopped being true a long time before that, and nobody has taken it down."
            mc "That's a whole person in one sheet of paper."
            hikari "Okay. That one. That's your department, and I'm not going to argue with it."
            $ reward_attributes_once("answer_wall_cat", [("insight", "small")], show="auto")
            $ remember("hikari", "picked the lost cat nobody had taken down")

    "She stops at the far end, in front of a set of double doors, and reads a timetable taped to the glass."
    hikari "Right. That's your first lecture. History, four floors up, and we have about ten minutes."
    mc "We're going up?"
    hikari "We're not going up. Not yet. You have to see student relations first."
    mc "Student Relations?"
    hikari "Student relations. Everybody has to go there when they first enroll."


################################################################################
## ACT THREE, SEVENTH BEAT: STUDENT RELATIONS
################################################################################
##
## The scene that explains the rules of the game to the player without once
## saying so. Attendance is the spine of it, because attendance is the thing the
## simulation will be measuring him on, and he does not know that yet.

label student_relations:

    scene bg_student_relations with walk_fade

    "A counter, and behind the counter a young woman who has the calm of someone who has seen every version of confused there is."
    clerk "Ah. You'll be the new one. [player_name] right?"
    mc "Yes. How did you..."
    clerk "Your file is open on my screen. It has been open since eight."
    hikari "Told you."
    clerk "Sit, both of you. This is not a test, and it is the only time anyone here will explain this slowly."

    clerk "First, your gakuseishou. Student card. You need it for everything."
    clerk "And you will lose it, so you keep it in the same pocket every single day."
    mc "(Gakuseishou. I got that one from the gakusei. I have heard gakusei about two hundred times since I landed.)"
    "She slides a laminated card across the counter. My photograph is already on it."
    mc "(I do not remember having my photograph taken.)"
    $ add_item("student_card")

    "I sit. Hikari sits beside me and folds her arms like someone settling in to watch a play she has already seen."
    clerk "Attendance. At most universities it is a suggestion. Here you will find that it is not."
    clerk "In every class you are marked present, absent, or late."
    clerk "Sit down before the bell and you are present. Walk in after it and you are late."
    mc "Late. That's all it is?"
    clerk "Three lates make one absence. Three absences in a course and you are not allowed to sit the final exam."
    clerk "You still attend. You simply do not get the mark."
    mc "(There is no version of that maths that I like.)"
    hikari "It's not as bad as it sounds."
    clerk "It is exactly as bad as it sounds, and you should tell him the truth."
    hikari "It is a little as bad as it sounds."

    clerk "Electives. Your department classes are fixed. Everything else you choose, in the first two weeks, on the system."
    clerk "Choose early. The good ones fill in a day, and the people who decide in the second week are choosing from what is left of them."
    mc "How do I know which ones to take?"
    clerk "You don't. Nobody does. Take one you need and one you are curious about. It is always the curious one you remember."
    clerk "There is a list. It is long. Take the list and do not lose the list."
    "She slides a printed booklet across the counter. It is, in fact, long."

    clerk "And circles."
    mc "Circles?"
    hikari "Clubs. Here they're called circles."
    clerk "You are adults now. Nobody makes you join anything and nobody makes you stay."
    clerk "That is the whole difference from where you came from."
    clerk "There is a reading circle. It is four people and a great deal of silence."
    clerk "There are language courses. Japanese, for the exchange students."
    clerk "The ones who take them seriously are the ones who stop needing me to read their post."
    clerk "There is a photography club. They call it Circle. It argues constantly and takes good photographs anyway."
    clerk "There is a hiking group that will try very hard to recruit you at the gate on Thursday."
    hikari "They got me."
    mc "(I believe her.)"
    clerk "And a number of other things under the gym, which you will find on your own and which I am not responsible for."

    # The second door that can be shut, and the first one gated on Grace. What is
    # behind it is not information - she has already given him all of that - it is
    # the kind of sentence you can only say to a stranger once you have decided to
    # be a person in front of them, which is exactly what Grace has been measuring
    # since the airport.
    menu:
        "Which one would you pick?":
            mc "If it was you. Out of all of them. Which one would you pick?"
            clerk "The reading circle. Four people and a great deal of silence, and they have never once asked me for anything."
            clerk "That is the highest praise I can give a circle."
            $ remember("clerk", "asked which circle she would pick")
        "I'll go and look at the photography one.":
            mc "The photography one. I'll go and find out what they argue about."
            clerk "They will argue with you on the first day. It is how they say hello."
            mc "(I have had one conversation in this country and I have already committed myself to a second one.)"
            $ remember("clerk", "said he would go and find the photography club")
        "[tag_grace] I'll come back." if has_attribute("grace", 2):
            mc "I'll come back. Not just when something breaks."
            clerk "..."
            clerk "I have worked this counter for twenty years. Students do not come back."
            clerk "I will hold you to that, [player_name]. It is a small thing and I will still hold you to it."
            $ reward_attributes_once("answer_circles_back", [("grace", "small")], show="auto")
            $ remember("clerk", "promised to come back when nothing was broken")

    mc "Thank you. Really."
    clerk "You are welcome. Come back when something breaks. Something always breaks."
    clerk "Now go. History starts in four minutes."
    mc "Four minutes?"
    "Hikari is already standing. She was on her feet before the clerk finished the sentence."
    hikari "Sorry. That one is on me. I'll see you up there."
    mc "You're leaving me?"
    hikari "If I walk in with you, we're both late. Only one of us gets to be."
    "She is through the door before I have stood up, and it swings shut behind her without a sound, which is somehow worse than a slam."
    clerk "The building is not small, [player_name]."
    mc "(She said it like a fact. Everything here is said like a fact.)"


################################################################################
## ACT THREE, EIGHTH BEAT: THE FIRST LECTURE
################################################################################
##
## The strict professor, and the first rule in Japan that he breaks without ever
## knowing it existed. The lecture topic is chosen on purpose: a country getting
## smaller is the premise of the whole game, and he hears it as a history lesson.

label first_class:
    stop music fadeout 3.0
    scene bg_lecture_hall with walk_fade
    play music "audio/Music/classroom.mp3" fadein 1.0

    "Four floors, and the stairs are exactly as bad as she said, and the door at the top is heavy and it opens inwards."
    "There is nobody on the stairs. There is nobody in the corridor either, and that is the part that is wrong."
    "The building went quiet while I was being told about electives."
    "Forty people look up at once."
    "At the front, a man in a grey cardigan stands half turned to a blackboard already covered in dates."
    "He does not turn around. He finishes the word he is writing, and then he turns around."
    professor "You are late."
    mc "I know. I'm the new one."
    "And then I see her."
    "Third row from the front, by the window. Notebook open. Pen out."
    "Sitting exactly where she would have sat if she had been here since breakfast."
    "Hikari. She does not look up."
    mc "(She left me at that counter and she is already inside and settled, and there is an empty seat beside her.)"
    "I start walking towards it."
    professor "I asked you a question."
    mc "Sorry. I'm just going to..."
    "Her hand closes around my sleeve and pulls. Hard."
    "I go down into the seat beside her, and the chair makes a noise the whole room hears."
    hikari "Don't answer him. Sit down. Say sorry and sit down."
    professor "I do not care who you are."
    professor "I asked who you are. I withdraw the question. It does not matter."
    "He has not looked at Hikari once. She came in before the bell, so as far as this room is concerned she is part of the furniture."
    mc "(He is not angry at the room. He is angry at me. It is a very specific kind of being looked at.)"
    professor "Sit. Come to me when the class ends."
    "Then he says something short and flat in Japanese, to the board rather than to me."
    "The room absorbs it the way a room absorbs weather."
    mc "(Not one word of that was for me. I hope.)"

    "Somewhere behind us a chair drags and nobody looks at us, which is somehow worse than if they had."
    "Beside me, Hikari has gone back to her notes as though she has been sitting here the whole time. She has."
    mc "(Nobody is late to his class.)"
    mc "(I have been in this country for one day and I have already broken a rule I did not know existed.)"
    "On the board the dates are old. 1945. 1960. 1990. And then a column of numbers, all the same shape, all of them going down."
    "He writes the last one and underlines it twice."
    professor "Every generation since is smaller than the one before it. That is not a mystery. It is arithmetic."
    professor "By the time the people in this room are my age, there will be fewer of you than there are seats."
    professor "The country has to decide what it does about that. And it is deciding. Slowly, and in rooms like this one."
    mc "(Something in my chest goes cold for a moment and does not say why.)"
    mc "(I'm tired. Long flight, longer morning. That's all it is.)"

    "The hour ends and he closes his notebook on a sentence he does not finish, and forty people stand up at once."
    hikari "Go."
    mc "You're not coming?"
    hikari "It's you he wants. I'll be by the door."
    show sister_standing
    hide sister_standing with Dissolve(3.0)
    

    "I walk to the front. It is a long walk, and the room empties around me the whole way, and it is emptier when I get there."
    mc "Professor. I wanted to introduce myself properly. I'm [player_name]. I'm the exchange student."
    professor "I know what you are. I read your file. That is not what this is about."
    professor "This is about the clock."
    professor "You believe you were on time. Arrive at the bell, sit between the bell and my first word, and you have lost the first word."
    professor "Do that three times and you have lost the class."
    professor "If it happens again there will be consequences. I do not say that as a threat. It is a description."
    mc "I'm sorry. I don't think I understand what I did wrong."
    professor "You were on time."

    # The third and last door in this pass, gated on Nerve, and deliberately the
    # one that opens onto the best outcome in the scene. Asking a professor who has
    # just finished dismissing you to say the thing again is not a smart answer, it
    # is a bold one, and it is the only reason he ends the day with something he can
    # actually use. The two open answers are honest and neither of them gets him it.
    menu:
        "Let him finish.":
            mc "..."
            $ remember("professor", "took the dismissal without arguing")
        "Apologise properly.":
            mc "I'm sorry. I'll be here early from now on. I mean it."
            professor "Yes. You will."
            $ remember("professor", "apologised and promised to come early")
        "[tag_nerve] Say that again. Slowly." if has_attribute("nerve", 2):
            mc "Could you say that again? Slowly. I would rather ask you now than get it wrong for a year."
            professor "..."
            professor "Yes. That is the correct question. Nobody in this room has ever asked it."
            professor "Five minutes before. Always. Write it on the front of your notebook and do not write anything else there."
            mc "(I don't think I have ever been given advice and a warning in the same sentence before.)"
            $ reward_attributes_once("answer_clock_ask", [("nerve", "small")], show="auto")
            $ remember("professor", "asked him to say the rule again, slowly")

    professor "Coming on time is late."
    professor "You are seated, ready, notebook open, pen out, five minutes before the class begins."
    professor "If you are still doing any of that after the bell, you are late."
    "I open my mouth to say something sensible and find that I do not have anything sensible."
    mc "(My whole life, on time has meant on time.)"
    mc "(He just told me that on time is late, and he was not joking, and not one person in that room would have disagreed with him.)"
    mc "(That is the rule that is going to take me the longest.)"
    professor "Go."
    "He turns back to the board before I have moved, which is its own kind of dismissal. I leave the class."
    play music "audio/Music/school.mp3" fadein 2.0
    scene bg_department_hall with walk_fade

    "At the door Hikari is waiting with her arms folded, watching the corridor the way a person counts something."
    hikari "Well? How did it go?"
    mc "I think I just got in trouble for being on time."
    hikari "You did."
    mc "And that went better than expected?"
    hikari "It went better than expected."
    mc "How?"
    hikari "Because you didn't argue with him. Everybody argues with him. It's the first thing everyone does."
    hikari "And then it is five minutes of shouting and a term on his list."
    mc "There's a list?"
    hikari "There's always a list."
    mc "(She is cheerful about this as well. I am starting to think cheerful is just how she carries things.)"
    hikari "You're fine. Honestly. That was practically a welcome."
    mc "Hikari. Why was nobody else late?"
    hikari "Because nobody is late. By Friday you'll be sitting in there at eight fifty-five with everyone else."
    hikari "And it will feel like the most normal thing in the world."
    mc "(I don't think it will.)"
    mc "That's why you went on ahead. At the counter."
    hikari "Mm."
    mc "You knew that if we walked in together, we would both be late."
    hikari "I knew."
    mc "Then why didn't you say anything? Two sentences on the way up. I would have listened."
    hikari "No, you wouldn't."
    mc "..."
    hikari "You'd have heard 'on time means five minutes early' and you'd have nodded."
    hikari "And you'd have filed it under one man in a cardigan being difficult. Everybody does. I did."
    hikari "You had to be the one he said it to. Now you know it in your body instead of your head, and I never had to say a word."
    mc "(The clerk explained everything to me slowly, because that is what she is there for.)"
    mc "(Hikari explained nothing at all, and I have learned more from her in ten minutes than I did from the whole of that counter.)"
    mc "(I don't know if that is kind. It worked.)"
    mc "(But I'm standing in a corridor four floors above a courtyard that swallowed a city.)"
    mc "(In a building I get to keep for the next year, and I have survived my first hour.)"
    mc "(Two days in. One hour of class. One rule, learned the hard way.)"
    hikari "Come on. I'm hungry, and I know a bad cafeteria and a worse one."
    mc "You said there were two."
    hikari "There are two."
    mc "..."
    hikari "Or don't. It's your first free afternoon. Nobody here is going to tell you what to do with it."
    hikari "And I am not going to be the first."
    mc "(She has been handing me this day since the platform. Now she is handing it back.)"

    # The first hour of the game that belongs to him, and the choice is deliberately
    # not a list of places. Hikari asks a question a person would ask, and the three
    # answers are three things he would actually say. Where each one leads is the
    # game's business, not his, so the player picks a shape of afternoon and the
    # script does the geography. Naming a destination here would give away a city
    # he has not been shown yet.
    menu:
        "I want to learn the way home.":
            mc "I'm going to walk back. On my own. If I don't learn the way now I'll never learn it."
            hikari "You'll get lost."
            mc "Probably. That's how I'll learn it."
            hikari "..."
            hikari "Don't take the west exit. That's the wrong one. That's all you're getting."
            $ first_day_activity = "walk_alone"
        "I'll come with you.":
            mc "I'll come. On one condition. Somewhere on the way you show me something other than the cafeteria."
            hikari "There is a lot of better places than the cafeteria."
            mc "(She answered before I finished the sentence. She has been waiting for the company since the corridor and did not say so.)"
            $ first_day_activity = "walk_hikari"
        "I want to find the photography club.":
            mc "The photography one. The clerk said they argue constantly. I want to know what about."
            hikari "Second floor, end of the corridor, the door with tape on it. They don't lock it."
            mc "You know where it is."
            hikari "Everyone knows where it is. Nobody goes in."
            $ first_day_activity = "photo_club"

    # Said once, and only after he has picked, so the explanation of the free
    # afternoon arrives with something already happening underneath it.
    if not store.after_school_hint_shown:
        $ store.after_school_hint_shown = True
        $ renpy.call_screen("hint_card", eyebrow="A NOTE ON THE AFTERNOON", body=store.hint_text_after_school)

    if first_day_activity == "walk_alone":
        jump after_school_walk_alone
    elif first_day_activity == "walk_hikari":
        jump after_school_run
    else:
        jump after_school_photo_club


################################################################################
## ACT ONE, NINTH BEAT: THE FIRST FREE AFTERNOON
################################################################################
##
## Three ways to spend it, and all three end the day at night, because the break
## between this act and the next one is a night rather than a landmark.
##
## Everything inside these three labels is day-one content. The visit counters
## they set are what the hub reads later; one outing, one scene, and the outing is
## gone. Nothing here can be walked back into and farmed.

label after_school_walk_alone:

    scene bg_school_gate with walk_fade
    stop music fadeout 2.0

    "We come out through the gate. At the corner she stops, because she has worked out that I am not turning the way she is."
    hikari "Last chance. I'm going that way."
    mc "I'm going this way."
    hikari "..."
    hikari "Don't take the west exit."
    mc "(Here we go. First time navigating this city on my own.)"

    scene black with walk_fade

    "The street I turn into is already in shadow, and it is not the shadow of a building. It is the time of day."
    "Was it this left? or the next one? Maybe I passed it?"
    "I remember a crossing with mirrors on the poles. A bakery with a cat painted on the glass. I do not remember which came first."
    "So I take a turn, on the grounds that it looks like a turn."
    "Ten minutes later the road is narrow. No mirrors on any pole, no cat on any window, and two convenience stores in a row."
    mc "(That is wrong. Somewhere behind me I chose, and I chose badly.)"
    mc "(She told me twice not to take the west exit. I did not take the west exit. I found a different wrong one.)"
    "I take the phone out of my pocket. It has a map on it."
    mc "Dang it, I forgot that I don't have reception yet!"
    mc "I need to get a data plan soon if I want to navigate around the city by myself better."
    "Then I put it back."
    "So I keep going, in the direction that feels like the direction, which is a method I have now disproved in practice."

    scene bg_alley with walk_fade

    "The sun goes down off the roofs while I walk. First the whole street is gold, then only the top floors are, then nothing is."
    "The streets get quieter. Not empty, nothing here is ever empty, but quieter, and the shops stop looking like they are for passers-by."
    "And then the lights on the poles come on, all of them at once, in a line, starting at the far end and coming towards me."
    mc "(It is getting dark. Eleven minutes. It was supposed to take eleven minutes.)"

    "And then I smell it."

    # The chef's first visit. The dialogue follows the beat sheet in
    # Dialogue/Locations/Ramen Shop - Chef/1st interaction.md: he points at a line
    # he cannot read, gets a bowl he did not order, and answers in the one Japanese
    # word he owns. The shop pays nothing for being entered; the point is his.
    scene bg_ramen_shop with walk_fade
    play music "audio/Music/ramen_shop.mp3" fadein 2.0

    "Broth, and steam, and fat hitting a hot pan behind a wall. My whole body turns towards it before I have decided anything."
    "A doorway with a cloth over it, dark blue and gone soft at the hem. A bowl painted on it in white. No glass, no sign I can read."
    "I lift the cloth and go in."



    "It is four seats and a counter and a wall of steam, and the steam is the only thing in here that moves."
    "There is one man behind the counter, in an apron and a towel tied around his head, and he does not look up."
    "The board on the wall is handwritten and I cannot read one character of it."
    "Under it, the prices in numbers, which everybody can read."
    "I put a thousand yen on the counter. He does not look at it."
    "He pushes it back with one finger and grunts at the empty space in front of the seat, which I take to mean afterwards."

    chef "いらっしゃい。"
    mc "(I know that one. Every shop in this country says it when a person walks in. It means welcome, and it means get on with it.)"

    # How he orders. All three roads end in the same bowl, because the chef is the
    # one steering and the protagonist has none of the language; what the player is
    # actually choosing is what kind of person he is when he cannot be understood.
    menu:
        "Order in English.":
            mc "Uh... hi. Ramen, please?"
            "He looks at me properly for the first time, about a second, and then he waves at the board. The whole board."
            mc "(That was not a no. That was him telling me that the menu is the menu.)"
        "Point at something.":
            mc "(Right. Fine. This is the part where I point.)"
            "I point at a line. Any line. The second one down, because I have seen one of its words on a packet in the kitchen."
            "He glances at where my finger is, and then at me, and his face does not move at all."
        "Ask him to choose.":
            mc "You choose. Whatever's good."
            "He stops. He looks at me a second longer than he looked at the money, and then says something short to the pots."
            mc "(It was not an answer. It was the closest thing to one I am going to get.)"
            mc "(I handed the decision to a man who has not said a word to me. For no reason I could defend, I think that was correct.)"

    chef "あいよ。"
    "He barks something at somebody. There is nobody else in the room. He is the kitchen and the waiter, and he is barking at himself."

    scene bg_ramen with walk_fade
    
    "A few minutes later he puts down a bowl, and it is not what I ordered, and I am no longer certain I could say what I ordered."
    "The broth is almost black. More pork than noodle. And a hill of green onions on top of that which should not be legal."
    mc "(Whatever I did back there, this is not it. This is not remotely it.)"
    "He crosses his arms and looks at it, and then at me, which is a sentence in a language I can read."

    # Both answers end in the same mouthful. What the player picks is whether he is
    # the sort of person who sends food back in a country where he cannot say the
    # words to send it back with.
    menu:
        "Say something.":
            mc "Uh... sorry. I think this is - this isn't what I -"
            "He watches me do it. He does not help. He does not move. He lets me run out of sentence."
            mc "(He is not being unkind. He is waiting for me to finish being a person who is about to send this back.)"
            "I stop talking. He pushes the bowl half a centimetre towards me with one finger."
            chef "どうぞ。"
            mc "(That one I know. It means here you go. It also means eat it.)"
        "Eat it anyway.":
            "I pick up the spoon before I can think about it, which he appears to consider the entire conversation."
            chef "どうぞ。"
            mc "(That one I know. It means here you go. It also means eat it.)"

    "I eat it."
    "The first mouthful hits like something walking into a door. Rich and smoky and far too much. The second is better than the first."
    mc "...This is actually amazing."
    "I say it half under my breath, in English, to nobody."
    "He hears the tone of it even if he does not have the words. He does not turn around."
    chef "うまい、だろ？"
    "I catch one word of that. One. It is the word on the packet in the kitchen and on the sign two doors down from the house."
    mc "Umai! Yes! Very umai!"

    "He snorts. A small sound, killed immediately. Something in his face moves for a quarter of a second before he turns back to the pots."
    "He says nothing else. I slurp, badly, and get broth on the counter, and he does not comment."
    "I am fairly sure that is the compliment."

    # All three ways of ordering and both answers end in this same bowl, so the rest
    # of the meal is not a choice and is not played out. It is summarised on black,
    # and every route comes back through it to the same empty bowl, the same bill,
    # and the same walk home.
    scene black with Dissolve(2.0)
    "I ate the rest of it watching the men either side of me, and did what they did."
    "Chopsticks in one hand, spoon in the other, head down over the bowl."
    "I ended up finishing the whole bowl, soup and all. There was nothing left in it but the pattern on the bottom."

    scene bg_ramen_empty with Dissolve(2.0)

    "When I finish I put the thousand yen back on the counter."
    "This time he takes it, counts the change without looking, and sets it beside my hand."
    $ spend_money(900)
    "A hundred yen. Nine hundred for the bowl. I do not know what I actually ordered and I do not think I ever will."
    mc "(That was the wrong bowl. But I would order it again.)"

    $ confidant_visits["chef"] = 1
    $ reward_attributes_once("chef_first_umai", [("grace", "small")], show="auto")
    $ remember("chef", "sat down in a shop he could not read and said the word back to him")

    # Back to the counter shot for this, for the same reason the whole scene
    # works this way: he does not say anything that is not sitting in front of
    # him, and this is going to happen across a counter. The fade is also what
    # gives the memory notice above its full time on screen before the phone
    # takes the whole frame.
    scene bg_ramen_shop with walk_fade

    "He has been looking at the phone on the counter since I put the money down."
    chef "「WIRE、やってるか」"
    "Two English sounds, dropped into a Japanese sentence, at the exact volume of the pots."
    mc "(I caught the whole thing. I have no idea how.)"
    mc "Yeah. My sister put it on here. Hikari. She set the whole thing up before I landed."
    "He grunts, which is what he does instead of a nod."
    "Then he turns a small laminated card round on the counter so that it is facing me."
    "A black square made out of smaller black squares. Under it, six words in English, in handwriting that is not his."
    chef "「読め」"
    mc "(Read it. That one is no mystery either. I am learning to read this room instead of the language.)"
    "I hold the phone over the card. The app takes it without asking me anything, and puts a name on the list."
    mc "So I know if you're shut before I walk down here for nothing."
    "He turns the card back round and goes to the pots, which is the conversation over."
    $ wire_unlock("chef")

    mc "(Home. Four minutes. Let's see if I can find it twice.)"
    "I come out from under the cloth and the street is dark, and I know exactly where I am."
    "Those two convenience stores are twenty metres away."
    mc "(That sign. That one there. I know that street.)"
    mc "(I was on it this morning, on the way to school, and I did not look at it once.)"
    "Home is four minutes away and it took me an hour to do it, and I would do it again exactly the same way."
    mc "(I found a ramen shop. I found it by getting lost, which means it was always findable. It was there the whole time.)"

    scene bg_home_exterior_night with walk_fade
    $ night_street()

    "It is properly dark by the time I reach the gate, and I do the arithmetic and do not like the answer."
    mc "(Late. On the first day. I have been in this country for two days and I am already late.)"

    scene bg_home_night with walk_fade

    "Hikari is in the kitchen with a cup she stopped drinking from a while ago, and she does not pretend not to have been waiting."
    hikari "You're late."
    father "Where have you been?"
    mc "I got lost."
    hikari "You got lost."
    mc "Everything was going well, then one wrong turn, and then a couple of hours of wrong turns. I didn't know where I was."
    father "Listen, I know you are an adult but this house has rules, and one of them is don't come home past eight o'clock."
    hikari "Come on, Dad. He said he got lost!"
    father "Anyways. Don't make it a pattern. I am going to bed. So should you."
    father "You still have school tomorrow."
    show father_standing
    mc "*I nod with my head.* (He goes to bed.)"
    hide father_standing with dissolve
    mc "Sorry Hikari, I should have listened and come home with you."
    mc "But on the bright side, I found this ramen place with a red lantern over the door."
    mc "Four seats. One man. He gave me a bowl I didn't order, and it was the best thing I've eaten here."
    hikari "..."
    hikari "The one near the two convenience stores."
    mc "You know it?"
    hikari "Yes I do. I go there sometimes, when I don't want to be in this house."
    mc "(That is the first thing she has told me about this house that she chose to tell me.)"
    hikari "Go to bed. You look tired."
    jump end_of_first_day


label after_school_run:

    # Hikari's first run. This is the sister's arc rather than a numbered confidant
    # chain (see her character file): a recurring after-school activity, not seven
    # meetings at one address, and the thing it is really tracking is her.
    #
    # Planned shape, for when it is written out:
    #   1  the first run, and how badly it goes
    #   2  the route, and how precisely she already knows it
    #   3  the evening he keeps up, and what that costs her
    #   4  the night neither of them says anything, on purpose
    #   5  the rain, the bridge, and the first true thing she says about the house
    #   6  the evening she asks him to run somewhere that is not home
    #   7  the last one, and the thing she has been running from

    scene bg_home_exterior_day with walk_fade
    stop music fadeout 2.0

    "We walk. Eleven minutes, the same eleven minutes as this morning, and this time I know which bakery is the one to ignore."
    "She talks the whole way. The professor. The clerk."
    "A vending machine on the corner that has been out of the same drink for two months."
    "I have worked out that she fills silences on purpose. I have not worked out why."

    menu:
        "You didn't have to walk me back.":
            mc "You didn't have to walk me back."
            hikari "I know."
            mc "That wasn't the point. The point is that you did."
            hikari "You're welcome. Don't make it a thing."
        "You know every corner of this street.":
            mc "You know every corner of this street."
            hikari "I've walked it a lot. That is the entire secret of knowing a street."
        "You could have left me at the gate.":
            mc "You could have left me at the gate, like everyone else."
            hikari "..."
            hikari "I answered every email you sent this year. That was my job."
            hikari "Walking you home is the same job. I'm just doing it where you can see it."

    "We get to the house and she does not go in."
    "She walks past it, to the corner, and stops, and starts doing something to her shoes."
    mc "(She is not going inside.)"
    hikari "Don't go in yet. If you sit down now you won't get back up. I've known you a day and that's already your method."
    hikari "I'm going out again. Same as every day."

    menu:
        "Out where?":
            mc "Out where?"
            hikari "The river. Two or three times a week, except the weeks it's five. Tonight counts."
        "You run. At this hour.":
            mc "You run. At this hour, on your first evening off."
            hikari "There's no evening off. There's just the part of the day nobody's watching."
        "Can I come?":
            mc "Can I come?"
            hikari "..."

    hikari "You can come. Go and change into something you can move in."
    mc "You're serious."
    hikari "I'm waiting outside. Don't take an hour."

    window hide
    scene black with Dissolve(1.5)

    mc "(Upstairs, I find the one pair of things in that case that was never meant for a classroom.)"
    mc "(Trainers I bought the day before I flew and have not once used. A shirt I do not mind ruining.)"
    mc "(Four minutes. It is the first thing I have done in this country that nobody told me to do.)"

    scene bg_home_exterior_day with walk_fade
    $ hikari_run = True

    "She is outside at the bottom of the steps with her arms crossed and her weight on one foot."
    "Same person, different clothes. Shorts, and a top that has been rained on a hundred times."
    mc "(She looks like somebody else. I decide not to say so.)"
    hikari "Why did that take so long?"
    mc "Four minutes."
    hikari "Exactly. Nobody changes in four minutes."
    hikari "Come on. I'll take you through my usual route."

    window hide
    scene black with Dissolve(1.5)

    "We walk for a while."
    "She sets a pace and then forgets me for about ten minutes, which I have decided was the test."

    scene bg_river with walk_fade

    "The path along the water goes further than I can see. A fence, a row of trees."
    "Every few hundred metres, a vending machine lit like an aquarium."
    "There is nobody else out here. The whole city is behind us, and it makes no sound at all."

    mc "This is the route?"
    hikari "Half of it. Four and a half kilometres to the second bridge. Tonight we're doing this much and turning round."
    mc "(She did not check anything. She said it the way a person says their own phone number.)"

    "She stretches against the fence, the way a person does something they have done four hundred times."
    hikari "Ready?"
    mc "I haven't run since I was seventeen, and I didn't want to then."
    hikari "Then there's nothing to ruin."

    "She goes."
    "She said she would go slow, and then she went."
    "Ninety seconds later I understood that slow had been the last kind thing she meant to say."

    "Twenty minutes later I am on my knees at a vending machine with my hands on my thighs."
    "She is not out of breath. She has bought us both something without asking, and mine is an energy drink I would never have chosen."
    mc "(She picked the one I would have picked. I don't know how she knew.)"
    hikari "You're not unfit. You're just new. Those are different things and it's rude to confuse them."
    mc "Thank you."
    hikari "That wasn't a compliment. That was a diagnosis."

    "We drink them standing up, under the lamp, with the river doing the thing rivers do."

    menu:
        "(Say nothing.)":
            "I don't say anything, because she has filled every silence today, and this is the first one she left open."
            hikari "..."
            hikari "Yeah."
        "Do you do this every day?":
            mc "Every day?"
            hikari "Most. The days I don't, I'm in the house, and I don't like who I am in the house on those days."
            mc "(That is the first thing today that she did not put a smile on top of.)"
        "Why the river?":
            mc "Why the river?"
            hikari "Because it goes one way and comes back the same way and it never asks me anything."
            mc "(She said that like a joke. She did not say it like a joke.)"

    mc "You come out here instead of going home."
    hikari "I come out here. It's the only hour of the day that's mine."
    hikari "You run until your head goes quiet. The first ten minutes are just your legs arguing with you."
    hikari "And then it stops hurting in the bad way, and everything goes easy. People call it the runner's high."
    hikari "It's real. It's why I'm out here and not in there."
    mc "(That is the most she has said all day, and she said all of it without slowing down once.)"

    hikari "Right. That was your lap."
    mc "That was not a lap."
    hikari "It was a lap. A generous one. Same time next week?"
    mc "Same time next week."
    hikari "Good. I wasn't asking."

    $ first_run_started = True
    $ hikari_visits = 1
    $ reward_attributes_once("run_first_river", [("nerve", "small")], show="auto")
    $ remember("hikari", "ran the river path with her on the first afternoon")

    # She is the one who put WIRE on the phone in the first place, so she is the
    # one who explains what it is for. She does it the way she does everything:
    # quickly, while looking at something else.
    hikari "Give me your phone."
    mc "Why."
    hikari "Because I'm not explaining it twice."
    "She takes it out of my hand, which is turning into how the two of us do things."
    hikari "You still have WIRE on there. I put it on before you landed."
    mc "I know. I never opened it."
    hikari "Open it."
    "I open it. It is a list, and her name is not on it."
    hikari "Add me."
    mc "..."
    hikari "Add me, so I can tell you things I'm not going to say in that kitchen."
    mc "(She says that at exactly the speed she says everything else, and she does not look at me while she says it.)"
    "I add her. She watches my thumb do the whole thing, which means she could have done it in half a second."
    hikari "Good."
    mc "Is that it?"
    hikari "That's it."
    mc "(It is not it.)"
    $ wire_unlock("hikari")

    "We walk back. Twenty minutes this time, because neither of us is in a hurry."
    "She talks less on the way back. Not nothing, less."
    "And the less she says, the more it sounds like something she does not do in front of people."

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    $ hikari_run = False

    "The house is dark except for the kitchen, and the kitchen is the wrong window to be lit at this hour."
    mc "(It is properly dark. I do not know how long we were out there.)"
    hikari "Ah."
    mc "Ah?"
    hikari "Kitchen light. That's them being awake."

    scene bg_home_night with walk_fade

    "Mother and Father are at the table, and neither of them is doing anything, which is how I know they have been waiting."
    mother "You are both very late."
    father "It is a school night. You are in this house by eight. That is the rule, and it is not a new rule."
    hikari "I know. I'm sorry."
    mc "It's my fault. I asked her to show me the river."
    father "..."
    father "The river."
    mc "The path along it. I didn't know how far it went."
    "Hikari does not correct me, which for a second is louder than anything she has said all day."
    mother "You could have sent a message. One message would have done."
    hikari "We got talking, and then we were halfway there, and we lost track of it."
    father "Lost track."
    hikari "We got lost in the conversation. It won't happen again."
    father "..."
    father "Eat something before you go up. There is rice."
    mc "(That is the whole punishment. It is somehow worse than shouting.)"
    hikari "We're fine. Goodnight."
    jump end_of_first_day


label after_school_photo_club:

    # Sim, as his character file has him: relentlessly positive, generous with
    # everything he has, and incapable of putting himself first. He does not
    # complain about his day job, his rejections, or his years of trying, and he
    # does not gossip about anybody in this room. What he says about other people
    # is always to their credit, and what he says about himself is always smaller
    # than the truth. The warmest thing he ever says lands on somebody else.
    #
    # He is not a student: he comes in from outside to guide the club, and the club
    # is called Circle.
    #
    # Planned shape of the seven visits, for when it is written:
    #   1  the argument, and the fact he arrives with nothing to shoot
    #   2  the club learns his name, and the basics, in two languages at once
    #   3  the first frame that is actually his, and Sim prouder of it than he is
    #   4  the club filling up, and the exhibition Sim introduces as somebody else's idea
    #   5  the quiet week, and the reason he started Circle, told as a joke
    #   6  the editor's email, and the promise he makes to the room
    #   7  the exhibition, and the strap he gives away

    scene bg_campus_interior with walk_fade
    stop music fadeout 2.0

    "The corridor on the second floor is longer than it has any right to be."
    "At the end of it is a door with a strip of tape down one side."
    "The tape is agreeing with the wall that the wall has won."
    "There is no proper sign. A sheet of printer paper, two words on it in marker, in English, and a circle drawn under them by hand."
    mc "(Circle. That is either the name of the club or a warning about the door.)"
    "I can hear them before I can see them. Two voices, going at it."
    mc "(They argue constantly. It is confirmed. I am outside the door and it is already confirmed.)"
    "I open the door."

    scene bg_photo_club with walk_fade

    "Someone has taken every chair in this room and put it in a rough circle. There are six people in it. None of them looks up."
    "One wall is covered in prints held on with the same tape."
    "Half of them have been written on in marker by somebody who was angry at the time."
    "Two of them are going at each other over a print, fast and cheerful, and nobody else is troubled by it."
    "It is just the sound this room makes."
    "Then one of them notices me, and the argument stops mid-sentence, and the whole room turns round at once, which is worse."
    sim "Ah! you must be the new one. Welcome, welcome. Come in, don't be shy. The doorway is the worst seat in the room."
    "He looks a little older than everyone else here."
    sim "Everyone. Everyone - this is our first-timer."
    sim "「初めて参加のお方です！みなさん、どうぞよろしくお願いします！」"
    "The room says it back at me in one voice. Somebody waves. Somebody takes a bag off the chair beside him and puts it on the floor."

    menu:
        "I found the right door, then.":
            mc "I found the right door, then. The paper one."
            sim "You did. No fees, no pressure, just us and some cameras and a great deal of trial and error."
        "So do I look like a lost tourist?":
            mc "So... do I look like a lost tourist?"
            sim "(grinning) Maybe a little. But that is the perfect place to start from. Most of us began exactly there."
        "I wasn't sure this was the right room.":
            mc "I wasn't sure I had the right room. There's tape on your door."
            sim "Then you did. See? You found it anyway. The tape just made it take longer."

    "I sit in the gap, which is exactly one person wide, next to a boy asleep with his arms folded and entirely committed to it."

    sim "So. Here is the whole club, and then you can decide about us."
    sim "Some come to build a portfolio. Some for the practice."
    sim "Some because they wanted somewhere to be on a Tuesday and this room was open."
    sim "Everybody gives what they have and takes what they need. It works both ways. Nobody pays, and nobody has to be any good."
    mc "(That is the second time in one day that somebody has explained a thing in this country by telling me what it gives other people.)"

    sim "So. Do you have a camera?"

    menu:
        "No. At least not today.":
            mc "Nothing. I got here yesterday. My camera is in a suitcase in a house I can't find my way back to."
        "Just my phone. Not well.":
            mc "Just my phone. I was caught off guard and didn't think of bringing it today."
            mc "So I can only shoot with my phone today."

    "I look at my hands, which are empty, and he follows my eyes down to them."
    sim "Then that is the best possible answer, and I am not saying it to be polite."
    sim "Phone cameras are better than most beginners realise."
    sim "And more usefully, if you had brought one, you would have spent the hour choosing a wall."
    sim "This way you have to look at the room first. The room is the part everybody skips."
    "He holds his hand out. I give a stranger my phone, which is a strange thing to do in a room I have been in for four minutes."
    "I do it anyway."
    "He turns it round, frames the light coming off the wall, and hands it back."
    sim "There. Now you have shot something. The light is wrong and it is crooked, and it is entirely yours."
    sim "See? First step. Half the prints on that wall started exactly like that one."

    sim "I should say who I am, since I am the strange one here. I don't study here. I come in twice a week because they let me."
    sim "By day I am in an office with the numbers. This is the other half of the day, and this is the half I would keep."
    sim "Ten years in this country, and I still feel like a beginner most days. I have decided that is the good part."

    menu:
        "You've been here that long?":
            mc "You've been here that long?"
            sim "Ten years. I came for one, and then this room happened, and a room like this is very hard to leave."
        "Do you ever think of leaving?":
            mc "Do you ever think of leaving?"
            sim "(shrugs) Sometimes. Then I think of this place. The people in it. It keeps me here, every time."

    "The woman from the argument says something across the room."
    "He answers her in Japanese without changing gear, then comes back to me in English."
    sim "「彼女が今日のモデル。今回のテーマは自然な笑顔だって。」"
    sim "She is modelling for us today, and the theme is a natural smile. Which means she is about to make every one of us work for it."
    sim "See? A little ecosystem. Everybody gets something."
    sim "She gets practice, they get their portfolio, and nobody has to be anybody's boss."

    menu:
        "And this is all volunteer?":
            mc "And this is all volunteer? Nobody is paying for any of it?"
            sim "Nobody pays for any of it. That is rather the point of it."
            sim "No client. No brief. Nobody to tell you what a good photograph is."
        "Sounds too good. What's the catch?":
            mc "Sounds too good. What's the catch?"
            sim "(grinning) The only catch is that once you come, you want to come again. That is the entire business model."

    sim "You don't have to join anything. Come. Sit. Look at what people put on the wall. That is the whole club."
    sim "Join us whenever you are ready. Everybody here started by sitting in that chair and saying nothing."

    sim "Right. Everyone."
    sim "「今日も楽しくやりましょう！」 Let's have fun today!"
    "The room cheers, lightly, the way a room cheers when it does this every week."
    "Somebody takes a print off the wall and starts arguing again."

    "He turns back to the prints and starts talking about one of them."
    "He does not ask me a single question about where I am from."
    "By the end of the hour I am fairly sure that is the kindest thing anybody in this city has done for me."
    mc "(Nobody has told me what to do tonight. Nobody has handed me anything.)"
    mc "(I am sitting on a plastic chair in a room that smells of fixer.)"

    $ confidant_visits["sim"] = 1
    $ reward_attributes_once("sim_circle_first", [("insight", "small")], show="auto")
    $ remember("sim", "walked into the circle with empty hands and was told it was the good answer")

    # He does not gate the club behind anything, so the group is the one thing he
    # has to give that costs him nothing and asks nothing. He gives it the same
    # way he gave the phone back an hour ago: like it was already mine.
    sim "Oh - wait. One thing before you go."
    sim "You have WIRE, don't you? Everybody in this room does."
    mc "My sister put it on my phone. I haven't really used it."
    sim "Then you are already most of the way in. That is the entire entry requirement."
    "He puts his hand out, the way he did an hour ago, and this time I hand the phone over without thinking about it."
    sim "There is a group. It is called Circle, and it is older than the room is."
    sim "Everybody posts what they shot that week, and everybody else says something about it. Mostly rude. Always useful."
    mc "And you want me in it."
    sim "(grinning) I want you in it because nobody in there knows your name yet, and that is a very easy thing to fix."
    "He gives the phone back with the group already open on it and my name already in the list."
    "He had it before I finished saying it this afternoon. I am not sure at which point he took it."
    $ wire_unlock("sim")

    "An hour later he walks me to the door and points down the corridor at the stairs. He tells me when they meet, and to bring nothing."
    "The nothing is the point, he says. Then he goes back in and shuts the door, and I can hear the argument starting again behind it."
    mc "(That is one place in this city I can find now without being shown.)"

    scene bg_home_exterior_night with walk_fade
    $ night_street()

    "It is properly dark when I get back, and I stand at the gate for a second doing the arithmetic."
    "Eleven minutes each way, twice, plus an hour in the room. That is not what the clock says."
    mc "(I stayed. Nobody told me to stay. I just stayed.)"

    scene bg_home_night with walk_fade

    "Hikari is on the stairs, sitting on the third step with her chin on her knees."
    "It is a thing I have not seen anyone do outside of films."
    hikari "You're late."
    mc "I know."
    hikari "I've been sitting here since dinner. Dad's been pretending to read the same page."
    mc "It's my fault. The club kept going and I lost track."
    hikari "The club."
    mc "The photography one. Second floor."
    hikari "You actually went in."
    mc "I actually went in."
    hikari "..."
    hikari "Good."

    father "Is that him?"
    "Father comes out of the kitchen with a dish towel he is not using."

    father "You are late."
    mc "I'm sorry."
    father "Hikari told us where you were. That is the only reason this is a conversation and not a rule."
    father "Eight o'clock. On a school night. We eat together, and we eat at eight."
    mc "I understand."
    father "Then eat. There is rice."
    mc "(That is the whole warning. It is somehow worse than shouting.)"
    hikari "Go on. Before he finds another sentence."
    jump end_of_first_day


################################################################################
## ACT ONE, TENTH BEAT: THE END OF THE FIRST DAY
################################################################################
##
## Every road out of the first afternoon arrives here. Whatever he chose, the day
## closes the same way: the stairs, the light off, and the whole of it played back
## in the dark. One label for all three, because the shape of the ending belongs
## to the day rather than to the place he ended it.

label end_of_first_day:

    scene bg_room_night with stair_fade
    $ room_ambient(True)

    "Upstairs, the door shuts behind me and the house goes quiet."
    "The quiet a house makes when everyone has agreed to stop talking about something."
    "I sit on the edge of the bed with my shoes still on and go through the day from the beginning."
    "I want to hear whether it sounds real."
    "A station at nine in the morning, and a sister who took me the long way for no reason she would give."
    "A professor who told me that arriving on time is late. A cafeteria I could not read."
    "And then an afternoon that belonged to nobody but me."

    if first_day_activity == "walk_alone":
        mc "(I got lost on purpose and it worked. That is the first thing in this country I have done by myself.)"
        mc "(Somewhere four minutes from this house there is a man who will not remember my face.)"
        mc "(And a bowl I will think about for a week.)"
    elif first_day_activity == "walk_hikari":
        mc "(I ran until I could not breathe, next to somebody who was not out of breath at all.)"
        mc "(She showed me a thing she does not show anybody, and then she walked me home and got shouted at for it.)"
    else:
        mc "(I walked into a room full of strangers and nobody asked me a single question about where I come from.)"
        mc "(There are prints on that wall with marker on them. Somebody was angry about a photograph. That is the whole club.)"

    mc "(Yesterday I got off a plane without knowing one word of the language.)"
    mc "(Today I went to school late, made a stranger laugh, found a place in this city, and came home after dark.)"
    mc "(I wonder if every day here is going to be like this.)"
    mc "(Full of new things, and surprises, and people who turn out to be nothing like the first thing you thought.)"

    "I lie back and look at a ceiling I have now looked at twice."
    "Out in the street somebody wheels a bicycle past, and then there is nothing at all."
    mc "(I would like every day to be like this one. I would like to be the sort of person this day was for.)"
    "I do not remember deciding to close my eyes."
    "They are heavier than they were a minute ago, and the lamp is further away than it was, and the day carries on without me."
    "Tomorrow there is a class at five minutes to nine, and nothing else written anywhere."
    mc "(Five minutes early. Notebook open. Pen out.)"
    "I mean to think about that. I am asleep before I start."

    window hide
    scene black with Dissolve(2.5)
    stop music fadeout 2.0
    return
