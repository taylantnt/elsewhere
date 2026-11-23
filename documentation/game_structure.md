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

The break between Act 1 and Act 2 is the first dream and the night it ends.
Act 1 is the arrival — the plane, the terminal, the journey, the house, and
the first dream. Act 2 begins the next morning and is deliberately one big
act: it holds the opening school days, the first weekend, the hub, and every
confidant arc. Act 3 is the glitch era, when the leaks turn structural. Act 4
is the revelation and the endings.

### 1.2 The acts

| Act | Title | What it covers | Ends on |
|-----|-------|----------------|---------|
| 1 | The Arrival | The plane, Narita terminal, the travel decision, the journey home, the house, the first dream | The end of the first dream, where `morning_call` begins Act 2 |
| 2 | The Long Middle | The opening school days, the free-roam hub, the confidant stories, and the midterm | **Built** through Day 50, the firefly outing |
| 3 | The Glitch | Incident (Days 51-53), slow burn (Days 54-63), then investigation (Days 64-83) | **Playable through Day 83** |
| 4 | The End | Hikari's revelation at the river, the ending routes, and the coda (Days 84-90) | **Playable**; Days 84-89 are a montage, Day 90 is played |

Day 7 has a forced introduction; the free-roam hub first opens on Day 8.
After the midterm arc, Day 21 hands off to `act2_day_router`. The hub is
unavailable during Days 51-53, reopens for Days 54-63, and closes permanently
on Wednesday, June 10 (Day 64). Day 64 sets `current_act` to 3 and replaces
the free afternoon with a scripted river visit. Day 69 starts the written
investigation (Days 70-83), and Day 82 hands off to `act4_bridge`, which sets
`current_act = 4` for the Day 90 ending. See
[the day map](act2_day_map.md) for the playable sequence.

**Day file naming (Act 2 onward):** files in `game/days/` are named
`special_day_NN_slug.rpy` for hand-written set pieces and `common_day_NN`
labels inside `common_days.rpy` for routine hub days. Every day ends with
`jump act2_day_router` once the shared router takes over; it maps `story_day` to the next day's label,
so inserting or filling a day never requires editing the previous one.

> The older numbering (Act 1 = the airport, Act 2 = the journey, Act 3 = the
> first day) is retired, and so is the intermediate numbering that made the
> first day "Act 1". Under the current map Act 1 is only the arrival; Act 2
> begins at `morning_call`, which is where `current_act` becomes 2.

---

## 2. Act 1, Part One — The Arrival

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
  hospital flash cuts in under the line "...signal holding. Bring him in."
- The monologue leaves the application and acceptance concrete, but not the
  reason for Japan or the departure: he remembers packing a bag, not the day he
  decided to leave home, and the last ordinary day before the flight feels detached.
  These gaps stay framed as jet lag and nerves until the dream reinterprets them.
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
| Check the Information Desk | `talk_assistant` | Empty with a BACK SOON sign until all three others are approached; the assistant returns, then gives the pamphlet |
| Ask the Veteran Assistant | `talk_veteran_assistant` | **Gated**: needs the pamphlet or all three of the others |
| Check the Information Boards | `check_boards` | Board text advances with `board_message_index` |
| Look at the Plants | `look_plants` | The plants get stranger each look (`plant_index`) |

- The Information Desk is a signpost, not a destination the player is meant to
  find first. Before all three others are approached, it is an empty desk with a
  `BACK SOON` sign; the protagonist can ask around the hub instead. Once the
  guard, timid man and cheerful woman have all been approached, the assistant
  returns and the pamphlet exchange can begin.
- The Information Desk and the veteran assistant are *knowledge* gates rather
  than attribute gates. The desk only helps once the security guard, the timid
  man and the cheerful woman have all been approached; the veteran then needs
  the pamphlet the desk gives him.

### 2.3 The travel decision (`label end_airport`, `label travel_choice`)
- Leaving the terminal is the first major attribute decision: the train awards
  **0.5 Insight**, the taxi **1.0 Nerve**. Selected airport replies can also
  award small, once-only gains.
- Taxi and train are deliberately not equal: they are two different afternoons,
  and both settle into the same house at different hours.

---

## 3. Act 1, Part Two — The Journey Home

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
  wrong way. Walking through earns **0.3 Nerve** (`nudge`); buying a ticket is
  neutral.
- The ticket machine is a reading puzzle — he matches the fare map against the
  pamphlet and gets it wrong anyway.
- Asking the station attendant resolves the ticket obstacle and awards
  **0.2 Grace**.
- The platform is the express-versus-local fork. The local is **not** a mistake;
  it is the slower, more deliberate answer. The express earns **0.2 Insight**;
  the choice also decides which `home_arrival` opening he gets.
- The express sets `boarded_shinkansen = True`. The local sets `arrived_late = True`.
- Fares come out of the wallet through `spend_money()`, which is where the
  money hint fires for the first time.

---

## 4. Act 1 Ends, Act 2 Begins — Home, the First Day, the Second Day

Everything from §4.1 to §4.2 is the end of Act 1. **The act break is the first
dream and the night it ends:** `morning_call` sets `current_act = 2`, and
§4.3 onwards is Act 2 — the long middle that holds every confidant arc.

### 4.1 Arrival at the house (`label home_arrival`)
- One label, three openings, chosen by the journey:
  - `travel_method == "taxi"` — he arrives early and the whole house is still up.
  - `boarded_shinkansen` — the express, a short walk, an almost dark neighbourhood.
  - otherwise (`arrived_late`) — the local, the mother alone, everyone else asleep.
- Hikari is asleep when he arrives, so the first meeting with her happens at
  breakfast. This is deliberate: he has been reading her emails for months and
  has never heard her voice.
- The boxes fork: acknowledge what she has already done (Grace), ask which boxes
  go upstairs (neutral), or ask to leave the heavy books until morning (a small
  Grace loss).

### 4.2 The first dream (`label dream_first_night`)
- The first dream is the narrative horror interlude; the memory-ordering board is
  archived separately and is no longer part of the story path.
