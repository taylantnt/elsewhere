################################################################################
## CALENDAR AND LOCATION HOURS
################################################################################
##
## One clock for the whole story.
##
## `story_day` is the canonical date. Day 1 is the arrival, Wednesday, April 8,
## 2026. Every day label sets its absolute day at the top with `set_story_day()`
## rather than counting scene transitions, so a branch can never leave the
## calendar one day behind. The HUD and the phone calendar only read it.
##
## Location hours live here too, but they are separate from story progress. A
## place can be ready for its next visit and still be closed today. The hub in
## locations.rpy combines both answers through `destination_state()`.
##
## Scripted scenes are never blocked by opening hours. The first visit to each
## confidant is written into a specific day; the schedule only governs the
## free-afternoon hub after that.


## --- THE ANCHOR ---
##
## Keep the year out of the HUD. It exists so month lengths, leap years and
## weekdays are real; the story only ever says the weekday and the date.
define story_calendar_anchor_year = 2026
define story_calendar_anchor_month = 4
define story_calendar_anchor_day = 8

define story_weekday_names = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
]
define story_weekday_short = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
define story_month_names = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

## The story beats already attached to a date. A day is only described once it
## has been reached, so browsing ahead cannot spoil a later scene.
define story_calendar_events = {
    1: "Arrival in Tokyo",
    2: "First school day",
    3: "Second school day",
    4: "Library errand",
    5: "Hikari's practice quiz",
    6: "The haiku quiz",
}

## Weekly opening rules, Monday = 0 through Sunday = 6.
##
## `open_days` means the place is open only on those days; leave it out and
## `closed_days` names the exceptions instead. `hours` is the short line the
## phone calendar shows on an open day. `closed_note` is the reason the hub and
## the calendar give when the place is shut.
##
## Canon already in the script:
##   * Chef's WIRE note: "Closed Wednesdays."
##   * Sim's first text: "Next meeting is Thursday."
## Hana's reading room keeps campus hours; Aya's cafe and Orson's bar have no
## written closure, so they are open every day.
define destination_schedules = {
    "sim": {
        "open_days": (3,),
        "hours": "Thursdays",
        "closed_note": "Circle meets Thursdays.",
    },
    "chef": {
        "closed_days": (2,),
        "hours": "Open except Wednesdays",
        "closed_note": "Closed Wednesdays.",
    },
    "hana": {
        "open_days": (0, 1, 2, 3, 4, 5),
        "hours": "Monday to Saturday",
        "closed_note": "Closed Sundays.",
    },
}

## The day the story is currently on. Only day labels write this.
default story_day = 1

## Which day the phone calendar has selected. None means "today" while the
## current month is on screen, and the first of the month while browsing.
default phone_calendar_selected = None

## How many months the phone calendar is away from the current story month.
default phone_calendar_month_offset = 0


