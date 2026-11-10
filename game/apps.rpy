################################################################################
## PHONE APPS
##
## A separate app launcher for the in-game quick menu. These screens read the
## same story data as the existing menus, but do not replace or redirect them.
################################################################################

init python:
    import time

    phone_apps_catalog = [
        ("messages", "Messages", False),
        ("calendar", "Calendar", False),
        ("journal", "Journal", False),
        ("camera", "Camera", False),
        ("inventory", "Inventory", False),
        ("wire", "WIRE", False),
        ("stats", "Stats", False),
        ("maps", "Maps", False),
        ("backup", "Backup", False),
        ("settings", "Settings", False),
    ]

    # The map is the phone's index of the city. Every entry carries a neutral
    # description written by the app and a private note written by him. The
    # note only appears after he has been there, so an unvisited place never
    # speaks in his voice. Adding a location is one more dict: the list and the
    # pins both read from this one table.
    phone_map_locations = [
        {
            "id": "school",
            "name": "University Campus",
            "area": "Bunkyo",
            "summary": "A university campus in Bunkyo, built around a gate, a courtyard, and quiet lecture halls.",
            "note": "The campus where all of this is supposed to start. It still feels borrowed.",
            "image": "images/backgrounds/bg_school_gate.png",
            "position": (96, 22),
        },
        {
            "id": "photo_club",
            "name": "Photography Club",
            "area": "Campus, Circle Room",
            "summary": "A small circle room on campus, shared by the photography club and its noticeboards.",
            "note": "Sim's circle room. Everyone there already knows how to stand beside each other.",
            "image": "images/backgrounds/bg_photo_club.png",
            "position": (112, 38),
        },
        {
            "id": "ramen_shop",
            "name": "Ramen Shop",
            "area": "Side Street",
            "summary": "A counter shop on a side street, open late, with a handwritten menu and a single row of stools.",
            "note": "Chef's counter. I remember the bowl better than the walk there.",
            "image": "images/backgrounds/bg_ramen_shop.png",
            "position": (148, 28),
        },
        {
            "id": "akihabara",
            "name": "Akihabara",
            "area": "Chiyoda",
            "summary": "An electronics district of bright signs, crowded streets, and stacked department stores.",
            "note": "Hamada Denki, eight floors, and a city that never stops selling.",
            "image": "images/backgrounds/bg_akihabara_hamada_outside.png",
            "position": (170, 44),
        },
        {
            "id": "harajuku",
            "name": "Harajuku",
            "area": "Shibuya",
            "summary": "A district of narrow streets, small boutiques, and quieter alleys behind the main avenue.",
            "note": "I came for the clothes and stayed for the side streets.",
            "image": "images/backgrounds/bg_harajuku.png",
            "position": (60, 80),
        },
        {
            "id": "asakusa",
            "name": "Asakusa",
            "area": "Taito",
            "summary": "The old temple district, anchored by Kaminarimon and the long shopping street beyond it.",
            "note": "Incense, tourists, and a gate older than everything around it.",
            "image": "images/backgrounds/bg_asakusa_kaminarimon.png",
            "position": (188, 72),
        },
    ]

    def apps_open(page=None):
        store.phone_apps_start_page = page

        while True:
            renpy.call_in_new_context("_phone_apps_open")

            if not store.camera_shot_requested:
                break

            # The camera shutter closes the phone on purpose: the photo must not
            # contain any of it. The shot is taken from the game context, where
            # the dialogue is still up, and then the phone comes back to the
            # page the player was on.
            store.camera_shot_requested = False
            renpy.call_in_new_context("_camera_capture_after_phone", _clear_layers=False)
            store.phone_apps_start_page = "camera"

    def phone_map_visit(location_id):
        if location_id not in store.phone_map_unlocked:
            store.phone_map_unlocked.append(location_id)
        if location_id not in store.phone_map_visited:
            store.phone_map_visited.append(location_id)

    def phone_map_is_unlocked(location_id):
        if location_id in store.phone_map_unlocked:
            return True

        # Preserve map discoveries for saves made before this feature existed.
        if location_id == "ramen_shop":
            return store.confidant_visits.get("chef", 0) > 0
        if location_id == "photo_club":
            return (
                store.confidant_visits.get("sim", 0) > 0
                or getattr(store, "first_day_activity", None) == "photo_club"
            )
        if location_id == "akihabara":
            return store.cellular_data_active

        return False

    def phone_map_is_visited(location_id):
        if location_id in store.phone_map_visited:
            return True

        if location_id == "school":
            return (
                bool(getattr(store, "first_day_activity", None))
                or getattr(store, "current_act", 1) > 1
            )
        if location_id == "ramen_shop":
            return store.confidant_visits.get("chef", 0) > 0
        if location_id == "photo_club":
            return (
                store.confidant_visits.get("sim", 0) > 0
                or getattr(store, "first_day_activity", None) == "photo_club"
            )
        if location_id == "akihabara":
            return store.cellular_data_active

        return False

    def phone_map_place(location_id):
        for place in phone_map_locations:
            if place["id"] == location_id:
                return place

        return None

    # The map draws photographs into fixed boxes. Ren'Py's `fit` only
    # letterboxes, so a 3:2 photograph spills out of a 16:9 frame; crop the
    # source to the frame's ratio first, then scale that crop to the exact
    # size. Sizes are cached because renpy.image_size() decompresses the file.
    phone_map_image_sizes = {}

    def phone_map_image_size(path):
        if path not in phone_map_image_sizes:
            try:
                phone_map_image_sizes[path] = renpy.image_size(path)
            except Exception:
                phone_map_image_sizes[path] = (16, 9)

        return phone_map_image_sizes[path]

    def phone_map_photo(path, width, height, dim=False):
        source_w, source_h = phone_map_image_size(path)
        target = float(width) / float(height)
        source = float(source_w) / float(source_h)

        if source > target:
            frac = (source_h * target) / float(source_w)
            crop = ((1.0 - frac) / 2.0, 0.0, frac, 1.0)
        else:
            frac = (source_w / target) / float(source_h)
            crop = (0.0, (1.0 - frac) / 2.0, 1.0, frac)

        return Transform(
            path,
            crop=crop,
            crop_relative=True,
            xysize=(width, height),
            matrixcolor=SaturationMatrix(0.0) if dim else None,
        )

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
default phone_apps_start_page = None
default phone_apps_wire_profile = None
default phone_apps_messages_contact = None
default phone_apps_inventory_item = None
default phone_apps_inventory_open = False
default phone_apps_backup_mode = None
default phone_apps_settings_tab = "general"
default phone_apps_map_location = None
default phone_apps_more_open = False
default phone_apps_more_return_page = None
default phone_apps_help_device = "keyboard"
default phone_apps_started_at = 0.0
default phone_apps_closing = False
default phone_apps_closed_at = 0.0
default phone_apps_close_offset = 0
default phone_apps_close_alpha = 1.0
default phone_map_unlocked = ["school"]
default phone_map_visited = []


