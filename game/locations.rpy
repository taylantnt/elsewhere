## Locations, Confidants and the Hub ###########################################
##
## Everything the game needs to answer two questions: "where can I go?" and "is
## there anything waiting for me there?"
##
## Nothing in this file plays a scene. It keeps the bookkeeping ― how much of a
## person's story the player has seen ― and draws the one screen that shows it.
## The story decides when the screen opens and what happens when a row is picked.
##
## The rule the screen exists to express:
##   * a person's story is told in seven visits, one per outing ― Chef's and
##     Hana's run to eight, because their eighth is the closed place, the end
##     of the arc;
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
    "hana":  "Library",
    "fortune": "Asakusa: The Fortune Teller",
    "walk_hikari": "Walk home with Hikari",
    "message_hikari": "Message Hikari",
    "walk_alone":  "Walk home alone",
    "home":        "Home",
    "library":     "Campus Library",
    "river":       "Riverbank",
    "harajuku":    "Harajuku: Takeshita Street",
    "karaoke":     "Karaoke Box",
    "night_market": "Night Food Stalls",
    "combini":     "Combini",
    "odaiba":      "Odaiba",
    "yokohama":    "Yokohama Chinatown",
    "ueno":        "Ueno Park",
    "shibuya":     "Shibuya Crossing",
    "shimokitazawa": "Shimokitazawa",
    "omotesando":  "Omotesando / Meiji Shrine",
    "tanaka":      "Combini: Night Shift",
}

## The city rows. These are not confidant arcs: no visits, no cap, no closing.
## They exist so a paused or closed afternoon still has somewhere to go.
define city_row_order = [
    "library", "river", "harajuku", "karaoke", "night_market", "combini",
    "odaiba", "yokohama", "ueno", "shibuya", "shimokitazawa", "omotesando",
    # The night shift is a city row, not a person: it is a place he goes to
    # work. It is filtered out until Tanaka puts the card in the window.
    "tanaka",
]

## How many of the seven visits have happened. Zero means they have never been
## met. Only the story writes these; the screen only reads them.
default confidant_visits = {
    "sim": 0,
    "orson": 0,
    "chef": 0,
    "aya": 0,
    "hana": 0,
    # The Fortune Teller is the one deliberate exception to the seven-visit
    # rule: three cards, three meetings, and then the deck is closed. She is
    # still not part of `confidant_order`, so she can never hold back the five
    # original arcs or their introduction gate.
    "fortune": 0,
}

## The hub row picked this afternoon, or None for Head Home. The day scene
## reads it on the way into dinner so the evening can carry the afternoon home.
default last_afternoon_place = None

## True when the picked row became one of Hikari's river runs rather than the
## ordinary walk home. The evening uses it to tell the two apart.
default last_afternoon_was_run = False

## Places Hikari has introduced during a Message Hikari outing. Once a place is
## in this list, its hub row is unlocked and can be visited alone later.
default hikari_tour_unlocked = []

## True while this afternoon's trip was one of Hikari's tours rather than a solo
## visit. The tour labels reset it before the hub row runs.
default last_afternoon_hikari_tour = False

## Day 7's dinner needs to know whether Hikari came home with him or was
## already at the table. She cannot be "home waiting" if she ran the river
## path beside him, so the ordinary dinner greeting forks on this.
default day7_walked_with_hikari = False

## Seven visits and the story is over: the person leaves. Every one of the five
## confidants then gets an eighth visit, the epilogue, where the place is still
## there and the person is not. The epilogue is repeatable: the row stays
## clickable and plays the same closing scene every time. `confidant_visit_totals`
## names the exceptions: the five arcs run to eight, and the Fortune Teller's
## shorter arc runs to three.
define confidant_visits_total = 7

define confidant_visit_totals = {
    "sim": 8,
    "orson": 8,
    "chef": 8,
    "aya": 8,
    "hana": 8,
    "fortune": 3,
}

## Which part of the story we are in. The story bumps this at an act break.
## Act 1 is the arrival (airport to first dream), which is before the player
## has any freedom at all, which is why the cap below starts at nothing.
## Act 2 is the long middle ― the big act that holds every confidant arc.
## Act 3 is the glitch era; the final visits land while the world breaks.
default current_act = 1

