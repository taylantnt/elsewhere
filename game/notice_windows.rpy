# Standalone notices sit above gameplay, but below system confirmations.
define notice_window_zorder = 180
define notice_page_duration = 8.0

init -1 python:
    guide_font = FontGroup()
    guide_font.add("DejaVuSans.ttf", 0x20, 0x024f)
    guide_font.add("fonts/KiwiMaru-Medium.ttf", None, None)

    def standalone_window_active():
        return any(renpy.get_screen(name) is not None for name in (
            "hint_card", "notice_page", "notice_confirm", "notice_name",
            "location_hub", "attribute_gain_card", "airport_phone",
        ))

    def cinematic_departure():
        renpy.call_in_new_context("_cinematic_departure")

label _cinematic_departure:
    call screen cinematic_black
    return

# Runs only after a load has been confirmed, before saved state replaces menus.
label before_load:
    call _cinematic_departure from _call__cinematic_departure
    return

transform cinematic_black_in:
    alpha 0.0
    linear 1.4 alpha 1.0

screen cinematic_black():
    modal True
    zorder 2100
    key "game_menu" action NullAction()
    key "rollback" action NullAction()
    key "dismiss" action NullAction()
    add Solid("#000000") at cinematic_black_in
    timer 3.4 action Return(True)

transform opening_in:
    alpha 0.0
    linear 1.4 alpha 1.0

transform opening_out:
    alpha 1.0
    linear 1.4 alpha 0.0

transform notice_window_still:
    alpha 1.0

transform notice_window_in:
    alpha 0.0
    yoffset gui.scale(12)
    easeout 0.35 alpha 1.0 yoffset 0

transform notice_window_out:
    alpha 1.0
    yoffset 0
    easein 0.28 alpha 0.0 yoffset gui.scale(-8)

transform notice_page_motion:
    alpha 0.0
    linear 1.4 alpha 1.0
    pause 5.2
    linear 1.4 alpha 0.0

transform notice_backdrop_in:
    alpha 0.0
    linear 0.35 alpha 0.78

transform notice_backdrop_out:
    alpha 0.78
    linear 0.28 alpha 0.0

style guide_category is default:
    font "DejaVuSans.ttf"
    size gui.scale(11)
    bold True
    color "#c8a06a"
    kerning gui.scale(2)
    outlines []

style guide_title is default:
    font "DejaVuSans.ttf"
    size gui.scale(30)
    bold True
    color "#f3eee5"
    outlines []

style guide_body is default:
    font guide_font
    size gui.scale(18)
    color "#ded8ce"
    line_spacing gui.scale(4)
    text_align 0.0
    outlines []

style guide_meta is default:
    font guide_font
    size gui.scale(12)
    color "#aaa297"
    outlines []

style guide_button is button:
    background Solid("#c8a06a")
    hover_background Solid("#e4bd87")
    insensitive_background Solid("#34312c")
    padding (gui.scale(24), gui.scale(12))
    xminimum gui.scale(132)

style guide_button_text is default:
    font guide_font
    size gui.scale(15)
    bold True
    color "#1c1b18"
    hover_color "#141310"
    insensitive_color "#827b70"
    text_align 0.5
    outlines []

style guide_input is default:
    font guide_font
    size gui.scale(26)
    color "#f3eee5"
    outlines []

screen standalone_notice_window(title, category="GUIDE", motion=None):
    # Block menu and rollback shortcuts while a required window owns input.
    key "game_menu" action NullAction()
    key "rollback" action NullAction()

    fixed:
        xalign 0.5
        yalign 0.5
        xysize (gui.scale(760), gui.scale(480))
        at (motion if motion is not None else notice_window_still)

        add Solid("#00000066"):
            xpos gui.scale(10)
            ypos gui.scale(14)
            xysize (gui.scale(760), gui.scale(480))
        add Solid("#51483b") xysize (gui.scale(760), gui.scale(480))
        add Solid("#1c1b18"):
            xpos gui.scale(1)
            ypos gui.scale(1)
            xysize (gui.scale(758), gui.scale(478))
        add Solid("#c8a06a"):
            xpos gui.scale(56)
            ypos gui.scale(42)
            xysize (gui.scale(3), gui.scale(52))

        text category style "guide_category" xpos gui.scale(74) ypos gui.scale(40)
        text title style "guide_title" xpos gui.scale(74) ypos gui.scale(61)
        add Solid("#3e3931"):
            xpos gui.scale(56)
            ypos gui.scale(116)
            xysize (gui.scale(648), gui.scale(1))

        fixed:
            xpos gui.scale(56)
            ypos gui.scale(145)
            xysize (gui.scale(648), gui.scale(291))
            transclude

