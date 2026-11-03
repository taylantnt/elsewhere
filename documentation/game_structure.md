# Game Structure & Level Flow
**Document type:** Game Design Specification
**Covers:** The scenes and systems that exist in `game/script.rpy`
**Status:** As-implemented reference, kept in step with the script

> This document describes the game **as it is built**, not as it is imagined.
> Anything that exists only in `game_concept.md` is listed at the end under
> "Not yet in the script" so the two documents cannot be confused.

---

## 1. The Shape of the Game

Elsewhere is a psychological thriller visual novel wearing a slice-of-life coat.
A foreign exchange student lands at Narita, gets to his host family, and survives
his first day at a Japanese university — while the world quietly leaks.

### 1.1 How an act is measured

An act ends when something becomes **permanent**: a door that cannot be
re-opened, a person who cannot be un-met, a truth that cannot be put back.
Length is not the measure. A fortnight in which nothing is settled is still the
same act; a single afternoon in which everything is, is a new one.

The break between the prologue and Act 1 is therefore a night, not a landmark.
The prologue ends when he sleeps; Act 1 begins when he wakes up in a house that
is already his. The break between Act 1 and Act 2 is the night at the end of the
first free afternoon. The last bell is not the boundary — the day does not stop
when class does, and the first afternoon in which he is allowed to choose
something is still Act 1. Act 1 ends when that afternoon is spent and he is back
in the house, which is the first fact of the game that nothing can undo.

### 1.2 The acts

| Act | Title | What it covers | Ends on |
|-----|-------|----------------|---------|
| Prologue | The Arrival | The plane, Narita terminal, the travel decision, the journey home, the house, the first dream | Falling asleep on the first night |
| 1 | The First Day | Morning, breakfast, the walk to university, the first hour of class, the first free afternoon and the three ways to spend it | The night at the end of the first free afternoon |
| 2 | The Long Middle | The free-roam hub, the seven-visit confidant stories, the leak worsening | *not written* |
| 3 | The End | The revelation and the endings | *not written* |

The prologue and Act 1 are built end to end. Act 1 ends on the night of the first
free afternoon — every one of the three after-school routes closes the same way,
on `scene black` after he is home (§4.6). That is the clean stopping point for a
demo build; the free-roam hub in §5.7 is what comes next, and §7 lists what is
waiting behind it.

Act 2 is expected to be much the longest, because it is the act that holds
everybody else's stories rather than the protagonist's. Act 3 is the endgame and
the three endings (Escape / Blue Pill / Failure), designed in `game_concept.md`.

> The older numbering (Act 1 = the airport, Act 2 = the journey, Act 3 = the
> first day) is retired. Everything that was Act 1 and Act 2 is now the prologue,
> and everything that was Act 3 is now Act 1.

---

## 2. Prologue, Part One — The Arrival

### 2.1 The notices and the name (`label start`, `label prologue`)
- `start` is not the story. It runs the two unskippable notice pages
  (A Work of Fiction, Lasting Decisions), the confirmation, and the name entry loop.
- Opening pages use a borderless monochrome layout on pure black, separate
  from the 760 x 480 in-game guide windows in `game/notice_windows.rpy`.
  Neither layout is a phone page, and neither carries an ELSEWHERE header.
- New Game, Continue and Load fade out over 1.4 seconds, hold black for two
  seconds, then fade into the destination. Loads use `before_load` and
  `config.after_load_transition`, preserving the normal load confirmations.
- I Understand fades the opening text out over 1.4 seconds, holds black for
  two seconds, then fades the name page in over 1.4 seconds.
- Modal windows draw at z-order 180, above dialogue, the HUD and bottom controls,
  but below system confirmations. They block game-menu and rollback shortcuts.
- Dialogue, portraits, the attribute HUD and bottom controls are hidden while
  standalone windows or attribute gain cards are open, then restored afterward.
- Opening notices each last eight seconds, including their fades, and cannot
  be dismissed early. Guides close with Got It; name entry supports Begin or Enter.
