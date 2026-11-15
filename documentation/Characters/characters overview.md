# Characters & Confidants: The Game Bible

## Core Characters

| Name | Role | Archetype | Affection Variable |
| :--- | :--- | :--- | :--- |
| **Protagonist** | Subject 04 | The Outsider | N/A |
| **Hikari Nagai** | Host Sister / Programmer | The Compass | `sister_affection` |
| **Tetsuo Nagai** | Host Father | The Schedule | N/A |
| **Miharu Nagai** | Host Mother | The Guardian | N/A |

## The Confidants (Social Links)

| Name | Location | Role | Key Theme |
| :--- | :--- | :--- | :--- |
| **Orson** | Lupin's Den (Bar) | Wolf Bar Master | Identity & Masks |
| **Sim** | Photography Club (Circle) | Founder & Visiting Guide | Connection & Vision |
| **Ramen Chef** | Ramen Shop | Gruff Mentor | Tradition & Acceptance |
| **Aya** | Maid Cafe | Hidden Dreamer | Courage & Safety |
| **Hana** | Reading Club | The Quiet Observer | Wisdom & Escapism |

## Limited & Extra Contacts

These are not seven-visit arcs. They are the two additions the Act 2 audit
justified: a wildcard and a job.

| Name | Location | Role | Key Theme |
| :--- | :--- | :--- | :--- |
| **The Fortune Teller** | Asakusa (folding table) | Oracle / meta guide | Fate, seams, and the white corridor |
| **Tanaka** | Combini (night shift) | Cold cashier / maybe the researcher's face | Work, scripts, and recognition |

- **The Fortune Teller** is a **three-card** exception: Day 13's scripted reading,
  one hub return that turns the second and third cards, and then the deck closes.
  `confidant_visit_totals["fortune"] = 3`.
- **Tanaka** is tracked by shifts, not visits: `tanaka_story` (0–7 teaching
  shifts, one per visit file in `game/job_combini/`) and `combini_shifts`
  (every shift worked, including the repeats after visit 7). The job row stays
  available after the arc, because the store does not close.
- **The tencho reveal (visit 6):** Tanaka is the store manager. The protagonist
  spent five teaching shifts assuming the manager was somebody else, and the
  reveal reframes the job; it parallels the researcher's role in the program.

## Mysterious Figures

- **The Robed Figure**: A dream-world recurring character urging the player to "Wake up."
- **The Doctors**: Clinical voices from the real world (Future Japan Facility).
- **The Fortune Teller**: An omnipotent, potentially meta guide who knows the simulation's rules.
- **Murakami**: The Japanese elective teacher. A woman, a mentor, and the second
  thematic spine of Act 2. Not a confidant; her WIRE meter counts lessons
  (`murakami_lessons`), not visits.

## Supporting Cast

Recurring non-confidant characters who give the locations their texture:

- **Circle members** (Rika, Nami, Marco, Riku) — Sim's photography club;
  see [`-Side Characters/Circle members.md`](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/-Side%20Characters/Circle%20members.md)
- **The Reading Circle regular** — Hana's silent scene partner at the library
- **Lupin's Den regulars** — the fox, the rabbit, the white mask; Orson's
  clientele
- **The combini regulars** — the old man who buys one banana, the teenager with
  three energy drinks, the mother with a bento and a carton of milk

---

## Detailed Character Links
- [Sister - Hikari Nagai](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/Sister - Hikari Nagai (永井 光)/character details.md)
- [Father - Tetsuo Nagai](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/Father - Tetsuo Nagai (永井 哲夫)/Character details.md)
- [Mother - Miharu Nagai](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/Mother - Miharu Nagai (永井 美晴)/character details.md)
- [Orson (Wolf Bar Master)](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/Bar Master - Orson/character details.md)
- [Sim (Founder of Circle)](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/Sim/character details.md)
- [Ramen Shop Chef](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/Ramen Shop Chef/character details.md)
- [Maid Aya](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/Maid Aya/character details.md)
- [Fortune Teller](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/Fortune Teller/character details.md)
