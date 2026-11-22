################################################################################
## THE CORRUPTION LAYER
################################################################################
##
## Days 54-63 are the slow burn. The hub reopens, lectures resume, dinner
## happens. The structure of normalcy holds while the content rots. This file
## holds the flag and the shared beats that fire around the confidant visit,
## not inside it. The visit is the eye of the storm. The wrongness lives in
## the morning, the walk home, the dinner, and the night.
##
## Levels:
##   0 = none (Days 1-53)
##   1 = subtle (Days 54-57) — one wrong detail per day, barely noticeable
##   2 = noticeable (Days 58-60) — Mother stalls, Hikari at the door, rows close
##   3 = undeniable (Days 61-63) — house geometry wrong, the sentence everywhere
##
## The flag is set by each day label. The beats are called by each day file at
## the points the skeleton would normally control: post-hub walk, dinner, night.

default corruption_level = 0

## Post-visit reflection. Fires after free_afternoon returns, before the walk
## home. Not inside the confidant visit. The wrongness is in MC, not in the
## person he just spent time with.
label corruption_post_visit:
    if corruption_level >= 2 and last_afternoon_place and last_afternoon_place != "home":
        "On the way home I catch my reflection in a shop window. I stop."
        "The face is mine. The posture is mine. But the eyes are too still. Like they are watching from inside the skull, not from outside it."
        mc "(When did I start looking like this. Or have I always looked like this and only just noticed.)"
    if corruption_level >= 3 and last_afternoon_place and last_afternoon_place != "home":
        "The street is the same street. The shops are the same shops. But the distances between them are wrong. The combini is closer than it was yesterday. Or I am walking faster without noticing."
        mc "(The city is not moving. I am not moving. Something between us has changed, and I do not have a word for it.)"
    return

## The morning echo. Fires in the kitchen, before breakfast dialogue. A single
## wrong detail that the family does not notice.
label corruption_morning:
    if corruption_level == 1:
        "The kitchen is the kitchen. The table is the table. But there is one thing different, and I cannot find it. It is like a word missing from a sentence I have read a hundred times."
    elif corruption_level == 2:
        "The kitchen is the kitchen. The clock on the wall is the clock on the wall. It is stopped. It has been stopped since yesterday, or since before yesterday. Nobody has mentioned it. Maybe it was always stopped."
    elif corruption_level >= 3:
        "The kitchen is the kitchen. But it is bigger. The table has not moved but there is more space around it, as if the walls took a step back in the night. I count the tiles from the door to the counter. More than yesterday. I counted yesterday."
    return

## The night wrongness. Called after the night menu closes, before the final
## narration. Each level escalates.
label corruption_night:
    if corruption_level == 1:
        "I lie in the dark and listen to the house. The six sounds. The fridge, the pipes, the timer, the street, the neighbour's dog, the thing I have never named."
        "Tonight the seventh sound is back. Or it was always there and I am only now hearing it because the other six are quieter."
        mc "(I am not going to find it. I am going to sleep. Whatever it is, it has been here longer than I have.)"
    elif corruption_level == 2:
        "I lie in the dark. The house is doing its sounds. All six. But they are in the wrong order."
        "The fridge should be first. Tonight the pipes are first, then the street, then the fridge. Like the sequence shifted. Like someone reordered the list."
        mc "(A list. That is the word that came. Not a pattern. A list. Like someone wrote the sounds down and put them in the wrong order.)"
    elif corruption_level >= 3:
        "I lie in the dark. The house is not doing its sounds."
        "All six are gone. Or they are so quiet they might as well be gone. The silence is not empty. It is full. It is the sound of a room holding its breath."
        "Then the fridge starts. Just the fridge. None of the others. It hums, and stops, and hums, and stops, like it is trying to remember the rest of the sequence."
        mc "(The house is forgetting how to be a house. I am in a house that is forgetting how to be a house.)"
    return
