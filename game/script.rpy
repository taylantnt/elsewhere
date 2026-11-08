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

    # 5. Random narrator stinger for the menu -> game handoff.
    #
    # The two "elsewhere normal" files each hold the narrator saying ELSEWHERE!
    # once; they are one-shot lines, so the choice between the two is made at
    # random the moment the player leaves the menu. They get a channel of their
    # own rather than the voice channel: Ren'Py's voice system stops whatever is
    # on "voice" at the start of every interaction that has no voice line
    # (voice_interact in 00voice.rpy), which killed the sting the instant a
    # loaded game resumed into dialogue. The "stinger" channel rides the voice
    # mixer, so it still follows the Voice volume slider, but nothing in the
    # voice pipeline touches it. It also stays off the music channel, so the
    # main menu theme keeps playing underneath instead of being replaced.
    import random

    renpy.music.register_channel("stinger", mixer="voice", loop=False)

    menu_stingers = [
        "audio/VO/elsewhere-normal.mp3",
        "audio/VO/elsewhere-normal2.mp3",
    ]

    def play_menu_stinger(fadein=0.3):
        renpy.music.play(random.choice(menu_stingers), channel="stinger",
                         loop=False, fadein=fadein)

    # The sting is fired at the click that starts the load, not after it: the
    # channel queue is global, so the queued one-shot survives renpy.load()
    # replacing the context and plays out over the black load cinematic while
    # the save is restored. Continue's click and a Load Game slot pick both
    # reach renpy.load(), so both are covered here and in the actions below.
    class MenuLoadSting(Action):
        def __init__(self, inner):
            self.inner = inner

        def __call__(self):
            play_menu_stinger()
            self.inner()

        def get_sensitive(self):
            return self.inner.get_sensitive()

        def get_selected(self):
            get_selected = getattr(self.inner, "get_selected", None)
            return get_selected() if get_selected else False

    # phone_files uses FileAction(slot), which resolves to FileLoad on the load
    # screen and FileSave on the save screen. Wrapping here means only real
    # loads from the title screen get the sting - in-game loads and saves do
    # not.
    def MenuFileSlot(slot):
        inner = FileAction(slot)
        if isinstance(inner, FileLoad) and store.main_menu:
            return MenuLoadSting(inner)
        return inner

    # 6. Menu -> game handoff actions.
    #
    # The built-in Start and Continue actions jump straight out of the menu
    # context, which reads as a hard cut at the menu, and the load flow hands off
    # without a beat of its own. These wrap the built-ins so the departure plays
    # the random narrator stinger at the click and the arrival fades through
    # the handoff rather than cutting.
    # The main menu theme itself is left alone: `main_menu_music` keeps playing
    # on the title screen, keeps playing under the stinger, and the story scenes
    # take over from there.
    #
    # Note: Start(), Continue() and ShowMenu() only build Action objects - they
    # do nothing until called, so each wrapper has to invoke the inner action.
    class MenuStart(Action):
        def __call__(self):
            play_menu_stinger()
            Start()()

        def get_sensitive(self):
            return True

    class MenuContinue(Action):
        def __call__(self):
            play_menu_stinger()
            Continue()()

        def get_sensitive(self):
            return Continue().get_sensitive()

    class MenuLoad(Action):
        def __call__(self):
            ShowMenu("load")()

        def get_sensitive(self):
            return True

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

# The menu -> game handoff: fade out of the menu, hold at black for a beat, and
# fade into the game. The built-in menu actions jump out of the menu context
# without a transition in hand, which reads as a hard cut at the menu; this is the
# one fade that belongs to leaving the menu and arriving in the story.
define menu_handoff_fade = Fade(1.4, 0.6, 1.4)

