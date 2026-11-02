################################################################################
## WIRE — THE PHONE APP
################################################################################
##
## WIRE is what the phone in his pocket is actually for. It is where the people
## he meets end up, and it is the only place in the game that says out loud how
## far he has got with any of them.
##
## This file is laid out the same way locations.rpy is, and for the same reason:
##
##   * the story decides who he meets and when, and calls wire_unlock();
##   * wire_unlock() is the only thing that ever writes to wire_unlocked, so a
##     contact cannot be added twice and the app can never open for nothing;
##   * the screen only reads. It never touches a visit count.
##
## It reads those counts from where they already live. A contact whose id is in
## `confidant_visits` takes its progress from there; anybody else names their own
## variable in the entry.
##
## What the app deliberately does not do is print a rank, a level or a score.
## Progress is drawn as a row of ticks, one per visit, because that is what a
## signal meter looks like and because a row of ticks can be read at a glance
## without inviting the player to optimise it.
##
## --- ADDING SOMEBODY NEW ---
##
## Add one entry to wire_contacts, add its id to wire_order, and call
## `$ wire_unlock("orson")` in the scene where he is first met. Nothing else.
##
## Keys on an entry:
##   "name"     what the app calls them.
##   "handle"   the line under the name, in the app's own idiom.
##   "note"     the one line the row shows. Keep it short: two lines fit a row,
##              a third one does not.
##   "color"    the contact's own colour on the tile and the meter.
##   "progress" optional. A path into the store. Defaults to the person's own
##              slot in confidant_visits.
##   "photo"    optional. A square image to use instead of the monogram tile.


## The order the roster lists people in. It is fixed rather than
## most-recent-first so that the list does not reshuffle itself every time
## somebody is added, which is how a real contact list behaves.
define wire_order = ["hikari", "chef", "sim"]

define wire_contacts = {

    "hikari": {
        "name": "Hikari",
        "handle": "@hikari",
        # She is the one who put the app on his phone, and she is the only
        # contact who is family. The line is the thing she would not say to him
        # in the street, which is the reason she wants to be on here at all.
        "note": "The things she will not say out loud.",
        "color": "#e0849b",
        "progress": ("hikari_visits",),
    },

    "chef": {
        "name": "Chef",
        "handle": "@lantern",
        # He never gave his name, so the app has none. What he did give is the
        # one piece of information he decided a stranger actually needed.
        "note": "Closed Wednesdays. Don't walk here for nothing.",
        "color": "#d2793a",
    },

    "sim": {
        "name": "Sim",
        "handle": "@circle",
        "note": "The club group. Everybody posts what they shot.",
        "color": "#4fb8d9",
    },
}

## Who is in the phone. Only wire_unlock() writes to this list.
default wire_unlocked = []

## False until the app has been explained once, the same way every other system
## in the game earns its one explanation and then never repeats it.
default wire_hint_shown = False


## --- THE PHONE ITSELF ---
##
## Four numbers, and everything the screen draws is placed against them rather
## than against the display. `wire_phone_*` is the slab the player sees;
## `wire_bezel` is the border the screen sits inside; `wire_screen_*` is what is
## left, which is the only area the layout is allowed to think about.
##
## The proportions are the point. A phone is much taller than it is wide, and a
## slab that is only half again as tall as it is wide reads as a small tablet
## however good the contents are. Keeping the numbers here means the whole app
## can be resized, or moved to a different display resolution, by editing one
## line instead of every offset below it.
define wire_phone_w = 408
define wire_phone_h = 664
define wire_bezel = 12
define wire_screen_w = 384
define wire_screen_h = 640


