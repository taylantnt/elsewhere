# Elsewhere — Character Attribute System
**Document type:** Game Design Specification  
**System:** Three-Pillar Character Progression  
**Status:** Core design reference, revised November 6, 2026

## 1. Overview

Elsewhere uses a three-attribute character progression system inspired by social-stat mechanics in life-simulation RPGs.

The system tracks the protagonist's personal development through three broad attributes:

1. **Insight** — The power to understand.
2. **Grace** — The power to connect.
3. **Nerve** — The power to act.

Each attribute represents a collection of related qualities rather than one narrow skill. Together, they describe how the protagonist understands the world, navigates relationships, and responds to uncertainty or adversity.

Actions throughout the game can increase one or more attributes. Attribute progression may unlock new dialogue choices, interactions, opportunities, clues, and alternative ways to approach situations.

The system should support Elsewhere's blend of university life, interpersonal relationships, and an increasingly mysterious underlying reality.

## 2. Core Design Philosophy

The attribute system must follow these principles.

### 2.1 Broad, meaningful attributes

Each attribute encompasses several related capabilities. Do not introduce separate stats for every individual quality already covered by Insight, Grace, or Nerve.

For example, intelligence, curiosity, observation, and analytical thinking belong under Insight rather than existing as four separate progression systems.

### 2.2 Actions express character

The player develops attributes by doing things, making decisions, and interacting with the world.

In a visual novel almost every action is a sentence, so **answering is doing**. A conversation the player can only listen to teaches the system nothing; the protagonist develops because he chooses what to say when something is actually at stake.

Reward a specific action, not a preferred personality. Grace can come from noticing another person's discomfort and responding thoughtfully. Nerve comes from speaking or acting despite uncertainty. Insight comes from observation and reasoning, not simply receiving information.

Two consequences follow from this, and both matter when authoring:

- **Tone alone is never a reward.** The answer must express a concrete behavior.
- **Not every answer pays.** Selected dialogue choices earn small gains; major events remain larger. Neutral answers must still be sensible and complete.

### 2.3 Progression creates opportunities

Increasing an attribute should provide meaningful benefits. Higher values may unlock additional choices or approaches, but they should not automatically determine every outcome.

The player should still be able to succeed through alternative approaches when appropriate.

### 2.4 No mandatory personality

The system must not imply that one attribute is morally superior to another.

A protagonist with high Insight and low Grace is not inherently worse than one with high Grace and low Insight. Different combinations represent different approaches to life.

### 2.5 Narrative integration

The attributes must feel like a natural part of the game rather than arbitrary RPG statistics.

Use them to support the narrative, character development, exploration, and player agency.

---

## 3. Attribute Definitions

### 3.1 Insight
**Core concept:** The power to understand.

Insight represents the protagonist's ability to learn, observe, reason, recognize patterns, and understand what lies beneath the surface.

It covers intellectual development as well as curiosity, perceptiveness, and analytical thinking.

**Included qualities**
- Knowledge and learning
- Academic ability
- Curiosity and investigation
- Observation and attention to detail
- Critical thinking and reasoning
- Pattern recognition
- Understanding motives and inconsistencies
- Connecting clues and interpreting evidence
- Questioning assumptions and perceived reality

**Typical actions that may increase Insight**
- Studying for university examinations
- Reading educational or intellectually challenging material
- Solving a difficult problem
- Investigating a suspicious event
- Carefully examining an unfamiliar place
- Recognizing a contradiction in someone's story
- Discovering a hidden connection between events
- Asking thoughtful questions or pursuing an explanation

**Potential gameplay benefits**
- Unlocking advanced academic dialogue
- Recognizing inconsistencies in the environment
- Discovering clues others overlook
- Identifying contradictions in conversations
- Understanding complex characters or situations
- Accessing alternative investigation options
- Recognizing irregularities in the simulation or underlying reality

**Insight does not automatically mean**
- Emotional intelligence
- Social popularity
- Courage
- Moral goodness
- Being correct about every suspicion

A perceptive protagonist can still misunderstand people, draw incorrect conclusions, or hesitate to act.

### 3.2 Grace
**Core concept:** The power to connect.

Grace represents the protagonist's ability to navigate social situations, understand others, communicate effectively, demonstrate empathy, and build trust.

It combines interpersonal awareness with communication and social adaptability.

