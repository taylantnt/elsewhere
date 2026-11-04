################################################################################
## PHONE APPS
##
## A separate app launcher for the in-game quick menu. These screens read the
## same story data as the existing menus, but do not replace or redirect them.
################################################################################

init python:
    import time

    phone_apps_catalog = [
        ("messages", "Messages", True),
        ("wire", "WIRE", False),
        ("settings", "Settings", False),
        ("camera", "Camera", True),
        ("inventory", "Inventory", False),
        ("stats", "Stats", False),
        ("journal", "Journal", False),
        ("backup", "Backup", False),
    ]

    def apps_open():
        renpy.call_in_new_context("_phone_apps_open")

    def phone_apps_begin_close():
        if store.phone_apps_closing:
            return

        elapsed = time.monotonic() - store.phone_apps_started_at
        progress = min(1.0, max(0.0, elapsed / 0.95))
        store.phone_apps_close_offset = gui.scale(int(760 * (1.0 - progress) ** 5))
        store.phone_apps_close_alpha = min(1.0, max(0.0, (elapsed - 0.55) / 0.3))
        store.phone_apps_closed_at = time.monotonic()
        store.phone_apps_closing = True


default phone_apps_page = None
default phone_apps_wire_profile = None
default phone_apps_inventory_item = None
default phone_apps_inventory_open = False
default phone_apps_backup_mode = None
default phone_apps_settings_tab = "general"
default phone_apps_started_at = 0.0
default phone_apps_closing = False
default phone_apps_closed_at = 0.0
default phone_apps_close_offset = 0
default phone_apps_close_alpha = 1.0


label _phone_apps_open:
    $ phone_apps_page = None
    $ phone_apps_wire_profile = None
    $ phone_apps_inventory_item = None
    $ phone_apps_inventory_open = False
    $ phone_apps_backup_mode = None
    $ phone_apps_settings_tab = "general"
    $ phone_apps_started_at = time.monotonic()
    $ phone_apps_closing = False
    $ phone_apps_close_offset = 0
    $ phone_apps_close_alpha = 1.0
    call screen phone_apps
    return


screen phone_app_icon(app_id, size=48, disabled=False):
    fixed:
        xysize (gui.scale(size), gui.scale(size))
        if app_id == "wire":
            add Transform("images/ui/apps/wire_app.png", xysize=(gui.scale(size), gui.scale(size)), fit="contain")
        else:
            $ icon_suffix = "_disabled" if disabled else ""
            add Transform("images/ui/apps/%s%s.png" % (app_id, icon_suffix), xysize=(gui.scale(size), gui.scale(size)), fit="contain")


screen phone_app_tile(app_id, label, disabled, action):
    button:
        xysize (gui.scale(74), gui.scale(112))
        background None
        hover_background Solid("#ffffff0b")
        action action

        fixed:
            xysize (gui.scale(74), gui.scale(112))
            fixed:
                xalign 0.5
                ypos gui.scale(6)
                xysize (gui.scale(60), gui.scale(60))
                use phone_app_icon(app_id, 60, disabled)

            text label:
                xalign 0.5
                ypos gui.scale(73)
                xmaximum gui.scale(72)
                textalign 0.5
                size gui.scale(11)
                color ("#a5afb6" if disabled else "#e4e9ec")
                outlines []