## The most of a person's story each act allows. A place whose visits have
## caught up with its cap is paused: the person is still there and still
## talking, but nothing new about them happens until the story moves on. This
## is the one dial that stops the player from spending the whole game on a
## single person ― turn a number up and that act opens more of everyone.
define act_confidant_cap = {
    1: 0,
    # Act 2 is the long middle and holds every written confidant arc. The caps
    # for Acts 3 and 4 were designed around glitch-era story that has not been
    # written yet; until those act breaks exist, keeping the cap at 5 strands
    # visits 6-8 behind an act the game never enters. Open the whole written arc
    # here and keep the "later" gate below as the anti-focusing rule. When the
    # Act 3/4 content lands, retune these numbers to pace it again.
    2: 8,
    3: 8,
    4: 8,
}


init python:

    # Destinations that are shown on the hub but cannot be travelled to yet.
    # They stay visible (greyed out) so the player can see where they will
    # eventually go; the unlock rules for each land later.
    disabled_destinations = {
        "walk_alone",
        "harajuku", "karaoke", "combini", "odaiba", "yokohama",
        "ueno", "shibuya", "shimokitazawa", "omotesando",
    }

    # The city destinations Message Hikari can introduce. They all begin locked;
    # the first tour adds one id to `hikari_tour_unlocked`, which opens both the
    # hub row and the ordinary solo city_row_* label.
    hikari_tour_spots = [
        "harajuku", "karaoke", "combini", "odaiba", "yokohama",
        "ueno", "shibuya", "shimokitazawa", "omotesando",
    ]

    # Only the tours with a written scene are offered. Add a place id here when
    # its label is ready; until then Message Hikari will not send the player into
    # a placeholder. Yokohama, Harajuku, Kuru Fuku Neko, Ueno, Shimokitazawa and
    # Omotesando / Meiji Shrine are written. The picker chooses randomly among
    # whatever is still locked.
    hikari_tour_written = ["yokohama", "harajuku", "karaoke", "ueno", "shimokitazawa", "omotesando"]

    def destination_unlocked(place):
        return place in store.hikari_tour_unlocked

    def destination_locked(place):
        return place in disabled_destinations and not destination_unlocked(place)

    def hikari_tour_available_spots():
        return [p for p in hikari_tour_spots if not destination_unlocked(p)]

    def unlock_hikari_tour_destination(place):
        if place not in store.hikari_tour_unlocked:
            store.hikari_tour_unlocked.append(place)

    # Console test helper: mark every written tour except one as already seen,
    # so the picker is forced to offer the one under test.
    def force_hikari_tour_spot(spot):
        store.hikari_tour_unlocked = [p for p in store.hikari_tour_written if p != spot]

    def confidant_cap():
        # If the table ever runs out of acts, the story is open.
        return act_confidant_cap.get(current_act, max(act_confidant_cap.values()))

    def confidant_visits_total_for(place):
        return confidant_visit_totals.get(place, confidant_visits_total)

    def all_confidants_met():
        # The introduction gate: nobody's story can be revisited until every
        # confidant has been met at least once. First visits are always open;
        # this only holds back seconds and later. The Fortune Teller is not in
        # `confidant_order`, so she can never block the original five.
        return all(confidant_visits.get(c, 0) > 0 for c in confidant_order)

    def hub_destination_order():
        """Every row the hub should show today, in reading order.

        The five original confidants stay first. The Fortune Teller joins the
        people only once her Asakusa card has been turned. The city rows follow,
        and the night shift appears at the bottom of the city list only after
        Tanaka has put the HELP WANTED card in his window.
        """
        people = list(confidant_order)
        if store.fortune_arc_started:
            people.append("fortune")
        # Riverbank, the night market, and the old separate Campus Library row
        # are gone from the hub entirely. Home routes into Hikari's run chain;
        # Message Hikari is the tour row that unlocks the locked city places.
        people += ["message_hikari", "walk_alone", "home"]

        removed_from_hub = {"river", "night_market", "library"}
        city = [
            p for p in city_row_order
            if p not in removed_from_hub
            and (p != "tanaka" or store.combini_job_unlocked)
        ]

        return people + city

    def destination_state(place):
        # "ready"        - there is a visit waiting to be played here
        # "epilogue"     - the seven visits are done; the place remains, and the
        #                  same closing scene can be replayed
        # "paused"       - the act has not caught up; nothing new will happen yet
        # "later"        - already visited, but not everyone has been met yet
        # "closed_today" - the place keeps weekly hours and is shut today
        # "closed"       - every visit is done; the story has finished
        # "locked" is folded into "paused" for colour purposes; the row label
        # and short mark below special-case the disabled set.
        if destination_locked(place):
            return "paused"
        if place not in confidant_visits:
            return "ready"
        seen = confidant_visits[place]
        # The five confidants keep their epilogue after the seventh visit. It
        # opens immediately, even when the act cap would otherwise pause them,
        # because the farewell is the end of the numbered arc.
        if place in confidant_order and seen >= 7:
            return "epilogue"
        if seen >= confidant_visits_total_for(place):
            return "closed"
        if not destination_is_open(place):
            return "closed_today"
        if seen >= confidant_cap():
            return "paused"
        if seen > 0 and not all_confidants_met():
            return "later"
        return "ready"

    def destination_state_label(place, state):
        if state == "ready":
            return "Visit available"
        if state == "epilogue":
            return "The story is over. The place remains."
        if destination_locked(place):
            return "Not available yet"
        # A place held by the introduction gate wears the same neutral line as
        # one held by the act cap. The player does not need to know which
        # mechanism is waiting, only that today has nothing new.
        if state == "paused" or state == "later":
            return "No new visit yet"
        if state == "closed_today":
            return destination_schedule_note(place)
        return "Story complete"

    def hub_state_color(state):
        # The name on the row dims as the row has less to offer, so the list
        # reads at a glance before any of the marks are read. "later" is shown
        # as "paused": the introduction gate is an internal reason, not a label
        # the player should see.
        if state == "ready":
            return "#e6e1d8"
        if state == "epilogue":
            return "#d6c7ae"
        if state == "paused" or state == "later" or state == "closed_today":
            return "#6f6a60"
        return "#413d36"

    def hub_bar_color(state):
        if state == "epilogue":
            return "#9a8a72"
        if state == "paused" or state == "later" or state == "closed_today":
            return "#7a7266"
        return "#2b2721"

    def hub_pin_color(state):
        # The map pin and the list dot share one colour language, so a player
        # can read the map without opening the legend and still be right.
        if state == "ready":
            return "#c8a06a"
        if state == "epilogue":
            return "#b8a382"
        if state == "paused" or state == "later":
            return "#7a8a94"
        if state == "closed_today":
            return "#5c574d"
        return "#413d36"

    def hub_state_short(state, place=None):
        # The row's right-hand label and the map legend share one short
        # vocabulary, so the list and the legend never disagree. "later" is
        # deliberately folded into "No new": naming it would hint at content
        # the player has not met yet.
        if destination_locked(place):
            return "Locked"
        if state == "ready":
            return "New"
        if state == "epilogue":
            return "Epilogue"
        if state == "paused" or state == "later":
            return "No new"
        if state == "closed_today":
            return "Closed"
        return "Complete"

    def hub_status_color(state):
        if state == "ready":
            return "#c8a06a"
        if state == "epilogue":
            return "#c0b09a"
        if state == "paused" or state == "later":
            return "#7a8a94"
        if state == "closed_today":
            return "#6f6a60"
        return "#413d36"

    def hub_legend_items():
        # No "later" entry: the state still exists, but it is shown as
        # "No new" so the legend never advertises an unmet cast.
        return [
            ("ready", hub_state_short("ready")),
            ("paused", hub_state_short("paused")),
            ("closed_today", hub_state_short("closed_today")),
            ("epilogue", hub_state_short("epilogue")),
            ("closed", hub_state_short("closed")),
        ]