**Included qualities**
- Empathy and compassion
- Charisma and social confidence
- Communication and conversational tact
- Emotional awareness
- Diplomacy and conflict resolution
- Persuasion and negotiation
- Building rapport and trust
- Reading social cues
- Making others feel comfortable
- Adapting to unfamiliar social expectations

**Typical actions that may increase Grace**
- Comforting a distressed friend
- Helping another student with a personal problem
- Resolving an argument constructively
- Successfully navigating an awkward interaction
- Making an effort to understand another person's perspective
- Helping a member of the host family
- Building trust through a meaningful conversation
- Handling a delicate social situation with tact

**Potential gameplay benefits**
- Unlocking empathetic dialogue options
- Building rapport with specific characters
- Defusing interpersonal conflicts
- Persuading someone to share information
- Navigating difficult social expectations
- Gaining access to certain social opportunities
- Creating alternative outcomes through cooperation and trust

**Grace does not automatically mean**
- Physical attractiveness
- Popularity
- Agreeableness
- Flattery
- Manipulation
- Always being kind or avoiding confrontation

Grace can involve setting boundaries, disagreeing respectfully, or confronting someone in a way that preserves dignity.

A socially perceptive protagonist may understand another person without necessarily agreeing with them.

### 3.3 Nerve
**Core concept:** The power to act.

Nerve represents the protagonist's willingness to act despite fear, uncertainty, pressure, discomfort, or potential consequences.

It combines courage, determination, initiative, and the capacity to confront difficult situations.

**Included qualities**
- Courage and bravery
- Determination and resolve
- Initiative
- Willingness to take risks
- Standing up to authority
- Resisting intimidation or peer pressure
- Confronting uncomfortable truths
- Persistence under pressure
- Acting despite uncertainty
- Defiance when circumstances demand it

**Typical actions that may increase Nerve**
- Challenging an unfair decision
- Standing up for another student
- Asking a question others are afraid to ask
- Confronting someone intimidating
- Investigating a disturbing discovery despite fear
- Taking responsibility for a difficult decision
- Trying something unfamiliar despite embarrassment
- Continuing a difficult task instead of giving up

**Potential gameplay benefits**
- Unlocking bold or confrontational dialogue options
- Challenging authority figures
- Pursuing dangerous or uncomfortable investigations
- Defending other characters
- Resisting intimidation
- Taking decisive action during a crisis
- Choosing to confront a mystery rather than avoid it

**Nerve does not automatically mean**
- Recklessness
- Aggression
- Physical strength
- Stubbornness
- Impulsiveness
- Fearlessness

A character with high Nerve can still experience fear. The defining quality is the willingness to act despite that fear.

Careful planning can require Nerve, just as impulsive behavior can reflect poor judgment rather than courage.

---

## 4. How Attributes Differ

When assigning attribute gains, use the following distinctions.

| Attribute | Primary question | Core behavior |
|---|---|---|
| Insight | What can I understand? | Learn, observe, investigate, reason |
| Grace | How can I connect? | Empathize, communicate, persuade, cooperate |
| Nerve | What am I willing to do? | Confront, risk, persist, act |

Some actions naturally overlap. The system should allow this when the action genuinely expresses multiple qualities.

For example, investigating a suspicious event might reward Insight. Investigating despite a frightening warning might reward both Insight and Nerve.

Do not force every action into exactly one category.

## 5. Attribute Gains and Activity Mapping

Attribute gains should reflect the substance of an action, not just its superficial appearance.

### Example gain table

| Player action | Suggested gain | Reason |
|---|---|---|
| Studying for an exam | Insight | Learning and academic development |
| Solving a difficult puzzle | Insight | Reasoning and problem-solving |
| Noticing a contradiction | Insight | Observation and critical thinking |
| Comforting a friend | Grace | Empathy and emotional awareness |
| Resolving an argument diplomatically | Grace | Communication and conflict resolution |
| Persuading someone through understanding | Grace | Rapport and social awareness |
| Challenging an unfair professor | Nerve | Confrontation and courage |
| Investigating something frightening | Insight + Nerve | Investigation combined with willingness to face risk |
| Standing up for a vulnerable student | Grace + Nerve | Empathy combined with decisive action |
| Carefully persuading someone to reconsider a false belief | Insight + Grace | Reasoning combined with interpersonal skill |
| Speaking up despite social embarrassment | Grace + Nerve | Communication combined with courage |