- The name entry cannot be left blank; the loop re-opens until something is typed.
- Starting state: `money = 30000`, `inventory = ["phone"]`, `japanese_fluency = 0`.
- `prologue` is the plane. He talks over the engine, establishes the thirty
  thousand yen and the fact that it is nowhere near enough, and the very first
  hospital flash cuts in under the line "Test initiating...".
- **No attribute HUD until he is actually standing in the world** — the cluster
  appears at the top of `airport_arrival`, not during the notices.

### 2.2 The terminal (`label airport_arrival`, `label airport_exploration`)
- After "I'll check the map on my phone.", the illustrated handset rises and
  displays NO SIGNAL. It holds for 2.5 seconds and lowers automatically.
  Gameplay controls and dialogue are hidden during this modal interlude.
  The existing "...", "No signal.", and "So much for the map." lines follow.
- `airport_arrival` sets the scene, kills the phone (no reception), and opens
  the **exploration hub**.
- The hub is a loop. He can talk to everyone and look at everything, in any order,
  and the hub returns after each branch:

| Hub option | Label | Notes |
|------------|-------|-------|
| Ask the Security Guard | `talk_security` | Two officers share the post; which one answers depends on `security_index` |
| Ask the Timid Man | `talk_timid_man` | |
| Ask the Cheerful Woman | `talk_cheerful_woman` | |
| Ask the Information Desk | `talk_assistant` | Gives the pamphlet (`has_pamphlet`) |
| Ask the Veteran Assistant | `talk_veteran_assistant` | **Gated**: needs the pamphlet or all three of the others |
| Check the Information Boards | `check_boards` | Board text advances with `board_message_index` |
| Look at the Plants | `look_plants` | The plants get stranger each look (`plant_index`) |

- The veteran assistant is the one pre-existing story gate, and it is a
  *knowledge* gate rather than an attribute gate: he will only help someone who
  has already tried the other doors.

### 2.3 The travel decision (`label end_airport`, `label travel_choice`)
- Leaving the terminal is the first major attribute decision: the train awards
  **2.0 Insight**, the taxi **2.0 Nerve**. Selected airport replies can already
  award small gains, but this remains the larger route-defining event.
- Taxi and train are deliberately not equal: they are two different afternoons,
  and both settle into the same house at different hours.

---

## 3. Prologue, Part Two — The Journey Home

The route taken here changes almost everything downstream: which arrival scene
plays, which dream he has, and how much money he has left.

### 3.1 Taxi route (`label taxi_warning`, `label taxi_stand`)
- The taxi is fast, expensive, and easy. It foregrounds **Nerve** — talking to a
  driver in a language he does not have.
- The meter is the set piece: ¥500 base plus ¥100 increments, and he sits and
  learns the rhythm of it because there is nothing else to do.
- In `taxi_stand`, confirming the fare despite embarrassment awards **0.5 Nerve**.
  Thanking the driver or looking out of the window earns nothing.

### 3.2 Train route (`label train_station` → `train_gate_slam` → `train_ticket`
→ `ticket_machine` → `train_platform` → `train_board`)
- The train is slow, cheap, and hard. It is the route that makes him *use the
  city* instead of being carried through it.
- The gate slams (`gate.wav` + `gate_shake`) because he walks through it the
  wrong way. Walking through and buying a ticket both move him on and **neither
  pays** — the turnstile does not remember anything, so the fork decides how he
  meets the station rather than who he is becoming.
- The ticket machine is a reading puzzle — he matches the fare map against the
  pamphlet and gets it wrong anyway.
- Asking the station attendant resolves the ticket obstacle and awards
  **2.0 Grace**. Small empathetic dialogue gains are separate from this event.
- The platform is the express-versus-local fork. The local is **not** a mistake;
  it is the slower, more deliberate answer, and neither sign pays — the choice
  only decides which `home_arrival` opening he gets.
