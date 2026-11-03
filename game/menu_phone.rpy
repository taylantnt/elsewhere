################################################################################
## Handheld menus
################################################################################

init offset = 5

default menu_phone_open = False
default menu_phone_started_at = 0.0
default menu_phone_closing = False
default menu_phone_closed_at = 0.0
default menu_phone_close_offset = 0
default menu_phone_close_alpha = 1.0

init python:
    import time

    menu_phone_font = FontGroup()
    menu_phone_font.add("DejaVuSans.ttf", 0x20, 0x024f)
    menu_phone_font.add("fonts/KiwiMaru-Medium.ttf", None, None)

    def menu_phone_begin():
        store.menu_phone_started_at = time.monotonic()
        store.menu_phone_closing = False
        store.menu_phone_open = True

    def menu_phone_end():
        if store.menu_phone_closing:
            return
        elapsed = time.monotonic() - store.menu_phone_started_at
        progress = min(1.0, max(0.0, elapsed / 0.95))
        store.menu_phone_close_offset = gui.scale(int(760 * (1.0 - progress) ** 5))
        store.menu_phone_close_alpha = min(1.0, max(0.0, (elapsed - 0.55) / 0.3))
        store.menu_phone_closed_at = time.monotonic()
        store.menu_phone_closing = True

    def menu_phone_finish_close():
        store.menu_phone_open = False
        store.menu_phone_closing = False

    # Rebuilds must not restart the gesture; both layers share the press time.
    def menu_phone_motion(trans, st, at, started_at):
        progress = min(1.0, max(0.0, (time.monotonic() - started_at) / 0.95))
        remaining = (1.0 - progress) ** 5
        trans.yoffset = gui.scale(int(760 * remaining))
        return 0.016 if progress < 1.0 else None

    def menu_phone_illumination(trans, st, at, started_at):
        progress = min(1.0, max(0.0, (time.monotonic() - started_at - 0.55) / 0.3))
        trans.alpha = progress
        return 0.016 if progress < 1.0 else None

    def menu_phone_lowering(trans, st, at, closed_at, initial_offset):
        progress = min(1.0, max(0.0, (time.monotonic() - closed_at) / 0.65))
        trans.yoffset = int(initial_offset + (gui.scale(760) - initial_offset) * progress ** 2)
        return 0.016 if progress < 1.0 else None

    def menu_phone_dimming(trans, st, at, closed_at, initial_alpha):
        progress = min(1.0, max(0.0, (time.monotonic() - closed_at) / 0.20))
        trans.alpha = initial_alpha * (1.0 - progress)
        return 0.016 if progress < 1.0 else None

# Coordinates match the illustrated screen aperture. The phone, not the wrist,
# is centered; all pages share these bounds so navigation never moves the grip.
define menu_phone_x = 506
define menu_phone_y = 44
define menu_phone_w = 270
define menu_phone_h = 620
define menu_phone_content_w = 242
define menu_phone_background = "images/ui/menu_background.png"

screen phone_backdrop():
    if main_menu:
        add Transform(menu_phone_background, xysize=(int(config.screen_width * 1.15), int(config.screen_height * 1.15)), fit="cover", blur=32.0, xalign=0.5, yalign=0.5)
        add Transform(menu_phone_background, xysize=(config.screen_width, config.screen_height), fit="contain", xalign=0.5, yalign=0.5)
        use sakura_blossoms
    else:
        add Solid("#11100f70")
    add Solid("#15130f65")

transform phone_raise(started_at):
    subpixel True
    xpos 0
    ypos 0
    xanchor 0.0
    yanchor 0.0
    function renpy.curry(menu_phone_motion)(started_at=started_at)

transform phone_wake(started_at):
    function renpy.curry(menu_phone_illumination)(started_at=started_at)

transform phone_lower(closed_at, initial_offset):
    subpixel True
    xpos 0
    ypos 0
    xanchor 0.0
    yanchor 0.0
    function renpy.curry(menu_phone_lowering)(closed_at=closed_at, initial_offset=initial_offset)

transform phone_sleep(closed_at, initial_alpha):
    function renpy.curry(menu_phone_dimming)(closed_at=closed_at, initial_alpha=initial_alpha)