## --- STYLES ---

style hub_mark_text is default:
    size gui.scale(20)
    italic True
    kerning gui.scale(3)

style hub_row_name is default:
    font guide_font
    size gui.scale(14)
    color "#e6e1d8"
    outlines []

style hub_row_status is default:
    font guide_font
    size gui.scale(9)
    color "#8a8377"
    outlines []

style hub_legend_text is default:
    font guide_font
    size gui.scale(9)
    color "#8a8377"
    outlines []


## --- MOTION ---
##
## Bare named transforms, not calls with arguments: a screen rebuilds a
## displayable whenever its `at` changes, and a transform built fresh on each
## render would restart instead of settling. The hub rebuilds on every hover
## because the map header follows the cursor, so this matters here more than
## usual.

transform hub_left_in:
    alpha 0.0
    xoffset -14
    easeout 0.40 alpha 1.0 xoffset 0

transform hub_right_in:
    alpha 0.0
    xoffset 14
    pause 0.06
    easeout 0.44 alpha 1.0 xoffset 0

transform hub_tip_in:
    alpha 0.0
    easeout 0.18 alpha 1.0

transform hub_row_hover:
    on idle:
        easeout 0.16 xoffset 0
    on hover:
        easeout 0.16 xoffset 3

transform hub_row_still:
    xoffset 0