label _phone_apps_open:
    $ phone_apps_page = phone_apps_start_page
    $ phone_apps_start_page = None
    $ phone_apps_wire_profile = None
    $ phone_apps_messages_contact = None
    $ phone_apps_inventory_item = None
    $ phone_apps_inventory_open = False
    $ phone_apps_backup_mode = None
    $ phone_apps_settings_tab = "general"
    $ phone_apps_map_location = None
    $ phone_apps_more_open = False
    $ phone_apps_more_return_page = None
    $ phone_apps_help_device = "keyboard"
    $ phone_calendar_selected = None
    $ phone_calendar_month_offset = 0
    $ phone_apps_started_at = time.monotonic()
    $ phone_apps_closing = False
    $ phone_apps_close_offset = 0
    $ phone_apps_close_alpha = 1.0
    call screen phone_apps
    if _return == "camera_shot":
        $ camera_shot_requested = True
    return


screen phone_app_icon(app_id, size=48, disabled=False):
    fixed:
        xysize (gui.scale(size), gui.scale(size))
        if app_id == "wire":
            $ wire_icon_path = "images/ui/apps/wire_app_disabled.png" if disabled else "images/ui/apps/wire_app.png"
            add Transform(wire_icon_path, xysize=(gui.scale(size), gui.scale(size)), fit="contain")
        else:
            $ icon_suffix = "_disabled" if disabled else ""
            add Transform("images/ui/apps/%s%s.png" % (app_id, icon_suffix), xysize=(gui.scale(size), gui.scale(size)), fit="contain")