screen standalone_notice_footer(meta, caption=None, action=None, enabled=True):
    fixed:
        ypos gui.scale(230)
        xysize (gui.scale(648), gui.scale(61))
        add Solid("#3e3931") xysize (gui.scale(648), gui.scale(1))
        text meta style "guide_meta":
            ypos gui.scale(30)
            yanchor 0.5
            xmaximum gui.scale(440)
        if caption is not None:
            textbutton caption:
                style "guide_button"
                action action
                sensitive enabled
                xalign 1.0
                ypos gui.scale(9)

screen hint_card(eyebrow, body):
    modal True
    zorder notice_window_zorder
    default hiding = False

    add Solid("#000000") at (notice_backdrop_out if hiding else notice_backdrop_in)
    use standalone_notice_window(eyebrow, motion=(notice_window_out if hiding else notice_window_in)):
        text body style "guide_body" xsize gui.scale(648)
        use standalone_notice_footer(
            "This notification is shown only once.",
            "Got It",
            SetScreenVariable("hiding", True),
            not hiding,
        )
    if hiding:
        timer 0.30 action Return()

style opening_category is guide_category:
    color "#858585"

style opening_title is guide_title:
    size gui.scale(40)
    bold False
    color "#eeeeee"

style opening_body is guide_body:
    color "#bdbdbd"
    line_spacing gui.scale(8)
    text_align 0.5
    xalign 0.5

style opening_meta is guide_meta:
    color "#777777"

style opening_button is guide_button:
    background None
    hover_background Solid("#191919")
    insensitive_background None
    padding (gui.scale(20), gui.scale(12))

style opening_button_text is guide_button_text:
    color "#eeeeee"
    hover_color "#ffffff"
    insensitive_color "#555555"

style opening_input is guide_input:
    size gui.scale(32)
    color "#eeeeee"
    text_align 0.5
    xalign 0.5

# Opening pages use typography and negative space, not the in-game card shell.
screen opening_layout(title, motion, category="BEFORE YOU BEGIN"):
    key "game_menu" action NullAction()
    key "rollback" action NullAction()
    fixed:
        xalign 0.5
        yalign 0.5
        xysize (gui.scale(680), gui.scale(420))
        at motion
        text category style "opening_category" xalign 0.5 xsize gui.scale(680) text_align 0.5
        text title style "opening_title" ypos gui.scale(42) xalign 0.5 xsize gui.scale(680) text_align 0.5
        add Solid("#777777"):
            ypos gui.scale(111)
            xysize (gui.scale(48), gui.scale(1))
            xalign 0.5
        fixed:
            ypos gui.scale(145)
            xysize (gui.scale(680), gui.scale(275))
            transclude

screen opening_footer(meta, caption=None, action=None, enabled=True):
    fixed:
        ypos gui.scale(208)
        xysize (gui.scale(680), gui.scale(76))
        text meta style "opening_meta" xalign 0.5 xsize gui.scale(680) text_align 0.5
        if caption is not None:
            textbutton caption:
                style "opening_button"
                xalign 0.5
                ypos gui.scale(28)
                action action
                sensitive enabled

screen notice_page(eyebrow, body, page):
    modal True
    zorder notice_window_zorder
    add Solid("#000000")
    use opening_layout(eyebrow, notice_page_motion):
        text body style "opening_body" xalign 0.5 xsize gui.scale(680)
        use opening_footer("%s  Continues automatically" % page)
    timer notice_page_duration action Return()

