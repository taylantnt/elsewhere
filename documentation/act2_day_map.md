# Act 2 / Act 3 Day Map (Days 8-69)

How the long middle and the slow-burn glitch are paced. Two kinds of day file
live in `game/days/`:

- **`special_day_NN_slug.rpy`**: a hand-written set piece. One file per day,
  its own label, ends with `jump act2_day_router`.
- **`common_day_NN`** (all inside `common_days.rpy`): a routine day. The label
  pins `story_day`, calls `common_day_core`, and the skeleton in that file
  runs morning, phone chat, kitchen, Hikari's lesson, collapsed commute,
  lecture (weekdays) or `off` beat (weekends), the hub, dinner, and night.

`act2_day_router` in `common_days.rpy` is the single source of truth for day
order. Every day ends by jumping to it; it reads `story_day` and jumps to the
next day's label. Finishing Day 69 starts the written investigation,
`special_day_70_the_table`, which runs through Day 83 in
`act3_investigation.rpy`. Day 82 hands off to `act4_bridge`, which compresses
only Days 84-89 and plays Day 90 before `end_of_build`.

## The pace

Roughly **3 special days per 2 common days** across Days 22-45. Specials are reserved for beats
that cannot survive the routine frame: holidays, incidents, confessions,
season turns, and Act 3 seeds. Commons carry the simulation-horror texture:
the world keeps working while something underneath it is not quite right.

| Days | Kind | Notes |
|---|---|---|
| 8-21 | special (14) | Already written: frog through results |
| 22 | special | `see_me`: professor follow-up after results |
| 23 | common | Umbrellas and distance |
| 24 | special | `early_may`: the week before Golden Week |
| 25 | common | The sorting (Saturday, no lecture) |
| 26 | special | `nakameguro`: Sunday of Golden Week, Hikari takes him to the canal for the last blossoms (nochizakura) |
| 27-29 | special x3 | Rest of Golden Week: `gw_trip`, `gw_evening`, `school_returns` |
| 30-32 | common | The slurp, the queue, the card |
| 33 | special | `absence`: a confidant arc closes; hub state changes |
| 34-40 | common | Machine, coffee shop, gap, curtain, last train, cloth, song |
| 41 | special | `leak`: first real wrongness, Act 3 seed: a repeating child, a shop that forgets it closed, and a twelfth door Hikari cannot see |
| 42-45 | common | Water, paw, button, lost thing |
| 46-50 | special x5 | Late Act 2: `tsukiji`, `kamakura`, `sento`, `hydrangea`, `fireflies`. The last warm days. Hub open. One glitch seed planted on Day 50 (the firefly walk). |
| 51-53 | special x3 | **Act 3 Incident.** `the_line`, `same_face`, `fragment`. Hub closed. Three hard days that crack the world open. |
| 54-63 | special x10 | **Act 3 Slow Burn (hybrid).** `the_return` through `the_threshold`. Hub reopens. Lecture + hub + dinner structure preserved, but corruption escalates from level 1 (deniable) through level 3 (undeniable). See `game/corruption.rpy` and the Act 3 section of `story_treatment.md`. |
| 64 | special | **Act 3 proper begins.** `the_rail`: Hikari takes him back to the firefly path. No free afternoon. |
| 65 | special | `the_answer`: the ghost question returns. The hospital voices disagree with the record. |
| 66-67 | special x2 | `the_notice`, `the_lot`: the shut ramen shop and the destroyed shop are distinct visits. |
| 68-69 | special x2 | `the_detail`, `the_copy`: one-off keepsake revisits, or compare memories and copies with Hikari. |

Totals for 8-69: **41 special, 16 common**, all written.
The last stubs closed on Days 24, 27, 28, 29, and 41.

## Writing a special day

1. Open its `special_day_NN_slug.rpy` stub.
2. Replace the `jump act2_day_router` after `call day_transition` with the
   scene. End the scene with `jump act2_day_router`.
3. Do not touch the router unless the day order itself changes.

## Writing or editing a common day