screen phone_app_tile(app_id, label, disabled, action):
    # The camera is only "disabled" until the story hands one over; the tile
    # still opens, so the player can read why it is dark.
    $ app_disabled = disabled or (app_id == "camera" and not camera_unlocked)

    button:
        xysize (gui.scale(74), gui.scale(94))
        background None
        hover_background Solid("#ffffff0b")
        action action
        sensitive (app_id not in ("messages", "maps", "wire", "calendar") or phone_app_unlocked(app_id))

        fixed:
            xysize (gui.scale(74), gui.scale(94))
            vbox:
                xalign 0.5
                yalign 0.5
                spacing gui.scale(6)

                use phone_app_icon(app_id, 54, app_disabled)

                text label:
                    xalign 0.5
                    xmaximum gui.scale(72)
                    textalign 0.5
                    size gui.scale(11)
                    color ("#a5afb6" if app_disabled else "#e4e9ec")
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

                    use wire_avatar(selected_contact, gui.scale(88))

                    text contact["name"]:
                        size gui.scale(27)
                        color "#e8eef2"
                        outlines []

                    text contact["handle"]:
                        size gui.scale(12)
                        color contact_color
                        outlines []

                    add Solid("#243139") xysize (gui.scale(210), 1)

                    text contact["note"]:
                        size gui.scale(15)
                        color "#c3ccd5"
                        xmaximum gui.scale(210)
                        outlines []

                    hbox:
                        spacing gui.scale(5)
                        use wire_meter(wire_progress(selected_contact), gui.scale(7), gui.scale(18), contact_color, wire_total(selected_contact))
                        text "[wire_progress(selected_contact)] / [wire_total(selected_contact)]":
                            size gui.scale(12)
                            color "#8c9aa4"
                            outlines []

                    add Solid("#243139") xysize (gui.scale(210), 1)
                    text "WHAT THEY REMEMBER":
                        size gui.scale(12)
                        kerning gui.scale(1)
                        color "#71808b"
                        outlines []

                    if contact_memories:
                        for note in contact_memories:
                            text note:
                                size gui.scale(15)
                                color "#c3ccd5"
                                xmaximum gui.scale(210)
                                outlines []
                    else:
                        text "Nothing yet.":
                            size gui.scale(15)
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
                    spacing gui.scale(9)

                    fixed:
                        xfill True
                        ysize gui.scale(35)
                        text "CONNECTIONS":
                            yalign 0.5
                            size gui.scale(12)
                            kerning gui.scale(2)
                            color "#71808b"
                            outlines []

                    add Solid("#243139") xysize (gui.scale(210), gui.scale(1))

                    for cid in contact_ids:
                        $ contact = wire_contacts[cid]
                        $ seen = wire_progress(cid)
                        button:
                            xfill True
                            ysize gui.scale(112)
                            background Solid("#141c22")
                            hover_background Solid("#1a282d")
                            action [SetVariable("phone_apps_wire_profile", cid), With(Dissolve(0.16))]

                            fixed:
                                xysize (gui.scale(210), gui.scale(112))
                                add Solid(contact["color"] + "66") xysize (gui.scale(3), gui.scale(112))
                                fixed:
                                    xpos gui.scale(14)
                                    yalign 0.5
                                    xysize (gui.scale(64), gui.scale(64))
                                    use wire_avatar(cid, gui.scale(64))
                                vbox:
                                    xpos gui.scale(88)
                                    ypos gui.scale(13)
                                    spacing gui.scale(3)
                                    text contact["name"]:
                                        size gui.scale(19)
                                        color "#e8eef2"
                                        outlines []
                                    text contact["handle"]:
                                        size gui.scale(14)
                                        color contact["color"]
                                        outlines []
                                hbox:
                                    xpos gui.scale(88)
                                    ypos gui.scale(82)
                                    spacing gui.scale(8)
                                    use wire_meter(seen, gui.scale(4), gui.scale(8), contact["color"], wire_total(cid))
                                    text "[seen] / [wire_total(cid)]":
                                        size gui.scale(12)
                                        kerning gui.scale(1)
                                        color "#5a6a76"
                                        yalign 0.5
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


## Maps opens on an index of the city: a small illustrated map, then every
## known place grouped by whether he has been there. The list is the primary
## navigation; the pins are a second way in. Both open the same detail page,
## which is why the list can grow to any number of locations while the map
## stays a fixed, decorative header.
screen phone_app_maps_contents():
    if phone_apps_map_location:
        use phone_app_map_detail(phone_apps_map_location)
    else:
        use phone_app_map_list


