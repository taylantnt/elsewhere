################################################################################
## DAY 12 — SUNDAY, APRIL 19, 2026 (THE ELECTIVE, PART 3)
################################################################################

label sunday_practice:
    $ set_story_day(12)
    call day_transition

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Sunday. The last day of the first week of the elective. The last day of the first week of anything."
    "Murakami's lesson today is about the pause. Not the pause in the poem. The pause in the mouth. The silence between two words that means more than the words."
    "The professor asks me to say the word for the river. In Japanese. I say it. It comes out wrong. He does not correct me. He writes the right one on the board and leaves the wrong one there on purpose."
    mc "The wrong one is still mine."
    professor "It is. That is the first thing the language teaches. That the mistake is the door."
    "The night is the night of the third lesson. I have a word for the river now. I have a word for the frog. I have a word for the quiet."
    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump end_of_build