Common day content lives in `COMMON_DAY_BEATS` at the bottom of
`common_days.rpy`, keyed by day number. Each beat owns: `morning`, `kitchen`,
`lesson` (Hikari teaches a manner or fact), `lecture` (school days only),
`off` (weekend days only), `walk`, `dinner`, `night_a/b/c`, `desk`, `close`,
and optionally `chat_note`. Lines are `(speaker, text)` tuples; `"narr"` is
narration.

Rules for new beats:

- One small true thing per day: a custom, a rule, a word with a shape.
- Hikari's `lesson` should teach something concrete (etiquette, vocabulary,
  a custom) or notice something about the city. Rotate subjects; do not
  repeat a lesson theme within the block.
- Murakami's `lecture` follows the elective's voice: the city as text,
  language as architecture, small ceremonies.
- No em dashes. Commas and periods do the work.

## Living systems in the common days

- **The wallet.** ¥700 is deducted daily in `day_transition`; below ¥5,000 the
  hub drops paid outings (work and free walks remain). `low_funds_nudge_shown`
  gives the reason once. See `game_structure.md` §5.3 for the arithmetic.
- **The journal.** Every common beat has a `notebook` line, collected once per
  day into `notebook_lines`. The phone Journal app has two tabs and opens on
  **JOURNAL** (left), which restores the raw `_history_list` dialogue dump;
  **NOTES** (right) shows that curated "THINGS I NOTICED" list. The game-menu
  Log still holds the full history.
- **The repetition.** Day 38 has Father repeat his Day 34 line word for word;
  `leak_after_dinner` fires `leak_audio` (now `audio/SFX/leak.mp3`) and Hikari
  asks "Did your father say that already?". Day 41 sets `door_twelfth_seen`;
  Day 42's `echo` answers the warm handle with cold temizu water. Both are
  deliberately rare.
- **The commute.** The sleeping man is appended to the rotating commute on
  routine weekdays, absent over Golden Week (25–29), and gone from the end seat
  on Day 45.
- **Cadence.** Tanaka's Day 30/34 reminders only arrive if a shift has actually
  been worked; otherwise Hikari nudges and the beat's `chat_note` is skipped.
  Day 34's `dinner_no_shift` is Father's quieter version of the same table.

## What comes after 45

Days 46-63 are written. The split is:

- **Days 46-50** are late Act 2: five special days (`tsukiji`, `kamakura`,
  `sento`, `hydrangea`, `fireflies`) that close out the warm middle. Hub open.
  Day 50 plants the single glitch seed that the next block picks up.
- **Days 51-53** are the Act 3 incident: three special days (`the_line`,
  `same_face`, `fragment`) with the hub closed. The world cracks open.
- **Days 54-63** are the Act 3 slow burn: ten special days (`the_return`
  through `the_threshold`) with the hub reopened. The lecture + hub + dinner
  structure is preserved so confidant arcs can still finish, but each day sets
  a `corruption_level` (0-3) and calls the three corruption labels in
  `game/corruption.rpy`. Wrongness escalates from deniable (Day 54) to
  undeniable (Day 63, with ChromaGlitch firing on Days 62-63).

- **Day 64** begins Act 3 proper. After Day 63's invitation, the router sends
  the story to `special_day_64_the_rail`. The hub does not reopen.
- **Days 65-69** use the inventory as a record of optional observations.
  The keepsakes are not consumed. No completion count is checked, and each
  day offers a main-story choice with no inventory requirement.
- **Days 70-83** are the written investigation in `act3_investigation.rpy`:
  Day 70 the table, 72 the ramen lot, 74 the photo club, 76 Lupin's Den,
  78 the cafe, 80 the library, 82 the house. Each ends with a player-only lab
  interlude. See `act3_investigation.md`.
- **Days 84-90** are the final week and Act 4 (June 30 to July 6, 2026):
  Days 84-89 are a montage in `act4_bridge`, and Day 90 is played in
  `act4_day_90.rpy`. See `act4_bridge.md` and `act4_skeleton.md`.