screen phone_app_map_list():
    $ map_width = gui.scale(menu_phone_content_w)
    $ map_visited = [place for place in phone_map_locations if phone_map_is_visited(place["id"])]
    $ map_unvisited = [place for place in phone_map_locations if not phone_map_is_visited(place["id"])]
    $ map_tip = GetTooltip()

    fixed:
        xysize (map_width, gui.scale(474))

        ## --- THE MAP ---
        fixed:
            xysize (map_width, gui.scale(126))
            add Solid("#0c161c")

            # City blocks, kept quiet so the pins do the talking.
            add Solid("#111f26") xpos gui.scale(14) ypos gui.scale(18) xysize (gui.scale(54), gui.scale(24))
            add Solid("#111f26") xpos gui.scale(78) ypos gui.scale(14) xysize (gui.scale(46), gui.scale(30))
            add Solid("#111f26") xpos gui.scale(140) ypos gui.scale(18) xysize (gui.scale(26), gui.scale(22))
            add Solid("#111f26") xpos gui.scale(176) ypos gui.scale(16) xysize (gui.scale(50), gui.scale(28))
            add Solid("#111f26") xpos gui.scale(12) ypos gui.scale(52) xysize (gui.scale(60), gui.scale(22))
            add Solid("#111f26") xpos gui.scale(84) ypos gui.scale(54) xysize (gui.scale(44), gui.scale(24))
            add Solid("#111f26") xpos gui.scale(138) ypos gui.scale(52) xysize (gui.scale(30), gui.scale(20))
            add Solid("#111f26") xpos gui.scale(180) ypos gui.scale(52) xysize (gui.scale(46), gui.scale(26))
            add Solid("#15261f") xpos gui.scale(14) ypos gui.scale(88) xysize (gui.scale(50), gui.scale(22))
            add Solid("#111f26") xpos gui.scale(74) ypos gui.scale(90) xysize (gui.scale(56), gui.scale(20))
            add Solid("#111f26") xpos gui.scale(142) ypos gui.scale(88) xysize (gui.scale(36), gui.scale(22))
            add Solid("#10242d") xpos gui.scale(188) ypos gui.scale(90) xysize (gui.scale(38), gui.scale(20))

            # Roads between them.
            add Solid("#1a2a32") xpos 0 ypos gui.scale(46) xysize (map_width, 2)
            add Solid("#1a2a32") xpos 0 ypos gui.scale(80) xysize (map_width, 2)
            add Solid("#1a2a32") xpos gui.scale(72) ypos 0 xysize (2, gui.scale(126))
            add Solid("#1a2a32") xpos gui.scale(134) ypos 0 xysize (2, gui.scale(126))
            add Solid("#1a2a32") xpos gui.scale(172) ypos 0 xysize (2, gui.scale(126))

            text "TOKYO":
                xpos gui.scale(8)
                ypos gui.scale(5)
                size gui.scale(10)
                kerning gui.scale(2)
                color "#8fa3ad"
                outlines []

            text "CITY MAP":
                xalign 1.0
                xoffset gui.scale(-8)
                ypos gui.scale(6)
                size gui.scale(9)
                kerning gui.scale(1)
                color "#55666f"
                outlines []

            for place in phone_map_locations:
                $ pin_visited = phone_map_is_visited(place["id"])
                $ pin_asset = "images/ui/apps/map_pin.png" if pin_visited else "images/ui/apps/map_pin_locked.png"
                button:
                    xpos gui.scale(place["position"][0] - 5)
                    ypos gui.scale(place["position"][1] - 5)
                    xysize (gui.scale(25), gui.scale(27))
                    background None
                    hover_background Solid("#c8a06a14")
                    tooltip place["name"]
                    action [
                        SetVariable("phone_apps_map_location", place["id"]),
                        With(Dissolve(0.14)),
                    ]
                    add pin_asset:
                        xalign 0.5
                        yalign 0.5
                        xysize (gui.scale(15), gui.scale(19))

            text (map_tip or "TAP A PIN TO OPEN"):
                xpos gui.scale(8)
                ypos gui.scale(110)
                size gui.scale(10)
                kerning gui.scale(1)
                color ("#d8b580" if map_tip else "#5c6d77")
                outlines []

        add Solid("#ffffff10") ypos gui.scale(126) xysize (map_width, 1)

        ## --- THE INDEX ---
        viewport:
            xpos 0
            ypos gui.scale(133)
            xysize (map_width, gui.scale(341))
            mousewheel True
            draggable True
            scrollbars "vertical"
            vscrollbar_xsize gui.scale(3)
            vscrollbar_base_bar Solid("#ffffff08")
            vscrollbar_thumb Solid("#c8a06a55")
            vscrollbar_unscrollable "hide"

            vbox:
                xsize (map_width - gui.scale(9))
                spacing gui.scale(1)

                use phone_app_map_group("VISITED", len(map_visited))

                if map_visited:
                    for place in map_visited:
                        use phone_app_map_row(place)
                else:
                    text "No places visited yet.":
                        xpos gui.scale(8)
                        ypos gui.scale(2)
                        size gui.scale(11)
                        color "#5c6b74"
                        outlines []

                null height gui.scale(5)

                use phone_app_map_group("NOT VISITED", len(map_unvisited))

                if map_unvisited:
                    for place in map_unvisited:
                        use phone_app_map_row(place)
                else:
                    text "Every known place has been visited.":
                        xpos gui.scale(8)
                        ypos gui.scale(2)
                        size gui.scale(11)
                        color "#5c6b74"
                        outlines []


screen phone_app_map_group(label, count):
    $ group_width = gui.scale(menu_phone_content_w) - gui.scale(9)

    fixed:
        xysize (group_width, gui.scale(26))

        text label:
            xpos gui.scale(4)
            yalign 0.5
            size gui.scale(11)
            bold True
            kerning gui.scale(1.5)
            color "#7f9099"
            outlines []

        text "[count]":
            xalign 1.0
            xoffset gui.scale(-14)
            yalign 0.5
            size gui.scale(11)
            color "#4f5f68"
            outlines []

        add Solid("#ffffff10"):
            xpos gui.scale(4)
            yalign 1.0
            xysize ((group_width - gui.scale(18)), 1)


