################################################################################
## MESSAGES — TEXTING, THREADS, AND THE PHONE BUZZ
################################################################################

default message_threads = {}
default message_unread = {}
default pending_messages = []
default messages_hint_shown = False

default phone_chat_started_at = 0.0
default phone_chat_closing = False
default phone_chat_closed_at = 0.0
default phone_chat_close_offset = 0
default phone_chat_close_alpha = 1.0

init python:
    import time

    def msg_contact_name(cid):
        return wire_contacts.get(cid, {}).get("name", cid.replace("_", " ").title())

    def msg_thread(cid):
        if cid not in store.message_threads:
            store.message_threads[cid] = []
        return store.message_threads[cid]

    def msg_unread(cid):
        return store.message_unread.get(cid, 0)

    def msg_last_text(cid):
        thread = store.message_threads.get(cid) or []
        return thread[-1]["text"] if thread else ""

    def msg_total():
        return sum(len(t) for t in store.message_threads.values())

    def msg_buzz():
        if renpy.loadable("audio/SFX/message_buzz.wav"):
            play_sfx("audio/SFX/message_buzz.wav")

    def receive_message(cid, text, img=None):
        msg = {"me": False, "text": text}
        if img:
            msg["img"] = img
        msg_thread(cid).append(msg)
        store.message_unread[cid] = msg_unread(cid) + 1
        msg_buzz()

    def send_message(cid, text, img=None):
        msg = {"me": True, "text": text}
        if img:
            msg["img"] = img
        msg_thread(cid).append(msg)
        store.message_unread[cid] = 0

    def queue_message(cid, text):
        store.pending_messages.append({"contact": cid, "text": text})

    def flush_pending_messages():
        if not store.cellular_data_active or not store.pending_messages:
            return
        for queued in list(store.pending_messages):
            receive_message(queued["contact"], queued["text"])
            renpy.pause(0.8, hard=True)
        store.pending_messages = []

    def run_chat(cid, beats):
        store.message_unread[cid] = 0
        store.phone_chat_started_at = time.monotonic()
        store.phone_chat_closing = False
        store.phone_chat_closed_at = 0.0
        
        try:
            for beat in beats:
                if "them" in beat:
                    receive_message(cid, beat["them"], img=beat.get("img"))
                elif "say" in beat:
                    send_message(cid, beat["say"], img=beat.get("img"))

                options = beat.get("options")
                # Blocking call to show screen and wait for interaction
                pick = renpy.call_screen("phone_chat_popup", cid=cid, options=options)

                if options is not None and pick is not None:
                    chosen = options[pick]
                    send_message(cid, chosen["send"], img=chosen.get("img"))

                    replies = chosen.get("them", [])
                    if not replies:
                        renpy.call_screen("phone_chat_popup", cid=cid, options=None)

                    for reply in replies:
                        if isinstance(reply, dict):
                            receive_message(cid, reply.get("text", ""), img=reply.get("img"))
                        else:
                            receive_message(cid, reply)
                        renpy.call_screen("phone_chat_popup", cid=cid, options=None)
        finally:
            # Prepare and trigger the lowering animation
            store.message_unread[cid] = 0
            store.phone_chat_closing = True
            store.phone_chat_closed_at = time.monotonic()
            
            # Snap current animation progress for a seamless handoff to lowering
            elapsed = time.monotonic() - store.phone_chat_started_at
            progress = min(1.0, max(0.0, elapsed / 0.95))
            store.phone_chat_close_offset = gui.scale(int(760 * (1.0 - progress) ** 5))
            store.phone_chat_close_alpha = min(1.0, max(0.0, (elapsed - 0.55) / 0.3))

            # Non-blocking show for the animation duration
            renpy.show_screen("phone_chat_popup", cid=cid, options=None)
            renpy.pause(0.7, hard=True)
            renpy.hide_screen("phone_chat_popup")
            renpy.restart_interaction()

