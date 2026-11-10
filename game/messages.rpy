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
        if not thread:
            return ""
        last = thread[-1]
        if last.get("text") == "(photo)":
            return "Photo"
        return last["text"]

    def msg_total():
        return sum(len(t) for t in store.message_threads.values())

    def msg_buzz():
        if renpy.loadable("audio/SFX/message_buzz.wav"):
            play_sfx("audio/SFX/message_buzz.wav")

    def phone_reply_label(label):
        # Reply suggestions read as message text, not as quoted dialogue.
        label = label.strip()
        if len(label) >= 2 and label[0] == '"' and label[-1] == '"':
            label = label[1:-1]
        return label

    def phone_chat_typing_time(text):
        # Long lines take a little longer to type, but never stall the scene.
        return min(1.85, 0.75 + len(text or "") * 0.016)

    def receive_message(cid, text, img=None, day=None):
        msg = {"me": False, "text": text, "anim_at": time.monotonic()}
        if img:
            msg["img"] = img
        if day:
            msg["day"] = day
        msg_thread(cid).append(msg)
        store.message_unread[cid] = msg_unread(cid) + 1
        msg_buzz()

    def send_message(cid, text, img=None):
        msg = {"me": True, "text": text, "anim_at": time.monotonic()}
        if img:
            msg["img"] = img
        msg_thread(cid).append(msg)
        store.message_unread[cid] = 0

    def queue_message(cid, text, img=None, day=None):
        store.pending_messages.append({
            "contact": cid,
            "text": text,
            "img": img,
            "day": day,
        })

    def deliver_pending_messages():
        """Move queued texts into their threads for a scene to present itself.

        `flush_pending_messages` is for delivery between scenes. This is for the
        first connection, where the phone is already in his hand and the scene
        wants to show the popup rather than let the texts land silently.
        """
        queued = list(store.pending_messages)
        store.pending_messages = []
        for item in queued:
            receive_message(
                item["contact"],
                item["text"],
                img=item.get("img"),
                day=item.get("day"),
            )
        return queued

    def flush_pending_messages():
        if not store.cellular_data_active or not store.pending_messages:
            return
        for queued in list(store.pending_messages):
            receive_message(
                queued["contact"],
                queued["text"],
                img=queued.get("img"),
                day=queued.get("day"),
            )
            renpy.pause(0.8, hard=True)
        store.pending_messages = []

    def run_chat(cid, beats):
        store.message_unread[cid] = 0
        store.phone_chat_started_at = time.monotonic()
        store.phone_chat_closing = False
        store.phone_chat_closed_at = 0.0

        def show(options=None, typing=False, auto=None, show_continue=False, options_delay=0.0):
            return renpy.call_screen(
                "phone_chat_popup",
                cid=cid,
                options=options,
                typing=typing,
                auto=auto,
                show_continue=show_continue,
                options_delay=options_delay,
            )

        def arrive(text, img=None):
            # The typing indicator is part of the conversation, not a transition
            # laid over it, so the app history shows exactly what the player saw.
            show(typing=True, auto=phone_chat_typing_time(text))
            receive_message(cid, text, img=img)

        try:
            for beat in beats:
                options = beat.get("options")
                pick = None

                if "them" in beat:
                    arrive(beat["them"], img=beat.get("img"))
                    if options:
                        pick = show(options=options, options_delay=0.45)
                    else:
                        show(auto=0.95)
                elif "say" in beat:
                    send_message(cid, beat["say"], img=beat.get("img"))
                    if options:
                        pick = show(options=options, options_delay=0.30)
                    else:
                        show(auto=0.65)
                elif options:
                    # An opening beat with no message lets the scene start on an
                    # empty thread, with the first line offered as a reply.
                    pick = show(options=options, options_delay=beat.get("options_delay", 0.0))

                if options and pick is not None:
                    chosen = options[pick]
                    send_message(cid, chosen["send"], img=chosen.get("img"))
                    show(auto=0.60)

                    for reply in chosen.get("them", []):
                        if isinstance(reply, dict):
                            reply_text = reply.get("text", "")
                            reply_img = reply.get("img")
                        else:
                            reply_text = reply
                            reply_img = None
                        arrive(reply_text, img=reply_img)
                        show(auto=0.95)

            # Everything has arrived. The composer becomes the way out.
            show(show_continue=True)
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

            # Non-blocking show for the animation duration. Keep the finished
            # footer in place so the phone lowers without changing its face.
            renpy.show_screen(
                "phone_chat_popup",
                cid=cid,
                options=None,
                typing=False,
                auto=None,
                show_continue=True,
                options_delay=0.0,
            )
            renpy.pause(0.7, hard=True)
            renpy.hide_screen("phone_chat_popup")
            renpy.restart_interaction()

