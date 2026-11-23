# Act 4: Day 90 Bridge

**Status: playable.** `game/days/act4_day_90.rpy` connects Day 83 to the Day 90
threshold and the epilogue coda. Days 70-83 are now playable investigation days
in `game/days/act3_investigation.rpy`; the bridge compresses only Days 84-89.

This follows the decided direction in `plan.md` and the sequence in
`act4_skeleton.md`. The whole act lives in one label block, and the three
endings share one coda, so it stays easier to revise than the day files.

## How it is reached

Day 82 hands off to `act4_bridge` after its morning scene. The router only has
to send Day 69 to the investigation.

```
special_day_69_the_copy
  -> special_day_70_the_table ... special_day_82_the_house
       -> act4_bridge
            -> act4_river
                 -> act4_escape  -> act4_coda -> end_of_build
                 -> act4_stay    -> act4_coda -> end_of_build
                 -> act4_failure -> act4_coda -> end_of_build
```

The bridge sets `current_act = 4` and pins the calendar to Days 84, 87, 89 and
90. Day 90 is Monday, July 6, 2026, the date already named in
`game_structure.md`.

## What the montage covers

- The coin on the first stair, left where neither of them will touch it on the
  night after the copy, pays off Day 69's last line. It is gone on Day 84.
- The last week of June has no weather, only a temperature that does not change.
- The clue count decides how the protagonist reads the investigation: he can lay
  the clues out and read the sentence they make (4+), suspect without proof
  (1-3), or carry the quiet of the rooms he left closed (0).
- Tetsuo repeats the machine line and asks about a class the protagonist does
  not take. The player chooses whether to write it down, tell Hikari, or let
  Miharu cover for him. This sets `act4_witness` and gives one micro reward.
- Hikari says she wrote the house and asks him to come to the river on Monday.
- The last day of June packs the keepsakes, the clues, and the folded page. None
  of them were made in the simulation; all of them were.

## Day 90

Hikari gives the revelation from `story_treatment.md`: she is a fragment of a
programmer, he is Subject 04 in a medicine-induced coma, the attributes are the
score, and the confidants were removed when their arcs completed because getting
close is the protocol. She also names the woman in the white coat outside, and
the channel the older Hikari built into the fragment.

The scene reads save state as texture, never as a gate:

- `investigation_clues` and `act4_evidence` add the lines that connect the
  investigation to the revelation. The six optional clues are counted; the two
  automatic Day 82 clues are not, so all three evidence branches stay reachable.
- `backdoor_message` lets Hikari explain the kitchen freeze as a telephone call
  from the older Hikari. `sim_double_exposure`, `aya_nurse_drawing` and
  `hana_book` add specific lines.
- `story_memory_keys` adds lines for the folded page, the first warning, the
  notebook rewriting his line, and the seventh river run.
- `confidant_visits` decides whether the ending has voices at the door and
  traces in the city. A player with no completed arcs still gets the full
  baseline route.
- `hikari_run_finished` changes one line in the Stay route.
- A readable `act4_consolidation` percentage is computed from met and completed
  arcs (58 to 96). Hikari quotes it and immediately says the number is the
  lab's, not a verdict. It is flavour, not a gate.

## The final choice

| Choice | Route | What changes |
|---|---|---|
| Take her hand | `act4_escape` | Wakes in the hospital. Maxed confidants speak from the other side of the door. The player gets one last action: ask who authorised the test, ask about the fragment, or answer to his own name. |
| Stay | `act4_stay` | The routine continues without the people. Maxed arcs leave lights on; unfinished places stay closed. Hikari is at the bend and does not come back. |
| Cannot choose | `act4_failure` | The test ends on its own terms. The city folds, the house gives the last image, and the clinical voice closes the session. The option states the cost on the label. |

Staying is an informed choice, not a delayed failure. The fragment's fate after
Escape is left unresolved. These are the two open questions from
`act4_skeleton.md` that the first pass had to answer to be playable.

## Coda

`act4_coda` is the montage from `story_treatment.md`: one line from inside each
person's head. Chef, Sim, Orson, Aya and Hana appear only if they were met, and
their line changes if their arc reached the repeatable epilogue. Hikari's line
changes with the ending. The final line is always the thesis:

> It was not real. You were. That is enough.

Then the existing `end_of_build` card plays.

## What is still open

- The facility sequence is compressed to the bedside. The older Hikari and
  Tanaka are seen only in the investigation's lab interludes, and the threshold
  conversation itself is represented by Hikari's account, not played.
- No numeric ending requirement exists. If later drafts add one, keep the
  baseline route and apply the skeleton's rule: check a sparse route and a
  relationship-heavy route before tuning it.
- The Escape route's fragment fate is deliberately unresolved. If a later route
  answers it, the answer belongs after the hospital bed, not in the river scene.
