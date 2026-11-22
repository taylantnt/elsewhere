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
| **Sim** | Photography Club (Circle) | Host & Visiting Guide | Connection & Vision |
| **Ramen Chef** | Ramen Shop | Gruff Mentor | Tradition & Acceptance |
| **Aya** | Maid Cafe | Hidden Dreamer | Courage & Safety |
| **Hana** | Reading Club | The Quiet Observer | Wisdom & Escapism |

## Limited & Extra Contacts

These are not seven-visit arcs. They are the two additions the Act 2 audit
justified: a wildcard and a job.

| Name | Location | Role | Key Theme |
| :--- | :--- | :--- | :--- |
| **The Fortune Teller** | Asakusa (folding table) | Oracle / meta guide | Fate, seams, and the white corridor |
| **Tanaka** | Combini (night shift) | Cold cashier / the Doctor's face inside the simulation | Work, scripts, and recognition |

- **The Fortune Teller** is a **three-card** exception: Day 13's scripted reading,
  one hub return that turns the second and third cards, and then the deck closes.
  `confidant_visit_totals["fortune"] = 3`.
- **Tanaka** is tracked by shifts, not visits: `tanaka_story` (0–7 teaching
  shifts, one per visit file in `game/job_combini/`) and `combini_shifts`
  (every shift worked, including the repeats after visit 7). The job row stays
  available after the arc, because the store does not close.
- **The tencho reveal (visit 6):** Tanaka is the store manager. The protagonist
  spent five teaching shifts assuming the manager was somebody else, and the
  reveal reframes the job. He is the face the program wears when it wants
  somebody to work. See [Tanaka / The Doctor](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/Tanaka%20-%20The%20Doctor/character%20details.md).

## Mysterious Figures

- **The Robed Figure**: A dream-world recurring character urging the player to "Wake up."
  `images/characters/hood.png` is the reserved portrait. It is on disk but
  deliberately unwired: the figure has no speaking lines yet.
- **The Doctor**: The clinical voice from the real world (Future Japan Facility).
  He is the same man as Tanaka, in a white coat and a surgical mask. The face is
  identical under the mask, and `images/characters/doctor.png` is the reserved
  portrait. It stays unwired until the later laboratory scenes so he keeps no
  face while he is only a voice in a dream.
- **The Fortune Teller**: An omnipotent, potentially meta guide who knows the simulation's rules.
- **Murakami**: The Japanese elective teacher. A woman, a mentor, and the second
  thematic spine of Act 2. A confidant with no ending: she has ten written visits
  in `confidant_visits/murakami.rpy` and then office hours continue forever. She
  stays out of `confidant_order`, so she never blocks the introduction gate. Her
  WIRE meter still counts lessons (`murakami_lessons`), not visits. She appears in
  the after-school list from the Day 10 fair; enrolling on Day 12 is a separate
  choice that only drives WIRE and dialogue.

## One Face, Two Jobs (Tanaka / The Doctor)

Canon decision, 2026-11-20. The cold cashier and the clinical voice are the same
person. In the simulation he is Tanaka the tencho, handing out a striped shirt
and a register script. Outside it he is the Doctor at the facility, running the
test, naming the subject by number and deciding when the day is over. He is the
face the system uses to keep people in line, and work is how he does it: a
shift here, an experiment there. The protagonist is not visiting the combini by
accident. He is being made to work in both places.

This is seeded in the shipped script but never stated outright: the first
counter scene says the fluorescent light makes Tanaka's face the doctor's face
(`city_rows.rpy:336`), visit 3 has him deflect the recognition with a line about
the world saving money on faces (`tanaka_visit_03.rpy:50-53`), and visit 6 puts
the tencho and the white room in the same paragraph (`tanaka_visit_06.rpy:47-52`).
The job shifts now carry the rest of the hint.

## Supporting Cast

Recurring non-confidant characters who give the locations their texture:

- **Circle members** (Nami, Marcus, Rika, Riku, Tapi) and **TT** (Tapi's
  boyfriend, a photographer who comes to the exhibition) — Sim's photography
  club;
  see [`-Side Characters/Circle members.md`](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/-Side%20Characters/Circle%20members.md)
- **The Reading Circle regular** — Hana's silent scene partner at the library
- **Lupin's Den regulars** — the fox, the rabbit, the white mask; Orson's
  clientele
- **The combini regulars** — the old man who buys one banana, the teenager with
  three energy drinks, the mother with a bento and a carton of milk

Recurring supporting characters with speaking lines now have portraits, wired as
side images in `game/script.rpy`: the Circle members (Nami, Tapi, Rika, Riku,
Marcus, TT), the elective's five exchange students (Wei, Priya, Oliver, Prakash,
Saman), Kenta and the two exchange students in the ramen shop, the woman in the
suit, and the reading-room regular. The masked Lupin's Den regulars and the
combini regulars have no speaking lines, so they stay faceless; the Robed Figure,
the Doctor and the generic `exchange_student` are deliberately unwired.

---

## Detailed Character Links
- [Sister - Hikari Nagai](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/Sister - Hikari Nagai (永井 光)/character details.md)
- [Father - Tetsuo Nagai](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/Father - Tetsuo Nagai (永井 哲夫)/Character details.md)
- [Mother - Miharu Nagai](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/Mother - Miharu Nagai (永井 美晴)/character details.md)
- [Orson (Wolf Bar Master)](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/Bar Master - Orson/character details.md)
- [Sim (Host of Circle)](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/Sim/character details.md)
- [Ramen Shop Chef](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/Ramen Shop Chef/character details.md)
- [Maid Aya](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/Maid Aya/character details.md)
- [Fortune Teller](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/Fortune Teller/character details.md)
- [Tanaka / The Doctor](file:///Users/taylan/Documents/GitHub/elsewhere/documentation/Characters/Tanaka%20-%20The%20Doctor/character%20details.md)
