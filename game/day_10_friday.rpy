################################################################################
## DAY 10 — FRIDAY, APRIL 17, 2026 (THE ELECTIVE: MURAKAMI)
################################################################################

label friday_morning:
    $ set_story_day(10)
    call day_transition
    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "The night of the long fuse is over. The fuse was shorter than I thought."
    "I wake on Friday. The room is the room. The receipt is on the desk. The phone is face-down. The week is not over, but the part that was a countdown is."
    "And that is when the notice arrives."

    # The elective: the Japanese course, taught by Murakami.
    professor "You passed the midterm."
    mc "I passed."
    professor "You passed the frog. Or the river. It does not matter which one you chose. The choosing was the lesson."
    menu:
        "Take the Japanese course. The elective with Murakami.":
            mc "Then I will take the Japanese course. The elective. With you."
            professor "Good. The language is not a subject. It is a country you walk into. I will be your teacher for it."
            $ japanese_fluency = min(5, japanese_fluency + 1)
        "I need a weekend first.":
            mc "I need a weekend first."
            professor "Take it when you take it. The door is not going anywhere. Neither is the quiet."
            $ japanese_fluency = min(5, japanese_fluency + 1)

    # First Murakami lesson: the sound of the name.
    "His first lesson is not about grammar. It is about the sound of the name."
    "He says the word for the river the way you would say a prayer. Or the way you would say a secret."
    "The room is quiet in a way that has a texture. The professor does not fill it. He does not need to."
    "The night after the first lesson is not a night of the fuse. It is a night of small sounds. The kettle. The refrigerator. The rain that is not rain."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump saturday_recovery
