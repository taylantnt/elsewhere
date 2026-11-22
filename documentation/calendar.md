# Calendar, Dates, and Location Hours
**Document type:** As-implemented reference
**Covers:** `game/calendar.rpy`, the date chip, the phone Calendar app, and weekly opening rules
**Status:** Built; dates are canonical from the airport through Tuesday, Day 21

> This is the document to check before writing a line that names a day or a date.
> The script does not infer dates from scene order. Each day label pins the
> absolute day, so branches and rollbacks cannot drift.

---

## 1. The Anchor

| Story day | Date | Day label |
|-----------|------|-----------|
| Day 1 | **Wednesday, April 8, 2026** | `airport_arrival` |
| Day 2 | Thursday, April 9 | `morning_call` |
| Day 3 | Friday, April 10 | `second_morning` |
| Day 4 | Saturday, April 11 | `saturday_off` |
| Day 5 | Sunday, April 12 | `sunday_morning` |
| Day 6 | Monday, April 13 | `monday_morning` |
| Day 7 | Tuesday, April 14 | `tuesday_morning` |
| Day 8 | Wednesday, April 15 | `wednesday_morning` |
| Day 9 | Thursday, April 16 | `thursday_morning` |
| Day 10 | Friday, April 17 | `friday_morning` |
| Day 11 | Saturday, April 18 | `saturday_recovery` |
| Day 12 | Sunday, April 19 | `sunday_practice` |
| Day 13 | Monday, April 20 | `monday_asakusa` |
| Day 14 | Tuesday, April 21 | `tuesday_week_two` |
| Day 15 | Wednesday, April 22 | `wednesday_preview` |
| Day 16 | Thursday, April 23 | `thursday_mitate` |
| Day 17 | Friday, April 24 | `friday_sounds` |
| Day 18 | Saturday, April 25 | `saturday_matsuri` |
| Day 19 | Sunday, April 26 | `sunday_mock` |
| Day 20 | Monday, April 27 | `monday_midterm` |
| Day 21 | Tuesday, April 28 | `tuesday_results` |

The year is an internal anchor only. The HUD and the phone Calendar show the
weekday and month/day; `2026` exists so month lengths and weekdays are real.
The anchor is set in `game/calendar.rpy`:

```renpy
define story_calendar_anchor_year = 2026
define story_calendar_anchor_month = 4
define story_calendar_anchor_day = 8
```

Changing those three values moves every displayed date without touching the
story labels.

---

## 2. What the Player Sees

- **Date chip (top left).** `screen story_day_hud` draws the full weekday and
  date, plus `DAY N · WEEK N`. It appears when `show_attribute_hud` becomes true
  at the airport, and hides during standalone notice windows.
- **Phone Calendar.** The phone launcher has a Calendar tile. It opens on the
  current month, highlights today, marks days that have a reached story beat,
  and lets the player browse months. Tapping a date shows:
  - the full date and `DAY N · WEEK N`;
  - the story beat for that day, if it has already happened;
  - which five confidant places are open that weekday, with their hours.
- **The calendar unlocks with the first connection.** The tile is not sensitive
  until `wire_unlocked` has its first entry, the same gate that opens the WIRE
  app. Before that, the Calendar screen shows `NOT UNLOCKED YET.` with
  `Your first connection opens the calendar.` This mirrors the empty/contact-led
  wording the other phone apps use before they have something to show.
- **The first-connection gate now covers the contact-led apps.** Messages,
  Maps, WIRE, and Calendar all wait for the first WIRE contact. Before the first
  confidant, those tiles are insensitive with grayed-out icons; after the first
  confidant, they become interactive. Maps are treated as contact-led in this
  build and open after the first connection.
- **The app icons are consistent.** Every phone app icon is the same rounded-square
  design with a centered white glyph; the contact-led ones go gray when locked.
- **The HUD date chip** is on screen from the airport, before any confidant has
  been met. The HUD is always on; the contact-led phone content waits for the
  first connection.