- A horror interlude built on `dream_static` and `hospital_flash`, with the audio
  slipping out of the world and the real room leaking through ("Keep the room at
  eighteen", "Six hours. He has been under six hours.").
- The branch is real: a taxi player dreams the taxi (a meter with no end), a
  train player dreams the train (stations repeating, nobody's pages turning).
- The day is now attempted through narrative rather than a board. The archived
  board still exists as `dream_put_the_day_back`, but it is no longer called by
  the main story.
- Nothing in the dream is ever labelled as real. The doctor's and the assistant's
  lines are **blank narration** — no name box, no portrait — so the room has no
  face.

**Dreams are not lab scenes.** Since Act 3, the player also sees short scenes
outside the simulation in `act3_investigation.rpy`. Those scenes are marked with
`centered "OUTSIDE THE SIMULATION"`, use third person, and give the Doctor and
the older Hikari portraits. The protagonist never sees them and never refers to
them. Dreams stay first person, inside the world, and faceless. Do not merge the
two conventions: the marker is the player's only way to tell which layer they
are in. See [act3_investigation.md](act3_investigation.md).

### 4.3 Morning (`label morning_call`, `label leaving_house`)
- At breakfast, Hikari mentions students asking about his arrival. He can ask
  what they know (a **0.2 Nerve loss**), ask about introductions (neutral), or
  explain how her emails helped (**0.5 Grace**).
- `leaving_house` is the amado (the sliding shutter) and the two-door fork: ask
  how she can hear a mood in a door, or admit he heard nothing. Both are neutral
  and both are remembered.
- The genkan beat ends with Hikari admitting she put WIRE on his phone before he
  landed (`wire_unlock("hikari")`). The river run later uses the app for her
  private message instead of adding her.

### 4.4 The walk to school (`label school_morning`, `label campus_grounds`)
- `school_morning` is the front-door list — the rules he memorised on the plane
  and the ones he got wrong. Fork: ask what she did on her own first day, admit
  the list was wrong, or ask where to check room changes. All three are neutral
  and all three are remembered.
- In the courtyard, noticing buildings from different periods awards **0.2 Insight**.

### 4.5 The university (`label department_tour`, `label student_relations`,
`label first_class`)
- `department_tour` is the poster wall, and it holds the **first door in the game
  that can actually be shut** — gated on 0.8 Insight points, behind "the lost
  cat, whose tape has gone yellow". The gated reply pays 0.2 Insight.
- `student_relations` establishes the rules of the place and holds the **Grace
  gate**, which requires 1.0 Grace point; the gated reply pays 0.2 Grace. The
  professor's dialogue offers a Nerve-gated option at 0.3 points. The clerk
  covers:

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
  Nerve-gated reply requests review of the registration-related late mark, and
  costs 0.2 Grace. Afterwards Hikari acknowledges leaving without directions.
  Asking her to
  warn him next time awards **0.5 Nerve** and costs **0.2 Grace**, without
  requiring an existing rank. It does not end the scene: she hands him the rest
  of the day and the fork opens (§4.6).

### 4.6 The first free afternoon (`label first_class` →
`after_school_walk_alone` / `after_school_run` / `after_school_photo_club`)
The first hour of the game that belongs to the player, and the first afternoon
of Act 2.

- **The fork is three things he would say, not a list of places.** Hikari asks
  whether he has plans, and the three answers are *"I want to learn the way
  home."*, *"I'll come with you."* and *"I want to find the photography club."*
  No destination is named in the menu. The player picks a shape of afternoon and
  the script does the geography, so the map is not spoiled by the choice that
  opens it. What he picks is stored in `first_day_activity` and never shown.
- **The hint card comes before he has picked**: `after_school_hint_shown`
  runs once, just before the menu, so the explanation of what free afternoons
  are for arrives while the choice is still his to make. It says what an
  afternoon costs (one a day), that it is spent on a person or a place, and that
  the ones with something waiting will announce themselves — without naming a
  single location.
- **All three routes converge on the same night**: a walk home, then
  `first_evening_dinner`, then `end_of_first_day`. Three different afternoons,
  one unchanged evening. None of them returns to the hub.
- **Only one afternoon route happens.** Within each route, selected answers
  award small gains. Ramen pays one attribute per menu choice (mostly micro,
  with an Insight nudge for the broth question); the run has an empathetic
  silence choice plus **0.5 Nerve** for completion; photography has
  participation, observation, and practical-help replies.
- `after_school_walk_alone` — he cannot use the map without reception, gets
  lost, and finds the ramen shop, which is also the demonstration
  that the shop was always findable. Contains the **Chef's first visit** in full
  (`いらっしゃい` / `あいよ` / an unexpected broth / `どうぞ` / `うまい、だろ？`),
  spends 900 yen and sets `confidant_visits["chef"] = 1`.
  Three menus cover ordering, asking about the broth, and responding to the chef.
  Ordering pays Nerve, Insight or Grace by approach; the broth question pays
  Insight, 「うまい」 meaning pays Insight, and thanking him pays Grace. Asking
  about the smoky flavour or pointing at the bottle pays nothing. The route then
  closes with an Insight award for finding the shop. The counter background
  returns before the chef's next line. The same first visit also exists as a
  standalone `chef_visit_01` in `game/confidant_visits/chef.rpy` for runs that
  skipped this route, and both are playable in the Chef arc replay.
- `after_school_run` — the sister's arc, not a numbered confidant chain. He walks
  home with Hikari, and she does not go into the house: she walks past it and
  changes her shoes, because the run is her daily thing and he has been handed the
  one evening she has not accounted for. Three menus: the walk home, the moment
  she invites him, and the drink they share afterwards. Sets `hikari_visits = 1`,
  awards the Nerve, and logs a memory against Hikari.
  The other six runs are written in `game/confidant_visits/hikari.rpy` and routed through
  `confidant_visit_hikari` (§5.7); visit 2 is reachable from the Day 7 hub.
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
  Four menus cover the doorway, observing the first image, Sim's photography and
  the club's origins, and participating in the session; the camera-availability
  menu was retired when the scene became narration-only.
  and the scene draws its lines from `documentation/Locations/Photography Club - Sim/1st
  interaction.md`. Sets `confidant_visits["sim"] = 1` and logs a memory.
  Selected replies earn Nerve for joining, Insight for reframing, or Grace for
  helping the model; finishing the first session closes the route with a further
  Grace award.
- `first_evening_dinner` closes every route. On the walk-alone route only, he
  is genuinely still full from the ramen, so the table gets one extra choice
  before the usual natto menu: **be honest** ("I'm still full") or **cover it**
  ("I'm starving"). Honest costs a little Grace (`first_dinner_declined`,
  `declined_dinner = True`) — Hikari names the shop, Tetsuo is disappointed but
  says it can't be helped because they couldn't communicate, and he explains
  the dinner-time rule; covering pays Grace and his regard. `second_morning`
  breakfast reads `declined_dinner` so father, mother and Hikari follow up on
  whichever happened.
- **Every confidant's current script presence is their first visit.**
  `confidant_visits` is written by the first-visit scenes — Chef on the
  walk-alone route, Sim on the photography route, Aya at the day-two maid cafe
  (§4.7), and Hana and Orson on Saturday (§4.8). WIRE reads it for contact
  progress, and `destination_state()` reads it for the hub (§5.7). The same
  scenes write the affection values: `chef_affection`, `sim_affection`,
  `aya_affection`, `hana_affection`, and `orson_affection` all have a written
  first increment.

### 4.7 The second day (`label first_night_memory`, `label second_morning`,
`label second_school_day`)

The first day that belongs to him, and the template for every day after it.

- `first_night_memory` runs between the days: the day-memory matching board
  (a 4×3 board, six pairs, from `build_first_day_memory_deck`, five wrong turns allowed,
  a win within three pays 0.3 Insight once). It is the night that closes day one.
  The faces are the commissioned tarot-style deck in `game/images/cards/`; each
  pair draws from that memory's own set of cards, so a replay can deal different
  art without changing which six memories the board is about.