screen phone_app_wire_contents(selected_contact):
    if wire_unlocked:
        $ contact_ids = [cid for cid in wire_order if cid in wire_unlocked]

        if selected_contact in wire_unlocked:
            $ contact = wire_contacts[selected_contact]
            $ contact_color = contact["color"]
            $ contact_memories = character_memories.get(selected_contact, [])

            viewport:
                xfill True
                yfill True
                mousewheel True
                draggable True
                style_prefix "phone_apps"
                scrollbars "vertical"
                vbox:
                    spacing gui.scale(11)

                    use wire_avatar(selected_contact, gui.scale(54))

                    text contact["name"]:
                        size gui.scale(18)
                        color "#e8eef2"
                        outlines []

                    text contact["handle"]:
                        size gui.scale(13)
                        color contact_color
                        outlines []

                    add Solid("#243139") xysize (gui.scale(210), 1)

                    text contact["note"]:
                        size gui.scale(14)
                        color "#c3ccd5"
                        xmaximum gui.scale(210)
                        outlines []

                    hbox:
                        spacing gui.scale(5)
                        use wire_meter(wire_progress(selected_contact), gui.scale(5), gui.scale(10), contact_color)
                        text "[wire_progress(selected_contact)] / [confidant_visits_total]":
                            size gui.scale(11)
                            color "#8c9aa4"
                            outlines []

                    add Solid("#243139") xysize (gui.scale(210), 1)
                    text "WHAT THEY REMEMBER":
                        size gui.scale(11)
                        kerning gui.scale(1)
                        color "#71808b"
                        outlines []

                    if contact_memories:
                        for note in contact_memories:
                            text note:
                                size gui.scale(13)
                                color "#c3ccd5"
                                xmaximum gui.scale(210)
                                outlines []
                    else:
                        text "Nothing yet.":
                            size gui.scale(13)
                            italic True
                            color "#75838d"
                            outlines []
        else:
            viewport:
                xfill True
                yfill True
                mousewheel True
                draggable True
                style_prefix "phone_apps"
                scrollbars "vertical"
                vbox:
                    spacing gui.scale(10)

                    fixed:
                        xfill True
                        ysize gui.scale(35)
                        text "CONNECTIONS":
                            yalign 0.5
                            size gui.scale(12)
                            kerning gui.scale(2)
                            color "#71808b"
                            outlines []
                        text ("LTE" if cellular_data_active else "OFFLINE"):
                            xalign 1.0
                            yalign 0.5
                            size gui.scale(11)
                            color ("#7fe0d0" if cellular_data_active else "#75838d")
                            outlines []

                    for cid in contact_ids:
                        $ contact = wire_contacts[cid]
                        $ seen = wire_progress(cid)
                        button:
                            xfill True
                            ysize gui.scale(82)
                            background Solid("#141c22")
                            hover_background Solid("#1a282d")
                            action [SetVariable("phone_apps_wire_profile", cid), With(Dissolve(0.16))]

                            fixed:
                                xysize (gui.scale(210), gui.scale(82))
                                add Solid(contact["color"] + "66") xysize (gui.scale(3), gui.scale(82))
                                fixed:
                                    xpos gui.scale(10)
                                    yalign 0.5
                                    xysize (gui.scale(46), gui.scale(46))
                                    use wire_avatar(cid, gui.scale(46))
                                vbox:
                                    xpos gui.scale(66)
                                    ypos gui.scale(12)
                                    spacing gui.scale(3)
                                    text contact["name"]:
                                        size gui.scale(13)
                                        color "#e8eef2"
                                        outlines []
                                    text contact["handle"]:
                                        size gui.scale(11)
                                        color contact["color"]
                                        outlines []
                                    text "[seen] / [confidant_visits_total] visits":
                                        size gui.scale(10)
                                        color "#83909a"
                                        outlines []
    else:
        vbox:
            xalign 0.5
            yalign 0.5
            spacing gui.scale(10)
            text "No contacts yet.":
                xalign 0.5
                size gui.scale(15)
                color "#dce4e8"
                outlines []
            text "People you meet will appear here.":
                xalign 0.5
                textalign 0.5
                size gui.scale(13)
                color "#83909a"
                outlines []


screen phone_app_journal_contents():
    predict False
    viewport:
        xfill True
        yfill True
        mousewheel True
        draggable True
        pagekeys True
        yinitial 1.0
        style_prefix "phone_apps"
        scrollbars "vertical"
        vbox:
            spacing gui.scale(10)
            text "RECENT MOMENTS":
                size gui.scale(12)
                kerning gui.scale(2)
                color "#71808b"
                outlines []

            if _history_list:
                for entry in reversed(_history_list):
                    vbox:
                        xfill True
                        spacing gui.scale(4)

                        if entry.who:
                            text entry.who:
                                size gui.scale(13)
                                color (entry.who_args.get("color", "#7fc8bd"))
                                outlines []

                        $ journal_text = renpy.filter_text_tags(entry.what, allow=gui.history_allow_tags)
                        text journal_text:
                            size gui.scale(14)
                            color "#d0d8dd"
                            xmaximum gui.scale(218)
                            substitute False
                            outlines []

                        add Solid("#243139") xysize (gui.scale(218), gui.scale(1))
            else:
                text "There are no recorded lines yet.":
                    size gui.scale(14)
                    color "#a7b5c1"
                    outlines []