init python:

    def wire_progress(contact_id):
        """How much of this person's story he has seen. Read-only."""
        path = wire_contacts.get(contact_id, {}).get("progress")

        if path is None:
            path = ("confidant_visits", contact_id)

        value = getattr(store, path[0], {})

        for key in path[1:]:
            if not isinstance(value, dict):
                return 0
            value = value.get(key, 0)

        return value if isinstance(value, int) else 0

    def wire_unlock(contact_id):
        """Put somebody in WIRE for the first time, then open the phone.

        Returns True the first time and False on every pass after that, so a
        scene that can be replayed adds nobody twice and interrupts nothing.

        The very first contact is the only one that needs the app explained, so
        it is the only one that gets a card first. Every one of them gets the
        phone itself, because the phone is the point: it stops the game, and
        the player watches the list they are building.
        """
        if contact_id in store.wire_unlocked:
            return False

        store.wire_unlocked.append(contact_id)

        if not store.wire_hint_shown:
            store.wire_hint_shown = True
            renpy.call_screen("hint_card", eyebrow="A NOTE ON YOUR PHONE",
                              body=store.hint_text_wire)

        # The same soft landing the attribute screen uses when a point arrives.
        # A name going into the phone is the same kind of event.
        play_sfx("audio/SFX/attribute_land.wav")

        renpy.call_screen("wire_app", new=contact_id)
        return True


# The one and only explanation of what the phone is for. It says what a name on
# the list means and stops there: what the player can do with the list is not
# decided yet, and a card that promises a mechanic would be lying.
define hint_text_wire = "WIRE is on your phone. It is where the people you meet end up.\n\nEvery name on it carries how far the two of you have come, and what that person is still holding on to.\n\nThere is no signal here yet. Everything on it is saved on the device."


################################################################################
## STYLES
################################################################################

style wire_button is default:
    background Solid("#17242ae0")
    hover_background Solid("#1f333cd0")
    insensitive_background Solid("#121a1f90")
    padding (gui.scale(20), gui.scale(9), gui.scale(20), gui.scale(9))

style wire_button_text is default:
    size gui.scale(15)
    kerning gui.scale(3)
    color "#6fc9bc"
    hover_color "#bff5ec"
    insensitive_color "#39504e"
    outlines []

style wire_label is default:
    size gui.scale(12)
    kerning gui.scale(3)
    color "#5a6a76"
    outlines []

style wire_name is default:
    size gui.scale(21)
    color "#e8eef2"
    outlines []

style wire_handle is default:
    size gui.scale(13)
    color "#5a6a76"
    outlines []

style wire_status is wire_label:
    size gui.scale(10)
    kerning gui.scale(2)

style wire_badge is default:
    size gui.scale(11)
    kerning gui.scale(2)
    color "#0d1115"
    outlines []

style wire_note is default:
    size gui.scale(14)
    line_spacing gui.scale(2)
    color "#8b97a3"
    outlines []

style wire_count is default:
    size gui.scale(12)
    kerning gui.scale(1)
    color "#5a6a76"
    outlines []

style wire_memory is default:
    size gui.scale(15)
    line_spacing gui.scale(3)
    color "#c3ccd5"
    outlines []


################################################################################
## MOTION
################################################################################
##
## All of these are bare named transforms with no arguments, for the reason the
## rest of the project uses them: a transform built from an argument is rebuilt
## on every screen pass and restarts its own animation, which would make the
## tiles flicker. A name is built once and holds still.

transform wire_backdrop_in:
    alpha 0.0
    linear 0.24 alpha 1.0

transform wire_backdrop_out:
    alpha 1.0
    linear 0.30 alpha 0.0

# The phone comes up out of the bottom of the frame the way a phone does when it
# is picked up: a short lift, settling rather than arriving.
transform wire_phone_in:
    alpha 0.0
    yoffset gui.scale(22)
    zoom 0.984
    ease 0.34 alpha 1.0 yoffset 0 zoom 1.0

transform wire_phone_out:
    alpha 1.0
    yoffset 0
    ease 0.28 alpha 0.0 yoffset gui.scale(12)

