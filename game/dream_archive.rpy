################################################################################
## ARCHIVE: "PUT THE DAY BACK"
################################################################################
##
## This is the full memory-ordering dream from the first build. It is kept
## intact because the board is still good, but the main story no longer calls
## it. Dreams now route through `dream_router` in dreams.rpy and change with the
## day's first visits.
##
## To try it again, set `dream_key = "put_the_day_back"` in the console and jump
## to `dream_put_the_day_back`, or wire that key into the router.
##
## It expects the shared dream visuals (`dream_static`, `glitch_jitter`) from
## script.rpy and the travel flags from the arrival. The label ends with
## `return` instead of `jump morning_call`, so it can be called from a test or a
## future dream without taking over the story.

init python:
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


label dream_put_the_day_back:

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

    return