screen phone_app_inventory_contents(selected_item):
    if selected_item in inventory and phone_apps_inventory_open:
        vbox:
            xfill True
            spacing gui.scale(12)
            add item_icon(selected_item, gui.scale(194)) xalign 0.5
            text item_name(selected_item):
                xalign 0.5
                size gui.scale(18)
                color "#f4eee4"
                outlines []
            text item_desc(selected_item):
                size gui.scale(15)
                color "#d0c8bd"
                xmaximum gui.scale(220)
                outlines []
            textbutton "CLOSE ITEM":
                style "phone_option"
                action [SetVariable("phone_apps_inventory_open", False), With(Dissolve(0.16))]
    elif selected_item in inventory:
        viewport:
            xfill True
            yfill True
            mousewheel True
            draggable True
            style_prefix "phone_apps"
            scrollbars "vertical"
            vbox:
                spacing gui.scale(12)
                add item_icon(selected_item, gui.scale(136)) xalign 0.5
                text item_name(selected_item):
                    size gui.scale(16)
                    color "#f4eee4"
                    outlines []
                text item_desc(selected_item):
                    size gui.scale(14)
                    color "#b4ada1"
                    xmaximum gui.scale(218)
                    outlines []
                text ("AVAILABLE TO OPEN" if item_usable(selected_item) else "CARRIED ITEM"):
                    size gui.scale(11)
                    kerning gui.scale(1)
                    color ("#8fd694" if item_usable(selected_item) else "#77838c")
                    outlines []
                if item_usable(selected_item):
                    textbutton item_use_label(selected_item).upper():
                        style "phone_option"
                        action [SetVariable("phone_apps_inventory_open", True), With(Dissolve(0.16))]
                else:
                    text "This item cannot be used.":
                        size gui.scale(13)
                        color "#87939b"
                        outlines []
    else:
        viewport:
            xfill True
            yfill True
            mousewheel True
            draggable True
            style_prefix "phone_apps"
            scrollbars "vertical"
            vbox:
                spacing gui.scale(9)
                text "WALLET":
                    size gui.scale(12)
                    kerning gui.scale(2)
                    color "#71808b"
                    outlines []
                text "¥ [money]":
                    size gui.scale(18)
                    color "#e7c08d"
                    outlines []
                add Solid("#243139") xysize (gui.scale(210), 1)

                if inventory:
                    for item in inventory:
                        button:
                            xfill True
                            yminimum gui.scale(76)
                            background Solid("#141c22")
                            hover_background Solid("#1a282d")
                            action [
                                SetVariable("phone_apps_inventory_item", item),
                                SetVariable("phone_apps_inventory_open", False),
                                With(Dissolve(0.16)),
                            ]
                            hbox:
                                spacing gui.scale(12)
                                add item_icon(item, gui.scale(54)) yalign 0.5
                                vbox:
                                    yalign 0.5
                                    spacing gui.scale(3)
                                    text item_name(item):
                                        size gui.scale(14)
                                        color "#e8eef2"
                                        outlines []
                                    text ("OPEN" if item_usable(item) else "IN BAG"):
                                        size gui.scale(10)
                                        kerning gui.scale(1)
                                        color "#82909a"
                                        outlines []
                else:
                    text "The bag is empty.":
                        size gui.scale(14)
                        color "#a7b5c1"
                        outlines []


screen phone_app_stats_contents():
    viewport:
        xfill True
        yfill True
        mousewheel True
        draggable True
        style_prefix "phone_apps"
        scrollbars "vertical"
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
                            text "RANK [orb_rank:02d] / 05":
                                style "phone_detail"
                                size gui.scale(12)
                            text attribute_rank_next_text(attribute_id):
                                style "phone_detail"
                                size gui.scale(12)
                    text attribute_blurb(attribute_id):
                        style "phone_detail"
                        size gui.scale(13)
                    hbox:
                        xfill True
                        text "TOTAL" style "phone_detail" size gui.scale(12)
                        text attribute_total_text(attribute_id):
                            style "phone_detail"
                            xalign 1.0
                            size gui.scale(13)
                            color orb_color
                    add Solid("#ffffff14") xysize (gui.scale(224), gui.scale(1))


