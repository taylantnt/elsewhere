# Tanaka / The Doctor: One Face, Two Jobs

**Status:** Canon decision, 2026-11-20. The identity is intentionally never
stated to the player. It is carried by the art and by small, throwaway lines.

## Who he is

Tanaka is the man behind the combini counter: cold, efficient, always there,
the tencho who has been running the store the whole time. The Doctor is the
clinical voice in the white room outside the simulation, the one who says
"Subject 04. Can you hear me?" and decides when a day is over. They are the same
man. The face is identical; in the facility he wears a white coat and a surgical
mask, and in the simulation he wears a blue striped shirt and a paper name tag
that says たなか.

`images/characters/combini_worker.png` and `images/characters/doctor.png` are
the same drawing with different clothes and the mask. On screen they should
read as a face the protagonist almost recognises, never as a clean "surprise,
it was him" reveal.

## What he does

He is the face the program uses to keep things in line. He does not threaten
anybody. He gives work:

- **Inside the simulation**, he gives the protagonist a shift, a shirt, a
  register script and a wage. The lessons are the test in miniature: order,
  timing, disposal, repetition, doing it again tomorrow. The job row never
  closes, so the work goes on after the teaching stops.
- **Outside it**, he runs the actual test. The subject is a number, the day is
  a protocol, and "consolidation" is a line in a record. The protagonist is
  being made to work there too, even if the work is only staying inside the
  scenario and producing a score.

That is why the tencho reveal lands where it does. The protagonist spends five
shifts asking who runs the store, and the answer is the man who was standing in
front of him. The manager was never somebody else in an office. The manager was
the voice ordering him around, the same way the Doctor is the voice ordering
the whole simulation around.

## Where the game already hints at it

- `game/city_rows.rpy:336` — "For a second the fluorescent light makes his face
  the doctor's face. Then it is just a tired man in a striped shirt."
- `game/script.rpy:1504-1505` — author comment: the cashier is "wearing the
  same face as somebody the protagonist has met in a room he cannot explain."
- `game/job_combini/tanaka_visit_03.rpy:50-53` — "You keep looking at me like
  you know me" / "That is how the world saves money on faces" / the register
  light becomes a white room with a door at the end.
- `game/job_combini/tanaka_visit_06.rpy:47-52` — the tencho reveal cuts to the
  white corridor, and the protagonist notices the same posture and patience in
  a room he cannot remember.
- `game/days/special_day_13_asakusa.rpy:360` — the only named Doctor line:
  "Subject 04. Can you hear me?" It plays inside a flash, with no portrait.

## Art and wiring

- `images/characters/combini_worker.png` is wired as Tanaka's side image.
- `images/characters/doctor.png` exists but has **no** `image=` on the `doctor`
  Character and no `image side` entry. Keep it that way until the laboratory
  scenes. Until then the clinical voice must stay faceless.
- `images/characters/nurse.png` is the real counterpart of Hikari: same woman,
  older and tired, in a white coat with glasses and a clipboard. Reserved for
  the Escape ending's "welcome back" beat. Also unwired.
- `images/characters/hood.png` is reserved for the Robed Figure. Also unwired;
  she has no lines yet.

## Design notes

- Do not let a line explain the identity. The player should catch it the way
  the protagonist catches it: twice, briefly, and then dismiss it.
- Tanaka's voice stays clipped and practical. He never says "simulation,"
  "facility," "experiment," or "researcher."
- The Doctor's voice stays clinical and bored. He uses numbers, not names, and
  treats waking the subject like a timer going off.
- The repetition of the job is the point. A person who keeps being made to work
  after the lesson ends is a person being kept in line.