- The express sets `boarded_shinkansen = True`. The local sets `arrived_late = True`.
- Fares come out of the wallet through `spend_money()`, which is where the
  money hint fires for the first time.

---

## 4. Prologue Ends, Then Act 1 — Home and the First Day

Everything from §4.1 to §4.2 is the last of the prologue. **The act break is the
night:** §4.3 onwards is Act 1, the first act in which he is awake inside the
story rather than being carried through it.

### 4.1 Arrival at the house (`label home_arrival`)
- One label, three openings, chosen by the journey:
  - `travel_method == "taxi"` — he arrives early and the whole house is still up.
  - `boarded_shinkansen` — the express, a short walk, an almost dark neighbourhood.
  - otherwise (`arrived_late`) — the local, the mother alone, everyone else asleep.
- Hikari is asleep when he arrives, so the first meeting with her happens at
  breakfast. This is deliberate: he has been reading her emails for months and
  has never heard her voice.
- The boxes fork: tell her the apologising is not necessary (Grace), ask her
  straight out whether she is worried (Nerve), or watch how she carries hers
  (Insight).

### 4.2 The first dream (`label dream_sequence`)
- The first **memory-reconstruction mini-game** ("put the day back").
- A horror interlude built on `dream_static` and `hospital_flash`, with the audio
  slipping out of the world and the real room leaking through ("Keep the room at
  eighteen", "Six hours. He has been under six hours.").
- The branch is real: a taxi player dreams the taxi (a meter with no end), a
  train player dreams the train (stations repeating, nobody's pages turning).
- Travel-route cards must be put back in the right order. It **cannot be failed**;
  a correct pick restores with `memory_restore.wav`, a wrong pick is annotated by
  the narrator with `memory_deviation.wav`.
- Nothing in the dream is ever labelled as real. The doctor's and the assistant's
  lines are **blank narration** — no name box, no portrait — so the room has no
  face.

### 4.3 Morning (`label morning_call`, `label leaving_house`)
- At breakfast, Hikari mentions students asking about his arrival. He can ask
  what they know, ask about introductions, or explain how her emails helped.
  The last reply awards **0.5 Grace**; the other replies are neutral.
- `leaving_house` is the amado (the sliding shutter) and the two-door fork: ask
  how she can hear a mood in a door (Insight), or admit he heard nothing (Nerve).

### 4.4 The walk to school (`label school_morning`, `label campus_grounds`)
- `school_morning` is the front-door list — the rules he memorised on the plane
  and the ones he got wrong. Fork: ask what she did on her own first day (Grace),
  admit the list was wrong, or ask where to check room changes. These are neutral.
- In the courtyard, noticing buildings from different periods awards **0.5 Insight**.

### 4.5 The university (`label department_tour`, `label student_relations`,
`label first_class`)
- `department_tour` is the poster wall, and it holds the **first door in the game
  that can actually be shut** — gated on Insight rank 2, behind "the lost cat,
  whose tape has gone yellow".
- `student_relations` establishes the rules of the place and holds the **Grace
  gate**. The clerk covers:

  | Rule | Detail |
  |------|--------|
  | Student card (`gakuseishou`) | Needed for everything; keep it in the same pocket |
  | Attendance | Marked present / late / absent |
  | Three lates | Equal one absence |
  | Three absences | No sitting the final exam; you still attend, you simply get no mark |
  | Electives | Chosen in the first two weeks, on the system, first come first served |
  | Circles | Reading, language, photography, hiking, and others; nobody makes you join |

- The card the clerk slides across the counter is pocketed here as a real Bag
  item (`add_item("student_card")`). It is not usable; its description is only
  that he should always have it with him and that it gets discounts.
- At the close of `student_relations` Hikari leaves ahead of him, because she
  knows she has to be inside before the professor and only one of them can
  afford to be late.
- `first_class` is the lecture hall, the "on time is late" professor, and the
  **Nerve gate**. He arrives alone after the bell, finds the empty seat beside
  her, and is stopped before he reaches it; she pulls him down, and only he is
  addressed, because she was not late. The professor's lecture (a shrinking
  population, "it is arithmetic") is the thematic spine of the whole game stated
  out loud for the first time. All replies receive the attendance rule. The
  Nerve-gated reply requests review of the registration-related late mark.
  Afterwards Hikari acknowledges leaving without directions. Asking her to
  warn him next time awards **0.5 Nerve** without requiring an existing rank.
  It does not end the scene: she hands him the rest of the day and the fork opens
  (§4.6).