screen phone_app_map_row(place):
    $ row_width = gui.scale(menu_phone_content_w) - gui.scale(9)
    $ row_visited = phone_map_is_visited(place["id"])
    $ row_photo = phone_map_photo(place["image"], gui.scale(54), gui.scale(32), dim=not row_visited)

    button:
        xysize (row_width, gui.scale(50))
        background None
        hover_background Solid("#ffffff0a")
        padding (0, 0)
        action [
            SetVariable("phone_apps_map_location", place["id"]),
            With(Dissolve(0.14)),
        ]

        fixed:
            xysize (row_width, gui.scale(50))

            add Solid("#82d7bf" if row_visited else "#3f4d55"):
                xpos 0
                ypos gui.scale(5)
                xysize (gui.scale(2), gui.scale(40))

            fixed:
                xpos gui.scale(9)
                ypos gui.scale(9)
                xysize (gui.scale(54), gui.scale(32))
                add Solid("#0d171d")
                add row_photo
                if not row_visited:
                    add Solid("#08111688") xysize (gui.scale(54), gui.scale(32))

            text place["name"]:
                xpos gui.scale(71)
                ypos gui.scale(6)
                xmaximum gui.scale(136)
                size gui.scale(15)
                color ("#e8eef2" if row_visited else "#9aa8b0")
                outlines []

            text place["area"].upper():
                xpos gui.scale(71)
                ypos gui.scale(28)
                xmaximum gui.scale(136)
                size gui.scale(10)
                kerning gui.scale(1)
                color ("#73848e" if row_visited else "#5a6871")
                outlines []

            text "›":
                xpos gui.scale(row_width - 16)
                yalign 0.5
                font "DejaVuSans.ttf"
                size gui.scale(18)
                color ("#c8a06a" if row_visited else "#4c5a63")
                outlines []


screen phone_app_map_detail(location_id):
    $ detail_place = phone_map_place(location_id) or phone_map_locations[0]
    $ detail_visited = phone_map_is_visited(detail_place["id"])
    $ detail_width = gui.scale(menu_phone_content_w)
    $ detail_photo_w = detail_width - gui.scale(8)
    $ detail_photo_h = gui.scale(128)
    $ detail_photo = phone_map_photo(detail_place["image"], detail_photo_w, detail_photo_h, dim=not detail_visited)

    fixed:
        xysize (detail_width, gui.scale(474))

        fixed:
            xpos gui.scale(4)
            ypos gui.scale(2)
            xysize (detail_photo_w, detail_photo_h)
            add Solid("#0d171d")
            add detail_photo
            if not detail_visited:
                add Solid("#08111670") xysize (detail_photo_w, detail_photo_h)

        text detail_place["name"]:
            xpos gui.scale(6)
            ypos gui.scale(136)
            size gui.scale(20)
            color "#f1eee7"
            outlines []

        text detail_place["area"].upper():
            xpos gui.scale(6)
            ypos gui.scale(165)
            size gui.scale(11)
            kerning gui.scale(1)
            color "#90a4ae"
            outlines []

        hbox:
            xalign 1.0
            xoffset gui.scale(-6)
            ypos gui.scale(164)
            spacing gui.scale(4)

            text "●":
                size gui.scale(8)
                yalign 0.5
                color ("#82d7bf" if detail_visited else "#5b6a73")
                outlines []

            text ("VISITED" if detail_visited else "NOT VISITED"):
                size gui.scale(11)
                bold True
                kerning gui.scale(1)
                color ("#82d7bf" if detail_visited else "#7d8a92")
                outlines []

        add Solid("#ffffff10"):
            xpos gui.scale(4)
            ypos gui.scale(184)
            xysize ((detail_width - gui.scale(8)), 1)

        text "ABOUT":
            xpos gui.scale(6)
            ypos gui.scale(192)
            size gui.scale(10)
            bold True
            kerning gui.scale(2)
            color "#5f707a"
            outlines []

        text detail_place["summary"]:
            xpos gui.scale(6)
            ypos gui.scale(207)
            xmaximum gui.scale(228)
            size gui.scale(15)
            line_spacing gui.scale(2)
            color "#c2ccd1"
            outlines []

        if detail_visited:
            text "FROM YOUR NOTES":
                xpos gui.scale(6)
                ypos gui.scale(296)
                size gui.scale(10)
                bold True
                kerning gui.scale(2)
                color "#5f707a"
                outlines []

            text detail_place["note"]:
                xpos gui.scale(6)
                ypos gui.scale(310)
                xmaximum gui.scale(228)
                size gui.scale(15)
                line_spacing gui.scale(2)
                color "#d8dfe2"
                outlines []
        else:
            text "NOT VISITED":
                xpos gui.scale(6)
                ypos gui.scale(296)
                size gui.scale(10)
                bold True
                kerning gui.scale(2)
                color "#5f707a"
                outlines []

            text "No photographs or notes from this area yet.":
                xpos gui.scale(6)
                ypos gui.scale(310)
                xmaximum gui.scale(228)
                size gui.scale(15)
                line_spacing gui.scale(2)
                color "#8d9aa2"
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
                for entry in _history_list:
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
                            text "[orb_rank]":
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
                            text "RANK [orb_rank] / 5":
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