These are design examples, not mandatory point values. Context determines the correct reward.

### 5.1 Multiple-attribute rewards

A single action may increase more than one attribute when it meaningfully expresses multiple qualities.

However:
- Do not reward every attribute for every action.
- Do not award extra attributes merely to make a choice feel rewarding.
- Do not give multiple rewards for the same underlying behavior without a clear design reason.
- Keep rewards consistent across comparable situations.

### 5.2 Choice-specific rewards

When a scene offers multiple approaches, different choices may express different attributes.

Example: The protagonist discovers that a professor has given a student an unfair grade.

- Investigate the grading evidence before acting: **Insight**
- Speak privately with the professor and seek a constructive resolution: **Grace**
- Challenge the professor directly in front of the class: **Nerve**

These choices are illustrative, not universal rules. A public confrontation could also involve Grace if written as a tactful defense of another student. A private conversation could require Nerve if it involves confronting someone intimidating.

Reward the behavior actually represented by the choice.

### 5.3 Passive activities and meaningful choices

Routine activities can grant small, predictable gains. Significant decisions may grant larger gains or multiple attributes.

Avoid requiring the player to grind repetitive activities excessively just to access essential narrative content.

Important story developments should remain accessible through reasonable play, while higher attributes can provide additional options or insights.

### 5.4 Dialogue answers

Selected dialogue answers earn modest, behavior-specific adjustments, often
between **0.1 and 0.5 points**. Other answers earn nothing and are not failures.
Intentional trade-offs can reduce one attribute while raising another, and a
negative value never lowers a total below zero.

Thoughtful treatment of someone, a concrete observation, or speaking despite
embarrassment can earn a small gain without changing the story's destination.
Larger events remain distinct and can grant 1.0 point.

Do not attach attribute prefixes to ordinary rewarded answers. The player
chooses the reply, then receives signed feedback. Colored attribute tags are
reserved for gated options.

**Rules for authoring an answer:**

1. **Points are selective and deliberate.** Name the behavior being rewarded. Routine agreement, greetings, and every factual question do not automatically pay.
2. **Usually one attribute per answer.** A clear trade-off may intentionally raise one attribute and lower another; show both signed changes and keep both values modest.
3. **A fork pays once, ever.** Anything reachable twice goes through `reward_attributes_once` with a unique flag (identifier form `answer_<scene>_<choice>`), and a conversation the player can walk back up to replays the stored answer rather than reopening the menu. See *Answering a person twice*, below.
4. **Each option must be a plausible response to the prompt.** Distinguish the replies without forcing three artificial personality types into every scene.
5. **Order the options so the brave one is not last by default.** The player reads the first line as the natural answer.

**Answering a person twice.** Any conversation the player can walk back into is a slot machine unless the game latches the answer. `remembered_choice(person)` returns what he already said to that person, or `None` if the two of them are new to each other; the label then jumps straight to the stored answer instead of offering the menu a second time, and `remember_choice(person, answer)` latches a fresh pick. Answer A once and every later visit is A, until a scene is written specifically to let him ask again. This is wired into the four airport conversations, which are the ones a player can loop through at will.

A deferred assistant request is an explicit exception: leaving the desk does not permanently latch refusal of the pamphlet required for progression. Successful direct and patient requests do latch and replay. Older saves with the former `nevermind` answer can ask again.

### 5.5 Implemented answer map

The [attribute rewards checklist](./attribute_rewards_checklist.md) is the
complete, current inventory of dialogue and event rewards through the playable
build, including signed changes, once-only flags, and point-gate requirements.
Keep it in sync
when editing this system rather than maintaining a second reward table here.
Rewards use `reward_attributes_once`, so a choice cannot be farmed by revisiting
its scene. The three afternoon routes remain mutually exclusive.

---

## 6. Progression Model

The exact numeric model may be determined during implementation, but it must preserve the design principles below.

### 6.1 Independent progression

Insight, Grace, and Nerve progress independently.

Improving one attribute must not automatically increase another unless an explicit game mechanic requires it.

### 6.2 Rank-based progression

Progression is a five-rank ladder:

| Rank | Name | Begins at (cumulative points) |
|---|---|---|
| 1 | Rank 1 | 0.0 |
| 2 | Rank 2 | 2.0 |
| 3 | Rank 3 | 5.0 |
| 4 | Rank 4 | 9.5 |
| 5 | Rank 5 | 15.0 |

These are **cumulative totals, not points-per-rank**: rank 2 begins when the attribute has 2.0 points in it, in total, since the beginning of the game. Each step costs more than the last, so the early game moves quickly and the later game means something.

The thresholds and names are configured in one place (`init python` in
`game/script.rpy`, `attribute_rank_thresholds` and `attribute_rank_names`).

### 6.3 Fractional accumulation

**Points may use tenths or halves.** Small dialogue adjustments can be as low as
0.1, and negative adjustments are intentional where a response reflects a
trade-off. Totals stop at 0.0 and 15.0; feedback shows the signed amount actually
applied. Rank thresholds are unchanged.

Use named reward sizes in story code so point changes remain consistent as the
dialogue grows. Losses have a named counterpart; reserve raw numbers for gates,
formatting, and calculations rather than individual dialogue rewards:

| Size | Points | Used for |
|---|---|---|
| `tiny` | 0.1 | A brief first contact or small gesture |
| `micro` | 0.2 | A short, clear answer |
| `micro_loss` | -0.2 | A mild, intentional trade-off |
| `nudge` | 0.3 | A thoughtful response or modest observation |
| `small` | 0.5 | A meaningful choice or route-defining beat |
| `medium` | 1.0 | A substantial set piece |
| `large` | 2.0 | Reserved for later act-turning decisions |

`add_attribute_points(attribute_id, amount, show)` accepts either a name or a
raw signed number. Prefer a named size for dialogue rewards; use explicit numbers
for point thresholds and formulas.

For the opening days, keep routine choices around 0.2–0.3 and a first-afternoon
route closer at 0.5. A single early scene should not award a full rank by
itself; reserve 1.0-point rewards for substantial set pieces.

### 6.4 Displaying progress

Every applied adjustment is shown, including losses. Which presentation is used
is decided centrally by `add_attribute_points`:

| Trigger | Presentation |
|---|---|
| A small adjustment inside a conversation (`show="auto"`) | **Tick chip.** A signed amount beneath the matching labeled HUD circle that rides over the next couple of lines and hides itself. Costs the player no click and no pause. |
| A rank change, whatever the size | **Gain card**, always; the card identifies a rank increase or decrease. |
| A turning point (`show="card"`) | **Gain card.** |
| Bookkeeping that is not a reward (`show=False`) | Nothing. |

**The tick chip** sits directly beneath the matching labeled attribute in the **top-right HUD**, where it is out of the reading path and never covers the dialogue plate it is talking about. It uses the attribute's accent colour and signed amount; the name stays on the circle above it. Adjustments to different attributes can appear together beneath their respective circles. The old top-centre slot is occupied by the character-memory notice (§7.8), so the two never collide: stats speak from the right, memory speaks from the centre.

**The gain card** uses three reserved circle cells in a wide triangle. Circles grow from 176 to 240 virtual pixels. The active attribute emits outward-fading ripples; inactive circles are subdued. Rank numerals and aligned labels render after the artwork, so circles cannot cover them. Names, `RANK 02 / 05`, factual descriptions, and points remaining use a fixed baseline. Qualitative ribbons such as "Emerging" and "Exceptional" are removed. The headline and gain readout occupy separate top corners. Continue appears after the sound and opening beats.

**The HUD** uses three labeled current-rank circular meters. Each resets on rank-up. A small amount chip is centered underneath its matching meter for 2.10 seconds. Each attribute has an independent expiry; a fresh gain refreshes only that chip. A short tick sound accompanies small gains.

**Two places to look at the state:**

- **HUD** — three static labeled circular meters, always on screen once the game begins.
- **Attributes page** — inside the shared phone menu, also reached from the bottom dock. Each row has a circle with a centered rank numeral, an uppercase name, a compact rank readout, points remaining, a factual description, and lifetime total. Progress is circular, not duplicated in a bar.

Notifications stay short. The system never interrupts with a wall of text about a half point.

### 6.5 As-implemented reference

Everything below lives in `game/script.rpy`, in `init python`, so there is one source of truth:

