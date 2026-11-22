# Planted Story Beats — Act 3/4 Seeds

**Purpose:** A single reference for every seed already planted in the shipped
build (Days 1-50) that Act 3 must pick up, pay off, or escalate. Open this file
before planning or writing any Act 3 scene.

**Scope:** Only beats that are already written into the game. Design-only
ideas from `story_treatment.md` are not listed here unless they have a shipped
hook.

**Exchange duration note:** The build is now framed as a **three-month
exchange program (April to June)**, not a year. All "year" references in the
shipped script have been corrected to "three months" or "summer." Act 3
(tsuyu, June) is the final month.

---

## 1. The Twelfth Door

**Where planted:** `special_day_41_leak.rpy` (Day 41, Monday May 18)
**Flag set:** `door_twelfth_seen = True`

The department corridor had eleven doors on Day 29 (Hikari and MC counted
them while cleaning handles). On Day 41 there are twelve. The twelfth sits
between the fire extinguisher and the notice board. The wall has no room for
it. The handle is silver, new, and **warm**. The door is locked. Knocking
produces a sound that stops in the wall "the way a sound does in a room with
curtains."

Hikari puts her hand on the same handle and feels only a **cold wall**. She
wipes her palm on her skirt afterward. She does not pretend to see it.

After the lecture, MC returns to the corridor. The twelfth door is gone. The
wall is a wall.

**Act 3 must:** escalate the door. Either it returns, or more doors appear
that only MC can see. The warm/cold split between MC and Hikari is the first
structural proof that they are experiencing different simulations, or
different layers of the same one.

---

## 2. The Notebook Changes Its Own Handwriting

**Where planted:** `special_day_41_leak.rpy` (Day 41, night)

MC writes four lines in his notebook. The fourth line reads:
"She put her hand on it. I felt a wall."

The next morning the fourth line reads:
"I put my hand on it. I felt a wall."

The handwriting is his. The pen is the pen he used. The ink is still wet on
the last word. He does not cross it out.

**Act 3 must:** decide who is editing the notebook. The simulation correcting
its own record, or Hikari's fragment rewriting what he wrote from inside.
This is the first time the world changes a thing he made, and it is the
object he trusts most.

---

## 3. The Repeating Child

**Where planted:** `special_day_41_leak.rpy` (Day 41), first glimpsed Day 13
(Asakusa)

A child in a yellow hat runs past the platform laughing, then runs past again
in the same direction with the same laugh. The station attendant does not
look up. She is later on the train (swinging her feet, same laugh), then at
the school gate (running up the path, same laugh). When MC turns around,
there is one child, standing still, holding a woman's hand. She does not
look at him.

MC first glimpsed this pattern at Asakusa on Day 13 and told himself he
imagined it for a month.

**Act 3 must:** escalate the repeats. More NPCs that loop, or the same child
appearing in places she cannot be. The treatment's "faces blur" stage (Act 3
Stage 2) is the natural extension: the same face in different places, doing
the same thing.

---

## 4. The Shop That Forgot It Closed

**Where planted:** `special_day_41_leak.rpy` (Day 41)

The corner shop was closed Saturday and Sunday (paper over glass, sign on
door). On Monday morning it is open: paper gone, sign gone, man sweeping,
shelves full, no dust. That night it is closed again: same paper, same sign,
but the tape at the corners has gone yellow "the way tape does, which takes
longer than a day."

**Act 3 must:** escalate the world resetting itself. Objects or places that
snap between states, with physical evidence (the aged tape) that both states
have existed for longer than the gap between them.

---

## 5. The Milk Date

**Where planted:** `special_day_41_leak.rpy` (Day 41, kitchen)

The milk carton in the fridge is turned so the date faces out. The date is
the nineteenth. MC checked it last Monday and it said the nineteenth then
too. Mother says she checked it this morning. MC puts it back, takes it out
again. The date is still the nineteenth.

**Act 3 must:** decide whether time-stamped objects are frozen, looping, or
being reset nightly. This is the domestic layer of the leak; the door and
the child are the public layer.

---

## 6. Father's Verbatim Repeat

**Where planted:** `common_days.rpy` Day 38 beat, `leak_after_dinner`

Father says, word for word, the line he said on Day 34:
"The week is a machine. The combini is a smaller machine. You are learning
to operate both."

Nothing about the delivery changes. `leak_audio` fires. Hikari asks "Did
your father say that already?" MC confirms. Hikari dismisses it: "Father
repeats himself. It is what fathers do." MC notes "the sound was wrong. I
do not know how."

**Act 3 must:** escalate Tetsuo's glitches. The treatment's Stage 4
("Tetsuo Breaks") is the payoff: a repeated sentence delivered twice in a
row, a pause one beat too long, an answer to a question nobody asked. Miharu
covers for him, which makes it worse. This is the first non-Hikari character
to visibly break.

---

## 7. The Echo: Cold Water for a Warm Handle

**Where planted:** `common_days.rpy` Day 42 beat, `echo` field

Only fires if `door_twelfth_seen` is True. At the shrine, MC holds his wrists
under the temizu water longer than the order requires. Narration: "A handle
was warm yesterday where there was no door. This is cold, and it is here. I
will take what is here." Hikari notices he washed twice. She says "The water
does not count. It just runs."

**Act 3 must:** decide whether MC is grounding himself in real sensations
against the leaks, or whether the cold water is also a simulation and the
grounding is false comfort. The echo is the first time MC chooses a physical
act to answer a glitch.

---

## 8. Hikari's Threshold Question

**Where planted:** `confidant_visits/hikari.rpy` `hikari_visit_07`
**Flag set:** `hikari_run_finished = True`

