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

    # Rank-up cues are timed around the animation and should not cut off the
    # opening swell or be cut short by an unrelated one-shot sound.
    renpy.music.register_channel("attribute_ui", mixer="sfx", loop=False)

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
image bg_akihabara_hamada_outside = Transform("images/backgrounds/bg_akihabara_hamada_outside.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_akihabara_hamada_inside = Transform("images/backgrounds/bg_akihabara_hamada_inside.png", xysize=(config.screen_width, config.screen_height), fit="cover")
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
image bg_kitchen_night = Transform("images/backgrounds/bg_kitchen_night.png", xysize=(config.screen_width, config.screen_height), fit="cover")

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
default father_affection = 0
default sim_affection = 0
default orson_affection = 0
default chef_affection = 0
default aya_affection = 0
default hana_affection = 0

# True if he declined Hikari's first river invitation. The run still exists as her
# habit; he simply is not on it yet, and WIRE unlocks later at the house instead.
default declined_first_run = False

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

# The haiku lesson is the first topic the player is asked to study deliberately.
# Keep their chosen approach in save data so a later exam can acknowledge it.
default haiku_study_method = ""

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
# These are deliberately floats. Small choices can nudge an attribute by a
# tenth or a few tenths, and signed trade-offs can lower one while raising
# another. Whole numbers would erase those distinctions.
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

# Transient feedback shown beneath the matching circle in the HUD.
default attribute_tick_events = {}
default attribute_tick_started = {}

# TEMPORARY: test-only shortcut target. Keeping this in script flow lets the
# rank-up animation start its own interactions safely.
label attribute_test_rank_up(attribute_id):

    $ ceiling = attribute_rank_ceiling(attribute_id)

    if ceiling is None:
        $ renpy.notify("%s is already at maximum rank." % attribute_name(attribute_id))
    else:
        $ add_attribute_points(
            attribute_id,
            amount=ceiling - attribute_total(attribute_id),
            show="card",
        )

    return

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
            renpy.call_screen("hint_card", eyebrow="Money", body=store.hint_text_money)
        return True

    def add_item(item):
        if item not in store.inventory:
            store.inventory.append(item)
            # The first thing he ever picks up gets explained, once, right before
            # the "picked up" toast so the toast is not talking over the card.
            if item == "pamphlet" and not store.pamphlet_hint_shown:
                store.pamphlet_hint_shown = True
                renpy.call_screen("hint_card", eyebrow="Your Bag", body=store.hint_text_bag)
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
            "blurb": "Observation and reasoning.",
            "color": "#5fb8ff",
            "color_soft": "#5fb8ff55",
        },
        "grace": {
            "name": "Grace",
            "blurb": "Empathy and communication.",
            "color": "#77d98b",
            "color_soft": "#77d98b55",
        },
        "nerve": {
            "name": "Nerve",
            "blurb": "Resolve under pressure.",
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
    # Rank thresholds are cumulative. Dialogue rewards may be fractional and
    # smaller than a half point, so they accumulate toward this ladder.
    attribute_rank_thresholds = [0.0, 2.0, 5.0, 9.5, 15.0]
    attribute_rank_names = [
        "Rank 01",
        "Rank 02",
        "Rank 03",
        "Rank 04",
        "Rank 05",
    ]

    # Standard reward sizes live here. Prefer a name over a raw number so later
    # scenes stay on the same ladder. Named losses keep the same vocabulary for
    # deliberate trade-offs.
    #
    #   tiny   — a flicker of behaviour (airport first contacts)
    #   micro  — a short, clear answer inside a conversation
    #   nudge  — a stronger reply that still is not a turning point
    #   small  — a real choice with a subject
    #   medium — a set-piece beat that closes a scene or a day
    #   large  — reserved for later act-turning decisions
    #
    # Soft trade-offs should usually cost `micro_loss` (-0.2), not half a point.
    attribute_reward_sizes = {
        "tiny": 0.1,
        "micro": 0.2,
        "micro_loss": -0.2,
        "nudge": 0.3,
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

    def attribute_ring_displayable(attribute_id, progress, size):
        segments = 24
        filled = int(max(0.0, min(1.0, progress)) * segments + 0.00001)
        large = size > 100
        dot_size = gui.scale(max(2, size * (0.022 if large else 0.075)))
        radius = gui.scale(size * (0.47 if large else 0.38))
        center = gui.scale(size * 0.5)
        empty_color = attribute_color_alpha(attribute_id, 0.16)
        dots = []

        for i in range(segments):
            angle = (2.0 * math.pi * i / segments) - (math.pi / 2.0)
            x = int(center + math.cos(angle) * radius - (dot_size * 0.5))
            y = int(center + math.sin(angle) * radius - (dot_size * 0.5))
            color = attribute_color(attribute_id) if i < filled else empty_color
            dots.append(Solid(color, xysize=(dot_size, dot_size), xpos=x, ypos=y))

        return Fixed(*dots, xysize=(gui.scale(size), gui.scale(size)))

    def attribute_orb_image(attribute_id):
        return "images/ui/attributes/%s_orb.png" % attribute_id

    def attribute_wave_image(attribute_id):
        return "images/ui/attributes/%s_wave.png" % attribute_id

    def attribute_orb_size(rank):
        """Reserved cells accommodate every rank without overlapping labels."""
        return 176 + (max(1, min(5, rank)) - 1) * 16

    def attribute_orb_position(attribute_id):
        return {
            "grace": (640, 300),
            "insight": (320, 372),
            "nerve": (960, 372),
        }[attribute_id]

    def attribute_orb_delay(attribute_id):
        return {
            "grace": 0.16,
            "insight": 0.0,
            "nerve": 0.32,
        }[attribute_id]

    def format_points(value):
        """Points as the player should read them: 1, not 1.0. 0.5 stays 0.5."""
        value = float(value)
        if abs(value - round(value)) < 0.001:
            return str(int(round(value)))
        return "%.1f" % value

    def format_signed_points(value):
        value = float(value)
        sign = "+" if value > 0 else "-" if value < 0 else ""
        return sign + format_points(abs(value))

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

        Circular meters reset at each rank; the HUD orb opacity uses lifetime
        progress separately so its surface only grows more solid.
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
        """Points remaining beneath the attribute's rank readout."""
        ceiling = attribute_rank_ceiling(attribute_id)

        if ceiling is None:
            return "Maximum rank"

        return "%s to next rank" % format_points(ceiling - attribute_total(attribute_id))

    def has_attribute(attribute_id, minimum_rank):
        """Whether a gated choice is open to him yet.

        This helper is for choices that explicitly need a rank, rather than a
        particular point total.
        """
        return attribute_rank(attribute_id) >= minimum_rank

    def has_attribute_points(attribute_id, minimum_points):
        """Whether a dialogue choice's minimum point total has been reached."""
        if attribute_id not in attribute_defs:
            raise Exception("Unknown attribute id: %r" % (attribute_id,))
        return attribute_total(attribute_id) >= float(minimum_points)

    def attribute_reward_value(amount):
        """A named size, or a raw number of points. Names are preferred."""
        if isinstance(amount, str):
            return float(attribute_reward_sizes.get(amount, attribute_reward_sizes["small"]))
        return float(amount)

    def add_attribute_points(attribute_id, amount="small", show="auto"):
        """Adjust an attribute and make sure the player sees what happened.

        Every adjustment shows something, including the small ones. Which of the two
        things it shows is decided here so no scene ever has to think about it:

          show="auto"  — the quiet ticker, or the full card on a rank change
          show="card"  — the full card, for a set-piece decision
          show=False   — nothing at all, for bookkeeping that is not a reward

        A rank change always takes the full card whatever the size.
        """
        if attribute_id not in attribute_defs:
            raise Exception("Unknown attribute id: %r" % (attribute_id,))

        points = attribute_reward_value(amount)
        before_rank = attribute_rank(attribute_id)
        before_total = attribute_total(attribute_id)
        after_total = round(max(0.0, min(
            attribute_rank_thresholds[-1],
            before_total + points,
        )), 2)
        points = round(after_total - before_total, 2)
        if points == 0:
            return before_total
        store.character_attributes[attribute_id] = after_total
        after_rank = attribute_rank(attribute_id)
        rank_up = after_rank > before_rank
        rank_down = after_rank < before_rank

        if show is False:
            return attribute_total(attribute_id)

        if rank_up or rank_down or show == "card":
            # Let the choice breathe for a moment before the card takes over, so
            # the reward reads as a follow-through rather than a cut.
            renpy.pause(0.45, hard=True)
            # Screen timers synchronize the landing and settle with the reveal.
            play_sfx("audio/SFX/attribute_swell.wav")
            renpy.call_screen("attribute_gain_card", attribute_id=attribute_id,
                              amount=points, rank_up=rank_up, rank_down=rank_down)
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
        renpy.call_screen("hint_card", eyebrow="Social Attributes",
                          body=store.hint_text_attribute)

    def show_attribute_tick(attribute_id, points):
        """Flash a small "+0.5" chip beneath the matching labeled HUD circle.

        This is what a half point in the middle of a conversation looks like. It
        must not cost the player a click or a beat, so it is a screen that shows
        itself, waits, and hides itself again.

        Each attribute has its own expiry. A fresh gain refreshes that chip's
        duration without removing another attribute's feedback.
        """
        store.attribute_tick_events[attribute_id] = points
        store.attribute_tick_started[attribute_id] = renpy.get_game_runtime()
        play_sfx("audio/SFX/attribute_tick.wav")
        renpy.show_screen("attribute_tick")

    def clear_attribute_tick(attribute_id):
        store.attribute_tick_events.pop(attribute_id, None)
        store.attribute_tick_started.pop(attribute_id, None)

    def expire_attribute_ticks():
        now = renpy.get_game_runtime()
        for attribute_id in list(store.attribute_tick_events):
            started = store.attribute_tick_started.get(attribute_id, now - 2.10)
            if now - started >= 2.10:
                clear_attribute_tick(attribute_id)
        if not store.attribute_tick_events:
            renpy.hide_screen("attribute_tick")

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
define hamada_staff = Character("Yamada", color="#b6d2e8", callback=type_sound, image="hamada_staff")

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
image side hamada_staff = At(Transform("images/characters/hamadadenki.png", xysize=(256, 384), fit="contain"), portrait_idle)

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
        "sister", "taxi_driver", "professor", "hamada_staff", "chef", "sim",
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

define notice_text_fiction = "This game is a work of fiction.\n\nAny resemblance to real people, living or dead, is coincidental. The characters do not represent real individuals."

define notice_text_choice = "Your choices can affect conversations, relationships and later events.\n\nSome decisions have lasting consequences. Other characters may remember what you say and do."

define notice_text_accept = "Some choices affect more than the current conversation.\n\nContinue when you are ready to make those decisions."

# The one-time hints. They are all drawn by the same card, so the only thing each
# caller supplies is the wording, and none of them ever runs twice.
define hint_text_money = "Open Bag from the bottom menu to check your cash.\n\nTravel, meals and purchases cost money. Check your balance before you spend."

define hint_text_bag = "Open Bag from the bottom menu to see the items you carry.\n\nSelect an item to read its description. If it can be used, its action appears below the description."

# The first point he ever earns. It names the three pillars and says where they
# come from, and deliberately says nothing about where they lead: the locked
# answer and the person who remembers are better met as surprises than explained
# here. Everything past this sentence is left for the player to find.
define hint_text_attribute = "Insight: observation and reasoning. Grace: thoughtful communication. Nerve: acting despite uncertainty.\n\nSome replies raise an attribute; some trade-offs lower one. Signed changes appear below their circle. Rank-ups open a separate screen. Open Attributes to check progress. Not every reply changes your attributes."

# The first afternoon he is allowed to spend. It names the thing he has just been
# handed and says what it is for, without listing where he can go: the places are
# meant to be found, and the ones that matter will announce themselves with a
# mark of their own. Called from the after-school fork, once, after the game has
# already taken him somewhere.
define hint_text_after_school = "Choose one activity each free afternoon: spend time with someone, visit a place, or head home. That choice leads into the rest of the day.\n\nSome activities develop attributes or relationships. Other activities wait for another opportunity; you do not need to visit everyone in one afternoon."

# The circles scale with rank. Two thin, colored wave rings travel outward from
# each orb and fade, keeping the surface alive without pulsing the text.
transform attribute_gain_cluster_in:
    alpha 0.0
    yoffset gui.scale(10)
    parallel:
        easeout 0.34 alpha 1.0
    parallel:
        easeout 0.46 yoffset 0

transform attribute_gain_cluster_out:
    alpha 1.0
    yoffset 0
    easein 0.26 alpha 0.0 yoffset gui.scale(-8)

transform attribute_gain_title_in:
    alpha 0.0
    xoffset gui.scale(-30)
    pause 0.48
    easeout 0.38 alpha 1.0 xoffset 0

transform attribute_gain_bar_in:
    alpha 0.0
    yoffset gui.scale(8)
    pause 1.08
    easeout 0.32 alpha 1.0 yoffset 0

transform attribute_gain_button_in:
    on show:
        alpha 0.0
        yoffset gui.scale(6)
        easeout 0.22 alpha 1.0 yoffset 0

transform attribute_gain_node_in(delay=0.0, start_zoom=0.82):
    xanchor 0.5
    yanchor 0.5
    alpha 0.0
    zoom start_zoom
    pause delay
    easeout 0.48 alpha 1.0 zoom 1.0

transform attribute_gain_wave_a(delay=0.0):
    xanchor 0.5
    yanchor 0.5
    alpha 0.0
    zoom 1.0
    pause delay
    block:
        alpha 0.30
        zoom 1.0
        easeout 1.50 alpha 0.0 zoom 1.56
        repeat

transform attribute_gain_wave_b(delay=0.0):
    xanchor 0.5
    yanchor 0.5
    alpha 0.0
    zoom 1.0
    pause delay
    block:
        alpha 0.28
        zoom 1.0
        easeout 1.50 alpha 0.0 zoom 1.56
        repeat

style attribute_gain_kicker is default:
    font "DejaVuSans.ttf"
    size gui.scale(13)
    color "#dce6ef"
    bold True
    kerning gui.scale(3)
    outlines []

style attribute_gain_title is default:
    font "DejaVuSans.ttf"
    size gui.scale(44)
    color "#f5f7fa"
    bold True
    italic True
    kerning gui.scale(-2)
    outlines []

style attribute_gain_name is default:
    font "DejaVuSans.ttf"
    size gui.scale(24)
    color "#ffffff"
    bold True
    kerning gui.scale(3)
    text_align 0.5
    outlines []

style attribute_gain_rank is default:
    font "DejaVuSans.ttf"
    size gui.scale(12)
    color "#ffffff"
    bold True
    kerning gui.scale(2)
    text_align 0.5
    outlines []

style attribute_gain_orb_number is default:
    font "DejaVuSans.ttf"
    color "#ffffff"
    bold True
    italic True
    text_align 0.5
    kerning gui.scale(-5)
    outlines []

style attribute_gain_ribbon is default:
    font "DejaVuSans.ttf"
    size gui.scale(12)
    color "#b9b7b1"
    kerning gui.scale(0)
    text_align 0.5
    outlines []

style attribute_gain_continue is button:
    background None
    hover_background Solid("#ffffff0d")
    padding (gui.scale(18), gui.scale(10))

style attribute_gain_continue_text is default:
    font "DejaVuSans.ttf"
    size gui.scale(15)
    bold True
    color "#d7d4cc"
    hover_color "#ffffff"
    kerning gui.scale(1)
    outlines []

screen attribute_gain_card(attribute_id, amount, rank_up=False, rank_down=False):
    modal True
    zorder 110

    default hiding = False
    default ready = False

    $ amount_text = format_signed_points(amount)
    $ current_name = attribute_name(attribute_id)
    $ active_color = attribute_defs[attribute_id]["color"]
    $ active_rank = attribute_rank(attribute_id)
    $ active_orb_size = attribute_orb_size(active_rank)
    $ active_orb_x, active_orb_y = attribute_orb_position(attribute_id)
    $ active_orb_delay = attribute_orb_delay(attribute_id)

    add Solid("#171613eb") at (attribute_gain_cluster_out if hiding else attribute_gain_cluster_in)

    fixed:
        at (attribute_gain_cluster_out if hiding else attribute_gain_cluster_in)
        xsize config.screen_width
        ysize config.screen_height

        # Waves live on the full-screen canvas, not inside the orb's clipped
        # bounds, so they can grow past the circle while staying centered on it.
        add attribute_wave_image(attribute_id):
            xysize (gui.scale(active_orb_size), gui.scale(active_orb_size))
            xpos gui.scale(active_orb_x)
            ypos gui.scale(active_orb_y)
            at attribute_gain_wave_a(active_orb_delay + 0.12)

        add attribute_wave_image(attribute_id):
            xysize (gui.scale(active_orb_size), gui.scale(active_orb_size))
            xpos gui.scale(active_orb_x)
            ypos gui.scale(active_orb_y)
            at attribute_gain_wave_b(active_orb_delay + 0.87)

        # Artwork scales inside reserved cells. Typography is a separate layer,
        # drawn after all circles and waves, with a fixed, shared baseline.
        for orb_id in attribute_order:
            $ orb_rank = attribute_rank(orb_id)
            $ orb_size = attribute_orb_size(orb_rank)
            $ orb_x, orb_y = attribute_orb_position(orb_id)
            $ orb_delay = attribute_orb_delay(orb_id)
            $ orb_target = (orb_id == attribute_id)
            $ orb_start_zoom = 0.72 if orb_target and rank_up else 0.84

            fixed:
                xpos gui.scale(orb_x)
                ypos gui.scale(orb_y)
                xysize (gui.scale(orb_size), gui.scale(orb_size))
                at attribute_gain_node_in(orb_delay, orb_start_zoom)

                add Transform(attribute_orb_image(orb_id), alpha=0.85 if orb_target else 0.25) xysize (gui.scale(orb_size), gui.scale(orb_size))
                add attribute_wave_image(orb_id) xysize (gui.scale(orb_size), gui.scale(orb_size))

            add attribute_ring_displayable(orb_id, attribute_rank_progress(orb_id), orb_size + 28):
                xpos gui.scale(orb_x)
                ypos gui.scale(orb_y)
                xanchor 0.5
                yanchor 0.5

        for orb_id in attribute_order:
            $ orb_rank = attribute_rank(orb_id)
            $ orb_x, orb_y = attribute_orb_position(orb_id)
            $ orb_color = attribute_color(orb_id)

            text "[orb_rank:02d]" style "attribute_gain_orb_number":
                xpos gui.scale(orb_x)
                ypos gui.scale(orb_y)
                xanchor 0.5
                yanchor 0.5
                size gui.scale(76)

            vbox:
                xpos gui.scale(orb_x - 140)
                ypos gui.scale(516)
                xsize gui.scale(280)
                spacing gui.scale(9)
                text attribute_name(orb_id).upper() style "attribute_gain_name" color orb_color xalign 0.5
                text "RANK [orb_rank:02d] / 05" style "attribute_gain_rank" xalign 0.5
                text attribute_blurb(orb_id) style "attribute_gain_ribbon" xalign 0.5
                text attribute_rank_next_text(orb_id) style "attribute_gain_ribbon" xalign 0.5

        vbox:
            at attribute_gain_title_in
            xpos gui.scale(90)
            ypos gui.scale(58)
            spacing gui.scale(8)

            text "SOCIAL ATTRIBUTES" style "attribute_gain_kicker"
            if rank_up:
                text "RANK UP" style "attribute_gain_title" color active_color
            elif rank_down:
                text "RANK DOWN" style "attribute_gain_title" color active_color
            elif amount < 0:
                text "ATTRIBUTE LOSS" style "attribute_gain_title" color active_color
            else:
                text "ATTRIBUTE GAIN" style "attribute_gain_title" color active_color

        vbox:
            at attribute_gain_bar_in
            xpos gui.scale(884)
            ypos gui.scale(66)
            xsize gui.scale(306)
            spacing gui.scale(10)
            text "[current_name.upper()]  [amount_text]" style "attribute_gain_name" color active_color xalign 1.0
            if rank_up:
                text "RANK [active_rank:02d] / 05" style "attribute_gain_rank" xalign 1.0
            else:
                text attribute_rank_next_text(attribute_id) style "attribute_gain_ribbon" xalign 1.0
            add Solid(active_color) xysize (gui.scale(306), gui.scale(2))

        if ready:
            textbutton "Continue" action SetScreenVariable("hiding", True) style "attribute_gain_continue" xalign 0.97 yalign 0.97 sensitive (not hiding) at attribute_gain_button_in

    timer 1.48 action Play("attribute_ui", "audio/SFX/attribute_tick.wav")
    timer 1.82 action Play("attribute_ui", "audio/SFX/attribute_settle.wav")
    timer 1.92 action SetScreenVariable("ready", True)

    if hiding:
        timer 0.300 action Return()

# --- THE QUIET GAIN, AND THE ORB CLUSTER ---
#
# Two pieces of feedback that run during play rather than stopping it.
#
# The chip shows a small signed adjustment. It appears over the top of the
# scene beneath its matching labeled circle and takes itself away again.
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

screen attribute_tick():
    zorder 95

    for index, attribute_id in enumerate(attribute_order):
        if attribute_id in attribute_tick_events:
            $ tick_color = attribute_color(attribute_id)
            $ tick_points = format_signed_points(attribute_tick_events[attribute_id])

            frame:
                at attribute_tick_appear
                xpos config.screen_width - gui.scale(221 - index * 77)
                xanchor 0.5
                ypos gui.scale(98)

                background Solid("#111820e8")
                padding (gui.scale(8), gui.scale(4))

                text tick_points style "attribute_tick_text" color tick_color

    timer 0.10 repeat True action Function(expire_attribute_ticks)

style attribute_tick_text is default:
    font "DejaVuSans.ttf"
    size gui.scale(15)
    bold True
    kerning gui.scale(1)
    outlines []

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

screen attribute_hud():
    zorder 90

    # Standalone windows keep the scene visible without gameplay UI behind them.
    if show_attribute_hud and not main_menu and not standalone_window_active():

        hbox:
            at attribute_hud_appear

            xalign 1.0
            yalign 0.0
            xoffset gui.scale(-28)
            yoffset gui.scale(24)
            spacing gui.scale(5)

            for orb_id in attribute_order:

                fixed:
                    xsize gui.scale(72)
                    ysize gui.scale(68)

                    add attribute_ring_displayable(orb_id, attribute_rank_progress(orb_id), 46) xalign 0.5

                    text attribute_name(orb_id).upper():
                        xalign 0.5
                        ypos gui.scale(51)
                        size gui.scale(9)
                        kerning gui.scale(1)
                        color "#c5cdd4"
                        outlines []

# --- START LABEL ---
label start:
    scene black with Fade(1.4, 0.0, 0.0)

    # Before the story, the two notices. Neither can be clicked past: each page
    # fades itself in and out and then returns on its own timer, so a new player
    # reads both whether they mean to or not. They only ever run here, which is
    # to say only on a new game. A loaded save resumes where it was.
    call screen notice_page("A Work of Fiction", notice_text_fiction, "1 / 2")
    call screen notice_page("Lasting Decisions", notice_text_choice, "2 / 2")

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
    
    "That flight felt endless."
    "I barely slept."
    "Still, I made it. Tokyo."
    "I'm here on my university's exchange program."
    
    
    "I should be excited. New university, host family, a year in Japan."
    "Instead, everything feels slightly out of focus."
    "I remember the application. The wait. The acceptance email."
    "I was thrilled when it came through. My friends said I was brave."
    "I can't remember what made me choose Japan."
    "There must have been a reason. I just can't get hold of it."
    "Maybe it's the flight. Or the nerves. Maybe this is what arriving somewhere alone feels like."

    
    # The wallet, established before he has spent a single yen of it.
    "I have thirty thousand yen, in cash, folded into the back of my wallet."
    "I hope it covers the first few days."
    "Thirty thousand yen doesn't go far when it has to cover everything."
    "I'll need to find a part-time job. I can't expect other people to handle it for me."
    
    # Foreshadowing glitch - the first crack in the simulation
    show hospital_flash onlayer overlay at truecenter:
        alpha 0.0
        linear 0.1 alpha 0.3
        linear 0.1 alpha 0.0
    
    "Syncing..."
    
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

    "Tokyo. I'm here."
    "Now I just need to get to the address."
    "I'll check the map on my phone."
    call screen airport_phone
    "..."
    "No signal."
    "So much for the map."
    "I should ask someone how to get there."

label airport_exploration:
    menu:
        "Ask the Security Guard":
            jump talk_security
        "Ask the Timid Man":
            jump talk_timid_man
        "Ask the Cheerful Woman":
            jump talk_cheerful_woman
        "Ask the Information Desk":
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
        mc "(I was only trying to ask a question.)"
        security "業務中です。話しかけないでください。"
        mc "(I showed him the address. Maybe he didn't understand what I wanted.)"
        security "……"
        mc "(He didn't even look at the screen. Maybe I should try someone else.)"
    else:
        security2 "……何か？"
        mc "(Her expression doesn't change.)"
        security2 "ここは立入制限区域です。この先は関係者以外通れません。"
        mc "(Restricted area. I'm not trying to go anywhere. I just want the exit.)"
        mc "Excuse me. Which way is...."
        security2 "総合案内所はあちらです。"
        mc "(She points behind me without turning around.)"
        security2 "私は持ち場を離れられません。他の人に聞いてください。"
        mc "(I caught 'information desk' and 'can't leave'. The rest went by too fast.)"
        security2 "それ以上は業務妨害とみなします。"
        mc "(Okay. Okay. I'm going.)"

    $ security_index += 1
    $ talked_to_security = True

    # The guard cannot be won over, so this fork is about how the protagonist
    # responds to being dismissed. Apologising nudges Grace, while pressing on
    # nudges Nerve; watching the crowd remains neutral.
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
    $ reward_attributes_once("answer_security_bow", [("grace", "tiny")], show="auto")
    mc "(Maybe the information desk can help.)"
    jump airport_exploration

label answer_security_press:
    mc "Excuse me. 中野3丁目. Please."
    mc "(They glanced at the phone, then at me, and turned away.)"
    $ reward_attributes_once("answer_security_press", [("nerve", "tiny")], show="auto")
    mc "(I don't know if they understood. Either way, I need to try someone else.)"
    mc "(Maybe the information desk can help.)"
    jump airport_exploration

label answer_security_watch:
    mc "(Never mind. If I watch where people are going, I might find the exit.)"
    mc "(Someone at the information desk might be able to help.)"
    jump airport_exploration

label talk_timid_man:
    timid_man "話しかけないでくれ！"
    timid_man "忙しくて雑談してる暇はないんだ。"
    mc "(I didn't catch any of that.)"
    $ talked_to_man1 = True

    # Re-entry repeats the answer, but noticing the word only pays once.
    $ prior_answer = remembered_choice("timid_man")

    if prior_answer == "again":
        jump answer_timid_again
    elif prior_answer == "aside":
        jump answer_timid_aside
    elif prior_answer == "listen":
        jump answer_timid_listen

    menu:
        "Ask where the information desk is.":
            $ remember_choice("timid_man", "again")
            jump answer_timid_again
        "Leave him to it.":
            $ remember_choice("timid_man", "aside")
            jump answer_timid_aside
        "Listen for a word I recognise.":
            $ remember_choice("timid_man", "listen")
            jump answer_timid_listen

label answer_timid_again:
    mc "Sorry. Information desk?"
    mc "(He repeated himself at the same speed.)"
    mc "(Maybe he can't stop. Maybe he just doesn't have time for me.)"
    mc "(I'll leave him alone.)"
    jump airport_exploration

label answer_timid_aside:
    mc "Ah - sorry. Sorry."
    mc "(I'll leave him alone.)"
    jump airport_exploration

label answer_timid_listen:
    mc "(...いそがしい.)"
    mc "(Isogashii. Busy. I practised that one on the plane.)"
    mc "(He isn't angry. He's busy.)"
    $ reward_attributes_once("answer_timid_listen", [("insight", "micro")], show="auto")
    mc "(I'll leave him alone.)"
    jump airport_exploration

label talk_cheerful_woman:
    cheerful_woman "こんにちは！日本へようこそ！"
    cheerful_woman "それでは、失礼します！楽しんでくださいね！"
    mc "(Welcome. I caught that much.)"

    $ talked_to_npc2 = True

    # She is the one warm face in the terminal, and the fork is about how much
    # he is willing to give back. The same answer repeats on later visits.
    $ prior_answer = remembered_choice("cheerful_woman")

    if prior_answer == "smile":
        jump answer_woman_smile
    elif prior_answer == "echo":
        jump answer_woman_echo

    menu:
        "Smile and bow.":
            $ remember_choice("cheerful_woman", "smile")
            jump answer_woman_smile
        "Thank her in Japanese.":
            $ remember_choice("cheerful_woman", "echo")
            jump answer_woman_echo

label answer_woman_smile:
    mc "(She's the first person here who's smiled at me.)"
    cheerful_woman "あら！ がんばってね！"
    $ reward_attributes_once("answer_woman_smile", [("grace", "micro")], show="auto")
    jump airport_exploration

label answer_woman_echo:
    mc "Arigatou gozaimasu."
    cheerful_woman "どういたしまして！"
    mc "(She smiles and waves before disappearing into the crowd.)"
    $ reward_attributes_once("answer_woman_echo", [("grace", "micro")], show="auto")
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
    assistant "*quietly to herself* English staff... on break."
    mc "I need to get to this address."
    assistant "アドレス？うーん… show... me?"
    
    # Successful requests are latched. Deferring is not a permanent refusal:
    # the pamphlet is required to leave the airport, including in older saves.
    $ prior_answer = remembered_choice("assistant")

    if prior_answer == "ask":
        jump answer_assistant_ask
    elif prior_answer == "patient":
        jump answer_assistant_patient

    menu:
        "Show her the address.":
            $ remember_choice("assistant", "ask")
            jump answer_assistant_ask
        "We can use the map. No rush.":
            $ remember_choice("assistant", "patient")
            jump answer_assistant_patient
        "I'll try another desk.":
            jump answer_assistant_nevermind

label answer_assistant_patient:
    mc "It's okay. We can use the map. I'm not in a hurry."
    assistant "Map... yes. ちず。"
    "She lets out a breath and reaches for a pamphlet."
    $ reward_attributes_once("answer_assistant_patient", [("insight", "micro")], show="auto")
    jump answer_assistant_ask

label answer_assistant_ask:
    mc "*Shows address on phone.* How do I get here?"
    # She cannot find the English for it and it starts to show. The second drawing
    # stays up until the pamphlet is in his hands and she has recovered.
    $ assistant_shy = True
    assistant "あー、これはね…でんしゃ？トレイン？"
    assistant "にっぽりえきから。。。えっと。。。ちょっとまってください。"
    assistant "*She unfolds a map covered in arrows and kanji.*"
    $ has_pamphlet = True
    $ add_item("pamphlet")
    mc "This is a lot to take in. Thank you."
    $ assistant_shy = False
    assistant "Good luck! がんばってください！"
    mc "Thanks. I'll give it a try."
    jump airport_exploration

label answer_assistant_nevermind:
    mc "Never mind. Thanks anyway."
    $ assistant_shy = False
    jump airport_exploration

label talk_veteran_assistant:
    if not has_pamphlet:
        veteran "You look a little lost. Can I help?"
        veteran "If you find a pamphlet lying around, I can try to translate it for you!"
        mc "Pamphlet? I'll go look for one."
        jump airport_exploration

    veteran "You look a little lost. Can I help?"
    veteran "What is that in your hand?"
    veteran "A pamphlet. Let me see."
    veteran "You're going to 中野3丁目, right?"
    mc "That's right."
    veteran "You can take the train or a taxi. The train is cheaper; a taxi goes straight to the door."
    veteran "Which would you like to hear about?"
    
    menu:
        "Tell me about the train.":
            veteran "First, buy a ticket before you go through the gate."
            veteran "Look for the express on the Keisei Line. The local stops at every station and takes much longer."
            veteran "It should be about forty-five minutes."
            jump taxi_choice
        "Tell me about the taxi.":
            veteran "Follow the signs outside to the taxi stand. Show the driver the address."
            veteran "Budget around ¥18,000. More if there's traffic."
            jump end_airport
        "I have what I need. Thank you.":
            $ reward_attributes_once("veteran_advice_decline", [("insight", "micro")], show="auto")
            jump end_airport

label taxi_choice:
    veteran "Would you like to hear about the taxi as well?"
    menu:
        "Tell me about the taxi.":
            veteran "The taxi stand is just outside. There may be a short wait."
            veteran "The fare will be around ¥18,000, perhaps more in traffic."
            veteran "Show the driver the address and they'll take you there."
            jump end_airport
        "I'll take the train. Thank you.":
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
    veteran "You're welcome. I hope you enjoy your time here."
    mc "Thanks. I hope so too."

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
    #
    # INTENTIONAL ROUTE ASYMMETRY (keep this when balancing later acts):
    #   * Train rewards Insight (reading systems, signs, transfers).
    #   * Taxi rewards Nerve (spending half the wallet to arrive safe).
    #   * Early gated options lean the same way: Insight doors open more easily
    #     after the train; Nerve doors open more easily after the taxi.
    # That is route identity, not a bug. Do not "fix" it by equalising the two.
    "Outside, the Tokyo night air hits me all at once."
    "Warmer than I expected. Damp. Full of sounds I don't have names for."
    mc "(Okay. 中野3丁目. Somewhere out there in all of that.)"
    mc "(She said there were two ways. Cheap and confusing, or simple and expensive.)"

    menu:
        "Take the taxi.":
            jump taxi_warning
        "Take the train.":
            $ travel_method = "train"
            $ reward_attributes_once("travel_route_attribute", [("insight", "small")])
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
            $ reward_attributes_once("travel_route_attribute", [("nerve", "medium")])
            jump taxi_stand
        "Take the train instead.":
            $ travel_method = "train"
            $ reward_attributes_once("travel_route_attribute", [("insight", "small")])
            jump train_station


# --- THE TAXI ---
# The easy route. First-time-foreigner moments, a driver he cannot understand,
# and the tired monologue that puts him to sleep in the back seat.

label taxi_stand:
    scene bg_taxi_stand with walk_fade
    play music "audio/Music/taxi.mp3" fadein 1.5

    "The terminal doors slide open before I reach them."
    mc "(Automatic doors. Right.)"

    "Outside, a row of taxis idles under the lights, engines ticking over."
    "A man in a white shirt and white gloves waves me toward the front of the line."
    mc "(...Gloves. He's wearing white gloves. To drive a car.)"
    mc "(Okay. Show him the pamphlet. That is the entire plan. Show him the pamphlet.)"

    "The taxi stops in front of me, and the rear door opens automatically."
    mc "(The driver opened it from his seat.)"
    mc "(There's a line behind me. Get in the car.)"

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

    menu:
        "Thank him in Japanese.":
            mc "Arigatou... gozaimasu."
            taxi_driver "お。日本語、上手ですね。"
            mc "(I don't know what that was, but it was warm, and he said it to the mirror rather than to me.)"
        "Ask him to confirm the fare.":
            mc "Excuse me. Around eighteen thousand yen?"
            taxi_driver "Yes. About. Traffic, little more."
            mc "Okay. Thank you."
            # Asking about money despite embarrassment, not merely spending it.
            $ reward_attributes_once("answer_taxi_fare", [("nerve", "small")], show="auto")
        "Watch the city through the window.":
            mc "(The driver knows the way. I can stop staring at the meter for a minute.)"

    "The city slides past the window in long wet streaks of light."
    "Buildings I've only seen in photographs. Signs I can't read. Vending machines on every corner, glowing like little aquariums."
    mc "(Vending machines. Everywhere. Every hundred metres, another one.)"
    mc "(Someone on the plane told me you can get hot coffee out of them. In a can. I thought he was joking.)"

    "I look at the little screen on the dashboard, because I cannot help myself."
    "*The meter reads 1,300.*"
    mc "(Thirteen hundred. We have been in this car for four minutes.)"

    "The driver says something and points out of my window. I nod and smile."
    mc "(I didn't understand a word. Maybe I can get by with a nod until my Japanese improves.)"

    "*The meter clicks. I look again.*"
    mc "(Three thousand eight hundred.)"
    mc "(Another hundred. Then another.)"
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

    # Acting on his own reading of the room earns a small Nerve reward; following
    # the advice and buying a ticket remains a neutral choice.
    menu:
        "Walk straight through.":
            $ reward_attributes_once("answer_train_gate", [("nerve", "nudge")], show="auto")
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
    mc "(That actually hit me.)"
    mc "(Right. Buy a ticket first.)"
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
            mc "(And it doesn't go to 中野.)"
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
            mc "(Not it.)"
            jump ticket_machine

        "Ask the station attendant.":
            "I catch the eye of a woman in a station uniform and hold the pamphlet up."
            mc "Sumimasen... 中野3丁目?"
            "She takes the pamphlet, reads it, and presses the button for me without a word."
            "¥1,300. A ticket slides out."
            mc "(That took her four seconds. It took me four minutes.)"
            mc "Arigatou gozaimasu."
            "She nods, already walking away."
            $ reward_attributes_once("answer_ticket_ask", [("grace", "micro")], show="auto")
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
            $ reward_attributes_once("answer_train_express", [("insight", "micro")], show="auto")
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
        "The walk from the station is short. Streetlights give the neighbourhood a warm glow."
        "Low houses line the street, most with a tiny garden or a bicycle by the wall."
        mc "Managed to catch the express and transfer at the right station. Not bad for my first time navigating solo."
    else:
        "The walk from the station takes forever."
        mc "That local stopped at every station between here and the airport. Twice, it felt like."
        mc "It's late. I hope I'm not waking anyone up."


    "I stand in front of a narrow two-storey house with one light on behind the curtains."
    mc "Home, for a year. I'll find out what that means in the morning."
    mc "What was the greeting again? Konnichiwa. That should work."
    "*Pushes for the doorbell.*"
    # The chime lands at the same moment as the line describing it, so the sound
    # and the text hit together instead of a beat apart.
    $ play_sfx("audio/SFX/doorbell.mp3")
    pause 3.0
    "*The chime is much louder than I expected. It bounces off the houses opposite.*"
    mc "(Everyone on this street heard that. I hope I didn't wake anyone in the house.)"

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
        father "You'll be part of the household while you're here. If you need anything, ask."
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
    "The stairs creak under both of us. She apologises for it, which only makes me notice it more."
    mother "Well, it's not a lot, but this will be your room for the year."
    mother "Hikari's room is next door, so please try not to make too much noise. She's a light sleeper."
    mother "Oh, and the things you shipped over arrived yesterday. They're still down by the door."
    mother "Would you help your old host mother carry them up?"
    mc "Of course. Let me help."

    mother "Sorry about the stairs. And the boxes. I should have brought them up earlier."
    menu:
        "You've already done a lot for me.":
            # Acknowledging her effort rather than dismissing her worry.
            $ reward_attributes_once("answer_boxes_reassure", [("grace", "nudge")], show="auto")
            mc "You've already done a lot for me. Let me do this bit."
            mother "Well. If you're sure. I've been fussing over that room all week."
        "Which ones go upstairs?":
            mc "All of these, or just the clothes?"
            mother "All three. The books are in the bottom one. Careful with that."
        "Can we leave the books until morning?":
            mc "Could we bring up the clothes now and leave the books until morning? I'm barely awake."
            mother "Of course. The books won't mind waiting."
            $ reward_attributes_once("answer_boxes_postpone", [("grace", "micro_loss")], show="auto")

    "*We carry what I need upstairs. She steadies the box while I find the light switch.*"
    if arrived_late:
        mother "Goodnight. Sleep well. We'll talk properly in the morning."
    else:
        mother "Goodnight. And truly, welcome. We'll talk properly in the morning."
    "*The door clicks shut, and then the house is completely silent.*"

    mc "Good thing I sent everything ahead. Thanks to that I only had to carry a small bag."
    if travel_method == "train":
        mc "I never would have managed the transfers with luggage."
    mc "Right. Unpacking."
    "*Cardboard. Tape. Clothes that smell like my old room.*"

    "Somewhere in the middle of it the room stops looking like a spare room and starts looking like somewhere a person lives."
    mc "I'm tired, but it finally feels like my room."
    mc "I'm grateful to have a place of my own."
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
        ease 0.16 zoom 1.018

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
    default bars = dream_static_bars(3, 0.08, False)
    timer 0.12 repeat True action SetScreenVariable("bars", dream_static_bars(3, 0.08, False))

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
        ypos 24
        spacing 5

        text "MEMORY / RECONSTRUCTION" xalign 0.5:
            size 11
            kerning 3
            color "#7f96a8"
            outlines []

        text "PUT THE DAY BACK" at dream_title_glitch:
            xalign 0.5
            size 30
            kerning 2
            color "#9bdcf5"
            outlines []

        text "Four memories happened today. Place them in the order they occurred.":
            xalign 0.5
            size 17
            color "#aab7c1"
            outlines []

    # How many readings remain.
    hbox:
        xpos 1210
        ypos 34
        xanchor 1.0
        spacing 7

        text "READINGS" size 11 color "#7f96a8" kerning 2 outlines []

        for i in range(3):
            add Solid("#9bdcf5" if i < attempts else "#26313a") xysize (22, 4)

        text "[attempts]/3" size 12 color "#bdcbd5" outlines []

    add Solid("#0d131c") xpos 48 ypos 132 xysize (590, 478)
    add Solid("#0d131c") xpos 652 ypos 132 xysize (580, 478)
    add Solid("#263542") xpos 48 ypos 132 xysize (590, 1)
    add Solid("#263542") xpos 652 ypos 132 xysize (580, 1)

    # --- the order he is rebuilding ----------------------------------------
    vbox:
        xpos 70
        ypos 150
        spacing 12

        hbox:
            spacing 16
            text "YOUR SEQUENCE" size 14 kerning 2 color "#9bdcf5" outlines []
            text "[len(placed)] / 4 PLACED" size 11 kerning 1 color "#7f96a8" outlines []

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
                    background Solid("#18232d")
                    hover_background Solid("#202f3b")
                    action [
                        Play("sfx", "audio/SFX/type_click.wav"),
                        SetScreenVariable("placed", placed[:i] + placed[i + 1:]),
                    ]

                    fixed:
                        xysize (560, 86)
                        add Solid("#9bdcf520", xysize=(54, 86))
                        add Solid("#263b4a") xysize (2, 86)
                        text "0[i + 1]" xpos 0 xsize 54 text_align 0.5 yalign 0.5 size 18 color "#9bdcf5" outlines []
                        text slot_text xpos 72 yalign 0.5 xmaximum 424 size 16 line_spacing 3 color "#e5edf2" outlines []
                        text "REMOVE" xpos 482 yalign 0.5 size 9 kerning 1 color "#738493" outlines []

            else:

                fixed:
                    xysize (560, 86)
                    add Solid("#161d27", xysize=(560, 86))
                    add Solid("#111922", xysize=(556, 82)) xoffset 2 yoffset 2
                    text "0[i + 1]" xpos 2 xsize 52 text_align 0.5 yalign 0.5 size 18 color "#536475" outlines []
                    text "SELECT A MEMORY FOR THIS POSITION" xpos 74 yalign 0.5 size 10 kerning 1 color "#465563" outlines []

    # --- the pile ----------------------------------------------------------
    vbox:
        xpos 700
        ypos 150
        spacing 8

        text "AVAILABLE MEMORIES" size 14 kerning 2 color "#9bdcf5" outlines []

        for c in pile:

            button:
                xysize (510, 66)
                at dream_card_hover
                background Solid("#151e27")
                hover_background Solid("#263642")
                insensitive_background Solid("#0b1016")
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
                    size 15
                    line_spacing 3
                    color "#e5edf2"
                    outlines []

    text "Select a placed memory to remove it. The sequence is checked only when you submit it.":
        xalign 0.5
        ypos 610
        size 12
        color "#788895"
        outlines []

    # --- the reading -------------------------------------------------------
    button:
        xpos 640
        xanchor 0.5
        ypos 644
        xysize (380, 46)
        background Solid("#163744" if full else "#141c24")
        hover_background Solid("#1e5061")
        sensitive full
        action Return(list(placed))

        text "REVIEW SEQUENCE":
            xalign 0.5
            yalign 0.5
            size 14
            kerning 2
            outlines []
            color ("#b8e9f4" if full else "#647481")


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
    "Keep the pod at eighteen."

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
    "Let him finish the day."

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
    "Whoa... I just had the strangest dream."
    "Something about the airport. A road with no end on it. Two voices talking over me like I wasn't in the room."
    mc "What was that about?"
    mc "It felt like the dream knew me. That's what I can't shake."
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

    "The kitchen smells like toast and green tea, with a faint woody smell underneath."
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
    hikari "A few people in the department have been asking when you'd arrive."
    hikari "I told them today. No pressure."
    menu:
        "What have you told them about me?":
            $ reward_attributes_once("answer_breakfast_questions", [("nerve", "micro_loss")], show="auto")
            mc "What have you told them about me?"
            hikari "That you're in our department and you ask a lot of questions."
            mc "Accurate, unfortunately."
            $ remember("hikari", "asked what the department knew about him")
        "Should I introduce myself today?":
            mc "Should I introduce myself, or wait until I'm less jet-lagged?"
            hikari "Today. Nobody remembers introductions anyway. It's a free practice run."
            $ remember("hikari", "asked about meeting the other students")
        "Thank you for the emails.":
            $ reward_attributes_once("answer_breakfast_emails", [("grace", "small")], show="auto")
            mc "I never properly thanked you for the emails. You made this a lot less frightening."
            hikari "You did thank me. Several times."
            hikari "But you're welcome."
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
    mother "It was one slice."

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
            mc "Does he close it differently when he's angry?"
            hikari "It's the speed. An angry amado is fast, and a fast one bounces off the frame."
            hikari "You'll hear it in a month. Everybody does. It's the first thing this house teaches you."
            $ remember("hikari", "asked her how she hears a door")
        "I didn't hear anything.":
            mc "...I didn't hear anything. Sorry. It was a door closing."
            hikari "You will. The frame rattles when somebody slams it."
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

    "(Two changes. At the second station I lose track of which floor we're on.)"
    "(Hikari waits by the stairs and points out the platform number.)"
    "(This is her father's route. Next time, she says, she'll show me the shorter one.)"

    scene bg_school_gate with Fade(0.0, 0.0, 2.0)
    $ phone_map_visit("school")
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
            mc "Were you this lost on your first day?"
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
        "Where do I check room changes?":
            mc "If a class moves, where do I check? The department board?"
            hikari "The board and the student portal. Check the portal before you leave home."
            $ remember("hikari", "asked how to check room changes")
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

    menu:
        "Which building is ours?":
            mc "Which building is ours? I want to recognise it when I'm on my own."
            hikari "The grey one behind the trees. I'll take you there."
            $ remember("hikari", "asked which building belonged to their department")
        "These buildings are different ages.":
            $ reward_attributes_once("answer_courtyard_buildings", [("insight", "micro")], show="auto")
            mc "Stone, glass, concrete. Was this built in stages?"
            hikari "Yes. The gym was here first. They kept adding things around it."
            $ remember("hikari", "noticed the campus had been built in stages")
        "Let's keep moving.":
            mc "I'll look around later. I don't want to make us late."
            hikari "Good call. This way."

    "She walks fast, which I am starting to understand is just how everyone here walks."
    "She points at things the way a person points at their own house."
    hikari "Library. Open until ten. You will not care about that in September and you will care about it very much in December."
    hikari "That is the cafeteria, and that is the other cafeteria, and there is a reason there are two, and the reason is terrible."
    hikari "Past those, the gym. Nobody uses the gym."
    mc "Was that here before the rest?"
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
    hikari "Anything on the board catch your eye?"

    # The first door in the game that can be shut, gated on a modest Insight total
    # rather than a full rank-up this early. The other two are open on day one:
    # they are opinions, and he is entitled to have those before he has earned
    # anything. The locked one is the only one that asks him to have *noticed*
    # something nobody pointed out to him.
    menu:
        "The film screening.":
            mc "The film screening. Can anyone go?"
            hikari "Anyone with a student card. They show one every Thursday."
            $ remember("hikari", "picked the film screening poster")
        "The three rooms for rent.":
            mc "There are three of those. Three different flats, three different people who all took the same photograph."
            hikari "Same agent, probably. People pass the adverts around when they move out."
            $ remember("hikari", "picked the three rooms for rent")
        "[tag_insight] The lost cat." if has_attribute_points("insight", 0.8):
            mc "The cat one. The tape has gone yellow and both bottom corners have curled."
            hikari "...Huh."
            mc "There's a date at the bottom. Last semester. Has anyone checked whether they found it?"
            hikari "I don't know. The number's still there. We could ask later."
            $ reward_attributes_once("answer_wall_cat", [("insight", "micro")], show="auto")
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

    "Behind the counter, a woman looks up from an open file and motions us towards two chairs."
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

    # This response asks for a modest investment in Grace; it should be reachable
    # before the first lecture, not require a full rank-up.
    menu:
        "Which one would you pick?":
            mc "If it was you. Out of all of them. Which one would you pick?"
            clerk "The reading circle. Four people and a great deal of silence, and they have never once asked me for anything."
            clerk "That is the highest praise I can give a circle."
            $ remember("clerk", "asked which circle she would pick")
        "When does the photography club meet?":
            mc "When does the photography club meet? Can I visit before joining?"
            clerk "This afternoon. Second floor. They welcome visitors."
            $ remember("clerk", "asked when he could visit the photography club")
        "[tag_grace] You've made this much easier." if has_attribute_points("grace", 1.0):
            mc "You've made this much easier. I was worried I'd miss something important."
            clerk "You're welcome. Keep the booklet. There's a lot to remember on your first day."
            $ reward_attributes_once("answer_circles_back", [("grace", "micro")], show="auto")
            $ remember("clerk", "told her the orientation had helped")

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
    professor "You are late. Your name?"
    mc "I know. I'm the new one."
    "And then I see her."
    "Third row from the front, by the window. Notebook open. Pen out."
    "Sitting exactly where she would have sat if she had been here since breakfast."
    "Hikari. She does not look up."
    mc "(She left me at that counter and she is already inside and settled, and there is an empty seat beside her.)"
    "I start walking towards it."
    professor "Wait. I haven't finished."
    mc "Sorry. I'm just going to..."
    "Her hand closes around my sleeve and pulls. Hard."
    "I go down into the seat beside her, and the chair makes a noise the whole room hears."
    hikari "Don't answer him. Sit down. Say sorry and sit down."
    professor "I do not care who you are."
    professor "We can do introductions after class. Sit down."
    "He has not looked at Hikari once. She came in before the bell, so as far as this room is concerned she is part of the furniture."
    mc "(He is not angry at the room. He is angry at me. It is a very specific kind of being looked at.)"
    professor "Sit. Come to me when the class ends."
    "Then he says something short and flat in Japanese, to the board rather than to me."
    "The room absorbs it the way a room absorbs weather."
    mc "(Not one word of that was for me. I hope.)"

    "Somewhere behind us a chair drags and nobody looks at us, which is somehow worse than if they had."
    "Beside me, Hikari has gone back to her notes as though she has been sitting here the whole time. She has."
    mc "(Nobody is late to his class.)"
    mc "(The clerk told me about the bell. I should have checked the time.)"
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
    hide sister_standing with Dissolve(2.0)
    

    "I walk to the front. It is a long walk, and the room empties around me the whole way, and it is emptier when I get there."
    mc "Professor. I wanted to introduce myself properly. I'm [player_name]. I'm the exchange student."
    professor "I know what you are. I read your file. That is not what this is about."
    professor "This is about the clock."
    professor "Arrive at the bell, sit between the bell and my first word, and you have lost the first word."
    professor "Do that three times and you have lost the class."
    professor "If it happens again there will be consequences. I do not say that as a threat. It is a description."
    mc "I was registering downstairs. I'm sorry I missed the start."
    professor "Then next time, allow more time. You should be seated before I begin."

    # Basic attendance information is available on every branch. A modest Nerve
    # investment opens a respectful challenge about the official appointment,
    # including on the train route.
    menu:
        "I'll write that down.":
            "I open my notebook and write the class time at the top of the page."
            $ remember("professor", "wrote down the attendance rule")
        "It won't happen again.":
            mc "I'm sorry. I'll be here early from now on. I mean it."
            professor "Yes. You will."
            $ remember("professor", "apologised and promised to come early")
        "[tag_nerve] Can we discuss today's late mark?" if has_attribute_points("nerve", "nudge"):
            mc "Could we discuss today's late mark? Student Relations asked me to register before coming here."
            professor "..."
            professor "Bring me the registration slip. If the appointment overlapped my class, I will review it."
            mc "Thank you. I'll bring it tomorrow."
            $ reward_attributes_once("answer_clock_ask", [("grace", "micro_loss")], show="auto")
            $ remember("professor", "asked him to review the registration delay")

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
    mc "Five minutes early. That's what he expects."
    hikari "Notebook open, pen ready. Every class."
    mc "And that went better than expected?"
    hikari "It went better than expected."
    mc "How?"
    hikari "Because you stayed and spoke to him. People sometimes just leave."
    hikari "Then he spends the rest of the week looking for them."
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
    hikari "I thought we'd have more time. Then I saw the clock and panicked."
    hikari "I should have told you where to go before I ran off. I'm sorry."
    menu:
        "Next time, warn me before you go.":
            $ reward_attributes_once("answer_hikari_warning", [("nerve", "small"), ("grace", "micro_loss")], show="auto")
            mc "Next time, warn me before you go. I can't follow a route I don't know."
            hikari "Fair. I will."
            $ remember("hikari", "asked her not to leave without warning")
        "Thanks for saving me a seat.":
            mc "Thanks for saving me a seat, at least."
            hikari "Window side. You'll want it when the heating starts."
            $ remember("hikari", "thanked her for saving him a seat")
        "Let's get something to eat.":
            mc "Let's get something to eat. I'd rather not spend all afternoon thinking about it."
            hikari "That is a very good plan."
            $ remember("hikari", "chose to move on after the lecture")
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
            hikari "I pass it on the way to the library. You'll hear them before you see them."
            $ first_day_activity = "photo_club"

    # Said once, and only after he has picked, so the explanation of the free
    # afternoon arrives with something already happening underneath it.
    if not store.after_school_hint_shown:
        $ store.after_school_hint_shown = True
        $ renpy.call_screen("hint_card", eyebrow="Free Afternoons", body=store.hint_text_after_school)

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
    $ phone_map_visit("ramen_shop")
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

    voice "audio/VO/welcome.wav"
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
        "Ask for his recommendation.":
            mc "Sumimasen. Osusume... recommendation?"
            "He stops. He looks at me a second longer than he looked at the money, and then says something short to the pots."
            mc "(I might have said that wrong. He points at the second line and waits for my nod.)"
            $ reward_attributes_once("answer_ramen_recommendation", [("nerve", "small")], show="auto")

    chef "あいよ。"
    "He barks something at somebody. There is nobody else in the room. He is the kitchen and the waiter, and he is barking at himself."

    scene bg_ramen with walk_fade
    
    "A few minutes later he puts down a bowl. It is much darker than the picture I had in my head."
    "The broth is almost black. More pork than noodle. And a hill of green onions on top of that which should not be legal."
    mc "(I thought I was ordering something lighter. I don't know what I actually asked for.)"
    "He crosses his arms and looks at it, and then at me, which is a sentence in a language I can read."

    # Both answers lead to the same meal. Restore the counter shot before the
    # chef speaks, so his portrait never covers the food close-up.
    menu:
        "Ask what kind of broth it is.":
            mc "Sumimasen. Shoyu? Miso?"
            "He follows my finger towards the bowl."
            "He points to the dark bottle beside the stove."
            mc "(Soy sauce. That answers that.)"
            "I stop talking. He pushes the bowl half a centimetre towards me with one finger."
            $ reward_attributes_once("answer_ramen_broth", [("insight", "nudge")], show="auto")
            scene bg_ramen_shop with walk_fade
            chef "どうぞ。"
            mc "(That one I know. It means here you go. It also means eat it.)"
        "Try it before asking.":
            "I pick up the spoon before I can think about it, which he appears to consider the entire conversation."
            scene bg_ramen_shop with walk_fade
            chef "どうぞ。"
            mc "(That one I know. It means here you go. It also means eat it.)"

    "I eat it."
    "The first mouthful hits like something walking into a door. Rich and smoky and far too much. The second is better than the first."
    mc "...This is actually amazing."
    "I say it half under my breath, in English, to nobody."
    "He hears the tone of it even if he does not have the words. He does not turn around."
    chef "うまい、だろ？"
    "I catch one word of that. One. It is the word on the packet in the kitchen and on the sign two doors down from the house."
    menu:
        "Tell him in Japanese.":
            mc "Umai. Arigatou gozaimasu."
            # Meeting him in his language after he hears the reaction.
            $ reward_attributes_once("chef_first_umai", [("grace", "small")], show="auto")
        "Ask what gives it the smoky flavour.":
            mc "The pork? Is that where the smoky taste comes from?"
            "He taps the edge of the grill with his ladle."
        "Smile and keep eating.":
            "I nod with the spoon still in my hand. He turns back to the stove."

    "He snorts. A small sound, killed immediately. Something in his face moves for a quarter of a second before he turns back to the pots."
    "He says nothing else. I slurp, badly, and get broth on the counter, and he does not comment."
    "I am fairly sure that is the compliment."

    # All three ways of ordering and both answers end in this same bowl, so the rest
    # of the meal is not a choice and is not played out. It is summarised on black,
    # and every route comes back through it to the same empty bowl, the same bill,
    # and the same walk home.
    scene black with Dissolve(2.0)
    "Two men came in while I ate. I watched how they held their chopsticks and tried the same grip."
    "Chopsticks in one hand, spoon in the other, head down over the bowl."
    "I ended up finishing the whole bowl, soup and all. There was nothing left in it but the pattern on the bottom."

    scene bg_ramen_empty with Dissolve(2.0)

    "When I finish I put the thousand yen back on the counter."
    "This time he takes it, counts the change without looking, and sets it beside my hand."
    $ spend_money(900)
    "A hundred yen. Nine hundred for the bowl. I do not know what I actually ordered and I do not think I ever will."
    mc "(Not what I expected. I'd order it again.)"

    $ confidant_visits["chef"] = 1
    $ remember("chef", "sat down in his shop and finished the bowl")

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
    mc "Yeah. Hikari put it on here. My host sister. She set the whole thing up before I landed."
    "He grunts, which is what he does instead of a nod."
    "Then he turns a small laminated card round on the counter so that it is facing me."
    "A black square made out of smaller black squares. Under it, six words in English, in handwriting that is not his."
    chef "「読め」"
    mc "(Read it. That one is no mystery either. I am learning to read this room instead of the language.)"
    "I hold the phone over the card. The app takes it without asking me anything, and puts a name on the list."
    mc "So I know if you're shut before I walk down here for nothing."
    "He turns the card back round and goes to the pots, which is the conversation over."
    $ wire_unlock("chef")
    # Forced closer for the walk route. Finding the shop by getting lost is the
    # Insight beat that matches the run's Nerve and the club's Grace.
    $ reward_attributes_once("walk_first_found", [("insight", "small")], show="card")
    $ chef_affection += 1

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
    father "Don't make it a pattern. You still have school tomorrow."
    father "Dinner is still warm. Sit down before you go upstairs."
    mc "Sorry Hikari, I should have listened and come home with you."
    mc "But on the bright side, I found this ramen place with a red lantern over the door."
    mc "Four seats. One man. He gave me a bowl I didn't order, and it was the best thing I've eaten here."
    hikari "..."
    hikari "The one near the two convenience stores."
    mc "You know it?"
    hikari "Yes I do. I go there sometimes, when I don't want to be in this house."
    mc "(That is the first thing she has told me about this house that she chose to tell me.)"
    hikari "Come on. If we leave it any longer, Dad will decide dinner is over."
    jump first_evening_dinner


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
        "Thanks for coming back with me.":
            mc "Thanks for coming back with me. You must have had other things to do."
            hikari "You're welcome. Don't make it a thing."
            $ reward_attributes_once("answer_run_thanks", [("grace", "nudge")], show="auto")
        "How long have you lived here?":
            mc "Have you lived on this street your whole life?"
            hikari "Since primary school. Mom still calls the bakery by its old name."
            $ reward_attributes_once("answer_run_history", [("insight", "nudge")], show="auto")
        "Which turn is ours?":
            mc "Which turn is ours? The one after the bakery?"
            hikari "Yes. Then straight until you see the blue gate."

    "We get to the house and she does not go in."
    mc "(She is not going inside.)"
    hikari "Would you like to go for a run?"
    hikari "I'm running after this. You can come if you want."

    menu:
        "Out where?":
            mc "Out where?"
            hikari "The river. Two or three times a week, except the weeks it's five. Tonight counts."
        "Can I come?":
            mc "Can I come?"
            hikari "..."
            hikari "Yes. You can come."
            $ reward_attributes_once("answer_run_join", [("nerve", "micro")], show="auto")
        "I don't run.":
            # A real soft exit. Declining costs nothing; it simply sends him home
            # while she keeps the route that was already hers.
            mc "I'm tired. I don't think I can run tonight."
            hikari "..."
            hikari "Fine. I'm still going."
            hikari "Don't wait up. And don't let Dad start a speech without me."
            $ declined_first_run = True
            $ remember("hikari", "declined the first river run")
            jump after_school_run_declined

    hikari "Go and change into something you can move in."
    mc "Oh? You're serious."
    hikari "I'm going to change as well. Let's meet in the front yard. Don't take an hour."

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
    play music "audio/Music/(shibuya night?) rain_at_the_crossing.mp3" fadein 2.0

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
    mc "(Cold, at least. Right now that's enough.)"
    hikari "You're not unfit. You're just new. Those are different things and it's rude to confuse them."
    mc "Thank you."
    hikari "That wasn't a compliment. That was a diagnosis."

    "We drink them under the lamp, listening to the water move past."

    menu:
        "Let her enjoy the quiet.":
            "I sit beside her and leave the silence alone."
            hikari "..."
            "Her shoulders settle. She puts the empty can down between her feet."
            $ reward_attributes_once("answer_river_quiet", [("grace", "small")], show="auto")
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
    # Small, not medium: the three first-afternoon routes should close at a
    # similar weight. Walk and photo use the same size on their forced beat.
    $ reward_attributes_once("run_first_river", [("nerve", "small")], show="card")
    $ sister_affection += 1
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
    father "It's a school night. You are expected home by eight. That's the rule."
    hikari "I know. I'm sorry."
    mc "It's my fault. I asked her to show me the river."
    father "..."
    father "The river."
    mc "The path along it. I didn't know how far it went."
    "Hikari does not correct me, which for a second is louder than anything she has said all day."
    mother "You could have asked someone to call home. We didn't know if you were safe."
    hikari "We got talking, and then we were halfway there, and we lost track of it."
    father "Lost track."
    hikari "We got lost in the conversation. It won't happen again."
    father "..."
    father "Dinner is still warm. Sit down before you go upstairs."
    mc "(He doesn't raise his voice. Somehow that makes it harder to answer.)"
    hikari "We'll eat first. Come on."
    jump first_evening_dinner


label after_school_run_declined:

    # He said no, and the game means it. She keeps the river; he keeps the house.
    # WIRE still unlocks tonight — she put the app on his phone in the first place —
    # but the Nerve card for finishing the run does not fire.

    scene bg_home_exterior_day with walk_fade

    "She turns toward the river without waiting for me to change my mind."
    "I watch her until the street bends and takes her, and then I am alone with the blue gate."
    mc "(That was the first invitation I have refused in this country.)"
    mc "(It feels smaller than I expected. And also worse.)"

    scene bg_home_day with walk_fade

    "Inside, the house is still in its afternoon shape. Mother's shoes by the door. A radio somewhere on low."
    mother "Back already?"
    mc "Hikari went for a run. I stayed."
    mother "Good. You look tired enough for two people."
    mother "There's barley tea in the fridge. Help yourself. Dinner is at eight, same as always."
    "She leaves me the kitchen and a glass that is already clean."

    "I drink the tea. I look at the street through the kitchen window. I do not open WIRE."
    mc "(If I open it now, there will be nobody on it, and that will feel like a decision I already made.)"

    window hide
    scene black with Dissolve(1.5)
    "The light outside thins. Someone comes home. The clock does the rest."

    scene bg_home_night with Dissolve(1.5)

    "Hikari comes back through the door with her hair damp and her face flushed the colour of exercise."
    hikari "You actually stayed."
    mc "You told me to."
    hikari "I told you not to wait up. That is different."
    "She drops her shoes, drinks water straight from the tap, and holds her hand out."
    hikari "Phone."
    mc "Why."
    hikari "Because I'm not explaining it twice, and because you are not getting out of this just because you sat on a chair."
    "I hand it over. She opens WIRE, finds her own name missing, and puts it there."
    hikari "Add me so I can tell you when I'm running late. And when I'm not coming home."
    mc "That's cheerful."
    hikari "It's practical."
    $ wire_unlock("hikari")
    $ sister_affection += 1
    $ remember("hikari", "added her on WIRE after declining the run")

    father "Dinner."
    "One word from the kitchen, and the conversation is over."
    hikari "Come on. He means both of us."
    jump first_evening_dinner


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
    $ phone_map_visit("photo_club")

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
        "Is this the photography club?":
            mc "Is this the photography club? I saw the notice downstairs."
            sim "Yes. No fees, no pressure, just us and some cameras and a great deal of trial and error."
        "Could I join today's session?":
            mc "Could I join today's session? I haven't done this with other people before."
            sim "Of course. There's a chair right here. We were just getting started."
            $ reward_attributes_once("answer_circle_join", [("nerve", "small")], show="auto")
        "Hikari told me I could drop in.":
            mc "Hikari said I could drop in. Is now a good time?"
            sim "Perfect timing. Come and sit with us."

    "I sit in the gap, which is exactly one person wide, next to a boy asleep with his arms folded and entirely committed to it."

    sim "So. Here is the whole club, and then you can decide about us."
    sim "Some come to build a portfolio. Some for the practice."
    sim "Some because they wanted somewhere to be on a Tuesday and this room was open."
    sim "Everybody gives what they have and takes what they need. It works both ways. Nobody pays, and nobody has to be any good."
    mc "(That is the second time in one day that somebody has explained a thing in this country by telling me what it gives other people.)"

    sim "So. Do you have a camera?"

    menu:
        "My camera's at home.":
            mc "My camera's at home. I wasn't expecting to come here today."
        "Only my phone today.":
            mc "Only my phone today. Will that be okay?"

    "I look at my hands, which are empty, and he follows my eyes down to them."
    sim "Then we'll use your phone."
    sim "Phone cameras are better than most beginners realise."
    sim "Start with the light, not the settings. Look at the wall beside the window."
    "He gestures across the room. I raise the phone and take a picture."
    sim "There. Now you have shot something. A little crooked, perhaps, but we can work with it."
    sim "See? First step. Half the prints on that wall started exactly like that one."
    sim "What do you notice?"
    menu:
        "The window is brighter than everything else.":
            mc "The window's so bright I can barely see the wall. Would leaving it out of the frame help?"
            sim "Try it."
            "I turn a little and take another picture. This time the strip of light on the wall keeps its shape."
            sim "There it is. Same room, different photograph."
            $ reward_attributes_once("sim_circle_first", [("insight", "small")], show="auto")
        "I tilted the phone.":
            mc "I tilted the phone. The door looks like it's falling over."
            sim "Easy to do. Try lining it up with the side of the screen."
        "I'm not sure what to look for yet.":
            mc "I'm not sure what to look for yet."
            sim "That's fine. Take a second one and compare them. Start with what changes."

    sim "I should say who I am, since I am the strange one here. I don't study here. I come in twice a week because they let me."
    sim "By day I am in an office with the numbers. This is the other half of the day, and this is the half I would keep."
    sim "Ten years in this country, and I still feel like a beginner most days. I have decided that is the good part."

    menu:
        "How did Circle start?":
            mc "How did Circle start?"
            sim "A few people wanted somewhere to show their photographs. We borrowed a room and kept coming back."
        "Do you shoot outside the club too?":
            mc "Do you shoot outside the club too?"
            sim "Whenever I can. Walking with a camera is a very good excuse to take the long way home."

    "The woman from the argument says something across the room."
    "He answers her in Japanese without changing gear, then comes back to me in English."
    sim "「彼女が今日のモデル。今回のテーマは自然な笑顔だって。」"
    sim "She is modelling for us today, and the theme is a natural smile. Which means she is about to make every one of us work for it."
    sim "See? A little ecosystem. Everybody gets something."
    sim "She gets practice, they get their portfolio, and nobody has to be anybody's boss."

    menu:
        "Can I help set things up?":
            mc "Can I help set things up? She shouldn't have to move all those chairs herself."
            sim "Yes, thank you. Leave her some space by the window."
            "I move the spare chairs back against the wall while she sets her bag down."
            $ reward_attributes_once("answer_circle_help", [("grace", "small")], show="auto")
        "Can I watch for a while first?":
            mc "Can I watch for a while first? I'd like to see how you work."
            sim "Absolutely. Sit where you can see, and ask whenever you want."
        "Do you choose a new theme each week?":
            mc "Do you choose a new theme each week?"
            sim "Usually. Someone suggests one, then we see what everyone makes of it."

    sim "You don't have to join anything. Come. Sit. Look at what people put on the wall. That is the whole club."
    sim "Join us whenever you are ready. Everybody here started by sitting in that chair and saying nothing."

    sim "Right. Everyone."
    sim "「今日も楽しくやりましょう！」 Let's have fun today!"
    "The room cheers, lightly, the way a room cheers when it does this every week."
    "Somebody takes a print off the wall and starts arguing again."

    "He turns back to the prints and starts talking about one of them."
    "He does not ask me a single question about where I am from."
    "By the end of the hour I am fairly sure that is the kindest thing anybody in this city has done for me."
    mc "(My phone has two new photographs on it. Neither looks like the ones on the wall.)"

    $ confidant_visits["sim"] = 1
    $ remember("sim", "joined the first session with his phone camera")

    # He does not gate the club behind anything, so the group is the one thing he
    # has to give that costs him nothing and asks nothing. He gives it the same
    # way he gave the phone back an hour ago: like it was already mine.
    sim "Oh - wait. One thing before you go."
    sim "You have WIRE, don't you? Everybody in this room does."
    mc "Hikari put it on my phone. My host sister. I haven't really used it."
    sim "Then you are already most of the way in. That is the entire entry requirement."
    "He puts his hand out, the way he did an hour ago, and this time I hand the phone over without thinking about it."
    sim "There is a group. It is called Circle, and it is older than the room is."
    sim "Everybody posts what they shot that week. We share ideas between meetings too."
    mc "Should I post the ones I took today?"
    sim "(grinning) Please do. We'd love to see them."
    "He opens the group invitation and hands the phone back. I type my name, and WIRE saves the invitation."
    mc "I can't see the posts yet."
    sim "Not without a signal. They will be there when you get connected."
    $ wire_unlock("sim")
    # Forced closer for the photo route. Sitting in a room of strangers and staying
    # is the Grace beat that matches the other first-afternoon finales.
    $ reward_attributes_once("photo_first_session", [("grace", "small")], show="card")
    $ sim_affection += 1

    "By the time I leave, the windows have gone dark. Sim walks me to the door and writes the next meeting time on a spare flyer."
    "Bring the camera if you like, he says. The phone is fine too."
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
    hikari "I've been sitting here since eight. Dad's been pretending to read the same page."
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
    father "Dinner is still warm. Come in and eat."
    mc "(He leaves it there. I can't tell if that's better.)"
    hikari "Come on. Before he finds another sentence."
    jump first_evening_dinner


################################################################################
## ACT ONE, TENTH BEAT: THE END OF THE FIRST DAY
################################################################################
##
## Every road out of the first afternoon arrives here. Whatever he chose, the day
## closes the same way: the stairs, the light off, and the whole of it played back
## in the dark. One label for all three, because the shape of the ending belongs
## to the day rather than to the place he ended it.

init python:
    def build_first_day_memory_deck(activity):
        common = [
            ("station", "The morning platform", "bg_station", "#76c6d9"),
            ("student_id", "A new student card", "images/ui/student_card.png", "#a9c8a4"),
            ("lecture", "The first lecture", "bg_lecture_hall", "#d4b77a"),
            ("home", "The house at night", "bg_home_exterior_night", "#8d9db9"),
        ]

        if activity == "walk_alone":
            route = [
                ("alley", "The wrong turn", "bg_alley", "#c07c56"),
                ("ramen_shop", "The red-lantern shop", "bg_ramen_shop", "#e38c55"),
                ("ramen_bowl", "The bowl I finished", "bg_ramen", "#d1a353"),
                ("chef", "The card on the counter", "images/characters/chef.png", "#b59a79"),
            ]
        elif activity == "walk_hikari":
            if store.declined_first_run:
                route = [
                    ("gate", "The blue gate alone", "bg_home_exterior_day", "#65aeb1"),
                    ("tea", "Barley tea in the kitchen", "images/backgrounds/bg_kitchen_day.png", "#e8c686"),
                    ("wire", "Her name on WIRE", "images/characters/sister.png", "#df8ea5"),
                    ("home_wait", "Dinner called from the kitchen", "images/backgrounds/bg_home_inside_night.png", "#8d9db9"),
                ]
            else:
                route = [
                    ("river", "The river path", "bg_river", "#65aeb1"),
                    ("running", "Hikari at a run", "images/characters/sister_run.png", "#df8ea5"),
                    ("kitchen", "The kitchen light", "images/backgrounds/bg_kitchen_night.png", "#e8c686"),
                    ("home_wait", "Someone waiting at home", "images/backgrounds/bg_home_inside_night.png", "#8d9db9"),
                ]
        else:
            route = [
                ("club", "The room called Circle", "bg_photo_club", "#67b8d0"),
                ("sim", "Sim at the door", "images/characters/sim.png", "#86c2d4"),
                ("campus", "The campus corridor", "bg_campus_interior", "#9aa9bd"),
                ("club_hall", "The club's hallway", "bg_department_hall", "#b4a68d"),
            ]

        cards = []
        for pair_id, title, art, accent in common + route:
            for copy in range(2):
                cards.append({
                    "pair": pair_id,
                    "title": title,
                    "art": art,
                    "accent": accent,
                })

        return cards


screen day_memory_match(cards, matched, misses, reveal_pair=None, preview=False):
    modal True
    zorder 100
    default first_selection = None
    default previewing = preview

    add Solid("#070b11")
    add Solid("#101923") xysize (config.screen_width, 1) ypos 118

    vbox:
        xalign 0.5
        ypos 20
        spacing 5

        text "FIRST NIGHT / MEMORY":
            xalign 0.5
            size 11
            kerning 3
            color "#8193a5"
            outlines []

        text "KEEP THE DAY TOGETHER":
            xalign 0.5
            size 28
            kerning 2
            color "#c5e0e8"
            outlines []

        text "Study the revealed board, then find all eight pairs before the third mismatch.":
            xalign 0.5
            size 15
            color "#a7b5c1"
            outlines []

    hbox:
        xalign 0.5
        ypos 103
        spacing 22

        text "PAIRS [len(matched) // 2] / 8":
            size 12
            kerning 2
            color "#7fc8bd"
            outlines []

        text "MISMATCHES":
            size 12
            kerning 2
            color "#8193a5"
            outlines []

        for mark in range(3):
            add Solid("#df8e8e" if mark < misses else "#27313b") xysize (28, 4) yalign 0.5

        text "[misses] / 3":
            size 12
            color "#c6d0d7"
            outlines []

    grid 4 4:
        xalign 0.5
        ypos 139
        spacing 11

        for i in range(len(cards)):
            $ face_up = previewing or i in matched or i == first_selection or (reveal_pair and i in reveal_pair)

            button:
                xysize (222, 112)
                background Solid("#111a24")
                hover_background Solid("#1b2936")
                sensitive (not previewing and not reveal_pair and i not in matched and i != first_selection)

                if first_selection is None:
                    action [
                        Play("sfx", "audio/SFX/type_click.wav"),
                        SetScreenVariable("first_selection", i),
                    ]
                else:
                    action [
                        Play("sfx", "audio/SFX/type_click.wav"),
                        Return((first_selection, i)),
                    ]

                fixed:
                    xysize (222, 112)

                    if face_up:
                        add Transform(cards[i]["art"], xysize=(222, 112), fit="cover")
                        add Solid("#071018c8") ypos 77 xysize (222, 35)
                        add Solid(cards[i]["accent"]) xysize (4, 112)

                        text cards[i]["title"]:
                            xpos 14
                            ypos 84
                            xmaximum 194
                            size 13
                            color "#f0f3f4"
                            outlines [(1, "#071018", 0, 0)]

                        if i in matched:
                            text "REMEMBERED":
                                xpos 12
                                ypos 8
                                size 8
                                kerning 1
                                color "#d7f0e5"
                                outlines [(1, "#071018", 0, 0)]
                    else:
                        add Solid("#17232e")
                        add Solid("#2b3c49") xysize (222, 1)
                        add Solid("#7fc8bd") xysize (3, 112)

                        text "ELSEWHERE":
                            xalign 0.5
                            yalign 0.43
                            size 15
                            kerning 3
                            color "#b9d1d8"
                            outlines []

                        text "DAY 01  /  MEMORY":
                            xalign 0.5
                            yalign 0.73
                            size 8
                            kerning 2
                            color "#647b8a"
                            outlines []

    if previewing:
        timer 6.0 action SetScreenVariable("previewing", False)
    elif reveal_pair:
        timer 0.85 action Return(None)

    hbox:
        xalign 0.5
        ypos 638
        spacing 12

        text ("MEMORIZE THE BOARD" if previewing else "MATCH THE MOMENTS"):
            size 10
            kerning 2
            color "#7b8b98"
            outlines []

        text ("The cards will turn over in a few seconds." if previewing else "The day is already starting to blur."):
            size 12
            color "#a7b5c1"
            outlines []


label first_evening_dinner:

    scene bg_kitchen_night with Dissolve(1.0)
    stop music fadeout 1.0
    play music "audio/Music/room_night.mp3" fadein 1.5

    "Mother has kept dinner warm. Rice, grilled fish, soup, and a small dish of natto sit between us."
    "The fermented soybeans smell sharper than anything else on the table."
    mother "You don't have to finish everything. Try what you like."
    father "No one is grading you."
    hikari "He says that like he hasn't been grading the rest of the day."
    father "I have not."
    "For the first time since I came home, the corner of his mouth moves."

    menu:
        "Try a little natto, and admit you're not sure about it.":
            "I take a small bite. The texture is stranger than the taste."
            mc "I can try it. I'm not sure I like it yet."
            father "That's fair. I didn't like it the first time either."
            hikari "You still make that face."
            father "I do not."
            mother "You do."
            $ father_affection += 1
            $ reward_attributes_once("first_dinner_natto", [("nerve", "micro")], show="auto")
            $ remember("father", "was honest about trying natto")
        "Ask Father how he got used to living here.":
            mc "Did it take you long to get used to this neighborhood?"
            father "I grew up two stops away. Your mother moved here after we married."
            mother "And he still gets lost in the department store."
            father "That place has eight floors."
            mc "I'm starting to understand the problem."
            father "You'll learn the streets. It takes time."
            $ father_affection += 1
            $ reward_attributes_once("first_dinner_neighborhood", [("insight", "micro")], show="auto")
            $ remember("father", "talked about learning the neighborhood")
        "Thank them for waiting and apologize without making an excuse.":
            mc "I'm sorry I kept you waiting. I should have found a way to let you know."
            father "You didn't have a working connection. Next time, ask someone to call."
            mc "I will."
            mother "That's all we wanted to hear."
            $ father_affection += 1
            $ reward_attributes_once("first_dinner_apology", [("grace", "micro")], show="auto")
            $ remember("father", "apologized for keeping the family waiting")

    father "The rule isn't there to make you ask permission for everything."
    father "If you're late, we need to know you're safe. That's all."
    mc "I understand. I'll tell you before I go somewhere after school."
    father "Good."
    "He passes me the soup without looking up. It is the first thing he has handed me all evening."

    "We eat. The rice is warm, and the table gets easier to sit at."
    "When dinner is over, Hikari stacks the bowls and points me toward the stairs."
    hikari "Come on. I'll walk you up."
    jump end_of_first_day


label end_of_first_day:

    scene bg_room_night with stair_fade
    $ room_ambient(True)

    "Upstairs, the door shuts behind me and the house goes quiet."
    "The quiet a house makes when everyone has agreed to stop talking about something."
    "I sit on the edge of the bed with my bag in my lap and go through the day from the beginning."
    "I want to hear whether it sounds real."
    "A station at nine in the morning, and a sister who took me the long way for no reason she would give."
    "A professor who expects everyone seated before the bell. A student card with my photograph on it."
    "And then an afternoon that belonged to nobody but me."

    if first_day_activity == "walk_alone":
        mc "(Two convenience stores. The blue cloth. I should write down the street name tomorrow.)"
        mc "(Somewhere four minutes from this house there is a man who will not remember my face.)"
        mc "(And a bowl I will think about for a week.)"
    elif first_day_activity == "walk_hikari":
        if declined_first_run:
            mc "(I said no to the river. She went anyway. That is still a kind of answer.)"
            mc "(Later she put her name on my phone like it was unfinished business.)"
        else:
            mc "(I ran until I could not breathe, next to somebody who was not out of breath at all.)"
            mc "(She showed me a thing she does not show anybody, and then she walked me home and got shouted at for it.)"
    else:
        mc "(I walked into a room full of strangers and nobody asked me a single question about where I come from.)"
        mc "(There are prints on that wall with marker on them. Somebody was angry about a photograph. That is the whole club.)"

    mc "(Yesterday I got off a plane without knowing one word of the language.)"
    mc "(Today I found a place, or a person, or a room I would not have found if I had stayed home.)"

    "I sit on the edge of the bed and check WIRE once more."
    if first_day_activity == "walk_alone":
        mc "(The chef's hours are here. The rest of the app still has nothing to show me.)"
    elif first_day_activity == "walk_hikari":
        mc "(Hikari's name is here. I can see the profile, but not send anything.)"
    else:
        mc "(Sim's invitation is saved. The group is still waiting for a connection.)"

    "The contact record is on the phone. The rest of WIRE is still out of reach."
    "A knock comes at the door, and Hikari opens it before I can answer."
    show sister_standing with dissolve
    hikari "You're still up."
    if first_day_activity == "walk_alone":
        mc "The chef's contact is there. I can't check if his hours change before I walk over."
    elif first_day_activity == "walk_hikari":
        mc "Your profile is there. I can't message you when I'm away from Wi-Fi."
    else:
        mc "Sim's Circle invite is saved. I can't load the group's posts yet."
    hikari "Right. The contacts stay on the phone. Messages and new posts need data."
    mc "I thought it was supposed to be on the phone already."
    hikari "The app is. The connection isn't."
    "She leans against the doorframe, the practical part of her already making a list."
    hikari "Tomorrow after school, we'll go to Akihabara and get you a plan."
    hikari "You already have a phone."
    hikari "We just need a sensible student plan, not a new handset and twelve things you don't need."
    mc "You know how to do that?"
    hikari "I know how to say no when somebody tries to sell us something extra."
    mc "That sounds useful."
    hikari "It is. Get some sleep. I'll come get you in the morning."

    menu:
        "Thank her for helping me figure it out.":
            mc "Thanks for helping me figure it out. I don't know how any of this works yet."
            hikari "That's why I'm explaining it."
            $ sister_affection += 1
            $ reward_attributes_once("first_night_hikari_thanks", [("grace", "micro")], show="auto")
        "Tell her she makes the house easier to understand.":
            mc "You make this house easier to understand."
            hikari "Don't tell anyone. I have a reputation."
            $ sister_affection += 1
            $ reward_attributes_once("first_night_hikari_observation", [("insight", "micro")], show="auto")
        "Promise you'll be ready when she comes to get you.":
            mc "I'll be ready when you come get me."
            hikari "You'd better be. I'm not waiting outside your door."
            $ sister_affection += 1
            $ reward_attributes_once("first_night_hikari_promise", [("nerve", "micro")], show="auto")
    hide sister_standing with dissolve

    "I put the phone beside my student card and turn off the lamp."
    mc "(Five minutes early. Notebook open. Pen out.)"
    "The day starts to break apart behind my eyes: the platform, the classroom, the place I chose."
    "I try to hold on to the order they came in."
    window hide
    scene black with Dissolve(2.5)
    stop music fadeout 2.0
    call first_night_memory
    jump second_morning


label first_night_memory:
    play music "audio/Music/dream sequence.wav" fadein 2.0
    $ day_memory_cards = build_first_day_memory_deck(first_day_activity)
    $ renpy.random.shuffle(day_memory_cards)
    $ day_memory_matched = []
    $ day_memory_misses = 0
    $ day_memory_preview = True

    while len(day_memory_matched) < len(day_memory_cards) and day_memory_misses < 3:
        call screen day_memory_match(day_memory_cards, day_memory_matched, day_memory_misses, None, day_memory_preview)
        $ day_memory_preview = False
        $ selected_pair = _return

        if day_memory_cards[selected_pair[0]]["pair"] == day_memory_cards[selected_pair[1]]["pair"]:
            $ day_memory_matched.extend(selected_pair)
        else:
            $ day_memory_misses += 1
            call screen day_memory_match(day_memory_cards, day_memory_matched, day_memory_misses, selected_pair, False)

    if len(day_memory_matched) == len(day_memory_cards):
        "The last two pictures settle into place. For a moment, the whole day makes sense in order."
        $ reward_attributes_once("first_night_memory_pairs", [("insight", "nudge")], show="auto")
    else:
        "Three wrong pairs, and the day slips out of order again."

    stop music fadeout 2.0
    return


label second_morning:
    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "I wake before the alarm, with the dream still caught in the back of my mind."
    mc "(The station was there again. This time the signs had no words on them.)"
    mc "(I knew where the train was going anyway. I just couldn't remember how.)"
    "The dreams are getting stranger. I try to make a list of what they have in common, and the list keeps changing."
    "A knock taps twice against the door."
    hikari "You awake? Breakfast. Dad's already asking questions."
    mc "About me?"
    hikari "About everything. Get dressed."
    "She waits just long enough to make sure I heard, then disappears down the stairs."

    scene bg_kitchen with walk_fade

    "The kitchen is bright with morning. Mother has set rice, miso soup, and grilled fish on the table."
    mother "Eat while it's warm. You have a full day."
    mc "Thank you. It smells great."
    father "How was your first day?"
    hikari "And don't start with the clock again."
    father "I was asking about the day."
    mc "A little confusing. I was late to class, but I found somewhere to go after school."

    if first_day_activity == "walk_alone":
        mc "I got lost and found a ramen shop. The chef gave me his WIRE contact."
        father "You got lost and made a contact. That is one way to do it."
    elif first_day_activity == "walk_hikari":
        if declined_first_run:
            mc "Hikari went running. I stayed home. She added me on WIRE when she got back."
            hikari "He was honest about being tired. That counts."
            father "Good. Better that than promising something he can't do."
        else:
            mc "Hikari showed me the river path. I added her on WIRE."
            hikari "He kept up for most of it."
            mc "That is not what happened."
    else:
        mc "I went to the photography club. Sim invited me to their group."
        father "A club already. You have been here one day."

    father "WIRE. What is that?"
    mc "It's an app for contacts. Some people use it for groups too, but I need an internet connection to load anything new."
    father "I haven't kept up with every new app. You mean the phone has no data?"
    hikari "He only has Wi-Fi. Outside the house, the app can't sync."
    father "Then get a proper plan. Just don't let the shop put you on a plan with extras you don't need."
    hikari "We won't. I'll take him to Akihabara after school."
    father "Read the monthly cost. Read the contract. If it says free, find out when it stops being free."
    hikari "I know, Dad."
    mother "He is helping, in his own way."
    father "I am helping."
    mc "(They have the same conversation every morning. I think that is how I know I am starting to belong here.)"

    mother "There's more fish if you're still hungry."
    hikari "We should leave soon. Today we are not going to run for the train."
    mc "I thought the proper way was the long way."
    hikari "It is. We can be early on the proper way."
    "I finish breakfast, pack my notebook, and make sure the student card is still in my bag."

    jump second_school_day


label second_school_day:
    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The route feels less like a test today. I recognize the corner shop and the station entrance."
    hikari "Tell me which platform we should take."

    menu:
        "The one on the left.":
            mc  "The one on the left. Local train, not the rapid."
            hikari "Good. You were listening yesterday."
            $ reward_attributes_once("answer_left", [("insight", "nudge")], show="auto")
        "The one on the right.":
            $ reward_attributes_once("answer_right", [("insight", "micro_loss")], show="auto")
            mc  "The one on the right. Rapid train, not the local."
            hikari "What? You were listening to anything I said yesterday?"
            hikari "Anyways let's get to the platform. We can talk on the train."

    "On the train she tells me which parts of Akihabara are older than the signs make them look, and which streets fill up before lunch."
    hikari "It is easier to get around when you know what you are looking for."
    mc "And if I don't?"
    hikari "Then you look around until something answers."

    scene black with Fade(1.0, 0.3, 0.0)
    stop music fadeout 1.0
    "The underground train carries us across the city."
    "By the time we come up near campus, the morning has found its pace."

    scene bg_school_gate with Fade(0.0, 0.0, 1.5)
    play music "audio/Music/school.mp3" fadein 1.5

    "We reach the gate with enough time to walk instead of hurry."
    hikari "Look at that. A whole morning without sprinting."
    mc "I am learning."
    hikari "Don't get used to the praise."

    scene bg_department_hall with walk_fade
    "The corridor is busier than yesterday. I find the lecture room before the bell."
    "At five minutes to nine, my notebook is open and my pen is ready."

    scene bg_lecture_hall with walk_fade
    professor "You are early today."
    mc "I remembered what you said."
    professor "Good. Then remember this as well. Today we begin with haiku."
    "He writes three short lines on the board, then circles a single word."
    professor "A haiku is often taught as five, seven, five. In Japanese, those are mora, not English syllables."
    professor "For today's lesson, remember the kigo: the seasonal word. It places the poem in a time of year, even when the poem never names that season directly."
    "He reads an example aloud. A frog, an old pond, the sound of water."
    "The room is still for a moment after he finishes."
    professor "The small detail is not decoration. It is the door into the whole poem."
    mc "(A season hidden inside one word. I write it in the margin.)"
    professor "You will see this again. Pay attention to what the word is doing, not only to how many syllables you can count."

    menu:
        "Take careful notes on the kigo.":
            $ haiku_study_method = "notes"
            mc "(I write: kigo = seasonal word; notice what it implies.)"
            $ reward_attributes_once("haiku_lesson_notes", [("grace", "nudge")], show="auto")
        "Listen closely to the example.":
            $ haiku_study_method = "listening"
            mc "(I set the pen down and listen to the poem again, looking for the season in the image.)"
            $ reward_attributes_once("haiku_lesson_listen", [("insight", "nudge")], show="auto")
        "Look up more examples online after class.":
            $ haiku_study_method = "research"
            mc "(I mark the word and make a note to compare a few translations later.)"
            $ reward_attributes_once("haiku_lesson_research", [("nerve", "nudge")], show="auto")

    "The bell rings. The professor closes his book, and the room breaks into conversation."
    hikari "You made it through a whole lecture on time."
    mc "I even wrote something down."
    hikari "Then let's not waste the rest of the day. Akihabara."
    mc "Now?"
    hikari "Now. The shop is less crowded before everyone gets out of work."

    scene black with Fade(1.5, 0.4, 0.0)
    stop music fadeout 1.0
    "We take the underground train. The stations pass in a bright sequence of names, transfers, and doors."
    "When we come back above ground, Akihabara is already louder than the train."

    scene bg_akihabara_hamada_outside with Fade(0.0, 0.0, 1.8)
    $ phone_map_visit("akihabara")
    "Hamada Denki rises over the intersection, floor after floor of glass and red signs."
    hikari "Eight floors. Cosmetics, refrigerators, cameras, console games, and parts for things I've never heard of."
    hikari "If you need to buy something and don't know where to start, this is usually the place."
    mc "And today?"
    hikari "A cellular plan. You already have a phone; we do not need to buy you another one."
    hikari "Stay close, and let me do most of the talking. If they ask you something, answer honestly. If they offer an extra, wait until we know what it costs."
    mc "Understood."
    hikari "Good. Let's go."

    scene bg_akihabara_hamada_inside with walk_fade
    stop music fadeout 1.0
    play music "audio/Music/hamadadenki.mp3" fadein 1.5

    "The entrance opens onto a bright floor that seems to run all the way to the ceiling."
    "Displays rise above the counters. A sign points up to cameras, games, appliances, audio, and mobile service."
    mc "(The outside looked enormous. From in here it looks like the outside was only the first room.)"
    hikari "Phones and service are on this floor. We're not shopping for a handset."
    "A staff member with a tablet approaches us."
    hamada_staff "Welcome to Hamada Denki. Are you looking for a phone today?"
    hikari "Not a phone. He needs a cellular plan for a device he already owns."
    hamada_staff "Of course. Is this your first plan in Japan?"
    if first_day_activity == "walk_alone":
        mc "Yes. Mostly maps, and a way to check a place's hours before I head out."
    elif first_day_activity == "walk_hikari":
        mc "Yes. Mostly maps, and a reliable way to reach my family when plans change."
    else:
        mc "Yes. Mostly maps, messages, and the Circle group Sim invited me to."
    hamada_staff "Then let's compare the student plans before we add anything."

    menu:
        "A basic plan is enough for now.":
            mc "A basic plan sounds right. I want to keep the monthly cost predictable."
            hamada_staff "Then we can start with the student plan and check whether its data allowance fits."
            $ reward_attributes_once("cellular_plan_modest", [("insight", "micro")], show="auto")
        "I would rather have enough data not to worry about every search.":
            mc "I would rather have enough data not to worry about every search."
            hamada_staff "We can compare the next tier too, and look at the monthly difference before you decide."
            $ reward_attributes_once("cellular_plan_usage", [("nerve", "micro")], show="auto")
        "Could we see the lowest student rate first?":
            mc "Could we see the lowest student rate first?"
            hamada_staff "Certainly. Your student ID may qualify you for the student discount."
            $ reward_attributes_once("cellular_plan_student_rate", [("grace", "micro")], show="auto")

    hamada_staff "May I see your student ID?"
    "I take the card from my wallet and pass it across the counter."
    hamada_staff "Thank you. This confirms your student discount. The account details you already registered will verify the line."
    hikari "And this plan is only the monthly data and calls? No handset payment?"
    hamada_staff "Correct. The phone is yours already. The student plan has a monthly fee; calls are charged only if you use them."
    hikari "Good. And what are these add-ons?"
    "He turns the tablet so we can see a list: device insurance, a video service, and extra cloud storage."
    hamada_staff "All optional. None is needed to activate the line."

    menu:
        "No add-ons. Show us the full monthly total.":
            mc "We don't need those. Could you show us the full monthly total before we sign?"
            hikari "Exactly."
            $ reward_attributes_once("cellular_plan_total", [("insight", "micro")], show="auto")
        "Let's keep it to the student plan and nothing else.":
            mc "Let's keep it to the student plan and nothing else, please."
            hikari "The basic plan is enough for now."
            $ reward_attributes_once("cellular_plan_basic", [("grace", "micro")], show="auto")
        "No extras, thanks.":
            mc "No extras, thanks."
            hamada_staff "Understood. I'll leave every optional service unchecked."
            $ reward_attributes_once("cellular_plan_decline_extras", [("nerve", "micro")], show="auto")

    "Yamada walks us through the monthly fee, the first partial bill, and the cancellation terms."
    "Hikari reads the summary twice. I read it once, then again where she points."
    hikari "No handset, no streaming service, no insurance. Just the plan we agreed on."
    mc "I understand."
    "I sign the form on the tablet. Yamada fits a SIM card into the phone and waits for the network to register."
    hamada_staff "There. The line is active. You should see the signal now."
    $ cellular_data_active = True
    call screen cellular_connection_phone
    "At the top of the screen, the empty signal indicator fills with bars."
    hikari "Open WIRE."
    "The app opens. The contact is still there; this time, the connection is too."
    call screen wire_app
    if first_day_activity == "walk_alone":
        hikari "There. Now you can check the shop hours before walking all the way there."
        mc "And get back without making an accidental tour of the neighborhood."
    elif first_day_activity == "walk_hikari":
        hikari "There. Now you can reach me if we get separated or plans change."
        mc "That will be useful."
    else:
        hikari "There. Now you can see what Circle has been posting."
        mc "I can send them the pictures I took, once I pick the right one."
    hikari "Use the map to get us to the station. No more accidental tours."

    stop music fadeout 2.0
    scene black with Dissolve(2.0)
    "We take the train home with a working phone, a new word in my notebook, and a day that feels less like a list of firsts."
    return
