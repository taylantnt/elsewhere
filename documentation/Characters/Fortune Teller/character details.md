# Character Profile: The Fortune Teller

## Snapshot

| Field | Detail |
| :--- | :--- |
| **Role** | Omnipotent guide / the game's meta voice |
| **Location** | Asakusa, at a folding table between the incense burner and the souvenir stalls. Later: a Harajuku side street and the corner near the house. |
| **Archetype** | The Oracle / The Developer's Hand |
| **Affection Variable** | `confidant_visits["fortune"]` — a **three-card** exception, not a seven-visit arc |
| **Language** | Cryptic, layered, often answers a question with a question |
| **Leaves / Closes?** | The deck closes after the third card. She is still present at the edges of the story; the hub row does not reopen. |

## Personality
- **Surface**: A whimsical roadside fortune teller. Cards, tea leaves, a knowing smile.
- **Deep**: She *knows*. She is aware of the simulation, aware of the player, and possibly aware that she is a character in a game. She never lies outright; she simply refuses to be useful on the first ask.

## Role in the Story
The Fortune Teller is the escape valve for every hint the game wants to give without explaining anything. She exists to make the player feel that the world has rules they have not discovered yet.

She is also the safest place to put **meta** material:
- She can describe the protagonist's life in terms of "chapters" or "routes."
- She can react to actions the protagonist has not told anyone about.
- She can break the fourth wall gently, once, and never apologise for it.

## Design Notes
- Described in the design docs as a **"mysterious self-insert"** — an authorial figure. She is **not** a seven-visit confidant and must never be *earned* like one.
- **Build decision (2026-11-12):** the user asked for her to be a hub confidant in a new Asakusa location. The compromise is a **three-card arc**: one scripted first reading in Day 13, then one hub visit that turns the second and third cards. This keeps the "one visit per chapter" rule and the "never earned" rule while giving her a row the player can return to.
- Give her a small, repeated visual tell (e.g. a glitching card, a reflection that lags a frame behind) so the player can spot her before the plot does.

## Interaction Rules (as built)
| Rule | Detail |
| :--- | :--- |
| Frequency | A Day 12 glimpse with Murakami, the Day 13 Asakusa reading with Hikari, and one hub return that turns cards two and three. The night corner is named by the cards, not played. No fourth visit. |
| Cost | Free. The brass bowl takes a coin but does not require one. |
| Function | Each visit gives exactly **one** piece of true information, wrapped in two pieces of noise |
| Escalation | Her hints sharpen as the white-corridor leaks accumulate. The third card names the facility directly. |
| Hub gate | `fortune_arc_started` is set by the Day 13 reading; `confidant_visit_totals["fortune"] = 3`; the row closes after the third card. |

## Signature Lines (draft — to be rewritten in your voice)
- "You've been here before. Not this street. This *moment*."
- "The cards say you're being looked after. I'd ask by whom, if I were you."
- "Come back when you're ready to hear it. You won't be. You'll come back anyway."

## Continuity Note
`character details.md` for the Fortune Teller was a single paragraph ("Omnipotent guide…"). This profile expands it into a usable design doc, but the **signature lines above are proposed, not written by you** — replace them with your own voice before they go into a script.
