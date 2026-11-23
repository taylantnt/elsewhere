# Act 3 Proper: Days 70-83, The Investigation

**Status: playable.** `game/days/act3_investigation.rpy` continues the
investigation from Day 69 to Day 83. It replaces the Days 70-89 montage that
the first-pass Act 4 bridge used. The bridge now only covers Days 84-89.

This is the slow-burn act the [day map](act2_day_map.md) describes: the hub is
closed, the people are gone, and the protagonist goes back to the places they
left behind. The keepsakes are the clues. The lab interludes are the part only
the player sees.

## The day chain

```
special_day_69_the_copy
  -> special_day_70_the_table
       -> special_day_72_the_shop
            -> special_day_74_the_circle
                 -> special_day_76_the_bar
                      -> special_day_78_the_cafe
                           -> special_day_80_the_library
                                -> special_day_82_the_house
                                     -> act4_bridge (Days 84-89)
```

Each label sets its own `story_day` and jumps to the next. The router only has
to send `story_day == 69` to `special_day_70_the_table`. Days 71, 73, 75, 77,
79 and 81 are rest days: they pass inside the jump and the transition card,
and no scene is written for them. That keeps each investigation day a deliberate
return instead of a routine.

## The clues

Each investigation day is built on one keepsake, one place, and one choice. The
choice decides how the clue is recorded, not whether the player is allowed to
continue. Any one branch records the clue; the three branches change the prose
and give a different micro attribute.

| Day | Place | Keepsake | Clue key | What it establishes |
|---|---|---|---|---|
| 70 | Home | Chef's chopsticks | `chopsticks_code` | The wrapping is printed with a file number, `04 / N-7`, not a maker's mark. |
| 72 | Ramen shop lot | Chef's chopsticks | `shop_tray_card` | The storeroom held MEAL SERVICE cards for POD 04, dated after the shop closed. |
| 74 | Photo club | Sim's strap | `sim_double_exposure`, `sim_corridor_frame` | A sealed box holds a white corridor and two Hikaris of different ages in one frame. |
| 76 | Lupin's Den | Orson's badge or coaster | `orson_guestbook` | H. NAGAI signed the guestbook before the protagonist arrived. |
| 78 | Maid cafe | Aya's page | `aya_nurse_drawing` | Aya drew the white room and the older Hikari, and wrote: she is not a ghost, she is a door. |
| 80 | Library | Hana's charm | `hana_book` | Hana left a book with a pressed hydrangea, a drawing of the door, and a warning not to let them finish his sentences. |
| 82 | Home | The house itself | `tetsuo_door`, `backdoor_message` | Tetsuo asks about the door at the end of the corridor; Hikari delivers the older Hikari's message. |

`act4_evidence` counts only the six optional clues, so the three Day 84 branches
are all reachable:

- 0 clues: some rooms were left closed.
- 1-3 clues: enough to suspect, not enough to prove.
- 4-6 clues: the protagonist can lay the clues out and read the sentence they
  make.

Day 90 also reads individual keys for specific lines (`backdoor_message`,
`sim_double_exposure`, `aya_nurse_drawing`). No clue gates the final choice.

## The lab interludes

Each day ends with a short scene outside the simulation. These are the scenes
the protagonist never sees. The convention is deliberate and must stay legible:

| Inside the world | Outside the world |
|---|---|
| First person, the protagonist narrating | Third person, watching the room |
| Dream voice is faceless | Doctor and older Hikari have portraits |
| The older Hikari appears as a reflection or a corridor | The older Hikari is in the room, tired, in a coat |
| `scene bg_*` inside the city | `scene bg_hospital2` or `bg_hospital3`, white walls |
| No marker | `centered "OUTSIDE THE SIMULATION"` before the scene |

Dream scenes stay inside the world. The `OUTSIDE THE SIMULATION` card is the
only thing that breaks the fourth wall this way, so the player can always tell
which layer they are in. The protagonist never refers to a lab scene afterward.

The interludes carry a second arc that the protagonist cannot see: Hikari
disliking the project and deciding to break it.

| Day | What the interludes show |
|---|---|
| 70 | Tanaka calls the subject stable. Hikari says he asked whether she was all right, which is not data. She decides to give the number a door. |
| 72 | The subject finds a tray card. Hikari says he has been seeing them for weeks. She opens a channel into the fragment. |
| 74 | Tanaka orders the fragment reset. Hikari refuses, and hides the door in the keepsakes: chopsticks, strap, badge, page, charm. |
| 76 | The guestbook was never in the scenario. Hikari says the record was always corrupt because she wrote it. |
| 78 | Aya's drawing reaches the lab. Tanaka calls it a deviation. Hikari pins it to the wall. |
| 80 | Five doors. The committee has signed Day 90. Hikari says she will be at the river. |
| 82 | The fragment is degrading. Hikari uploads a one-use key into the keepsakes and sits with the subject. The fragment looks at the camera. |

That key is what makes the ending possible without the protagonist ever knowing
it was built. On Day 90, Hikari can say the channel was her, and the Escape
route can open because the door was placed in the keepsakes during these days.

## The kitchen freezes

The freeze is planted twice, in the same place, with escalation:

- **Day 70:** Hikari stands at the sink with the tap running and does not
  respond. When she comes back she says, "I was getting water." The first lab
  interlude follows, so the player has just seen the room she was standing in.
- **Day 82:** It happens again. This time the protagonist does not call her
  name. He sees the white corridor in the window and the older Hikari at the end
  of it. The older Hikari raises a hand and Hikari's hand rises under the tap.
  This time she remembers a woman with her face and delivers the message.

Day 82 makes the freeze a channel, not a glitch. That is the reason the
backdoor can reach the protagonist on Day 90.

## What feeds Day 90

- `investigation_clues` and `act4_evidence` change the Day 84 montage, the
  revelation, and the final coda's texture.
- `backdoor_message` lets Hikari explain the sink and the channel.
- `sim_double_exposure`, `aya_nurse_drawing` and `hana_book` add specific lines.
- Completed confidant arcs still decide whether the ending has voices at the
  door and lights left on in the city.

## Open

- Days 71, 73, 75, 77, 79 and 81 are rest days with no scene. If they are
  written later, give them the house and the family, not another revisit.
- The lab interludes use `bg_hospital2` and `bg_hospital3`, which are placeholders
  if the final art is not in yet.
- The clue prose is first-pass. The clue keys and the Day 90 reads are the
  contract; the lines can be rewritten without touching the logic.
