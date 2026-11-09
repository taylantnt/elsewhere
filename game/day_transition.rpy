################################################################################
## THE DAY TRANSITION
################################################################################
##
## The full-screen card that carries the story from one day to the next. It is
## called at the top of every day label, after the night scene and before the
## morning, so the calendar is something the player sees rather than something
## the HUD quietly updates.
##
## The shape is a horizontal strip of days. The day that just ended is centred
## and bright; the strip slides one slot left, the old day shrinks and fades,
## and the new day glides into the centre. The last frame holds until the
## player clicks or presses a key. It never advances on its own, and rollback,
## skip, and the game menu are blocked while it is up.
##
## `day_transition_cards()` and `day_transition_sparks()` are pure data so the
## screen can be re-evaluated by its timers without re-rolling positions.

define day_transition_slot = 330
define day_transition_center = 640
define day_transition_card_y = 318
define day_transition_rail_y = 500

## `dismiss` covers the mouse, space, enter and the gamepad. The rest of the
## keys are added so "press any key" is honest on a keyboard.
define day_transition_extra_keys = (
    ["K_" + c for c in "abcdefghijklmnopqrstuvwxyz"]
    + ["K_" + str(d) for d in range(10)]
    + ["K_LEFT", "K_RIGHT", "K_UP", "K_DOWN", "K_TAB", "K_BACKSPACE",
       "K_DELETE", "K_INSERT", "K_HOME", "K_END", "K_PAGEDOWN"]
)

init python:

    def day_transition_card(day):
        """The display data for one day on the strip."""
        day = max(1, int(day))
        date_value = story_calendar_date(day)
        return {
            "day": day,
            "eyebrow": "DAY %d" % day,
            "month": story_month_names[date_value.month - 1].upper(),
            "number": "%02d" % date_value.day,
            "weekday": story_weekday_names[date_value.weekday()].upper(),
            "meta": "WEEK %d" % story_week_number(day),
            "event": story_calendar_events.get(day, ""),
        }

    def day_transition_cards(from_day, to_day):
        """The four slots around the move, with their start and end states."""
        from_day = max(1, int(from_day))
        to_day = max(1, int(to_day))

        specs = []

        # The slot before the old day only exists once there is a day before it.
        if from_day > 1:
            specs.append((from_day - 1, -1, -2, 0.66, 0.56, 0.15, 0.06, False))

        specs.append((from_day, 0, -1, 1.00, 0.72, 1.00, 0.22, False))
        specs.append((to_day, 1, 0, 0.72, 1.00, 0.22, 1.00, True))
        specs.append((to_day + 1, 2, 1, 0.56, 0.66, 0.06, 0.15, False))

        cards = []
        for day, start_slot, end_slot, start_zoom, end_zoom, start_alpha, end_alpha, land in specs:
            cards.append({
                "card": day_transition_card(day),
                "start_x": start_slot * day_transition_slot,
                "end_x": end_slot * day_transition_slot,
                "start_zoom": start_zoom,
                "end_zoom": end_zoom,
                "start_alpha": start_alpha,
                "end_alpha": end_alpha,
                "land": land,
            })
        return cards

    def day_transition_sparks():
        """Fixed spark positions so a screen timer cannot reshuffle them."""
        return [
            (500, 250, 1.62, 0.16, 34),
            (790, 268, 1.70, 0.12, 28),
            (470, 380, 1.76, 0.10, 24),
            (820, 408, 1.66, 0.18, 38),
            (560, 470, 1.82, 0.12, 30),
            (720, 492, 1.74, 0.14, 26),
            (628, 176, 1.68, 0.11, 22),
            (858, 332, 1.80, 0.09, 20),
        ]


## --- THE MOTION --------------------------------------------------------------
##
## Everything below is deliberately slow enough to read. The card move is 0.95s
## and the whole sequence is under two seconds before the hold.

transform day_transition_screen_in:
    alpha 0.0
    linear 0.45 alpha 1.0

transform day_transition_glow:
    alpha 0.0
    zoom 1.04
    linear 0.65 alpha 0.58 zoom 1.0
    block:
        ease 4.2 zoom 1.018
        ease 4.2 zoom 1.0
        repeat

transform day_transition_rays:
    alpha 0.0
    rotate 0
    linear 0.9 alpha 0.05
    block:
        linear 40.0 rotate 10
        linear 40.0 rotate 0
        repeat