### 4.6 The first free afternoon (`label first_class` →
`after_school_walk_alone` / `after_school_run` / `after_school_photo_club`)
The first hour of the game that belongs to the player, and the boundary of Act 1.

- **The fork is three things he would say, not a list of places.** Hikari asks
  whether he has plans, and the three answers are *"I want to learn the way
  home."*, *"I'll come with you."* and *"I want to find the photography club."*
  No destination is named in the menu. The player picks a shape of afternoon and
  the script does the geography, so the map is not spoiled by the choice that
  opens it. What he picks is stored in `first_day_activity` and never shown.
- **The hint card comes after he has picked**, not before: `after_school_hint_shown`
  runs once, once the game has already taken him somewhere, so the explanation of
  what free afternoons are for arrives with something to look at. It says what an
  afternoon costs (one a day), that it is spent on a person or a place, and that
  the ones with something waiting will announce themselves — without naming a
  single location.
- **All three routes end the same way**: a walk home, `scene black`, the music
  down, `return`. Three different afternoons, one unchanged night. That is what
  makes this the act break rather than the last bell.
- **Only one afternoon route happens.** Within each route, selected answers
  award small gains. Ramen has Japanese recommendation and appreciation replies;
  the run has an empathetic silence choice plus **1.0 Nerve** for completion;
  photography has participation, observation, and practical-help replies.
- `after_school_walk_alone` — he cannot use the map without reception, gets
  lost, and finds the ramen shop, which is also the demonstration
  that the shop was always findable. Contains the **Chef's first visit** in full
  (`いらっしゃい` / `あいよ` / an unexpected broth / `どうぞ` / `うまい、だろ？`),
  spends 900 yen and sets `confidant_visits["chef"] = 1`.
  Three menus cover ordering, asking about the broth, and responding to the chef.
  Recommendation earns Nerve; Japanese appreciation earns Grace. Other replies
  earn nothing. The counter background returns before the chef's next line.
- `after_school_run` — the sister's arc, not a numbered confidant chain. He walks
  home with Hikari, and she does not go into the house: she walks past it and
  changes her shoes, because the run is her daily thing and he has been handed the
  one evening she has not accounted for. Three menus: the walk home, the moment
  she invites him, and the drink they share afterwards. Sets `first_run_started`,
  awards the Nerve, and logs a memory against Hikari. Written as far as the first
  night; the seven beats it opens are listed above the label and **are not
  written** (§7).
- `after_school_photo_club` — **Sim is not a student.** He is the photographer who
  comes into the university twice a week to guide **Circle**, the photography club,
  and he frames it as something he is *allowed* to do rather than something he does
  for anyone. He is written to a hard rule: **he never complains, never blames
  anybody, never gossips about anyone in the room, and always puts the other person
  first.** What he says about other people is to their credit; what he says about
  himself is always smaller than the truth; the warmest thing he says in the scene
  lands on the protagonist, not on himself. The circle is the school activity and
  the mentor is the visitor, which is what keeps his seven-visit farewell possible.
  The protagonist uses his phone to take and compare photographs.
  Five menus cover the doorway, camera availability, observing the first image,
  Sim's photography and the club's origins, and participating in the session.
  and the scene draws its lines from `Dialogue/Locations/Photography Club - Sim/1st
  interaction.md`. Sets `confidant_visits["sim"] = 1` and logs a memory.
  Selected replies earn Nerve for joining, Insight for reframing, or Grace for
  helping the model. Sitting through the meeting does not automatically pay.
