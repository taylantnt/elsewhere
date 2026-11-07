# Exam Period & Course Load

**Status:** design memo — the first quiz arc is scripted (Hikari's Sunday
practice and the professor's Monday quiz); later exam-period scenes remain
future.
**Why it exists:** Hana's introduction (and the Reading Club errand) hangs off
exam season, and the lectures the protagonist attends should all teach
something that can come back as an exam question. This file is the memo of
what he actually sat through, so the quiz and the errand have material to draw
on.

The professor’s quiz announcement and Hikari’s library errand are seeded in
`second_school_day` (`quiz_announced`, `library_errand_available`), Hikari's
room visit on the night of day two sets the exam timeline and the exact library
directions, and the errand is resolved in `reading_club_first` on the Saturday
sequence (haiku study sheets from the course reserve). The first quiz is now
written on both sides: `sunday_morning` runs Hikari's three-question practice
quiz off those sheets, and `monday_lecture` runs the professor's three-question
quiz. Both are menu-style, score into `sunday_quiz_score` /
`monday_quiz_score`, and record per-question flags so later dialogue can name
the miss.

---

## Timeline

| When | What |
|------|------|
| Wednesday, April 8 (Day 1) | Arrival at Narita, the trip home, the first night. |
| Thursday, April 9 (Day 2, first school day) | Orientation; the clerk's attendance rules; first lecture. |
| Friday, April 10 (Day 3, second school day) | Haiku lecture announces the quiz; Hikari gives the library route; the quiz is set for Monday, April 13. |
| Saturday, April 11 (Day 4) | Library errand: the haiku study sheets from the course reserve; Hana's introduction. |
| Sunday, April 12 (Day 5) | Hikari's three-question practice quiz off the handout. |
| Monday, April 13 (Day 6) | The professor's three-question quiz at the end of the haiku lecture; the result colors the afternoon and evening. |
| Act 2, late | The wider exam period — later exams, optional `run_quiz` sets, results echoing in later dialogue. |
| Act 3 | No classes — the world is breaking. (Deliberate contrast.) |

The first quiz sits at the end of the haiku unit, in the second week of Act 2.
The wider exam period is undecided; mid-to-late Act 2 is the right window
because it puts Hana's introduction early enough for her seven visits to
finish before Act 3. The canonical day/date table and the rule for advancing
the calendar are in `documentation/calendar.md`.

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
- The Sunday and Monday quizzes are menu-style in `script.rpy` rather than
  `run_quiz`, so their wrong answers get bespoke teacher reactions and
  per-question flags (`sunday_q1_correct`–`sunday_q3_correct`,
  `monday_q1_correct`–`monday_q3_correct`).
- Reward convention (agreed 2026-11-06): dialogue/menu quizzes — Sunday
  practice and the Monday lecture quiz — pay Insight `micro` per correct
  answer (`sunday_quiz_q*`, `monday_quiz_q*`). `run_quiz`-based quizzes use
  the clean-sheet shape instead: Insight `small` for all-correct
  (`exam_quiz_clean`), nothing otherwise, so the real exam feels distinct.

## Open questions

- Does the protagonist *take* the exams, or just survive the season? (A graded
  result could feed the Act 3 "assimilated enough" check for the endings.)
- ~~Does Hikari write the study guide, or does she just point at the library?~~
  Resolved: she points him at the library, then quizzes him from the handout
  on Sunday.
- ~~Which course does the missing department document belong to?~~ Resolved:
  the errand is a stapled set of haiku study sheets (kigo lists, example
  poems) from the course reserve — the haiku/literature course.
