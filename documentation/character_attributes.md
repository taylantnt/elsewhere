# Elsewhere — Character Attribute System
**Document type:** Game Design Specification  
**System:** Three-Pillar Character Progression  
**Status:** Core design reference

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

The test is not "did the player pick the nice option", it is **"did that answer cost him something"**. Grace is not awarded for politeness, it is awarded for the moment he decides to be a person in front of somebody. Nerve is not awarded for agreeing, it is awarded for asking the thing he would rather not ask. Insight is not awarded for being told a fact, it is awarded for noticing one.

Two consequences follow from this, and both matter when authoring:

- **Tone alone is never a reward.** A scene must put something on the line for the answer to be worth anything.
- **Most answers pay nothing at all.** Answering is not the same as *changing*. Giving the player a voice and giving the protagonist a point are two different jobs, and only the second one is scarce. A fork moves a number only when something actually turns because of the answer. See §5.4.

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

An answering fork in Elsewhere is not a vending machine. The fork exists to give the player a voice, and most of the time that is all it does: the options are still written as three different people, the shape of the fork is unchanged, and **none of them pays anything.**

So the default shape of a fork is:

> **three options, one attribute each, all three worth the same, and in most scenes the worth is nothing.**

The player is not being asked to find the answer that pays. He is being asked what kind of person he is about the same ten seconds. Hikari says there is a pool on whether he would turn up; asking who started it, asking what she bet, and thanking her for the emails are three different people, and all three of them are worth zero points - but Hikari keeps the answer either way.

**Where points do come from.** A reward is reserved for a **turning point**: a moment after which the story is different because of what he chose, not merely coloured by it. In the first act there are exactly two:

1. **The route.** Train or taxi is the one decision in Act 1 that changes what the rest of the day is made of, and it is the one that decides which of Insight or Nerve he starts to become.
2. **The ticket attendant.** The single place the game pays him for admitting he cannot solve a building by himself, and the only route into Grace in the first act.

Everything else - the gate, the ticket machine, the platform signs, the boxes, the pool breakfast, the door, the walk to campus, the courtyard, the poster wall, the circles desk, the professor's rule - stays as dialogue and pays nothing.

**Rules for authoring an answer:**

1. **Points are scarce and deliberate.** Assume a fork pays nothing unless you can say, out loud, what *turned* because of it. A fork that pays for atmosphere teaches the player to fish for points instead of choosing a person to be.
2. **One attribute per answer, at most one size.** Two attributes in a single line of dialogue is a set-piece, not a conversation.
3. **A fork pays once, ever.** Anything reachable twice goes through `reward_attributes_once` with a unique flag (identifier form `answer_<scene>_<choice>`), and a conversation the player can walk back up to replays the stored answer rather than reopening the menu. See *Answering a person twice*, below.
4. **Each option must be a different kind of person.** If two options would be remembered identically, one of them is decoration and should be cut or rewritten.
5. **Order the options so the brave one is not last by default.** The player reads the first line as the natural answer.

**Answering a person twice.** Any conversation the player can walk back into is a slot machine unless the game latches the answer. `remembered_choice(person)` returns what he already said to that person, or `None` if the two of them are new to each other; the label then jumps straight to the stored answer instead of offering the menu a second time, and `remember_choice(person, answer)` latches a fresh pick. Answer A once and every later visit is A, until a scene is written specifically to let him ask again. This is wired into the four airport conversations, which are the ones a player can loop through at will.

An answer that is replayed this way is still *remembered* (§7.8) even though it pays nothing. Voice and memory are the point of a fork; the point is the exception.

### 5.5 Implemented answer map

Every point in the first act, as of the balance pass. Every one of these is a `reward_attributes_once` flag, so none of them can be earned twice. Use this table when rebalancing: the left column is what the player gets, and the right column is what it cost him.

| Flag | Where | Attribute | Size |
|---|---|---|---|
| `travel_route_attribute` | Act 1, the landing strip - take the train or take the taxi | Insight (train) / Nerve (taxi) | large |
| `answer_ticket_ask` | Act 2, the ticket machine - give up and ask a station attendant | Grace | large |
| `answer_wall_cat` | Act 3, the poster wall - the lost cat *(gated: Insight rank 2)* | Insight | small |
| `answer_circles_back` | Act 3, the circles desk - promise to come back *(gated: Grace rank 2)* | Grace | small |
| `answer_clock_ask` | Act 3, the professor - ask him to say the rule again *(gated: Nerve rank 2)* | Nerve | small |

**Reading the map.** The route decision is the act's one true turning point and is worth a full `large` (2.0), which is exactly rank 2, so a player who takes the train ends the act at Insight rank 2 and a player who takes the taxi ends it at Nerve rank 2. The three gated answers are not a source of points but the reward for already having them: each pays a token half point on top of the door it opened. The ticket attendant sits on the train side, so Grace and Nerve are the two attributes a single first act cannot both raise.

