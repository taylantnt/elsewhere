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
## Act 1 is the arrival (airport to first dream), which is before the player
## has any freedom at all, which is why the cap below starts at nothing.
## Act 2 is the long middle — the big act that holds every confidant arc.
## Act 3 is the glitch era; the final visits land while the world breaks.
default current_act = 1

## The most of a person's story each act allows. A place whose visits have
## caught up with its cap is paused: the person is still there and still
## talking, but nothing new about them happens until the story moves on. This
## is the one dial that stops the player from spending the whole game on a
## single person — turn a number up and that act opens more of everyone.
define act_confidant_cap = {
    1: 0,
    2: 5,
    3: 7,
    4: 7,
}


init python:

    def confidant_cap():
        # If the table ever runs out of acts, the story is open.
        return act_confidant_cap.get(current_act, confidant_visits_total)

    def all_confidants_met():
        # The introduction gate: nobody's story can be revisited until every
        # confidant has been met at least once. First visits are always open;
        # this only holds back seconds and later.
        return all(confidant_visits.get(c, 0) > 0 for c in confidant_order)

    def destination_state(place):
        # "ready"  - there is a visit waiting to be played here
        # "paused" - the act has not caught up; nothing new will happen yet
        # "later"  - already visited, but not everyone has been met yet
        # "closed" - all seven visits are done; the story has finished
        if place not in confidant_visits:
            return "ready"
        seen = confidant_visits[place]
        if seen >= confidant_visits_total:
            return "closed"
        if seen >= confidant_cap():
            return "paused"
        if seen > 0 and not all_confidants_met():
            return "later"
        return "ready"

    def hub_state_color(state):
        # The name on the row dims as the row has less to offer, so the list
        # reads at a glance before any of the marks are read.
        if state == "ready":
            return "#e6e1d8"
        if state == "later":
            return "#8a8377"
        if state == "paused":
            return "#6f6a60"
        return "#413d36"

    def hub_bar_color(state):
        if state == "paused":
            return "#7a7266"
        if state == "later":
            return "#5c574d"
        return "#2b2721"


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

screen location_hub(places=None, heading="Free Afternoon", blurb="Choose one destination for this afternoon."):

    modal True
    zorder notice_window_zorder
    $ hub_places = places if places is not None else confidant_order

    add Solid("#000000") at notice_backdrop_in
    use standalone_notice_window(heading, "DESTINATIONS", notice_window_in):
        text blurb style "guide_body" xsize gui.scale(648)
        viewport:
            ypos gui.scale(54)
            xysize (gui.scale(648), gui.scale(156))
            mousewheel True
            draggable True
            vbox:
                spacing gui.scale(4)
                for place in hub_places:
                    $ place_state = destination_state(place)
                    $ place_name = destination_names.get(place, place)
                    $ place_status = {"ready": "Visit available", "paused": "No new visit yet", "later": "Come back another day", "closed": "Story complete"}[place_state]
                    button:
                        action Return(place)
                        sensitive (place_state == "ready")
                        background Solid("#25221d")
                        hover_background Solid("#393126")
                        insensitive_background Solid("#181714")
                        padding (gui.scale(12), gui.scale(10))
                        fixed:
                            xysize (gui.scale(624), gui.scale(26))
                            text place_name style "guide_body" color hub_state_color(place_state) yalign 0.5
                            text place_status style "guide_meta" xalign 1.0 yalign 0.5
        use standalone_notice_footer("Scroll to see more destinations.", "Head Home", Return(None))