- `second_morning` is breakfast at the house — the WIRE/phone-plan argument
  with Tetsuo, conditional on `first_day_activity` — and hands off to
  `second_school_day`.
- `second_school_day` is the full rhythm: walk to campus, the **haiku lecture**
  (kigo = the seasonal word; three study-method choices paying Insight/Nerve),
  then Akihabara with Hikari for the **cellular plan** at Hamada Denki
  (`cellular_data_active` flips on, WIRE gets signal, and the day-one message
  queue finally delivers — chef advert, Sim welcome, or Hikari's river text,
  with a test reply on her route), Hikari leaves for
  Shibuya, and the afternoon is free exploration ending in the **maid cafe** —
  Aya's first visit, scripted in full: rules and pricing, omurice with the
  ketchup cat, the moe moe kyun spell, the WIRE card (`confidant_visits["aya"] = 1`,
  `wire_unlock("aya")`), and the walk back to the station.
- The scene ends on the train home. Leaving the cafe he texts Hikari through
  the new **Messages** app (`run_chat`, §5.8), and on the train her "did you
  find the station?" exchange — including the notebook-cat photo and a
  three-way reply choice — plays out as real texts.
- The night that closes day two is now written: the family kitchen table, the
  food detail, the dinner-boundary beats, Tetsuo's station-writing lesson, the
  quiz/library seed, Hikari steering him to the library, the solo reflection,
  and sleep.
- After that, `label night_room_visit` runs as part of the normal night
  sequence (the debug key `0` jumps straight to it): Hikari comes into his room
  instead of leaving and lays out the
  exam timeline — quiz next week, midterms in three or four. She gives the
  exact library directions (third floor, east wing, past the vending machines,
  left at the noticeboard with the taped corner, door with no sign) and a
  three-option menu for how he takes it; each reply is remembered and pays a
  small once-only reward.
- That night routes through `dream_router` with `dream_key = "day_two_cellular_maid"`
  and reaches the day-two dream placeholder in `game/dreams.rpy`, which now
  jumps to `saturday_off` (§4.8) rather than straight to `end_of_build`.

### 4.8 The weekend (`label saturday_off` → `home_sukiyaki` → `sunday_morning`)

The day after the dream — the off day the exam talk pointed at. Written as one
continuous Saturday: morning, library, the walk home, and the night meal.