screen phone_msg_bubble(msg, cid, accent):
    if msg["me"]:
        frame:
            xalign 1.0
            xmaximum gui.scale(180)
            background Solid(accent)
            padding (gui.scale(9), gui.scale(6))
            vbox:
                spacing gui.scale(4)
                if msg.get("img") and renpy.loadable(msg["img"]):
                    add msg["img"] xysize (gui.scale(132), gui.scale(88))
                if msg["text"] and msg["text"] != "(photo)":
                    text msg["text"]:
                        size gui.scale(13)
                        color "#0d1115"
                        outlines []
                        xmaximum gui.scale(162)
                        textalign 1.0
    else:
        hbox:
            spacing gui.scale(6)
            if cid in wire_contacts:
                use wire_avatar(cid, gui.scale(24))
            else:
                add Solid(accent + "55", xysize=(gui.scale(24), gui.scale(24)))
            frame:
                xmaximum gui.scale(180)
                background Solid("#1d2b33")
                padding (gui.scale(9), gui.scale(6))
                vbox:
                    spacing gui.scale(4)
                    if msg.get("img") and renpy.loadable(msg["img"]):
                        add msg["img"] xysize (gui.scale(132), gui.scale(88))
                    if msg["text"] and msg["text"] != "(photo)":
                        text msg["text"]:
                            size gui.scale(13)
                            color "#e6ebef"
                            outlines []
                            xmaximum gui.scale(162)

screen phone_chat_popup(cid, options=None, is_closing=None):
    modal not getattr(store, "phone_chat_closing", False)
    zorder 150

    $ closing = is_closing if is_closing is not None else getattr(store, "phone_chat_closing", False)

    key "game_menu" action NullAction()
    key "rollback" action NullAction()
    key "dismiss" action NullAction()

    add Solid("#030609d8")

    if options is None:
        key "K_RETURN" action Return(None)
        key "K_KP_ENTER" action Return(None)
        key "K_SPACE" action Return(None)

    # Aperture is 558px high. Header is 38px. Padding/Gap is 4px.
    # Content area for thread + options is 516px.
    $ opt_h = 188 if options is not None else 0
    $ thread_h = 516 - opt_h

    use phone_hardware(
        animate=True,
        raised_at=getattr(store, "phone_chat_started_at", 0.0),
        closing=closing,
        closing_at=getattr(store, "phone_chat_closed_at", 0.0),
        close_offset=getattr(store, "phone_chat_close_offset", 0),
        close_alpha=getattr(store, "phone_chat_close_alpha", 1.0)
    ):
        add "images/ui/apps/phone_screen.png":
            xysize (gui.scale(menu_phone_w), gui.scale(menu_phone_h))
        use phone_status

        fixed:
            xpos gui.scale(14)
            ypos gui.scale(36)
            xysize (gui.scale(menu_phone_content_w), gui.scale(558))

            fixed:
                xfill True
                ysize gui.scale(38)
                vbox:
                    xalign 0.5
                    yalign 0.5
                    spacing gui.scale(1)
                    text "Messages":
                        xalign 0.5
                        size gui.scale(15)
                        color "#f0eee8"
                        outlines []
                    text msg_contact_name(cid):
                        xalign 0.5
                        size gui.scale(10)
                        color "#9aa8b0"
                        outlines []

                textbutton "×":
                    style "phone_small_button"
                    xalign 1.0
                    yalign 0.5
                    action Return(None)

            add Solid("#ffffff16") ypos gui.scale(39) xysize (gui.scale(menu_phone_content_w), gui.scale(1))

            fixed:
                xpos 0
                ypos gui.scale(42)
                xysize (gui.scale(menu_phone_content_w), gui.scale(516))

                fixed:
                    xsize gui.scale(menu_phone_content_w)
                    ysize gui.scale(thread_h)
                    use phone_app_messages_thread_contents(cid)

                if options is not None:
                    frame:
                        ypos gui.scale(thread_h)
                        xysize (gui.scale(menu_phone_content_w), gui.scale(opt_h))
                        background Solid("#0b141bf7")
                        padding (gui.scale(8), gui.scale(8))
                        vbox:
                            xfill True
                            yfill True
                            spacing gui.scale(6)
                            for i, opt in enumerate(options):
                                use phone_chat_option(opt["label"], i, cid)
                
                elif not store.phone_chat_closing:
                    button:
                        ypos gui.scale(456)
                        xfill True
                        ysize gui.scale(60)
                        background Solid("#14232b")
                        hover_background Solid("#21343d")
                        action Return(None)

                        text "TAP TO CONTINUE  ›":
                            xalign 0.5
                            yalign 0.5
                            size gui.scale(12)
                            bold True
                            kerning gui.scale(1)
                            color "#d8b580"
                            hover_color "#fff2dc"
                            outlines []