screen phone_hardware(animate=False, raised_at=0.0, closing=False):
    fixed:
        xysize (config.screen_width, config.screen_height)
        if closing:
            at phone_lower(menu_phone_closed_at, menu_phone_close_offset)
        elif animate:
            at phone_raise(raised_at)
        add "images/ui/menu_hand.png":
            xpos gui.scale(252)
            ypos gui.scale(-76)
            xysize (gui.scale(800), gui.scale(1071))
        fixed:
            xpos gui.scale(menu_phone_x)
            ypos gui.scale(menu_phone_y)
            xysize (gui.scale(menu_phone_w), gui.scale(menu_phone_h))
            if closing:
                at phone_sleep(menu_phone_closed_at, menu_phone_close_alpha)
            elif animate:
                at phone_wake(raised_at)
            transclude

screen phone_status():
    fixed:
        xfill True
        ysize gui.scale(26)
        text "20:00":
            style "phone_status"
            xpos gui.scale(17)
            yalign 0.5
        add Solid("#090908"):
            xalign 0.5
            yalign 0.5
            xysize (gui.scale(52), gui.scale(8))
        text "OFFLINE":
            style "phone_status"
            xalign 1.0
            xoffset gui.scale(-17)
            yalign 0.5

transform airport_phone_motion:
    yoffset gui.scale(760)
    easeout 0.95 yoffset 0
    pause 2.5
    easein 0.65 yoffset gui.scale(760)

screen airport_phone():
    modal True
    zorder notice_window_zorder
    key "game_menu" action NullAction()
    key "rollback" action NullAction()
    key "dismiss" action NullAction()
    fixed:
        xysize (config.screen_width, config.screen_height)
        at airport_phone_motion
        use phone_hardware():
            add Solid("#101112")
            text "MAP":
                font menu_phone_font
                size gui.scale(12)
                color "#85898d"
                outlines []
                xalign 0.5
                ypos gui.scale(66)
            vbox:
                xalign 0.5
                yalign 0.48
                spacing gui.scale(16)
                text "NO SIGNAL":
                    font menu_phone_font
                    size gui.scale(25)
                    bold True
                    color "#f0f0f0"
                    outlines []
                    xalign 0.5
                text "Unable to connect.":
                    font menu_phone_font
                    size gui.scale(13)
                    color "#93989d"
                    outlines []
                    xalign 0.5
    timer 4.15 action Return()

screen phone_row(caption, action, detail=None):
    button:
        style "phone_row"
        sensitive not menu_phone_closing
        action action
        hbox:
            yalign 0.5
            xfill True
            vbox:
                xsize gui.scale(202)
                spacing gui.scale(3)
                text caption style "phone_row_text"
                if detail:
                    text detail style "phone_detail"
            text ">":
                style "phone_detail"
                yalign 0.5

screen phone_links():
    vbox:
        xfill True
        spacing gui.scale(2)
        if main_menu:
            use phone_row(_("New Game"), [Function(cinematic_departure), Start()])
            use phone_row(_("Continue"), Continue())
        else:
            use phone_row(_("Resume"), Return())
            use phone_row(_("History"), ShowMenu("history"))
            use phone_row(_("Save"), ShowMenu("save"))
            use phone_row(_("Bag"), ShowMenu("inventory"))
            use phone_row(_("Attributes"), ShowMenu("attributes"))
        use phone_row(_("Load"), ShowMenu("load"))
        use phone_row(_("Settings"), ShowMenu("preferences"))
        use phone_row(_("About"), ShowMenu("about"))
        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
            use phone_row(_("Help"), ShowMenu("help"))
        if _in_replay:
            use phone_row(_("End Replay"), EndReplay(confirm=True))
        elif not main_menu:
            use phone_row(_("Main Menu"), MainMenu())
        if renpy.variant("pc"):
            use phone_row(_("Quit"), Quit(confirm=True))