transform day_transition_rail:
    alpha 0.0
    linear 0.8 alpha 1.0

transform day_transition_rail_spark:
    alpha 0.0
    zoom 0.12
    pause 1.55
    linear 0.22 alpha 0.85 zoom 0.17
    block:
        linear 1.25 alpha 0.42 zoom 0.14
        linear 1.25 alpha 0.85 zoom 0.17
        repeat

transform day_transition_card_move(start_x, end_x, start_zoom, end_zoom, start_alpha, end_alpha):
    xpos day_transition_center
    xanchor 0.5
    ypos day_transition_card_y
    yanchor 0.5
    xoffset start_x
    zoom start_zoom
    alpha start_alpha
    pause 0.85
    ease 0.95 xoffset end_x zoom end_zoom alpha end_alpha

transform day_transition_card_land(start_x, end_x, start_zoom, end_zoom, start_alpha, end_alpha):
    xpos day_transition_center
    xanchor 0.5
    ypos day_transition_card_y
    yanchor 0.5
    xoffset start_x
    zoom start_zoom
    alpha start_alpha
    pause 0.85
    ease 0.95 xoffset end_x zoom end_zoom alpha end_alpha
    easeout 0.10 zoom (end_zoom * 1.014)
    ease 0.22 zoom end_zoom

transform day_transition_rule:
    xzoom 0.0
    pause 0.55
    easeout 0.45 xzoom 1.0

transform day_transition_sweep:
    xoffset -560
    alpha 0.0
    pause 0.92
    linear 0.16 alpha 0.22
    ease 0.95 xoffset 560
    linear 0.16 alpha 0.0

transform day_transition_spark(x, y, delay, size, rise):
    xpos x
    ypos y
    xanchor 0.5
    yanchor 0.5
    zoom size
    alpha 0.0
    pause delay
    linear 0.10 alpha 0.9
    easeout 0.9 ypos (y - rise) alpha 0.0

transform day_transition_prompt_in:
    alpha 0.0
    pause 2.05
    linear 0.40 alpha 1.0

transform day_transition_prompt_dot:
    alpha 0.35
    block:
        linear 0.85 alpha 1.0
        linear 0.85 alpha 0.35
        repeat


## --- THE CARD ----------------------------------------------------------------

style day_transition_eyebrow is default:
    font "DejaVuSans.ttf"
    size gui.scale(11)
    bold True
    color "#c8a06a"
    kerning gui.scale(4)
    outlines []

style day_transition_month is default:
    font "DejaVuSans.ttf"
    size gui.scale(14)
    bold True
    color "#9a8e7d"
    kerning gui.scale(6)
    outlines []

style day_transition_number is default:
    font "DejaVuSans.ttf"
    size gui.scale(148)
    bold True
    color "#f3eee5"
    kerning gui.scale(-2)
    outlines [(gui.scale(10), "#c8a06a10", 0, 0), (gui.scale(4), "#c8a06a1a", 0, 0)]

style day_transition_weekday is default:
    font "DejaVuSans.ttf"
    size gui.scale(26)
    bold True
    color "#f3eee5"
    kerning gui.scale(3)
    outlines []

style day_transition_event is default:
    font "DejaVuSans.ttf"
    size gui.scale(13)
    color "#8f877b"
    text_align 0.5
    line_spacing gui.scale(2)
    outlines []

style day_transition_meta is default:
    font "DejaVuSans.ttf"
    size gui.scale(10)
    bold True
    color "#c8a06a"
    kerning gui.scale(3)
    outlines []

style day_transition_prompt is default:
    font "DejaVuSans.ttf"
    size gui.scale(11)
    bold True
    color "#c8a06a"
    kerning gui.scale(4)
    outlines []


screen day_transition_date_card(card):
    fixed:
        xsize 300
        ysize 380

        text card["eyebrow"]:
            style "day_transition_eyebrow"
            xalign 0.5
            ypos 0

        text card["month"]:
            style "day_transition_month"
            xalign 0.5
            ypos 22

        text card["number"]:
            style "day_transition_number"
            xalign 0.5
            ypos 34

        text card["weekday"]:
            style "day_transition_weekday"
            xalign 0.5
            ypos 218

        add Solid("#c8a06a") xysize (56, 1) xalign 0.5 ypos 262 at day_transition_rule

        if card["event"]:
            text card["event"]:
                style "day_transition_event"
                xalign 0.5
                xsize 280
                ypos 276

        text card["meta"]:
            style "day_transition_meta"
            xalign 0.5
            ypos 340

        add Solid("#c8a06a") xysize (46, 2) xalign 0.5 ypos 366


