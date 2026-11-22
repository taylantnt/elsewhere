📌 Location & Character System Overview

Hey team! Here’s how the location-based character progression will work in our game:
    •    🎯 Every major location has a “Main Character.”
    •    Example: Maid Café → the Maid character (Aya)
    •    Example: Bar → Orson (the Bar Master)
    •    🗨️ Each time the player visits that location, they interact with the main character.
    •    Over time, the relationship grows deeper.
    •    The player learns more about the character’s personality, struggles, and backstory.
    •    🔄 Each location has 7 numbered interactions.
    •    These are separate encounters across multiple visits.
    •    Each one adds new layers to the relationship and story.
    •    🎭 After the 7th interaction, the storyline for that location concludes.
    •    The location stays visitable, but the main character is gone.
    •    An 8th epilogue visit replays the same closing scene every time.

✨ Example outcomes:
    •    The Maid character, Aya could quit her job to pursue her dreams.
    •    Orson, the Master of the bar, might close down his bar.

This gives each location its own “mini-arc,” while also tying into the larger narrative.

---

## The Two Exceptions (as built, 2026-11-12)

The seven numbered visits are the spine, not the whole skeleton. Every one of the
five confidants also has a repeatable eighth epilogue at the same place.

### The Fortune Teller — seven visits, and she reads the script

She is a **confidant with a twist**: not in `confidant_order` (she is met on
Day 13, after the introduction gate opens, so requiring her would deadlock
revisits), but otherwise treated like the five — `confidant_visits["fortune"]`,
`confidant_visit_totals["fortune"] = 8`, epilogue state at visit 7, WIRE
contact from Day 13. Her row opens after the Day 13 reading
(`fortune_arc_started`).

Visit 1 is the Day 13 scene itself. Visits 2–7 and the repeatable corner
epilogue live in `game/confidant_visits/fortune.rpy`. Her premise is that she
reads the "pages" — the script of his life — and comments on choices before
they are made: the ghost question on the midterm, the blank page that is his
to write, and the corner where she stays after the table folds.

### Murakami — the elective that never ends

She is a **confidant with no ending**: the Japanese elective teacher from
Day 10, met during the fair. Like the Fortune Teller she stays out of
`confidant_order`, but she is a full confidant otherwise —
`confidant_visits["murakami"]`, her own file
`game/confidant_visits/murakami.rpy`, her own hub row "Japanese Elective"
under PEOPLE, and a WIRE contact whose meter counts lessons rather than
visits.

**She appears after school from the Day 10 meeting.** `hub_destination_order()`
checks `"murakami" in wire_unlocked`, not enrollment, so the row is present from
the fair onward and also shows in the phone calendar's WHO'S OPEN list.

**Enrollment is still the player's choice, not the script's.** Day 10 is only the
meeting: Murakami gives him the course sheet and homework, and the decision
to actually learn is deferred to a solo beat on the night of Day 12. Choosing
enroll sets `murakami_enrolled`, which now drives the WIRE meter and the
enrollment dialogue rather than visibility. Declining is not a dead end — the
embedded classes on Days 14–17 still happen (informal auditing; she teaches
whoever shows up), and `murakami_daily_ping` re-offers enrollment on Day 14 and
weekly after, then sends office-hours reminders on every third weekday once he
is in. Her six misfiled common-day lecture dicts were removed; the professor
teaches the daily class, Murakami teaches her own visits.

The arc is **comedy, not closure**: ten written visits set in the small
second-floor classroom with a recurring cast of exchange students (Wei the
kanji reader, Priya, Oliver, Prakash, Saman), each visit a different flavor of
"the whole class misunderstands the same thing." After visit 10 the
dispatcher falls through to `murakami_lesson_repeat`, a rotating office-hours
scene, and `destination_state()` exempts her from the closed/paused/cap
checks entirely — the room stays open forever, which is the point.

The four embedded elective lessons on Days 10–17 (`murakami_lessons` 1–4)
still live in the special day files; the hub arc counts separately in
`confidant_visits`.

### Tanaka — the combini job

Tanaka is a **job contact**, not a confidant. His row is `Convenience Store`,
listed under the hub's **JOBS** section (separate from THE CITY), and it appears
only after `combini_job_unlocked` is set by the first counter scene — which
Day 8 scripts as a linear afternoon, so the job is story-earned rather than
hub-optional. A shift pays ¥4,800 (¥1,200 × 4 hours), consumes the
afternoon, and advances `tanaka_story` (0–7). The row never closes, because the
store does not.

The seven teaching shifts live in `game/job_combini/`, one file per shift:

| Visit | File | The lesson |
| :--- | :--- | :--- |
| 1 | `tanaka_visit_01.rpy` | The register and the script; irasshaimase is not an apology |
| 2 | `tanaka_visit_02.rpy` | The floor: new stock, eye level, the height of a child's hand |
| 3 | `tanaka_visit_03.rpy` | The hot case: the grill, brown, and the exact second |
| 4 | `tanaka_visit_04.rpy` | The fryer: timers, disposal, and quality as a schedule |
| 5 | `tanaka_visit_05.rpy` | Just enough: the order, and not fearing the sold-out sleeve |
| 6 | `tanaka_visit_06.rpy` | The tencho reveal: the man ordering him around owns the store |
| 7 | `tanaka_visit_07.rpy` | Closing: the last judgment call, and what a store says to everyone |

After visit 7, `tanaka_visit_repeat` in `tanaka_job.rpy` carries the row: same
four hours, same wage, no new lesson. Work does not end; it stops teaching.

## The City Rows

These are **not** confidant arcs. They have no visit counts, no caps, and no
closures. They exist so a paused or closed afternoon still has somewhere to go.
Each one carries one small cultural moment and a choice that does not have to
pay.

| Row | Location | Cultural moment |
| :--- | :--- | :--- |
| `library` | Campus Library | Study as a room that keeps its promises |
| `river` | Riverbank | The one thing in the city not in a hurry |
| `harajuku` | Harajuku: Takeshita Street | The crowd as a performance |
| `karaoke` | Karaoke Box | Singing badly in a room built for people who sing well |
| `night_market` | Night Food Stalls | Eating standing up |
| `combini` | Combini | The convenience store as a machine for living |
| `odaiba` | Odaiba | The future that already happened; the statue blinks |
| `yokohama` | Yokohama Chinatown | The other foreigner |
| `ueno` | Ueno Park | Hanami, blue tarps, and the sitting being the point |
| `shibuya` | Shibuya Crossing | A thousand people walking into each other and nobody touching |
| `shimokitazawa` | Shimokitazawa | A neighborhood that stopped performing |
| `omotesando` | Omotesando / Meiji Shrine | The city gets quiet at the gate |
| `tanaka` | Combini: Night Shift | Work, the script, and the wage (job row) |

The first six existed before the audit. The last seven are the 2026-11-12
expansion (Odaiba, Yokohama, Ueno, Shibuya, Shimokitazawa, Omotesando, and the
job row). All of them use `bg_or_placeholder()` until the art arrives.