screen phone_title():
    default raise_phone = not menu_phone_open
    use phone_backdrop
    if not menu_phone_open:
        textbutton _("START GAME"):
            style "phone_start"
            xalign 0.5
            yalign 0.5
            action Function(menu_phone_begin)
            default_focus True
        key "K_RETURN" action Function(menu_phone_begin)
        key "K_KP_ENTER" action Function(menu_phone_begin)
    else:
        use phone_hardware(animate=raise_phone, raised_at=menu_phone_started_at, closing=menu_phone_closing):
            use phone_status
            fixed:
                xpos gui.scale(14)
                ypos gui.scale(36)
                xysize (gui.scale(menu_phone_content_w), gui.scale(558))
                vbox:
                    spacing gui.scale(12)
                    text "elsewhere" style "phone_brand"
                    text _("MENU") style "phone_detail"
                    viewport:
                        style_prefix "phone"
                        mousewheel True
                        draggable True
                        scrollbars "vertical"
                        ysize gui.scale(446)
                        vbox:
                            use phone_links
                            null height gui.scale(10)
                            text _("Version [config.version]") style "phone_detail"
            textbutton _("Close"):
                style "phone_small_button"
                xalign 0.5
                yalign 1.0
                yoffset gui.scale(-10)
                sensitive not menu_phone_closing
                action [SetLocalVariable("raise_phone", True), Function(menu_phone_end)]
        if menu_phone_closing:
            # Keep the handset mounted until it has completely cleared the view.
            timer 0.70 action Function(menu_phone_finish_close)
        key "K_ESCAPE" action [SetLocalVariable("raise_phone", True), Function(menu_phone_end)]

screen phone_game_menu(title, scroll=None, yinitial=0.0, spacing=0, back_action=None, show_navigation=True):
    default drawer = False
    use phone_backdrop
    use phone_hardware:
        use phone_status
        fixed:
            xpos gui.scale(14)
            ypos gui.scale(29)
            xysize (gui.scale(menu_phone_content_w), gui.scale(43))
            textbutton _("Back"):
                style "phone_small_button"
                yalign 0.5
                action (SetLocalVariable("drawer", False) if drawer else (back_action if back_action is not None else (ShowMenu("main_menu") if main_menu else Return())))
            text ( _("Menu") if drawer else title ):
                style "phone_heading"
                xalign 0.5
                yalign 0.5
                xmaximum gui.scale(135)
            if show_navigation:
                textbutton "=":
                    style "phone_small_button"
                    xalign 1.0
                    yalign 0.5
                    action ToggleLocalVariable("drawer")
                    alt _("Open menu")
        add Solid("#ffffff16"):
            xpos gui.scale(14)
            ypos gui.scale(74)
            xysize (gui.scale(menu_phone_content_w), 1)
        # Both dimensions are fixed: oversized children cannot escape the glass.
        viewport:
            style_prefix "phone"
            xpos gui.scale(14)
            ypos gui.scale(88)
            xysize (gui.scale(menu_phone_content_w), gui.scale(501))
            mousewheel True
            draggable True
            pagekeys True
            yinitial yinitial
            scrollbars "vertical"
            style "phone_viewport"
            if drawer:
                use phone_links
            else:
                vbox:
                    xsize gui.scale(230)
                    spacing spacing
                    transclude
        textbutton (_("Menu") if show_navigation else _("Close")):
            style "phone_small_button"
            xalign 0.5
            yalign 1.0
            yoffset gui.scale(-6)
            action (ToggleLocalVariable("drawer") if show_navigation else back_action)
    if main_menu and show_navigation:
        key "game_menu" action [SetVariable("menu_phone_open", True), ShowMenu("main_menu")]

screen phone_files(title):
    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))
    use game_menu(title):
        vbox:
            spacing gui.scale(12)
            button:
                style "phone_row"
                action page_name_value.Toggle()
                key_events True
                input:
                    style "phone_row_text"
                    value page_name_value
                    length 24
            hbox:
                spacing gui.scale(4)
                textbutton "<" style "phone_small_button" action FilePagePrevious()
                if config.has_autosave:
                    textbutton "A" style "phone_small_button" action FilePage("auto")
                if config.has_quicksave:
                    textbutton "Q" style "phone_small_button" action FilePage("quick")
                textbutton ">" style "phone_small_button" action FilePageNext()
            vpgrid:
                cols 5
                xfill True
                spacing gui.scale(3)
                for page in range(1, 10):
                    textbutton "[page]" style "phone_page_button" action FilePage(page)
            for slot in range(1, gui.file_slot_cols * gui.file_slot_rows + 1):
                button:
                    style "phone_save_button"
                    action FileAction(slot)
                    key "save_delete" action FileDelete(slot)
                    vbox:
                        spacing gui.scale(6)
                        add FileScreenshot(slot):
                            xysize (gui.scale(210), gui.scale(118))
                        text _("Slot [slot]") style "phone_row_text"
                        text FileTime(slot, format=_("%Y-%m-%d  %H:%M"), empty=_("Empty")) style "phone_detail"
                        if FileSaveName(slot):
                            text FileSaveName(slot) style "phone_detail"
                if FileLoadable(slot):
                    textbutton _("Delete"):
                        style "phone_small_button"
                        action FileDelete(slot)
            if config.has_sync:
                if CurrentScreenName() == "save":
                    textbutton _("Upload Sync") style "phone_small_button" action UploadSync()
                else:
                    textbutton _("Download Sync") style "phone_small_button" action DownloadSync()
    key "save_page_prev" action FilePagePrevious()
    key "save_page_next" action FilePageNext()