screen phone_chat_option(label, index, cid):
    $ contact = wire_contacts.get(cid, {"color": "#8fd8c8"})
    $ accent = contact.get("color", "#8fd8c8")

    button:
        xfill True
        yminimum gui.scale(40)
        background Solid("#ffffff08")
        hover_background Solid("#c8a06a22")
        padding (gui.scale(9), gui.scale(6))
        action Return(index)

        hbox:
            xfill True
            spacing gui.scale(8)
            fixed:
                xsize gui.scale(3)
                yfill True
                add Solid(accent)
            text label:
                xmaximum gui.scale(190)
                yalign 0.5
                size gui.scale(12)
                color "#edf0f1"
                outlines []
            text "›":
                yalign 0.5
                size gui.scale(15)
                color accent
                outlines []

screen phone_app_messages_contents():
    $ thread_ids = [cid for cid in wire_order if store.message_threads.get(cid)]
    $ thread_ids += [cid for cid in store.message_threads
                     if cid not in wire_order and store.message_threads[cid]]

    if thread_ids:
        viewport:
            xfill True
            yfill True
            mousewheel True
            draggable True
            pagekeys True
            yinitial 1.0
            style_prefix "phone_apps"
            scrollbars None
            vbox:
                spacing gui.scale(4)

                for cid in thread_ids:
                    $ contact = wire_contacts.get(cid, {"name": msg_contact_name(cid), "color": "#8fd8c8"})
                    $ unread = msg_unread(cid)
                    button:
                        xfill True
                        ysize gui.scale(52)
                        background None
                        hover_background Solid("#ffffff0d")
                        action [
                            SetVariable("phone_apps_page", "messages_thread"),
                            SetVariable("phone_apps_messages_contact", cid),
                            With(Dissolve(0.16)),
                        ]
                        hbox:
                            yalign 0.5
                            spacing gui.scale(9)
                            xfill True
                            if cid in wire_contacts:
                                use wire_avatar(cid, gui.scale(40))
                            else:
                                add Solid(contact["color"], xysize=(gui.scale(40), gui.scale(40)))
                            vbox:
                                xsize gui.scale(145)
                                spacing gui.scale(1)
                                text contact["name"]:
                                    size gui.scale(15)
                                    color "#e8eef2"
                                    outlines []
                                text msg_last_text(cid):
                                    size gui.scale(12)
                                    color "#8b97a3"
                                    outlines []
                                    xmaximum gui.scale(145)
                                    ymaximum gui.scale(15)
                            if unread:
                                fixed:
                                    xsize gui.scale(20)
                                    ysize gui.scale(20)
                                    add Solid("#c94f4f", xysize=(gui.scale(16), gui.scale(16)))
                                    text "[unread]":
                                        size gui.scale(9)
                                        color "#ffffff"
                                        outlines []
                                        xalign 0.5
                                        yalign 0.5
                            text ">":
                                style "phone_detail"
                                yalign 0.5
                                xalign 1.0
                                xfill True
    else:
        vbox:
            xalign 0.5
            yalign 0.5
            spacing gui.scale(10)
            text "No messages yet.":
                size gui.scale(15)
                color "#c3ccd5"
                outlines []
            text "People you meet can text once you have a data plan.":
                size gui.scale(12)
                color "#75838d"
                textalign 0.5
                xmaximum gui.scale(menu_phone_content_w)
                outlines []

screen phone_app_messages_thread_contents(cid):
    $ contact = wire_contacts.get(cid, {"name": msg_contact_name(cid), "color": "#8fd8c8"})
    $ accent = contact.get("color", "#8fd8c8")
    $ thread = msg_thread(cid)

    viewport:
        xfill True
        yfill True
        mousewheel True
        draggable True
        pagekeys True
        yinitial 1.0
        style_prefix "phone_apps"
        scrollbars None
        vbox:
            spacing gui.scale(7)
            for msg in thread:
                use phone_msg_bubble(msg, cid, accent)