transform wire_body_in:
    alpha 0.0
    yoffset gui.scale(8)
    pause 0.10
    ease 0.34 alpha 1.0 yoffset 0

# The one thing on the screen that keeps moving. It marks the row that was just
# added and nothing else, so it is the only thing the eye is drawn to when the
# app opens, and it stops being true the moment the app closes.
transform wire_new_pulse:
    block:
        alpha 1.0
        ease 1.10 alpha 0.30
        ease 1.10 alpha 1.0
        repeat

# A five-pixel status light, breathing. It reads as "the app is running" and it
# gives the header somewhere to live while the roster is being read.
transform wire_live_dot:
    block:
        alpha 0.45
        ease 1.80 alpha 1.0
        ease 1.80 alpha 0.45
        repeat


################################################################################
## PIECES
################################################################################

## The contact's tile. A square of their own colour with their initial on it,
## and a bar along the bottom in the same colour. If the entry names a "photo",
## that is used instead, so real art can be dropped in with no code change.
screen wire_avatar(cid, px):

    $ wire_entry = wire_contacts[cid]
    $ wire_accent = wire_entry["color"]
    $ wire_photo = wire_entry.get("photo")
    $ wire_initial_size = int(px * 0.44)
    $ wire_bar = max(2, int(px * 0.05))

    fixed:
        xysize (px, px)

        if wire_photo and renpy.loadable(wire_photo):
            add Transform(wire_photo, xysize=(px, px), fit="cover")
        else:
            add Solid(wire_accent + "26", xysize=(px, px))

            text wire_entry["name"][0].upper():
                xalign 0.5
                yalign 0.5
                size wire_initial_size
                italic True
                color wire_accent
                outlines []

            add Solid(wire_accent, xysize=(px, wire_bar)) xpos 0 ypos (px - wire_bar)


## The progress meter. One tick per visit, filled up to where he has got to.
## There is no number attached to it anywhere on the roster, on purpose: the
## shape is the whole message.
screen wire_meter(seen, w, h, filled):

    hbox:
        spacing max(2, int(w * 0.75))

        for i in range(confidant_visits_total):
            add Solid(filled if i < seen else "#232b33", xysize=(w, h))


## One row of the roster. The tick that marks a row as new is the only thing
## here that is allowed to move.
screen wire_row(cid, is_new):

    $ wire_entry = wire_contacts[cid]
    $ wire_accent = wire_entry["color"]
    $ wire_seen = wire_progress(cid)

    # A row is as wide as the roster column, not as wide as the screen, because
    # the roster is inset by 12 either side. `wire_row_w` is the width the row
    # actually gets, and the two right-hand values below are measured back from
    # its right edge rather than from the display.
    $ wire_row_w = wire_screen_w - 24
    $ wire_readout_w = 64
    $ wire_info_w = wire_row_w - 178

    fixed:
        xysize (gui.scale(wire_row_w), gui.scale(118))

        add Solid("#182129" if is_new else "#121920", xysize=(gui.scale(wire_row_w), gui.scale(118)))

        # The contact's colour down the left edge. On the new row it breathes.
        if is_new:
            add Solid(wire_accent, xysize=(gui.scale(4), gui.scale(118))) at wire_new_pulse
        else:
            add Solid(wire_accent + "55", xysize=(gui.scale(4), gui.scale(118)))

        # `use` cannot take a property block, so the tile gets a box of its own
        # to sit in and the box does the placing.
        fixed:
            xpos gui.scale(16)
            ypos gui.scale(20)
            xysize (gui.scale(64), gui.scale(64))
            use wire_avatar(cid, gui.scale(64))

        vbox:
            xpos gui.scale(96)
            ypos gui.scale(16)
            spacing gui.scale(5)

            fixed:
                xsize gui.scale(wire_info_w)
                ysize gui.scale(30)

                text wire_entry["name"] style "wire_name":
                    xpos 0
                    ypos 0
                    xmaximum gui.scale(wire_info_w - 62)

                if is_new:
                    fixed:
                        xpos gui.scale(wire_info_w - 52)
                        ypos gui.scale(2)
                        xysize (gui.scale(52), gui.scale(20))
                        at wire_new_pulse

                        add Solid(wire_accent + "22")

                        text "NEW" style "wire_badge" color wire_accent:
                            xalign 0.5
                            yalign 0.5

            text wire_entry["handle"] style "wire_handle" xmaximum gui.scale(wire_info_w)

            # Stops 12 short of the readout block, so a long note wraps instead
            # of running under the meter.
            text wire_entry["note"] style "wire_note" xmaximum gui.scale(wire_info_w)

        # The readout on the right is given a width of its own, so the meter and
        # the count line up on the right edge together instead of each ending
        # wherever its own text happens to stop.
        vbox:
            xpos gui.scale(wire_row_w - 72)
            xsize gui.scale(wire_readout_w)
            ypos gui.scale(18)
            spacing gui.scale(12)

            hbox:
                xalign 1.0
                use wire_meter(wire_seen, gui.scale(4), gui.scale(14), wire_accent)

            text "[wire_seen] / [confidant_visits_total]" style "wire_count" xalign 1.0


