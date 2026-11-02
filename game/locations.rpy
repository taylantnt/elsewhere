## Locations, Confidants and the Hub ###########################################
##
## Everything the game needs to answer two questions: "where can I go?" and "is
## there anything waiting for me there?"
##
## Nothing in this file plays a scene. It keeps the bookkeeping — how much of a
## person's story the player has seen — and draws the one screen that shows it.
## The story decides when the screen opens and what happens when a row is picked.
##
## The rule the screen exists to express:
##   * a person's story is told in seven visits, one per outing;
##   * the story only lets it move so far in each act, so a place is either
##     *waiting* (there is a scene to play) or *paused* (the act has not caught
##     up, and nothing new will happen until it does).


## --- THE PEOPLE AND THEIR PLACES ---
##
## `confidant_order` is the five written storylines. `destination_names` is what
## the player reads on a row, and it also holds the two plain activities that
## have no seven-visit story of their own: walking home with Hikari, and walking
## home alone. A destination that is not in `confidant_visits` is always waiting,
## because there is no story there to hold back.

define confidant_order = ["sim", "orson", "chef", "aya", "hana"]

define destination_names = {
    "sim":   "Photography Club",
    "orson": "Lupin's Den",
    "chef":  "Ramen Shop",
    "aya":   "Maid Cafe",
    "hana":  "Reading Club",
    "walk_hikari": "Walk home with Hikari",
    "walk_alone":  "Walk home alone",
}

## How many of the seven visits have happened. Zero means they have never been
## met. Only the story writes these; the screen only reads them.
default confidant_visits = {
    "sim": 0,
    "orson": 0,
    "chef": 0,
    "aya": 0,
    "hana": 0,
}

## Seven visits and the story is over: the person leaves, and the row has
## nothing left to give.
define confidant_visits_total = 7

## Which part of the story we are in. The story bumps this at an act break.
## Act 1 is the first day, which is before the player has any freedom at all,
## which is why the cap below starts at nothing.
default current_act = 1

## The most of a person's story each act allows. A place whose visits have
## caught up with its cap is paused: the person is still there and still
## talking, but nothing new about them happens until the story moves on. This
## is the one dial that stops the player from spending the whole game on a
## single person — turn a number up and that act opens more of everyone.
define act_confidant_cap = {
    1: 0,
    2: 3,
    3: 5,
    4: 7,
}


init python:

    def confidant_cap():
        # If the table ever runs out of acts, the story is open.
        return act_confidant_cap.get(current_act, confidant_visits_total)

    def destination_state(place):
        # "ready"  - there is a visit waiting to be played here
        # "paused" - the act has not caught up; nothing new will happen yet
        # "closed" - all seven visits are done; the story has finished
        if place not in confidant_visits:
            return "ready"
        seen = confidant_visits[place]
        if seen >= confidant_visits_total:
            return "closed"
        if seen >= confidant_cap():
            return "paused"
        return "ready"

    def hub_state_color(state):
        # The name on the row dims as the row has less to offer, so the list
        # reads at a glance before any of the marks are read.
        if state == "ready":
            return "#e6e1d8"
        if state == "paused":
            return "#6f6a60"
        return "#413d36"

    def hub_bar_color(state):
        return "#7a7266" if state == "paused" else "#2b2721"


## --- STYLES ---

style hub_place is default:
    size gui.scale(26)
    italic True
    kerning gui.scale(2)

style hub_mark_text is default:
    size gui.scale(20)
    italic True
    kerning gui.scale(3)

style hub_legend_text is default:
    size gui.scale(17)
    color "#8a8377"
    kerning gui.scale(0.5)

style hub_button is default:
    background None
    hover_background Solid("#3d362bf0")
    insensitive_background None
    padding (gui.scale(26), gui.scale(9), gui.scale(26), gui.scale(9))


## --- THE MARK ---
##
## The mark beside a row. The pause is drawn as two solid blocks rather than
## typed, because no font in the project can be relied on to carry a pause
## glyph and a missing one prints as an empty box.