transform hub_pin_hover:
    on idle:
        easeout 0.16 yoffset 0
    on hover:
        easeout 0.16 yoffset -2

transform hub_pin_pulse:
    alpha 0.10
    block:
        easeout 1.4 alpha 0.30
        easein 1.4 alpha 0.10
        repeat

## The epilogue pin breathes more slowly than a new one. The place is still
## there, but it is not waiting for anything.
transform hub_epilogue_pulse:
    alpha 0.08
    block:
        easeout 2.0 alpha 0.22
        easein 2.0 alpha 0.08
        repeat

## The word on a live row blinks, so the eye finds it without reading every
## line. A soft dip rather than a hard flash: the hub is a quiet screen, and a
## list full of strobing labels would fight the map.
transform hub_new_blink:
    alpha 1.0
    block:
        pause 1.45
        easeout 0.18 alpha 0.30
        easein 0.26 alpha 1.0
        repeat


## --- THE MARK ---
##
## The mark beside a row. The pause is drawn as two solid blocks rather than
## typed, because no font in the project can be relied on to carry a pause
## glyph and a missing one prints as an empty box. A closed-today mark uses the
## DejaVu multiplication sign instead, which is available in that font.

screen hub_mark(state):

    fixed:
        xsize gui.scale(54)
        ysize gui.scale(24)

        if state == "ready":
            text "( ! )" style "hub_mark_text" color gui.accent_color xalign 0.5 yalign 0.5
        elif state == "epilogue":
            add Transform(Solid(hub_bar_color(state)), xysize=(gui.scale(8), gui.scale(8)), rotate=45) xalign 0.5 yalign 0.5
        elif state == "closed_today":
            text "×":
                style "hub_mark_text"
                font "DejaVuSans.ttf"
                color hub_bar_color(state)
                xalign 0.5
                yalign 0.5
        else:
            hbox:
                xalign 0.5
                yalign 0.5
                spacing gui.scale(5)

                add Solid(hub_bar_color(state)) xysize (gui.scale(3), gui.scale(18))
                add Solid(hub_bar_color(state)) xysize (gui.scale(3), gui.scale(18))


## --- THE HUB ---
##
## The free-afternoon screen puts the list on the left and the map on the
## right, so the player reads the destinations in words first and sees the city
## beside them. Every destination the player could go to is a pin on the map,
## coloured by what it can do today; the list spells the same thing out, because
## a map should never be the only way to read a menu. Only a ready pin or row
## can be picked.
##
## `places` is which rows to show, and in what order. Leave it out and every
## destination the hub currently offers is listed. `heading` and `blurb` are
## the two lines at the top, so the same screen can open after school, at
## night, or on a day off without a second copy of it existing.
##
## The screen returns the id of the row that was picked (e.g. "sim"), or None
## if the player chose to leave the day as it is.