| Item | Name |
|---|---|
| Values | `character_attributes` (float per attribute id) |
| Definitions, colours, blurbs | `attribute_defs` |
| Draw order | `attribute_order` = `insight`, `grace`, `nerve` |
| Coloured tags | `attribute_tag`, `tag_insight`, `tag_grace`, `tag_nerve` (generated from `attribute_defs`, so they can never drift from the colours) |
| Rank thresholds | `attribute_rank_thresholds` |
| Rank names | `attribute_rank_names` |
| Reward sizes | `attribute_reward_sizes` |
| Awarding | `add_attribute_points`, `reward_attributes_once` |
| Reading | `attribute_total`, `attribute_rank`, `attribute_rank_name`, `attribute_progress`, `attribute_rank_progress`, `attribute_rank_next_text` |
| Gating | `has_attribute(attribute_id, minimum_rank)` and `has_attribute_points(attribute_id, minimum_points)` |
| One-time flags | `attribute_reward_flags` (list of string flags) |
| Answer replay | `remembered_choice`, `remember_choice`, and the `remembered_choices` dict (`default`) |
| Character memory | `remember`, and the `character_memories` dict (`default`) |

UI: `screen attribute_hud`, `screen attribute_tick`, `screen attribute_gain_card` (plus `show_attribute_tick`), `screen memory_notice` (plus the `memory_notice_appear` transform), and `screen attributes()` in `game/screens.rpy`.

---

## 7. Dialogue and Narrative Integration

Attributes should expand the player's choices rather than simply label dialogue as good or bad.

### 7.1 Attribute-gated dialogue

Higher attributes may unlock special dialogue options.

Examples:

**Insight requirement**
> "That doesn't match what you told me yesterday. What actually happened?"

**Grace requirement**
> "You don't have to explain everything right now. I just want to understand."

**Nerve requirement**
> "I'm not leaving until you tell me why this happened."

These are illustrative lines. Final dialogue should match the speaker, scene, and emotional context.

### 7.2 Show the approach, not just the requirement

A locked option **stays on the page and goes grey** rather than disappearing. A greyed line tells the player that a way of answering exists here that he is not yet capable of, which is the entire point of gating; a line that is simply absent teaches nothing. This is `config.menu_include_disabled = True`, set once in `game/script.rpy`.

The option carries a small coloured prefix naming the attribute it wants, written as `[tag_insight]`, `[tag_grace]` or `[tag_nerve]` at the front of the caption, which the substitution pass expands into a coloured `[Insight]`-style tag. The three tag strings are generated from `attribute_defs` so they can never drift out of step with the attribute colours.

```renpy
"[tag_grace] You've made this much easier." if has_attribute_points("grace", 1.0):
    ...
```

### 7.3 Use the minimum that keeps a choice attainable

Attribute gates may use either rank or raw points. Use
`has_attribute_points(attribute_id, minimum_points)` for early branches where a
full rank would be an unnecessarily high barrier; keep rank-based checks for
choices that explicitly need developed capability.

The first university dialogue gates use 0.8 Insight, 1.0 Grace, and 0.3 Nerve.
These are reachable through deliberate choices before the relevant scenes,
including on either travel route, without changing the rank ladder.

### 7.4 No gates at the beginning

**The prologue and the first morning before the university contain no locked answers.** Ordinary dialogue gains do not need an existing attribute rank.

Gates begin inside the university sequence. Smaller observations and responses
accumulate alongside travel and route rewards, so route choice is not the only
source of development. Gated replies provide an additional approach, not
information required to continue.

The first three gates are one per attribute, and each one is a different kind of door:

- **Insight** (poster wall) — asks him to have noticed a detail nobody pointed out.
- **Grace** (student relations) — acknowledges how the clerk has helped with an overwhelming first day.
- **Nerve** (the professor) — respectfully requests review of a late mark caused by official registration. All branches still receive the full attendance rule.

### 7.5 No guaranteed success

An attribute requirement indicates that the protagonist has developed a relevant capability. It does not guarantee that another character will agree, cooperate, or reveal the truth.

Outcomes should also consider:
- The other character's personality
- Previous interactions
- Relationship state
- Available evidence
- The circumstances of the scene
- Earlier player decisions

### 7.6 Relationships remain distinct

Grace is not a replacement for relationship progression.

A protagonist may have high Grace while maintaining a poor relationship with a particular character. Likewise, a character may trust the protagonist because of previous events even if Grace is relatively low.

