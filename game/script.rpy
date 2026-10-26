# --- CORE SYSTEMS: LANGUAGE & PROGRESSION ---

# Define custom text tags for the language system
init python:
    # 1. JAPANESE FONT FIX
    # The default Ren'Py font (DejaVuSans) has no kana/kanji, which is why every
    # Japanese line rendered as empty boxes ("tofu"). Every text style is pointed
    # at a CJK-capable font that ships inside game/fonts/.
    #
    # To change the typeface later, just drop another .ttf/.otf into game/fonts/
    # and update the three strings below.
    #
    # gui.rpy points gui.text_font / gui.name_text_font / gui.interface_text_font
    # at this font, and screens.rpy reads those. The style.* assignments below are
    # a fallback for any text drawn outside the standard styles.
    define_font = "fonts/mini-wakuwaku-maru.otf"
    gui.text_font = define_font
    gui.name_text_font = define_font
    gui.interface_text_font = define_font
    style.default.font = define_font
    style.say_dialogue.font = define_font
    style.say_label.font = define_font
    style.button_text.font = define_font
    style.menu_choice.font = define_font
    style.input.font = define_font

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
# airport.png is only 626x417, so it is scaled up and centre-cropped to fill the
# 1280x720 screen rather than stretched out of shape.
image bg_airport = Transform("images/backgrounds/airport.png", xysize=(config.screen_width, config.screen_height), fit="cover")
image bg_home = Solid("#1C1B18")
image bg_train = Solid("#1C1B18")
image hospital_flash = Solid("#d9e6ee")

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
        return True

    def add_item(item):
        if item not in store.inventory:
            store.inventory.append(item)
            renpy.notify(_("Picked up: %s") % item)

    def remove_item(item):
        if item in store.inventory:
            store.inventory.remove(item)

    def has_item(item):
        return item in store.inventory

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
define security = Character("Security", callback=type_sound)

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

    # What he landed with: enough for a train ticket and a first meal. Everything
    # after that he has to earn or go without, which is the point of the wallet.
    $ money = 5000

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
    "Please check your flight departure time carefully. Gates close 30 minutes before departure."
    jump airport_exploration

label look_plants:
    "Oh what a great plant!"
    jump airport_exploration

label end_airport:
    # Reached only from the veteran's branch, so it is the veteran who sees him off.
    veteran "Glad to help! Enjoy your trip, and welcome to Japan!"
    mc "...Thanks. I'll try my best."

    # He is out of the terminal, so the crowd and its music go with it.
    stop music fadeout 2.0
    stop ambient fadeout 2.0
    return