- **The first visit is the whole of each confidant's presence in the script.**
  Nothing reads `confidant_visits` yet; the counter is written here so the hub has
  something true to read when it is wired up (§5.7).

---

## 5. Systems

The script is one file (`game/script.rpy`) organised as: core systems in `init`,
then the running story. Systems are documented in full in their own specs; this
is the index.

### 5.1 Character attributes — see `character_attributes.md`
- Three attributes: **Insight** (understand), **Grace** (connect), **Nerve** (act),
  each carrying its own colour — blue, green, red — on every circular meter, tick, card and tag.
- **Points are selective.** Small gains occur on concrete, thoughtful, observant,
  or courageous dialogue actions. Routine replies do not automatically pay.
  Larger events remain distinct from conversation rewards.
- Points are **fractional** (halves). Named sizes: `small` = 0.5, `medium` = 1.0
  (first-reading puzzle success and first run), `large` = 2.0. A `large` is exactly rank 2, so the route
  decision is the one answer in the act that moves a rank on its own.
- Presentation: a quiet **tick chip** in the top-right corner for an ordinary
  gain (`show="auto"`) and the full **gain card** for a rank-up or a turning point.
- The full-screen card uses fixed circle cells, outward ripples, and separately
  layered text. Qualitative ribbons are replaced by `RANK 02 / 05`.
  The phone page uses circular progress, concise descriptions, and totals.
- **Circular meters fill toward the next rank** — the three labeled rings begin
  empty and fill in colored segments as points accumulate; each ring resets when
  its rank advances.
- Every award goes through `reward_attributes_once` with a unique
  `answer_<scene>_<choice>` flag. A hub conversation also **latches its answer**
  with `remember_choice`, so re-entering it replays the stored reply instead of
  re-opening the menu — that latch, not the flag, is what stops the farming.
- **Important characters remember what he said.** `remember(who, note)` logs an
  answer against a character and shows a short `(Hikari will remember that)`
  notice at the top of the screen. Memory is not a reward; it is the record of
  what he did, and it is kept separately from what he is becoming.
- Gates are by **rank**, never by raw points, and **ranks are 1-based** — the
  first rank is 1, so `has_attribute(id, 2)` is the smallest gate that closes
  anything. A gate of `1` is always a bug.
- **The first day up to the walk to campus contains no locked answers.** The
  first three gates are one per attribute, and all three are in the university:
  Insight at the poster wall, Grace at student relations, Nerve in the lecture hall.
- See `character_attributes.md` §5.5 for the complete implemented reward map.

### 5.2 Language progression
- Japanese starts plain and turns coloured as fluency rises. The `{jp}` tag and
  the `language_tag` helper handle it; at `japanese_fluency >= 5` the text is
  `#87cefa`.
- Hiragana and katakana are used freely; Kanji only where the font group covers it.

### 5.3 Money and the Bag
- Money is the everyday resource: fares, food, a book from a stall. Starts at
  ¥30,000 and only ever goes down through `spend_money()`.
- The cash indicator is hidden from the main overlay and visible only in the Bag.
- The Bag is an RPG-style grid with a fixed description panel and per-item action
  verbs (`item_use_label(item)`, e.g. "Open" for the pamphlet).
- Two one-time hint cards explain the wallet and the bag the first time each is used.

### 5.4 Attendance
- Established in dialogue in `student_relations` and reinforced in `first_class`.
- **Not yet a tracked counter.** There is no `lates`/`absences` variable in the
  script today; the rule is narrated. When a class schedule exists, this is where
  the counter and the exam-disqualification flag belong.

### 5.5 The dream mini-game
- The memory-ordering board in `dream_sequence`. The player has three readings;
  an incorrect submitted order costs one reading and preserves the current board.
  Only solving it on the first reading awards Insight.