init python:
    def phone_message_motion(trans, st, at, started_at, mine):
        elapsed = time.monotonic() - started_at
        progress = min(1.0, max(0.0, elapsed / 0.24))
        eased = 1.0 - (1.0 - progress) ** 3
        trans.alpha = eased
        trans.yoffset = int((1.0 - eased) * 9)
        trans.xoffset = int((1.0 - eased) * (5 if mine else -5))
        return 0.016 if progress < 1.0 else None


transform phone_message_enter(started_at=0.0, mine=False):
    subpixel True
    function renpy.curry(phone_message_motion)(started_at=started_at, mine=mine)


transform phone_typing_enter:
    alpha 0.0
    yoffset gui.scale(6)
    easeout 0.18 alpha 1.0 yoffset 0


transform phone_typing_dot(delay=0.0):
    yoffset 0
    pause delay
    block:
        easeout 0.15 yoffset gui.scale(-3)
        easein 0.15 yoffset 0
        pause 0.42
        repeat


transform phone_sheet_reveal:
    alpha 0.0
    yoffset gui.scale(22)
    easeout 0.24 alpha 1.0 yoffset 0


transform phone_options_reveal(delay=0.0):
    alpha 0.0
    yoffset gui.scale(5)
    pause delay
    easeout 0.18 alpha 1.0 yoffset 0


transform phone_continue_reveal:
    alpha 0.0
    yoffset gui.scale(5)
    easeout 0.20 alpha 1.0 yoffset 0


transform phone_continue_chevron:
    alpha 0.55
    pause 0.85
    linear 0.35 alpha 1.0
    pause 0.85
    linear 0.35 alpha 0.55
    repeat


screen phone_msg_bubble(msg, cid, accent, show_avatar=True):
    $ bubble_bg = Transform(
        Frame("images/ui/apps/msg_round.png", gui.scale(12), gui.scale(12)),
        matrixcolor=TintMatrix(accent if msg["me"] else "#1d2b33"),
    )
    $ entry_time = msg.get("anim_at", 0.0)

    if msg["me"]:
        frame:
            xalign 1.0
            xmaximum gui.scale(188)
            background bubble_bg
            padding (gui.scale(10), gui.scale(7))
            at phone_message_enter(entry_time, True)
            vbox:
                spacing gui.scale(4)
                if msg.get("img") and renpy.loadable(msg["img"]):
                    add msg["img"] xysize (gui.scale(132), gui.scale(88))
                if msg["text"] and msg["text"] != "(photo)":
                    text msg["text"]:
                        size gui.scale(15)
                        color "#0d1115"
                        outlines []
                        xmaximum gui.scale(164)
                        textalign 1.0
    else:
        hbox:
            spacing gui.scale(6)
            at phone_message_enter(entry_time, False)
            if show_avatar and cid in wire_contacts:
                use wire_avatar(cid, gui.scale(28))
            elif show_avatar:
                add Solid(accent + "55", xysize=(gui.scale(28), gui.scale(28)))
            else:
                null width gui.scale(28)
            frame:
                xmaximum gui.scale(182)
                background bubble_bg
                padding (gui.scale(10), gui.scale(7))
                vbox:
                    spacing gui.scale(4)
                    if msg.get("img") and renpy.loadable(msg["img"]):
                        add msg["img"] xysize (gui.scale(132), gui.scale(88))
                    if msg["text"] and msg["text"] != "(photo)":
                        text msg["text"]:
                            size gui.scale(15)
                            color "#e6ebef"
                            outlines []
                            xmaximum gui.scale(160)


screen phone_typing_bubble(cid, show_avatar=True):
    $ contact = wire_contacts.get(cid, {"color": "#8fd8c8"})
    $ accent = contact.get("color", "#8fd8c8")
    $ typing_bg = Transform(
        Frame("images/ui/apps/msg_round.png", gui.scale(12), gui.scale(12)),
        matrixcolor=TintMatrix("#1d2b33"),
    )

    hbox:
        spacing gui.scale(6)
        at phone_typing_enter
        if show_avatar and cid in wire_contacts:
            use wire_avatar(cid, gui.scale(28))
        elif show_avatar:
            add Solid(accent + "55", xysize=(gui.scale(28), gui.scale(28)))
        else:
            null width gui.scale(28)
        frame:
            background typing_bg
            padding (gui.scale(11), gui.scale(8))
            fixed:
                xysize (gui.scale(26), gui.scale(10))
                for dot in range(3):
                    add Solid("#aebbc4"):
                        xysize (gui.scale(4), gui.scale(4))
                        xpos gui.scale(dot * 9)
                        ypos gui.scale(3)
                        at phone_typing_dot(dot * 0.12)