screen phone_app_backup_contents(mode, page_value):
    if mode is None:
        vbox:
            xfill True
            ypos gui.scale(14)
            spacing gui.scale(10)
            text "SAVE OR RESTORE":
                size gui.scale(12)
                kerning gui.scale(2)
                color "#71808b"
                outlines []
            text "Choose what you want to do with your story.":
                size gui.scale(14)
                color "#b4ada1"
                xmaximum gui.scale(210)
                outlines []
            textbutton "SAVE GAME":
                style "phone_option"
                action [SetVariable("phone_apps_backup_mode", "save"), With(Dissolve(0.16))]
            textbutton "LOAD GAME":
                style "phone_option"
                action [SetVariable("phone_apps_backup_mode", "load"), With(Dissolve(0.16))]
    else:
        vbox:
            xfill True
            spacing gui.scale(6)
            button:
                xfill True
                ysize gui.scale(28)
                background Solid("#141c22")
                hover_background Solid("#1a282d")
                action page_value.Toggle()
                key_events True
                input:
                    style "phone_detail"
                    value page_value
                    length 24
            hbox:
                xalign 0.5
                spacing gui.scale(4)
                textbutton "<" style "phone_small_button" action FilePagePrevious()
                if config.has_autosave:
                    textbutton "A" style "phone_small_button" action FilePage("auto")
                if config.has_quicksave:
                    textbutton "Q" style "phone_small_button" action FilePage("quick")
                textbutton ">" style "phone_small_button" action FilePageNext()
            vpgrid:
                cols 5
                xalign 0.5
                spacing gui.scale(2)
                for page in range(1, 10):
                    textbutton "[page]":
                        style "phone_page_button"
                        action FilePage(page)

            viewport:
                xfill True
                ysize gui.scale(342)
                mousewheel True
                draggable True
                style_prefix "phone_apps"
                scrollbars "vertical"
                vbox:
                    spacing gui.scale(7)
                    for slot in range(1, gui.file_slot_cols * gui.file_slot_rows + 1):
                        button:
                            xfill True
                            ysize gui.scale(118)
                            background Solid("#141c22")
                            hover_background Solid("#1a282d")
                            sensitive (mode == "save" or FileLoadable(slot))
                            action (FileSave(slot) if mode == "save" else FileLoad(slot))
                            vbox:
                                spacing gui.scale(4)
                                add FileScreenshot(slot):
                                    xysize (gui.scale(202), gui.scale(74))
                                text (FileSaveName(slot) or "Empty slot"):
                                    size gui.scale(12)
                                    color "#e8eef2"
                                    outlines []
                                text FileTime(slot, format="%Y-%m-%d  %H:%M", empty="No save data"):
                                    size gui.scale(10)
                                    color "#83909a"
                                    outlines []