screen phone_preferences():
    use game_menu(_("Settings")):
        vbox:
            spacing gui.scale(14)
            if renpy.variant("pc") or renpy.variant("web"):
                text _("Display") style "phone_heading"
                textbutton _("Window") style "phone_option" action Preference("display", "window")
                textbutton _("Fullscreen") style "phone_option" action Preference("display", "fullscreen")
            text _("Skip") style "phone_heading"
            textbutton _("Unseen Text") style "phone_option" action Preference("skip", "toggle")
            textbutton _("After Choices") style "phone_option" action Preference("after choices", "toggle")
            textbutton _("Transitions") style "phone_option" action InvertSelected(Preference("transitions", "toggle"))
            text _("Text Speed") style "phone_heading"
            bar value Preference("text speed") style "phone_slider"
            text _("Auto-Forward Time") style "phone_heading"
            bar value Preference("auto-forward time") style "phone_slider"
            if config.has_music:
                text _("Music Volume") style "phone_heading"
                bar value Preference("music volume") style "phone_slider"
            if config.has_sound:
                text _("Sound Volume") style "phone_heading"
                bar value Preference("sound volume") style "phone_slider"
                if config.sample_sound:
                    textbutton _("Test Sound") style "phone_option" action Play("sound", config.sample_sound)
            if config.has_voice:
                text _("Voice Volume") style "phone_heading"
                bar value Preference("voice volume") style "phone_slider"
                if config.sample_voice:
                    textbutton _("Test Voice") style "phone_option" action Play("voice", config.sample_voice)
            textbutton _("Mute All") style "phone_option" action Preference("all mute", "toggle")
            textbutton _("Accessibility") style "phone_option" action Show("_accessibility")
            null height gui.scale(12)

screen phone_inventory():
    default browsing = 0
    default viewing = None
    use game_menu(_("Bag")):
        vbox:
            spacing gui.scale(14)
            text _("Cash: ¥ [money]") style "phone_heading"
            if inventory:
                $ current_index = min(browsing, len(inventory) - 1)
                $ current_item = inventory[current_index]
                vpgrid:
                    cols 2
                    spacing gui.scale(8)
                    for i, item in enumerate(inventory):
                        button:
                            style "phone_item"
                            action SetLocalVariable("browsing", i)
                            selected (i == current_index)
                            vbox:
                                spacing gui.scale(6)
                                add item_icon(item, gui.scale(70)) xalign 0.5
                                text item_name(item):
                                    style "phone_detail"
                                    textalign 0.5
                                    xalign 0.5
                text item_name(current_item) style "phone_heading"
                text item_desc(current_item) style "phone_body"
                if item_usable(current_item):
                    textbutton item_use_label(current_item):
                        style "phone_option"
                        action SetLocalVariable("viewing", current_item)
                else:
                    text _("Cannot be used") style "phone_detail" color "#d68989"
            else:
                text _("No items.") style "phone_body"
    if viewing:
        use phone_item_view(viewing, SetLocalVariable("viewing", None))

screen phone_item_view(item, close_action):
    modal True
    zorder 150
    fixed:
        xpos gui.scale(menu_phone_x + 14)
        ypos gui.scale(menu_phone_y + 80)
        xysize (gui.scale(menu_phone_content_w), gui.scale(520))
        button:
            style "phone_blocker"
            xfill True
            yfill True
            action NullAction()
        viewport:
            xfill True
            ysize gui.scale(458)
            mousewheel True
            draggable True
            vbox:
                spacing gui.scale(18)
                text item_name(item) style "phone_heading"
                add item_icon(item, gui.scale(226)) xalign 0.5
                text item_desc(item) style "phone_body"
        textbutton _("Close"):
            style "phone_option"
            yalign 1.0
            action close_action
    key "game_menu" action close_action