screen phone_chat_popup(cid, options=None, typing=False, auto=None, show_continue=False, options_delay=0.0):
    modal not getattr(store, "phone_chat_closing", False)
    zorder 150
    default options_ready = options_delay <= 0.0

    $ closing = getattr(store, "phone_chat_closing", False)
    $ content_h = gui.scale(474)
    $ footer_h = gui.scale(66)
    $ opt_h = min(content_h - gui.scale(120), gui.scale(18 + len(options) * 52)) if options else 0
    $ sheet_h = opt_h if options else footer_h
    $ thread_top = content_h - sheet_h
    $ sheet_bg = Transform(
        Frame("images/ui/apps/msg_sheet.png", left=gui.scale(16), top=gui.scale(16),
              right=gui.scale(16), bottom=0),
        matrixcolor=TintMatrix("#0b141b"),
    )
    $ composer_bg = Transform(
        Frame("images/ui/apps/msg_round.png", gui.scale(12), gui.scale(12)),
        matrixcolor=TintMatrix("#ffffff"),
        alpha=0.05,
    )
    $ send_bg = Transform(
        Frame("images/ui/apps/msg_round.png", gui.scale(12), gui.scale(12)),
        matrixcolor=TintMatrix("#243640"),
    )
    $ continue_bg = Transform(
        Frame("images/ui/apps/msg_round.png", gui.scale(12), gui.scale(12)),
        matrixcolor=TintMatrix("#17262e"),
    )
    $ continue_hover = Transform(
        Frame("images/ui/apps/msg_round.png", gui.scale(12), gui.scale(12)),
        matrixcolor=TintMatrix("#20343e"),
    )

    key "game_menu" action NullAction()
    key "rollback" action NullAction()
    key "dismiss" action NullAction()

    if auto is not None:
        timer auto action Return(None)
    if options and options_delay > 0:
        timer options_delay action SetScreenVariable("options_ready", True)

    if options is None and not closing:
        key "K_RETURN" action Return(None)
        key "K_KP_ENTER" action Return(None)
        key "K_SPACE" action Return(None)

    add Solid("#030609d8")

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

        use phone_app_shell(
            title="Messages",
            subtitle=msg_contact_name(cid),
            close_action=(Return(None) if show_continue and not closing else None),
            close_sensitive=not closing,
        ):
            fixed:
                xysize (gui.scale(menu_phone_content_w), content_h)

                # The thread uses the full body. The footer floats above its
                # bottom edge, so the phone never resizes between steps; the
                # thread's bottom padding keeps the newest bubble clear of it.
                fixed:
                    xsize gui.scale(menu_phone_content_w)
                    ysize content_h
                    use phone_app_messages_thread_contents(
                        cid,
                        typing=typing,
                        bottom_pad=(sheet_h + gui.scale(10)),
                    )

                if options:
                    frame:
                        ypos thread_top
                        xysize (gui.scale(menu_phone_content_w), opt_h)
                        background sheet_bg
                        padding (gui.scale(10), gui.scale(9))
                        at phone_sheet_reveal
                        add Solid("#ffffff10"):
                            xpos gui.scale(6)
                            xysize ((gui.scale(menu_phone_content_w) - gui.scale(12)), 1)
                        if options_ready:
                            vbox:
                                xfill True
                                yalign 0.5
                                spacing gui.scale(5)
                                for i, opt in enumerate(options):
                                    use phone_chat_option(opt["label"], i, cid)

                elif show_continue:
                    frame:
                        ypos thread_top
                        xysize (gui.scale(menu_phone_content_w), footer_h)
                        background sheet_bg
                        padding (0, 0)
                        button:
                            xalign 0.5
                            ypos gui.scale(11)
                            xsize (gui.scale(menu_phone_content_w) - gui.scale(26))
                            ysize gui.scale(44)
                            background continue_bg
                            hover_background continue_hover
                            sensitive not closing
                            action Return(None)
                            at phone_continue_reveal
                            hbox:
                                xalign 0.5
                                yalign 0.5
                                spacing gui.scale(7)
                                text "TAP TO CONTINUE":
                                    size gui.scale(13)
                                    bold True
                                    kerning gui.scale(1.5)
                                    color "#d8b580"
                                    outlines []
                                text "›":
                                    font "DejaVuSans.ttf"
                                    size gui.scale(17)
                                    color "#d8b580"
                                    outlines []
                                    at phone_continue_chevron

                else:
                    frame:
                        ypos thread_top
                        xysize (gui.scale(menu_phone_content_w), footer_h)
                        background sheet_bg
                        padding (0, 0)
                        fixed:
                            xalign 0.5
                            ypos gui.scale(12)
                            xysize ((gui.scale(menu_phone_content_w) - gui.scale(28)), gui.scale(36))
                            add composer_bg:
                                xysize ((gui.scale(menu_phone_content_w) - gui.scale(28)), gui.scale(36))
                            text "Message":
                                xpos gui.scale(12)
                                yalign 0.5
                                size gui.scale(13)
                                color "#5f6f79"
                                outlines []
                            fixed:
                                xalign 1.0
                                xoffset gui.scale(-6)
                                yalign 0.5
                                xysize (gui.scale(24), gui.scale(24))
                                add send_bg:
                                    xysize (gui.scale(24), gui.scale(24))
                                text "↑":
                                    font "DejaVuSans.ttf"
                                    xalign 0.5
                                    yalign 0.5
                                    size gui.scale(14)
                                    color "#7e8f99"
                                    outlines []