## Where each destination sits on the free-afternoon map. The map is a stylised
## Tokyo, not a real one: the pins are spread so nothing overlaps and the
## colours carry the meaning. Coordinates are normalised to the map panel, so
## the same table survives any future resize.
define hub_map_positions = {
    "hana":          (0.13, 0.15),
    "library":       (0.29, 0.10),
    "sim":           (0.46, 0.17),
    "ueno":          (0.64, 0.10),
    "fortune":       (0.84, 0.16),
    "shimokitazawa": (0.14, 0.36),
    "orson":         (0.33, 0.40),
    "chef":          (0.55, 0.33),
    "aya":           (0.79, 0.39),
    "harajuku":      (0.09, 0.56),
    "omotesando":    (0.25, 0.60),
    "shibuya":       (0.41, 0.53),
    "karaoke":       (0.57, 0.58),
    "night_market":  (0.72, 0.51),
    "tanaka":        (0.90, 0.59),
    "message_hikari": (0.10, 0.77),
    "river":         (0.30, 0.75),
    "combini":       (0.45, 0.79),
    "odaiba":        (0.66, 0.74),
    "walk_alone":    (0.29, 0.91),
    "home":          (0.10, 0.91),
    "yokohama":      (0.78, 0.90),
}

## The city blocks under the pins. Each entry is (x, y, width, height, colour)
## in map-panel pixels. Kept quiet so the pins do the talking.
define hub_map_blocks = [
    # North
    (10, 8, 54, 22, "#12241d"),
    (74, 10, 46, 18, "#101f26"),
    (130, 6, 58, 24, "#101f26"),
    (198, 10, 50, 18, "#101f26"),
    (258, 6, 56, 24, "#101f26"),
    # Upper middle
    (12, 40, 48, 18, "#101f26"),
    (70, 36, 58, 24, "#101f26"),
    (138, 42, 44, 16, "#101f26"),
    (192, 36, 54, 24, "#101f26"),
    (256, 42, 56, 16, "#101f26"),
    # Middle
    (12, 72, 46, 18, "#101f26"),
    (68, 76, 54, 14, "#101f26"),
    (132, 70, 58, 22, "#101f26"),
    (200, 76, 48, 14, "#101f26"),
    (258, 70, 54, 22, "#101f26"),
    # Lower middle
    (12, 104, 50, 18, "#101f26"),
    (72, 108, 46, 14, "#101f26"),
    (128, 102, 62, 22, "#101f26"),
    (200, 108, 46, 14, "#101f26"),
    (256, 102, 56, 22, "#101f26"),
    # South
    (0, 164, 48, 24, "#0e222b"),
    (58, 168, 48, 20, "#101f26"),
    (116, 162, 58, 26, "#101f26"),
    (184, 168, 48, 20, "#101f26"),
    (242, 162, 52, 26, "#101f26"),
    (304, 168, 20, 20, "#0e222b"),
]


screen hub_map_pin(place, hovered=None, selected=None):
    $ place_state = destination_state(place)
    $ pin_nx, pin_ny = hub_map_positions[place]
    $ pin_x = int(pin_nx * gui.scale(324)) - gui.scale(10)
    $ pin_y = int(pin_ny * gui.scale(188)) - gui.scale(12)
    $ pin_color = hub_pin_color(place_state)
    $ is_ready = place_state in ("ready", "epilogue")
    $ pin_halo = "#f0d3a6" if place_state == "ready" else "#e8dcc4"

    button:
        xpos pin_x
        ypos pin_y
        xysize (gui.scale(20), gui.scale(24))
        background None
        hover_background None
        tooltip place
        action (SetScreenVariable("selected_place", place) if is_ready else NullAction())
        at hub_pin_hover

        fixed:
            xysize (gui.scale(20), gui.scale(24))

            # The glow breathes under a ready pin, so the map has a heartbeat
            # without any of the closed places moving. An epilogue pin breathes
            # more slowly: the place is still there, but it is not waiting.
            if place_state == "ready":
                add Transform(Solid("#c8a06a"), xysize=(gui.scale(13), gui.scale(13)), rotate=45) xalign 0.5 ypos 0 at hub_pin_pulse
            elif place_state == "epilogue":
                add Transform(Solid("#b8a382"), xysize=(gui.scale(13), gui.scale(13)), rotate=45) xalign 0.5 ypos 0 at hub_epilogue_pulse

            # A soft halo when either the pin or its row is under the cursor.
            if hovered == place:
                add Transform(Solid(pin_halo), xysize=(gui.scale(13), gui.scale(13)), rotate=45, alpha=0.22) xalign 0.5 ypos 0

            add Transform(Solid(pin_color), xysize=(gui.scale(8), gui.scale(8)), rotate=45) xalign 0.5 ypos gui.scale(2)
            add Solid(pin_color) xysize (gui.scale(1), gui.scale(6)) xalign 0.5 ypos gui.scale(10)
            add Solid(pin_color) xysize (gui.scale(3), gui.scale(1)) xalign 0.5 ypos gui.scale(16)