## --- THE SCREEN --------------------------------------------------------------

screen day_transition_screen(from_day, to_day, cards, sparks):
    modal True
    zorder 2000

    default ready = False
    timer 2.20 action SetScreenVariable("ready", True)

    # Nothing advances the screen until the animation has landed. After that
    # a click or any key returns; the game menu, rollback and skip stay blocked
    # for the whole time the card is up.
    key "dismiss" action If(ready, true=Return(True), false=NullAction())
    key "game_menu" action NullAction()
    key "rollback" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "fast_skip" action NullAction()
    for _keysym in day_transition_extra_keys:
        key _keysym action If(ready, true=Return(True), false=NullAction())

    # The soundtrack of the move: a riser under the slide and a settle when
    # the new day lands. The tick is the smallest possible lock-in.
    timer 0.15 action Play("sound", "audio/SFX/attribute_rise.wav", relative_volume=0.62)
    timer 1.78 action Play("sound", "audio/SFX/attribute_settle.wav", relative_volume=0.75)
    timer 1.80 action Play("sound", "audio/SFX/type_click.wav", relative_volume=0.35)

    # --- backdrop ------------------------------------------------------------
    add Solid("#070606")

    add "images/ui/day_transition/day_glow.png" xalign 0.5 yalign 0.5 yoffset gui.scale(-12) at day_transition_glow

    add "images/ui/memory/memory_win_rays.png" xalign 0.5 yalign 0.5 zoom 1.9 alpha 0.04 at day_transition_rays

    add "images/ui/day_transition/day_vignette.png"

    add "images/ui/day_transition/day_grain.png" xysize (config.screen_width, config.screen_height) alpha 0.5

    # --- the rail the days sit on ---------------------------------------
    add "images/ui/day_transition/day_rail.png" xalign 0.5 ypos day_transition_rail_y at day_transition_rail

    add "images/ui/memory/memory_spark.png" xpos day_transition_center ypos (day_transition_rail_y + 1) xanchor 0.5 yanchor 0.5 at day_transition_rail_spark

    # --- the strip -------------------------------------------------------
    for spec in cards:
        if spec["land"]:
            fixed:
                xysize (300, 380)
                at day_transition_card_land(
                    spec["start_x"], spec["end_x"],
                    spec["start_zoom"], spec["end_zoom"],
                    spec["start_alpha"], spec["end_alpha"],
                )
                use day_transition_date_card(spec["card"])
        else:
            fixed:
                xysize (300, 380)
                at day_transition_card_move(
                    spec["start_x"], spec["end_x"],
                    spec["start_zoom"], spec["end_zoom"],
                    spec["start_alpha"], spec["end_alpha"],
                )
                use day_transition_date_card(spec["card"])

    # --- light sweep across the move ------------------------------------
    add "images/ui/day_transition/day_sweep.png" xalign 0.5 yalign 0.5 at day_transition_sweep

    # --- the glints around the landing ----------------------------------
    for x, y, delay, size, rise in sparks:
        add "images/ui/memory/memory_spark.png" at day_transition_spark(x, y, delay, size, rise)

    # --- hold ------------------------------------------------------------
    frame:
        at day_transition_prompt_in
        xalign 0.5
        yalign 0.955
        background None

        hbox:
            spacing gui.scale(10)

            add Solid("#c8a06a") xysize (4, 4) yalign 0.5 at day_transition_prompt_dot

            text "CLICK OR PRESS ANY KEY" style "day_transition_prompt" yalign 0.5


## --- THE LABEL ---------------------------------------------------------------

label day_transition:
    # Day labels set story_day before calling this, so the strip knows both
    # ends of the move without counting anything itself.
    if story_day <= 1:
        return

    $ dt_from = max(1, int(story_day) - 1)
    $ dt_to = int(story_day)
    $ dt_cards = day_transition_cards(dt_from, dt_to)
    $ dt_sparks = day_transition_sparks()

    window hide
    stop music fadeout 0.9
    scene black with Dissolve(0.35)
    call screen day_transition_screen(dt_from, dt_to, dt_cards, dt_sparks)

    $ dt_from = None
    $ dt_to = None
    $ dt_cards = None
    $ dt_sparks = None
    return
