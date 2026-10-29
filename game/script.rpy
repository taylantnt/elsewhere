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
    def type_sound(event, interact=True, **kwargs):
        if not interact:
            return
        if event == "show_done":
            renpy.sound.play("audio/SFX/type_click.wav", loop=True)
        elif event == "slow_done":
            renpy.sound.stop()

    # A separate channel for looping place ambience, so the murmur of a room can
    # sit underneath the music track instead of fighting it for one channel.
    renpy.music.register_channel("ambient", mixer="sfx", loop=True)

    # And a channel for one-shot interface sounds: money changing hands, the
    # ticket gate snapping shut. They need their own channel because the music
    # and ambience channels are both busy, and because the typewriter click loops
    # on `sound` and would be cut off by - and would cut off - anything else.
    renpy.music.register_channel("sfx", mixer="sfx", loop=False)

    def play_sfx(path):
        renpy.sound.play(path, channel="sfx")

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

# Everything from the gate inwards is still waiting on art. Each one prints the
# room it is standing in until the real background arrives, and swapping one in
# is a single line: replace the placeholder_bg(...) call with
#     Transform("images/backgrounds/bg_campus_interior.png", ...)
# and nothing in the script below has to move.
image bg_campus_interior = Transform("images/backgrounds/bg_campus.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_department_hall = placeholder_bg("#3a3630", "OUR DEPARTMENT\nSECOND FLOOR")
image bg_student_relations = placeholder_bg("#33302c", "STUDENT RELATIONS\nOFFICE")
image bg_lecture_hall = Transform("images/backgrounds/bg_lecture_hall.png", xysize=(config.screen_width, config.screen_height), fit="cover")

image bg_train = Solid("#1C1B18")
image hospital_flash = Solid("#d9e6ee")

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

# --- CHARACTER ATTRIBUTES ---
# The three-pillar progression system. Values live in save data, while the
# definitions and thresholds live in one place below so scene code only has to
# ask for a named reward.
default character_attributes = {
    "insight": 0,
    "grace": 0,
    "nerve": 0,
}
default attribute_reward_flags = []

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
    attribute_defs = {
        "insight": {
            "name": "Insight",
            "blurb": "The power to understand.",
            "color": "#6fd8ff",
            "color_soft": "#6fd8ff55",
        },
        "grace": {
            "name": "Grace",
            "blurb": "The power to connect.",
            "color": "#8ce6d1",
            "color_soft": "#8ce6d155",
        },
        "nerve": {
            "name": "Nerve",
            "blurb": "The power to act.",
            "color": "#6f8cff",
            "color_soft": "#6f8cff55",
        },
    }

    attribute_rank_thresholds = [0, 3, 6, 10, 15]
    attribute_rank_names = [
        "Developing",
        "Emerging",
        "Capable",
        "Accomplished",
        "Exceptional",
    ]

    def attribute_name(attribute_id):
        return attribute_defs.get(attribute_id, {}).get("name", attribute_id.title())

    def attribute_blurb(attribute_id):
        return attribute_defs.get(attribute_id, {}).get("blurb", "")

    def attribute_total(attribute_id):
        return max(0, int(store.character_attributes.get(attribute_id, 0)))

    def attribute_rank(attribute_id):
        total = attribute_total(attribute_id)
        rank = 1

        for i, threshold in enumerate(attribute_rank_thresholds, start=1):
            if total >= threshold:
                rank = i

        return min(rank, len(attribute_rank_names))

    def attribute_rank_name(attribute_id):
        return attribute_rank_names[attribute_rank(attribute_id) - 1]

    def add_attribute_points(attribute_id, amount=1, show=True):
        if attribute_id not in attribute_defs:
            raise Exception("Unknown attribute id: %r" % (attribute_id,))

        amount = int(amount)

        if amount <= 0:
            return attribute_total(attribute_id)

        store.character_attributes[attribute_id] = attribute_total(attribute_id) + amount

        if show:
            # Let the choice breathe for a moment before the stat screen takes
            # over, so the reward feels like a follow-through rather than a cut.
            renpy.pause(0.45, hard=True)
            # The riser opens the animation and runs for 1.70s, which is exactly
            # as long as the stat takes to travel out of the middle. The landing
            # sound is fired by the screen itself, on a timer, so the two stay in
            # step no matter how the motion is retimed.
            play_sfx("audio/SFX/attribute_rise.wav")
            renpy.call_screen("attribute_gain_card", attribute_id=attribute_id, amount=amount)

        return store.character_attributes[attribute_id]

    def reward_attributes_once(flag, rewards):
        """Apply a one-time reward definition so a major choice cannot double-pay."""
        if flag in store.attribute_reward_flags:
            return False

        store.attribute_reward_flags.append(flag)

        for attribute_id, amount in rewards:
            add_attribute_points(attribute_id, amount=amount, show=True)

        return True


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
define chef = Character("Chef", color="#deb887", callback=type_sound)
define sim = Character("Sim", color="#add8e6", callback=type_sound)
define aya = Character("Aya", color="#dda0dd", callback=type_sound)
define hana = Character("Hana", color="#98fb98", callback=type_sound)

# Generic NPCs
define stranger = Character("Stranger", callback=type_sound)

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

image side assistant = At(Transform("images/characters/assistant.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side veteran = At(Transform("images/characters/veteran.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side security = At(Transform("images/characters/security.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side security2 = At(Transform("images/characters/security2.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side mother = At(Transform("images/characters/mother.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side father = At(Transform("images/characters/father.png", xysize=(256, 384), fit="contain"), portrait_idle)

# Hikari. She is asleep on the night he arrives and awake on the morning after,
# which makes the kitchen her first appearance on screen, so this is the first
# time her picture is needed.
image side sister = At(Transform("images/characters/sister.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side taxi_driver = At(Transform("images/characters/taxidriver.png", xysize=(256, 384), fit="contain"), portrait_idle)

# The professor already has a portrait on disk, so he uses it. Student Relations
# is still just a box with the job written on it; when the art arrives, replace
# the placeholder_portrait(...) call with
#     Transform("images/characters/clerk.png", xysize=(256, 384), fit="contain")
image side professor = At(Transform("images/characters/teacher.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side clerk = At(placeholder_portrait("#4a4038", "STUDENT\nRELATIONS"), portrait_idle)

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

# The one-time hints. Both are drawn by the same card, so the only thing each
# caller supplies is the wording. The first payment and the first item he picks
# up each get one, and neither ever runs twice.
define hint_text_money = "Make sure to check your cash in your bag, so you know you have enough for the things you need."

define hint_text_bag = "Make sure to check the items in your bag. It might be useful."

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

screen attribute_gain_card(attribute_id, amount):
    modal True

    default hiding = False

    $ current_total = attribute_total(attribute_id)
    $ current_rank = attribute_rank(attribute_id)
    $ current_rank_name = attribute_rank_name(attribute_id)
    $ current_name = attribute_name(attribute_id)
    $ current_blurb = attribute_blurb(attribute_id)
    $ active_color = attribute_defs[attribute_id]["color"]
    $ active_soft = attribute_defs[attribute_id]["color_soft"]

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
                    text "+[amount]" style "attribute_gain_plus" xalign 0.5

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
                    text "+[amount]" style "attribute_gain_plus" xalign 0.5

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
                    text "+[amount]" style "attribute_gain_plus" xalign 0.5

        # The title waits until the move has already started.
        vbox:
            at attribute_gain_title_in
            xpos gui.scale(30)
            ypos gui.scale(82)
            spacing gui.scale(-18)

            text "ATTRIBUTE" style "attribute_gain_title"
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
            text "Grace [attribute_total(\"grace\")]" xpos gui.scale(408) ypos gui.scale(162) xsize gui.scale(170) style "attribute_gain_mini" color "#f4efe6"

        if attribute_id != "insight":
            text "Insight [attribute_total(\"insight\")]" xpos gui.scale(198) ypos gui.scale(356) xsize gui.scale(180) style "attribute_gain_mini" color "#f4efe6"

        if attribute_id != "nerve":
            text "Nerve [attribute_total(\"nerve\")]" xpos gui.scale(620) ypos gui.scale(356) xsize gui.scale(180) style "attribute_gain_mini" color "#f4efe6"

        textbutton "Okay" action SetScreenVariable("hiding", True) style "notice_button" xalign 0.5 yalign 1.0 yoffset gui.scale(10) sensitive (not hiding)

    # The landing fire is on a timer rather than a second play_sfx call, so it
    # stays locked to the motion: 1.70s is the moment the stat finishes its
    # travel and settles into its orb. Retime the transforms and this beat has to
    # be moved with them.
    timer 1.70 action Play("sfx", "audio/SFX/attribute_land.wav")

    if hiding:
        timer 0.440 action Return()

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
    scene black
    play music "audio/Music/dream sequence 1 (short loop).wav" fadein 2.0
    
    "Wow... that was a long flight."
    "I think that was the longest flight of my life."
    "But... I made it. I'm finally here."
    "Japan."
    
    "It doesn’t feel real yet. The signs, the announcements, the air—it’s all so different."
    "I came here as a foreign exchange student. A fresh start in a new country."
    "Host family, a new university, a new language, a new life."
    
    # The wallet, established before he has spent a single yen of it.
    "And thirty thousand yen, in cash, folded into the back of my wallet."
    "That's all of it. Every shift I worked, every coin I saved, everything I own in the world."
    "Thirty thousand yen to start a whole new life."
    "It's not enough. It's nowhere near enough."
    "But it's more than nothing. It gets me to my host family and it buys me one meal."
    "After that I'll have to figure something out."
    "I have to."
    
    # Foreshadowing glitch - the first crack in the simulation
    show hospital_flash onlayer overlay at truecenter:
        alpha 0.0
        linear 0.1 alpha 0.3
        linear 0.1 alpha 0.0
    
    "Test initiating..."
    
    "I should focus on what’s ahead."
    "A new home. A host family. A whole country waiting to be explored."
    
    stop music fadeout 1.0
    jump airport_arrival

label airport_arrival:
    scene bg_airport

    # The terminal: a calm track riding over the murmur of the crowd. The ambience
    # is on its own channel so it layers underneath the music, and both loop until
    # he leaves the building (see label end_airport).
    play music "audio/Music/airportscene.mp3" fadein 1.5
    play ambient "audio/SFX/airport.ogg" fadein 1.5

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
    mc "(Maybe I should ask someone who isn't radiating pure stress.)"
    jump airport_exploration

label talk_timid_man:
    stranger "話しかけないでくれ！"
    stranger "忙しくて雑談してる暇はないんだ。"
    stranger "どいてくれ、今は大事な用事がある。"
    mc "(What...? I have no idea what he just said.)"
    mc "(I guess he doesn't want to talk...)"
    $ talked_to_man1 = True
    jump airport_exploration

label talk_cheerful_woman:
    stranger "こんにちは！日本へようこそ！"
    stranger "それでは、失礼いします！幸せになりますように！"
    mc "(Uhh… she said something about… sushi?)"
    mc "(Wait. Did she just recommend a sushi restaurant?)"
    mc "(Or was that a blessing for my sushi-related future?)"
    mc "(Well, she's smiling, so I'll just smile back and nod.)"
    $ talked_to_npc2 = True
    jump airport_exploration

label talk_assistant:
    if not (talked_to_security and talked_to_man1 and talked_to_npc2):
        assistant "いらっしゃいませ～。ようこそ。"
        jump airport_exploration
    
    assistant "いらっしゃいませ～。ようこそ。"
    mc "Hi! Um… Can you help me?"
    assistant "えっ…えいご…すこしだけ…"
    assistant "えいごのスタッフは…いまやすみ…"
    assistant "*muttering to herself* English staff... break time now... しょうがないね。"
    mc "...Okay... Umm, I need to find this place."
    assistant "アドレス？うーん… show... me?"
    
    menu:
        "Show address on phone":
            mc "*Shows address on phone.* Can you tell me how to go here?"
            assistant "あー、これはね…でんしゃ？トレイン？"
            assistant "うえのえき…から…えっと…ちょっとまってね。"
            assistant "*Takes out a japanese map full of arrows and kanji.*"
            $ has_pamphlet = True
            $ add_item("pamphlet")
            mc "Uh… this is... kind of amazing but also terrifying."
            assistant "No problem, Good Luck! がんばってください！"
            mc "...Thanks. I'll try my best."
        "Nevermind":
            mc "Nevermind, thanks anyway."
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
    veteran "You’ve got two ways to get there. Train is cheaper, but a bit tricky. Taxi’s simple, but pricey. Want details?"
    
    menu:
        "Tell me about the train":
            veteran "Alright, here's the deal. First, buy a ticket before going in. You can’t enter the platform without it."
            veteran "Then wait for the express train. Not the local one! Unless you enjoy long rides and sore feet."
            veteran "Follow the signs for the Keisei Line. It'll get you there in about 45 minutes."
            jump taxi_choice
        "No, I'm good. Thanks!":
            jump end_airport

label taxi_choice:
    veteran "Want me to explain the taxi option too, or are you ready to go?"
    menu:
        "Tell me about the taxi":
            veteran "Just head outside and find the taxi stand. There’s usually a line, so be patient."
            veteran "It might cost around ¥18,000, maybe more if traffic’s bad. But it’s the easiest route."
            veteran "Just show the driver your pamphlet. They’ll handle the rest."
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
    mc "...Thanks. I'll try my best.. Hopefully I can get there."

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
        "Take a taxi (about 18,000 Yen)":
            jump taxi_warning
        "Take the train (much cheaper)":
            $ travel_method = "train"
            $ reward_attributes_once("travel_route_attribute", [("insight", 1)])
            jump train_station


label taxi_warning:
    mc "(A taxi would take me all the way to the door.)"
    mc "(No transfers. No signs I can't read. No standing on the wrong platform in the dark.)"
    mc "(But eighteen thousand yen. That's more than half of everything I own.)"
    mc "(If I take the train, that money buys me food for a fortnight.)"
    mc "(...but only if I actually get there.)"
    mc "(So. Spend it and arrive safe, or risk getting lost and keep the money.)"

    menu:
        "Take the taxi anyway. Arrive safe.":
            $ travel_method = "taxi"
            $ reward_attributes_once("travel_route_attribute", [("nerve", 1)])
            jump taxi_stand
        "Never mind. I'll take the train.":
            $ travel_method = "train"
            $ reward_attributes_once("travel_route_attribute", [("insight", 1)])
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
    taxi_driver "中野3丁目ですね。かしこまりました。遠いけど、大丈夫？"
    mc "(...I understood one word of that and it was 中野.)"
    mc "Ah, um... 中野3丁目... please?"
    taxi_driver "*laughs* Okay, okay. 中野3丁目. No problem."
    mc "(He laughed. I'm choosing to believe that was friendly.)"

    "The meter starts ticking and we pull away from the kerb."
    mc "(No ticket. No button. No card. It just... starts.)"
    mc "(Airport to 中野3丁目. I'd guessed about eighteen thousand for that.)"
    mc "(A confident guess, made by a man who has been awake for twenty hours.)"
    mc "(...Maybe it'll be less. Hopefully it'll be less.)"

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

    menu:
        "Just walk through the gate":
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
        "Press the 320 Yen Ticket button":
            if has_item("ticket_320"):
                mc "(I already purchased this ticket. It's the wrong one.)"
                jump ticket_machine
            $ buy_item(320, "ticket_320")
            "A ticket drops into the tray with a soft clack."
            mc "(That was satisfying. That was also very cheap.)"
            mc "(...and it goes somewhere that is extremely not 中野.)"
            mc "(Put it down. Try again.)"
            jump ticket_machine

        "Press the 800 Yen Ticket button":
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

        "Give up and ask a station attendant":
            "I catch the eye of a woman in a station uniform and hold the pamphlet up."
            mc "Sumimasen... 中野3丁目?"
            "She takes the pamphlet, reads it, and presses the button for me without a word."
            "¥1,300. A ticket slides out."
            mc "(That took her four seconds. It took me four minutes.)"
            mc "Arigatou gozaimasu."
            "She nods, already walking away."
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
        "Take the train on the sign with eight stations (express)":
            $ boarded_shinkansen = True
            jump train_board
        "Take the train on the sign with twenty-three stations (local)":
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
        mc "I can't believe I'm actually here. On the express, heading toward my new life."
        mc "The station was terrifying, but it worked out. I bought a ticket. I found the right train."
        mc "I wonder what my host family will be like. We've exchanged emails. I've seen their photos. But meeting them in person is different."
        mc "What if I can't communicate properly? What if they were expecting someone better?"
        mc "Let me practise. Watashi namae... no, that's wrong."
        mc "Watashino namae wa... yes. That's the one. I'm glad I studied a little before I came."
        mc "But there is so much I don't know. How will Japan really be? Like the films? Like the photographs?"
        mc "And school. I hope I can make friends. I hope I'm not just the foreign student."
        mc "What if I make cultural mistakes? What if I can't keep up in class?"
        mc "*Takes a deep breath.* No. I can't think like that."
        mc "I worked for this. The language study, the paperwork, saving every yen I could get my hands on."
        mc "My family thought I was mad, coming here alone. Maybe I was."
        mc "But I want to see a completely different world. Learn about it. Learn about myself."
        mc "*Looking at the passing scenery.* Everything is different already. The roofs. The signs. The little gardens squeezed between the houses."
        mc "First, though, I need to make a good impression. They're taking a real risk, letting a stranger into their home."
        mc "I hope I can show them I'm grateful."
        mc "*Yawns.* All this thinking about my new life has made me so tired... My eyelids feel heavy..."
    else:
        "*Settling into the seat as the carriage fills up around me.*"
        mc "Well. This is it. I'm finally on my way to my host family."
        mc "I made it onto the train. Despite everything at the station, it worked out."
        mc "The local feels more... honest, somehow. I get to see the Japan people actually live in."
        mc "The station was stressful, but I figured it out on my own. Maybe I'm more ready for this than I thought."
        mc "My host family. I wonder if they're nervous about meeting me too."
        mc "We've exchanged so many emails, and I've seen their photographs. But face to face is different."
        mc "I should practise my introduction again. Watashi namae... no, that's wrong."
        mc "Watashino namae wa... that's better. I'm glad I studied some Japanese before coming."
        mc "But there's still so much I don't know. What will daily life actually be like?"
        mc "Will I be able to adapt? To the customs? The food? The expectations?"
        mc "*Looking out at the suburban landscape.* This route shows me a different side of Japan."
        mc "Not just the big cities. The neighbourhoods where people actually live."
        mc "I hope I can become part of that. Not a tourist. Someone who really experiences this."
        mc "School, too. I hope I can make friends and not just be the foreign student."
        mc "*Checking the time.* Almost there. I can feel the butterflies."
        mc "This is what I've been working toward for so long. The late nights. The saving. All of it."
        mc "My family thinks I'm crazy for doing this alone. But I know it's what I need to do."
        mc "*Yawns.* All this thinking about my new life has made me so tired... My eyelids feel heavy..."

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
    # Deliberately silent. After an airport and a train, the quiet of a residential
    # street is the point. Add `play music "audio/Music/..." fadein 2.0` here if you
    # want something under it.

    if travel_method == "taxi":
        # The ride and the fare already happened in label taxi_stand, so this is
        # just him standing on the street with the taxi pulling away.
        "*Steps out into a street far too narrow to be sensible.*"
        "Barely any pavement, a gutter, and somebody's bicycle leaning against a wall."
        "The taxi pulls away, and then it's just me and the crickets."
    elif boarded_shinkansen:
        "The walk from the station is short, and the neighbourhood is almost entirely dark."
        "Low houses one behind the other, each with a tiny garden and a bicycle leaning against the wall."
        mc "Managed to catch the express and transfer at the right station. Not bad for my first time navigating solo."
    else:
        "The walk from the station takes forever."
        mc "Man... that local train stopped at every single station. Took forever to get here."
        mc "It's already pretty late. I hope I'm not waking anyone up..."

    "I stand in front of a narrow two-storey house with one light on behind the curtains."
    mc "Still can't believe I'm actually here. My home. At least for the next year."
    mc "Alright. What was the proper greeting again? Konnichiwa? That works, right?"
    mc "Okay. Let's do this."
    "*Reaches for the doorbell.*"
    # The chime lands at the same moment as the line describing it, so the sound
    # and the text hit together instead of a beat apart.
    $ play_sfx("audio/SFX/doorbell.mp3")
    "*The chime is much louder than I expected. It bounces off the houses opposite.*"
    mc "(Oh no. Everyone on this street heard that.)"

    if arrived_late:
        # Late arrival, which is the train. Only the mother is still up, and the
        # whole scene is quiet.
        "The door opens a crack, then all the way, carefully."
        mother "Oh! You made it."
        mother "Thank goodness. We thought you'd got lost somewhere between the airport and here."
        mother "Come in, come in. Quickly. It's cold out, and everyone else is asleep."
        "*She holds the door and waves me in with her whole arm.*"
        mc "Sorry. The train took much longer than I thought, and I..."
        mother "It's alright. Truly. You're here now, that's all that matters."
        mother "Shoes off here. Then straight up the stairs, quietly."

        scene bg_home_night with walk_fade

        mother "My husband is already asleep, so you'll meet him properly in the morning. I'm Miharu Nagai."
        mc "Ah. Konnichiwa. I'm..."
        mother "I know who you are, [player_name]. We've been waiting months for you."
        mother "Hikari is the one who wrote all those emails. She's asleep too. She doesn't even know you've arrived, so she'll get a surprise at breakfast."
        mc "(Hikari. The one who answered every single one of my questions about the university.)"
        mc "(I'll thank her tomorrow. When my brain works.)"
        mother "Come. Your room is at the top of the stairs."
    else:
        # Early arrival, which is the taxi. It went straight to the door, so he is
        # here sooner than the family expected and the whole house is still up.
        "The door opens before I've finished panicking."
        mother "Oh! You're earlier than I expected!"
        mother "We said an hour, maybe two, with the traffic. Not this early."
        mother "You took a taxi, didn't you. Sensible. I'm so glad you made it. Welcome!"
        mother "Come on in. You must be exhausted."
        "*She has my bag out of my hands before I manage to say anything.*"

        scene bg_home_night with walk_fade

        mother "Welcome again, [player_name]. I'm Miharu Nagai."
        father "And I'm Tetsuo Nagai. So you finally found our home, [player_name]. Miharu told us you'd be arriving today."
        father "We keep things the proper way in this house. None of that new gadget nonsense. A good letter, or a proper face-to-face talk, works best."
        mother "Tetsuo still uses the same flip phone he bought ten years ago. But don't worry, I'm happy to help you with anything you need."
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
    pause 3.0

    scene bg_room_night with stair_fade

    # The room, and the boxes that arrived before he did.
    "The stairs creak under both of us. She apologises for the creaking, which is somehow more embarrassing than the creaking."
    mother "Well, it's not a lot, but this will be your room for the year."
    mother "Hikari's room is next door, so please try not to make too much noise. She's a light sleeper."
    mother "Oh, and the things you shipped over arrived yesterday. They're still down by the door."
    mother "Would you help your old host mother carry them up?"
    mc "Of course. Let me help."

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

        cards = []
        for i, text in enumerate(real):
            cards.append({"id": "real%d" % i, "text": text, "real": True})
        for i, text in enumerate(fake):
            cards.append({"id": "fake%d" % i, "text": text, "real": False})

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
# Only the card that was just picked gets one of these, and every one of them is
# a bare statement rather than a call with arguments: a screen rebuilds a
# displayable whenever its `at` changes, so an animated transform built fresh on
# each render would restart forever instead of settling.
#
# Cards lift a little under the cursor, so the board feels like something you are
# handling rather than a form you are filling in.
transform dream_card_hover:
    zoom 1.0
    on idle:
        ease 0.16 zoom 1.0
    on hover:
        ease 0.16 zoom 1.045

# A memory that was his: the card punches out and comes back, so the eye follows
# the pick instead of having to notice a colour change.
transform dream_card_found:
    zoom 1.0
    ease 0.10 zoom 1.075
    ease 0.22 zoom 1.0

# A memory that was planted: the card flinches, like something caught moving.
transform dream_card_missed:
    xoffset 0
    linear 0.045 xoffset -11
    linear 0.045 xoffset 10
    linear 0.045 xoffset -8
    linear 0.045 xoffset 6
    linear 0.045 xoffset -3
    linear 0.045 xoffset 0

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


# The sorting game. The screen only draws what the label tells it is true, so the
# label can interrupt the dream with a voice from the other room between picks,
# which is the whole reason this is not a single self-contained screen.
#
# The board answers the touch itself rather than waiting for the label to come
# back around. A click is a hard commit: the card reacts and its sound plays at
# that instant, the rest of the board goes inert, and only then is the pick handed
# back. That is why the sound lives in here instead of in the label.
screen dream_reconstruct(cards, found, missed):

    modal True
    zorder 100

    add Solid("#04050a")

    # Interference over the board itself, kept lighter than the full-screen
    # version: it should feel like the picture is unwell, not make the words hard
    # to read.
    default bars = dream_static_bars(3, 0.16, False)
    timer 0.09 repeat True action SetScreenVariable("bars", dream_static_bars(3, 0.16, False))

    # Empty until the player commits to a card, then the id of that card. The
    # board reads it so the touched card can answer before the pick is handed back.
    default picked = ""
    default pending = None

    $ total_real = len([c for c in cards if c["real"]])

    vbox:
        xalign 0.5
        ypos 48
        spacing 8

        text "PUT THE DAY BACK" at dream_title_glitch:
            xalign 0.5
            size 34
            color "#8fd8ff"
            outlines []

        text "Four of these happened today. Touch the four that are yours.":
            xalign 0.5
            size 19
            color "#6b7a8c"
            outlines []

        text "[len(found)] / [total_real] recovered":
            xalign 0.5
            size 17
            color ("#86e3ac" if len(found) < total_real else "#c8f0d8")
            outlines []

    vbox:
        xalign 0.5
        yalign 0.58
        spacing 18

        for row in range(0, len(cards), 3):

            hbox:
                spacing 18

                for c in cards[row:row + 3]:

                    $ is_found = c["id"] in found
                    $ is_missed = c["id"] in missed
                    $ is_picked = c["id"] == picked
                    # The card answers the moment it is touched, so the board has
                    # to show the result before the label has been told about it.
                    $ reveal = is_picked and c["real"]
                    $ wrong = is_picked and not c["real"]
                    $ card_at = (dream_card_found if c["real"] else dream_card_missed) if is_picked else dream_card_hover

                    button:
                        xysize (300, 150)
                        at card_at
                        background Solid("#14301f" if (is_found or reveal) else ("#301016" if (is_missed or wrong) else "#11151c"))
                        hover_background Solid("#1d2531")
                        sensitive (not is_found and not is_missed and picked == "")
                        action [
                            Play("sfx", "audio/SFX/memory_restore.wav" if c["real"] else "audio/SFX/memory_deviation.wav"),
                            SetScreenVariable("picked", c["id"]),
                            SetScreenVariable("pending", c),
                        ]

                        text c["text"]:
                            xalign 0.5
                            yalign 0.5
                            xmaximum 250
                            text_align 0.5
                            size 19
                            line_spacing 2
                            color ("#86e3ac" if (is_found or reveal) else ("#ff9aa2" if (is_missed or wrong) else "#e8e2d6"))

    # Let the card finish its reaction before the label takes over. Timed, so a
    # committed pick is never something the player has to click through twice.
    if pending:
        timer 0.42 action Return(pending)


label dream_sequence:

    # He is asleep. The house is quiet and the dark behind his eyes is not.
    stop music fadeout 2.0
    pause 1.5

    # The dream gets its own bed of sound. It is a loop, so nothing has to be
    # restarted while the sequence plays out.
    play music "audio/Music/dream sequence 1 (short loop).wav" fadein 3.0

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

    # The game. Four of the cards are the day he actually had; the rest are what
    # the room would prefer he remembered. Nothing here can be lost, only looked
    # at, so there is no fail state: the pressure comes from the picture coming
    # apart around him and from what the two voices say while it does.
    $ dream_cards = build_dream_cards(travel_method, boarded_shinkansen)
    $ dream_found = []
    $ dream_missed = []
    $ dream_target = len([c for c in dream_cards if c["real"]])

    while len(dream_found) < dream_target:

        call screen dream_reconstruct(dream_cards, dream_found, dream_missed)
        $ dream_pick = _return

        if dream_pick["real"]:

            # The sound for this already played inside the screen, at the moment
            # the card was touched, so it lands on the click instead of after the
            # line below has been read.
            $ dream_found.append(dream_pick["id"])

            if len(dream_found) == 1:
                "That one is mine. That one happened."
            elif len(dream_found) == 2:
                "That one too. I can still smell it."
            elif len(dream_found) == 3:
                "Three. That one happened, I'm certain of it."
            else:
                "And that one. That is all four."

        else:

            $ dream_missed.append(dream_pick["id"])
            show screen dream_static

            if len(dream_missed) == 1:
                "He is reaching for something that was never in the scene."
                "Log the deviation and leave it. Do not correct him."
            else:
                "Should we bring him up?"
                "No. Let him keep looking. It is more useful when he finds it himself."

            hide screen dream_static

    window hide
    "Four of them. All four are mine, and they are back where they go."
    "The airport, the ride, the street, the bell. That was today."
    "That is all of it. That is everything that happened."

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
    # tea_under_the_canopy is a warm, unhurried track and it is the closest thing
    # in the library to a kitchen in the morning. Easy to swap for something else
    # once the rest of the house has a soundtrack.
    scene bg_room_day with Dissolve(2.0)
    play music "audio/Music/(Hanami? Nature setting?) tea_under_the_canopy.mp3" fadein 2.0

    "Light in a room I still don't recognise. It takes me three seconds to remember where I am."
    "Japan. The house. The room with the boxes in it."
    mc "My first morning."
    "The dream is already going soft at the edges, the way dreams do."
    "Something about the airport. A road with no end on it. Two voices talking over me like I wasn't in the room."
    mc "What was that about?"
    "I try to hold onto it and it comes apart like wet paper."

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
        father "It is also the correct way, when you land that late and you are carrying things. Know what things cost here and you will be fine."
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
    mother "You are being a schedule."
    "Hikari puts a bowl down in front of me without being asked and sits opposite, elbows on the table, which Tetsuo visibly decides not to mention."
    hikari "Ignore him. He does this to everybody. He did it to me, and I have lived here my whole life."
    hikari "Okay. University. Same department, same building, which was completely not arranged."
    mc "Was it arranged?"
    hikari "It was arranged."
    hikari "Everyone has been asking about you since April, by the way. There is a pool."
    mc "A pool."
    hikari "On whether you'd actually turn up. I'm not telling you what I bet."

    # Tetsuo's one piece of advice for the year, and it is also the thesis of his
    # character: keep to the routine and nothing bad can happen.
    father "The school will have rules. They will all be written down, and they will all be simple."
    father "Follow them and nothing will happen to you. That is all a school is."
    mc "(He says it like a fact about schools. It lands like a fact about me.)"

    mother "Don't listen to him, dear. The teachers are kind. The other students will be curious for a week and then they will be ordinary."
    mother "If anything at all happens, you call me. You still have the number I wrote out for you?"
    mc "I have it."
    mother "You have it. Good."
    mc "(She asks the way people ask when they already know the answer.)"

    hikari "Right. Go and grab your bag. I will be waiting for you here."
    mc "Wait a minute.. Are we leaving already?"

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

    "And then the kitchen is loud and ordinary, and I am standing in the middle of it with a bowl in my hands and no idea what to do with either."
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

    # The rule, and the reason for it, because Hikari never gives a rule without a
    # reason. The mosquitoes are not a metaphor.
    hikari "Rule one. You close the screen behind you. Every single time. It isn't about manners."
    mc "Then what is it about?"
    hikari "Mosquitoes. Moths. And one summer I left it open for about ten seconds and a cicada got into my room at two in the morning and screamed until dawn."
    mc "Screamed."
    hikari "It is not a small insect. It's a loud bird that got lost."
    mc "(That is the most serious she has been all morning, and it was about a bug.)"

    # And then he gets it wrong, in the ordinary way that everybody gets it wrong,
    # which is the point: he isn't being tested, he's being taught.
    "I go out first, because that is what you do when somebody is showing you the way out of their own house."
    "The screen slides easily. I pull it shut with one hand on the middle, the way I'd close any other door, and it bounces off the frame and hangs there, open by a hand's width."
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

    scene bg_school_gate with walk_fade

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
    "She says it the way she said the umbrella on the way out. Like it is obvious, and like she has already decided to be patient with me about it."
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
    mc "(From the street it was one building behind a wall. That is honestly all I could see. A wall, a roof, and about four metres of it.)"
    mc "(Inside, it keeps going.)"
    "A courtyard, and then another one behind it, and a covered walkway between the two, and above the walkway a second floor of windows, and above that a third."
    "There are trees along the path, big ones, old enough that somebody planted them on purpose a long time ago and then waited."
    "People cross the courtyard in every direction at once and none of them collide, which means there is an order to it that I cannot see yet."
    mc "(It's a different world in here. That isn't a figure of speech.)"
    mc "(I watched the city disappear behind a wall in three steps.)"
    hikari "You've stopped walking."
    mc "I'm looking."
    hikari "Everybody does that. First years, exchange students, and once a visiting professor, which was funnier than it sounds."
    hikari "Come on. The good part is the other direction."

    "She walks fast, which I am starting to understand is just how everyone here walks, and she points at things the way a person points at their own house."
    hikari "Library. Open until ten. You will not care about that in September and you will care about it very much in December."
    hikari "That is the cafeteria, and that is the other cafeteria, and there is a reason there are two, and the reason is terrible."
    hikari "Past those, the gym. Nobody uses the gym."
    mc "Then why is there a gym?"
    hikari "Because there was a building here before there was a university. The rest grew around it. Stick close at the crossing."
    mc "(Stone next to glass next to concrete, and the concrete is the oldest of the three. Nobody designed this place in one go. It happened to it.)"

    "She turns down a path and the courtyard narrows into a plain grey building with a set of steps and too many doors."
    hikari "And this is ours."
    mc "Ours."
    hikari "You and me. Same department, so same building, so for the next four years that door is the one you will get tired of."
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
    "Posters on both walls. A reading group, a film screening, a room for rent, three rooms for rent, a lost cat that is almost certainly not still lost."
    hikari "Which one is yours?"
    mc "Sorry?"
    hikari "The posters. Everybody picks one on the first day. That is your department. The wall decides it."
    mc "(There is no way to answer that without guessing wrong, so I don't.)"

    "She stops at the far end, in front of a set of double doors, and reads a timetable taped to the glass."
    hikari "Right. That's your first lecture. History, four floors up, and we have about ten minutes."
    mc "We're going up?"
    hikari "We're not going up. Not yet. You have to see the office first."
    mc "What office?"
    hikari "The office. Everybody has to do the office. It is the price of being a person here."


################################################################################
## ACT THREE, SEVENTH BEAT: STUDENT RELATIONS
################################################################################
##
## The scene that explains the rules of the game to the player without once
## saying so. Attendance is the spine of it, because attendance is the thing the
## simulation will be measuring him on, and he does not know that yet.

label student_relations:

    scene bg_student_relations with walk_fade

    "The office smells like green tea and warm photocopier."
    "A counter, a ticketing machine with a queue number on it, and behind the counter a woman who has clearly been doing this for twenty years and has the calm of someone who has seen every version of confused there is."
    clerk "Ah. You'll be the new one. [player_name]."
    mc "Yes. How did you..."
    clerk "Your file is open on my screen. It has been open since eight."
    hikari "Told you."
    clerk "Sit, both of you. This is not a test, and it is the only time anyone here will explain this slowly."

    clerk "First, your gakuseishou. Student card. You need it for everything, and you will lose it, so you keep it in the same pocket every single day."
    mc "(Gakuseishou. I got that one from the gakusei. I have heard gakusei about two hundred times since I landed.)"

    "I sit. Hikari sits beside me and folds her arms like someone settling in to watch a play she has already seen."
    clerk "Attendance. At most universities it is a suggestion. Here you will find that it is not."
    clerk "In every class you are marked present, absent, or late. Sit down before the bell and you are present. Walk in after it and you are late."
    mc "Late. That's all it is?"
    clerk "Three lates make one absence. Three absences in a course and you are not allowed to sit the final exam. You still attend. You simply do not get the mark."
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
    clerk "You are adults now. Nobody makes you join anything and nobody makes you stay, and that is the whole difference from where you came from."
    clerk "There is a reading circle. It is four people and a great deal of silence."
    clerk "There are language courses. Japanese, for the exchange students. The ones who take them seriously are the ones who stop needing me to read their post."
    clerk "There is a photography circle. It argues constantly and takes good photographs anyway."
    clerk "There is a hiking group that will try very hard to recruit you at the gate on Thursday."
    hikari "They got me."
    mc "(I believe her.)"
    clerk "And a number of other things under the gym, which you will find on your own and which I am not responsible for."

    mc "Thank you. Really."
    clerk "You are welcome. Come back when something breaks. Something always breaks."
    clerk "Now go. History started four minutes ago."
    mc "Four minutes?"
    clerk "The building is not small. Off you go."


################################################################################
## ACT THREE, EIGHTH BEAT: THE FIRST LECTURE
################################################################################
##
## The strict professor, and the first rule in Japan that he breaks without ever
## knowing it existed. The lecture topic is chosen on purpose: a country getting
## smaller is the premise of the whole game, and he hears it as a history lesson.

label first_class:

    scene bg_lecture_hall with walk_fade
    stop music fadeout 3.0

    "Four floors, and the stairs are exactly as bad as she said, and the door at the top is heavy and it opens inwards."
    "Forty people look up at once."
    "At the front, a man in a grey cardigan stands half turned to a blackboard that is already covered in dates. He does not turn around. He finishes the word he is writing, and then he turns around."
    professor "You are late."
    mc "I know. I'm the new one."
    hikari "Don't."
    "She has my sleeve and she is pulling me down into the nearest empty row before I finish the sentence."
    hikari "Don't answer him. Sit down. Say sorry and sit down."
    professor "I do not care who you are."
    professor "I asked who you are. I withdraw the question. It does not matter."
    professor "Sit. Come to me when the class ends."
    "Then he says something short and flat in Japanese, to the board rather than to me, and the room absorbs it the way a room absorbs weather."
    mc "(Not one word of that was for me. I hope.)"

    "We sit. Somewhere behind us a chair drags and nobody looks at us, which is somehow worse than if they had."
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

    "I walk to the front. It is a long walk, and the room empties around me the whole way, and it is emptier when I get there."
    mc "Professor. I wanted to introduce myself properly. I'm [player_name]. I'm the exchange student."
    professor "I know what you are. I read your file. That is not what this is about."
    professor "This is about the clock."
    professor "You believe you were on time. You were barely late. Arrive at the bell, sit between the bell and my first word, and you have lost the first word. Do that three times and you have lost the class."
    professor "If it happens again there will be consequences. I do not say that as a threat. It is a description."
    mc "I'm sorry. I don't think I understand what I did wrong."
    professor "You were on time."
    mc "..."
    professor "Coming on time is late."
    professor "You are seated, ready, notebook open, pen out, five minutes before the class begins. If you are still doing any of that after the bell, you are late."
    "I open my mouth to say something sensible and find that I do not have anything sensible."
    mc "(My whole life, on time has meant on time.)"
    mc "(He just told me that on time is late, and he was not joking, and not one person in that room would have disagreed with him.)"
    mc "(That is the rule that is going to take me the longest.)"
    professor "Go."
    "He turns back to the board before I have moved, which is its own kind of dismissal."

    "At the door Hikari is waiting with her arms folded, watching the corridor the way a person counts something."
    hikari "Well?"
    mc "I think I just got in trouble for being on time."
    hikari "You did."
    mc "And that went better than expected?"
    hikari "It went better than expected."
    mc "How?"
    hikari "Because you didn't argue with him. Everybody argues with him. It's the first thing everyone does, and then it is five minutes of shouting and a term on his list."
    mc "There's a list."
    hikari "There's always a list."
    mc "(She is cheerful about this as well. I am starting to think cheerful is just how she carries things.)"
    hikari "You're fine. Honestly. That was practically a welcome."
    mc "Hikari. Why was nobody else late?"
    hikari "Because nobody is late. By Friday you'll be sitting in there at eight fifty-five with everyone else, and it will feel like the most normal thing in the world."
    mc "(I don't think it will.)"
    mc "(But I'm standing in a corridor four floors above a courtyard that swallowed a city, in a building I get to keep for four years, and I have survived my first hour.)"
    mc "(Small victories. That's what today has been.)"
    hikari "Come on. I'm hungry, and I know a bad cafeteria and a worse one."
    mc "You said there were two."
    hikari "There are two."

    window hide
    scene black with Dissolve(2.5)
    stop music fadeout 2.0
    return
