# Attribute Rewards Checklist

Current code snapshot: November 3, 2026.

This is an editable checklist of all 34 story choice menus currently in
`game/script.rpy`, including every answer with no attribute reward. The two
non-dialogue rewards are listed separately. Unwritten future scenes and the
developer rank-up shortcut are not story rewards.

## How To Edit

Edit the **Reward (editable)** cell beside an answer:

- `No rewards`: no attribute points.
- `Nerve`, `Insight`, or `Grace`: a small reward of **+0.5**.
- `Nerve +1.0`, `Insight +2.0`, etc.: an explicit point amount.
- Write a note beside the entry if you also want the dialogue changed.

Keep the IDs, answer text, source labels and existing flag names where possible.
They let me match your edits to the correct branch, even when an answer appears
in several scenes. No need to edit code yourself.

**Editing this file does not change the game automatically.** Ask me to apply
the edited checklist when you are ready. I can update the dialogue reward code,
preserve existing one-time flags, add flags for newly rewarded answers, and
check that repeat conversations cannot award points again.

The reward fields below describe the current implementation, not suggestions.
`No rewards` means no **attribute** reward; a choice can still affect money,
items, character memories, arrival time or the story.

Small = +0.5; medium = +1.0; large = +2.0. Rewards pay once per flag, with new
points capped at 15.0 per attribute. Existing rank requirements are listed in
Notes separately from rewards. Changing a reward does not change its requirement.

## Airport

### M01. Airport Exploration