**Known consequence.** Because Grace only flows from the train side, a taxi player reaches the university with the Nerve door open and the Grace door shut. That is an intended cost of the route, not an oversight, but any rebalancing should keep exactly one full-rank source per attribute reachable on one route.

**Everything else pays nothing.** The station gate, the ticket machine's own menu, the platform signs, the boxes, the pool breakfast, the door, the walk to campus, the courtyard, the poster wall's other two answers, the circles desk's other two answers, and the professor's other two answers are all still forks, all still written as three different people, and all worth zero. They are recorded against the character (§7.8) rather than banked. The full list of the removed flags is in the git history for `game/script.rpy`.

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
| 1 | Developing | 0.0 |
| 2 | Emerging | 2.0 |
| 3 | Capable | 5.0 |
| 4 | Accomplished | 9.5 |
| 5 | Exceptional | 15.0 |

These are **cumulative totals, not points-per-rank**: rank 2 begins when the attribute has 2.0 points in it, in total, since the beginning of the game. Each step costs more than the last, so the early game moves quickly and the later game means something.

The thresholds, names, and reward sizes are configured in one place (`init python` in `game/script.rpy`, `attribute_rank_thresholds` and `attribute_rank_names`) and are never written into a scene.

### 6.3 Fractional accumulation

**Every point in the game is measured in halves, and most answers are worth none of them.** The smallest reward is half a point, so the ladder is a record of *accumulation* rather than of any one clever reply. A turning point is the deliberate exception: the route decision is worth a full rank, because it is the one fork in the act that changes what the act is.

Rewards are named rather than numbered, so the entire economy can be retuned from one dictionary without touching a line of dialogue:

| Size | Points | Used for |
|---|---|---|
| `small` | 0.5 | A token on top of a door that was already open; noticing something; a moment of nerve |
| `medium` | 1.0 | A real choice with a subject. Defined but currently unused - no site in the first act needs a middle size. |
| `large` | 2.0 | A turning point: a choice that changes what happens next, not just how it is said. Equal to the first rank, so it is used once per act at most. |

`add_attribute_points(attribute_id, amount, show)` accepts either a name or a raw number. **Names are always preferred in scene code.**

### 6.4 Displaying progress

Every gain is shown, including the smallest ones. Which of the two presentations is used is decided centrally by `add_attribute_points` so no scene ever has to think about it:

| Trigger | Presentation |
|---|---|
| A token gain inside a conversation (`show="auto"`) | **Tick chip.** A small `Insight +0.5` note that rides over the next couple of lines and hides itself. Costs the player no click and no pause. |
| A rank up, whatever the size | **Gain card**, always. |
| A turning point (`show="card"`) | **Gain card.** |
| Bookkeeping that is not a reward (`show=False`) | Nothing. |

**The tick chip** sits in the **top-right corner, below the orb cluster**, where it is out of the reading path and never covers the dialogue plate it is talking about. The old top-centre slot is now occupied by the character-memory notice (§7.8), so the two never collide: stats speak from the right, memory speaks from the centre.

**The gain card** is a full-screen moment: the point starts in the middle of the screen, the current rank is named, and the stat then travels out of the centre and eases into its own orb, where it pulses. It is preceded by a short hold so the choice has room to land, and it cannot be clicked through.

**The orbs** are the visual statement of the whole system. Each of the three circles is mostly transparent when empty and becomes progressively solid as points are gathered, measured against the **final** threshold, so an orb only ever gets more solid and never recedes when a rank is crossed. Rank is a label; solidity is the lifetime total. The Attributes page (below) additionally shows a bar scoped to the **current** rank, which is the only place the player sees the next-rank arithmetic.

**Two places to look at the state:**

- **HUD** — three small orbs, always on screen once the game begins, showing solidity at a glance without a number.
- **Attributes page** — reached from the in-game menu **or from the `Attributes` button in the bottom dock**, one row per attribute: name, rank, blurb, the current-rank bar, and the points to the next rank.

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
| Reading | `attribute_total`, `attribute_rank`, `attribute_rank_name`, `attribute_progress`, `attribute_orb_alpha`, `attribute_rank_next_text` |
| Gating | `has_attribute(attribute_id, minimum_rank)` |
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
"[tag_grace] Tell her you will be back." if has_attribute("grace", 2):
    ...