screen phone_app_settings_contents(tab):
    vbox:
        spacing gui.scale(8)
        hbox:
            xfill True
            textbutton "GENERAL":
                style "phone_small_button"
                text_color ("#e7c08d" if tab == "general" else "#aab4bb")
                action [SetVariable("phone_apps_settings_tab", "general"), With(Dissolve(0.16))]
            textbutton "ACCESSIBILITY":
                style "phone_small_button"
                text_color ("#e7c08d" if tab == "accessibility" else "#aab4bb")
                action [SetVariable("phone_apps_settings_tab", "accessibility"), With(Dissolve(0.16))]

        viewport:
            xfill True
            ysize gui.scale(425)
            mousewheel True
            draggable True
            style_prefix "phone_apps"
            scrollbars "vertical"
            vbox:
                spacing gui.scale(9)

                if tab == "general":
                    if renpy.variant("pc") or renpy.variant("web"):
                        text "DISPLAY" style "phone_heading" size gui.scale(13)
                        textbutton "Window" style "phone_option" action Preference("display", "window")
                        textbutton "Fullscreen" style "phone_option" action Preference("display", "fullscreen")

                    text "SKIP" style "phone_heading" size gui.scale(13)
                    textbutton "Unseen Text" style "phone_option" action Preference("skip", "toggle")
                    textbutton "After Choices" style "phone_option" action Preference("after choices", "toggle")
                    textbutton "Transitions" style "phone_option" action InvertSelected(Preference("transitions", "toggle"))

                    text "TEXT SPEED" style "phone_heading" size gui.scale(13)
                    bar value Preference("text speed") style "phone_slider"
                    text "Auto-Forward Time" style "phone_detail"
                    bar value Preference("auto-forward time") style "phone_slider"

                    text "VOLUME" style "phone_heading" size gui.scale(13)
                    if config.has_music:
                        text "Music" style "phone_detail"
                        bar value Preference("music volume") style "phone_slider"
                    if config.has_sound:
                        text "Sound Effects" style "phone_detail"
                        bar value Preference("sound volume") style "phone_slider"
                        if config.sample_sound:
                            textbutton "Test Sound" style "phone_option" action Play("sound", config.sample_sound)
                    if config.has_voice:
                        text "Voice" style "phone_detail"
                        bar value Preference("voice volume") style "phone_slider"
                        if config.sample_voice:
                            textbutton "Test Voice" style "phone_option" action Play("voice", config.sample_voice)
                    textbutton "Mute All" style "phone_option" action Preference("all mute", "toggle")

                else:
                    text "SELF-VOICING" style "phone_heading" size gui.scale(13)
                    textbutton "Off" style "phone_option" action Preference("self voicing", "disable")
                    textbutton "Text-to-speech" style "phone_option" action Preference("self voicing", "enable")
                    textbutton "Clipboard" style "phone_option" action Preference("clipboard voicing", "enable")
                    textbutton "Debug" style "phone_option" action Preference("debug voicing", "enable")
                    text "Voice Volume" style "phone_detail"
                    bar value Preference("voice volume") style "phone_slider"
                    textbutton "Reset Voice Volume" style "phone_small_button" action Preference("voice volume", 1.0)
                    text "Self-Voicing Volume Drop" style "phone_detail"
                    bar value Preference("self voicing volume drop") style "phone_slider"
                    textbutton "Reset Volume Drop" style "phone_small_button" action Preference("self voicing volume drop", 0.5)
                    text "MONO AUDIO" style "phone_heading" size gui.scale(13)
                    textbutton "Enable Mono Audio" style "phone_option" action Preference("mono audio", "enable")
                    textbutton "Disable Mono Audio" style "phone_option" action Preference("mono audio", "disable")
                    text "FONT OVERRIDE" style "phone_heading" size gui.scale(13)
                    textbutton "Default" style "phone_option" action Preference("font transform", None)
                    textbutton "DejaVu Sans" style "phone_option" action Preference("font transform", "dejavusans")
                    textbutton "OpenDyslexic" style "phone_option" action Preference("font transform", "opendyslexic")
                    text "HIGH CONTRAST TEXT" style "phone_heading" size gui.scale(13)
                    textbutton "Enable" style "phone_option" action Preference("high contrast text", "enable")
                    textbutton "Disable" style "phone_option" action Preference("high contrast text", "disable")
                    text "Text Size" style "phone_detail"
                    bar value Preference("font size") style "phone_slider"
                    textbutton "Reset Text Size" style "phone_small_button" action Preference("font size", 1.0)
                    text "Line Spacing" style "phone_detail"
                    bar value Preference("font line spacing") style "phone_slider"
                    textbutton "Reset Line Spacing" style "phone_small_button" action Preference("font line spacing", 1.0)
                    text "Kerning" style "phone_detail"
                    bar value Preference("font kerning") style "phone_slider"
                    textbutton "Reset Kerning" style "phone_small_button" action Preference("font kerning", 0.0)
                    text "Some font and text-size combinations may make controls difficult to read.":
                        style "phone_detail"
                        xmaximum gui.scale(210)