screen phone_apps_about_contents():
    viewport:
        xfill True
        yfill True
        mousewheel True
        draggable True
        style_prefix "phone_apps"
        scrollbars "vertical"
        vbox:
            spacing gui.scale(14)
            text "[config.name!t]":
                style "phone_heading"
                size gui.scale(24)
            text "Version [config.version!t]":
                style "phone_detail"
                size gui.scale(14)
            if gui.about:
                text "[gui.about!t]":
                    style "phone_body"
                    size gui.scale(14)
            text "Made with Ren'Py [renpy.version_only].":
                style "phone_body"
                size gui.scale(14)
            text "[renpy.license!t]":
                style "phone_detail"
                size gui.scale(12)


screen phone_apps_help_contents(device):
    vbox:
        spacing gui.scale(10)
        hbox:
            spacing gui.scale(3)
            textbutton "KEYBOARD":
                style "phone_small_button"
                text_color ("#e7c08d" if device == "keyboard" else "#aab4bb")
                action SetVariable("phone_apps_help_device", "keyboard")
            textbutton "MOUSE":
                style "phone_small_button"
                text_color ("#e7c08d" if device == "mouse" else "#aab4bb")
                action SetVariable("phone_apps_help_device", "mouse")
            if GamepadExists():
                textbutton "PAD":
                    style "phone_small_button"
                    text_color ("#e7c08d" if device == "gamepad" else "#aab4bb")
                    action SetVariable("phone_apps_help_device", "gamepad")

        viewport:
            xfill True
            ysize gui.scale(420)
            mousewheel True
            draggable True
            style_prefix "phone_apps"
            scrollbars "vertical"
            vbox:
                spacing gui.scale(11)
                if device == "keyboard":
                    $ bindings = [
                        ("Enter", "Advance dialogue or activate a control."),
                        ("Space", "Advance dialogue."),
                        ("Arrow Keys", "Navigate the interface."),
                        ("Escape", "Open the phone."),
                        ("Ctrl / Tab", "Hold to skip / toggle skipping."),
                        ("Page Up / Down", "Roll back / roll forward."),
                        ("H", "Hide the interface."),
                        ("S", "Take a photo of the scene."),
                        ("V", "Toggle self-voicing."),
                        ("Shift+A", "Open accessibility settings."),
                    ]
                    if not camera_unlocked:
                        $ bindings = [binding for binding in bindings if binding[0] != "S"]
                elif device == "mouse":
                    $ bindings = [
                        ("Left Click", "Advance dialogue or activate a control."),
                        ("Middle Click", "Hide the interface."),
                        ("Right Click", "Right-click is disabled during gameplay."),
                        ("Mouse Wheel", "Scroll menus and roll back dialogue."),
                    ]
                else:
                    $ bindings = [
                        ("A / Right Trigger", "Advance dialogue or activate a control."),
                        ("Left Shoulder", "Roll back."),
                        ("Right Shoulder", "Roll forward."),
                        ("D-Pad / Sticks", "Navigate controls."),
                        ("Start / B", "Open or close the phone."),
                        ("Y", "Hide the interface."),
                    ]
                for caption, description in bindings:
                    vbox:
                        spacing gui.scale(2)
                        text caption:
                            style "phone_heading"
                            size gui.scale(15)
                        text description:
                            style "phone_body"
                            size gui.scale(13)
                            xmaximum gui.scale(215)
                if device == "gamepad":
                    textbutton "CALIBRATE CONTROLLER":
                        style "phone_option"
                        action GamepadCalibrate()


screen phone_apps_exit_confirm(kind):
    vbox:
        xalign 0.5
        yalign 0.4
        xsize gui.scale(216)
        spacing gui.scale(16)
        text ("Return to the title screen?" if kind == "title" else "Quit the game?"):
            style "phone_heading"
            size gui.scale(20)
            xalign 0.5
            textalign 0.5
        text (
            "Unsaved progress may be lost."
            if kind == "title"
            else "Are you sure you want to close the game?"
        ):
            style "phone_body"
            size gui.scale(14)
            xalign 0.5
            textalign 0.5
        textbutton "YES":
            style "phone_option"
            action (MainMenu(confirm=False) if kind == "title" else Quit(confirm=False))
        textbutton "CANCEL":
            style "phone_option"
            action [
                SetVariable("phone_apps_page", phone_apps_more_return_page),
                SetVariable("phone_apps_more_open", True),
                With(Dissolve(0.16)),
            ]