Keep general character attributes distinct from individual relationship values and relationship milestones.

### 7.6.1 Relationship Trust Levels

Relationship values are written separately from the three attributes. The
current build uses `sister_affection` for Hikari and `father_affection` for
Tetsuo, plus per-confidant placeholders for Sim, Orson, Chef, Aya and Hana. Those
values are **trust**, not points to spend.

The helper implementation in `game/script.rpy` reads them through
`affection_level()`, with thresholds:

| Level | Begins at | Meaning |
|---|---:|---|
| 1 | 1 | Known enough that the person has let the protagonist closer than a stranger. |
| 2 | 3 | Trusted enough that the person expects the protagonist to mean what he says. |
| 3 | 5 | Close enough that the person brings the thing they would not say aloud. |
| 4 | 8 | Family enough that the door is open without asking. |

Hikari’s affection should rise from better answers and real observations; Tetsuo’s
from kept promises, responsibility, and practical care. Aya’s first maid-cafe
visit now increments her relationship value. Future confidant content can use the
same helper rather than adding a second affection system.

### 7.7 Mystery and discovery

Insight and Nerve should be especially useful in the mystery elements of Elsewhere.

Insight may help the protagonist recognize anomalies, connect clues, and question assumptions.

Nerve may help the protagonist pursue those discoveries despite fear, social pressure, or the risk of consequences.

Neither attribute should automatically reveal the entire mystery. Evidence, story progression, and player decisions remain important.

Grace may provide another route through the mystery by helping the protagonist build trust, obtain testimony, or understand the people involved.

### 7.8 Characters remember what he said

Attributes say what the protagonist is *becoming*. They say nothing about what he actually said to anyone, and in a game whose theme is that getting close to someone is what makes them leave, the things he said have to land somewhere.

So there is a second, separate record: **character memory**. When an important character is on the other end of a fork, the answer is logged against them with `remember(who, note)`, and the player sees

> *(Hikari will remember that)*

as a short centred notice that fades in under the top of the screen and fades out on its own after about two and a half seconds. It costs no click and does not pause the game.

Design rules:

- **Memory is not a reward.** A remembered answer pays nothing and a paying answer is still remembered; the two systems are independent and neither substitutes for the other. That is the whole point: an answer can be free and still matter.
- **Memory is for people who matter.** Tag someone when losing them is a scene the story is going to spend; do not tag a stranger the protagonist will never see again. The characters tagged so far are **Hikari**, the **circles clerk**, the **professor**, **Tetsuo** (the father), and **Sim**.
- **Write the note as a plain fact, first person.** `remember("hikari", "asked what she saw in the courtyard, years ago")` - not "was kind", not "earned Grace". It is a log of what he did, not of what it was worth.
- **A replayed answer is still remembered, but only once.** A latched answer (§5.4) that the game plays back on a second visit must not log its memory again, so the notice does not repeat.
- **The name on screen is not the id.** The keys are lowercase ids; the notice reads from `memory_names` so it can say "Hikari" rather than "hikari", and anything untagged falls back to a capitalised id.

The notice is `screen memory_notice` plus the `memory_notice_appear` transform, and it takes the **top-centre** slot, which the stat tick chip has vacated (§6.4). Stats speak from the right, memory from the centre.

---

## 8. UI and Terminology

Use these names and descriptions consistently throughout the game.

| Attribute | Short description | UI identity |
|---|---|---|
| Insight | Observation and reasoning | Observation, discovery, intellect |
| Grace | Empathy and communication | Empathy, communication, trust |
| Nerve | Resolve under pressure | Courage, resolve, initiative |

### UI writing rules

- Always use the canonical names: **Insight**, **Grace**, and **Nerve**.
- Use the same capitalization in menus, dialogue requirements, notifications, documentation, and code-facing identifiers where practical.
- Avoid switching between synonyms such as Wisdom, Intelligence, Charm, Charisma, Bravery, and Guts as if they were separate attributes.
- Synonyms may appear in ordinary dialogue, but they must not introduce new progression categories.
- Keep gain notifications short and unobtrusive.
- Do not reveal hidden narrative information through attribute labels unless explicitly intended.
- **Each attribute owns one colour, everywhere.** Insight is blue (`#5fb8ff`), Grace is green (`#77d98b`), Nerve is red (`#ff6b6b`). The same colour is used on the HUD chip, tick chip, gain card, and gated-answer tag, and the tag strings are generated from the colour table so they cannot drift. Colour is how the player tells three attributes apart at a glance without reading a word.
- Colour must never be the *only* signal. Every coloured element also carries the attribute's name, so the system stays readable for colour-blind players.
- The Attributes page is reachable both from the in-game menu and from the `Attributes` button in the bottom dock; the dock is the discoverable route and must stay there.