## Everything the app knows about one person. The list at the bottom is the same
## memory the game records when he says something that matters, so the app is
## the one place the player can read back what a person is holding onto.
screen wire_profile(cid):

    $ wire_entry = wire_contacts[cid]
    $ wire_accent = wire_entry["color"]
    $ wire_seen = wire_progress(cid)
    $ wire_memories = character_memories.get(cid, [])

    # The viewport is inset by the same 12 the header uses, so every line of
    # text in the app starts on the same left edge whichever page is open.
    viewport:
        xpos gui.scale(12)
        ypos gui.scale(58)
        xysize (gui.scale(wire_screen_w - 24), gui.scale(wire_screen_h - 82))
        mousewheel True
        draggable True
        scrollbars None

        vbox:
            spacing gui.scale(16)

            use wire_avatar(cid, gui.scale(88))

            vbox:
                spacing gui.scale(4)
                text wire_entry["name"] style "wire_name" size gui.scale(27)
                text wire_entry["handle"] style "wire_handle"

            add Solid("#1e252d") xysize (gui.scale(wire_screen_w - 24), 1)

            vbox:
                spacing gui.scale(10)

                hbox:
                    spacing gui.scale(8)
                    use wire_meter(wire_seen, gui.scale(7), gui.scale(18), wire_accent)
                    text "[wire_seen] / [confidant_visits_total]" style "wire_count" yalign 1.0

                text wire_entry["note"] style "wire_note" size gui.scale(15) xmaximum gui.scale(wire_screen_w - 24)

            add Solid("#1e252d") xysize (gui.scale(wire_screen_w - 24), 1)

            text "WHAT THEY REMEMBER" style "wire_label"

            if wire_memories:
                for wire_memory in wire_memories:
                    text wire_memory style "wire_memory" xmaximum gui.scale(wire_screen_w - 24)
            else:
                text "Nothing yet." style "wire_note" italic True


################################################################################
## THE APP
################################################################################