```

### 7.3 Gates are by rank, never by points

`has_attribute(attribute_id, minimum_rank)` compares the **rank**, not the raw total. A locked line therefore means *"he has not become that person yet"* rather than *"you are half a point short"*. That is the difference between a door and a toll booth, and it is the reason a half point earned twelve scenes ago can quietly open something now.

**Ranks are 1-based and start at 1, so `minimum_rank=2` is the first number that can actually close anything.** A gate of `1` is true from the first line of the game and is always a bug. Rank 2 is 2.0 points in that attribute.

### 7.4 No gates at the beginning

**The airport (Act 1), the journey home (Act 2) and the first day up to the walk to campus (Act 3) contain no locked answers at all.** The player has just started the game; the protagonist has no personality yet, so refusing him an answer would be refusing him a character he has not had the chance to build.

Gates begin inside the university sequence, at the end of the first day. Because points are now scarce, the door and the key arrive together: the route decision on the landing strip is worth a full rank, which is exactly what the three end-of-day gates ask for. A player who took the train walks into the university able to open the Insight door; a player who took the taxi walks in able to open the Nerve door; a player who took the train and asked the attendant can open the Grace door instead. Which doors are open on the first day is therefore a direct consequence of the one real decision in the act, which is the intended shape.

The first three gates are one per attribute, and each one is a different kind of door:

- **Insight** (poster wall) — asks him to have noticed a detail nobody pointed out.
- **Grace** (student relations) — asks him to have decided to be a person in front of a stranger.
- **Nerve** (the professor) — asks him to say the thing he would rather not say, and it is the only route to the scene's best outcome.

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
- **Memory is for people who matter.** Tag someone when losing them is a scene the story is going to spend; do not tag a stranger the protagonist will never see again. The characters tagged so far are **Hikari**, the **circles clerk**, and the **professor**.
- **Write the note as a plain fact, first person.** `remember("hikari", "asked what she saw in the courtyard, years ago")` - not "was kind", not "earned Grace". It is a log of what he did, not of what it was worth.
- **A replayed answer is still remembered, but only once.** A latched answer (§5.4) that the game plays back on a second visit must not log its memory again, so the notice does not repeat.
- **The name on screen is not the id.** The keys are lowercase ids; the notice reads from `memory_names` so it can say "Hikari" rather than "hikari", and anything untagged falls back to a capitalised id.

The notice is `screen memory_notice` plus the `memory_notice_appear` transform, and it takes the **top-centre** slot, which the stat tick chip has vacated (§6.4). Stats speak from the right, memory from the centre.

---

## 8. UI and Terminology

Use these names and descriptions consistently throughout the game.

| Attribute | Short description | UI identity |
|---|---|---|
| Insight | The power to understand | Observation, discovery, intellect |
| Grace | The power to connect | Empathy, communication, trust |
| Nerve | The power to act | Courage, resolve, initiative |

### UI writing rules

- Always use the canonical names: **Insight**, **Grace**, and **Nerve**.
- Use the same capitalization in menus, dialogue requirements, notifications, documentation, and code-facing identifiers where practical.
- Avoid switching between synonyms such as Wisdom, Intelligence, Charm, Charisma, Bravery, and Guts as if they were separate attributes.
- Synonyms may appear in ordinary dialogue, but they must not introduce new progression categories.
- Keep gain notifications short and unobtrusive.
- Do not reveal hidden narrative information through attribute labels unless explicitly intended.
- **Each attribute owns one colour, everywhere.** Insight is blue (`#5fb8ff`), Grace is green (`#77d98b`), Nerve is red (`#ff6b6b`). The same colour is used on the orb, the tick chip, the gain card, and the gated-answer tag, and the tag strings are generated from the colour table so they cannot drift. Colour is how the player tells three attributes apart at a glance without reading a word.
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
11. **Points are scarce.** Most forks pay nothing. A new reward must be justified as a turning point, not as a nice moment, and the justification belongs in a comment at the point of use.
12. **A fork never re-rolls.** Any conversation the player can walk back into latches its answer with `remember_choice` and replays it.

---

## 11. Future Design Decisions

The following details remain intentionally open until the broader game design supports a decision:

- Final numeric range and progression thresholds
- Final rank names
- Attribute icons and visual styling
- Exact point rewards for individual activities
- Whether progress is always visible or partly hidden
- Whether certain narrative branches require multiple attributes
- How attributes interact with endings and major story outcomes
- Whether any special scenes use attribute combinations rather than individual thresholds

The coding assistant may recommend solutions, but must not treat provisional examples in this document as finalized requirements.

The first act's award set itself is settled and listed in §5.5, but it is expected to be rebalanced as Acts 2 and 3 are written; the mechanics around it (§5.4 replay, §7.8 memory, §6.4 presentation) are the parts meant to stay fixed.

---

## 12. Final Design Statement

**Insight. Grace. Nerve.**

The protagonist grows by learning to understand the world, learning to connect with the people within it, and learning to act when circumstances make action difficult.

These three attributes form the foundation of Elsewhere's personal-development system.

Every implementation should preserve that purpose: the system exists to create meaningful choices, reflect the player's development, and connect everyday university life with the deeper mysteries of Elsewhere.