screen phone_apps():
    modal True
    zorder 130
    default backup_page_value = FilePageNameInputValue(pattern="Page {}", auto="Automatic saves", quick="Quick saves")

    add Solid("#030609d8")

    use phone_hardware(
        animate=True,
        raised_at=phone_apps_started_at,
        closing=phone_apps_closing,
        closing_at=phone_apps_closed_at,
        close_offset=phone_apps_close_offset,
        close_alpha=phone_apps_close_alpha,
    ):
        add "images/ui/apps/phone_screen.png":
            xysize (gui.scale(menu_phone_w), gui.scale(menu_phone_h))
        use phone_status

        fixed:
            xpos gui.scale(14)
            ypos gui.scale(34)
            xysize (gui.scale(menu_phone_content_w), gui.scale(548))

            fixed:
                xfill True
                ysize gui.scale(38)
                if phone_apps_page is not None:
                    textbutton "<":
                        style "phone_small_button"
                        xsize gui.scale(34)
                        yalign 0.5
                        action (
                            [SetVariable("phone_apps_wire_profile", None), With(Dissolve(0.16))]
                            if phone_apps_page == "wire" and phone_apps_wire_profile else
                            [SetVariable("phone_apps_inventory_open", False), With(Dissolve(0.16))]
                            if phone_apps_page == "inventory" and phone_apps_inventory_open else
                            [SetVariable("phone_apps_inventory_item", None), With(Dissolve(0.16))]
                            if phone_apps_page == "inventory" and phone_apps_inventory_item else
                            [SetVariable("phone_apps_backup_mode", None), With(Dissolve(0.16))]
                            if phone_apps_page == "backup" and phone_apps_backup_mode else
                            [SetVariable("phone_apps_page", None), With(Dissolve(0.16))]
                        )

                $ app_titles = {
                    None: "Apps",
                    "messages": "Messages",
                    "wire": "WIRE",
                    "settings": "Settings",
                    "camera": "Camera",
                    "inventory": "Inventory",
                    "stats": "Stats",
                    "journal": "Journal",
                    "backup": ("Cloud / " + phone_apps_backup_mode.title() if phone_apps_backup_mode else "Cloud"),
                }

                text app_titles[phone_apps_page]:
                    xalign 0.5
                    yalign 0.5
                    xmaximum gui.scale(172)
                    textalign 0.5
                    size gui.scale(15)
                    color "#f0eee8"
                    outlines []

                textbutton "×":
                    style "phone_small_button"
                    xalign 1.0
                    yalign 0.5
                    sensitive not phone_apps_closing
                    action Function(phone_apps_begin_close)

            add Solid("#ffffff16") ypos gui.scale(42) xysize (gui.scale(menu_phone_content_w), gui.scale(1))

            fixed:
                xpos 0
                ypos gui.scale(50)
                xysize (gui.scale(menu_phone_content_w), gui.scale(474))

                if phone_apps_page is None:
                    vbox:
                        xalign 0.5
                        ypos gui.scale(15)
                        spacing gui.scale(10)

                        text "YOUR PHONE":
                            xalign 0.5
                            size gui.scale(12)
                            kerning gui.scale(2)
                            color "#71808b"
                            outlines []

                        grid 3 3:
                            xalign 0.5
                            spacing gui.scale(5)

                            for app_id, app_name, disabled in phone_apps_catalog:
                                use phone_app_tile(
                                    app_id,
                                    app_name,
                                    disabled,
                                    [SetVariable("phone_apps_page", app_id), With(Dissolve(0.16))],
                                )

                            null width gui.scale(74) height gui.scale(112)

                        text "A few apps are still finding their place.":
                            xalign 0.5
                            size gui.scale(11)
                            color "#64727e"
                            outlines []
                elif phone_apps_page in ("messages", "camera"):
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        spacing gui.scale(12)
                        use phone_app_icon(phone_apps_page, 72)
                        text "NOT AVAILABLE YET":
                            xalign 0.5
                            size gui.scale(14)
                            kerning gui.scale(1)
                            color "#dce4e8"
                            outlines []
                        text (
                            "Messages will be added later."
                            if phone_apps_page == "messages"
                            else "The camera is not available yet."
                        ):
                            xalign 0.5
                            textalign 0.5
                            xmaximum gui.scale(205)
                            size gui.scale(13)
                            color "#83909a"
                            outlines []
                elif phone_apps_page == "wire":
                    use phone_app_wire_contents(phone_apps_wire_profile)
                elif phone_apps_page == "inventory":
                    use phone_app_inventory_contents(phone_apps_inventory_item)
                elif phone_apps_page == "stats":
                    use phone_app_stats_contents
                elif phone_apps_page == "journal":
                    use phone_app_journal_contents
                elif phone_apps_page == "backup":
                    use phone_app_backup_contents(
                        phone_apps_backup_mode,
                        backup_page_value,
                    )
                elif phone_apps_page == "settings":
                    use phone_app_settings_contents(phone_apps_settings_tab)

            textbutton "CLOSE":
                style "phone_small_button"
                xalign 0.5
                yalign 1.0
                yoffset gui.scale(7)
                sensitive not phone_apps_closing
                action Function(phone_apps_begin_close)

    if phone_apps_closing:
        timer 0.70 action Return()

    key "game_menu" action Function(phone_apps_begin_close)
    key "rollback" action NullAction()


style phone_apps_vscrollbar is phone_vscrollbar:
    xsize gui.scale(8)