screen hub_row(place, hovered=None, selected=None):
    $ place_state = destination_state(place)
    $ place_name = destination_names.get(place, place)
    $ place_short = hub_state_short(place_state, place)
    $ is_ready = place_state in ("ready", "epilogue")
    $ is_hovered = hovered == place
    $ row_motion = hub_row_hover if is_ready else hub_row_still
    $ status_motion = hub_new_blink if place_state == "ready" else hub_row_still
    $ status_hover = "#e4bd87" if place_state == "ready" else ("#e8dcc4" if place_state == "epilogue" else hub_status_color(place_state))

    button:
        action (SetScreenVariable("selected_place", place) if is_ready else NullAction())
        background None
        hover_background None
        padding (0, 0)
        xysize (gui.scale(302), gui.scale(23))
        tooltip place
        at row_motion

        fixed:
            xysize (gui.scale(302), gui.scale(23))

            if selected == place:
                add Solid("#c8a06a18")

            if is_hovered:
                add Solid("#ffffff08")

            add Solid("#26231e") xysize (gui.scale(302), gui.scale(1)) ypos gui.scale(22)

            add Solid(hub_pin_color(place_state)) xysize (gui.scale(2), gui.scale(13)) xpos 0 yalign 0.5
            add Solid(hub_pin_color(place_state)) xysize (gui.scale(5), gui.scale(5)) xpos gui.scale(10) yalign 0.5

            text place_name:
                style "hub_row_name"
                color hub_state_color(place_state)
                hover_color ("#f5eee2" if is_ready else hub_state_color(place_state))
                xpos gui.scale(22)
                yalign 0.5

            text place_short:
                style "hub_row_status"
                color hub_status_color(place_state)
                hover_color status_hover
                xalign 1.0
                xoffset gui.scale(-8)
                yalign 0.5
                at status_motion


