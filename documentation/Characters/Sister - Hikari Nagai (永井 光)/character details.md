# Character Profile: Hikari Nagai (永井 光)

## Snapshot

| Field | Detail |
| :--- | :--- |
| **Role** | Host sister — and, in the real world outside the simulation, a programmer on the project |
| **Location** | The host family home, the river, and the city tours she introduces |
| **Archetype** | The Compass |
| **Affection Variable** | `sister_affection` |
| **Language** | Bilingual in effect — she sets up WIRE and can explain a word when the story puts her in the room, but she is not a translator for every Japanese-only scene |
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
Hikari's arc is not a numbered 1–7 chain like the location characters. It is a progression tracked by `hikari_visits`, and it runs *parallel* to the confidant arcs rather than ending them. (`sister_affection` tracks the relationship, but it is never read to gate scenes; only `hikari_visits` does.) In the shipped Act 2 build the runs move through warmth and the first stirrings of unease:

| Stage | `hikari_visits` | Beat |
| :--- | :--- | :--- |
| Warmth | 0–1 | She plays the host sister perfectly: warm, teasing, helpful. She set up WIRE and is the reason the protagonist can text anyone. |
| Unease | 2–3 | She starts testing the protagonist with small questions and admits the run is something she needs. |
| Small truths | 4–5 | She says the first true thing about the house and asks whether the street looks the same to him. **(Act 3/4 — not yet written):** a repeated face, a sentence she has said before, a memory that does not line up; a name, a date, a detail that could not exist inside the world. She never calls it a simulation. |
| The Threshold | 6–7 | She asks whether they have done this before and asks him to remember. The reveal itself belongs to Act 3/4; the seventh river run ends on the question that opens it. |

## The River Run (Act 2)

The parallel arc's Act 2 spine is the recurring river run. The first run is the
Day 2 afternoon fork (`after_school_run` in `script.rpy`); visits 2–7 live in
`game/confidant_visits/hikari.rpy` and are routed by `confidant_visit_hikari` from the hub's
"Walk home with Hikari" row. `hikari_visits` counts the runs and feeds the WIRE
progress meter; `sister_affection` carries the relationship but does not gate any
scene. The seven beats:

| Run | Label | Beat | What it costs her |
| :--- | :--- | :--- | :--- |
| 1 | `after_school_run` | He struggles; she invites him and tells him he kept up. | She lets someone see the thing she does for herself. |
| 2 | `hikari_visit_02` | The route from memory. | She admits she needs the run, not just likes it. |
| 3 | `hikari_visit_03` | He keeps up for ten minutes. | He sees her face when she is not performing. |
| 4 | `hikari_visit_04` | The night neither of them says anything. | She admits she does not know where the performance ends. |
| 5 | `hikari_visit_05` | The rain, the amado, the street question. | She says the first true thing about the house. |
| 6 | `hikari_visit_06` | The part of the river she keeps for herself. | She admits it is not the house she is running from. |
| 7 | `hikari_visit_07` | The last run; she asks if they have done this before. | She asks him to remember the promise. |

The seventh run sets `hikari_run_finished = True`. The run chain does not
resolve the Threshold; it ends on the question. After visit 7 the hub row falls
back to the ordinary walk home (`afternoon_walk_hikari`), so she remains
available without the run repeating. Visits 2–7 are reachable from the shipped
Day 8+ hub; after visit 7 the row falls back to the ordinary walk.

## How Her Arc Ends
Her arc is the engine of the endgame, so it does not "close" — it forks:
- **High affection + protagonist accepts the truth** → she helps you escape the facility. She betrays the project she is part of.
- **High affection + protagonist refuses** → she lets you stay. Whether that is mercy or failure depends on the ending.
- **Low affection** → she breaks under the pressure and withdraws. The protagonist wakes without a guide, and the simulation simply ends on its own terms.

## What She Symbolises in the Simulation
She is the conscience of the project. The others leave for ordinary human reasons; Hikari is the only one who tries to leave because the world itself is wrong — even though, within it, she is the one who stays. Her Japanese line style should stay casual and warm even when the content turns eerie.

## Writing Notes
- She is the **language bridge in principle** — she set up WIRE and can explain a word when the story puts her in the room — but she is not a walk-on translator for every Japanese scene. The Chef arc deliberately has the protagonist work things out from gesture, repetition, and the bowls in front of him.
- Her warmth must be genuine, never sinister. The horror comes from *the reader*, not from her.
- She is the only character who should ever say the word "real" in a way that lands.

## Signature Lines
- "You're late."
- "The route is not the point. The point is that I know it without looking."
- "I hear everything."
- *(late game, quietly)* "Don't you ever feel like we've done this before?"

## Continuity Note
In `home.md`, the Mother's line reads: *"Miharu's room is next door so please try not to make a lot of noise. She is a light sleeper."* Because **Miharu is the mother**, that line almost certainly should refer to **Hikari's** room. Flagged for correction when the home scene is scripted.
