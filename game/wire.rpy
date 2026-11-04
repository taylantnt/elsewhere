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
##   * wire_open() is how menus and the quick shortcut reopen the app later;
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
##   "note"     the short line the row shows. It can wrap to two lines.
##   "color"    the contact's own colour on the tile and the meter.
##   "progress" optional. A path into the store. Defaults to the person's own
##              slot in confidant_visits.
##   "photo"    optional. A portrait image to use instead of the monogram tile.
##   "photo_crop" optional. A normalized (x, y, width, height) face crop.


## The order the roster lists people in. It is fixed rather than
## most-recent-first so that the list does not reshuffle itself every time
## somebody is added, which is how a real contact list behaves.
define wire_order = ["hikari", "chef", "sim", "aya"]

define wire_contacts = {

    "hikari": {
        "name": "Hikari",
        "handle": "@hikari",
        # She is the one who put the app on his phone, and she is the only
        # contact who is family. The line is the thing she would not say to him
        # in the street, which is the reason she wants to be on here at all.
        "note": "The things she will not say out loud.",
        "color": "#e0849b",
        "photo": "images/characters/sister.png",
        "photo_crop": (0.13, 0.015, 0.60, 0.40),
        "progress": ("hikari_visits",),
    },

    "chef": {
        "name": "Chef",
        "handle": "@lantern",
        # He never gave his name, so the app has none. What he did give is the
        # one piece of information he decided a stranger actually needed.
        "note": "Closed Wednesdays. Don't walk here for nothing.",
        "color": "#d2793a",
        "photo": "images/characters/chef.png",
        "photo_crop": (0.25, 0.005, 0.48, 0.32),
    },

    "sim": {
        "name": "Sim",
        "handle": "@circle",
        "note": "The club group. Everybody posts what they shot.",
        "color": "#4fb8d9",
        "photo": "images/characters/sim.png",
        "photo_crop": (0.25, 0.0, 0.50, 0.333),
    },

    "aya": {
        "name": "Aya",
        "handle": "@maidfever",
        "note": "A first visit, a kitty in ketchup, and a little magic.",
        "color": "#e084b7",
        "photo": "images/characters/aya.png",
        "photo_crop": (0.28, 0.04, 0.45, 0.28),
        "progress": ("confidant_visits", "aya"),
    },
}

## Who is in the phone. Only wire_unlock() writes to this list.
default wire_unlocked = []

## Local contact records remain available offline; syncing needs mobile data.
default cellular_data_active = False

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
            renpy.call_screen("hint_card", eyebrow="WIRE",
                              body=store.hint_text_wire)

        # The same soft landing the attribute screen uses when a point arrives.
        # A name going into the phone is the same kind of event.
        play_sfx("audio/SFX/wire_connect.wav")

        renpy.call_screen("wire_app", new=contact_id)
        return True

    def wire_open():
        """Reopen WIRE from a menu or shortcut. Quiet if the list is still empty."""
        if not store.wire_unlocked:
            return
        # A new context keeps the quick menu from eating the dialogue underneath.
        renpy.call_in_new_context("_wire_open")


# Private entry point for wire_open(). Kept as a label so call screen can Return
# cleanly without the shortcut needing to know how the phone dismisses itself.
label _wire_open:
    call screen wire_app
    return