screen phone_chat_option(label, index, cid):
    $ contact = wire_contacts.get(cid, {"color": "#8fd8c8"})
    $ accent = contact.get("color", "#8fd8c8")
    $ option_bg = Transform(
        Frame("images/ui/apps/msg_round.png", gui.scale(11), gui.scale(11)),
        matrixcolor=TintMatrix("#ffffff"),
        alpha=0.045,
    )
    $ option_hover = Transform(
        Frame("images/ui/apps/msg_round.png", gui.scale(11), gui.scale(11)),
        matrixcolor=TintMatrix(accent),
        alpha=0.20,
    )

    button:
        xfill True
        yminimum gui.scale(46)
        background option_bg
        hover_background option_hover
        padding (gui.scale(10), gui.scale(6))
        action Return(index)
        at phone_options_reveal(index * 0.035)

        hbox:
            xfill True
            yalign 0.5
            spacing gui.scale(8)
            add Solid(accent) xysize (gui.scale(3), gui.scale(26))
            text phone_reply_label(label):
                xmaximum gui.scale(182)
                yalign 0.5
                size gui.scale(14)
                color "#edf0f1"
                outlines []
            text "›":
                font "DejaVuSans.ttf"
                yalign 0.5
                size gui.scale(16)
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
                        ysize gui.scale(66)
                        background None
                        hover_background Solid("#ffffff0d")
                        action [
                            SetVariable("phone_apps_page", "messages_thread"),
                            SetVariable("phone_apps_messages_contact", cid),
                            With(Dissolve(0.16)),
                        ]
                        hbox:
                            yalign 0.5
                            spacing gui.scale(10)
                            xfill True
                            if cid in wire_contacts:
                                use wire_avatar(cid, gui.scale(44))
                            else:
                                add Solid(contact["color"], xysize=(gui.scale(44), gui.scale(44)))
                            vbox:
                                xsize gui.scale(140)
                                spacing gui.scale(2)
                                text contact["name"]:
                                    size gui.scale(17)
                                    color "#e8eef2"
                                    outlines []
                                # Two lines of preview, clipped so a long message
                                # can never push the avatar out of its row.
                                fixed:
                                    xsize gui.scale(140)
                                    ysize gui.scale(34)
                                    clipping True
                                    text msg_last_text(cid):
                                        size gui.scale(13)
                                        color "#8b97a3"
                                        outlines []
                                        xmaximum gui.scale(140)
                            if unread:
                                fixed:
                                    xsize gui.scale(22)
                                    ysize gui.scale(22)
                                    add Solid("#c94f4f", xysize=(gui.scale(18), gui.scale(18)))
                                    text "[unread]":
                                        size gui.scale(10)
                                        color "#ffffff"
                                        outlines []
                                        xalign 0.5
                                        yalign 0.5
                            text ">":
                                style "phone_detail"
                                size gui.scale(15)
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
                size gui.scale(13)
                color "#75838d"
                textalign 0.5
                xmaximum gui.scale(menu_phone_content_w)
                outlines []

screen phone_app_messages_thread_contents(cid, typing=False, bottom_pad=18):
    $ contact = wire_contacts.get(cid, {"name": msg_contact_name(cid), "color": "#8fd8c8"})
    $ accent = contact.get("color", "#8fd8c8")
    $ thread = msg_thread(cid)
    $ typing_show_avatar = not (thread and not thread[-1]["me"])

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
            for index, msg in enumerate(thread):
                $ day_label = "YESTERDAY" if msg.get("day") == "yesterday" else "TODAY"
                $ prev_day_label = (("YESTERDAY" if thread[index - 1].get("day") == "yesterday" else "TODAY") if index else None)
                if day_label != prev_day_label:
                    text "[day_label]  ·  20:00":
                        xalign 0.5
                        size gui.scale(10)
                        kerning gui.scale(1)
                        color "#66757f"
                        outlines []
                $ same_sender = index > 0 and thread[index - 1]["me"] == msg["me"] and prev_day_label == day_label
                use phone_msg_bubble(msg, cid, accent, show_avatar=not same_sender)
            if typing:
                use phone_typing_bubble(cid, typing_show_avatar)
            null height gui.scale(bottom_pad)