### In-game input and choice presentation

- **Right-click does nothing during the game.** The mouse must not be able to open the game menu, so `config.keymap["game_menu"]` is filtered down to the keyboard keys (Escape) and the `mouseup` bindings are removed. A stray right-click in the middle of a scene must not interrupt the fiction.
- **A hovered choice keeps its plate and lifts it; it does not repaint it.** The choice art is a near-black plate. Hovering lightens the plate a shade (`Solid("#3d362bf0")`) and moves the text to the accent colour. The old hover swapped in a mid-tone amber plate with dark text, which was the readability complaint.
- **A locked choice gets its own recessed chip.** There is no insensitive choice art in `gui/button`, so locked answers used to fall back to the idle plate and read as selectable. They now sit on a darkened, recessed chip (`Solid("#100f0dcc")`) with dimmed text, so a closed door looks closed.

---

## 9. Implementation Guidelines for the Coding Assistant

The following requirements govern all code that implements or modifies this system.

### 9.1 Preserve the three-attribute model

The canonical attributes are:
- Insight
- Grace
- Nerve

Do not introduce additional core character attributes without explicit design approval.

Individual skills, quest flags, relationship values, inventory statistics, and other mechanics may exist independently when needed, but they must not silently expand this three-pillar system.

### 9.2 Centralize definitions

Where the existing architecture permits, keep attribute identifiers, display names, descriptions, rank thresholds, and progression configuration in a central location.

Avoid duplicating progression rules across unrelated scenes or scripts.

### 9.3 Use stable identifiers

Recommended internal identifiers are:

- `insight`
- `grace`
- `nerve`

Display names should remain separate from internal identifiers wherever the project architecture supports that separation.

### 9.4 Reuse existing architecture

Before implementing the system:
1. Inspect the existing project structure.
2. Identify current save data, dialogue logic, activity handling, and UI patterns.
3. Reuse established architecture where appropriate.
4. Avoid creating duplicate managers, conflicting data stores, or parallel progression systems.
5. Follow the project's existing language and coding conventions.

Do not assume that a particular manager, resource, autoload, scene, or script already exists.

### 9.5 Persist progression correctly

Attribute values must be saved and restored through the game's established save/load system.

Loading a save must not reset, duplicate, or unexpectedly increase attribute values.

If the project does not yet have a save system, document that dependency before introducing a new persistence design.

### 9.6 Make rewards explicit

Each action that grants attributes should use an explicit, reviewable reward definition.

Avoid awarding attributes through hidden side effects that make it difficult to understand why a value changed.

Ensure that repeated triggers, dialogue re-entry, scene reloads, and save/load cycles cannot accidentally duplicate one-time rewards.

A conversation the player can walk back into must also **latch its answer** with `remember_choice`, so re-entering it plays back the stored reply rather than reopening the menu. One-time flags stop a point being earned twice; the latch stops a *different* answer being chosen twice, which is the actual farming exploit.

### 9.7 Keep UI and game logic separate

The UI should display attribute state and communicate rewards. It should not independently own the authoritative attribute values.

All attribute changes should pass through the project's established state-management mechanism.

### 9.8 Validate changes

When modifying this system:
- Check for misspelled or unknown attribute identifiers.
- Prevent unintended negative values or values beyond configured limits.
- Verify that rewards are applied only when intended.
- Verify save/load behavior.
- Test rank thresholds and gated dialogue.
- Ensure existing scenes and dialogue remain functional.
- Avoid breaking unrelated gameplay systems.

---

## 10. Design Consistency Rules

These rules are mandatory unless the game designer explicitly changes this specification.