# The one and only explanation of what the phone is for. It says what a name on
# the list means and stops there: what the player can do with the list is not
# decided yet, and a card that promises a mechanic would be lying.
define hint_text_wire = "WIRE keeps local records of the people you get to know. Select a contact to see your visits and the moments they remember.\n\nProfiles stay on your phone, but messages, group posts, and updates need an internet connection. Without a data plan, WIRE cannot sync when you are away from Wi-Fi."


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
    size gui.scale(13)
    line_spacing gui.scale(1)
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
            add Solid(wire_accent + "26", xysize=(px, px))
            add Transform(wire_photo, crop=wire_entry.get("photo_crop"), xysize=(px, px))
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

    # The progress readout sits below the note so long descriptions keep the
    # full width of the card.
    $ wire_row_w = wire_screen_w - 24
    $ wire_info_w = wire_row_w - 108

    fixed:
        xysize (gui.scale(wire_row_w), gui.scale(112))

        add Solid("#1a282d" if is_new else "#141c22", xysize=(gui.scale(wire_row_w), gui.scale(112)))

        # The contact's colour down the left edge. On the new row it breathes.
        if is_new:
            add Solid(wire_accent, xysize=(gui.scale(3), gui.scale(112))) at wire_new_pulse
        else:
            add Solid(wire_accent + "55", xysize=(gui.scale(3), gui.scale(112)))

        # `use` cannot take a property block, so the tile gets a box of its own
        # to sit in and the box does the placing.
        fixed:
            xpos gui.scale(14)
            ypos gui.scale(22)
            xysize (gui.scale(56), gui.scale(56))
            use wire_avatar(cid, gui.scale(56))

        vbox:
            xpos gui.scale(82)
            ypos gui.scale(10)
            spacing gui.scale(2)

            fixed:
                xsize gui.scale(wire_info_w)
                ysize gui.scale(24)

                text wire_entry["name"] style "wire_name":
                    xpos 0
                    ypos 0
                    size gui.scale(19)
                    xmaximum gui.scale(wire_info_w - 58)

                if is_new:
                    fixed:
                        xpos gui.scale(wire_info_w - 48)
                        ypos gui.scale(2)
                        xysize (gui.scale(46), gui.scale(18))
                        at wire_new_pulse

                        add Solid(wire_accent + "22")

                        text "NEW" style "wire_badge" color wire_accent:
                            xalign 0.5
                            yalign 0.5

            text wire_entry["handle"] style "wire_handle" size gui.scale(12) xmaximum gui.scale(wire_info_w)

            text wire_entry["note"] style "wire_note" xmaximum gui.scale(wire_info_w) ymaximum gui.scale(34)

        hbox:
            xpos gui.scale(82)
            ypos gui.scale(91)
            spacing gui.scale(7)

            use wire_meter(wire_seen, gui.scale(4), gui.scale(8), wire_accent)

            text "[wire_seen] / [confidant_visits_total]" style "wire_count" yalign 0.5