init python:
    import calendar as pycalendar
    import datetime

    # --- READING THE CLOCK ---------------------------------------------------

    def story_calendar_start_date():
        return datetime.date(
            story_calendar_anchor_year,
            story_calendar_anchor_month,
            story_calendar_anchor_day,
        )

    def story_calendar_date(day=None):
        """The real date for a story day. Day 1 is the anchor date."""
        if day is None:
            day = store.story_day
        return story_calendar_start_date() + datetime.timedelta(days=max(1, int(day)) - 1)

    def story_calendar_day_for_date(date_value):
        """Which story day a calendar date is. Zero or less is before arrival."""
        return (date_value - story_calendar_start_date()).days + 1

    def story_calendar_weekday(day=None):
        """Monday = 0 through Sunday = 6, matching datetime.date.weekday()."""
        return story_calendar_date(day).weekday()

    def story_weekday_name(day=None):
        return story_weekday_names[story_calendar_weekday(day)]

    def story_weekday_short_name(day=None):
        return story_weekday_short[story_calendar_weekday(day)]

    def story_week_number(day=None):
        if day is None:
            day = store.story_day
        return ((max(1, int(day)) - 1) // 7) + 1

    def calendar_date_label(date_value):
        return "%s, %s %d" % (
            story_weekday_names[date_value.weekday()],
            story_month_names[date_value.month - 1],
            date_value.day,
        )

    def story_date_label(day=None):
        return calendar_date_label(story_calendar_date(day))

    def story_date_category(day=None):
        """The compact, all-caps date used by the hub eyebrow."""
        if day is None:
            day = store.story_day
        date_value = story_calendar_date(day)
        return "%s · %s %d · DAY %d" % (
            story_weekday_names[date_value.weekday()].upper(),
            story_month_names[date_value.month - 1].upper(),
            date_value.day,
            int(day),
        )

    # --- WRITING THE CLOCK ---------------------------------------------------

    def set_story_day(day):
        """Pin the story to an absolute day. Safe to call again after rollback."""
        store.story_day = max(1, int(day))

    def advance_story_day(count=1):
        """Move forward from the current day. Use for new day labels."""
        store.story_day = max(1, int(store.story_day) + int(count))

    # --- OPENING HOURS -------------------------------------------------------

    def destination_is_open(place, weekday=None):
        if weekday is None:
            weekday = story_calendar_weekday()

        rule = destination_schedules.get(place)
        if not rule:
            return True

        open_days = rule.get("open_days")
        if open_days is not None:
            return weekday in open_days
        return weekday not in rule.get("closed_days", ())

    def destination_schedule_label(place):
        rule = destination_schedules.get(place)
        if not rule:
            return "Daily"
        return rule.get("hours", "Daily")

    def destination_schedule_note(place, weekday=None):
        if destination_is_open(place, weekday):
            return "Open today."
        rule = destination_schedules.get(place, {})
        return rule.get("closed_note", "Closed today.")

    # --- PHONE CALENDAR ------------------------------------------------------

    def phone_calendar_view_date():
        """The first of the month the calendar is currently showing."""
        today = story_calendar_date()
        month = today.month - 1 + int(store.phone_calendar_month_offset)
        year = today.year + month // 12
        month = month % 12 + 1
        return datetime.date(year, month, 1)

    def phone_calendar_shift_month(delta):
        store.phone_calendar_month_offset = int(store.phone_calendar_month_offset) + int(delta)
        store.phone_calendar_selected = None

    def phone_calendar_selected_date():
        raw = store.phone_calendar_selected
        if raw:
            try:
                return datetime.date.fromisoformat(raw)
            except (TypeError, ValueError):
                store.phone_calendar_selected = None

        view = phone_calendar_view_date()
        today = story_calendar_date()
        if view.year == today.year and view.month == today.month:
            return today
        return view

    def phone_calendar_month_weeks(view_date):
        """Six Monday-first weeks, including the days either side of the month."""
        weeks = pycalendar.Calendar(firstweekday=0).monthdatescalendar(
            view_date.year,
            view_date.month,
        )
        while len(weeks) < 6:
            last = weeks[-1][-1]
            weeks.append([
                last + datetime.timedelta(days=offset)
                for offset in range(1, 8)
            ])
        return weeks[:6]

    def phone_calendar_day_line(date_value):
        story_number = story_calendar_day_for_date(date_value)
        if story_number < 1:
            return "BEFORE ARRIVAL"
        if story_number == int(store.story_day):
            return "TODAY · DAY %d · WEEK %d" % (
                story_number,
                story_week_number(story_number),
            )
        return "DAY %d · WEEK %d" % (
            story_number,
            story_week_number(story_number),
        )

    def phone_calendar_event(date_value):
        story_number = story_calendar_day_for_date(date_value)
        if story_number < 1 or story_number > int(store.story_day):
            return None
        return story_calendar_events.get(story_number)

    def phone_calendar_has_event(date_value):
        return phone_calendar_event(date_value) is not None

    def phone_app_unlocked(app_id):
        # The contact-led phone content waits for the first connection, just
        # like the calendar. Maps share the first-connection gate in this build.
        if app_id in ("messages", "maps", "wire", "calendar"):
            return len(store.wire_unlocked) > 0
        return True


## --- THE DATE CHIP ---
##
## The top-left corner. It rides the same switches as the attribute HUD: off
## during the title and the opening notices, on as soon as he is standing in
## the airport, hidden behind standalone windows.

transform story_day_hud_appear:
    alpha 0.0
    linear 0.55 alpha 1.0

screen story_day_hud():
    zorder 90

    if show_attribute_hud and not main_menu and not standalone_window_active():
        frame:
            style "story_day_frame"
            at story_day_hud_appear

            vbox:
                spacing gui.scale(1)

                text story_date_label().upper():
                    style "story_day_date"

                text "DAY %d  ·  WEEK %d" % (story_day, story_week_number()):
                    style "story_day_meta"

style story_day_frame is empty:
    xpos gui.scale(28)
    ypos gui.scale(24)
    background Solid("#0e0d0ccc")
    padding (gui.scale(16), gui.scale(7), gui.scale(16), gui.scale(7))

style story_day_date is default:
    font "DejaVuSans.ttf"
    size gui.scale(17)
    bold True
    color "#f3eee5"
    kerning gui.scale(1)
    outlines []

style story_day_meta is default:
    font "DejaVuSans.ttf"
    size gui.scale(9)
    bold True
    color "#c8a06a"
    kerning gui.scale(1)
    outlines []


## --- THE PHONE CALENDAR -------------------------------------------------------
##
## A month grid, the selected day's story beat, and the five confidant places
## with their hours. Tapping a date changes the selected day; the arrows move
## between months. The current day is always one tap away because opening the
## app starts on the current month.
##
## The calendar is locked until the first contact lands in WIRE, the same gate
## the phone uses for the first connection. Before that it shows the same kind
## of empty/unlocked message the other contact-led apps use.

screen phone_app_calendar_contents_locked():
    vbox:
        xalign 0.5
        yalign 0.5
        spacing gui.scale(10)

        text "NOT UNLOCKED YET.":
            xalign 0.5
            size gui.scale(15)
            bold True
            color "#dce4e8"
            outlines []

        text "Your first connection opens the calendar.":
            xalign 0.5
            textalign 0.5
            size gui.scale(13)
            color "#83909a"
            outlines []


screen phone_app_calendar_contents():
    $ calendar_view = phone_calendar_view_date()
    $ calendar_selected = phone_calendar_selected_date()
    $ calendar_weeks = phone_calendar_month_weeks(calendar_view)
    $ calendar_today = story_calendar_date()
    $ calendar_weekday = calendar_selected.weekday()
    $ calendar_event = phone_calendar_event(calendar_selected)

    fixed:
        xysize (gui.scale(menu_phone_content_w), gui.scale(474))

        vbox:
            xalign 0.5
            spacing gui.scale(4)

            fixed:
                xfill True
                ysize gui.scale(22)

                textbutton "‹":
                    style "phone_small_button"
                    xalign 0.0
                    yalign 0.5
                    text_font "DejaVuSans.ttf"
                    text_size gui.scale(18)
                    padding (gui.scale(6), 0)
                    action Function(phone_calendar_shift_month, -1)

                text "%s %d" % (story_month_names[calendar_view.month - 1].upper(), calendar_view.year):
                    xalign 0.5
                    yalign 0.5
                    size gui.scale(14)
                    bold True
                    kerning gui.scale(1)
                    color "#f1eee7"
                    outlines []

                textbutton "›":
                    style "phone_small_button"
                    xalign 1.0
                    yalign 0.5
                    text_font "DejaVuSans.ttf"
                    text_size gui.scale(18)
                    padding (gui.scale(6), 0)
                    action Function(phone_calendar_shift_month, 1)

            hbox:
                xalign 0.5
                spacing gui.scale(1)

                for weekday_label in story_weekday_short:
                    fixed:
                        xysize (gui.scale(31), gui.scale(13))
                        text weekday_label:
                            xalign 0.5
                            yalign 0.5
                            size gui.scale(8)
                            kerning gui.scale(0.5)
                            color "#71808b"
                            outlines []

            vbox:
                xalign 0.5
                spacing gui.scale(1)

                for calendar_week in calendar_weeks:
                    hbox:
                        spacing gui.scale(1)

                        for calendar_date in calendar_week:
                            $ calendar_is_today = calendar_date == calendar_today
                            $ calendar_is_selected = calendar_date == calendar_selected
                            $ calendar_is_other_month = calendar_date.month != calendar_view.month
                            $ calendar_has_event = phone_calendar_has_event(calendar_date)

                            button:
                                xysize (gui.scale(31), gui.scale(25))
                                background (
                                    Solid("#c8a06a") if calendar_is_selected else
                                    Solid("#2b3a3f") if calendar_is_today else
                                    None
                                )
                                hover_background Solid("#26343a")
                                action SetVariable("phone_calendar_selected", calendar_date.isoformat())

                                fixed:
                                    xysize (gui.scale(31), gui.scale(25))

                                    text str(calendar_date.day):
                                        xalign 0.5
                                        yalign 0.5
                                        size gui.scale(11)
                                        color (
                                            "#16130f" if calendar_is_selected else
                                            "#f3eee5" if calendar_is_today else
                                            "#5f6a70" if calendar_is_other_month else
                                            "#c3ccd5"
                                        )
                                        outlines []

                                    if calendar_has_event and not calendar_is_selected:
                                        add Solid("#c8a06a"):
                                            xalign 0.5
                                            ypos gui.scale(21)
                                            xysize (gui.scale(3), gui.scale(3))

            add Solid("#243139") xysize (gui.scale(menu_phone_content_w), 1)

            text calendar_date_label(calendar_selected):
                size gui.scale(13)
                color "#f1eee7"
                outlines []

            text phone_calendar_day_line(calendar_selected):
                size gui.scale(9)
                bold True
                kerning gui.scale(1)
                color "#c8a06a"
                outlines []

            if calendar_event:
                text calendar_event:
                    size gui.scale(11)
                    color "#aab7bf"
                    outlines []

            text "WHO'S OPEN":
                size gui.scale(9)
                bold True
                kerning gui.scale(2)
                color "#71808b"
                outlines []

            for place in confidant_order:
                $ place_open = destination_is_open(place, calendar_weekday)
                $ place_note = destination_schedule_note(place, calendar_weekday)

                fixed:
                    xfill True
                    ysize gui.scale(24)

                    text destination_names.get(place, place):
                        xpos 0
                        ypos 0
                        size gui.scale(11)
                        color ("#dce4e8" if place_open else "#7b858c")
                        outlines []

                    text ("OPEN" if place_open else "CLOSED"):
                        xalign 1.0
                        ypos 0
                        size gui.scale(9)
                        bold True
                        kerning gui.scale(1)
                        color ("#82d7bf" if place_open else "#d98b7a")
                        outlines []

                    text (destination_schedule_label(place) if place_open else place_note):
                        xpos 0
                        ypos gui.scale(12)
                        size gui.scale(9)
                        color "#71808b"
                        outlines []

            text "Some doors keep their own hours.":
                size gui.scale(9)
                italic True
                color "#64727e"
                outlines []
