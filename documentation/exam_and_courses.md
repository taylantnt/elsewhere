# Exam Period & Course Load

**Status:** design memo — partially scripted seed, full exam/quiz arc still future.
**Why it exists:** Hana's introduction (and the Reading Club errand) hangs off
exam season, and the lectures the protagonist attends should all teach
something that can come back as an exam question. This file is the memo of
what he actually sat through, so the quiz and the errand have material to draw
on.

The professor’s quiz announcement and Hikari’s library errand are now seeded in
`second_school_day` (`quiz_announced`, `library_errand_available`); the full quiz
scenes and the Hana reading-club introduction remain unwritten.

---

## Proposed timeline

| When | What |
|------|------|
| Act 2, week 1–2 | Syllabi handed out; first lectures (history, haiku/literature). Clerk's attendance rules start to matter. |
| Act 2, mid | **Exam season announced** — the errand seed: Hikari tells him the library is where people go to actually get something done (study + documents). This is where Hana's intro hangs. |
| Act 2, late | Exam period itself. Optional quiz scenes (`game/quiz.rpy`) reward Insight; results can echo in later dialogue. |
| Act 3 | No classes — the world is breaking. (Deliberate contrast.) |

The exact date is undecided; mid-to-late Act 2 is the right window because it
puts Hana's introduction early enough for her seven visits to finish before
Act 3.

## Courses (each lecture teaches something usable later)

### History — "the shrinking country"

- **Theme:** Japan's population decline as arithmetic, not tragedy. The
  professor's first lecture already states the game's thesis ("it is
  arithmetic"). Later lectures: regional depopulation, automation, the
  government response.
- **Literature tie:** taught alongside excerpts — *The Memory Police* or a
  Japanese text on societal pressure to conform. The course treats literature
  as evidence, which is itself a theme (who gets to write the record?).
- **Sample exam questions:**
  - "What did the professor say was the real cause of the population decline —
    and what did he say it was *not*?"
  - "Which region did the lecture use as its example, and what happened there?"
  - "The clerk said three absences means what, exactly?" *(attendance rules
    become examinable — ties to §5.4 of game_structure.md)*

### Haiku / Literature — kigo and the seasonal word

- **Theme:** the small detail as the door into the whole poem. Already
  scripted in `second_school_day`.
- **Literature tie:** this *is* the literature course in practice — haiku
  units connect to novel units (a poem about a season ↔ a novel about a
  disappearing one).
- **Sample exam questions:**
  - "What is a kigo, and what does it do that naming the season does not?"
  - "In the example poem, which word was the kigo?" *(frog / old pond)*
  - "Five-seven-five counts what, exactly — and why did the professor say the
    count is not the point?"

### (future) Language / electives

- The clerk's electives list is wide open — a Japanese-language course for
  exchange students is already named in `student_relations`. Natural fit for
  the `japanese_fluency` progression and for the chef/Sim language beats.

## Mechanics

- `game/quiz.rpy` provides `run_quiz(questions)` — a no-timer, no-fail
  question screen returning per-question correctness. Use it for:
  - a short **pop quiz** after a lecture (2–3 questions, tiny Insight reward),
  - the **exam period** itself (longer set, bigger reward, once-only),
  - the **Hana errand** (a "find the document" beat can reuse the same
    screen as a retrieval puzzle later).
- Attendance counter (`lates`/`absences`) is still unimplemented — the exam
  arc is the natural place to add it, since three absences = no final exam.
- Rewards should stay small and once-only (`reward_attributes_once`), per the
  minigame guardrails.

## Open questions

- Does the protagonist *take* the exams, or just survive the season? (A graded
  result could feed the Act 3 "assimilated enough" check for the endings.)
- Does Hikari write the study guide, or does she just point at the library?
- Which course does the missing department document belong to? (Needs one —
  it's the concrete reason he walks into the reading circle's corridor.)
