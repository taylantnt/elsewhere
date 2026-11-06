# Elsewhere — Implementation Plan & Tracker

**Purpose:** the single place that says what is built, what is next, and in
what order. Update the checkbox (and date) as things land. Story detail lives
in `story_treatment.md` and the per-location interaction docs; this file is the
*order of work*.

---

## Act Map (decided 2026-11-05)

| Act | Title | Covers | Status |
|-----|-------|--------|--------|
| 1 | The Arrival | Airport → home → first dream → first night | **Built** |
| 2 | The Long Middle | First day, second day, the hub, all confidant visits | **In progress** — days 1–2 built, hub not yet reached by the story |
| 3 | The Glitch | The leaks stop being atmospheric and start being structural (treatment "Escalating Mystery" stages 1–5) | Not written |
| 4 | The End | The revelation, the three endings, and the epilogue coda | Not written |

Notes:

- Act 2 is deliberately **one big act**. It holds every confidant arc.
- Act 3 begins when broken things start appearing on purpose: repeated
  sentences, blurred faces, dream bleed-through, Tetsuo glitching.
- Act 4 begins at the river talk where Hikari tells him what she is.
- The **epilogue** is the short coda after an ending where the characters'
  thoughts play one last time — it is not a separate act.
- Act boundary is one line: `$ current_act = 2` at `morning_call`, `$ current_act = 3`
  / `4` at the future act breaks. If Act 2 should officially start on the
  *second* morning instead, move that one line.

## Confidant visit caps (act_confidant_cap)

| Act | Max visits per confidant |
|-----|--------------------------|
| 1 | 0 (no hub yet) |
| 2 | 5 — visits 1–5 during the long middle |
| 3 | 7 — final visits land as the world breaks |
| 4 | 7 (default) |

Final visits (6–7, the departures) are meant to fall inside Act 3's collapse,
which is the simulation removing people as the test measures his equilibrium.

## Hub rules

- One destination per afternoon.
- **Introduction gate:** a confidant place with 0 visits is always available
  (once the act cap allows). A place you have already visited is **"later"**
  until *every* confidant has been met at least once — then free choice.
- Act cap still applies on top: a place that has caught up with
  `act_confidant_cap[current_act]` shows **paused**.
- State order in `destination_state()`: closed → paused → later → ready.

## Endings (Act 4) — decided direction

- **The Escape:** Hikari guides him out. Confidants who were maxed out
  (all 7 visits) remember their original programming — they were built to
  help the subject — and can assist. Under-massed escape is harder.
- **The Blue Pill:** he stays. The world keeps running without the people
  who mattered.
- **The Failure:** he never reaches the threshold / is not assimilated enough.
  The simulation ends on its own terms: hard to move, things get worse, cut to
  the doctors — *"this one was also a failed experiment"*, *"bring in the next
  participant"* — then the title screen. Epilogue coda: characters' thoughts.

---

## To Do

### Code

- [x] 2026-11-05 — Chef teaches `umai` in `after_school_walk_alone` (was: word
      recognized from a packet). Docs synced.
- [x] 2026-11-05 — `game_structure.md` updated: new act table, §4.7 second
      day, §5.7 hub gating + `free_afternoon`, §6 state vars, §7 refreshed,
      stale `Dialogue/` paths fixed.
- [x] 2026-11-05 — Act map decided; `act_confidant_cap` retuned to
      `{1:0, 2:5, 3:7, 4:7}`; `current_act = 2` set at `morning_call`; script
      act headers renumbered to match.
- [x] 2026-11-05 — Hub "later" gate (no revisits until all five met) +
      `free_afternoon` dispatch wired in `locations.rpy` / `script.rpy`.
- [x] 2026-11-05 — Orson visit 1 rewritten as a hybrid (near-silent but with
      hooks: two cryptic lines, the water, the note bowl); treatment synced.
- [x] 2026-11-05 — Sim supporting cast documented (`-Side Characters/
      Circle members.md` + characters overview); names kept as-is per user.
- [x] 2026-11-05 — `documentation/exam_and_courses.md` created (timeline,
      course themes, literature ties, sample questions); `game/quiz.rpy`
      quiz mechanic added.
- [x] 2026-11-05 — Attribute rank ladder + reward sizes documented as the
      working baseline in `character_attributes.md` §11.
- [x] 2026-11-05 — Level stubs created for akihabara/harajuku/asakusa/
      odaiba/yokohama_chinatown; empty Part Time Jobs folders removed (ideas
      moved here).
- [x] 2026-11-05 — Dialogue scrub: removed " - " and em-dashes from
      player-facing text; ranks unpadded to "Rank 1–5" everywhere
      (`attribute_rank_names`, HUD, phone app, docs).
- [x] 2026-11-05 — `audio/SFX/attribute_rankup.wav` generated (synthesized
      chime); rank-ups now play it instead of `attribute_swell.wav`.