- `saturday_off` — wake-up, a normal breakfast (sukiyaki is only mentioned as
  *tonight's* plan — father has supposedly been planning it since Thursday),
  Hikari's route-check reprise and her "I'm telling Dad you ran away" threat.
  Friday's plan is already settled — Hikari steered him to the library — so
  Saturday opens on that errand.
- `library_search` — he cannot find the door Hikari described. A three-option
  menu (ask the student by the window / follow the green-tea smell / check the
  floor directory) — all three converge on the same unlabeled door.
- `reading_club_first` — the errand pays off: the haiku study sheets from the
  course reserve (`library_errand_available` clears, Insight micro). Then
  **Hana's first interaction**, written from
  `documentation/Locations/Reading Club - Hana/1st interaction.md`: the two
  rules, the pick-a-book menu, the girl shelving returns, the eye contact, the
  flee, the book she leaves on his table, and the return attempt that makes her
  drop it — with a handmade WIRE card sliding out. He keeps the book. Sets
  Hana's visit count to at least 1, increments `hana_affection`, logs a memory,
  unlocks her WIRE contact from the card, and pays a Grace micro.
- Messages interlude — `run_chat("hikari", ...)` on the way out: "You alive?",
  the sukiyaki photo beat, and the "come straight home" energy.
- He takes the long way anyway and finds **Lupin's Den** — Orson's first
  interaction, written from `documentation/Locations/Bar - Orson/1st
  interaction.md`: the lost approach and wolf-signed door, the accidental step
  inside, the masked regulars, the un-ordered water, the fluent-English
  reassurance, the two-choice beat, "You found us. Most people don't.", the
  wooden note bowl, and the counter WIRE card he scans on the way home. Sets
  Orson's visit count to at least 1, increments `orson_affection`, logs a
  memory, unlocks his WIRE contact, and pays a Nerve micro.
- `home_sukiyaki` — the night meal: Mother explains sukiyaki properly ("what
  you make when the people you want to feed are the ones coming home"), and
  the family clocks that he found a bar. Before bed, Tetsuo drives everyone
  to Honki! for pudding. The trip introduces the shop, marks it on the
  phone map, and unlocks the station branch for later hub afternoons.

### 4.9 Sunday and Monday (`label sunday_morning` → `monday_morning` → `monday_lecture` → `tuesday_morning`)

The two days after the Saturday sequence. `home_sukiyaki` jumps to
`sunday_morning` instead of `end_of_build`.

- `sunday_morning` — the quiet day. Hikari collects on the Friday-night study
  plan with a three-question practice quiz off the haiku handout (menu-style,
  not `quiz.rpy`): kigo definition, what 5-7-5 counts, and the three-absences
  rule as the trick question. `sunday_quiz_score` drives her reaction and a
  sister affection bump; `sunday_q1_correct`–`sunday_q3_correct` let her name
  the actual miss, and each correct answer pays an Insight micro. The
  afternoon is a WIRE beat — four or five contacts depending on the first-day
  route, with Hana and Orson each showing one tick and one memory. Dinner,
  night, straight into Monday (no dream).
- `monday_morning` / `monday_lecture` — the first full school day. The haiku
  lecture runs the exam-preview material (old pond / frog as the kigo example)
  and the real quiz lands as three menu questions scored into
  `monday_quiz_score`, with `monday_q1_correct`–`monday_q3_correct` recording
  the misses. The afternoon is the second-confidant fork: it reads
  `first_day_activity` and pushes toward the confidant the player has not met
  yet. Sim-first offers the wrong train line toward the ramen shop, a Hikari
  WIRE chat that becomes the first run, or a combini errand that still gets him
  lost at the ramen shop; chef-first has Hikari call him home for the first run;
  Hikari-first walks home alone through three routes that all reach the ramen
  shop. Dinner then forks: the ramen route gets the still-full confess/cover
  choice, while the river run leaves both of them starving. Then night,
  `tuesday_morning`.

### 4.10 The forced second-confidant day (`label tuesday_morning` → `label tuesday_lecture` → forced visit → evening → night → `wednesday_morning`)

Tuesday, April 14 (Day 7) closes the first-week introductions. `monday_morning`
ends on `jump tuesday_morning`; the afternoon no longer opens the hub. Instead
`tuesday_lecture` checks which of Sim, Chef, or Hikari's first run is still
unmet and forces that meeting: Sim gets a special Tuesday campus session because
Thursday's Circle meeting is already gone, Chef gets a broth-smell lead-in to
`chef_visit_01`, and Hikari gets a WIRE "come home" into `hikari_first_run`.
`free_afternoon` begins on Day 8.

- `tuesday_morning` — breakfast with the family, the midterm briefing, Hikari's
  walk to the gate. Three breakfast options, one per attribute at Insight micro,
  Grace micro, and Nerve micro. The morning ends at the gate; `tuesday_lecture`
  follows.
- `tuesday_lecture` — the haiku lecture on the interval `間` and the load-bearing
  pause. Three options, one per attribute at micro: the pause is load-bearing
  (Insight), asking whether a poem can have too much space (Nerve), sliding the
  handout to the student behind (Grace). After the bell it routes to
  `day7_sim_campus`, `day7_missing_chef`, or `day7_missing_hikari` by which
  confidant is still at zero visits, then falls through to the shared evening.
- Evening / night — dinner reads `last_afternoon_place` (`sim` / `chef` /
  `walk_hikari` + `last_afternoon_was_run`), then the study desk and the first
  quiet night of the week. If Hikari came home with him, they arrive together
  and she says "we're late" and shoulders the blame herself; on every other
  route she was already at the table with the family. Three night options, one
  per attribute at micro: reading the kigo list aloud (Insight), asking about
  Hikari's seminar (Grace), admitting fear of the midterm (Nerve). The night
  ends on the dream beat and into `wednesday_morning`.

The two walks are generic hub rows for the days after this one: they are always
open rows, they pay once per answered question, and each pays one attribute per
option at micro size. `walk_hikari` is Grace / Insight / Nerve, `walk_alone` is
Insight / Grace / Nerve — the same three-attribute spread. On a day when
Hikari's run chain has a run waiting, `walk_hikari` plays that run instead
(§5.7); before the first run it plays the shorter `hikari_first_run` fallback,
and the generic walk is the fallback once the chain is finished.

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
- Points use tenths or halves. Common named sizes: `tiny` = 0.1, `micro` = 0.2,
  `nudge` = 0.3, `small` = 0.5, `medium` = 1.0 (first-reading puzzle success),
  `large` = 2.0 (reserved for future set pieces). Many dialogue rewards use
  smaller explicit amounts. Signed changes are clamped between 0 and 15 points.
- Presentation: a quiet **tick chip** in the top-right corner for an ordinary
  adjustment (`show="auto"`) and the full **gain card** for a rank change or a
  turning point.
- The full-screen card uses fixed circle cells, outward ripples, and separately
  layered text. Qualitative ribbons are replaced by `RANK 02 / 05`.
  The phone page uses circular progress, concise descriptions, and totals.
- **Circular meters fill toward the next rank** — the three labeled rings begin
  empty and fill in colored segments as points accumulate; each ring resets when
  its rank advances.
- Every award goes through `reward_attributes_once` with a unique
  `answer_<scene>_<choice>` flag. A repeatable airport conversation also
  **latches its answer** with `remember_choice`, so re-entering it replays the
  stored reply instead of re-opening the menu — that latch, not the flag, is what
  stops the farming.
- **Important characters remember what he said.** `remember(who, note)` logs an
  answer against a character and shows a short `(Hikari will remember that)`
  notice at the top of the screen. Memory is not a reward; it is the record of
  what he did, and it is kept separately from what he is becoming.
- The early gates use **raw points** through `has_attribute_points`: 0.8 Insight
  at the poster wall, 1.0 Grace at student relations, and 0.3 Nerve in the
  lecture hall. Rank gates remain available for later, larger doors, and
  **ranks are 1-based** — the first rank is 1, so `has_attribute(id, 2)` is the
  smallest rank gate that closes anything. A rank gate of `1` is always a bug.
- **The first day up to the walk to campus contains no attribute-locked
  answers.** The first three gates are one per attribute, and all three are in
  the university:
  Insight at the poster wall, Grace at student relations, Nerve in the lecture hall.
- See `character_attributes.md` §5.5 for the complete implemented reward map.

### 5.2 Language progression
- Japanese starts plain and turns coloured as fluency rises. The `{jp}` tag and
  the `language_tag` helper handle it; at `japanese_fluency >= 5` the text is
  `#87cefa`.
- Murakami's Japanese elective raises `japanese_fluency` by 1 per lesson,
  capped at 5: Days 10–17 in `game/days/` (fair, Jimbocho, old city, week two,
  sound words) plus every office-hours visit in
  `game/confidant_visits/murakami.rpy`. Day 10 is only the meeting; the choice
  to enroll is the player's, on the night of Day 12 (`murakami_enrolled`),
  with Murakami's daily ping offering a retry if he waits.
- Hiragana and katakana are used freely; Kanji only where the font group covers it.
- **The font has holes.** Kanji come from Kiwi Maru and everything else from
  mini-wakuwaku-maru (`game/gui.rpy`). Both accept a character they have no
  glyph for and Ren'Py then draws nothing, so the character silently vanishes
  from the line instead of showing a box. Macrons are the usual casualty
  (`ō`, `ū`, `ā`, `ē`, `ī`) along with `—`, `·`, `¥`, `é`, `•` and most dingbat
  or geometric symbols. Romaji follows the author's plain convention instead:
  `Bashou`, `Sensou-ji`, `Taishou`, `roumaji`, `nomihoudai`. For punctuation use
  what the font has: `・` (katakana middle dot) for a separator, `￥` for yen.
  Avoid dashes entirely, since `—` renders blank; use a colon where one fits,
  or rephrase the line.
- A screen that genuinely needs one of the missing symbols can pin its own font
  (`font "DejaVuSans.ttf"` / `text_font "DejaVuSans.ttf"`), which is how the
  chevrons, skip triangle, overflow dots and minigame symbols are drawn.
- **DejaVu Sans is the mirror image of the game font.** It has `·`, `¥`, `•`
  and `—`, but no `・` or `￥`, and it draws a tofu box (□) for a missing glyph
  rather than nothing. So never pin bare DejaVu Sans on an element that shows
  the game's `・` or `￥` — the HUD date chip and the memory-screen eyebrow used
  to do exactly that and rendered boxes. Those screens use the `ui_font`
  group from `game/gui.rpy` instead: DejaVu Sans for Latin (0x20–0x024f), Kiwi
  Maru for everything else. It keeps the same clean look on ASCII labels while
  covering the punctuation. `guide_font` (notice windows) and `menu_phone_font`
  (phone UI) are the same two-font pattern.
- `python3 tools/check_fonts.py` scans every `.rpy` file for characters that
  would render blank and prints the file and line. It reads the FontGroup rules
  out of `game/gui.rpy`, skips comments, and honours per-element font overrides
  and a `# check_fonts: pinned` marker. Run it after adding any line of text.

### 5.3 Money and the Bag
- Money is the everyday resource: fares, food, a book from a stall. Starts at
  ¥30,000. `spend_money()` handles chosen purchases; `pay_transit()` silently
  removes ¥700 every day from Day 2 onward in the shared `day_transition` label.
- The wallet has a sustain floor of ¥5,000, not a fail state. Below it, paid
  outings drop out of the hub and the one-time line is "I don't have enough to
  get by the day. I should take that shift." Work and the free walks stay open.
  With ¥4,800 a shift and the job unlocked on Day 8, even a taxi arrival (¥17,600
  on Day 1) still has ¥7,500 on Day 8; the floor cannot fire before the job
  exists. A frugal train arrival first feels it around Day 35.
- The cash indicator is hidden from the main overlay and visible only in the Bag.
- The Bag is an RPG-style grid with a fixed description panel and per-item action
  verbs (`item_use_label(item)`, e.g. "Open" for the pamphlet).
- Two one-time hint cards explain the wallet and the bag the first time each is used.

### 5.4 Attendance
- Established in dialogue in `student_relations` and reinforced in `first_class`.
- **Not yet a tracked counter.** There is no `lates`/`absences` variable in the
  script today; the rule is narrated. When a class schedule exists, this is where
  the counter and the exam-disqualification flag belong.

### 5.5 The dream mini-game (archived)
- The memory-ordering board is implemented as `dream_put_the_day_back` in
  `game/dream_archive.rpy`; it is no longer on the story's active path. The
  player has three readings;
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
- **A link's story is told in seven numbered visits**, one per outing
  (`documentation/Locations/overview.md`). The seventh is the farewell. Every
  one of the five then keeps an eighth **epilogue** visit: the place is still on
  the hub, the same closing scene replays every time, and the row reads
  **Epilogue** rather than **Complete**. The epilogue bypasses the act cap and
  the weekly schedule, because the place is no longer keeping hours for anyone.
- **Growth is capped by act, not by time slots.** `act_confidant_cap` is the one
  dial. It says how much of anybody's story the current act allows, and a place
  that has caught up with it is **paused**: the person is still there and still
  talking, but nothing new about them happens until the story moves on. This is
  what stops a player from spending the whole game on one person. Weekly opening
  hours are a separate system (§5.9): the act cap is story progress, the hours
  are whether the door is open today.
- **Introductions come before revisits.** A place with zero visits is always
  available (within the act cap). A place already visited stays closed to new
  visits until *every* confidant has been met at least once. The hub shows that
  as **No new**, not as a separate "Later" label, so the list never hints at a
  cast the player has not met. `all_confidants_met()` in `locations.rpy` is the
  check. This keeps the first week of Act 2 a tour of the city rather than a
  single friendship.
- **One scene per outing.** Picking a place spends the day. The current
  `free_afternoon` stub routes to the visit labels and returns; the
  `remember_choice` latch belongs to the real day loop when it is written.
- **Links never move the spine.** The plot happens whether the player visits
  anybody or not. A missed outing costs content, never progression. That is the
  whole reason this is not hard branching: the hub fans out, and every branch
  falls back onto the same next scene. The only true forks are the few that
  settle an ending flag.
- **The hub** (`screen location_hub`) shares the standalone notice window and
  puts the scrollable destination list on the left with the map on the right.
  Every destination is a pin on a stylised Tokyo map, coloured by state: gold
  for New, blue-grey for No new, dark grey for Closed, muted tan for Epilogue,
  near-black for Complete. A compact legend under the map explains the colours.
  The word New blinks on a live row, so the eye finds the open destinations
  without reading every line. A row held by the introduction gate is shown as
  No new, not as a separate Later label, because naming that state would hint at
  a cast the player has not met yet. Hovering a pin or a row shows its name and
  full status in the map header and the strip beneath it, and lights the
  matching row or pin on the other side. Clicking a ready or epilogue pin or row
  picks it. The list spells the same thing out in words, so a map is never the
  only way to read the menu. Only ready and epilogue pins and rows are
  clickable; Head Home remains available in the fixed footer. The eyebrow
  carries the current in-game date.
- **The hub is wired and reached.** `label free_afternoon` (end of
  `script.rpy`) calls the screen and jumps to `confidant_visit_<place>`; the
  five confidant visit labels are written scenes, and the two walks
  (`afternoon_walk_hikari`, `afternoon_walk_alone`) are new generic rows. A
  day scene `call`s it after lunch; `None` from the screen means the
  afternoon was left unspent and the day continues. The first-afternoon fork
  (§4.6) stays hand-written dialogue because Hikari is asking the question
  there — that is deliberate, not an oversight. The hub opens on Day 9; Day 8
  (`wednesday_morning`) is a linear day whose afternoon is the combini
  discovery, Day 7 (`tuesday_morning` → `tuesday_lecture`) is forced to the
  last first-week confidant before `free_afternoon` begins, and every later
  hub day is this shape with different content.

#### Hikari's run chain (inside the hub)

Hikari is the one hub row that is not a confidant chain. The row is
`walk_hikari`, and `free_afternoon` sends it to `confidant_visit_hikari`
(`game/confidant_visits/hikari.rpy`) instead of straight to a walk label. That dispatcher reads
`hikari_visits`:

- `0` — the first run was skipped on Day 2, so the row plays the shorter
  `hikari_first_run` fallback instead of the ordinary walk;
- `1`–`6` — the next run (`hikari_visit_02` … `hikari_visit_07`);
- `7` — the run chain is complete and the row falls back to the ordinary walk.

Every run sets `last_afternoon_was_run = True` while it plays; `free_afternoon`
clears it before every row, and `afternoon_walk_hikari` clears it when the
fallback walk is taken. The Day 7 dinner reads it to distinguish "the river
path" from "the long way home." Visit 7 sets `hikari_run_finished = True` for
the Act 3/4 threshold. The run chain is tracked by `hikari_visits`, not
`confidant_visits`, so it does not affect the confidant caps or the "all
confidants met" gate; WIRE reads `hikari_visits` through its contact entry.
Visits 2–5 are reachable in the Days 7–14 build (Act 2 caps each confidant at
five); visits 6–7 are written and wait for Act 3.

#### City rows and the two extra contacts (2026-11-12)

`hub_destination_order()` in `locations.rpy` is now the single source of the
hub list: the five confidants, the Fortune Teller once `fortune_arc_started`,
the two walks, then the city rows, then the job rows. The job row is filtered
out until `combini_job_unlocked`. (The Fortune Teller is not a city row: she
joins the people list once `fortune_arc_started`.)

- **City rows** are not confidant arcs: no visits, no cap, no closure. The
  current list is `library`, `river`, `harajuku`, `karaoke`, `night_market`,
  `combini`, `odaiba`, `yokohama`, `ueno`, `shibuya`, `shimokitazawa`,
  `omotesando`. Each carries one cultural
  moment and a choice that does not have to pay; `last_afternoon_place` is the
  only state the evening reads.
- **Job rows** (`job_order`) get their own JOBS section in the hub list,
  separate from THE CITY: work is not wandering. Today it holds only
  `tanaka`, shown as "Convenience Store" once `combini_job_unlocked`.
- **The Fortune Teller** is a seven-visit confidant with one deliberate
  exception: she is not in `confidant_order`, because she is met on Day 13 —
  after the introduction gate opens — and requiring her would strand every
  confidant revisit until then. She is still in `confidant_visits`, gets the
  same cap and epilogue treatment (`confidant_visit_totals["fortune"] = 8`,
  and `destination_state()` gives her the epilogue state at visit 7), and is
  unlocked in WIRE on Day 13. Visit 1 is the Day 13 reading itself; visits
  2–7 and the corner epilogue live in `game/confidant_visits/fortune.rpy`,
  dispatched by `confidant_visit_fortune` from `free_afternoon`. Her arc is
  meta on purpose: she reads the "pages" — the script itself — and comments
  on choices before they are made, ending on the corner she promised in
  visit 2.
- **Tanaka and the combini job.** `combini_first_counter` is the first-visit
  Q&A and sets `combini_job_unlocked`. It is no longer hub-gated: Day 8
  (`wednesday_morning`) is a linear day whose afternoon is the discovery — he
  finds the combini on his own, sees the HELP WANTED card, and goes in. The
  `not tanaka_met` guards in `city_row_combini` and Day 13's Asakusa stop
  remain as fallbacks for runs that somehow met him first (arc replay). The
  shift itself is structured like a
  confidant arc: `label tanaka_shift` in `game/job_combini/tanaka_job.rpy` is a
  dispatcher that reads `tanaka_story` and jumps to one file per teaching
  shift, `tanaka_visit_01.rpy` … `tanaka_visit_07.rpy` — the register, the
  floor, the hot case, the fryer, the order, the tencho reveal, and closing.
  A shift pays ¥4,800, spends the afternoon, advances `tanaka_story` (0–7) and
  `combini_shifts`, and unlocks Tanaka in WIRE. Visit 6 reveals that Tanaka is
  the **tencho** — the store manager who has been doing the work the whole
  time. After visit 7 the job repeats (`tanaka_visit_repeat`): the row never
  closes, because the store does not.

### 5.8 Messages — texting, threads, and the buzz
`game/messages.rpy`. WIRE is the contacts book; Messages is the conversation.
Threads are keyed by the same contact ids, so unlocking somebody in WIRE is
what makes them textable.

- `send_message` / `receive_message` are the only writers; `receive_message`
  plays `audio/SFX/message_buzz.wav` and bumps the thread's unread count.
- `run_chat(cid, beats)` is how a scene plays an exchange: every beat lands in
  the thread AND shows it inside the quick-menu phone (`phone_chat_popup`
  reuses `phone_hardware`/`phone_status` and the shared `phone_app_shell`, so
  the chat has the same header, body bounds, and bubbles as the Messages app),
  so app history and what the player saw cannot disagree. Beat types:
  `{"them": ..., "img"?}`, `{"say": ..., "img"?}`, and `"options"` on ANY beat
  turns the bottom of the phone into a sliding reply sheet
  (`{"label","send","img"?,"them":[...]}`). An opening `options`-only beat is
  legal: the thread starts empty with the first line offered as a suggestion.
- Incoming beats arrive on their own. `run_chat` shows a typing bubble for
  `phone_chat_typing_time(text)` (scaled to line length, capped at 1.85s), then
  appends the message and holds it briefly before the next step. Choosing a
  reply appends the outgoing bubble immediately; any `them` replies attached to
  that choice then arrive one at a time with their own typing beat. Bubbles
  animate in from their stored `anim_at` monotonic timestamp, so a rebuild of
  the same screen does not restart the entrance — the effect is time-based,
  not tied to the screen's lifetime.
- The popup reserves its footer at all times: the reply sheet or composer
  floats over the bottom of the thread, and the thread gets matching bottom
  padding so the newest bubble never hides behind it. While the conversation
  is live the header shows no close button; once every beat has arrived, the
  composer becomes a pulsing **TAP TO CONTINUE** pill (and the header `×`
  appears) as the way back to the scene.
- `queue_message` + `flush_pending_messages` is the timing answer for texts
  that should arrive while he is busy: queue during a scene, flush at day
  turns (`second_morning`, `free_afternoon`). No signal, no delivery — the
  queue just waits. Entries may carry `day="yesterday"` and an optional image;
  the thread renderer prints `YESTERDAY` / `TODAY` separators from that field.
- `deliver_pending_messages()` is the same queue for a scene that stages the
  arrival itself. The first connection at Hamada Denki uses it: the chef's
  advert (walk-alone), Sim's Circle welcome (photo club), or Hikari's message
  from the river (run route) lands while Hikari is still standing there. The
  Hikari branch then offers one test reply in the popup, sends it, and lets her
  confirm in person that it arrived.
- The Messages app inside the phone launcher (`phone_app_messages_contents` /
  `phone_app_messages_thread_contents`) is read-only history: conversation
  list with unread badges, then bubbles. Replies only happen in story scenes.
- First use: the Akihabara walk home and the train ride home from the maid
  cafe (§4.7).

### 5.9 Calendar and opening hours
`game/calendar.rpy`. The story has one canonical day counter, one visible date,
and one place to say which weekdays a destination is open.

- **The anchor is fixed.** Day 1 is Wednesday, April 8; Day 2 is Thursday,
  April 9; and the built story runs through Monday, June 15 (Day 69). The
  investigation then pins Days 70, 72, 74, 76, 78, 80, 82 and 83, and the Act 4
  bridge pins Days 84, 87, 89 and 90, ending on Monday, July 6.
  Every day label pins its absolute day at the top with `set_story_day()`, so a
  branch or a rollback cannot leave the calendar a day behind. The full date
  table lives in `documentation/calendar.md`.
- **The player can see it.** `screen story_day_hud` is the top-left date chip,
  with the full weekday/date and `DAY N · WEEK N`. It rides the same switch as
  the attribute HUD (`show_attribute_hud`) and is hidden by standalone windows.
- **The phone has a Calendar app.** `phone_app_calendar_contents` draws a month
  grid, highlights today, marks days whose story beat has been reached, and
  shows the selected day's date and confidant opening hours. Browsing ahead
  does not reveal future beats. It is locked until the first contact is in WIRE;
  before that it shows `NOT UNLOCKED YET.` and `Your first connection opens the
  calendar.`
- **The first-connection gate now covers the contact-led apps.** Messages,
  Maps, WIRE, and Calendar all wait for the first WIRE contact; before it they
  are insensitive with grayed-out icons, and after it they become interactive.
- **The phone icons are one design language.** The launcher tiles draw the same
  rounded-square gradient tiles with a centered white glyph, and every app has a
  grayed-out `_disabled` variant used by the first-connection lock and the
  always-off camera. The tile body centers the icon and label through a
  centered vbox, so icons no longer drift inside their tile.
- **Weekly hours are data, not prose.** `destination_schedules` holds
  `open_days` or `closed_days` per place, plus the short `hours` line and the
  `closed_note` reason. Known canon: Ramen Shop is closed Wednesday (Chef's
  WIRE note) and Photography Club only meets Thursday (Sim's first text).
  Hana's reading room is Monday–Saturday; Aya and Orson have no written
  closure. `destination_is_open(place, weekday)` is the read-only check.
- **The hub combines hours with story state.** `destination_state()` returns
  `epilogue` before the act cap and before the schedule for any of the five
  confidants at seven or more visits. Otherwise `closed_today` comes before the
  act-cap pause, so a ready place can still be shut. A finished seven-visit arc
  with no epilogue reads Story complete rather than Closed today. The row mark
  for a closed day is `×`.
- **Scripted scenes ignore the schedule.** The first visit to every confidant
  is written on a specific day and must play even if that place would be shut
  in the hub. Opening hours only govern the free-afternoon hub after the
  introductions.

### 5.10 The day transition (`label day_transition`, `screen day_transition_screen`)

`game/day_transition.rpy`. The day counter is now a performance, not just a
number: every day label that opens a new day calls `call day_transition` right
after `set_story_day()`, so the move from the old day into the new one plays in
full before the new day's scene.

- **The strip.** The screen holds four card slots on a hairline rail. The day
  that just ended is centred and bright; the new day slides in from the side and
  settles, while the cards before/after shrink and fade. `day_transition_cards`
  builds the slots from `story_day - 1` and `story_day`, so the transition never
  carries its own day counter.
- **The move.** The card slide is a 0.95 s eased move (`ease`, Ren'Py's smooth
  in-out warper) plus a settle overshoot; the screen fades in over the black
  backdrop; the rail, glow, rays, vignette and grain all have their own timings.
- **Audio.** Riser (`attribute_rise.wav`) under the slide, settle hit
  (`attribute_settle.wav`) on landing, small tick (`type_click.wav`) for the
  lock-in; the music fades out (`stop music fadeout`) during the card.
- **The gate.** `screen day_transition_screen` is modal and sits at zorder 2000.
  Game menu, rollback, skip and fast-skip key actions are blocked; the
  `dismiss` key (plus a broad extra-key list so "press any key" holds) returns
  only once `ready` flips at 2.20 s. The full page therefore holds until the
  player presses a key or clicks, and never advances on its own.
- **HUD layering.** `standalone_window_active()` in `notice_windows.rpy` now
  includes `day_transition_screen`, so the date chip, attribute HUD and quick
  menu stay hidden behind the transition.

### 5.11 The nightmare rhythm

`game/dreams.rpy` (`label dream_router`). Nightmares are sparse by design; the
day progression does not depend on them.

- **Night one** (`label dream_first_night`) is the mandatory horror interlude and
  the origin beat of the dream logic. The act break (§4) ends inside it.
- **Night two** (`label night_room_visit` → `dream_key = "day_two_cellular_maid"`)
  is the reactive nightmare, the consequence of the phone-plan beat rather than a
  repeat of night one; it routes through the same router.
- **Nights three and later are quiet.** On the built path they fade to black from
  the night scene without routing through a nightmare, and the final night of the
  build ends on the Tuesday night beat without a dream at all.
- The router's fallback (`dream_generic`) is the seam for future activity-reactive
  keys; no built night forces one, so a nightmare only ever plays when the story
  has earned one.

Because the day transition (§5.10) is wired into every morning label that opens a
new day, the full-screen day progression now plays after **every** night — quiet
or nightmare — so the calendar move is never lost to a missing dream.

---

## 6. State Written by the Story

| Variable | Set by | Effect |
|----------|--------|--------|
| `player_name` | name entry | Every line of his own; the name the family uses |
| `money` | `start`, `spend_money()` | The wallet |
| `inventory` | `start`, `add_item()` | The Bag |
| `japanese_fluency` | initialised in `start`; +1 per Murakami lesson (Days 10–17) and per office-hours visit, cap 5 | Colour and comprehension of Japanese; `{jp}` text turns `#87cefa` at 5 |
| `murakami_enrolled` | the Day 12 night choice, or Murakami's enrollment text if he waits | Drives the WIRE meter and enrollment dialogue; the hub row opens on the Day 10 meeting instead; office-hours reminders start once set |
| `travel_method` | `travel_choice` | Taxi vs train downstream (`home_arrival`, `dream_router`) |
| `boarded_shinkansen` | `train_platform` | Express vs local |
| `arrived_late` | train route | Which `home_arrival` opening plays |
| `has_pamphlet` | `talk_assistant` | Unlocks the veteran assistant; used by the ticket machine |
| `assistant_returned` / `desk_checks` | `talk_assistant` | The assistant returns after the hub gate; the empty desk is visible before that |
| `talked_to_security` / `talked_to_man1` / `talked_to_npc2` | airport hub | The veteran assistant's alternate unlock |
| `security_index` / `board_message_index` / `plant_index` | airport hub | Which variant of a repeated interaction you get |
| `character_attributes` | `add_attribute_points()` | The three attributes |
| `attribute_reward_flags` | `reward_attributes_once()` | Stops any answer from paying twice |
| `remembered_choices` | `remember_choice()` | The answer he already gave a person, so they replay it instead of re-rolling |
| `character_memories` | `remember()` | What an important character is holding onto |
| `memory_names` | `remember()` | How those people are named in the `(X will remember that)` notice |
| `show_attribute_hud` | `airport_arrival` | Whether the three labeled attribute meters are on screen |
| `money_hint_shown` / `pamphlet_hint_shown` / `after_school_hint_shown` | first use of each | One-time tutorial cards |
| `first_day_activity` | the first-afternoon fork in `first_class` | Which shape of afternoon he picked (`walk_alone` / `walk_hikari` / `photo_club`); read immediately, never shown |
| `day6_route` / `day6_chef_route` / `day6_ate_out` / `day6_dinner_declined` | `monday_lecture` Day 6 fork and dinner | Internal carry for the second-confidant route and whether he ate out / skipped dinner; never shown |
| `hikari_visits` | `after_school_run` / `hikari_first_run` (first run) and `hikari_visit_02`–`07` (the rest) | Hikari's own run count — feeds her WIRE progress ticks and routes `confidant_visit_hikari`; separate from the confidant table |
| `hikari_run_finished` | `hikari_visit_07` | True once the seventh river run has happened; the run arc is complete and the Act 3/4 threshold is next |
| `last_afternoon_was_run` | `free_afternoon` (cleared), `hikari_visit_02`–`07` (set) | True when the hub row became a river run; the Day 7 dinner uses it to tell a run from the ordinary walk |
| `dream_key` | `start`, first-night sleep, day-two night | Which dream the router selects: `first_night`, `day_two_cellular_maid`, `put_the_day_back`, a future activity key, or `generic` |
| `quiz_announced` | `second_school_day` haiku lecture | The professor planted the short quiz; Hikari turns it into the library seed |
| `library_errand_available` | day-two night seed, cleared in `reading_club_first` | The library errand is seeded Friday night and consumed by the Saturday scene |
| `sunday_quiz_score` / `sunday_q1_correct`–`sunday_q3_correct` | `sunday_morning` practice quiz | Hikari's closing reaction branches on the score and names the actual missed question |
| `monday_quiz_score` / `monday_q1_correct`–`monday_q3_correct` | `monday_lecture` quiz | The score drives the closing narration; the flags identify which question he missed |
| `current_act` | `morning_call` (→ 2), `special_day_64_the_rail` (→ 3), `act4_bridge` (→ 4) | Which act's caps are in force (`act_confidant_cap`) |
| `act4_final` / `act4_maxed` / `act4_consolidation` | `act4_bridge`, set from save state | The Day 90 route, the completed arcs, and the readable consolidation number |
| `story_day` | `set_story_day()` at the top of each day label (`airport_arrival` = 1, `morning_call` = 2, `second_morning` = 3, `saturday_off` = 4, `sunday_morning` = 5, `monday_morning` = 6) | The canonical date; the HUD, phone Calendar and weekly hours all read it |
| `phone_calendar_selected` | the phone Calendar date grid | Which date the calendar's detail pane is showing; `None` means today (or the first of a browsed month) |
| `phone_calendar_month_offset` | the phone Calendar arrows | How many months the grid is from the current story month |
| `confidant_visits` | `after_school_walk_alone` (chef), `after_school_photo_club` (sim), the maid cafe scene (aya), and the Saturday scenes (`hana`, `orson`) | How many visits each person has had. The five confidants run to eight (`confidant_visit_totals`): seven numbered visits and a repeatable epilogue. `destination_state()` and WIRE read it |
| `declined_dinner` | `first_evening_dinner` (walk-alone route only) | He told the family he was still full from ramen; `second_morning` breakfast reads it so the two days agree |
| `sister_affection`, `father_affection`, `sim_affection`, `chef_affection`, `aya_affection`, `hana_affection`, `orson_affection` | The relevant first-visit/run/dinner/night beats; `add_affection()` in `script.rpy` | Relationship trust, written by the story and read through the affection helpers (`affection_level`, thresholds). Every confidant has a first-visit increment; Hikari and Tetsuo also gain from selected family/run beats. |
| `cellular_data_active` | `second_school_day` (Hamada Denki) | WIRE can sync off-Wi-Fi; gates `phone_map_is_unlocked("akihabara")` |
| `wire_unlocked` | `wire_unlock()` — Hikari in `leaving_house`, others in their first-visit scenes | Who is in the WIRE roster (`wire_order` = hikari, chef, sim, aya, hana, orson, murakami, tanaka) |
| `message_threads` / `message_unread` | `send_message()` / `receive_message()` in `messages.rpy` | The actual texts, per contact; unread counts per thread |
| `pending_messages` | `queue_message()` | Texts that arrive while the phone is out of reach; `flush_pending_messages()` delivers them at day turns if `cellular_data_active` |
| `phone_apps_messages_contact` | the Messages app | Which thread is open inside the phone UI |
| `phone_map_unlocked` / `phone_map_visited` | `phone_map_visit()` | Which map pins exist and which have been seen |
| `day_memory_*` | `first_night_memory` | The 4×3 day-recall board state |
| `haiku_study_method` | `second_school_day` haiku menu | Which study approach he picked; read by nothing yet |
| `place` (transient) | `free_afternoon` | The hub row picked this afternoon; not saved |

### 5.12 Arc replay (console test mode)

`game/arc_replay.rpy` is a test-only way to watch a confidant's chain without
playing the days between visits. Shift+O, then `jump arc_replay` for a menu, or
jump straight to `arc_replay_sim`, `arc_replay_orson`, `arc_replay_aya` or
`arc_replay_hana`.

The replay **calls the real visit labels** in order, with a black caption card
between each one, so the dialogue, menus, reward cards and WIRE messages are
exactly the ones from play. `arc_replay_begin()` snapshots the save state before
the chain and `arc_replay_end()` restores it afterwards, so a test run on a live
save does not advance your counters or spend your rewards. Quitting halfway
through a replay skips the restore.

Sim's chain includes his standalone visit 1. For Orson, Aya and Hana, visit 1
is inside the Day 1/2 routes and cannot be called on its own, so those replays
start at visit 2. Individual scenes still have their own `test_*` labels (Sim's
in `sim.rpy`, Hikari's tours in `hikari_tour.rpy`, the minigames in
`game/minigames/`).

---

## 7. Not Yet in the Script

These exist in `game_concept.md` and in the character files, but there is **no
scene for them yet**. They are listed here so nobody goes looking for a label
that does not exist.

- **The full Act 4 runtime in one scene.** Days 70-83 are playable investigation
  days in `act3_investigation.rpy`. The bridge compresses Days 84-89 into a
  montage, then plays Day 90. Later scenes are scripted days, not an extension
  of the hub loop.
- **The facility threshold.** The investigation's lab interludes show the
  older Hikari and Tanaka, but the threshold conversation itself is compressed
  to Hikari's account. See [act3_investigation.md](act3_investigation.md),
  [act4_bridge.md](act4_bridge.md), and
  [the Act 4 skeleton](act4_skeleton.md) for what is built and what is open.
- **The photography club's camera.** The first visit is built around arriving with
  nothing to shoot (§4.6). Circle hands over the camera at the end of that first
  session, in both the Day 2 route and the standalone `sim_visit_01`; the phone
  is what he actually shoots with until then.
- **The fortune teller, and the city locations.** Asakusa, Harajuku, Odaiba,
  Yokohama Chinatown, Ueno, Shibuya, Shimokitazawa, and Omotesando / Meiji
  Shrine are playable city rows (§5.7, `game/city_rows.rpy`). The Fortune
  Teller is a three-card limited confidant, not a seven-visit arc. Akihabara is
  still treatment-only.
- **A class schedule, the attendance counter, and the rest of the exam
  period.** The attendance *rule* is narrated in
  `student_relations`/`first_class` (§5.4), and the first quiz arc is
  scripted — Hikari's Sunday practice and the professor's Monday quiz in
  `script.rpy` — but there is still no `lates`/`absences` variable, no
  general-purpose class-schedule system, and no later exam sequence.
  `documentation/exam_and_courses.md` holds the plan, including the reusable
  quiz screen in `game/quiz.rpy`. Weekly *location* hours are separate and are
  implemented in `game/calendar.rpy` (§5.9).
- **Real art** — anything still calling `placeholder_bg(...)` or
  `bg_or_placeholder(...)` prints its own name on screen until the asset arrives.
  The older Act 2 placeholders are the **ramen shop** (`bg_ramen.png`,
  `bg_ramen_empty.png`) and the **photography club room** (`bg_photo_club.png`).
  The 2026-11-12 rows add `bg_fortune_stall` (real art now — renamed from
  `bg_yokohama_fortune.png`), `bg_combini`, `bg_odaiba`, `bg_yokohama`,
  `bg_ueno`, `bg_shibuya`, `bg_shimokitazawa`, and `bg_omotesando`. Drop any
  matching file into `images/backgrounds/` and the picture takes over by
  itself. `screen photo_mode` also still references
  `images/ui/camera_frame.png`, which does not exist, so calling it would fail.
