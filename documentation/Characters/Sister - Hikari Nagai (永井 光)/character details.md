# Character Profile: Hikari Nagai (永井 光)

## Snapshot

| Field | Detail |
| :--- | :--- |
| **Role** | Host sister — and, in the real world outside the simulation, a programmer on the project |
| **Location** | The host family home; she also appears at the Ramen Shop (Interactions 4 & 6) as translator |
| **Archetype** | The Compass |
| **Affection Variable** | `sister_affection` |
| **Language** | Bilingual in effect — she is the protagonist's translator and therefore the bridge to every Japanese-only character |
| **Confidant Theme** | Truth, guilt, and the cost of waking up |
| **Leaves / Closes?** | No — she is the one who stays. Her arc is about whether she helps you leave. |

## Name Meaning
**光 (Hikari)** — "light." **永井 (Nagai)** — "eternal well," suggesting endless depth. She is the only character whose name promises illumination and depth at the same time, which is exactly what she withholds until the end.

## Personality
- **Surface**: Extroverted, energetic, grounded. She is the one who sent the emails and the one who makes the house feel like a home.
- **Deep**: Something in her is *wrong* and she can feel it without being able to name it. She loves her family and her life here — and she is quietly certain that her life is not entirely real. She is carrying guilt she cannot explain, because a part of her remembers writing this world.

## Backstory
Hikari is the *essence* of a real-world programmer — not a deliberate avatar, but a fragment of her author that leaked into the code while the simulation was being built. That is why she is the first to sense the seams and the last to understand them. Because her essence went in accidentally, she is not fully aware of what she is: she experiences her suspicion as a private, unshakable anxiety rather than as knowledge.

## Confidant Arc
Hikari's arc is not a numbered 1–7 chain like the location characters. It is a **gated progression** driven by `sister_affection`, and it runs *parallel* to the confidant arcs rather than ending them:

| Stage | `sister_affection` | Beat |
| :--- | :--- | :--- |
| Warmth | 0–2 | She plays the host sister perfectly: warm, teasing, helpful. She translates for the protagonist at the Ramen Shop. |
| Unease | 3–4 | She starts noticing things — a repeated face, a sentence she has said before, a memory that does not line up. She tests the protagonist with small questions. |
| Small truths | 5–6 | She begins to sneak the protagonist information: a name, a date, a detail that could not exist inside the world. She never calls it a simulation. |
| The Threshold | 7+ | She is ready to reveal what she is. The reveal itself belongs to Act 3/4; the seventh river run ends on the question that opens it. |

## The River Run (Act 2)

The parallel arc's Act 2 spine is the recurring river run. The first run is the
Day 2 afternoon fork (`after_school_run` in `script.rpy`); visits 2–7 live in
`game/hikari.rpy` and are routed by `confidant_visit_hikari` from the hub's
"Walk home with Hikari" row. `hikari_visits` counts the runs and feeds the WIRE
progress meter; `sister_affection` carries the relationship. The seven beats:

| Run | Label | Beat | What it costs her |
| :--- | :--- | :--- | :--- |
| 1 | `after_school_run` | He cannot keep up; she invites him anyway. | She lets someone see the thing she does for herself. |
| 2 | `hikari_visit_02` | The route from memory. | She admits she needs the run, not just likes it. |
| 3 | `hikari_visit_03` | He keeps up for ten minutes. | He sees her face when she is not performing. |
| 4 | `hikari_visit_04` | The night neither of them says anything. | She admits she does not know where the performance ends. |
| 5 | `hikari_visit_05` | The rain, the amado, the street question. | She says the first true thing about the house. |
| 6 | `hikari_visit_06` | The part of the river she keeps for herself. | She admits it is not the house she is running from. |
| 7 | `hikari_visit_07` | The last run; she asks if they have done this before. | She asks him to remember the promise. |

The seventh run sets `hikari_run_finished = True`. The run chain does not
resolve the Threshold; it ends on the question. After visit 7 the hub row falls
back to the ordinary walk home (`afternoon_walk_hikari`), so she remains
available without the run repeating. Only the second run is reachable in the
current Day 7 build; visits 3–7 are wired for later hub days.

## How Her Arc Ends
Her arc is the engine of the endgame, so it does not "close" — it forks:
- **High affection + protagonist accepts the truth** → she helps you escape the facility. She betrays the project she is part of.
- **High affection + protagonist refuses** → she lets you stay. Whether that is mercy or failure depends on the ending.
- **Low affection** → she breaks under the pressure and withdraws. The protagonist wakes without a guide, and the simulation simply ends on its own terms.

## What She Symbolises in the Simulation
She is the conscience of the project. The others leave because of ordinary human reasons; Hikari is the only one who leaves because the world itself is wrong. Her Japanese line style should stay casual and warm even when the content turns eerie.

## Writing Notes
- She is the **translator device**. Whenever a Japanese-only scene needs to be understood, Hikari is the honest reason it is.
- Her warmth must be genuine, never sinister. The horror comes from *the reader*, not from her.
- She is the only character who should ever say the word "real" in a way that lands.

## Signature Lines
- "Ah… I thought I'd find you here."
- "Tonight's different. He wanted you here."
- "…He says eating together like this, it feels like family."
- *(late game, quietly)* "Don't you ever feel like we've done this before?"

## Continuity Note
In `home.md`, the Mother's line reads: *"Miharu's room is next door so please try not to make a lot of noise. She is a light sleeper."* Because **Miharu is the mother**, that line almost certainly should refer to **Hikari's** room. Flagged for correction when the home scene is scripted.