- [x] 2026-11-05 — Ramen dinner choice: `first_evening_dinner` (walk-alone
      route) offers honest-full (punished: `declined_dinner`, Grace loss,
      father's dinner-time rule) vs cover-and-eat (rewarded); `second_morning`
      breakfast follows up on either.
- [x] 2026-11-05 — Messages app: `game/messages.rpy` (threads keyed by WIRE
      contact ids, `run_chat` beat player, `queue_message`/`flush_pending_messages`
      for off-screen texts, `message_buzz.wav`), Messages page in the phone
      launcher (list + read-only thread), and the Akihabara/train-home
      exchanges rewritten as live chats.
- [x] 2026-11-06 — Information Desk: empty-desk `BACK SOON` flow before the
      security/timid/cheerful gate; assistant returns and the pamphlet branch
      opens after all three are approached.
- [x] 2026-11-06 — End-of-build card: `end_of_build` + `end_of_build_card`
      in `notice_windows.rpy`; night-two dream now routes through `dream_router`
      and lands there.
- [x] 2026-11-06 — Post-train-night expansion: family dinner/kitchen beats,
      food detail, station-writing lesson, quiz/library seed, weekend menu,
      reflection, sleep, day-two dream placeholder.
- [x] 2026-11-06 — Dream arrangement: board moved to `dream_archive.rpy`;
      first dream now uses narrative-only flow through `dream_router`;
      future activity keys parked in `dreams.rpy`.
- [x] 2026-11-06 — Relationship trust: affection helpers/thresholds added;
      Hikari/father weighted increments; Aya first-visit increment; other
      confidants ready for future levels.
- [x] 2026-11-06 — Menu handoff: new `MenuStart` / `MenuContinue` / `MenuLoad`
      actions in `game/script.rpy` wrap the built-ins (invoking the inner
      action, since `Start()`/`Continue()`/`ShowMenu()` only build Action
      objects) so new game / continue / load play the random one-shot narrator
      stinger (`audio/VO/elsewhere-normal.mp3` or `elsewhere-normal2.mp3`,
      looped off on a dedicated `stinger` channel - mixer `voice`, but immune
      to `voice_interact` killing the `voice` channel each interaction - so
      the menu theme keeps playing).
      New game, continue, and load-slot picks all play it at the click;
      `MenuFileSlot` wraps `FileAction` in `phone_files` so only title-screen
      loads get it. The arrival fades through
      `menu_handoff_fade` (`Fade(1.4, 0.6, 1.4)`) instead of hard-cutting;
      `label start` now uses the named handoff fade, and menu/game/end
      transitions are set to dissolve in `game/options.rpy`. The main menu theme
      (`config.main_menu_music`) is left to keep playing on the title screen and
      continue into the story.
- [ ] Wire `free_afternoon` into a real day loop (needs a day-3+ scene:
      morning → lecture → hub → night). Visit labels
      (`confidant_visit_<place>`) are stubs until the Act 2 scenes are written.
- [ ] Script Orson and Hana introductions (hub "ready" rows currently fall
      through to stubs).
- [ ] Remaining 32 confidant visits (chef 2–7, sim 2–7, orson 1–7, aya 2–7,
      hana 1–7). Interaction docs are written for all of them.
- [ ] Hikari's recurring run beats 2–7 (user intends to write these).
- [ ] Act 3 glitch content (treatment "Escalating Mystery" stages 1–5).
- [ ] Act 4 revelation + endings + epilogue.
- [ ] Fortune teller encounters (3, one per chapter — see treatment).
- [ ] Tokyo location visits: Asakusa, Odaiba, Harajuku, Yokohama Chinatown
      (treatment has full scenes; `Levels/` stubs created).
- [ ] Cultural-shock vignettes (onsen, 2 AM FamilyMart, karaoke, rush-hour
      train, matsuri) — treatment has them, unscripted.
- [ ] Exam period arc (see `exam_and_courses.md`): seed exam date, quiz
      mechanic exists (`game/quiz.rpy`), Hana's library errand hangs off it.
- [ ] Attendance counter (`lates`/`absences`) — rule is narrated only (§5.4
      of game_structure.md).
- [ ] Class schedule + literature tie-ins (see `exam_and_courses.md`).

### Art / assets

- [ ] `bg_department_hall`, `bg_ramen`, `bg_ramen_empty`, `bg_photo_club`
      placeholders → real art (drop file in `images/backgrounds/`).
- [ ] Portraits still missing: `hana.png` (needed before her scenes),
      orson, fortune teller, side characters.
- [ ] `images/ui/camera_frame.png` referenced by `screen photo_mode`.
- [ ] `images/messages/notebook_page.png` is a generated placeholder for the
      notebook-cat photo texted on the train — replace with real art when
      ready (swap the path in `script.rpy` `run_chat` or drop a new file in).
- [ ] Sim's supporting cast portraits (user will provide): Rika, Nami,
      Marco, Riku — see `Characters/characters overview.md`.

### Design decisions still open

- [x] 2026-11-05 — Rank names settled as "Rank 1–5" (see
      `character_attributes.md` §11); real names can replace them later if
      Act 2 gates want them.
- [ ] Whether Act 4 needs its own cap row or the 7-default is enough.
- [ ] Part-time jobs (ideas below) — none scheduled.

### Part-time job ideas (parking lot)

Existing reminder folders were empty and removed; ideas live here instead:

- Combini (convenience store) night shift — money grind, Grace/Nerve beats
- Curry shop kitchen help
- Game center prize counter / arcade staff
- Bookstore shelf-stocker (pairs with Hana's library arc?)
- Izakaya dishwashing
- Shrine/temple groundskeeping (ties to Asakusa + fortune teller)
- English conversation tutor (ties to Aya's English backstory)
- Photo studio assistant (ties to Sim)

### Level stubs to fill

`documentation/Levels/`: `akihabara.md`, `harajuku.md` (0 bytes),
`asakusa.md`, `odaiba.md`, `yokohama_chinatown.md` (new stubs).
Treatment already contains the Asakusa/Odaiba/Harajuku/Chinatown scenes.
