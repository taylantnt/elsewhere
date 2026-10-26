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
image bg_airport = Transform("images/backgrounds/airport.png", xysize=(config.screen_width, config.screen_height), fit="cover")

# Every scene below is still waiting for its background.
image bg_taxi_stand = placeholder_bg("#101014", "TAXI STAND BACKGROUND")
image bg_taxi_interior = placeholder_bg("#0c0c11", "INSIDE TAXI")
image bg_station = placeholder_bg("#14161a", "TRAIN STATION")
image bg_platform = placeholder_bg("#171b20", "NEXT PLATFORM")
image bg_train_interior = placeholder_bg("#1a1815", "INSIDE TRAIN")
image bg_home_exterior = placeholder_bg("#0d0c10", "OUTSIDE THE HOUSE")
image bg_home = placeholder_bg("#1C1B18", "INSIDE THE HOUSE")
image bg_room = placeholder_bg("#151310", "MY ROOM")

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
        return True

    def add_item(item):
        if item not in store.inventory:
            store.inventory.append(item)
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
            "desc": "A folded map covered in arrows and kanji. I can't read it, but other people can.",
            "usable": True,
        },

        "ticket_320": {
            "name": "¥320 Ticket",
            "icon": "images/ui/ticket.png",
            "desc": "I purchased the wrong ticket, so this cannot be used.",
            "usable": False,
        },

        "ticket_800": {
            "name": "¥800 Ticket",
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
define mc = Character("Me", callback=type_sound)
define hikari = Character("Hikari", color="#ffb6c1", callback=type_sound) 
define orson = Character("Orson", color="#a9a9a9", callback=type_sound)
define chef = Character("Chef", color="#deb887", callback=type_sound)
define sim = Character("Sim", color="#add8e6", callback=type_sound)
define aya = Character("Aya", color="#dda0dd", callback=type_sound)
define hana = Character("Hana", color="#98fb98", callback=type_sound)

# Generic NPCs
define stranger = Character("Stranger", callback=type_sound)
define security = Character("Security", callback=type_sound, image="security")

# The driver who takes him home if he picks the taxi. No picture drawn yet, so he
# speaks without one, which is fine.
define taxi_driver = Character("Taxi Driver", callback=type_sound)

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
transform portrait_idle:
    subpixel True
    yoffset 0
    ease 1.6 yoffset 4
    ease 1.6 yoffset 0
    repeat

# A quicker, shallower version of the same motion, used while speaking.
transform portrait_talk:
    subpixel True
    yoffset 0
    ease 0.11 yoffset 6
    ease 0.11 yoffset 0
    repeat

image side assistant = At(Transform("images/characters/assistant.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side veteran = At(Transform("images/characters/veteran.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side security = At(Transform("images/characters/security.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side mother = At(Transform("images/characters/mother.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side father = At(Transform("images/characters/father.png", xysize=(256, 384), fit="contain"), portrait_idle)

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

# --- START LABEL ---
label start:
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
    "Host family, new school, new language, new life."
    
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
    
    doctor "Subject assimilation test initiating..."
    
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
    security "ちょっと、下がってください。"
    mc "(Huh? I'm just trying to ask something...)"
    security "業務中です。話しかけないでください。"
    $ talked_to_security = True
    mc "(Did I do something wrong? I just showed my smartphone to him...)"
    security "……"
    mc "(He didn’t even *look* at it... Is this guy part robot or something?)"
    mc "(Okay... maybe I should ask someone who isn't radiating pure stress.)"
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
    stranger "こんにちは！初めてお会いしますね！"
    stranger "日本へようこそ！楽しい滞在になりますように！"
    stranger "もし道に迷ったら、遠慮なく聞いてくださいね！"
    mc "(Uhh… she said something about… sushi?)"
    mc "(Or maybe she thinks I look like someone she knows?)"
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
    veteran "Let me have a look at that pamphlet. These things are more puzzle than guide, huh?"
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
    mc "...Thanks. I'll try my best."

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
    mc "(The veteran said there were two ways. Cheap and confusing, or simple and expensive.)"

    menu:
        "Take a taxi (about ¥18,000)":
            jump taxi_warning
        "Take the train (much cheaper)":
            $ travel_method = "train"
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
            jump taxi_stand
        "Never mind. I'll take the train.":
            $ travel_method = "train"
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

    taxi_driver "お客さん、どちらまで？"
    mc "(That's my cue.)"
    "*Hands the pamphlet over the seat.*"
    taxi_driver "中野3丁目ね。わかった。遠いけど、大丈夫？"
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
    scene bg_taxi_interior with Dissolve(1.5)

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
    $ play_sfx("audio/SFX/gate.wav")
    "The flaps snap shut hard, right across my shins, and a buzzer goes off above my head loud enough to turn three heads." with gate_shake
    mc "WHOAH!"
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
        "Press the ¥320 button":
            if has_item("ticket_320"):
                mc "(I already purchased this ticket. It's the wrong one.)"
                jump ticket_machine
            $ buy_item(320, "ticket_320")
            "A ticket drops into the tray with a soft clack."
            mc "(That was satisfying. That was also very cheap.)"
            mc "(...and it goes somewhere that is extremely not 中野.)"
            mc "(Put it down. Try again.)"
            jump ticket_machine

        "Press the ¥800 button":
            if has_item("ticket_800"):
                mc "(I already purchased this ticket. It's the wrong one.)"
                jump ticket_machine
            $ buy_item(800, "ticket_800")
            "A ticket drops into the tray with a soft clack."
            mc "(800. That's the number from the pamphlet.)"
            mc "(That has to be it. Please let that be it.)"
            "I hold it up against the fare map above the machines. The arrow pointing at 中野 lands on a different row entirely."
            mc "(...Not it. Not it either.)"
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
    scene bg_home_exterior with walk_fade
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

        scene bg_home with walk_fade

        mother "My husband is already asleep, so you'll meet him properly in the morning. I'm Miharu Nagai."
        mc "Ah. Konnichiwa. I'm..."
        mother "I know who you are. We've been waiting months for you."
        mother "Hikari is the one who wrote all those emails. She's asleep too. She doesn't even know you've arrived, so she'll get a surprise at breakfast."
        mc "(Hikari. The one who answered every single one of my questions about the school.)"
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

        scene bg_home with walk_fade

        mother " Welcome again. I'm Miharu Nagai."
        father "And I'm Tetsuo Nagai. So you finally found our home. Miharu told us you'd be arriving today."
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

    scene bg_room with stair_fade

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
    return