- Glitches are intentional and intense (`dream_static`: flashing bands and washes);
  while the memory board is active, the interference is softened so card text
  and ordering controls remain easy to read.
- The board separates the ordered sequence from available memories, labels
  remaining readings, and offers a clear review action when all four slots are filled.

### 5.6 Presentation
- **Portraits**: large, centred, anchored at `yalign 1.0`, `zoom 1.8`, with a
  "talking" animation driven off the global game clock so it never resets between
  lines.
- **Transitions**: `walk_fade = Fade(1.2, 0.3, 1.2)` for a change of location,
  `stair_fade = Fade(1.6, 0.6, 1.6)` for stairs. All transitions and timed pauses
  are unskippable by click (`_dismiss_pause = False`).
- **Placeholder backgrounds** print the name of the art they are waiting for in
  the middle of the screen, so a missing asset is obvious and never errors out.

### 5.7 Free roam, links and the hub
The rules that let the player loose among the confidants without the script
fanning out into unmanageable branches. The bookkeeping and the screen live in
`game/locations.rpy`.

- **A link feeds the attribute system, it does not run beside it.** A confidant's
  story is where a locked attribute door is worth opening: the link is the route,
  the attribute is the reward. This restates `game_concept.md` so the two cannot
  drift apart.
- **A link's story is told in seven visits**, one per outing
  (`Dialogue/Locations/overview.md`). After the seventh the story is over: the
  person leaves or the place shuts, and the row stops offering anything.
- **Growth is capped by act, not by time slots.** `act_confidant_cap` is the one
  dial. It says how much of anybody's story the current act allows, and a place
  that has caught up with it is **paused**: the person is still there and still
  talking, but nothing new about them happens until the story moves on. This is
  what stops a player from spending the whole game on one person, and it needs no
  scheduling system to enforce.
- **One scene per outing.** Picking a place spends the day, and the answer is
  latched with `remember_choice`, so the same visit cannot be farmed twice.
- **Links never move the spine.** The plot happens whether the player visits
  anybody or not. A missed outing costs content, never progression. That is the
  whole reason this is not hard branching: the hub fans out, and every branch
  falls back onto the same next scene. The only true forks are the few that
  settle an ending flag.
- **The hub** (`screen location_hub`) shares the standalone notice window.
  Each row spells out its state: Visit available, No new visit yet, or Story
  complete. Only available rows are clickable. The destination list scrolls;
  Head Home remains available in the fixed footer.
- **The hub screen is not used yet, and the first free afternoon does not use it.**
  The Act 1 fork is a hand-written three-way branch inside `first_class` (§4.6),
  because Hikari is asking the question and the answers are lines of dialogue
  rather than rows to click. `location_hub` exists for the point where the day is
  a standing offer rather than a scene — when it is wired up the shape is
  `call screen location_hub([...])`, then branch on `_return`, where `None` means
  the day was left unspent. It carries the destination status labels; the
  dialogue that opens it is written per scene.

---

## 6. State Written by the Story