screen hub_mark(state):

    fixed:
        xsize gui.scale(54)
        ysize gui.scale(24)

        if state == "ready":
            text "( ! )" style "hub_mark_text" color gui.accent_color xalign 0.5 yalign 0.5
        else:
            hbox:
                xalign 0.5
                yalign 0.5
                spacing gui.scale(5)

                add Solid(hub_bar_color(state)) xysize (gui.scale(3), gui.scale(18))
                add Solid(hub_bar_color(state)) xysize (gui.scale(3), gui.scale(18))


## --- THE HUB ---
##
## `places` is which rows to show, and in what order. Leave it out and every
## confidant location is listed. `heading` and `blurb` are the two lines at the
## top, so the same screen can open after school, at night, or on a day off
## without a second copy of it existing.
##
## The screen returns the id of the row that was picked (e.g. "sim"), or None if
## the player chose to leave the day as it is. Only a waiting row can be picked:
## a paused or finished place does nothing when clicked, which is the point of
## the mark.

screen location_hub(places=None, heading="AFTER SCHOOL", blurb="The rest of the day is yours. Pick one place."):

    modal True

    $ hub_places = places if places is not None else confidant_order

    add Solid("#0b0a09e6")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing gui.scale(30)

        vbox:
            xalign 0.5
            spacing gui.scale(13)

            text heading style "notice_label" xalign 0.5
            add Solid("#3a352e") xysize (gui.scale(380), 1) xalign 0.5
            text blurb style "notice_body" xalign 0.5

        vbox:
            xalign 0.5
            spacing gui.scale(2)

            for place in hub_places:

                $ place_state = destination_state(place)
                $ place_name = destination_names.get(place, place)

                button:
                    style "hub_button"
                    action Return(place)
                    sensitive (place_state == "ready")

                    fixed:
                        xsize gui.scale(560)
                        ysize gui.scale(44)

                        text place_name:
                            style "hub_place"
                            color hub_state_color(place_state)
                            xalign 0.0
                            yalign 0.5

                        fixed:
                            xalign 1.0
                            yalign 0.5
                            use hub_mark(place_state)

        vbox:
            xalign 0.5
            spacing gui.scale(9)

            add Solid("#241f19") xysize (gui.scale(380), 1) xalign 0.5

            hbox:
                xalign 0.0
                spacing gui.scale(18)

                fixed:
                    xsize gui.scale(54)
                    ysize gui.scale(24)
                    text "( ! )" style "hub_mark_text" color gui.accent_color xalign 0.5 yalign 0.5

                text "Something is waiting here." style "hub_legend_text" yalign 0.5

            hbox:
                xalign 0.0
                spacing gui.scale(18)

                fixed:
                    xsize gui.scale(54)
                    ysize gui.scale(24)
                    hbox:
                        xalign 0.5
                        yalign 0.5
                        spacing gui.scale(5)
                        add Solid(hub_bar_color("paused")) xysize (gui.scale(3), gui.scale(18))
                        add Solid(hub_bar_color("paused")) xysize (gui.scale(3), gui.scale(18))

                text "Nothing new yet. Come back later in the story." style "hub_legend_text" yalign 0.5

            hbox:
                xalign 0.0
                spacing gui.scale(18)

                fixed:
                    xsize gui.scale(54)
                    ysize gui.scale(24)
                    hbox:
                        xalign 0.5
                        yalign 0.5
                        spacing gui.scale(5)
                        add Solid(hub_bar_color("closed")) xysize (gui.scale(3), gui.scale(18))
                        add Solid(hub_bar_color("closed")) xysize (gui.scale(3), gui.scale(18))

                text "Their story has finished, and they have moved on." style "hub_legend_text" yalign 0.5

        # A hub with no door out is a softlock waiting to happen, so leaving is
        # always on offer. It costs the day, which is what makes picking a place
        # matter.
        textbutton "Leave it for today." action Return(None) style "notice_button" xalign 0.5