screen phone_attributes():
    if config.developer:
        key "1" action Call("attribute_test_rank_up", "insight")
        key "2" action Call("attribute_test_rank_up", "grace")
        key "3" action Call("attribute_test_rank_up", "nerve")
    use game_menu(_("Attributes")):
        vbox:
            spacing gui.scale(18)
            for attribute_id in attribute_order:
                $ orb_color = attribute_color(attribute_id)
                $ orb_progress = attribute_rank_progress(attribute_id)
                $ orb_rank = attribute_rank(attribute_id)
                vbox:
                    spacing gui.scale(9)
                    hbox:
                        spacing gui.scale(12)
                        fixed:
                            xysize (gui.scale(76), gui.scale(76))
                            add attribute_ring_displayable(attribute_id, orb_progress, 76)
                            text "[orb_rank:02d]":
                                font "DejaVuSans.ttf"
                                size gui.scale(26)
                                bold True
                                color "#f4eee4"
                                xalign 0.5
                                yalign 0.5
                        vbox:
                            yalign 0.5
                            xsize gui.scale(136)
                            spacing gui.scale(6)
                            text attribute_name(attribute_id).upper():
                                style "phone_heading"
                                size gui.scale(17)
                                kerning gui.scale(1)
                                bold True
                                color orb_color
                            text "RANK [orb_rank:02d] / 05" style "phone_detail" size gui.scale(10)
                            text attribute_rank_next_text(attribute_id) style "phone_detail"
                    text attribute_blurb(attribute_id) style "phone_detail"
                    hbox:
                        xfill True
                        text "TOTAL" style "phone_detail" size gui.scale(10)
                        text attribute_total_text(attribute_id):
                            style "phone_detail"
                            xalign 1.0
                            color orb_color
                    add Solid("#ffffff14") xysize (gui.scale(224), gui.scale(1))

screen phone_help():
    default device = "keyboard"
    use game_menu(_("Help")):
        vbox:
            spacing gui.scale(12)
            hbox:
                textbutton _("Keys") style "phone_small_button" action SetLocalVariable("device", "keyboard")
                textbutton _("Mouse") style "phone_small_button" action SetLocalVariable("device", "mouse")
                if GamepadExists():
                    textbutton _("Pad") style "phone_small_button" action SetLocalVariable("device", "gamepad")
            if device == "keyboard":
                $ bindings = [
                    (_("Enter"), _("Advance dialogue or activate a control.")),
                    (_("Space"), _("Advance dialogue.")),
                    (_("Arrow Keys"), _("Navigate controls.")),
                    (_("Escape"), _("Open or close the menu.")),
                    (_("Ctrl / Tab"), _("Hold to skip / toggle skipping.")),
                    (_("Page Up / Down"), _("Roll back / roll forward.")),
                    ("H", _("Hide the interface.")),
                    ("S", _("Take a screenshot.")),
                    ("V", _("Toggle self-voicing.")),
                    ("Shift+A", _("Open accessibility settings.")),
                ]
            elif device == "mouse":
                $ bindings = [
                    (_("Left Click"), _("Advance dialogue or activate a control.")),
                    (_("Middle Click"), _("Hide the interface.")),
                    (_("Right Click"), _("Disabled during gameplay.")),
                    (_("Mouse Wheel"), _("Roll back / roll forward.")),
                ]
            else:
                $ bindings = [
                    (_("A / Right Trigger"), _("Advance dialogue or activate a control.")),
                    (_("Left Shoulder"), _("Roll back.")),
                    (_("Right Shoulder"), _("Roll forward.")),
                    (_("D-Pad / Sticks"), _("Navigate controls.")),
                    (_("Start / B"), _("Open or close the menu.")),
                    ("Y", _("Hide the interface.")),
                ]
            for caption, description in bindings:
                text caption style "phone_heading"
                text description style "phone_body"
                null height gui.scale(6)
            if device == "gamepad":
                textbutton _("Calibrate") style "phone_option" action GamepadCalibrate()

