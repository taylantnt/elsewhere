################################################################################
## DREAMS
################################################################################
##
## One router, one label per dream. The story decides what the day was; the
## router decides which dream follows it. A first visit can plant its own dream
## by setting `dream_key` before sleep:
##
##     $ dream_key = "ramen"
##     jump dream_router
##
## The first night is the only dream that is mandatory. Every other key below is
## a place for the activity-reactive dreams to land once those scenes are
## written. The old "put the day back" board is archived in dream_archive.rpy;
## it still works, but it is not on the story's path any more.
##
## Planned keys (not written yet):
##   "ramen"       — the bowl that will not let him choose
##   "photo_club"  — a photograph that keeps taking itself
##   "hikari_run"  — the river path, no phone, no money, no Hikari
##
## When one of those dreams is written, add its branch here and point the first
## visit at it. Nothing else in the day loop needs to change.

default dream_key = "first_night"
default dream_history = []


label dream_router:

    if dream_key == "first_night":
        jump dream_first_night
    elif dream_key == "day_two_cellular_maid":
        jump dream_day_two_cellular_maid
    elif dream_key == "put_the_day_back":
        jump dream_put_the_day_back
    else:
        # A day with no dream of its own still gets a quiet fade rather than a
        # crash. Future keys can be added above as their scenes are written.
        jump dream_generic


## --- DAY TWO: THE PHONE AND THE CAFE -----------------------------------------
##
## PLACEHOLDER. This is the dream after the cellular-plan day and Aya's first
## visit. It is deliberately short: the shape is here, the game is not. Replace
## the middle with the real cellular/maid-cafe dream when that scene is designed.
##
## The two things the day gave him are a line that reaches the city and a room
## that calls him Master. The dream makes both of them contracts.

label dream_day_two_cellular_maid:

    stop music fadeout 2.0
    pause 1.2

    play music "audio/Music/dream sequence.wav" fadein 3.0

    show screen dream_static
    pause 1.0
    hide screen dream_static

    scene bg_akihabara_hamada_inside at glitch_jitter with Dissolve(0.35)
    "I am back in Hamada Denki. The floor goes up forever, and every floor is the same floor."
    "A clerk with Aya's smile slides a contract across the counter. The monthly fee is printed in years."
    mc "I only wanted a phone plan."
    "She turns the tablet around. On the screen, the maid cafe is already open, and I am already sitting at a table."
    "The contract has a line for the number of visits. It already says seven."
    "The signal bars on my phone light up one by one. Each bar is a small white door."
    "The last door opens. Somewhere behind me, a bell rings."

    show hospital_flash onlayer overlay at truecenter:
        alpha 0.0
        linear 0.08 alpha 0.6
        linear 0.08 alpha 0.0
    "He signed it."
    "He does not remember signing it."

    scene bg_maidcafe at glitch_jitter with Dissolve(0.35)
    "The cafe is empty. Aya is drawing a cat in ketchup on every plate, and every plate is mine."
    aya "You already ordered this, Master."
    mc "I don't remember."
    aya "That's all right. You don't have to remember. You just have to come back."
    "The cat on the omelette opens its eyes."
    "I wake up before it finishes the sentence."

    stop music fadeout 3.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump saturday_off


## --- QUIET FALLBACK ----------------------------------------------------------
##
## Used only if a scene sets a dream key before its dream exists. It ends the
## build rather than dropping the player into a half-written scene.

label dream_generic:

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    "The dream goes somewhere I cannot follow."
    stop music fadeout 2.0
    pause 1.0
    jump end_of_build