## Everything the app knows about one person. The list at the bottom is the same
## memory the game records when he says something that matters, so the app is
## the one place the player can read back what a person is holding onto.
screen wire_profile(cid):

    $ wire_entry = wire_contacts[cid]
    $ wire_accent = wire_entry["color"]
    $ wire_seen = wire_progress(cid)
    $ wire_memories = character_memories.get(cid, [])

    # The viewport stays below the status and navigation bars.
    viewport:
        xpos gui.scale(12)
        ypos gui.scale(68)
        xysize (gui.scale(wire_screen_w - 24), gui.scale(wire_screen_h - 92))
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

            add Solid("#243139") xysize (gui.scale(wire_screen_w - 24), 1)

            vbox:
                spacing gui.scale(10)

                hbox:
                    spacing gui.scale(8)
                    use wire_meter(wire_seen, gui.scale(7), gui.scale(18), wire_accent)
                    text "[wire_seen] / [confidant_visits_total]" style "wire_count" yalign 1.0

                text wire_entry["note"] style "wire_note" size gui.scale(15) xmaximum gui.scale(wire_screen_w - 24)

            add Solid("#243139") xysize (gui.scale(wire_screen_w - 24), 1)

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

            # A quiet status bar makes the app feel native to the handset
            # without adding controls that the story does not support.
            text "9:41":
                xpos gui.scale(16)
                ypos gui.scale(5)
                size gui.scale(10)
                color "#75838d"
                outlines []

            if cellular_data_active:
                text "HAMADA 5G":
                    xpos gui.scale(wire_screen_w - 16)
                    xanchor 1.0
                    ypos gui.scale(5)
                    size gui.scale(9)
                    kerning gui.scale(1)
                    color "#7fe0d0"
                    outlines []
            else:
                text "NO SIGNAL":
                    xpos gui.scale(wire_screen_w - 16)
                    xanchor 1.0
                    ypos gui.scale(5)
                    size gui.scale(9)
                    kerning gui.scale(1)
                    color "#596872"
                    outlines []

            if selected:

                fixed:
                    xalign 0.5
                    ypos gui.scale(25)
                    xysize (gui.scale(42), gui.scale(4))
                    add Solid("#26313a")

                # --- the app's second page, and the way back to the first ---
                textbutton "BACK" action SetScreenVariable("selected", None) style "wire_button":
                    xpos gui.scale(12)
                    ypos gui.scale(22)

                use wire_profile(selected)

            else:

                # --- safe area / top app chrome ---
                fixed:
                    xalign 0.5
                    ypos gui.scale(25)
                    xysize (gui.scale(42), gui.scale(4))
                    add Solid("#26313a")

                fixed:
                    xpos gui.scale(16)
                    ypos gui.scale(34)
                    xysize (gui.scale(wire_screen_w - 32), gui.scale(68))

                    fixed:
                        xpos 0
                        ypos gui.scale(10)
                        xysize (gui.scale(6), gui.scale(6))
                        at wire_live_dot
                        add Solid("#7fe0d0" if cellular_data_active else "#75838d", xysize=(gui.scale(6), gui.scale(6)))

                    text "WIRE":
                        xpos gui.scale(14)
                        ypos 0
                        size gui.scale(25)
                        kerning gui.scale(5)
                        color "#7fe0d0"
                        outlines []

                    text "CONNECTIONS":
                        xpos gui.scale(14)
                        ypos gui.scale(34)
                        style "wire_label"

                    fixed:
                        xpos gui.scale(wire_screen_w - 100)
                        ypos gui.scale(34)
                        xysize (gui.scale(84), gui.scale(24))

                        add Solid("#18232a")

                        if cellular_data_active:
                            for bar in range(4):
                                add Solid("#7fe0d0") xpos gui.scale(8 + bar * 5) ypos gui.scale(15 - bar * 3) xysize (gui.scale(3), gui.scale(5 + bar * 3))

                            text "5G":
                                xpos gui.scale(34)
                                ypos gui.scale(3)
                                style "wire_status"
                                color "#7fe0d0"
                        else:
                            text "OFFLINE":
                                xalign 0.5
                                ypos gui.scale(3)
                                style "wire_status"
                                color "#8998a2"

                add Solid("#243139") xysize (gui.scale(wire_screen_w - 32), 1) xpos gui.scale(16) ypos gui.scale(110)

                # --- the roster ---
                #
                # Its height is whatever is left between the second header line
                # and the footer rule, so the roster grows with the phone.
                viewport:
                    at wire_body_in
                    xpos gui.scale(16)
                    ypos gui.scale(122)
                    xysize (gui.scale(wire_screen_w - 32), gui.scale(wire_screen_h - 228))
                    mousewheel True
                    draggable True
                    scrollbars None

                    vbox:
                        spacing gui.scale(9)

                        for wire_cid in roster:
                            button:
                                action SetScreenVariable("selected", wire_cid)
                                background None
                                hover_background Solid("#ffffff08")
                                use wire_row(wire_cid, wire_cid == new)

                # --- footer ---
                add Solid("#243139") xysize (gui.scale(wire_screen_w - 32), 1) xpos gui.scale(16) ypos gui.scale(wire_screen_h - 92)

                text ("SYNCED" if cellular_data_active else "SAVED ON DEVICE"):
                    xpos gui.scale(16)
                    ypos gui.scale(wire_screen_h - 73)
                    style "wire_status"
                    color ("#7fa99f" if cellular_data_active else "#596872")

                textbutton "CLOSE APP" action SetScreenVariable("hiding", True) style "wire_button" sensitive (not hiding):
                    xalign 1.0
                    xoffset gui.scale(-16)
                    ypos gui.scale(wire_screen_h - 82)

                fixed:
                    xalign 0.5
                    ypos gui.scale(wire_screen_h - 15)
                    xysize (gui.scale(72), gui.scale(4))
                    add Solid("#26313a")

    if hiding:
        timer 0.300 action Return()