- **Location hub.** `screen location_hub` uses the same date in its eyebrow and
  shows `Closed today` style rows for places that keep weekly hours. A closed
  row cannot be picked.

The HUD is read-only. The story is the only thing that writes `story_day`.

---

## 3. Advancing the Day

At the top of every new day label, call one of these:

```renpy
$ set_story_day(7)          # absolute: safest for a scripted day
$ advance_story_day()       # one day forward from wherever the story is
```

Use `set_story_day()` for the current linear story. `advance_story_day()` is
convenient for a future repeating loop, but it must only be called once per day
transition. Because Ren'Py rollback restores `story_day` with the rest of the
store, either call is safe to replay after a rollback.

A new day label should also add its beat to `story_calendar_events` in
`game/calendar.rpy`:

```renpy
define story_calendar_events = {
    1: "Arrival in Tokyo",
    2: "First school day",
    # ...
    7: "The first hub afternoon",
}
```

An event only appears once the player has reached that day, so adding a future
entry does not spoil it.

After `set_story_day()` (or the advance), every current day label also calls
`call day_transition` before its first scene beat, so the calendar move is
performed by the full-screen day progression (`game/day_transition.rpy`) rather
than by a silent counter bump. The transition is modal and holds until the player
presses a key or clicks, so the day label's first scene beat only runs once the
card has been dismissed.

---

## 4. Weekly Opening Rules

`destination_schedules` in `game/calendar.rpy` is the single source of truth.
Days are `Monday = 0` through `Sunday = 6`.

| Destination id | Place | Rule | Why |
|----------------|-------|------|-----|
| `sim` | Photography Club | Open **Thursdays only** | Sim's first text: "Thursday. Bring the camera." |
| `chef` | Ramen Shop | Closed **Wednesdays** | Chef's WIRE note: "Closed Wednesdays." |
| `hana` | Reading Club | Open **Monday to Saturday** | Campus reading room; closed Sunday. |
| `aya` | Maid Cafe | Open daily | No written closure. |
| `orson` | Lupin's Den | Open daily | No written closure. |
| `walk_hikari` | Walk home with Hikari | Always available | Not a scheduled place; plays the next river run when one is waiting, the first run if it was skipped, otherwise the ordinary walk. |
| `walk_alone` | Walk home alone | Always available | Not a scheduled place. |
| `fortune` | Asakusa: The Fortune Teller | Always available once `fortune_arc_started` | A seven-visit confidant kept out of `confidant_order` so she cannot gate the other arcs; visit 1 is the Day 13 reading, visits 2–7 and the corner epilogue live in `game/confidant_visits/fortune.rpy`. |
| `tanaka` | Convenience Store | Always available once `combini_job_unlocked` | A job row under the hub's JOBS section, not a confidant; shifts are tracked by `tanaka_story`. |
| city rows | Library, river, Harajuku, karaoke, night market, combini, Odaiba, Yokohama, Ueno, Shibuya, Shimokitazawa, Omotesando | No entry, so open every day | The city does not close. |

Each entry has three fields:

```renpy
"chef": {
    "closed_days": (2,),                       # Wednesday
    "hours": "Open except Wednesdays",         # shown on an open day
    "closed_note": "Closed Wednesdays.",       # shown on a closed day
},
```

Use `open_days` instead of `closed_days` for a place that only opens on named
days. If a place has no entry, it is open every day.

**Scripted scenes ignore the schedule.** The first visit to every confidant is
written into a specific day and must be allowed to happen even if the hub would
consider that place closed. The schedule only governs the free-afternoon hub
(`free_afternoon` / `location_hub`) after the introductions.

`destination_state()` in `game/locations.rpy` checks hours before the visit
cap, so a ready place can still be `closed_today`. The five confidants' eighth
epilogue is checked before hours and before the cap, so a finished arc stays
visitable on any day. Story completion (`closed`) wins over hours.

---

## 5. Existing Saves

`story_day` defaults to 1. A save made before this system existed will show the
arrival date until its next day label runs. This is a development-build
limitation, not a story rule: the current day is pinned at the top of each day
label, so the next transition corrects it.