screen wire_app(new=None):

    modal True
    zorder 120

    default hiding = False
    default selected = None

    # Nobody writes to wire_unlocked here. The screen just lists it, in the
    # order the app keeps its contacts in.
    $ roster = [c for c in wire_order if c in wire_unlocked]

    if hiding:
        add Solid("#04050a") at wire_backdrop_out
    else:
        add Solid("#04050a") at wire_backdrop_in

    frame:
        at (wire_phone_out if hiding else wire_phone_in)

        xalign 0.5
        yalign 0.5
        xysize (gui.scale(wire_phone_w), gui.scale(wire_phone_h))
        background Solid("#14181d")
        padding (gui.scale(wire_bezel), gui.scale(wire_bezel), gui.scale(wire_bezel), gui.scale(wire_bezel))

        # The screen inside the body. The body is only a bezel, so the inner
        # slab is a shade darker and everything else is drawn on it.
        fixed:
            xysize (gui.scale(wire_screen_w), gui.scale(wire_screen_h))

            add Solid("#0a0d11")

            if selected:

                fixed:
                    xalign 0.5
                    ypos gui.scale(10)
                    xysize (gui.scale(84), gui.scale(6))
                    add Solid("#1a2128")

                # --- the app's second page, and the way back to the first ---
                textbutton "BACK" action SetScreenVariable("selected", None) style "wire_button":
                    xpos gui.scale(16)
                    ypos gui.scale(20)

                use wire_profile(selected)

            else:

                # --- safe area / top app chrome ---
                fixed:
                    xalign 0.5
                    ypos gui.scale(10)
                    xysize (gui.scale(84), gui.scale(6))
                    add Solid("#1a2128")

                fixed:
                    xpos gui.scale(16)
                    ypos gui.scale(24)
                    xysize (gui.scale(wire_screen_w - 32), gui.scale(72))

                    fixed:
                        xpos 0
                        ypos gui.scale(8)
                        xysize (gui.scale(6), gui.scale(6))
                        at wire_live_dot
                        add Solid("#7fe0d0", xysize=(gui.scale(6), gui.scale(6)))

                    text "WIRE":
                        xpos gui.scale(14)
                        ypos 0
                        size gui.scale(27)
                        kerning gui.scale(5)
                        color "#7fe0d0"
                        outlines []

                    text "CONNECTIONS":
                        xpos gui.scale(14)
                        ypos gui.scale(34)
                        style "wire_label"

                    fixed:
                        xpos gui.scale(wire_screen_w - 140)
                        ypos gui.scale(30)
                        xysize (gui.scale(108), gui.scale(24))

                        add Solid("#141b22")

                        text "OFFLINE":
                            xalign 0.5
                            ypos gui.scale(3)
                            style "wire_status"
                            color "#6d7c88"

                    text "SAVED ON DEVICE":
                        xpos gui.scale(wire_screen_w - 16)
                        xanchor 1.0
                        ypos gui.scale(58)
                        style "wire_status"
                        color "#3f4d56"

                add Solid("#1e252d") xysize (gui.scale(wire_screen_w - 32), 1) xpos gui.scale(16) ypos gui.scale(108)

                # --- the roster ---
                #
                # Its height is whatever is left between the second header line
                # and the footer rule, so the roster grows with the phone.
                viewport:
                    at wire_body_in
                    xpos gui.scale(16)
                    ypos gui.scale(124)
                    xysize (gui.scale(wire_screen_w - 32), gui.scale(wire_screen_h - 236))
                    mousewheel True
                    draggable True
                    scrollbars None

                    vbox:
                        spacing gui.scale(12)

                        for wire_cid in roster:
                            button:
                                action SetScreenVariable("selected", wire_cid)
                                background None
                                hover_background Solid("#ffffff08")
                                use wire_row(wire_cid, wire_cid == new)

                # --- footer ---
                add Solid("#1e252d") xysize (gui.scale(wire_screen_w - 32), 1) xpos gui.scale(16) ypos gui.scale(wire_screen_h - 96)

                text "WIRE 1.0":
                    xpos gui.scale(16)
                    ypos gui.scale(wire_screen_h - 72)
                    style "wire_status"
                    color "#39464f"

                textbutton "PUT IT AWAY" action SetScreenVariable("hiding", True) style "wire_button" sensitive (not hiding):
                    xalign 0.5
                    ypos gui.scale(wire_screen_h - 84)

                fixed:
                    xalign 0.5
                    ypos gui.scale(wire_screen_h - 24)
                    xysize (gui.scale(116), gui.scale(5))
                    add Solid("#1a2128")

    if hiding:
        timer 0.300 action Return()