screen location_hub(places=None, heading="Free Afternoon", blurb="Choose one destination for this afternoon."):
    modal True
    zorder notice_window_zorder
    default selected_place = None
    key "K_RETURN" action If(selected_place is not None, Return(selected_place), NullAction())
    $ hub_places = places if places is not None else hub_destination_order()
    $ hub_people = [p for p in hub_places if p not in city_row_order]
    $ hub_city = [p for p in hub_places if p in city_row_order]

    # The tooltip is the destination id, not a sentence. The parent turns it
    # into the map header and the hover strip, and the rows and pins use it to
    # light each other up.
    $ hub_tip_raw = GetTooltip()
    $ hub_tip_place = hub_tip_raw if hub_tip_raw in destination_names else None
    $ hub_tip_name = destination_names.get(hub_tip_place) if hub_tip_place else None
    $ hub_tip_state = destination_state(hub_tip_place) if hub_tip_place else None
    $ hub_tip_status = destination_state_label(hub_tip_place, hub_tip_state) if hub_tip_place else None
    $ hub_tip_color = ("#e4bd87" if hub_tip_state == "ready" else ("#d6c7ae" if hub_tip_state == "epilogue" else "#b9b1a5")) if hub_tip_state else "#5c6d77"

    add Solid("#000000") at notice_backdrop_in
    use standalone_notice_window(heading, "DESTINATIONS  ・  " + story_date_category(), notice_window_in):
        fixed:
            xysize (gui.scale(648), gui.scale(230))

            ## --- THE LIST ---
            fixed:
                xysize (gui.scale(306), gui.scale(230))
                at hub_left_in

                text blurb:
                    style "guide_body"
                    xsize gui.scale(306)
                    size gui.scale(13)
                    line_spacing gui.scale(2)
                    color "#cfc8bd"

                text "PEOPLE":
                    style "guide_meta"
                    color "#c8a06a"
                    kerning gui.scale(2)
                    ypos gui.scale(38)

                add Solid("#2a2620") ypos gui.scale(54) xysize (gui.scale(306), gui.scale(1))

                viewport:
                    ypos gui.scale(62)
                    xysize (gui.scale(306), gui.scale(168))
                    mousewheel True
                    draggable True

                    vbox:
                        spacing gui.scale(1)
                        for place in hub_people:
                            use hub_row(place, hub_tip_place, selected_place)
                        if hub_city:
                            null height gui.scale(7)
                            text "THE CITY":
                                style "guide_meta"
                                color "#c8a06a"
                                kerning gui.scale(2)
                            add Solid("#2a2620") xysize (gui.scale(302), gui.scale(1))
                            null height gui.scale(3)
                            for place in hub_city:
                                use hub_row(place, hub_tip_place, selected_place)

            add Solid("#2a2620") xpos gui.scale(315) ypos 0 xysize (gui.scale(1), gui.scale(230))

            ## --- THE MAP ---
            fixed:
                xpos gui.scale(324)
                xysize (gui.scale(324), gui.scale(230))
                at hub_right_in

                text "THE MAP":
                    style "guide_meta"
                    color "#c8a06a"
                    kerning gui.scale(2)
                    xpos gui.scale(10)

                text (hub_tip_name or "HOVER A PIN"):
                    size gui.scale(10)
                    color hub_tip_color
                    kerning gui.scale(1)
                    outlines []
                    xalign 1.0
                    xoffset gui.scale(-10)
                    ypos gui.scale(1)
                    at hub_tip_in

                add Solid("#2a3a42") ypos gui.scale(18) xysize (gui.scale(324), gui.scale(1))

                fixed:
                    ypos gui.scale(24)
                    xysize (gui.scale(324), gui.scale(188))

                    add Solid("#22323a") xysize (gui.scale(324), gui.scale(188))
                    add Solid("#0b1419") xpos gui.scale(1) ypos gui.scale(1) xysize (gui.scale(322), gui.scale(186))

                    for bx, by, bw, bh, bcolor in hub_map_blocks:
                        add Solid(bcolor) xpos gui.scale(bx) ypos gui.scale(by) xysize (gui.scale(bw), gui.scale(bh))

                    for rx in (66, 126, 190, 250, 302):
                        add Solid("#152831") xpos gui.scale(rx) ypos gui.scale(1) xysize (gui.scale(1), gui.scale(186))
                    for ry in (34, 66, 98, 130, 158):
                        add Solid("#152831") xpos gui.scale(1) ypos gui.scale(ry) xysize (gui.scale(322), gui.scale(1))

                    # Keep the frame crisp where the edge blocks meet it.
                    add Solid("#22323a") xpos 0 ypos 0 xysize (gui.scale(324), gui.scale(1))
                    add Solid("#22323a") xpos 0 ypos gui.scale(187) xysize (gui.scale(324), gui.scale(1))
                    add Solid("#22323a") xpos 0 ypos 0 xysize (gui.scale(1), gui.scale(188))
                    add Solid("#22323a") xpos gui.scale(323) ypos 0 xysize (gui.scale(1), gui.scale(188))

                    for place in hub_places:
                        if place in hub_map_positions:
                            use hub_map_pin(place, hub_tip_place, selected_place)

                add Solid("#2a3a42") ypos gui.scale(212) xysize (gui.scale(324), gui.scale(1))

                fixed:
                    ypos gui.scale(213)
                    xysize (gui.scale(324), gui.scale(17))

                    if hub_tip_place:
                        text (hub_tip_name + "  ・  " + hub_tip_status):
                            size gui.scale(9)
                            color hub_tip_color
                            xpos gui.scale(10)
                            yalign 0.5
                            layout "nobreak"
                            outlines []
                            at hub_tip_in
                    else:
                        hbox:
                            spacing gui.scale(10)
                            xpos gui.scale(10)
                            yalign 0.5
                            for state, label in hub_legend_items():
                                hbox:
                                    spacing gui.scale(3)
                                    add Solid(hub_pin_color(state)) xysize (gui.scale(6), gui.scale(6)) yalign 0.5
                                    text label:
                                        style "hub_legend_text"
                                        yalign 0.5

        use standalone_notice_footer("Select a destination, then travel.", "Travel Here", Return(selected_place), selected_place is not None)