screen phone_confirm(message, yes_action, no_action):
    use phone_backdrop
    use phone_hardware:
        use phone_status
    fixed:
        xpos gui.scale(menu_phone_x + 14)
        ypos gui.scale(menu_phone_y + 80)
        xysize (gui.scale(menu_phone_content_w), gui.scale(520))
        add Solid("#1c1b18")
        vbox:
            ypos gui.scale(74)
            xsize gui.scale(230)
            spacing gui.scale(22)
            text _("Confirm") style "phone_heading"
            text _(message) style "phone_body"
            textbutton _("Yes") style "phone_option" action yes_action
            textbutton _("No") style "phone_option" action no_action

screen _accessibility():
    layer config.interface_layer
    zorder 2000
    modal True
    use phone_game_menu(_("Accessibility"), back_action=Hide("_accessibility"), show_navigation=False):
        vbox:
            spacing gui.scale(12)
            text _("Self-Voicing") style "phone_heading"
            textbutton _("Off") style "phone_option" action Preference("self voicing", "disable")
            textbutton _("Text-to-speech") style "phone_option" action Preference("self voicing", "enable")
            textbutton _("Clipboard") style "phone_option" action Preference("clipboard voicing", "enable")
            textbutton _("Debug") style "phone_option" action Preference("debug voicing", "enable")
            if renpy.variant("touch"):
                text _("Self-voicing support is limited on touch screens.") style "phone_detail"
            text _("Voice Volume") style "phone_heading"
            bar value Preference("voice volume") style "phone_slider"
            textbutton _("Reset Voice Volume") style "phone_small_button" action Preference("voice volume", 1.0)
            text _("Self-Voicing Volume Drop") style "phone_heading"
            bar value Preference("self voicing volume drop") style "phone_slider"
            textbutton _("Reset Volume Drop") style "phone_small_button" action Preference("self voicing volume drop", 0.5)
            text _("Mono Audio") style "phone_heading"
            textbutton _("Enable") style "phone_option" action Preference("mono audio", "enable")
            textbutton _("Disable") style "phone_option" action Preference("mono audio", "disable")
            text _("Font Override") style "phone_heading"
            textbutton _("Default") style "phone_option" action Preference("font transform", None)
            textbutton _("DejaVu Sans") style "phone_option" action Preference("font transform", "dejavusans")
            textbutton _("OpenDyslexic") style "phone_option" action Preference("font transform", "opendyslexic")
            text _("High Contrast Text") style "phone_heading"
            textbutton _("Enable") style "phone_option" action Preference("high contrast text", "enable")
            textbutton _("Disable") style "phone_option" action Preference("high contrast text", "disable")
            text _("Text Size") style "phone_heading"
            bar value Preference("font size") style "phone_slider"
            textbutton _("Reset Text Size") style "phone_small_button" action Preference("font size", 1.0)
            text _("Line Spacing") style "phone_heading"
            bar value Preference("font line spacing") style "phone_slider"
            textbutton _("Reset Line Spacing") style "phone_small_button" action Preference("font line spacing", 1.0)
            text _("Kerning") style "phone_heading"
            bar value Preference("font kerning") style "phone_slider"
            textbutton _("Reset Kerning") style "phone_small_button" action Preference("font kerning", 0.0)
            text _("Some font and text-size combinations may make controls difficult to read. Reset the settings if needed.") style "phone_detail"
    key "game_menu" action Hide("_accessibility")

screen _gamepad_select(joysticks):
    layer config.interface_layer
    modal True
    use phone_game_menu(_("Controller"), back_action=Return("cancel"), show_navigation=False):
        vbox:
            spacing gui.scale(16)
            text _("Select a controller to calibrate.") style "phone_body"
            if not joysticks:
                text _("No controllers available.") style "phone_detail"
            for i, name in joysticks:
                textbutton "[i]: [name]" style "phone_option" action Return(i)
    key "game_menu" action Return("cancel")

screen _gamepad_control(name, control, kind, mappings, back, i, total):
    layer config.interface_layer
    modal True
    use phone_game_menu(_("Calibration"), back_action=Return("cancel"), show_navigation=False):
        vbox:
            spacing gui.scale(16)
            text "[name] ([i]/[total])" style "phone_heading"
            text _("Press or move the '[control!s]' [kind].") style "phone_body"
            if len(mappings) >= 2:
                textbutton _("Skip (A)") style "phone_option" action Return("skip")
            if back and len(mappings) >= 3:
                textbutton _("Back (B)") style "phone_option" action Return(back)
    add _gamepad.EventWatcher(mappings)
    key "game_menu" action Return("cancel")