1. **Insight means understanding.** Learning, observation, analysis, curiosity, and investigation belong here.
2. **Grace means connection.** Empathy, communication, persuasion, social awareness, and trust-building belong here.
3. **Nerve means action despite difficulty.** Courage, initiative, resolve, confrontation, and willingness to take risks belong here.
4. Actions may reward multiple attributes, but only when each reward is justified by the action's actual content.
5. Attributes represent development, not moral worth.
6. Attribute levels can unlock options, but must not replace narrative context or relationship progression.
7. Attribute names and meanings must remain consistent across code, UI, and documentation.
8. Do not introduce new core stats without explicit approval.
9. Do not change the progression model or rank thresholds silently.
10. If a proposed feature conflicts with this document, identify the conflict and recommend a resolution before implementing the change.
11. **Points are selective.** Small dialogue gains need a concrete observation, thoughtful response, or act of resolve. Larger rewards belong to substantial events, not routine greetings.
12. **A fork never re-rolls.** Any conversation the player can walk back into latches its answer with `remember_choice` and replays it.

---

## 11. Progression Values — Working Baseline

These are the values **as implemented** in `game/script.rpy`. They are the
defaults to design against, not sacred numbers — revisit them when Act 2/3
content shows where the pacing actually lands.

### Rank ladder (per attribute, cumulative totals)

| Rank | Total points needed | Name (current) |
|------|--------------------:|----------------|
| 1 | 0 | Rank 1 |
| 2 | 2.0 | Rank 2 |
| 3 | 5.0 | Rank 3 |
| 4 | 9.5 | Rank 4 |
| 5 | 15.0 | Rank 5 |

The gaps widen on purpose (2 → 3 → 4.5 → 5.5), so early game moves fast and
the top ranks mean something. Attributes clamp at 0–15.

### Reward sizes

| Name | Points | Use for |
|------|-------:|---------|
| `tiny` | 0.1 | A flicker of behaviour (airport first contacts) |
| `micro` | 0.2 | A short, clear answer inside a conversation |
| `micro_loss` | −0.2 | Soft trade-off cost |
| `nudge` | 0.3 | A stronger reply that is not a turning point |
| `small` | 0.5 | A real choice with a subject |
| `medium` | 1.0 | A set-piece beat that closes a scene or a day |
| `large` | 2.0 | Reserved for act-turning decisions |

### Still genuinely open

- **Rank names.** "Rank 1–05" is a placeholder ladder. When later gates start
  mattering, pick real names — they appear on the gain card and the Attributes
  page, so they should mean something (e.g. per-attribute names, or a shared
  vocabulary like Observer → Fixture → Known → Indispensable → ???).
- **Icons and visual styling** beyond the current orb set.
- **Whether progress is always visible or partly hidden** in later acts.
- **Attribute combinations** for major scenes (e.g. an escape route that wants
  Insight *and* Nerve).
- **How attributes interact with endings** — e.g. whether "assimilated enough"
  for The Escape is measured in ranks, points, or confidant visits.

The mechanics around rewards (§5.4 replay, §7.8 memory, §6.4 presentation)
are the parts meant to stay fixed.

---

## 12. Final Design Statement

**Insight. Grace. Nerve.**

The protagonist grows by learning to understand the world, learning to connect with the people within it, and learning to act when circumstances make action difficult.

These three attributes form the foundation of Elsewhere's personal-development system.

Every implementation should preserve that purpose: the system exists to create meaningful choices, reflect the player's development, and connect everyday university life with the deeper mysteries of Elsewhere.

---

## 12.1 Final Balance Verdict — 2026-11-06

**Verdict: no balance tuning is required at this stage of the current build.**

- The first gates remain deliberately small: **0.8 Insight**, **1.0 Grace**, and **0.3 Nerve**.
- The new night-table unhinged response adds a second Nerve gate at **1.2** rather than replacing or raising the early gate, so the first three doors still lead there first.
- The taxi’s Nerve bonus and the family/night/weekend rewards stay within the existing small-reward scale; the new night and weekend answers use `micro` (0.2) and relationship increments rather than attribute inflation.
- The archived day-one board removes the 1.0 Insight set-piece reward from the active path, but the day-one memory board still pays **0.3 Insight** when solved and the active story otherwise carries its intended pacing.
- A player should still be able to reach **Rank 2** in at least one attribute through deliberate play by the end of day two; no single route is wallowing, and the player is never forced onto one attribute’s treadmill.

The next balance pass should wait for Act 2 confidant scenes and Act 3/4 choices, not for this batch.