screen notice_confirm(question):
    modal True
    zorder notice_window_zorder
    default hiding = False
    add Solid("#000000")
    use opening_layout("Before You Begin", opening_out if hiding else opening_in, "CONFIRMATION"):
        text question style "opening_body" xalign 0.5 xsize gui.scale(680)
        use opening_footer("Confirm to continue.", "I Understand", SetScreenVariable("hiding", True), not hiding)
    if hiding:
        timer 3.4 action Return(True)

screen notice_name():
    modal True
    zorder notice_window_zorder
    add Solid("#000000")
    use opening_layout("Your Name", opening_in):
        text "Enter the name other characters will use for you." style "opening_body" xalign 0.5 xsize gui.scale(680)
        fixed:
            xalign 0.5
            ypos gui.scale(65)
            xysize (gui.scale(680), gui.scale(72))
            input:
                id "input"
                xalign 0.5
                value VariableInputValue("player_name", returnable=False)
                length 12
                exclude "{}[]"
                style "opening_input"
                pixel_width gui.scale(300)
            add Solid("#454545"):
                ypos gui.scale(65)
                xysize (gui.scale(300), gui.scale(1))
                xalign 0.5
        use opening_footer(
            "Up to 12 characters. A name is required.",
            "Begin",
            Return(True),
            bool(player_name.strip()),
        )
    # Handle Enter before the input consumes it, including the blank-name case.
    key ["K_RETURN", "K_KP_ENTER"] action If(bool(player_name.strip()), Return(True), NullAction())

# The end-of-build card. It is deliberately a title card rather than a dialog
# box: the story has stopped, and the screen should feel like the lights coming
# up in a theatre, not like another conversation.
#
# It is reached from `label end_of_build` at the bottom of script.rpy. When new
# scenes are written, move the jump to `end_of_build` to the new last scene and
# leave the label where it is. The card then stays the fallback for every build.
transform end_card_in:
    alpha 0.0
    linear 1.0 alpha 1.0

transform end_cursor:
    alpha 0.15
    block:
        linear 0.9 alpha 1.0
        linear 0.9 alpha 0.15
        repeat

screen end_of_build_card():
    modal True
    zorder 2000
    key "game_menu" action NullAction()
    key "rollback" action NullAction()

    add Solid("#050505")
    fixed:
        xalign 0.5
        yalign 0.5
        xysize (gui.scale(860), gui.scale(560))
        at end_card_in

        add Solid("#0c0b0a") xysize (gui.scale(860), gui.scale(560))
        add Solid("#c8a06a"):
            xpos gui.scale(56)
            ypos gui.scale(52)
            xysize (gui.scale(64), gui.scale(2))

        vbox:
            xalign 0.5
            yalign 0.5
            spacing gui.scale(18)
            xsize gui.scale(700)

            text "ELSEWHERE" style "guide_category":
                xalign 0.5
                text_align 0.5
                kerning gui.scale(5)
                color "#c8a06a"

            text "THANK YOU FOR PLAYING" style "guide_title":
                xalign 0.5
                xsize gui.scale(700)
                text_align 0.5
                size gui.scale(38)
                kerning gui.scale(2)
                color "#f3eee5"

            add Solid("#3e3931") xalign 0.5 xysize (gui.scale(120), gui.scale(1))

            text "You have reached the end of the current build." style "guide_body":
                xalign 0.5
                xsize gui.scale(620)
                text_align 0.5
                color "#ded8ce"

            text "New days, conversations, and routes are being written now.\nYour save will be waiting when they arrive." style "guide_body":
                xalign 0.5
                xsize gui.scale(620)
                text_align 0.5
                color "#aaa297"
                size gui.scale(16)
                line_spacing gui.scale(5)

            text "STAY TUNED" style "guide_category":
                xalign 0.5
                text_align 0.5
                kerning gui.scale(5)
                color "#c8a06a"

            textbutton "Return to Title":
                style "guide_button"
                xalign 0.5
                action Return()

    # A small pulse in the bottom corner, like a cursor waiting on the next line.
    text "■" xalign 0.97 yalign 0.95 size gui.scale(10) color "#c8a06a" at end_cursor
