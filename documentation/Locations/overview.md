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

### The Fortune Teller — three cards, not seven

She is a **limited confidant**, not a seven-visit arc. Her row is in Asakusa and
opens after the Day 13 reading (`fortune_arc_started`). The count is
`confidant_visits["fortune"]`, the total is 3, and the third card closes the
deck. She is deliberately **not** in `confidant_order`, so she can never block
the five original arcs or their introduction gate.

### Tanaka — the combini job

Tanaka is a **job contact**, not a confidant. His row is `Combini: Night Shift`
and it appears in **THE CITY** section only after `combini_job_unlocked` is set
by the first counter scene. A shift pays ¥4,800 (¥1,200 × 4 hours), consumes the
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