# Circle — Supporting Cast

The recurring members of Sim's photography club, **Circle**. They are
supporting characters, not confidants: they give the room its texture and
prove that the club is a real community, not a stage for Sim's arc. Each has
appeared across the written interactions under
`documentation/Locations/Photography Club - Sim/`.

| Name | Role | First appears | Notes |
| :--- | :--- | :--- | :--- |
| **Rika** | Member / recurring model | Visit 3 | Warm, theatrical energy ("my face — giant on a wall!"). The person the group photographs most often; her arc mirrors the club's growth. |
| **Nami** | Member / lighting lead | Day 2 first session (named by Sim there) | Dry, blunt, competent. Argues with Sim from the first scene ("You two have had this argument every week since March") and runs half the lighting by visit 4. The old note that she "wouldn't speak above a whisper" described an earlier draft, not the written voice. |
| **Marcus** | Member | Visit 1 (named in visit 2) | Laughs easily; argues that autofocus is lazy and that the poster matters as much as the photograph. Makes the exhibition map. |
| **Riku** | Member | Visit 2 (named by Sim; speaks there) | Quiet, plain-spoken. Took the best print on the wall by accident because he was late and did not look through the viewfinder. Designs the exhibition labels. |
| **Tapi** | Member / model | Named in the Day 2 first session; met in visit 2 | The second model. Quiet and precise rather than theatrical; has spent more time in front of a lens than anyone else in the room. Deadpan ("It is the same thing"). Models, brings coffee, and stays after Sim leaves. |
| **TT** | Guest / photographer | Named in the Day 2 first session; seen in visit 7 | Tapi's boyfriend, a working photographer. Not a student and not a member. Comes to the exhibition with a camera, argues about the lighting, and takes the one photograph in the show that a Circle member did not make — a portrait of Sim. |

## Portraits

All six have real art now, wired as side images in `game/script.rpy`:

- `circle_nami_standing.png` and `circle_nami_sitting.png` — a `ConditionSwitch`
  keyed on `nami_pose` ("standing" by default, "sitting" for the epilogue on the
  steps). Every Sim session resets it to "standing" (`sim_common_open`, with an
  explicit reset in visit 7).
- `circle_tapi.png` — Tapi, the dark-haired model in black knit.
- `circle_tt.png` — TT, the older man in a cap and glasses.
- `marcus.png` — Marcus, who makes the exhibition posters and map.
- `rika.png` — Rika, the theatrical model the group photographs most often.
- `riku.png` — Riku, the quiet, plain-spoken member who designs the labels.

Sim has his own portrait too, so the whole room has a face while it talks.
The `Character()` declarations and `image=` tags live in `game/confidant_visits/sim.rpy`.

## Notes for scripting

- Keep them consistent with the rule that Sim never gossips: what they say
  about each other is to their credit.
- Tapi's voice is short, literal and dry. She notices what people do with their
  eyes rather than what they say. Rika is the theatrical one; do not give Tapi
  Rika's lines or the other way round.
- TT is a grown-up with a job and a camera. He is warm and direct, not a
  wide-eyed fan of the club, and his interest in the room is professional as
  much as personal. His relationship with Tapi is shown in small, settled
  gestures — she hands him a cup, he knows when to raise the camera — never in
  an on-stage confession.
- They are the reason Circle can come back after Sim's departure (visit 7): the
  room stays open, the prints go into a box in the epilogue, and the members
  talk about who will host next. The club itself is on hold until then.