At the bridge on the last run, Hikari asks: "Don't you ever feel like we've
done this before?" She says she has been running since before she can
remember, and "I don't think there is a part where it makes sense. I think
I've been running the wrong way."

She makes MC promise: "If I ever ask you to run somewhere I haven't taken
you, say yes." He says he will. She says "Don't promise. Just remember."

A queued WIRE message arrives the next day: "I meant what I said. About
running somewhere I haven't taken you. I'm not asking yet. I'm just putting
it somewhere you can find it."

**Act 3 must:** deliver on the promise. Hikari asks MC to run somewhere that
is not home, and that run is the path to the revelation (or the escape). The
promise is the mechanism by which she opens Act 4. `hikari_run_finished` is
the threshold flag the treatment names for Act 3/4 entry.

---

## 9. Hikari's First Truth About the House

**Where planted:** `confidant_visits/hikari.rpy` `hikari_visit_05`

The bridge in the rain. Hikari says her father closes the amado the same way
every night. She used to think the amado was what safety sounded like. Now
she wonders who taught him to do it in that order. She asks: "Does this
street look right to you?"

**Act 3 must:** pay off the amado. The order of the locks, the sound of the
house sealing itself, is a detail Hikari wrote and does not remember writing.
The street looking "right" is the first time she tests whether MC's
simulation matches hers.

---

## 10. The Fortune Teller's Prophecies

**Where planted:** `confidant_visits/fortuneteller.rpy` (visits 2-7),
`script.rpy` (Day 13 Asakusa reading)

Seeded lines that Act 3 must either fulfill or subvert:

- **"The person who put you here is not the person you think."** (visit 2)
- **"One has you walking out of a door. One has you staying at a table. One
  has you never arriving at all."** (visit 4, the three endings)
- **"There is a page in your book that is blank. Not unwritten, unwritable.
  It stays blank until you stand on it."** (visit 5, the blank page = MC's
  choice)
- **"Somebody is reading ahead of me... the patience of a man who has already
  read the ending and is only waiting for the middle to catch up."** (visit 5,
  the watcher = the lab staff / Tanaka)
- **"When you see the person reading over my shoulder, do not look at their
  face. Look at what they are holding... Everyone in this city has the same
  hands. That is the problem."** (visit 5)
- **"Stop looking for the door at the end of the corridor. It is not a
  destination. It is a threshold."** (visit 5, ties to the twelfth door)
- **"In six days a man will hand you a page with three questions on it. You
  will know two of them. The third will be in your own handwriting, and it
  will not have been there a moment before."** (visit 3, the ghost question)
- **"The door you keep looking for is not at the end of the corridor... It is
  the question they will ask you."** (visit 7)
- **The folded page** given on the corner (visit 3): "Do not read it tonight.
  Some pages only work if you are not looking at them." MC still carries it.

**Act 3 must:** deliver the ghost question (a quiz/exam page where a third
question appears in MC's own handwriting that he did not write). The folded
page must be opened at the right moment. The "same hands" line must pay off
when MC sees the lab staff or realizes the NPCs share a model.

---

## 11. The Two People at the Rail

**Where planted:** `special_day_50_fireflies.rpy` (Day 50, end of build)

After the fireflies, MC looks back. Two figures (a tall one and a short one,
side by side) stand at the rail where he and Hikari were. There is no path
to that spot except the one they walked. He did not see or hear anyone pass
them. `leak_audio` fires. When he looks again, they are gone.

MC keeps it off the notebook page: "That one I keep off the page, which is
what I have started doing with the things I am not ready to see written
down." He can tell Hikari about it in the night menu.

**Paid off on Day 64** (`special_day_64_the_rail`): they return in daylight.
The figures are recognisably the protagonist and Hikari, but the earlier
scene plays out differently: the torch falls. What caused the replay is
still open. The scene works whether or not the player told her on Day 50.

---

## 12. The Leak Audio Layer

**Where planted:** `leaks.rpy`, called on Days 16, 17, 18 (x2), 19, 20, 41,
50.

A short sound sting (`audio/SFX/leak.mp3`) that marks a seam without
explaining it. No visual. The player learns to associate the sound with
"something is wrong here" before the text confirms it.

**Act 3 must:** escalate the sound. The treatment's Stage 3 ("The Dream
Breaks Through") adds the hospital room as a visible space, not just a
flash. The leak sound should precede longer and longer hospital bleed-ins,
until the sound and the image arrive together.

---

## Threshold Flags for Act 3 Entry

| Flag | Set by | Meaning |
|---|---|---|
| `door_twelfth_seen` | Day 41 | MC has touched a door that is not there. The first structural glitch. |
| `hikari_run_finished` | `hikari_visit_07` | Hikari has asked the threshold question and MC has promised to say yes. The Act 3/4 gate. |
| `fortune_arc_started` | Day 13 Asakusa | The Fortune Teller is a contact. Her prophecies are live. |
| `confidant_visits["fortune"]` | visits 2-7 | Tracks how many prophecies have been delivered. Visit 7 gives the corner card. |

---

## What Act 3 Must Not Forget

- **The promise.** MC promised to say yes if Hikari asks him to run somewhere
  she has not taken him. That run is the spine of Act 4's reveal.
- **The folded page.** MC carries a folded page from the Fortune Teller that
  he has not read. It must be opened at the threshold.
- **The notebook edits itself.** The simulation can rewrite what MC writes.
  His record is not safe.
- **Hikari cannot see the door.** She is not on the same layer. Her warmth
  does not change when she says it, which is what makes the reveal land.
- **Tetsuo is the first to break after Hikari.** Miharu covers for him. The
  family is the last layer to go.
- **The three endings** (escape, stay, fail) are already named by the Fortune
  Teller. Act 3 does not invent them; it routes toward them.