# airport.png is only 626x417, so it is scaled up and centre-cropped to fill the
# 1280x720 screen rather than stretched out of shape. It has real art, so it gets
# no placeholder label.
image bg_airplane = Transform("images/backgrounds/bg_airplane.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_airport = Transform("images/backgrounds/bg_airport.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_station = Transform("images/backgrounds/bg_station.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_platform = Transform("images/backgrounds/bg_platform.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_akihabara_hamada_outside = Transform("images/backgrounds/bg_akihabara_hamada_outside.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_akihabara_hamada_inside = Transform("images/backgrounds/bg_akihabara_hamada_inside.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_akihabara = Transform("images/backgrounds/bg_akihabara.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_maidcafe = Transform("images/backgrounds/bg_maidcafe.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_maidcafe_omurice = Transform("images/backgrounds/bg_omurice.png", xysize=(config.screen_width, config.screen_height), fit="cover")
# The house and his bedroom each come in two lights: the night he arrives in, and
# the morning he wakes up to. They are the same rooms either way, so they are named
# by time of day rather than by room. Pick whichever matches the hour of the scene.
image bg_home_night = Transform("images/backgrounds/bg_home_inside_night.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_nightfood = Transform("images/backgrounds/bg_nightfood.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_home_day = Transform("images/backgrounds/bg_home_inside_day.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_room_night = Transform("images/backgrounds/bg_room_night.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_room_day = Transform("images/backgrounds/bg_room_day.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_train_interior = Transform("images/backgrounds/bg_train_interior.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_home_exterior_night = Transform("images/backgrounds/bg_home_exterior_night.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_home_exterior_day = Transform("images/backgrounds/bg_home_exterior_day.png", xysize=(config.screen_width, config.screen_height), fit="cover")

# The kitchen on the first morning, which is where Act 2 begins. Real art, so
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
image bg_library = Transform("images/backgrounds/bg_library.png", xysize=(config.screen_width, config.screen_height), fit="cover")

# The two rooms the first free afternoon can end in. The ramen shop has art now
# (it lives at images/backgrounds/bg_ramen_shop.png, which is why the scene name
# and the file name differ slightly). The club room is still being drawn, so it
# keeps printing its own name until bg_photo_club.png arrives.
image bg_ramen_shop = bg_or_placeholder("bg_ramen_shop", "#2b2118", "RAMEN SHOP\nLATE")
image bg_ramen = bg_or_placeholder("bg_ramen", "#2b2118", "RAMEN\nLATE")
# The same counter a few minutes later, with the bowl finished. Every route through
# the shop ends on this shot, right before he pays.
image bg_ramen_empty = bg_or_placeholder("bg_ramen_empty", "#2b2118", "EMPTY BOWL\nLATE")
image bg_photo_club = bg_or_placeholder("bg_photo_club", "#2f3230", "PHOTOGRAPHY CLUB\nCIRCLE / CLUB ROOM")

# The river path Hikari runs. Real art, so no placeholder label.
image bg_river = bg_or_placeholder("bg_river_dusk", "#1a2230", "RIVER PATH\nEVENING")
image bg_river_night = Transform("images/backgrounds/bg_river_night.png", xysize=(config.screen_width, config.screen_height), fit="cover")

# The narrow street he ends up in when he takes the wrong turn out of the school
# gate, and walks deeper into the evening until he finds the ramen shop doorway.
# The art is already low and warm, so nothing darkens it; the dialogue is what
# moves the light down.
image bg_alley = bg_or_placeholder("bg_alley", "#2a2320", "SIDE STREET\nDUSK")
image bg_lupins_den = Transform("images/backgrounds/bg_bar.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_nakanostation_night = Transform("images/backgrounds/bg_nakanostation_night.png", xysize=(config.screen_width, config.screen_height), fit="cover")


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

# Relationship values are trust, not a score. Hikari's rises when he actually
# sees her instead of only accepting her help; Tetsuo's rises when he keeps a
# promise, takes responsibility, or lets the family know where he is. The same
# ladder is available to every confidant. The current build reads the sister
# and father levels for extra beats; the confidant values are written on their
# first visits and wait for their own later scenes.
#
#   1  Known     at 1   — they have let him closer than a stranger
#   2  Trusted   at 3   — they expect him to mean what he says
#   3  Close     at 5   — they bring him the thing they would not say aloud
#   4  Family    at 8   — the door is open without asking
#
# Levels are read through affection_level(character), so a scene can gate a
# confidence or an extra beat without inventing a second stat.
init python:
    affection_level_thresholds = [0, 1, 3, 5, 8]
    affection_level_names = ["New", "Known", "Trusted", "Close", "Family"]

    def affection_value(character):
        return getattr(store, character + "_affection", 0)

    def affection_level(character):
        value = affection_value(character)
        level = 0
        for index, threshold in enumerate(affection_level_thresholds):
            if value >= threshold:
                level = index + 1
        return level

    def affection_at_least(character, level):
        return affection_level(character) >= level

    def add_affection(character, amount=1):
        """Change a relationship by a deliberate amount.

        This is not an attribute reward and does not pop a card. A relationship
        is read by later scenes, not spent like currency.
        """
        attribute = character + "_affection"
        if not hasattr(store, attribute):
            raise Exception("Unknown affection id: %r" % (character,))
        setattr(store, attribute, max(0, getattr(store, attribute) + amount))

# True if he told the family he was still full from ramen and skipped dinner.
# Only possible on the walk-alone route; the next morning's breakfast reads it.
default declined_dinner = False

# Airport state
default talked_to_security = False
default talked_to_man1 = False
default talked_to_npc2 = False
default has_pamphlet = False
default assistant_returned = False
default desk_checks = 0

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

# The professor plants the first quiz, and Hikari turns it into a place to go.
# The Saturday library scene reads `library_errand_available` and clears it
# once he has the haiku study sheets.
default quiz_announced = False
default library_errand_available = False

# The practice quiz and the real haiku quiz each keep their score and their
# per-question results. The score drives the scene's closing narration; the
# individual flags keep later dialogue from claiming he got a question right
# when he did not.
default sunday_quiz_score = 0
default sunday_q1_correct = False
default sunday_q2_correct = False
default sunday_q3_correct = False
default monday_quiz_score = 0
default monday_q1_correct = False
default monday_q2_correct = False
default monday_q3_correct = False


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
    "father": "Tetsuo",
    "chef": "Chef",
    "sim": "Sim",
    "aya": "Aya",
    "hana": "Hana",
    "orson": "Orson",
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
                renpy.call_screen("hint_card", eyebrow="Inventory", body=store.hint_text_bag)
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
        "Rank 1",
        "Rank 2",
        "Rank 3",
        "Rank 4",
        "Rank 5",
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
            dots.append(Solid("#05080db8", xysize=(dot_size + gui.scale(2), dot_size + gui.scale(2)), xpos=x - gui.scale(1), ypos=y - gui.scale(1)))
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
            # A rank change is the rare, bigger moment, so it gets its own cue;
            # an ordinary card keeps the swell.
            if rank_up:
                play_sfx("audio/SFX/attribute_rankup.wav")
            else:
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
define orson = Character("Orson", color="#a9a9a9", callback=type_sound, image="orson")
define chef = Character("Chef", color="#deb887", callback=type_sound, image="chef")
define sim = Character("Sim", color="#add8e6", callback=type_sound, image="sim")
define aya = Character("Aya", color="#dda0dd", callback=type_sound, image="aya")
define maid = Character("Maid", color="#dca0dd", callback=type_sound, image="Maid")
define hana = Character("Hana", color="#98fb98", callback=type_sound, image="hana")

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

# The wolf behind Lupin's Den bar. He is "the Master" to everyone which includes
# the player — his name is something the story has not earned yet, so the name
# box stays a title until a later visit says otherwise.
define bar_master = Character("The Master", color="#a9a9a9", callback=type_sound, image="orson")

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
define yamada = Character("Yamada", color="#b6d2e8", callback=type_sound, image="yamada")

# The regular who explains how the reading room works. A name in the box, no
# portrait: she is furniture with a voice, and the scene is about Hana anyway.
define quiet_student = Character("Student", color="#9aa48f", callback=type_sound)

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
image side yamada = At(Transform("images/characters/hamadadenki.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side aya = At(Transform("images/characters/aya.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side Maid = At(Transform("images/characters/maid.png", xysize=(256, 384), fit="contain"), portrait_idle)

# The two people whose stories the first free afternoon can open: the ramen chef
# near home, and Sim, who runs the photography club, Circle. Both portraits are already
# on disk, so unlike the three below they need no placeholder.
image side chef = At(Transform("images/characters/chef.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side sim = At(Transform("images/characters/sim.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side hana = At(Transform("images/characters/hana.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side orson = At(Transform("images/characters/orson.png", xysize=(256, 384), fit="contain"), portrait_idle)

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
        "sister", "taxi_driver", "professor", "yamada", "chef", "sim",
        "hana", "orson", "clerk", "timid_man", "cheerful_woman",
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
define hint_text_money = "You can check your cash in Inventory app using the Phone.\n\nTravel, meals and purchases cost money. Check your balance before you spend."

define hint_text_bag = "You can check your items using inventory app on your phone.\n\nSelect an item to read its description. If it can be used, its action appears below the description."

# The first point he ever earns. It names the three pillars and says where they
# come from, and deliberately says nothing about where they lead: the locked
# answer and the person who remembers are better met as surprises than explained
# here. Everything past this sentence is left for the player to find.
define hint_text_attribute = "Insight: observation and reasoning. Grace: thoughtful communication. Nerve: acting despite uncertainty.\n\nSome replies raise an attribute; some trade-offs lower one. Signed changes appear below their circle. Rank-ups open a separate screen. Open Attributes app on your phone to check progress. Not every reply changes your attributes."

# The first afternoon he is allowed to spend. It names the thing he has just been
# handed and says what it is for, without listing where he can go: the places are
# meant to be found, and the ones that matter will announce themselves with a
# mark of their own. Called from the after-school fork, once, after the game has
# already taken him somewhere.
define hint_text_after_school = "Choose one activity each free afternoon: spend time with someone, visit a place, or head home. That choice leads into the rest of the day.\n\nSome activities develop attributes or relationships. Other activities wait for another opportunity; you cannot visit more than one location in one afternoon."

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

            text "[orb_rank]" style "attribute_gain_orb_number":
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
                text "RANK [orb_rank] / 5" style "attribute_gain_rank" xalign 0.5
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
                text "RANK [active_rank] / 5" style "attribute_gain_rank" xalign 1.0
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
                        bold True
                        color "#c5cdd4"
                        outlines [(gui.scale(1), "#05080de8", 0, gui.scale(1))]

# --- START LABEL ---
label start:
    scene black with menu_handoff_fade

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
    scene bg_airplane with Fade(2.0, 1.0, 0.0)
    #DISABLED FOR NOW# play music "audio/Music/dream sequence 1 (short loop).wav" fadein 2.0#
    play music "audio/SFX/airplane.mp3" fadein 2.0
    
    "That flight felt endless."
    "I barely slept."
    "Still, I made it. Tokyo."
    "I'm here on my university's exchange program."
    
    
    "The seat in front of me is still reclined into my lap. A baby three rows back has been crying since we crossed the coast."
    "New university. Host family. A year in Japan."
    "I remember the application. The wait. The acceptance email on a Tuesday morning."
    "I was thrilled when it came through. My friends said I was brave."
    "I remember packing a bag. I don't remember the day I decided to leave home."
    "The last ordinary day before the flight is a room I can describe without being in it."
    "I can't remember what made me choose Japan."
    "A professor, a brochure, something I turned into a plan. I can feel the shape of the reason, but the reason itself won't come."
    "Everything before the airport feels like it happened to someone I used to know. Maybe that's what leaving home does."
    "Maybe it's the flight. Or the nerves. Maybe this is what arriving somewhere alone feels like."

    
    # The wallet, established before he has spent a single yen of it.
    "I have thirty thousand yen, in cash, folded into the back of my wallet."
    "It has to cover the first few days, and it won't go far when it has to cover everything."
    "I'll need to find a part-time job. I can't expect other people to handle it for me."
    
    # Foreshadowing glitch - the first crack in the simulation
    # show hospital_flash onlayer overlay at truecenter: (disabled)
    #    alpha 0.0
    #    linear 0.08 alpha 0.6
     #   linear 0.08 alpha 0.0#
    
    "..." with gate_shake
    "ugh..."
    "my head.."
    
    "I should focus on what's ahead."
    "A door, and a family I have only ever seen in photographs."
    
    stop music fadeout 3.0
    jump airport_arrival

label airport_arrival:
    # The calendar starts here: arrival is Day 1, Wednesday, April 8.
    $ set_story_day(1)

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
        "Check the Information Desk":
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
        "Apologise and step back.":
            $ remember_choice("security", "bow")
            jump answer_security_bow
        "Show him the address one more time.":
            $ remember_choice("security", "press")
            jump answer_security_press
        "Let it go. Watch how everyone else moves.":
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
        "Back off. He's busy.":
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
    mc "Ah, sorry. Sorry."
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
        $ desk_checks += 1
        "The information desk is empty."
        "A laminated sign sits where the assistant should be: 「ただいま席を外しております」. Under it, someone has written BACK SOON in careful English."
        if desk_checks == 1:
            mc "(So she stepped away. That explains the empty desk, at least.)"
            mc "(If I wait here, I'll be waiting on a sign. I should ask the people out here first.)"
        else:
            mc "(Still empty. I've been circling the same hall.)"
            mc "(The guard, the man by the phones, the woman in the bright coat. One of them must know the way out.)"
        "A staff member in a grey coat crosses behind the counter without stopping."
        mc "(I'll check back once I've asked around.)"
        jump airport_exploration

    if not assistant_returned:
        $ assistant_returned = True
        "The desk is not empty now. The assistant is behind it, straightening a stack of pamphlets that was already straight."
        mc "(There she is.)"

    assistant "いらっしゃいませ～。ようこそ。"
    mc "Hi! Um... Can you help me?"
    # The moment she realises she has to do this in English. She wears the second
    # drawing from here until the address is sorted out, one way or the other.
    $ assistant_shy = True
    assistant "えっ…えいご…すこしだけ…"
    assistant "えいごのスタッフは…いまやすみ…"
    "She murmurs under her breath, trying out the words."
    assistant "English staff... on break."
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
            $ remember_choice("assistant", "nevermind")
            jump answer_assistant_nevermind

label answer_assistant_patient:
    mc "It's okay. We can use the map. I'm not in a hurry."
    "She holds still for a moment."
    "Then she lets out a breath."
    assistant "Map... yes. ちず。"
    "She reaches for a pamphlet."
    $ reward_attributes_once("answer_assistant_patient", [("insight", "micro")], show="auto")
    jump answer_assistant_ask

label answer_assistant_ask:
    "I hold up my phone to show her the address."
    mc "How do I get here?"
    # She cannot find the English for it and it starts to show. The second drawing
    # stays up until the pamphlet is in his hands and she has recovered.
    $ assistant_shy = True
    assistant "あー、これはね…でんしゃ？トレイン？"
    assistant "にっぽりえきから。。。えっと。。。ちょっとまってください。"
    "She unfolds a map covered in arrows and kanji."
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
        veteran "If you pick up one of the pamphlets from the desk, I might be able to help you work through it."
        mc "Pamphlet? I'll go look for one."
        jump airport_exploration

    veteran "You look a little lost. That pamphlet! Let me see... Are you trying to get to 中野3丁目?"
    mc "That's right."
    veteran "..."
    "He unfolds it and runs a finger down the margin."
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
    # Seeing the last notice means he has read the whole board.
    if board_message_index == len(board_messages) - 1:
        $ reward_attributes_once("information_seeker", [("grace", "tiny")], show="auto")
    $ board_message_index = (board_message_index + 1) % len(board_messages)
    jump airport_exploration

label look_plants:
    # The first plant is a nice plant. The tenth is a cry for help.
    $ plant_line = plant_dialogues[min(plant_index, len(plant_dialogues) - 1)]
    "[plant_line]"
    # Sticking around until the tenth plant earns a little nerve.
    if plant_index == len(plant_dialogues) - 1:
        $ reward_attributes_once("plant_determination", [("nerve", "tiny")], show="auto")
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
## ACT ONE: GETTING HOME
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

    "I climb in and pull the door shut."
    "The seats are spotless. There is lace over the headrests."
    mc "(Lace. There is lace. In a taxi.)"

    taxi_driver "お客様、どちらまで？"
    mc "(That's my cue.)"
    "I hand the pamphlet over the seat."
    taxi_driver "中野3丁目ですね。かしこまりました。遠いですが、大丈夫でしょうか？"
    mc "(...I understood one word of that and it was 中野.)"
    mc "Ah, um... 中野3丁目... please?"
    "The driver chuckles."
    taxi_driver "Okay, okay. 中野3丁目. No problem."
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
    "The meter reads 1,300."
    mc "(Thirteen hundred. We have been in this car for four minutes.)"

    "The driver says something and points out of my window. I nod and smile."
    mc "(I didn't understand a word. Maybe I can get by with a nod until my Japanese improves.)"

    "The meter clicks. I look again."
    mc "(Three thousand eight hundred.)"
    mc "(Another hundred. Then another.)"
    mc "(And it climbs while we sit at a red light. It goes up while we do absolutely nothing.)"
    mc "(Eighteen thousand. That guess was made before I understood anything about anything.)"

    "Half an hour later the roads get narrow and the lights get fewer."
    "He slows, checks a street sign, turns, and the city goes quiet behind us."
    "The meter reads 9,200."
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

    "The meter ticks past 13,400. We are still not there."
    mc "(...)"

    mc "(My eyes feel so heavy.)"
    "I lean my head against the window."
    "I close my eyes, just for a minute."

    window hide
    scene black with Dissolve(1.5)
    pause 1.5
    scene bg_taxi_interior_final with Dissolve(1.5)

    "I wake up to the indicator ticking, and the car not moving."
    taxi_driver "着きましたよ。中野3丁目。"
    mc "(...中野. That was 中野. I'm awake.)"

    "The meter is still glowing. I finally let myself look at the number."
    "The meter reads 17,600."
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
    "I squint at the pamphlet. The characters swim a little."
    mc "(...800. I think that's 800. It's next to 中野, so it has to be the fare.)"
    mc "(Unless it's the platform number. Or the exit number. Or something I haven't thought of yet.)"
    hide pamphlet with dissolve


label ticket_machine:
    menu:
        "Try the 320 yen button, it's cheap enough to test.":
            if has_item("ticket_320"):
                mc "(I already purchased this ticket. It's the wrong one.)"
                jump ticket_machine
            $ buy_item(320, "ticket_320")
            "A ticket drops into the tray with a soft clack."
            mc "(That was satisfying. That was also very cheap.)"
            mc "(And it doesn't go to 中野.)"
            mc "(Put it down. Try again.)"
            jump ticket_machine

        "Try the 800 yen button. That was the number on the pamphlet.":
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

        "Ask the attendant.":
            $ reward_attributes_once("answer_ticket_ask", [("grace", "micro")], show="auto")
            "I catch the eye of a woman in a station uniform and hold the pamphlet up."
            mc "Sumimasen... 中野3丁目?"
            "She takes the pamphlet, reads it, and presses the button for me without a word."
            $ spend_money(1300)
            "¥1,300 Yen... A ticket slides out."
            mc "(That took her four seconds. It took me four minutes.)"
            mc "Arigatou gozaimasu."
            "She nods, already walking away."
            jump train_platform


label train_platform:
    # The only ticket that actually works, and not one he could ever have found
    # on his own. That is the whole point of the scene.
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
        "I look out of the window as the city blurs past."
        mc "Express. Right train, right direction, right carriage. Three things I got right today."
        mc "Watashi namae... no. Watashino namae wa... there. It still works."
        mc "What if they were expecting someone better? Somebody who can actually talk."
        "The roofs go by. Then the signs. Then the little gardens squeezed between the houses."
        mc "No. I worked two years for this seat. Nobody handed it to me."
        "I yawn, my eyelids suddenly heavy."
        mc "Just for a minute."
    else:
        "I settle into the seat as the carriage fills up around me."
        mc "On the train. On my own. That was the first test, and I got through it."
        mc "This line stops everywhere, so I get to see the parts of it that are not for visitors."
        mc "Watashino namae wa... okay. That one still works too."
        mc "I don't know what the house will be like. I don't know what I will be like in it."
        mc "Everybody at home said I was mad to come alone. Some of them were right."
        "I yawn, leaning my head against the cool glass."
        mc "Just for a minute."

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
## ACT ONE: HOME
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
        "I step out onto the street."
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
    "I reach for the doorbell."
    # The chime lands at the same moment as the line describing it, so the sound
    # and the text hit together instead of a beat apart.
    $ play_sfx("audio/SFX/doorbell.mp3")
    pause 3.0
    "The chime is much louder than I expected. It bounces off the houses opposite."
    mc "(Everyone on this street heard that. I hope I didn't wake anyone in the house.)"

    if arrived_late:
        # Late arrival, which is the train. Only the mother is still up, and the
        # whole scene is quiet.
        $ play_sfx("audio/SFX/door_open.mp3")
        "The door opens a crack, then all the way, carefully."
        mother "Oh! You made it."
        mother "Thank goodness. We thought you'd got lost somewhere between the airport and here."
        mother "Come in, come in. Quickly. It's cold out, and everyone else is asleep."
        "She holds the door and waves me in with her whole arm."
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
        "She has my bag out of my hands before I manage to say anything."
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

    "We carry what I need upstairs. She steadies the box while I find the light switch."
    if arrived_late:
        mother "Goodnight. Sleep well. We'll talk properly in the morning."
    else:
        mother "Goodnight. And truly, welcome. We'll talk properly in the morning."
    "The door clicks shut, and then the house is completely silent."

    mc "Good thing I sent everything ahead. Thanks to that I only had to carry a small bag."
    if travel_method == "train":
        mc "I never would have managed the transfers with luggage."
    mc "Right. Unpacking."
    "Cardboard. Tape. Clothes that smell like my old room."

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
    $ dream_key = "first_night"
    jump dream_router


################################################################################
## ACT ONE, LAST BEAT: THE FIRST DREAM
################################################################################
##
## He falls asleep at the end of the first night and the day he just had comes
## back to him in the wrong order, with things in it that were never there.
## Underneath the dream there are two voices in a room he has never been in,
## discussing him in the third person. They are the same white light and the same
## clinical register that cut into him on the plane, so the player has already
## been taught how to read them: this is what is actually happening to him.
##
## The dream tries to sort the real memories of today from the planted ones, and
## fails. The ordering board that used to sit here is archived in
## dream_archive.rpy; the story now lets the dream talk over him instead. It is
## not possible to fail the scene. It is very possible to be told things he
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

# The interference itself. Drawn on the overlay layer so it crosses the dialogue
# as well as the picture: the voice he is hearing is not coming from the room he
# thinks he is standing in.
screen dream_static():
    layer "overlay"

    default bars = dream_static_bars()
    timer 0.05 repeat True action SetScreenVariable("bars", dream_static_bars())

    for b in bars:
        add b


label dream_first_night:

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

    # The first slip. A single frame of white, and a line that sounds less like
    # the dream than like the game failing to load it.
    show hospital_flash onlayer overlay at truecenter:
        alpha 0.0
        linear 0.1 alpha 0.45
        linear 0.1 alpha 0.0
    $ renpy.say(None, "scene reload failed.", interact=False)
    pause 0.35

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

    "The street does not let me leave. The bell is still ringing after the door has already closed."
    "The light behind the curtains goes out before I reach it. The bicycles are still against the wall."
    "It is only a dream, I tell myself. Dreams do not keep order anyway."

    scene black with Dissolve(0.6)
    "And then the pieces of today come loose and scatter."
    mc "No. Wait."
    mc "I know what today was. I was there for all of it."
    "Everything I did today is lying on the floor of my head, mixed up with things I have never seen."
    "I try to put the airport first. It becomes the house. I try to put the house first. It becomes the road."
    "The harder I hold on, the faster they move."
    "Four of them are mine. I know that much: the airport, the ride, the street, the bell."
    "The others are not. A woman in white, calling a name that is almost mine. A corridor of doors, and behind every one of them my room."
    "I do not know why it matters that I keep them apart. It matters."

    "The pieces slow down. Not because I have fixed them. Because the dream is done hiding them."
    "The woman in white turns toward me. I cannot see her face."

    "The dream does not answer me. It simply stops repeating the day."
    "The bell stops. The woman in white is already gone."

    stop music fadeout 3.0
    scene black with Dissolve(1.5)
    pause 1.5

    jump morning_call

################################################################################
## ACT TWO, FIRST BEAT: THE FIRST MORNING
################################################################################
##
## Act 2 begins here: the arrival is over, and from this morning onward the
## days belong to him. `current_act` moves to 2 so the confidant caps in
## locations.rpy start to apply.
label morning_call:
    $ current_act = 2
    # Day 2: Thursday, April 9. The first school day.
    $ set_story_day(2)

    # Waking up. The dream lets go of him slowly, the way a hand does once it has
    # decided you can stand on your own.
    #
    # The room in the morning. room_ambient plays room_day.mp3 here by default;
    # this scene is where that track lives, so nothing is overridden.
    scene bg_room_day with Dissolve(2.0)
    $ room_ambient(False)
    "Three seconds before I remember where I am."
    "The airport. A road with no end on it. Two voices talking over me like I wasn't in the room."
    mc "(What was that?)"
    mc "(It felt like the dream knew me. That's what I can't shake.)"
    "I try to hold onto it and it comes apart like wet paper."
    "Then the room assembles itself around me. Low ceiling. Boxes. A window with the wrong light."
    "Japan. The house. The room with the boxes in it."
    mc "My first morning."


    # And then the house starts moving. This is the first Japanese household he
    # has ever heard wake up.
    "Then the whole house wakes up around me at once."
    "Pans, somewhere below. A radio turned down low. Wood moving."
    "Feet on the stairs, two steps at a time, and then three quick knocks on my door."
    "It slides open before I can answer it."
    hikari "Morning. You're awake. I'd already knocked once."
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
        "I never said this properly. The emails you made this less frightening.":
            $ reward_attributes_once("answer_breakfast_emails", [("grace", "small")], show="auto")
            mc "I never said this properly. The emails you made this less frightening."
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
## ACT TWO, SECOND BEAT: LEAVING THE HOUSE
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

    hikari "Your phone."
    mc "What about it?"
    hikari "I put WIRE on it before you landed. You'll need it this week."
    mc "When did you"
    hikari "Before you landed. It's what sisters do."
    "I open it before I can ask the follow-up. Her name is the only contact on the list."
    $ wire_unlock("hikari")

    jump school_morning


################################################################################
## ACT TWO, THIRD BEAT: WALKING TO SCHOOL
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
## ACT TWO, FOURTH BEAT: INSIDE THE GATE
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
## ACT TWO, FIFTH BEAT: THEIR DEPARTMENT
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
## ACT TWO, SIXTH BEAT: STUDENT RELATIONS
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
## ACT TWO, SEVENTH BEAT: THE FIRST LECTURE
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
        "[tag_nerve] Can we discuss today's late mark?" if has_attribute_points("nerve", attribute_reward_value("nudge")):
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
    hikari "Because you stayed and spoke to him. Most people just leave."
    hikari "He spends the rest of the week looking for them."
    mc "(She is cheerful about this as well. I am starting to think cheerful is just how she carries things.)"
    hikari "Honestly, that was practically a welcome."
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
        "I'd rather just move on. Let's eat.":
            mc "I'd rather just move on. Let's eat."
            hikari "That is a very good plan."
            $ remember("hikari", "chose to move on after the lecture")
    hikari "Come on. I'm hungry, and I know a bad cafeteria and a worse one."
    mc "You said there were two."
    hikari "There are two."
    mc "..."
    hikari "Or don't. It's your first free afternoon. Nobody here is going to tell you what to do with it."
    hikari "And I am not going to be the first."
    mc "(She has been handing me this day since the platform. Now she is handing it back.)"

    # Said once, before he picks, so the explanation of the free afternoon
    # arrives while the choice is still his to make.
    if not store.after_school_hint_shown:
        $ store.after_school_hint_shown = True
        $ renpy.call_screen("hint_card", eyebrow="Free Afternoons", body=store.hint_text_after_school)

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

    if first_day_activity == "walk_alone":
        jump after_school_walk_alone
    elif first_day_activity == "walk_hikari":
        jump after_school_run
    else:
        jump after_school_photo_club


################################################################################
## ACT TWO, EIGHTH BEAT: THE FIRST FREE AFTERNOON
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
    mc "(No signal. Right. That's a problem for tomorrow.)"
    "I put it back."
    "So I keep going, in the direction that feels like the direction, which is a method I have now disproved in practice."

    scene bg_alley with walk_fade

    "The sun goes down off the roofs while I walk. First the whole street is gold, then only the top floors are, then nothing is."
    "The streets get quieter. Not empty, nothing here is ever empty, but quieter, and the shops stop looking like they are for passers-by."
    "And then the lights on the poles come on, all of them at once, in a line, starting at the far end and coming towards me."
    mc "(It is getting dark. Eleven minutes. It was supposed to take eleven minutes.)"

    "And then I smell it."

    # The chef's first visit. The dialogue follows the beat sheet in
    # documentation/Locations/Ramen Shop - Chef/1st interaction.md: he points at a line
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

    voice "audio/VO/ramen_welcome.mp3"
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
    
    voice "audio/VO/ramen_ok.mp3"
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
            chef "どうぞ。"
            mc "(That one I know. It means here you go. It also means eat it.)"
        "Try it before asking.":
            "I pick up the spoon before I can think about it, which he appears to consider the entire conversation."
            chef "どうぞ。"
            mc "(That one I know. It means here you go. It also means eat it.)"

    "I eat it."
    "The first mouthful hits like something walking into a door. Rich and smoky and far too much. The second is better than the first."
    mc "...This is actually amazing."
    "I say it half under my breath, in English, to nobody."
    "He hears the tone of it even if he does not have the words. He does not turn around."
    chef "うまい、だろ？"
    "One word, said to the pot, in a voice that has clearly said it ten thousand times."
    mc "(No idea what that was. But the way he said it, it sounded like a verdict on the bowl.)"
    menu:
        "Ask what it means.":
            mc "Sumimasen. What does that mean?"
            chef "「うまい。」"
            "He says it again, slower this time, and points at the bowl with the ladle."
            mc "Umai?"
            chef "「うん。うまい。」"
            "He grunts yes and turns back to the pots. That is the lesson."
            # The first word of the language, taught mid-bite by the man who
            # never speaks it. No packet, no sign — he learns it here.
            $ reward_attributes_once("chef_first_umai", [("grace", "small")], show="auto")
        "Thank him properly.":
            mc "Arigatou gozaimasu."
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

    # The meal continues in the shop. No more choices, just the eating, and the
    # room around it. Every route comes back through the same empty bowl, the
    # same bill, and the same walk home.
    scene black with walk_fade
    "Two men come in while I eat. They sit at the other end of the counter without speaking, and the chef puts two bowls down without looking at either of them."
    "I watch how they hold their chopsticks and try the same grip. It is not the grip I know."
    "Chopsticks in one hand, spoon in the other, head down over the bowl. They eat the way this country eats, and I copy it badly, and neither of them looks up."
    "I finish the whole bowl. Soup and all. There is nothing left in it but the pattern on the bottom, and I am surprised by how much I want there to be."

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
    # The shop's only broadcast, sent while the phone still has no data. It
    # waits in the queue until the line goes live the next day.
    $ queue_message("chef", "New bowl. 900 yen. Closed Wednesday.", day="yesterday")
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
    mc "(She looks like somebody else. I have enough sense not to say it.)"
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
            "For a long moment, neither of us says anything. The river moves in the dark, steady and cold."
            hikari "It's the only hour of the day that's mine."
        "Do you do this every day?":
            mc "Every day?"
            hikari "Most. The days I don't, I'm in the house, and I don't like who I am in the house on those days."
            mc "(That is the first thing today that she did not put a smile on top of.)"
            mc "You come out here instead of going home."
            hikari "I come out here. It's the only hour of the day that's mine."
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
    scene bg_river_night with walk_fade


    $ first_run_started = True
    $ hikari_visits = 1
    # Small, not medium: the three first-afternoon routes should close at a
    # similar weight. Walk and photo use the same size on their forced beat.
    $ reward_attributes_once("run_first_river", [("nerve", "small")], show="card")
    $ add_affection("sister", 1)
    $ remember("hikari", "ran the river path with her on the first afternoon")

    # WIRE is already hers from the morning; the run is where she uses it for the
    # thing she will not say in the kitchen. She does it the way she does
    # everything: quickly, while looking at something else.
    hikari "Give me your phone."
    mc "Why."
    hikari "Because I'm not explaining it twice."
    "She takes it out of my hand, which is turning into how the two of us do things."
    hikari "You still haven't opened WIRE."
    mc "I know. I never opened it."
    hikari "Open it."
    "I open it. It is a list with one name on it, and the name is hers."
    hikari "That's the point of it."
    mc "(That is not it.)"
    "She does not look at me while she says the next part, which is how I know it matters."
    hikari "There's a message in there for when you get signal. Read it when you have one. Not here."
    # The thing she would not say in the kitchen. It is queued before his phone
    # has data, so it reaches him at Hamada Denki with everything else.
    $ queue_message("hikari", "Thanks for coming out with me. You kept up better than you think. Don't tell anyone I said that.", day="yesterday")

    "We walk back. Twenty minutes this time, because neither of us is in a hurry."
    "She talks less on the way back. Not nothing, less."
    "And the less she says, the more it sounds like something she does not do in front of people."

    scene bg_home_exterior_night with walk_fade
    $ night_street()

    "The house is dark except for the kitchen, and the kitchen is the wrong window to be lit at this hour."
    mc "(It is properly dark. I do not know how long we were out there.)"
    hikari "Ah."
    mc "Ah?"
    hikari "Kitchen light. That's them being awake."
    hikari "Meet you at the kitchen, I want to change these sweaty clothes first."

    scene bg_home_night with walk_fade
    $ hikari_run = False
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


label after_school_photo_club:

    # Sim's rules (full version in game_structure.md §4.6 and his character
    # file): never complains, never blames anyone, puts others first; what he
    # says about himself is always smaller than the truth. He is not a student —
    # he comes in from outside to guide the club, which is called Circle.
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
    play music "audio/Music/circle.mp3" fadein 2.0
    $ phone_map_visit("photo_club")

    "Someone has taken every chair in this room and put it in a rough circle. There are six people in it. None of them looks up."
    "One wall is covered in prints held on with the same tape."
    "Half of them have been written on in marker by somebody who was angry at the time."
    "Two of them are going at each other over a print, fast and cheerful, and nobody else is troubled by it."
    "It is just the sound this room makes."
    "Then one of them notices me, and the argument stops mid-sentence, and the whole room turns round at once, which is worse."
    sim "Ah! you must be the new one. Welcome, welcome. Come in, don't be shy. The doorway is the worst seat in the room."
    "He looks a little older than everyone else here."
    sim "Everyone! Everyone! this is our first-timer."
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
    mc "(Two rooms in one day, and both of them told me who they were for before they told me anything else.)"

    sim "So. Do you have a camera?"

    mc "Not with me. Only my phone."
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
    sim "Oh, wait. One thing before you go."
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
    # Circle's welcome message. Like the chef's advert, it is queued until the
    # phone has a data plan; Hikari is still standing there when it lands.
    $ queue_message("sim", "Welcome to Circle! I posted the two photographs you took today. The window one already has replies. Next meeting is Thursday. Bring the camera if you have it.", day="yesterday")
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
    "She has made a seat out of it. She does not look uncomfortable in it at all."
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
## ACT TWO, NINTH BEAT: THE END OF THE FIRST DAY
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
                    # Portraits crop toward the top of the frame so the card
                    # shows a face and shoulders instead of a torso slice.
                    "focus": 0.15 if art.startswith("images/characters/") else 0.5,
                })

        return cards


# A memory card is a photo card: the art cover-fills the whole face and a dark
# scrim carries the caption. fit "cover" alone only scales the image up — it
# never clips the overflow, which is what let portraits spill over the card
# edges. The viewport below is the only container that actually clips, so the
# cover-scaled image lives in an oversized fixed centered inside it, and the
# scroll position pins the window to the middle of that frame.
#
# The face itself is added inline here with an `at memory_card_face_in` so the
# flip-in animation can run on show; the per-card focus crops the portrait.
screen memory_card_art(art, focus):
    viewport:
        xysize (198, 118)
        xpos 1
        ypos 1
        xinitial 0.5
        yinitial 0.5
        mousewheel False
        draggable False
        pagekeys False
        scrollbars None
        fixed:
            xysize (262, 182)
            add art:
                xysize (206, 126)
                fit "cover"
                xalign 0.5
                yalign focus

transform memory_card_hover:
    anchor (0.5, 0.5)
    on hover:
        easeout 0.10 zoom 1.045
    on idle:
        easeout 0.10 zoom 1.0


transform memory_card_face_in:
    on show:
        alpha 0.0
        zoom 0.88
        easeout 0.28 alpha 1.0 zoom 1.0


transform memory_card_back_in:
    on show:
        alpha 0.0
        easeout 0.30 alpha 1.0

screen day_memory_match(cards, matched, misses, reveal_pair=None, preview=False):
    modal True
    zorder 100
    default first_selection = None
    default previewing = preview

    $ pairs_found = len(matched) // 2

    add Solid("#05080d")
    add Solid("#1a2634") xpos 198 ypos 104 xysize (884, 580)
    add Solid("#0a131d") xpos 199 ypos 105 xysize (882, 578)

    vbox:
        xalign 0.5
        ypos 28
        spacing 6

        text "FIRST NIGHT / MEMORY":
            xalign 0.5
            size 11
            kerning 4
            color "#7d93a6"
            outlines []

        text "KEEP THE DAY TOGETHER":
            xalign 0.5
            size 30
            bold True
            kerning 2
            color "#d7e8f0"
            outlines []

        text ("Memorize the board. It turns over in six seconds." if previewing
              else "Find all eight pairs. Three mismatches and the day fades."):
            xalign 0.5
            size 13
            color "#8fa2b1"
            outlines []

    hbox:
        xalign 0.5
        ypos 122
        spacing 26

        hbox:
            spacing 6
            text "MEMORIES":
                size 10
                kerning 2
                color "#7d93a6"
                outlines []
                yalign 0.5
            for n in range(8):
                add Transform(Solid("#69c9b4" if n < pairs_found else "#223140"), xysize=(8, 8), rotate=45)
            text "[pairs_found] / 8":
                size 11
                color "#c6d0d7"
                outlines []
                yalign 0.5

        hbox:
            spacing 6
            text "MISMATCHES":
                size 10
                kerning 2
                color "#7d93a6"
                outlines []
                yalign 0.5
            for mark in range(3):
                add Transform(Solid("#d97b7b" if mark < misses else "#223140"), xysize=(8, 8), rotate=45)

    grid 4 4:
        xalign 0.5
        ypos 152
        spacing 10

        for i in range(len(cards)):
            $ face_up = previewing or i in matched or i == first_selection or (reveal_pair and i in reveal_pair)
            $ highlighted = (not previewing) and (i == first_selection or (reveal_pair and i in reveal_pair))
            $ accent = cards[i]["accent"]

            button:
                xysize (200, 120)
                background Solid("#0d1620")
                hover_background Solid("#14202d")
                insensitive_background Solid("#0b121a")
                sensitive (not previewing and not reveal_pair and i not in matched and i != first_selection)
                at memory_card_hover

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
                    xysize (200, 120)

                    if highlighted:
                        add Solid(accent + "30") xpos -3 ypos -3 xysize (206, 126)

                    add Solid("#0e1722") at memory_card_back_in

                    # One-pixel frame, drawn over the face plate.
                    add Solid("#2a3a48") xysize (200, 1)
                    add Solid("#2a3a48") xysize (200, 1) ypos 119
                    add Solid("#2a3a48") xysize (1, 120)
                    add Solid("#2a3a48") xysize (1, 120) xpos 199

                    if face_up:
                        fixed:
                            xysize (262, 182)
                            add cards[i]["art"]:
                                xysize (206, 126)
                                fit "cover"
                                xalign 0.5
                                yalign cards[i].get("focus", 0.5)
                            at memory_card_face_in

                        if i in matched:
                            add Solid("#04080ecc") xpos 1 ypos 1 xysize (198, 118)

                        add Solid("#050a12b8") xpos 1 ypos 80 xysize (198, 39)
                        add Solid("#050a1240") xpos 1 ypos 72 xysize (198, 8)

                        add Solid(accent + "d9") xpos 1 ypos 1 xysize (3, 118)

                        if i in matched:
                            fixed:
                                xpos 118
                                ypos 5
                                xysize (76, 18)
                                add Solid("#0e2f24e0")
                                text "REMEMBERED":
                                    xalign 0.5
                                    yalign 0.5
                                    size 8
                                    kerning 1
                                    color "#a9ecd0"
                                    outlines []

                        text cards[i]["title"]:
                            xpos 12
                            ypos 84
                            xmaximum 178
                            ymaximum 34
                            size 13
                            color "#eef4f7"
                            outlines [(1, "#050a12", 0, 0)]
                    else:
                        add Solid("#0d1620") xpos 1 ypos 1 xysize (198, 118)

                        add Solid(accent + "55") xpos 1 ypos 1 xysize (3, 118)

                        fixed:
                            xalign 0.5
                            yalign 0.42
                            xysize (200, 60)
                            vbox:
                                xalign 0.5
                                spacing 7
                                add Transform(Solid(accent + "aa"), xysize=(10, 10), rotate=45)
                                text "ELSEWHERE":
                                    xalign 0.5
                                    size 14
                                    kerning 3
                                    color "#b9d1d8"
                                    outlines []
                                text "DAY 01  /  MEMORY":
                                    xalign 0.5
                                    size 8
                                    kerning 2
                                    color "#5d7180"
                                    outlines []

    if previewing:
        timer 6.0 action SetScreenVariable("previewing", False)
    elif reveal_pair:
        timer 0.85 action Return(None)

    hbox:
        xalign 0.5
        ypos 676
        spacing 14

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

    # Only the ramen route leaves him genuinely full. Everyone else came home
    # hungry, so the choice below would not exist for them — and the morning
    # after reads `declined_dinner` to keep the two days consistent.
    if first_day_activity == "walk_alone":
        mc "(I am still full. That bowl was enormous. But Mother kept this warm, and they waited for me.)"
        menu:
            "Be honest. Tell them you're still full from the ramen.":
                mc "I... I actually just had a really big bowl of ramen. I'm still full."
                "The table goes quiet for a second. Mother looks at the fish, then at me."
                hikari "The one near the two convenience stores."
                mc "Yeah. The chef made me a bowl I didn't order, and it was... a lot."
                father "..."
                father "I'm glad you found somewhere to eat. But when this family sits down, we eat together."
                father "We couldn't talk to you about it, and that isn't your fault. But dinner time is dinner time."
                mother "There's rice in the pot. If you get hungry later."
                $ declined_dinner = True
                $ reward_attributes_once("first_dinner_declined", [("grace", "micro_loss")], show="auto")
                $ remember("father", "told him he was still full from ramen on his first night")
                $ remember("hikari", "covered for him when he skipped dinner")
                jump end_of_first_day
            "Say you're hungry, and sit down to eat with them.":
                mc "I'm starving, actually. What is natto?"
                $ reward_attributes_once("first_dinner_covered", [("grace", "small")], show="auto")
                # He chose the table over the easier exit. That is the thing
                # Tetsuo was actually asking for.
                $ add_affection("father", 2)
                $ remember("father", "ate dinner with the family even though he was still full")
                $ remember("hikari", "he covered for being too full to explain")

    menu:
        "Try the natto. Admit you're not sure about it yet.":
            "I take a small bite. The texture is stranger than the taste."
            mc "I can try it. I'm not sure I like it yet."
            father "That's fair. I didn't like it the first time either."
            hikari "You still make that face."
            father "I do not."
            mother "You do."
            # Honesty at the table, offered without making it a performance.
            $ add_affection("father", 1)
            $ reward_attributes_once("first_dinner_natto", [("nerve", "micro")], show="auto")
            $ remember("father", "was honest about trying natto")
        "How long did it take to get used to the neighborhood?":
            mc "How long did it take to get used to the neighborhood?"
            father "I grew up two stops away. Your mother moved here after we married."
            mother "And he still gets lost in the department store."
            father "That place has eight floors."
            mc "I'm starting to understand the problem."
            father "You'll learn the streets. It takes time."
            # He asked about Tetsuo's life instead of only his own.
            $ add_affection("father", 1)
            $ reward_attributes_once("first_dinner_neighborhood", [("insight", "micro")], show="auto")
            $ remember("father", "talked about learning the neighborhood")
        "I'm sorry I kept you waiting. I should have called.":
            mc "I'm sorry I kept you waiting. I should have called."
            father "You didn't have a working connection. Next time, ask someone to call."
            mc "I will."
            mother "That's all we wanted to hear."
            # Taking responsibility without being asked is worth more than a
            # polite apology after the fact.
            $ add_affection("father", 2)
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
        mc "(I ran until I could not breathe, next to somebody who was not out of breath at all.)"
        mc "(She showed me a thing she does not show anybody, and then she walked me home and got shouted at for it.)"
    else:
        mc "(I walked into a room full of strangers and nobody asked me a single question about where I come from.)"
        mc "(There are prints on that wall with marker on them. Somebody was angry about a photograph. That is the whole club.)"

    mc "(Yesterday I got off a plane without knowing one word of the language.)"
    mc "(Today I found a place, or a person, or a room I would not have found if I had stayed home.)"

    "I sit on the edge of the bed and check WIRE once more."
    if first_day_activity == "walk_alone":
        mc "(Hikari's name was already there from the morning. The chef's hours are here too.)"
    elif first_day_activity == "walk_hikari":
        mc "(It is just Hikari's name. I can see the profile, but not send anything.)"
    else:
        mc "(Hikari is there from the morning. Sim's invitation is saved too.)"

    "The contact records are on the phone. The rest of WIRE is still out of reach."
    "A knock comes at the door, and Hikari opens it before I can answer."
    show sister_standing with dissolve
    hikari "You're still up."
    if first_day_activity == "walk_alone":
        mc "Your name was already there this morning. The chef's contact is there too."
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
            $ add_affection("sister", 1)
            $ reward_attributes_once("first_night_hikari_thanks", [("grace", "micro")], show="auto")
        "Tell her she makes the house easier to understand.":
            mc "You make this house easier to understand."
            hikari "Don't tell anyone. I have a reputation."
            # He noticed what she does for the house, not only what she does
            # for him. That lands harder than being thanked.
            $ add_affection("sister", 2)
            $ reward_attributes_once("first_night_hikari_observation", [("insight", "micro")], show="auto")
        "Promise you'll be ready when she comes to get you.":
            mc "I'll be ready when you come get me."
            hikari "You'd better be. I'm not waiting outside your door."
            $ add_affection("sister", 1)
            $ reward_attributes_once("first_night_hikari_promise", [("nerve", "micro")], show="auto")
    hide sister_standing with dissolve

    "I put the phone beside my student card and turn off the lamp."
    mc "(Five minutes early. Notebook open. Pen out.)"
    "The day starts to break apart behind my eyes: the platform, the classroom, the place I chose."
    "I try to hold on to the order they came in."
    window hide
    scene black with Dissolve(2.5)
    stop music fadeout 2.0
    call first_night_memory from _call_first_night_memory
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
            $ renpy.sound.play("audio/SFX/memory_restore.wav", channel="sfx")
        else:
            $ day_memory_misses += 1
            $ renpy.sound.play("audio/SFX/memory_deviation.wav", channel="sfx")
            call screen day_memory_match(day_memory_cards, day_memory_matched, day_memory_misses, selected_pair, False)

    if len(day_memory_matched) == len(day_memory_cards):
        "The last two pictures settle into place. For a moment, the whole day makes sense in order."
        $ reward_attributes_once("first_night_memory_pairs", [("insight", "nudge")], show="auto")
    else:
        "Three wrong pairs, and the day slips out of order again."

    stop music fadeout 2.0
    return


## ACT TWO, TENTH BEAT: THE SECOND DAY
################################################################################
##
## The first full day that belongs to him: lecture, the Hamada Denki errand,
## then Akihabara free until the maid cafe. This is the shape every later day
## repeats — the difference is that from here on the afternoon is the hub's.

label second_morning:
    # Day 3: Friday, April 10. The second school day.
    $ set_story_day(3)

    # Anything queued while the phone had no signal lands here, with the buzz.
    $ flush_pending_messages()
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
        if declined_dinner:
            mc "I got lost, found a ramen shop, and told them I was too full for dinner. Dad didn't say much about it."
            father "You don't skip dinner in this house. If you're hungry, we eat together. That's the rule."
            hikari "He found a ramen place by getting completely lost. Honestly, that's kind of amazing."
            mother "There's rice in the pot if you want some before we leave."
        else:
            mc "I got lost and found a ramen shop. The chef gave me his WIRE contact."
            father "You got lost and made a contact. That is one way to do it."
    elif first_day_activity == "walk_hikari":
        mc "Hikari showed me the river path. Her WIRE profile was already waiting."
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


label first_connection_messages:
    # The Hamada Denki line is live. The queue was filled on day one, before the
    # phone could sync; this is the first moment those texts can arrive.
    if not pending_messages:
        return

    $ arrived_from = pending_messages[0]["contact"]

    "My phone buzzes once against my palm."
    $ deliver_pending_messages()

    if arrived_from == "hikari":
        hikari "That should be me."
        mc "You're standing right here."
        hikari "I know. Look at the message I sent yesterday."
        $ run_chat("hikari", [
            {"options": [
                {"label": "\"Testing. Can you see this?\"",
                 "send": "Testing. Can you see this?"},
            ], "options_delay": 0.5},
        ])
        $ msg_buzz()
        hikari "There. See? I got your message."
        mc "You could have just told me."
        hikari "And for the record, I meant what I wrote."
        mc "..."
        hikari "Don't make it a thing."

    elif arrived_from == "chef":
        hikari "That was your phone. The chef found you."
        $ run_chat("chef", [])
        hikari "An advertisement. You've been a customer for one day."
        mc "It's the most he's ever said to me."
        hikari "Then he must want you back."

    elif arrived_from == "sim":
        hikari "That was your phone. Sim already found you."
        $ run_chat("sim", [])
        hikari "He posted your photographs, didn't he."
        mc "The window one has replies."
        hikari "Of course it does. He probably replied first."

    return


label second_school_day:
    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The route feels less like a test today. I recognize the corner shop and the station entrance."
    hikari "Tell me which platform we should take."

    menu:
        "The one on the left. Local train":
            mc  "The one on the left. Local train, not the rapid."
            hikari "Good. You were listening yesterday."
            $ reward_attributes_once("answer_left", [("insight", "nudge")], show="auto")
        "The one on the right. Rapid train":
            mc  "The one on the right. Rapid train, not the local."
            hikari "Other one. The rapid skips our stop."
            hikari "You'll remember it next time."

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
    "The professor sees me and nods. I take my seat."
    professor "You are early today."
    mc "I remembered what you said."
    professor "Good. Then remember this as well. Today we begin with haiku."
    "He writes three short lines on the board, then circles a single word."
    professor "Five, seven, five. You will have been taught that in school."
    professor "In Japanese those are mora, not syllables, but the count is not the point."
    "He taps the circled word with his chalk."
    professor "This is the kigo. The seasonal word. It places the poem in a time of year without naming the season."
    "He reads an example aloud. A frog, an old pond, the sound of water."
    "For a moment the room belongs to the poem. Then the chalk goes back to the board."
    professor "The small detail is not decoration. It is the door into the whole poem."
    mc "(A season hidden inside one word. I write it in the margin.)"
    professor "You will see this again. Pay attention to what the word is doing, not only to how many mora you can count."
    professor "Next week, a short quiz. Three questions. The kigo will be one of them."
    $ quiz_announced = True
    mc "(Three questions. I have the weekend to make sure one of them is not a guess.)"

    menu:
        "Take careful notes on the kigo.":
            $ haiku_study_method = "notes"
            mc "(I write: kigo = seasonal word; notice what it implies.)"
            $ reward_attributes_once("haiku_lesson_notes", [("insight", "nudge")], show="auto")
        "Listen closely to the example.":
            $ haiku_study_method = "listening"
            mc "(I set the pen down and listen to the poem again, looking for the season in the image.)"
            $ reward_attributes_once("haiku_lesson_listen", [("insight", "nudge")], show="auto")
        "Look up more examples online after class.":
            $ haiku_study_method = "research"
            mc "(I mark the word and make a note to compare a few translations later.)"
            $ reward_attributes_once("haiku_lesson_research", [("nerve", "nudge")], show="auto")
                
    scene black with Fade(1.0, 0.3, 0.0)
    "I write the last line of the haiku in my notebook, then look up at the professor."
    "The bell rings. The professor closes his book, and the room breaks into conversation."
    scene bg_department_hall with walk_fade



    hikari "You made it through a whole lecture on time."
    mc "I even wrote something down."
    hikari "Then let's not waste the rest of the day. Akihabara."
    mc "Now?"
    hikari "Now. The shop is less crowded while everyone is still at work."

    scene black with Fade(1.5, 0.4, 0.0)
    stop music fadeout 1.0
    "We take the underground train. The stations pass in a bright sequence of names, transfers, and doors."
    "When we come back above ground, Akihabara is already louder than the train."

    scene bg_akihabara_hamada_outside with Fade(0.0, 0.0, 1.8)
    play music "audio/SFX/akihabara.mp3" fadein 1.5
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
    yamada "Welcome to Hamada Denki. Are you looking for a phone today?"
    hikari "Not a phone. He needs a cellular plan for a device he already owns."
    yamada "Of course. Is this your first plan in Japan?"
    if first_day_activity == "walk_alone":
        mc "Yes. Mostly maps, and a way to check a place's hours before I head out."
    elif first_day_activity == "walk_hikari":
        mc "Yes. Mostly maps, and a reliable way to reach my family when plans change."
    else:
        mc "Yes. Mostly maps, messages, and the Circle group Sim invited me to."
    yamada "Then let's compare the student plans before we add anything."

    menu:
        "A basic plan is enough for now.":
            $ reward_attributes_once("cellular_plan_modest", [("insight", "micro")], show="auto")
            mc "A basic plan sounds right. I want to keep the monthly cost predictable."
            yamada "Then we can start with the student plan and check whether its data allowance fits."
        "I would rather have enough data not to worry about every search.":
            $ reward_attributes_once("cellular_plan_usage", [("nerve", "micro")], show="auto")
            mc "I would rather have enough data not to worry about every search."
            yamada "We can compare the next tier too, and look at the monthly difference before you decide."
        "Could we see the lowest student rate first?":
            $ reward_attributes_once("cellular_plan_student_rate", [("grace", "micro")], show="auto")
            mc "Could we see the lowest student rate first?"
            yamada "Certainly. Your student ID may qualify you for the student discount."

    yamada "May I see your student ID?"
    "I take the card from my wallet and pass it across the counter."
    yamada "Thank you. This confirms your student discount. The account details you already registered will verify the line."
    hikari "And this plan is only the monthly data and calls? No handset payment?"
    yamada "Correct. The phone is yours already. The student plan has a monthly fee; calls are charged only if you use them."
    hikari "Good. And what are these add-ons?"
    "He turns the tablet so we can see a list: device insurance, a video service, and extra cloud storage."
    yamada "All optional. None is needed to activate the line."

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
            yamada "Understood. I'll leave every optional service unchecked."
            $ reward_attributes_once("cellular_plan_decline_extras", [("nerve", "micro")], show="auto")

    "Yamada walks us through the monthly fee, the first partial bill, and the cancellation terms."
    "Hikari reads the summary twice. I read it once, then again where she points."
    hikari "No handset, no streaming service, no insurance. Just the plan we agreed on."
    mc "I understand."
    "I sign the form on the tablet. Yamada fits a SIM card into the phone and waits for the network to register."
    yamada "There. The line is active. You should see the signal now."
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
    call first_connection_messages from _call_first_connection_messages
    hikari "Your map has Akihabara saved now. Use it if you want to get back to the station, and message me if you need anything."
    mc "I'll try the map before I try guessing."
    hikari "Good. Guessing is how you end up on the wrong side of a very large electronics store."
    "She checks the time on her phone and makes a small, apologetic face."
    hikari "I have to get to Shibuya for some shopping later, so I should head out soon. You should still explore Akihabara while you're here; there's a lot to see."
    hikari "I wanted to show you around properly, but I'm sorry I can't stay and guide you."
    mc "It's all right. I can look around for a bit."
    hikari "You have a working map and a working phone now. That's a pretty good start."
    mc "And a very detailed warning about maid cafes?"
    hikari "One warning. If someone in a maid outfit is handing out flyers, keep moving. They're persistent once you stop."
    mc "(She says it like she was one of the ones who stopped.)"
    hikari "Message me when you're heading back. Have fun."
    "She gives me a quick wave and heads toward the station, already checking the time."

    scene bg_akihabara with walk_fade
    stop music fadeout 1.0
    play music "audio/Music/akihabara.mp3" fadein 1.5
    "Without Hikari beside me, Akihabara seems to get louder."
    "Arcade music spills outside as a racing game revs, a rhythm game draws cheers, and a prize machine clatters over both."
    mc "(I can hear three different games from here, and I can't tell which one is winning.)"
    "The electronic shops are just as imposing as Hamada Denki."
    "Their windows are packed with cameras, headphones, game consoles, tiny components, and displays bright enough to compete with the signs above them."
    mc "(We spent all that time in one store, and it still felt like we only saw a corner of it.)"
    "I stop at a display of cameras. The models look almost identical until I read the labels, and then the numbers make them seem even more different."
    mc "(A month ago, I might have walked past without thinking. Now I keep wondering what I could photograph here.)"
    "A little farther on, I pass a narrow game shop stacked from floor to ceiling with boxes."
    "A few people are studying the shelves with the concentration of students before an exam."
    mc "(Everyone here seems to know exactly what they came for. I wonder if that feeling comes from living here long enough.)"
    "I open the map on my phone. The blue marker gives my location, but not a reason to choose one street over another."

    menu:
        "Follow the arcade sounds for a while.":
            $ reward_attributes_once("akihabara_explore_arcades", [("nerve", "micro")], show="auto")
            "I follow the music to the entrance of an arcade. Rows of machines glow under the dark ceiling."
            mc "(I don't have to be good at any of them to look.)"
        "Take a closer look at the camera displays.":
            $ reward_attributes_once("akihabara_explore_cameras", [("insight", "micro")], show="auto")
            "I pause in front of the camera shop window and compare the compact models with the larger lenses."
            mc "(The one with the bigger lens looks more serious. That probably isn't a useful way to choose.)"
        "Keep to the main street and watch the crowd.":
            $ reward_attributes_once("akihabara_explore_crowd", [("grace", "micro")], show="auto")
            "I stay on the main street and watch the crowd flow around signboards, shop entrances, and people passing out flyers."
            mc "(There are patterns to it. Once I notice them, the crowd feels a little less like something I have to fight.)"

    "The streets are full of small decisions: which entrance to try, which sign to read, when to step aside and let a group pass."
    "Between the shopfronts, I start noticing the maids: black-and-white dresses, colorful aprons, little signs held out toward the passing crowd."
    "Some people accept a flyer. Others smile and keep walking. The maids call after them, but no one seems surprised by the routine."
    mc "(Hikari did say they could be persistent.)"
    "I'd heard about maid cafes before coming to Japan."
    "Back home, they had sounded almost like a story someone made up: a cafe where the staff dressed as maids and called the customers Master."
    mc "(I wanted to see one. I just hadn't decided if I wanted to admit that out loud.)"

    "One of the maids approaches, leaving enough space that I can keep walking if I want to."
    maid "Hello! Are you exploring Akihabara for the first time? We have a maid cafe just upstairs. I can explain how it works, if you're curious."

    menu:
        "I'm only looking around. I'm not sure yet.":
            $ reward_attributes_once("akihabara_maid_cafe_cautious", [("grace", "micro")], show="auto")
            mc "I'm only looking around. I'm not sure it's for me."
            maid "That's completely fine. You can look at the menu and the prices first. If you decide it's not your thing, no hard feelings."
        "I've heard about maid cafes. I've wanted to see one.":
            $ reward_attributes_once("akihabara_maid_cafe_curiosity", [("nerve", "micro")], show="auto")
            mc "I've heard about maid cafes. I've wanted to see one, actually."
            maid "Then your timing is perfect! I'll explain everything before you order. First visits can be a little surprising."
        "How do I know what to expect inside?":
            $ reward_attributes_once("akihabara_maid_cafe_questions", [("insight", "micro")], show="auto")
            mc "How do I know what to expect inside?"
            maid "A fair question. I'll go through the prices and the rules before you decide. You can say no at any point."

    "She points to a standing menu beside the entrance. The prices are printed clearly, and through the open doorway I can see other customers at their tables."
    "There's a seating charge, and the menu lists the time limit and any extra options separately."
    maid "You only order what you want. I won't add anything without asking you first."
    mc "(That is more practical than the mystery I had built up in my head.)"
    maid "No rush. I'll show you the menu, and you can still change your mind."
    mc "(Hikari's warning is still in my head. But Aya hasn't tugged at my sleeve or tried to hurry me. She seems friendly, and the place is bright and busy.)"
    mc "(Maybe being nervous and being curious can happen at the same time.)"
    mc "All right. I'll take a look."
    maid "Wonderful! This way, please."
    stop music fadeout 2.0
    scene black with Dissolve(2.0)
    play music "audio/Music/maidcafe.mp3"
    scene bg_maidcafe with walk_fade
    "The street noise falls away behind the door. Pink lights glow against polished tables, and a cheerful greeting rises from around the room."
    "The other maids greet the room in Japanese. I recognize the sound from the street, but not every word."
    aya "Welcome, Master! Is this your first time here?"
    mc "Yes. I've heard about maid cafes, but I wasn't sure what to expect."
    aya "I'm Aya, by the way. I'll be looking after you today."
    mc "(So Aya is the name on the badge. That makes this feel a little less like walking into a storybook.)"
    aya "The idea is that we're not only serving food. We make the visit playful. You can call us by our maid names, and we'll call you Master or Princess if you prefer."
    mc "And the magic spell?"
    aya "That's one of the little performances. Before some dishes, we do a short 'deliciousness' spell together. You can join in, or just watch. Nobody will make you do it."
    mc "(She says it like it is a real option. I look at the menu again, and this time I read it properly.)"
    "Aya checks that I understand the seating charge and points out the order section of the menu."
    "The time limit is printed beside it, along with the prices for optional photos and special sets."
    aya "If you want anything, just call me over. If you're not sure what something is, ask. I can explain it in English."
    "She gives me time to look through the menu instead of filling the silence for me."

    menu:
        "Ask what the extra options are for.":
            $ reward_attributes_once("maid_cafe_understand_options", [("insight", "micro")], show="auto")
            mc "Could you explain the extra options?"
            aya "Of course. Some sets include a drink or dessert, and some include a photo with a maid. Each one has its own price, so you can choose separately."
            mc "(Drink, dessert, photo. Three separate things, three separate prices. I can work with that.)"
        "Tell her the whole place is a little overwhelming.":
            $ reward_attributes_once("maid_cafe_admit_nerves", [("nerve", "micro")], show="auto")
            mc "I think I'm a little overwhelmed."
            aya "That's normal on a first visit. We can take it one step at a time: choose a drink or meal, and ignore everything else until you feel ready."
            mc "(One step at a time. I can do that.)"
        "Thank her for explaining things clearly.":
            $ reward_attributes_once("maid_cafe_thank_aya", [("grace", "micro")], show="auto")
            mc "Thanks for explaining all of that. It helps."
            aya "You're welcome. I like when first-time guests know what they're choosing."
            mc "(That sounds sincere. Maybe the cheerful voice isn't all an act.)"

    aya "Would you like a recommendation, or would you rather choose for yourself?"

    menu:
        "Please recommend something.":
            $ reward_attributes_once("maid_cafe_first_recommendation", [("grace", "micro")], show="auto")
            mc "A recommendation would be nice."
            aya "Then I suggest the omurice. It's fluffy, and I can draw something on top with ketchup just for you."
            mc "Sounds good. Let's do that."
        "I'll try choosing for myself.":
            $ reward_attributes_once("maid_cafe_first_independent_order", [("nerve", "micro")], show="auto")
            mc "I'll try choosing for myself."
            aya "Ooh, confident! What catches your eye?"
            mc "The omurice. It says it's your specialty."
            aya "A classic! I can draw something on top with ketchup just for you."
        "What do most people order?":
            $ reward_attributes_once("maid_cafe_first_popular_order", [("insight", "micro")], show="auto")
            mc "What do most people order?"
            aya "The omurice is our specialty. The parfaits are popular too, especially if you want something sweet."
            mc "Let's go with the omurice, then."
            aya "Great choice! I can draw something on top with ketchup just for you."

    "Aya repeats the order and the price before she takes the menu, giving me one last chance to change it."
    mc "That's right."
    aya "Then I'll make it special for you."
    "When she returns, she sets the plate down carefully and reaches for the ketchup bottle."
    scene bg_maidcafe_omurice with Dissolve(0.5)
    "Aya draws a small kitty on the golden omelet, adding whiskers and a tiny bow before turning the plate toward me."
    aya "There! What do you think?"
    mc "(It looks too cheerful to eat. That isn't going to stop me, is it?)"
    scene bg_maidcafe with Dissolve(0.5)
    aya "Before you eat, we do the magic spell together. Copy me, okay?"
    "She makes a heart with her hands and leans toward the plate."
    menu:
        "Try the spell with her.":
            $ reward_attributes_once("maid_cafe_join_spell", [("nerve", "micro")], show="auto")
            aya "Are you ready?"
            mc "(I am in a crowded cafe in Akihabara, making a heart with my hands over lunch. The room does not stop for it. Neither do I.)"
            voice "audio/VO/moekyun.mp3"
            aya "Moe moe...Kyun!"
            mc "Moe moe... kyun."
            aya "Perfect! Now it'll be extra delicious."
        "Smile and let her do the spell for both of us.":
            $ reward_attributes_once("maid_cafe_watch_spell", [("grace", "micro")], show="auto")
            mc "I think I'll watch this time."
            aya "Of course! I'll do it for both of us."
            "Aya makes the heart shape over the plate and chants the spell with a flourish."
            voice "audio/VO/moekyun.mp3"
            aya "Moe...Kyun!"
            mc "(For a second the whole room is in on it. Then the next table orders, and the moment moves on.)"
    "The omurice is better than I expected. Aya checks in once, then gives me room to eat while the room's noise settles into something almost comfortable."
    aya "Did you enjoy it, Master?"
    mc "Yeah. More than I expected."
    aya "I'm glad! You did great for your first visit."
    mc "I mostly ordered lunch."
    aya "And learned the spell. That counts."
    "She clears the plate and leaves a small card beside the bill, with the cafe's name and opening hours printed on it."
    aya "If you come back, you can ask for me. I'll remember your first visit."
    mc "(I don't know if I'll be back soon, but the idea doesn't feel strange anymore.)"
    "As I get ready to leave, Aya takes a second card from her apron. This one has a square WIRE code on it."
    aya "Before you go, would you like to add me on WIRE? You can use this to check in next time."
    aya "It's like a little stamp card: your visits build up toward small discounts and returning-customer bonuses."
    mc "So I scan this?"
    aya "Exactly. It's the cafe account I use for guests. No pressure, but if you come back, it'll make checking in easier."
    "I open the scanner on my phone and hold it over the code. Aya's name appears on the screen."
    mc "(A new contact, from a place I only walked into because I was curious.)"
    $ confidant_visits["aya"] = max(confidant_visits.get("aya", 0), 1)
    # Aya joins the cast with the same first-visit regard the chef and Sim get.
    # The number is a relationship level, not a reward; later cafe scenes read it.
    $ aya_affection += 1
    $ wire_unlock("aya")
    mc "There. You're in my contacts."
    aya "And now you have a reason to come back!"
    aya "Thank you for visiting, Master. Please be careful on your way back to the station."
    mc "I will. Thanks, Aya."

    scene bg_akihabara with walk_fade
    stop music fadeout 1.0
    play music "audio/Music/akihabara.mp3" fadein 1.5
    "Outside, the arcades and bright shop signs are waiting exactly where I left them."
    "Hikari said to message her when I head back, so I take out the phone while the light lasts."
    $ run_chat("hikari", [
        {"options": [
            {"label": "\"I'm heading back to the station now.\"",
             "send": "I'm heading back to the station now."},
        ]},
        {"them": "Good. Don't get lost in any more cafes."},
        {"them": "Did you actually go in, or did you just collect flyers?", "options": [
            {"label": "\"I went in. Ordered lunch. Did the spell.\"",
             "send": "I went in. Ordered lunch. Did the spell.",
             "them": ["Good. First-timer rites complete.",
                      "The kitty drawing better be good."]},
            {"label": "\"I might have collected a flyer or two.\"",
             "send": "I might have collected a flyer or two.",
             "them": ["Honest. I respect it.",
                      "The cafe will still be there next time."]},
        ]},
    ])
    mc "(I went in. I ordered lunch. I did the spell. The last one is going in the notebook.)"
    "A group of students passes me, comparing keychains from a capsule machine. I let them go by, then check the station sign."
    "I find the station using the map. This time I check the sign before choosing an entrance."
    scene bg_train_interior with walk_fade
    stop music fadeout 0.8
    play music "audio/Music/train.mp3" fadein 1.5
    "On the train, I open my notebook and write down the phrase I heard at the cafe door: 'okaerinasaimase', welcome home."
    "Under it, I add a small drawing of a cat with a bow. It comes out less like a cat and more like a dumpling."
    mc "(I'll remember the real one better.)"
    "My phone buzzes against my leg. Hikari asks if I found the station."
    mc "(Right. Cellular. The phone is actually a phone now.)"
    $ run_chat("hikari", [
        {"them": "Did you make it to the station okay?", "options": [
            {"label": "\"Just got here.\"",
             "send": "Just got here.",
             "them": ["Good."]},
            {"label": "\"Lost again, but I found the exit.\"",
             "send": "Lost again, but I found the exit.",
             "them": ["You have a map now. Use it."]},
        ]},
        {"say": "(photo)", "img": "images/messages/notebook_page.png"},
        {"them": "That cat looks like it needs help.", "options": [
            {"label": "\"It's a work in progress.\"",
             "send": "It's a work in progress.",
             "them": ["Good. You can practice on the train."]},
            {"label": "\"It's supposed to be a cat.\"",
             "send": "It's supposed to be a cat.",
             "them": ["Sure it is.", "Practice anyway."]},
            {"label": "\"I'll send you the real one later.\"",
             "send": "I'll send you the real one later.",
             "them": ["I'll hold you to that."]},
        ]},
    ])
    "The city slips past the window. Hamada Denki, the arcade signs, and the cafe's pink lights settle into separate memories instead of one long blur."
    "I arrived with a phone that could only reach the house. Now it can get me across the city, and I have a reason to look forward to opening it again."
    stop music fadeout 3.0

    # The day does not end on the train. It ends at the kitchen table, where the
    # family gets to ask what the new phone and the new city actually cost him,
    # and then upstairs, where the first weekend is waiting.
    scene bg_nakanostation_night with walk_fade
    $ night_street()

    "The station is emptying out. The last of the office crowd goes down the stairs ahead of me, and the lights over the ticket gate make everything look newly washed."
    "I know the turn out of the station now. I do not have to stop and check the map."
    mc "(That is one thing I can do here. It is not a small thing.)"

    scene bg_home_exterior_night with walk_fade

    "The kitchen window is lit. Not the porch light. The kitchen."
    mc "(They waited up.)"

    scene bg_home_night with walk_fade
    "The front door is unlocked. I slide it shut behind me and put my shoes on the rack, beside Hikari's."
    "For a second the house smells like dinner and laundry and something older underneath, the way a house smells when people have been in it for years."

    scene bg_kitchen_night with walk_fade
    $ room_ambient(True)

    "Mother is at the table with a cup of tea she has finished. Father has the newspaper open at the same page he was pretending to read this morning."
    mother "There you are."
    father "You're back."
    hikari "Told you."
    mc "You were all waiting?"
    hikari "Dad checked the clock four times."
    father "I checked it once."
    mother "Four times."
    father "..."
    "He turns the page. It is the same page."
    mother "Sit. There's rice left, and the soup is still hot."

    scene bg_nightfood with walk_fade

    "She sets a bowl in front of me. The rice is cold at the edges and warm in the middle. The miso has tofu and wakame in it, and a small dish of pickled cucumber sits beside the bowl."
    father "Rice first. Then the fish. The soup between."
    hikari "He means there's no wrong way to eat it."
    father "There is a right way."
    hikari "There is his way."
    mc "(I pick up the chopsticks and start with the rice.)"

    father "So. What did today cost you?"
    hikari "Dad."
    father "It is a fair question. He bought a phone plan."
    mc "It's not a trap?"
    father "It is a question."
    "He says it without looking up from the newspaper. Mother keeps her tea between both hands and watches us over the rim."

    menu:
        "I checked the total before I signed. It was less than I expected.":
            mc "I checked the total before I signed. It came in lower than I expected."
            father "Good. Then you read the numbers, not the sign on the wall."
            $ reward_attributes_once("night_table_total", [("insight", "micro")], show="auto")
            $ add_affection("father", 2)
        "I spent what I needed to. Nothing extra.":
            mc "I spent what I needed to. No handset, no extras, no insurance I didn't ask for."
            father "Then you did it properly."
            $ reward_attributes_once("night_table_plain", [("grace", "micro")], show="auto")
            $ add_affection("father", 1)
        "I'd rather not turn dinner into a bill.":
            mc "I'd rather not turn dinner into a bill."
            "The newspaper comes down an inch."
            father "..."
            father "That is fair too. You are allowed to keep some things for yourself."
            mother "That was a good answer."
            hikari "He's learning."
            $ reward_attributes_once("night_table_boundary", [("nerve", "micro")], show="auto")
            $ add_affection("father", 1)
        "[tag_nerve] I could tell you. Then you could tell me what the car cost." if has_attribute_points("nerve", 1.2):
            mc "I could tell you. Then you could tell me what the car cost."
            "Hikari's chopsticks stop halfway to her mouth."
            father "..."
            father "The car is paid for."
            mc "So is the phone plan."
            father "..."
            "Something moves at the corner of his mouth. It is gone before I can be sure."
            hikari "Oh no. He's got a sense of humor."
            mother "Don't encourage him."
            $ reward_attributes_once("night_table_nerve", [("nerve", "micro")], show="auto")
            $ add_affection("father", 1)

    father "The plan is a tool. Keep it in your pocket when you walk. Look up."
    hikari "Don't mind him. He says that to me every time I leave the house."
    father "Because you don't look up."
    hikari "See?"
    mc "(It is the same conversation they have every morning. It is starting to sound less like an argument and more like a door being held open.)"

    hikari "He went to a maid cafe."
    mc "Hikari."
    father "..."
    mother "Did you enjoy it?"
    mc "I did. More than I expected."
    father "Then you paid for something you enjoyed. That is not a waste."
    hikari "Dad."
    father "What? I am being supportive."
    mother "You are being supportive at the table."
    "I look down at my rice. It is the first time all day that I have not known where to put my face."
    father "Next time, tell us where you are going. Not so we can stop you. So we know where to start looking."
    mc "I will."
    hikari "Don't mind him. He's been practicing that sentence all evening."
    father "I have not."
    mother "You have."

    # The first writing lesson the family gives him is the two characters for
    # his own station. It is practical, small, and exactly how Tetsuo says he
    # cares: by making sure the boy can read his way home.
    father "The station. You can say it. Can you read it?"
    mc "..."
    father "Then learn it."
    "He takes the receipt from beside his cup and writes two characters on the back. 中野."
    father "Nakano. Middle field. The first one means middle. The second one means field."
    mc "(I have seen those two shapes on the address he sent me. I did not know they were a place.)"
    father "Say it."
    mc "Nakano."
    father "Again."
    mc "Nakano."
    "He puts the receipt on the table between us. It is a map now, or the beginning of one."
    if affection_at_least("father", 2):
        "Under the characters, he draws two lines and a small box. The station, the corner, the house."
        father "In case you get lost."
        hikari "He's been practicing being helpful. It still looks like a rule."
        father "It is a map."
        mc "(It is a map. It is also the most he has given me since I arrived.)"

    mc "The professor said there's a quiz next week. Three questions. The kigo is one of them."
    father "Then study."
    hikari "There's a reading room on the third floor. East wing. The one with the long tables."
    hikari "I pass it on the way to my class. It's quiet. Too quiet, if you ask me."
    mc "You're giving me a destination."
    hikari "I'm giving you a quiet room. What you do there is your business."
    hikari "There's a reading club that meets there. They don't recruit. They just read."
    $ library_errand_available = True
    mc "(A quiet room, a quiz, and a club that does not recruit. It sounds like the beginning of a plan.)"

    "Mother takes the empty bowls. Father folds the newspaper, which has not moved all evening."
    father "It's Friday. The weekend starts tomorrow."
    hikari "Two days. No school."
    father "Then use them."
    hikari "Don't mind him."
    mc "I'm starting to think that's your answer for everything."
    hikari "It's a good answer."

    scene bg_room_night with stair_fade
    $ room_ambient(True)

    "Hikari walks me up. The stairs creak under both of us, and this time she does not apologise for it."
    "I carry the receipt up and set it on the desk. She watches me do it."
    hikari "So. Two days. What are you going to do tomorrow?"
    mc "I haven't decided."
    hikari "Then decide. That's the whole point of a day off."

    hikari "You've decided. You just haven't said it out loud."
    mc "The reading room. If the quiz is real, I can't afford to guess."
    hikari "Then it's settled. Library first thing. Before the crowds, before the excuses."
    $ reward_attributes_once("night_weekend_study", [("insight", "micro")], show="auto")
    $ add_affection("sister", 1)

    if affection_at_least("sister", 2):
        hikari "Hey. Today. At the cafe. You didn't have to go in."
        mc "I know."
        hikari "I'm glad you did."
        "She says it to the doorframe, not to me."
    else:
        hikari "Get some sleep. The library isn't going anywhere."

    jump night_room_visit


label night_room_visit:
    # She doesn't go downstairs. She leans in the doorframe a moment longer,
    # then comes in and sits on the edge of my desk — a thing she has never done
    # before — because there is one more thing she has clearly been saving.
    hikari "One more thing. The quiz is next week, and after that it's midterms. Three weeks. Maybe four."
    mc "I can handle three weeks."
    hikari "You can barely handle a school day. But yes. You can."
    "She picks up the receipt from the desk, the one with 中野 on the back, turns it over, and sets it down again."
    hikari "The library is where people actually get things done. Not the classroom. The classroom is where they tell you what to think about."
    hikari "The library is where you find out if you agree."
    hikari "Third floor. East wing. Past the vending machines, left at the noticeboard with the corner taped back on. The door has no sign."
    mc "How do I know which door has no sign when half of them don't?"
    hikari "Because you've walked past it both days you've been on campus and never once looked up."
    mc "(She has. She notices things. It is unsettling how good she is at it.)"
    hikari "Tomorrow. Don't sleep through it. Don't wander off. And if you get lost,"
    mc "Ask literally anyone."
    hikari "Ask the person reading. They're always the ones who know where things are."

    menu:
        "\"I'll be at the library first thing.\"":
            mc "I'll be at the library first thing."
            hikari "Good. Go to bed, then."
            $ remember("hikari", "promised to study at the library before anything else")
            $ reward_attributes_once("night_room_library_promise", [("insight", "micro")], show="auto")
            $ add_affection("sister", 1)
        "\"What do I actually need to study?\"":
            mc "What do I actually need to study?"
            hikari "The haiku handout. The history notes. Everything the professors said that sounded like it mattered."
            hikari "If you only have an hour, do the handout. If you have three, do everything and then some."
            $ remember("hikari", "asked her what to study before the quiz")
            $ reward_attributes_once("night_room_study_plan", [("grace", "micro")], show="auto")
            $ add_affection("sister", 1)
        "\"You're going to quiz me, aren't you.\"":
            mc "You're going to quiz me, aren't you."
            hikari "..."
            hikari "Maybe."
            mc "(She is. I know she is. She has been waiting all evening to do this.)"
            $ remember("hikari", "teased her about quizzing him before the exams")
            $ reward_attributes_once("night_room_tease", [("grace", "micro")], show="auto")
            $ add_affection("sister", 1)

    "She pulls the door shut behind her this time. Her footsteps go down the stairs, pause at the bottom, and then the kitchen light clicks off."
    "I stand in the middle of my room, looking at the receipt on the desk."

    "Two days ago I landed with a phone that could only reach the house. Tonight I came home on a train I found by myself."
    "That is not a life yet. It is a route. Routes can be repeated."
    "I set the receipt beside the phone. 中野. Two characters I could not have read this morning."
    "Then I turn off the lamp."

    window hide
    scene black with Dissolve(2.5)
    stop music fadeout 2.0
    pause 1.0

    $ dream_key = "day_two_cellular_maid"
    jump dream_router


################################################################################
## ACT TWO: THE HUB
################################################################################
##
## The free afternoon as a standing offer. A day scene calls `free_afternoon`
## after lunch; the hub asks where the afternoon goes, and the answer jumps to
## that place's visit label. `None` (Head Home) means the day was left unspent.
##
## The visit labels below are stubs on purpose: each one is where that person's
## next scene plugs in, written from the matching file under
## documentation/Locations/. A stub ends the afternoon quietly so an unfinished
## place can never soft-lock the day. When a visit is scripted it should end
## with `return`, which lands back in the day scene that called this.
##
## The gating (one visit per outing, no revisits until everyone has been met,
## act caps) all lives in destination_state() in locations.rpy — this label
## only routes.

label free_afternoon:

    # Overnight and between-visit texts arrive here if the line is live.
    $ flush_pending_messages()
    $ place = renpy.call_screen("location_hub")

    if place == "sim":
        jump confidant_visit_sim
    elif place == "orson":
        jump confidant_visit_orson
    elif place == "chef":
        jump confidant_visit_chef
    elif place == "aya":
        jump confidant_visit_aya
    elif place == "hana":
        jump confidant_visit_hana

    # None, or anything the hub should not have offered: the afternoon is his
    # to spend elsewhere, so the day simply continues.
    return


################################################################################
## THE WEEKEND: LIBRARY, HANA, AND LUPIN'S DEN
################################################################################
##
## The day after the day-two dream. Friday's exam talk sends him to the library
## on his one free day; the errand is real (the haiku handout), but the room he
## ends up studying in is the reading club's, which is where Hana's first
## interaction lives. On the way home he takes a wrong turn and finds Orson's
## bar. Both introductions are written from the matching files under
## documentation/Locations/ and both set their first-visit tracking.

label saturday_off:
    # Day 4: Saturday, April 11. The library, Hana, and Lupin's Den.
    $ set_story_day(4)

    # Overnight texts land here if the line is live.
    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "I wake before the rest of the house, which is new. The house is quiet on Saturdays in a different way."
    "No train, no clock ticking in anybody's head."
    mc "(The dream was the phone plan again. Contracts with a visit count already filled in.)"
    "I lie there a minute anyway. Some part of me is still checking the dream for hidden rooms."

    scene bg_kitchen with walk_fade
    "The kitchen smells like miso and grilled fish."
    "A normal Saturday breakfast, which is its own small event in this house."
    mother "You're up early. Good. Eat something before you disappear."
    mc "I'm going to the library. Hikari gave me the route."
    mother "The library. Good. A library is a building that keeps its promises."
    father "Eat first. Breakfast can wait ten minutes. You cannot."
    hikari "He's already dressed. He's been dressed since before I came down."
    mc "(She is not wrong. I have been awake for twenty minutes and already regretting getting up.)"

    "I eat standing up, which earns me a look from Father that I decide not to understand."
    mother "There's sukiyaki tonight, if you behave. Your father has been planning it since Thursday."
    father "I have not."
    hikari "He has. He asked the butcher."
    hikari "Route check. Third floor, east wing, past the vending machines,"
    hikari "left at the noticeboard with the taped corner. Door with no sign."
    mc "You sound like a recording."
    hikari "I am a recording. Play me when you get lost."
    hikari "And take your phone. Not for the map, for me."
    mc "For you?"
    hikari "So I can find you. If you're not back by dinner, I'm telling Dad you ran away."
    "She says it flat, which is how you can tell she means it."

    scene bg_school_gate with walk_fade
    "Saturday campus is a different building. Fewer people, older light,"
    "the kind of quiet that has weight to it."
    "Friday's plan held: the library, the studying, the handout."
    jump library_search


label library_search:
    # The directions are exact, which is the problem: exact directions fail in
    # exactly one way, and I have found it.
    scene bg_campus_interior with walk_fade

    "The library is bigger than it looks from outside, which is the first lesson of this building."
    mc "(Hikari said third floor, east wing. Third floor, east wing."
    mc "I have repeated it enough times that it should be a street address by now.)"

    "The third floor is mostly empty on a Saturday. I count the doors as I go:"
    "seminar rooms, a stairwell, a storage closet with a padlock older than I am."
    "No noticeboard with a taped corner. No vending machines. 'East wing' might be a rumor."
    "I try the floor plan by the stairs. The library is one building inside the building,"
    "and I keep missing the door that leads into it."
    "Around me, students read like it is a job they applied for."

    menu:
        "Ask the student reading by the window.":
            mc "Excuse me, which way is the reading room?"
            "The girl looks up. She is about my age, has a pencil behind her ear,"
            "and has clearly been on the same page for a while."
            quiet_student "...Third floor, but you're already here. You're looking for the room with the low tables."
            mc "The one with no sign?"
            quiet_student "That one. Quietest room in the building. People go there to read, some to study."
            quiet_student "They share the same quiet."
            mc "(That is almost word for word what Hikari said. She must have sat in that room herself once.)"
        "Follow the smell of green tea.":
            "I follow the smell. Green tea and old paper, either the library or a very specific kind of trap."
            "The corridor narrows. The ceiling fan ticks somewhere overhead. The smell gets stronger."
            "A door stands open a crack, and through it I can see low tables and the tops of bent heads."
        "Check the floor directory by the stairs.":
            "The directory is a hand-drawn map someone taped to the wall,"
            "corrected in three different handwriting styles."
            "It says: EAST WING, then QUIET ROOMS, then a door drawn with no label at all."
            "Somebody has added a red-pen arrow and the characters 「ここ」."
            mc "(Even the map admits it doesn't have a name.)"

    "Whichever way I turn, it is the same door. Low wooden tables, mismatched chairs,"
    "one long window with the blinds half drawn."
    "The air smells like paper and green tea. A handful of students are already seated, reading."
    "Somewhere near the back, a ceiling fan ticks."
    "I almost turn around at the threshold. It feels like walking into a place where everyone already"
    "knows the rules and I wasn't given the manual."
    jump reading_club_first


label reading_club_first:
    scene bg_library with walk_fade

    "The rules turn out to be two rules, delivered by a student at the nearest table,"
    "who has decided I am harmless enough to explain things to."
    quiet_student "First time? Don't worry, it's not a club-club. No forms, no speeches."
    quiet_student "Just pick any book off the shelves and sit down. We read for an hour."
    quiet_student "Sometimes people share a thought when the hour ends. Sometimes nobody says anything at all."
    quiet_student "Both are fine."

    menu:
        "\"Can I read in Japanese... even if I'm slow?\"":
            mc "Can I read in Japanese... even if I'm slow?"
            quiet_student "Slow is allowed. This is the one room in the city where nobody will rush you."
        "\"I don't really know what to pick.\"":
            mc "I don't really know what to pick."
            quiet_student "Then pick the shortest one. Nobody's grading you. That's the whole point of this place."

    "I came for documents, which feels like cheating at a place like this."
    "The course reserve is two shelves over: a thin packet of past lecture handouts,"
    "and on top of it a stapled set of haiku study sheets, kigo lists, example poems, the works."
    mc "(Hikari was right. People do come here to actually get something done.)"
    "I take the haiku sheets to a table by the window. The student who explained the rules sits two tables down"
    "and goes back to her book like I am furniture."
    $ reward_attributes_once("library_errand_docs", [("insight", "micro")], show="auto")
    $ library_errand_available = False

    "And then I see her."
    "A girl is shelving returns at the far wall. Dark hair, plain clothes,"
    "moving so carefully she barely makes a sound."
    "She slots a book into place, then looks up, and for one split second, our eyes meet."
    "The moment I register her, she looks away. A book slips in her hands."
    "She catches it, tucks her chin down, and walks quickly out of the room through the side door,"
    "like the air between us had turned to glass."
    "Gone. Just like that."
    "I take two steps toward the side door before I talk myself out of it."
    "Whatever she is, she didn't ask to be followed."
    mc "Who's that?"
    quiet_student "Oh... Hana? She volunteers here. Shelves the returns, straightens everything, never stays long."
    quiet_student "Her badge says it, she wrote it herself, I think. Nobody's ever heard her say it out loud."
    quiet_student "Doesn't really... talk. Every time someone tries, she runs off. But she's always around."
    quiet_student "Every single week."
    mc "Has she ever said anything to anyone?"
    quiet_student "Not to me."
    "She says it with a small, unbothered laugh, the way you laugh about weather."
    mc "(I write it down anyway. Hana. That's her name now, whether she wants it to be or not.)"

    "The hour ends the way it said it would, without anyone announcing it. Pages close. Chairs scrape."
    "People gather their things."
    "And then she passes my table."
    "The girl from the far wall, Hana, walks the aisle between the desks with a book hugged to her chest,"
    "and for one unguarded second she is simply *there*:"
    "same height as the shelves she moves between, breathing like everyone else."
    "She sets a slim, older volume on the desk beside my elbow. Square to the edge. Deliberate."
    "Then she is gone through the side door before anyone can look up."
    "I look toward the door. There is no one there."
    "The ceiling fan ticks. Somewhere, a page turns."
    "I don't know her. I don't know why she left a book on my desk."
    "I only know she didn't want me to see her do it."
    "I leave it where it is. Whatever it is, it isn't mine to take."
    "I slide the haiku sheets into my bag. Then I pack up slowly, like the room might object."

    $ confidant_visits["hana"] = max(confidant_visits.get("hana", 0), 1)
    $ hana_affection += 1
    $ remember("hana", "watched her flee the reading room on his first visit")
    $ wire_unlock("hana")
    $ reward_attributes_once("reading_club_first", [("grace", "micro")], show="auto")

    scene bg_campus_interior with walk_fade
    "Outside, the light has gone the color of weak tea."
    "Saturday is ending the way Saturdays do, all at once."
    "My phone buzzes in my pocket. Hikari."
    $ run_chat("hikari", [
        {"them": "You alive?", "options": [
            {"label": "\"Alive. Just left the library.\"",
             "send": "Alive. Just left the library.",
             "them": ["Of course you are.", "That's where you said you'd be."]},
            {"label": "\"Define alive.\"",
             "send": "Define alive.",
             "them": ["That is not an answer.", "Are you on your way back?"]},
        ]},
        {"them": "(photo)", "img": "images/backgrounds/bg_nightfood.png"},
        {"them": "Sukiyaki tonight. Mom's already arguing with Dad about the broth.", "options": [
            {"label": "\"It looks incredible.\"",
             "send": "It looks incredible.",
             "them": ["It will taste better than it looks. She's been practicing all week."]},
            {"label": "\"Teach me to make it.\"",
             "send": "Teach me to make it.",
             "them": ["You'll be on potato duty. It's the only job with no way to fail."]},
        ]},
        {"them": "Don't take the long way home. The trains stop running at eleven and Dad will notice if you're late.", "options": [
            {"label": "\"I'm heading back now.\"",
             "send": "I'm heading back now.",
             "them": ["Good.", "See you at dinner."]},
            {"label": "\"What could possibly go wrong.\"",
             "send": "What could possibly go wrong.",
             "them": ["Everything.", "I am not joking. Come straight home."]},
        ]},
    ])
    mc "(She has never once said 'come straight home' without meaning it literally and completely.)"

    # She said come straight home. I take a different route instead, which is not
    # technically disobeying anything, and the neighborhood obliges by getting
    # worse at being a neighborhood with every turn.
    "The map puts me on a street I've never seen, and every turn after that is a guess."
    "Fewer students, more shutters, the kind of street that only exists after the shops that serve them"
    "have gone home."
    scene bg_alley with walk_fade
    "I pass a doorway with a cloth over it and a small wolf painted on the sign."
    "The paint is faded but deliberate, the kind of sign made by someone who cares about it."
    mc "(A bar, maybe. Or a shrine. Or a noticeboard with ambitions.)"
    "Inside is warm in a way the street is not, amber light on polished wood, low jazz,"
    "the smell of citrus peel and whiskey."
    jump lupins_den_first


label lupins_den_first:
    scene bg_lupins_den with walk_fade

    "It is a narrow room. Patrons sit in quiet clusters along the counter, a fox, a rabbit,"
    "a plain white face, all in partial masks, none of them talking to each other."
    "The air smells of citrus peel and whiskey. Somewhere a glass is set down too gently,"
    "like it costs something to make noise here."
    "Behind the counter, a wolf in a half-mask is polishing a glass."
    "He does not look up when I take the stool at the end of the counter."
    "The only spot that fits without bumping shoulders. The stool wobbles."
    bar_master "..."
    "That is the whole greeting. He goes back to the glass."
    "Somewhere down the bar the rabbit laughs at nothing, too loudly, and nobody else reacts,"
    "like it happens every night."
    "After a while he sets a glass of water in front of me. I didn't order anything."
    "I didn't order anything from anyone, there is no menu I can read."

    menu:
        "\"...Thanks.\"":
            mc "...Thanks."
            "The wolf mask tilts, barely, in what might be a nod."
            bar_master "You found us. Most people don't."
            $ reward_attributes_once("lupins_den_thanks", [("grace", "micro")], show="auto")
        "(Say nothing. Drink the water.)":
            "I pick up the glass and drink. He notices anyway, the wolf mask tilts, barely,"
            "in what might be a nod."
            bar_master "You found us. Most people don't."

    "Two of the masked regulars finish their drinks and leave without a word."
    "The third, the fox, catches my eye for half a second and looks away first,"
    "which somehow feels like the polite thing to do here."
    "Before I leave, the wolf says one more thing, still not looking up,"
    bar_master "The water's on the house. The conversation isn't. But you're welcome to it."
    "I don't know what that means. I don't think I'm supposed to."
    "On the counter, a small wooden bowl with a card beside it,"
    "something about leaving a note for the Master. I don't use it. But I remember it exists."
    "Like a door I could knock on next time."
    "I leave a little lighter than I arrived, and with one question I can't shake:"
    "what do people talk about in a place where nobody has to show their face?"

    $ confidant_visits["orson"] = max(confidant_visits.get("orson", 0), 1)
    $ orson_affection += 1
    $ remember("orson", "found Lupin's Den on a wrong turn home from the library")
    $ wire_unlock("orson")
    $ reward_attributes_once("lupins_den_first", [("nerve", "micro")], show="auto")

    scene bg_alley with walk_fade
    "The street outside is the same street, but I am seeing it differently now,"
    "like the bar added a layer to it that wasn't there before."
    jump home_sukiyaki


label home_sukiyaki:
    scene bg_home_exterior_night with walk_fade
    $ night_street()

    "The kitchen window is lit. Not the porch light. The kitchen."
    mc "(They waited up.)"

    scene bg_nightfood with walk_fade
    "Inside, the table is set for four, and in the middle of it a pot is still steaming, sukiyaki,"
    "the sweet-soy broth gone glossy, beef slices fanned on a plate,"
    "mountains of vegetables waiting their turn."
    mother "You're home. Sit. The beef goes in last, that's the part everyone gets wrong."
    mother "For anyone who's never had it, thin beef, sweet soy, vegetables that hold their shape."
    mother "You cook it at the table so everybody gets some."
    mother "It's what you make when the people you want to feed are the ones coming home."
    mc "(Nobody says it directly. Nobody has to.)"
    mc "Hikari sent me a picture."
    mother "She sends pictures of everything. It's her way of saying she was thinking about you while you were"
    mother "out."
    hikari "It is not."
    mother "It is exactly that."
    father "You took the long way."
    mc "I got a little lost."
    hikari "He told me the second I walked in. He always knows."
    father "The long way and the lost way are the same way until you find it."
    hikari "He found a bar."
    "The room goes quiet for exactly one breath."
    father "..."
    mother "A bar. Did you eat there?"
    mc "They gave me water. It was... nice, actually."
    hikari "Define nice."
    mc "Like the room had already decided I was allowed to be there."
    "Mother laughs, the real one, the one that gets away before she can stop it."
    mother "Then you should go back. Some doors only open once."
    hikari "He's not going back. He's going to eat sukiyaki before it gets cold."
    "I sit down. The beef goes into the pot one slice at a time, and for a moment nobody says anything,"
    "and the steam does the talking for all of us."
    "That is enough. That is more than enough."

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the house winds down the way it always does, father's newspaper, mother's tea things,"
    "Hikari's footsteps on the stairs that creak under her anyway."
    "I lie in the dark and try to remember the girl's face at the library. It doesn't stay."
    "She didn't want it to."
    "Tomorrow the quiz study continues. Tonight there is sukiyaki and sleep,"
    "and both of them were earned."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump sunday_morning


################################################################################
## SUNDAY: THE QUIET DAY
################################################################################
##
## The second off day. No school, no errand — just Hikari collecting on the
## "Maybe." she left hanging Friday night, a WIRE app that finally has enough
## names to be interesting, and a family that notices everything.

label sunday_morning:
    # Day 5: Sunday, April 12. The practice quiz at home.
    $ set_story_day(5)

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Sunday arrives the way Sundays do, late, and without apology."
    "I wake to the smell of miso soup and the sound of father reading the sports page out loud,"
    "which is somehow worse than the newspaper staying folded."
    mc "(Saturday is already a story I tell myself. Library, a girl made of held breath,"
    mc "a bar full of masks, sukiyaki. It took one day to become the best day I've had here.)"

    scene bg_kitchen with walk_fade
    mother "You're up. Good. There's rice if you want it."
    father "The city can wait until Monday. So can you, apparently."
    hikari "Dad."
    mother "Hikari's been waiting for you since seven. There's something on the table."
    "On the table: the haiku handout from Saturday, a pencil,"
    "and a look on Hikari's face that I have learned to recognize."
    "It means she has been thinking about something since breakfast."

    hikari "So. Before Monday eats your whole week, I'm quizzing you. Right now. No take-backs."
    mc "You're serious."
    hikari "I gave you the route on Friday. Today I'm checking the work."
    mc "(The politeness era is over.)"
    hikari "Three questions. The handout. If you get them wrong I'll pretend it was a warm-up."

    scene bg_home_day with walk_fade
    "We move to the low table in the front room. Father retreats to his newspaper with the specific"
    "dignity of a man who has decided this is not his problem."
    "I open the handout. Kigo lists, example poems, the works,"
    "the same stapled sheets I carried home Saturday and haven't opened since."
    hikari "Question one. What is a kigo?"
    $ sunday_quiz_score = 0
    $ sunday_q1_correct = False
    $ sunday_q2_correct = False
    $ sunday_q3_correct = False
    menu:
        "\"The seasonal word that carries the whole poem.\"":
            mc "The seasonal word that carries the whole poem."
            hikari "Correct. It does more than name the season, it tells you what the season feels like from the inside."
            $ sunday_q1_correct = True
            $ sunday_quiz_score += 1
            $ reward_attributes_once("sunday_quiz_q1", [("insight", "micro")], show="auto")
        "\"A counting rule for syllables.\"":
            mc "A counting rule for syllables."
            hikari "That's the five-seven-five. Different thing. The count is the skeleton; the kigo is the weather."
        "\"The poet's pen name.\"":
            mc "The poet's pen name."
            hikari "No. Though if it were, I'd respect it, pen names are just masks for writers."

    hikari "Question two. Five-seven-five counts what, exactly?"
    menu:
        "\"Mora, on, not syllables.\"":
            mc "Mora, on, not syllables."
            hikari "Right. Japanese counts sounds, not English syllables."
            hikari "The professor said the count isn't the point, but it is the door."
            $ sunday_q2_correct = True
            $ sunday_quiz_score += 1
            $ reward_attributes_once("sunday_quiz_q2", [("insight", "micro")], show="auto")
        "\"Words.\"":
            mc "Words."
            hikari "No, sounds. Five sounds, seven sounds, five sounds. You'd be amazed how many words that is."
        "\"Characters.\"":
            mc "Characters."
            hikari "Closer, but no. It's not how long the line looks, it's how many beats are in it."

    hikari "Last one. This is the trick question, so think before you answer."
    hikari "The clerk said three absences means what, exactly?"
    menu:
        "\"You can't sit the final exam. You still attend, you just get no mark.\"":
            mc "You can't sit the final exam. You still attend, you just get no mark."
            hikari "..."
            hikari "You were listening in student relations."
            hikari "Correct. Attendance is a currency here, and three absences is broke."
            $ sunday_q3_correct = True
            $ sunday_quiz_score += 1
            $ reward_attributes_once("sunday_quiz_q3", [("insight", "micro")], show="auto")
        "\"You fail the class.\"":
            mc "You fail the class."
            hikari "No. Colder than that, you don't fail, you just... don't count."
            hikari "The seat stays warm and the mark stays blank."
        "\"Nothing. It's a suggestion.\"":
            mc "Nothing. It's a suggestion."
            hikari "If it were a suggestion, the clerk wouldn't have said it twice."

    if sunday_quiz_score == 3:
        hikari "Huh."
        hikari "Maybe you'll survive midterms after all. Don't let it go to your head,"
        hikari "the real quiz has a professor watching."
        $ remember("hikari", "passed her Sunday practice quiz without help")
        $ add_affection("sister", 2)
    elif sunday_quiz_score == 2:
        if not sunday_q3_correct:
            hikari "Two out of three. The attendance one almost got you,"
            hikari "that one's the one people forget until it costs them."
            $ remember("hikari", "nearly forgot the three-absences rule on her quiz")
        elif not sunday_q1_correct:
            hikari "Two out of three. You lost the kigo, which is the one I would have bet on you getting."
            hikari "The seasonal word is the door into the whole poem. Remember that."
            $ remember("hikari", "missed the kigo definition on her quiz")
        else:
            hikari "Two out of three. You can name the season, but the count still trips you."
            hikari "Sounds, not words. The professor will not let that one slide twice."
            $ remember("hikari", "lost the counting question on her quiz")
        $ add_affection("sister", 1)
    else:
        hikari "We're doing this again before midterms. Same table, same handout, and this time you read before I ask."
        $ remember("hikari", "struggled through her Sunday practice quiz")
        $ add_affection("sister", 1)

    "She collects the handout, squares it against the table edge,"
    "and slides it back across the table to me, like it was always mine."
    mc "(It was always hers. I was just the exam.)"

    # The afternoon belongs to him. WIRE has been growing all week; now it has
    # Hikari, whoever he met on day one, Aya, and the two people he met yesterday.
    scene bg_room_day with walk_fade
    "The afternoon stretches out in the particular way Sunday afternoons do, too much room,"
    "not enough reason to leave it."
    "I open WIRE on the phone."
    $ renpy.call_screen("wire_app")
    if first_day_activity == "walk_alone":
        "Five names now. Hikari at the top, where she has always been. Chef and Aya from before."
        "And at the bottom, two new ones."
    elif first_day_activity == "photo_club":
        "Five names now. Hikari at the top, where she has always been. Sim and Aya from before."
        "And at the bottom, two new ones."
    else:
        "Four names now. Hikari at the top, where she has always been. Aya from before."
        "And at the bottom, two new ones."
    "Hana: one tick out of seven. Orson: one tick out of seven."
    mc "(Two people I met yesterday are already rows in my phone. The app counts things faster than I do.)"
    "I open Hana's profile. The note says she shelves returns and never quite says anything. Underneath:"
    "one memory, that she fled a room I was sitting in."
    mc "(I didn't say anything to her. I didn't do anything. The app still counted it, because I was there."
    mc "I think that's the whole point of the thing.)"
    "Orson's note is drier: Lupin's Den, the water's on the house."
    "One memory, a wrong turn home from the library."
    mc "(A bar I walked into by accident is now a contact."
    mc "I don't know whether to be flattered or concerned.)"
    "I put the phone down. The house is quiet in the way it gets when everyone's doing their own separate"
    "Sunday."

    scene bg_kitchen_night with walk_fade
    "Dinner is earlier than usual, which Mother insists is a Sunday rule she just invented."
    mother "Eat. Tomorrow is a school day and I can already see the tired in your posture."
    father "It's one day. He survived the airport."
    hikari "The airport was four days ago."
    father "..."
    "Nobody argues with that. I eat."

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, my room is exactly where I left it, except the receipt is still on the desk,"
    "and so is the haiku handout, which I don't remember putting there."
    "I must have carried it up without deciding to."
    mc "(I tell myself it's for the quiz. It's not for the quiz."
    mc "It's because Saturday's library is still in my chest somewhere,"
    mc "and the handout is the closest thing to it I have.)"
    "I read the kigo list until the words stop meaning anything and start meaning everything,"
    "which is how I know it's time to sleep."
    "Tomorrow is Monday. The quiz is tomorrow. Midterms after that."
    "The house makes its night sounds, the fridge, the pipes, Hikari's door,"
    if first_day_activity == "walk_hikari":
        "and I lie in the dark with four names in my phone and one book I didn't take."
    else:
        "and I lie in the dark with five names in my phone and one book I didn't take."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump monday_morning


################################################################################
## MONDAY: THE QUIZ DAY
################################################################################
##
## The first full school day after the weekend. The haiku lecture runs the
## exam-preview material from Saturday's handout, and the quiz lands at the
## end of it — three questions, menu-style, scored into `monday_quiz_score`.

label monday_morning:
    # Day 6: Monday, April 13. The haiku quiz and the last built scene.
    $ set_story_day(6)

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)
    "Monday morning has a shape to it now. Alarm, shower, the good shirt,"
    "the one without the tag still in the collar."
    "Downstairs, the kitchen is doing its weekday version: quicker, louder, already behind schedule."
    scene bg_kitchen with walk_fade
    mother "Eat. You have a quiz today, yes?"
    mc "Yes. He announced it on Friday. Three questions."
    mother "Then eat like it matters."
    father "It does matter."
    if sunday_quiz_score == 3:
        hikari "He got three out of three on my quiz yesterday."
    elif sunday_quiz_score == 2:
        hikari "He got two out of three on my quiz yesterday. The one he missed, he won't miss again."
    else:
        hikari "He sat my practice quiz yesterday. It was not pretty."
    father "Your quiz."
    hikari "Same material."
    mc "(She's not wrong. That's the annoying part.)"

    scene bg_school_gate with walk_fade
    "The gate knows me now. The security guard on the morning shift nods once,"
    "which I have decided is the closest thing this university has to a welcome."
    scene bg_campus_interior with walk_fade
    "The lecture hall fills the way it did Friday, latecomers folding themselves into the back,"
    "the professor already at the podium like the bell is a suggestion."
    jump monday_lecture


label monday_lecture:
    scene bg_lecture_hall with walk_fade

    "The professor does not do a warm-up. He does not do attendance."
    "He starts mid-sentence, the way a man starts when he has already said the important part in his"
    "head."
    professor "Today we finish the unit. Kigo, the seasonal word, is not decoration. It is the poem's climate."
    professor "A haiku without one is just three lines that happen to be short."
    "He writes on the board: old pond. Stillness. Then, in a different hand: frog."
    professor "The pond is a place. The frog is a season, spring, the first warmth,"
    professor "the moment the water is warm enough to matter."
    professor "Which word is the kigo?"
    "A pause. Thirty students not breathing."
    professor "It is not a trick question. It is the easiest question I have."
    $ monday_quiz_score = 0
    $ monday_q1_correct = False
    $ monday_q2_correct = False
    $ monday_q3_correct = False
    menu:
        "frog":
            mc "Frog."
            professor "Correct. The pond tells you where. The frog tells you when."
            $ monday_q1_correct = True
            $ monday_quiz_score += 1
            $ reward_attributes_once("monday_quiz_q1", [("insight", "micro")], show="auto")
        "old pond":
            mc "Old pond."
            professor "That is the setting. The kigo is what the setting is *doing*, and a pond does nothing. A frog jumps."
            "A few students write it down anyway, which tells me they knew."
        "stillness":
            mc "Stillness."
            professor "An atmosphere, not a season. Close, but the kigo has a calendar. Stillness does not."

    professor "Second. Five-seven-five counts what?"
    menu:
        "Mora, on, not syllables.":
            mc "Mora, on, not syllables."
            professor "Correct. Japanese counts mora. English counts syllables. They are not the same ruler."
            $ monday_q2_correct = True
            $ monday_quiz_score += 1
            $ reward_attributes_once("monday_quiz_q2", [("insight", "micro")], show="auto")
        "Words.":
            mc "Words."
            professor "No. Three words can be fifteen sounds or five. Count the sounds, not the words."
        "Characters.":
            mc "Characters."
            professor "That is a property of the writing system, not the poem. The poem counts beats, on."

    professor "Last one. Attendance. Three absences means what, exactly?"
    menu:
        "You can't sit the final exam, you still attend, you just get no mark.":
            mc "You can't sit the final exam, you still attend, you just get no mark."
            professor "Correct. Precisely. The rule is arithmetic, like everything else in this course."
            $ monday_q3_correct = True
            $ monday_quiz_score += 1
            $ reward_attributes_once("monday_quiz_q3", [("insight", "micro")], show="auto")
        "You fail the class.":
            mc "You fail the class."
            professor "No. Colder than failing, you attend, you sit, you simply have no mark to show for it."
        "Nothing. It's a suggestion.":
            mc "Nothing. It's a suggestion."
            professor "The clerk says it twice for a reason."

    professor "That is the quiz. Three questions, and you have all heard them before,"
    professor "the only new thing today is that they count."
    "He collects nothing. There is no paper. The quiz was the questions themselves,"
    "and the score is whatever the department decides it is."
    "The bell does not ring so much as give up."
    scene bg_campus_interior with walk_fade

    if monday_quiz_score == 3:
        mc "(Three for three. Hikari's quiz was real training."
        mc "I should tell her, no, she'll find out, she always does.)"
        $ remember("professor", "answered all three quiz questions correctly")
    elif monday_quiz_score == 2:
        if not monday_q1_correct:
            mc "(Two out of three. The kigo question was the trick, the pond was right there and still wrong.)"
        elif not monday_q2_correct:
            mc "(Two out of three. I counted something, but I counted it in English.)"
        else:
            mc "(Two out of three. The attendance rule. The clerk says it twice and I still let it slide.)"
    else:
        mc "(One or fewer. The handout clearly needs a second reading.)"
        if sunday_quiz_score <= 1:
            mc "Hikari's 'read before I ask' was not a suggestion."
        else:
            mc "Hikari is going to have something to say about this."

    "Hikari has afternoon seminar. I have nothing until dinner,"
    "which is the first unstructured hour this week that isn't an errand."
    "I could go back to the library. I could find the reading room again and see if the girl with the"
    "badge is there. I could do neither and just walk."
    menu:
        "Walk the campus until it stops feeling like a map.":
            "I take the long way around the pond, the real pond, not the one in the poem,"
            "and let the Saturday leg muscles do the work."
            "The reading room's corridor passes on my left. The door has no sign, exactly like she said."
            "I don't go in. Whatever she left on that desk was for a Saturday. Today is Monday."
            mc "(I'm learning the shape of this place. That's what the afternoons are for.)"
        "Go back to the library and finish the handout properly.":
            "I go back to the third floor, east wing, and find the door without needing the smell of green tea"
            "this time."
            "The room is emptier than Saturday. The low tables, the blinds, the fan, all exactly as described."
            "I read the kigo list until the words stop being a list and start being a weather report."
            mc "(Somewhere in this building is a girl made of held breath. Today she is not here."
            mc "The room is just a room, and that is fine, it means she has a life somewhere that isn't this one.)"
        "Check the phone. Hikari is asking how the quiz went.":
            $ run_chat("hikari", [
                {"them": "How'd the quiz go?", "options": [
                    {"label": "\"Three for three. Your training worked.\"",
                     "send": "Three for three. Your training worked.",
                     "them": ["Good. That's the easy one out of the way.", "Don't let it go to your head. Midterms are longer."]},
                    {"label": "\"The pond was a trick.\"",
                     "send": "The pond was a trick.",
                     "them": ["It wasn't a trick. The pond is the setting. The frog is the kigo.", "Read the handout again tonight."]},
                    {"label": "\"I blacked out.\"",
                     "send": "I blacked out.",
                     "them": ["Then you should be home studying, not texting me.", "I'm telling Dad you ran away."]},
                ]},
            ])
            mc "(She knows. She always knows. The only question is whether she says it first or makes me say it.)"

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    "The house is lit the way it is on school nights, kitchen bright, living room warm,"
    "one window upstairs already dark."
    scene bg_kitchen_night with walk_fade
    "Mother has miso soup and rice ready. Father has the newspaper folded to the sports page,"
    "which means he is pretending not to listen."
    mother "How was the quiz?"
    mc "Three questions. I think I got them."
    mother "Then eat like you got them."
    if sunday_q3_correct:
        hikari "He got the attendance one right on my quiz yesterday."
    else:
        hikari "I put the attendance question on my quiz yesterday. He knows it now."
    father "Your quiz had an attendance question?"
    hikari "It was a good question."
    "The soup is hot. The rice is warm. Outside, the city does its Monday thing, trains, neon,"
    "the particular hum of a week starting."
    "I eat. I answer questions about my day that aren't questions."
    "I let the house hold me the way it does on nights like this."

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the room is mine again, the receipt on the desk, the phone face-down,"
    "the handout still open to the kigo list."
    mc "(Monday is a school day. Tuesday will be too."
    mc "The quiz is behind me, midterms after that, and somewhere in the middle of it all is a girl who"
    mc "leaves books on desks and a bartender who gives water away for free.)"
    "I close the handout. Tomorrow I will open it again."
    "The week has started. Whatever it turns into, it started."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump end_of_build


################################################################################
## END OF THE CURRENT BUILD
################################################################################
##
## Append new scenes ABOVE this label and make the new last scene jump here.
## The label itself should never need to move: it is the fallback that catches
## every build, so the player always gets a deliberate ending instead of a bare
## return to the title screen.

label end_of_build:

    stop music fadeout 2.0
    stop ambient fadeout 2.0
    scene black with Dissolve(1.5)
    call screen end_of_build_card
    return