style phone_body is gui_text:
    font menu_phone_font
    size gui.scale(16)
    color "#eee8dd"
    outlines []
    xmaximum gui.scale(230)

style phone_detail is phone_body:
    size gui.scale(12)
    color "#b4ada1"

style phone_status is phone_detail:
    font "DejaVuSans.ttf"
    size gui.scale(9)

style phone_heading is phone_body:
    size gui.scale(19)
    color "#f4eee4"

style phone_brand is phone_heading:
    font "DejaVuSans.ttf"
    size gui.scale(27)
    kerning gui.scale(-1)

style phone_row is button:
    xfill True
    yminimum gui.scale(45)
    background None
    hover_background Solid("#ffffff0d")
    padding (gui.scale(6), gui.scale(9))

style phone_row_text is phone_body:
    size gui.scale(18)
    hover_color "#e7c08d"
    insensitive_color "#686257"

style phone_small_button is button:
    background None
    hover_background Solid("#ffffff12")
    padding (gui.scale(5), gui.scale(7))

style phone_small_button_text is phone_detail:
    size gui.scale(14)
    color "#d8b580"
    hover_color "#fff2dc"
    selected_color "#fff2dc"
    insensitive_color "#686257"

style phone_page_button is phone_small_button:
    xsize gui.scale(42)

style phone_option is phone_row:
    background Solid("#ffffff08")
    selected_background Solid("#c8a06a25")

style phone_option_text is phone_row_text:
    selected_color "#e7c08d"

style phone_save_button is phone_option:
    padding (gui.scale(8), gui.scale(10))
    ysize gui.scale(212)

style phone_item is phone_option:
    xsize gui.scale(110)
    yminimum gui.scale(112)
    padding (gui.scale(8), gui.scale(8))

style phone_slider is slider:
    xsize gui.scale(224)
    ysize gui.scale(22)
    left_bar Solid("#c8a06a")
    right_bar Solid("#ffffff20")
    thumb Transform(Solid("#f2e4cc"), xysize=(gui.scale(4), gui.scale(22)))
    thumb_shadow None
    thumb_offset gui.scale(3)

style phone_progress is bar:
    xsize gui.scale(224)
    ysize gui.scale(5)
    left_bar Solid("#c8a06a")
    right_bar Solid("#ffffff20")
    thumb None
    thumb_shadow None

style phone_viewport is viewport:
    xfill False
    yfill False

style phone_blocker is button:
    background Solid("#1c1b18")
    hover_background Solid("#1c1b18")
    padding (0, 0)

style phone_page_button_text is phone_small_button_text:
    xalign 0.5

style phone_side is side:
    spacing gui.scale(6)

style phone_vscrollbar is vscrollbar:
    xsize gui.scale(3)
    base_bar Solid("#ffffff08")
    thumb Solid("#c8a06a80")
    unscrollable "hide"

style phone_start is button:
    background None
    hover_background None
    padding (gui.scale(24), gui.scale(20))

style phone_start_text is gui_text:
    font "DejaVuSans.ttf"
    size gui.scale(26)
    color "#f4eee4"
    hover_color "#e7c08d"
    kerning gui.scale(3)
    outlines [(gui.scale(2), "#00000080", 0, gui.scale(2))]

# The remaining text pages use the shared shell, but need narrow text geometry.
style about_text:
    font menu_phone_font
    size gui.scale(16)
    xmaximum gui.scale(226)
    outlines []

style about_label_text:
    font menu_phone_font
    size gui.scale(22)
    outlines []

style history_window:
    ysize None
    bottom_padding gui.scale(22)

style history_name:
    xpos 0
    ypos 0
    xanchor 0.0
    xsize gui.scale(226)

style history_name_text:
    font menu_phone_font
    size gui.scale(17)
    min_width 0
    textalign 0.0

style history_text:
    font menu_phone_font
    xpos 0
    ypos gui.scale(28)
    xanchor 0.0
    xsize gui.scale(226)
    min_width 0
    size gui.scale(16)
    textalign 0.0
    outlines []

style history_label_text:
    size gui.scale(16)
    xmaximum gui.scale(226)