| Variable | Set by | Effect |
|----------|--------|--------|
| `player_name` | name entry | Every line of his own; the name the family uses |
| `money` | `start`, `spend_money()` | The wallet |
| `inventory` | `start`, `add_item()` | The Bag |
| `japanese_fluency` | story | Colour and comprehension of Japanese |
| `travel_method` | `travel_choice` | Taxi vs train downstream (`home_arrival`, `dream_sequence`) |
| `boarded_shinkansen` | `train_platform` | Express vs local |
| `arrived_late` | train route | Which `home_arrival` opening plays |
| `has_pamphlet` | `talk_assistant` | Unlocks the veteran assistant; used by the ticket machine |
| `talked_to_security` / `talked_to_man1` / `talked_to_npc2` | airport hub | The veteran assistant's alternate unlock |
| `security_index` / `board_message_index` / `plant_index` | airport hub | Which variant of a repeated interaction you get |
| `character_attributes` | `add_attribute_points()` | The three attributes |
| `attribute_reward_flags` | `reward_attributes_once()` | Stops any answer from paying twice |
| `remembered_choices` | `remember_choice()` | The answer he already gave a person, so they replay it instead of re-rolling |
| `character_memories` | `remember()` | What an important character is holding onto |
| `memory_names` | `remember()` | How those people are named in the `(X will remember that)` notice |
| `show_attribute_hud` | `airport_arrival` | Whether the three labeled attribute meters are on screen |
| `money_hint_shown` / `pamphlet_hint_shown` / `after_school_hint_shown` | first use of each | One-time tutorial cards |
| `first_day_activity` | the Act 1 fork in `first_class` | Which shape of afternoon he picked (`walk_alone` / `walk_hikari` / `photo_club`); read immediately, never shown |
| `first_run_started` | `after_school_run` | The first river run happened. The run is not a confidant slot yet, so this is the only record of it |
| `current_act` | the story, at each act break | Which act's caps are in force (`act_confidant_cap`) |
| `confidant_visits` | `after_school_walk_alone` (chef), `after_school_photo_club` (sim) | How many of the seven visits each person has had; `destination_state()` and the hub read it, nothing else writes it yet |
| `sister_affection`, `sim_affection`, `orson_affection`, `chef_affection`, `aya_affection`, `hana_affection` | **nothing yet** | Declared placeholders for a confidant's *relationship quality*; no code reads or writes them. Note this is not the visit count, which is `confidant_visits` |

---

## 7. Not Yet in the Script

These exist in `game_concept.md` and in the character files, but there is **no
scene for them yet**. They are listed here so nobody goes looking for a label
that does not exist.

- **Act 2 and Act 3**: the long middle and the endgame. The revelation (the
  facility) and the three endings (Escape / Blue Pill / Failure) both live in
  Act 3.
- **The free-roam hub**: `screen location_hub` and its state marks exist (§5.7),
  but no scene opens it. The Act 1 fork (§4.6) is hand-written dialogue instead,
  and that is deliberate.
- **The confidant locations beyond their first visit.** The ramen shop (Chef)
  and the photography club (Sim) each have their **first** visit in the script
  (§4.6); the bar (Orson), the reading circle (Hana) and the maid cafe (Aya) have
  none. Every one of the five has a progression summary and seven written
  interactions under `Dialogue/Locations/`, and none of those outlines is in the
  script — including the six remaining visits for the two confidants who are.
- **The seven-visit run with Hikari.** `after_school_run` (§4.6) is written as far
  as the first night and sets `first_run_started`. The run becomes a recurring
  after-school activity rather than a seven-visit chain, and the shape of the
  seven beats is written as comments above the first one. **Nothing else in the
  documentation describes the run.** It is new content, not something waiting to
  be wired up, and the user has said they intend to write it themselves.
- **The photography club's camera.** The first visit is built around arriving with
  nothing to shoot (§4.6). The seven-interaction outline assumes a "beginner's
  camera" by the third visit, so the camera still has to be acquired somewhere
  between the first visit and the third.
- **The fortune teller, and the Akihabara / Harajuku mini-games.** The Level
  files for Akihabara and Harajuku are **empty**, so neither has anything written.
- **The candidate destinations** (`Dialogue/Levels/Levels overview.md`): Asakusa,
  Odaiba, Harajuku, Akihabara, Yokohama-Chinatown, school, home and room, the
  train, the station, and the airport.
- **A class schedule and the attendance counter**: see §5.4.
- **Real art** — anything still calling `placeholder_bg(...)` or
  `bg_or_placeholder(...)` prints its own name on screen until the asset arrives.
  The two Act 1 rooms that are still placeholders are the **ramen shop**
  (`bg_ramen.png`) and the **photography club room** (`bg_photo_club.png`); drop
  either file into `images/backgrounds/` and the picture takes over by itself.
  `screen photo_mode` also still references `images/ui/camera_frame.png`, which
  does not exist, so calling it would fail.