Source: [`airport_exploration`](../game/script.rpy#L1760).
Context: choose whom to approach or what to examine.

These hub selections do not award points themselves. Any rewarded answer
inside the resulting conversation is listed in its own section.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M01.01 | Ask the Security Guard | No rewards | Opens M02. |
| M01.02 | Ask the Timid Man | No rewards | Opens M03. |
| M01.03 | Ask the Cheerful Woman | No rewards | Opens M04. |
| M01.04 | Ask the Information Desk | No rewards | M05 opens after all three initial NPCs have been approached. |
| M01.05 | Ask the Veteran Assistant | No rewards | Available with the pamphlet or after all three initial NPCs have been approached. His full advice needs the pamphlet. |
| M01.06 | Check the Information Boards | No rewards | Cycles the board notices. |
| M01.07 | Look at the Plants | No rewards | Cycles the plant observations. |

### M02. Responding To The Security Guard

Source: [`talk_security`](../game/script.rpy#L1777).
Context: the guard dismisses the protagonist or directs him away.
Repeat visits replay the chosen answer.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M02.01 | Apologise. | No rewards | `answer_security_bow`; says "Sumimasen. Sumimasen." |
| M02.02 | Point at the address again. | No rewards | `answer_security_press`; tries showing the address again. |
| M02.03 | Watch where everyone else goes. | No rewards | `answer_security_watch`; looks for the exit. |

### M03. Responding To The Timid Man

Source: [`talk_timid_man`](../game/script.rpy#L1851).
Context: he speaks too quickly for the protagonist to understand.
Repeat visits replay the chosen answer.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M03.01 | Ask where the information desk is. | No rewards | `answer_timid_again`. |
| M03.02 | Leave him to it. | No rewards | `answer_timid_aside`. |
| M03.03 | Listen for a word I recognise. | Insight +0.5 | Recognises "isogashii" as "busy"; flag `answer_timid_listen`. |

### M04. Responding To The Cheerful Woman

Source: [`talk_cheerful_woman`](../game/script.rpy#L1898).
Context: she welcomes the protagonist to Japan.
Repeat visits replay the chosen answer.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M04.01 | Smile and bow. | No rewards | `answer_woman_smile`. |
| M04.02 | Thank her in Japanese. | No rewards | `answer_woman_echo`; says "Arigatou gozaimasu." |

### M05. Asking The Information Desk For Help

Source: [`talk_assistant`](../game/script.rpy#L1933).
Context: the assistant is anxious about speaking English and asks to see the address.
Successful requests replay on later visits. Trying another desk does not prevent
the player from returning for the pamphlet.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M05.01 | Show her the address. | No rewards | `answer_assistant_ask`; receives the pamphlet. |
| M05.02 | We can use the map. No rush. | Grace +0.5 | `answer_assistant_patient`; flag `answer_assistant_patient`; then receives the same pamphlet. |
| M05.03 | I'll try another desk. | No rewards | `answer_assistant_nevermind`; leaves without the pamphlet. |

### M06. The Veteran Assistant's Travel Advice

Source: [`talk_veteran_assistant`](../game/script.rpy#L1996).
Prompt: "Which would you like to hear about?"

Asking for advice is not the actual travel decision.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M06.01 | Tell me about the train. | No rewards | Leads to M07. |
| M06.02 | Tell me about the taxi. | No rewards | Receives taxi advice, then leaves the terminal. |
| M06.03 | I have what I need. Thank you. | No rewards | Leaves the terminal. |

### M07. Additional Taxi Advice

Source: [`taxi_choice`](../game/script.rpy#L2024).
Prompt: "Would you like to hear about the taxi as well?"

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M07.01 | Tell me about the taxi. | No rewards | Receives taxi advice. |
| M07.02 | I'll take the train. Thank you. | No rewards | This answer does not lock in the route or award points; M08 is the actual decision. |

## Travel

### M08. Choosing How To Get Home

Source: [`travel_choice`](../game/script.rpy#L2078).
Context: choose between the expensive taxi and the cheaper train.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M08.01 | Take the taxi. | No rewards | Opens the cost warning in M09. The taxi reward is only awarded if the player confirms there. |
| M08.02 | Take the train. | Insight +2.0 | Sets the train route; flag `travel_route_attribute`. |

### M09. Confirming The Taxi After The Cost Warning

Source: [`taxi_warning`](../game/script.rpy#L2096).
Context: spending about eighteen thousand yen would use more than half the starting cash.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M09.01 | Take the taxi anyway. | Nerve +2.0 | Sets the taxi route; flag `travel_route_attribute`. |
| M09.02 | Take the train instead. | Insight +2.0 | Sets the train route; flag `travel_route_attribute`. |

M08.02, M09.01 and M09.02 share one flag. They are alternative ways of making
the same route decision, not three rewards the player can collect.

### M10. Speaking To The Taxi Driver

Source: [`taxi_stand`](../game/script.rpy#L2119).
Context: the meter has started; the protagonist is uncertain about the fare.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M10.01 | Thank him in Japanese. | No rewards | Says "Arigatou... gozaimasu." |
| M10.02 | Ask him to confirm the fare. | Nerve +0.5 | Asks whether it will be around eighteen thousand yen; flag `answer_taxi_fare`. |
| M10.03 | Watch the city through the window. | No rewards | Stops watching the meter for a moment. |

### M11. Approaching The Train Gate

Source: [`train_station`](../game/script.rpy#L2246).
Context: people appear to walk through the gate without anyone checking.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M11.01 | Walk straight through. | No rewards | Gate closes; then proceeds to the ticket machine. |
| M11.02 | Buy a ticket first. | No rewards | Proceeds directly to the ticket machine. |

### M12. Using The Ticket Machine

Source: [`ticket_machine`](../game/script.rpy#L2306).
Context: the protagonist cannot identify the correct fare from the pamphlet.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M12.01 | Press the 320 Yen ticket. | No rewards | Wrong ticket; costs 320 yen the first time; menu repeats. |
| M12.02 | Press the 800 Yen ticket. | No rewards | Wrong ticket; costs 800 yen the first time; menu repeats. |
| M12.03 | Ask the station attendant. | Grace +2.0 | Attendant selects the correct 1,300-yen ticket; flag `answer_ticket_ask`. |

### M13. Choosing A Platform

Source: [`train_platform`](../game/script.rpy#L2344).
Context: one sign lists eight stations; the other lists twenty-three.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M13.01 | The sign with eight stations. | No rewards | Faster train; sets `boarded_shinkansen = True`. |
| M13.02 | The sign with twenty-three stations. | No rewards | Slower train; sets `boarded_shinkansen = False`. |

## Host Family And Morning

### M14. Helping Miharu With The Boxes

Source: [`home_arrival`](../game/script.rpy#L2423), menu at line 2531.
Prompt: "Sorry about the stairs. And the boxes. I should have brought them up earlier."

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M14.01 | You've already done a lot for me. | Grace +0.5 | Acknowledges her effort; flag `answer_boxes_reassure`. |
| M14.02 | Which ones go upstairs? | No rewards | Asks whether to carry all the boxes or just the clothes. |
| M14.03 | Can we leave the books until morning? | No rewards | Asks to postpone the heavier unpacking because of fatigue. |

### M15. Breakfast With Hikari

Source: [`morning_call`](../game/script.rpy#L3112), menu at line 3185.
Context: people in the department have been asking when the protagonist will arrive.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M15.01 | What have you told them about me? | No rewards | Hikari remembers the question. |
| M15.02 | Should I introduce myself today? | No rewards | Hikari remembers the question. |
| M15.03 | Thank you for the emails. | Grace +0.5 | Explains that her emails made the move less frightening; flag `answer_breakfast_emails`; Hikari remembers. |

### M16. Listening To The Screen Door

Source: [`leaving_house`](../game/script.rpy#L3252).
Context: Hikari says she can hear a person's mood in how they close the amado.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M16.01 | How can you hear a difference? | No rewards | Asks whether her father closes it differently when angry; Hikari remembers. |
| M16.02 | I didn't hear anything. | No rewards | Admits it sounded like an ordinary door; Hikari remembers. |

## University

### M17. Before Entering The University

Source: [`school_morning`](../game/script.rpy#L3330).
Context: Hikari has explained the university's basic expectations.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M17.01 | What did you do, your first day? | No rewards | Asks whether she was this lost; Hikari remembers. |
| M17.02 | I had a list. It was wrong. | No rewards | Admits the expectations brought from the plane were inaccurate; Hikari remembers. |
| M17.03 | Where do I check room changes? | No rewards | Asks about the department board and student portal; Hikari remembers. |

### M18. Looking At The Campus

Source: [`campus_grounds`](../game/script.rpy#L3429).
Context: the campus is much larger and more varied than it looked from outside.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M18.01 | Which building is ours? | No rewards | Asks which building belongs to their department; Hikari remembers. |
| M18.02 | These buildings are different ages. | Insight +0.5 | Notices construction from different periods; flag `answer_courtyard_buildings`; Hikari remembers. |
| M18.03 | Let's keep moving. | No rewards | Chooses not to make them late. |

### M19. The Department Noticeboard

Source: [`department_tour`](../game/script.rpy#L3490).
Prompt: "Anything on the board catch your eye?"

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M19.01 | The film screening. | No rewards | Asks whether anyone can attend; Hikari remembers. |
| M19.02 | The three rooms for rent. | No rewards | Notices the identical photographs; Hikari remembers. |
| M19.03 | [Insight] The lost cat. | Insight +0.5 | Requires Insight rank 2; flag `answer_wall_cat`; examines the old tape and date; Hikari remembers. |

### M20. Student Relations And Circles

Source: [`student_relations`](../game/script.rpy#L3539).
Context: the clerk has explained student cards, attendance, electives and circles.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M20.01 | Which one would you pick? | No rewards | Asks which circle the clerk would choose; she remembers. |
| M20.02 | When does the photography club meet? | No rewards | Asks whether visitors can attend; the clerk remembers. |
| M20.03 | [Grace] You've made this much easier. | Grace +0.5 | Requires Grace rank 2; flag `answer_circles_back`; the clerk remembers. |

### M21. Discussing The Late Mark With The Professor

Source: [`first_class`](../game/script.rpy#L3632), menu at line 3697.
Context: Student Relations registration made the protagonist late for his first lecture.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M21.01 | I'll write that down. | No rewards | Records the attendance rule; the professor remembers. |
| M21.02 | It won't happen again. | No rewards | Apologises and promises to arrive early; the professor remembers. |
| M21.03 | [Nerve] Can we discuss today's late mark? | Nerve +0.5 | Requires Nerve rank 2; flag `answer_clock_ask`; requests review of the registration conflict; the professor remembers. |

### M22. Responding To Hikari After Class

Source: [`first_class`](../game/script.rpy#L3632), menu at line 3749.
Prompt: "I should have told you where to go before I ran off. I'm sorry."

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M22.01 | Next time, warn me before you go. | Nerve +0.5 | Sets a boundary about being left without directions; flag `answer_hikari_warning`; Hikari remembers. |
| M22.02 | Thanks for saving me a seat. | No rewards | Hikari remembers the thanks. |
| M22.03 | Let's get something to eat. | No rewards | Moves on from the lecture; Hikari remembers. |

### M23. Choosing The First Free Afternoon

Source: [`first_class`](../game/script.rpy#L3632), menu at line 3777.
Context: Hikari leaves the afternoon up to the protagonist.

The route-selection answers do not award points themselves. Subsequent
dialogue and activity rewards are listed below. Only one afternoon route is
played in this act.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M23.01 | I want to learn the way home. | No rewards | Walks alone; leads to the ramen shop, M24-M26. |
| M23.02 | I'll come with you. | No rewards | Walks with Hikari; leads to the run, M27-M29 and E02. |
| M23.03 | I want to find the photography club. | No rewards | Visits Circle, M30-M34. |

## Ramen Shop Route

### M24. Ordering Ramen

Source: [`after_school_walk_alone`](../game/script.rpy#L3822), menu at line 3884.
Context: the handwritten menu is unreadable to the protagonist.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M24.01 | Order in English. | No rewards | Asks for ramen in English. |
| M24.02 | Point at something. | No rewards | Points at the second menu line. |
| M24.03 | Ask for his recommendation. | Nerve +0.5 | Tries "Osusume" in unfamiliar Japanese; flag `answer_ramen_recommendation`. |

### M25. Receiving The Bowl

Source: [`after_school_walk_alone`](../game/script.rpy#L3822), menu at line 3911.
Context: the broth is darker and heavier than expected.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M25.01 | Ask what kind of broth it is. | No rewards | Asks "Shoyu? Miso?" |
| M25.02 | Try it before asking. | No rewards | Starts eating instead. |

### M26. Responding To The Chef About The Taste

Source: [`after_school_walk_alone`](../game/script.rpy#L3822), menu at line 3934.
Prompt: the chef says "うまい、だろ？" after hearing the protagonist enjoy the ramen.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M26.01 | Tell him in Japanese. | Grace +0.5 | Says "Umai. Arigatou gozaimasu."; flag `chef_first_umai`. |
| M26.02 | Ask what gives it the smoky flavour. | No rewards | Asks whether the flavour comes from the pork. |
| M26.03 | Smile and keep eating. | No rewards | Nods and continues eating. |

Finishing the bowl, paying for it, meeting the chef and unlocking WIRE do not
award additional attribute points. The first chef visit is recorded separately.

## Hikari's Run Route

### M27. Walking Home With Hikari

Source: [`after_school_run`](../game/script.rpy#L4032), menu at line 4055.
Context: the two are walking home through the neighbourhood.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M27.01 | Thanks for coming back with me. | No rewards | Acknowledges that she might have had other plans. |
| M27.02 | How long have you lived here? | No rewards | Asks whether she has always lived on this street. |
| M27.03 | Which turning is ours? | No rewards | Checks the route home. |

### M28. Before Going For A Run

Source: [`after_school_run`](../game/script.rpy#L4032), menu at line 4072.
Context: Hikari walks past the house and says she is going out again.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M28.01 | Out where? | No rewards | Asks where she is going. |
| M28.02 | Is this your usual running route? | No rewards | Asks whether she normally leaves from here. |
| M28.03 | Can I come? | No rewards | Asks to join her. |

All three answers lead to the run. Its completion reward is E02, not a separate
reward on each of these answers.

### M29. Resting Beside The River

Source: [`after_school_run`](../game/script.rpy#L4032), menu at line 4139.
Context: they drink under a lamp and listen to the water.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M29.01 | Let her enjoy the quiet. | Grace +0.5 | Gives her space without filling the silence; flag `answer_river_quiet`. |
| M29.02 | Do you do this every day? | No rewards | Asks how often she runs. |
| M29.03 | Why the river? | No rewards | Asks why she chooses this route. |

## Photography Club Route

### M30. Entering Circle

Source: [`after_school_photo_club`](../game/script.rpy#L4230), menu at line 4277.
Context: the room turns to look at the newcomer and Sim welcomes him.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M30.01 | Is this the photography club? | No rewards | Confirms he has found the right room. |
| M30.02 | Could I join today's session? | Nerve +0.5 | Asks to participate despite being new to group sessions; flag `answer_circle_join`. |
| M30.03 | Hikari told me I could drop in. | No rewards | Checks whether now is a good time. |

### M31. Answering The Camera Question

Source: [`after_school_photo_club`](../game/script.rpy#L4230), menu at line 4299.
Prompt: "So. Do you have a camera?"

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M31.01 | My camera's at home. | No rewards | Explains he was not expecting to visit today. |
| M31.02 | Only my phone today. | No rewards | Asks whether his phone is enough. |

### M32. Looking At The First Photograph

Source: [`after_school_photo_club`](../game/script.rpy#L4230), menu at line 4313.
Prompt: "What do you notice?"

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M32.01 | The window is brighter than everything else. | Insight +0.5 | Recognises the exposure problem and reframes the shot; flag `sim_circle_first`. |
| M32.02 | I tilted the phone. | No rewards | Notices the crooked door in the photograph. |
| M32.03 | I'm not sure what to look for yet. | No rewards | Asks for time and guidance. |

### M33. Asking Sim About Photography

Source: [`after_school_photo_club`](../game/script.rpy#L4230), menu at line 4331.
Context: Sim explains that he works in an office and guides Circle outside work.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M33.01 | How did Circle start? | No rewards | Asks how the club began. |
| M33.02 | Do you shoot outside the club too? | No rewards | Asks about his photography outside Circle. |

### M34. Preparing For The Model Session

Source: [`after_school_photo_club`](../game/script.rpy#L4230), menu at line 4346.
Context: a volunteer is modelling and the theme is a natural smile.

| ID | Answer / Choice | Reward (editable) | Notes |
|---|---|---|---|
| M34.01 | Can I help set things up? | Grace +0.5 | Moves spare chairs so the model has room; flag `answer_circle_help`. |
| M34.02 | Can I watch for a while first? | No rewards | Asks to observe before participating. |
| M34.03 | Do you choose a new theme each week? | No rewards | Asks how session themes work. |

Completing the session, recording Sim's first visit and unlocking WIRE do not
award extra attribute points. `sim_circle_first` pays for M32.01 specifically,
not for attending the club.

## Rewards Outside Dialogue Choices

### E01. Put The Day Back: Memory Puzzle

Source: [`dream_sequence`](../game/script.rpy#L2952), reward at line 3091.
The player places four true memories in order and submits REVIEW SEQUENCE.
Three readings are available; only an incorrect reading reduces the counter.

| ID | Outcome / Action | Reward (editable) | Notes |
|---|---|---|---|
| E01.01 | Correct sequence on the first reading. | Insight +1.0 | Flag `dream_day_order`; `dream_solved` is true and `dream_attempts == 3`. |
| E01.02 | Correct sequence on the second reading. | No rewards | Puzzle is solved, but the first-reading reward is not awarded. |
| E01.03 | Correct sequence on the third reading. | No rewards | Puzzle is solved, but the first-reading reward is not awarded. |
| E01.04 | Incorrect sequence on a reading. | No rewards | Loses one reading; the arrangement is preserved. |
| E01.05 | All three readings used without solving. | No rewards | Continues the story without the puzzle reward. |
| E01.06 | Place or remove a memory card. | No rewards | Arrangement controls do not award points themselves. |

### E02. Completing Hikari's First Run

Source: [`after_school_run`](../game/script.rpy#L4032), reward at line 4169.

| ID | Outcome / Action | Reward (editable) | Notes |
|---|---|---|---|
| E02.01 | Complete the first river run with Hikari. | Nerve +1.0 | Flag `run_first_river`; awarded on the run route regardless of M27-M29 answers. |

## Other Existing Screens

These are not additional dialogue forks or attribute rewards:

- WIRE records visits and memories; unlocking a contact does not award attributes.
- The destination hub in `game/locations.rpy` currently has no attribute awards
  and is not connected to the playable first-afternoon selection. Future
  destination visits are not implemented rewards.
- The camera preview's Take Photo and Exit buttons do not award attributes.
- Notices, name entry, tutorial acknowledgements and gain-card Continue buttons
  do not award attributes.
- The developer-only rank-up shortcut is a testing tool, not a story reward.

## Notes For Applying Edits Later

Use the row IDs to describe any special instructions, for example:

- `M02.02: Nerve +0.5. Keep the answer text.`
- `M27.01: Grace.`
- `M32.02: Insight +0.5.`
- `M19.03: No rewards. Keep the Insight rank 2 requirement.`

Unless you say otherwise, bare attribute names mean +0.5, dialogue wording and
rank requirements stay unchanged, and new awards use the existing notification
system. Existing rewards remain once-only. Newly rewarded answers in repeatable
conversations need their own stable flag while keeping the answer-replay logic.

For route selectors and shared event flags, I will distinguish a new immediate
reward from the reward already awarded later in the route. This prevents an
edit to a hub answer from accidentally duplicating its conversation reward.