screen phone_app_shell(title, subtitle=None, back_action=None, close_action=None, close_sensitive=True):
    # Shared chrome for every in-phone app. The story chat popup uses this too,
    # so a message arriving during a scene cannot drift away from the Messages
    # app's header, content bounds, and footer placement.
    fixed:
        xpos gui.scale(14)
        ypos gui.scale(34)
        xysize (gui.scale(menu_phone_content_w), gui.scale(548))

        fixed:
            xfill True
            ysize gui.scale(38)
            if back_action is not None:
                textbutton "<":
                    style "phone_small_button"
                    xsize gui.scale(34)
                    yalign 0.5
                    action back_action

            vbox:
                xalign 0.5
                yalign 0.5
                spacing gui.scale(1)
                text title:
                    xalign 0.5
                    xmaximum gui.scale(172)
                    textalign 0.5
                    size gui.scale(15)
                    color "#f0eee8"
                    outlines []
                if subtitle:
                    text subtitle:
                        xalign 0.5
                        size gui.scale(10)
                        color "#9aa8b0"
                        outlines []

            if close_action is not None:
                textbutton "×":
                    style "phone_small_button"
                    xalign 1.0
                    yalign 0.5
                    sensitive close_sensitive
                    action close_action

        add Solid("#ffffff16") ypos gui.scale(42) xysize (gui.scale(menu_phone_content_w), gui.scale(1))

        fixed:
            xpos 0
            ypos gui.scale(50)
            xysize (gui.scale(menu_phone_content_w), gui.scale(474))
            transclude


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

        $ app_titles = {
            None: "Phone",
            "messages": "Messages",
            "messages_thread": "Messages",
            "calendar": "Calendar",
            "wire": "WIRE",
            "settings": "Settings",
            "camera": "Camera",
            "inventory": "Inventory",
            "maps": "Maps",
            "stats": "Stats",
            "journal": "Journal",
            "backup": ("Cloud / " + phone_apps_backup_mode.title() if phone_apps_backup_mode else "Cloud"),
            "about": "About",
            "help": "Help",
            "confirm_title": "Return to Title",
            "confirm_quit": "Quit Game",
        }
        $ app_title = app_titles[phone_apps_page]
        $ app_subtitle = (
            msg_contact_name(phone_apps_messages_contact)
            if phone_apps_page == "messages_thread" else
            (phone_map_place(phone_apps_map_location) or {}).get("name")
            if phone_apps_page == "maps" and phone_apps_map_location else
            None
        )
        $ app_back_action = None if phone_apps_page is None else (
            [SetVariable("phone_apps_wire_profile", None), With(Dissolve(0.16))]
            if phone_apps_page == "wire" and phone_apps_wire_profile else
            [SetVariable("phone_apps_inventory_open", False), With(Dissolve(0.16))]
            if phone_apps_page == "inventory" and phone_apps_inventory_open else
            [SetVariable("phone_apps_inventory_item", None), With(Dissolve(0.16))]
            if phone_apps_page == "inventory" and phone_apps_inventory_item else
            [SetVariable("phone_apps_backup_mode", None), With(Dissolve(0.16))]
            if phone_apps_page == "backup" and phone_apps_backup_mode else
            [SetVariable("phone_apps_map_location", None), With(Dissolve(0.16))]
            if phone_apps_page == "maps" and phone_apps_map_location else
            [
                SetVariable("phone_apps_page", "messages"),
                SetVariable("phone_apps_messages_contact", None),
                With(Dissolve(0.16)),
            ]
            if phone_apps_page == "messages_thread" and phone_apps_messages_contact else
            [
                SetVariable("phone_apps_page", phone_apps_more_return_page),
                SetVariable("phone_apps_more_open", True),
                With(Dissolve(0.16)),
            ]
            if phone_apps_page in ("about", "help", "confirm_title", "confirm_quit") else
            [SetVariable("phone_apps_page", None), With(Dissolve(0.16))]
        )

        use phone_app_shell(
            title=app_title,
            subtitle=app_subtitle,
            back_action=app_back_action,
            close_action=Function(phone_apps_begin_close),
            close_sensitive=not phone_apps_closing,
        ):
            fixed:
                xpos 0
                ypos 0
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

                        grid 3 4:
                            xalign 0.5
                            spacing gui.scale(5)

                            for app_id, app_name, disabled in phone_apps_catalog:
                                use phone_app_tile(
                                    app_id,
                                    app_name,
                                    disabled or (app_id in ("messages", "maps", "wire", "calendar") and not phone_app_unlocked(app_id)),
                                    [SetVariable("phone_apps_page", app_id), With(Dissolve(0.16))],
                                )

                        text "A few apps are still finding their place.":
                            xalign 0.5
                            size gui.scale(11)
                            color "#64727e"
                            outlines []
                elif phone_apps_page == "about":
                    use phone_apps_about_contents
                elif phone_apps_page == "help":
                    use phone_apps_help_contents(phone_apps_help_device)
                elif phone_apps_page == "confirm_title":
                    use phone_apps_exit_confirm("title")
                elif phone_apps_page == "confirm_quit":
                    use phone_apps_exit_confirm("quit")
                elif phone_apps_page == "messages":
                    use phone_app_messages_contents
                elif phone_apps_page == "messages_thread":
                    use phone_app_messages_thread_contents(phone_apps_messages_contact)
                elif phone_apps_page == "camera":
                    use phone_app_camera_contents
                elif phone_apps_page == "wire":
                    use phone_app_wire_contents(phone_apps_wire_profile)
                elif phone_apps_page == "inventory":
                    use phone_app_inventory_contents(phone_apps_inventory_item)
                elif phone_apps_page == "maps":
                    use phone_app_maps_contents
                elif phone_apps_page == "stats":
                    use phone_app_stats_contents
                elif phone_apps_page == "journal":
                    use phone_app_journal_contents
                elif phone_apps_page == "calendar":
                    if phone_app_unlocked("calendar"):
                        use phone_app_calendar_contents
                    else:
                        use phone_app_calendar_contents_locked
                elif phone_apps_page == "backup":
                    use phone_app_backup_contents(
                        phone_apps_backup_mode,
                        backup_page_value,
                    )
                elif phone_apps_page == "settings":
                    use phone_app_settings_contents(phone_apps_settings_tab)

        fixed:
            xpos gui.scale(14)
            ypos gui.scale(34)
            xysize (gui.scale(menu_phone_content_w), gui.scale(548))

            # A quiet footer edge separates the app body from CLOSE and the
            # menu handle. It sits exactly where every app's 474px body ends.
            add Solid("#ffffff10"):
                ypos gui.scale(524)
                xysize (gui.scale(menu_phone_content_w), 1)

            textbutton "CLOSE":
                style "phone_small_button"
                xalign 0.5
                yalign 1.0
                yoffset gui.scale(2)
                text_size gui.scale(11)
                text_kerning gui.scale(1)
                padding (gui.scale(8), gui.scale(2))
                sensitive not phone_apps_closing
                action Function(phone_apps_begin_close)

            textbutton "⋮":
                style "phone_small_button"
                xalign 1.0
                yalign 1.0
                xoffset gui.scale(-8)
                yoffset gui.scale(1)
                text_font "DejaVuSans.ttf"
                text_size gui.scale(17)
                padding (gui.scale(6), gui.scale(1))
                sensitive not phone_apps_closing
                action ToggleVariable("phone_apps_more_open")

            if phone_apps_more_open:
                frame:
                    xpos gui.scale(38)
                    ypos gui.scale(333)
                    xsize gui.scale(190)
                    background Solid("#17242df2")
                    padding (gui.scale(8), gui.scale(8))
                    vbox:
                        spacing gui.scale(3)
                        textbutton "ABOUT":
                            style "phone_apps_menu_option"
                            action [
                                SetVariable("phone_apps_more_return_page", phone_apps_page),
                                SetVariable("phone_apps_page", "about"),
                                SetVariable("phone_apps_more_open", False),
                                With(Dissolve(0.16)),
                            ]
                        textbutton "HELP":
                            style "phone_apps_menu_option"
                            action [
                                SetVariable("phone_apps_more_return_page", phone_apps_page),
                                SetVariable("phone_apps_help_device", "keyboard"),
                                SetVariable("phone_apps_page", "help"),
                                SetVariable("phone_apps_more_open", False),
                                With(Dissolve(0.16)),
                            ]
                        if not main_menu:
                            textbutton "RETURN TO TITLE":
                                style "phone_apps_menu_option"
                                action [
                                    SetVariable("phone_apps_more_return_page", phone_apps_page),
                                    SetVariable("phone_apps_page", "confirm_title"),
                                    SetVariable("phone_apps_more_open", False),
                                    With(Dissolve(0.16)),
                                ]
                        if renpy.variant("pc"):
                            textbutton "QUIT GAME":
                                style "phone_apps_menu_option"
                                action [
                                    SetVariable("phone_apps_more_return_page", phone_apps_page),
                                    SetVariable("phone_apps_page", "confirm_quit"),
                                    SetVariable("phone_apps_more_open", False),
                                    With(Dissolve(0.16)),
                                ]

    if phone_apps_closing:
        timer 0.70 action Return()

    key "game_menu" action Function(phone_apps_begin_close)


style phone_apps_vscrollbar is phone_vscrollbar:
    xsize gui.scale(8)

style phone_apps_menu_option is phone_option:
    yminimum gui.scale(34)
    padding (gui.scale(7), gui.scale(4))

style phone_apps_menu_option_text is phone_option_text:
    size gui.scale(12)
