################################################################################
## DAY 9 — THURSDAY, APRIL 16, 2026 (THE MIDTERM)
################################################################################

label thursday_morning:
    $ set_story_day(9)
    call day_transition
    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    scene bg_lecture_hall with walk_fade
    play music "audio/Music/classroom.mp3" fadein 1.0
    "The hall is the same hall. Forty seats, the same window, the same chalkboard of dates."
    professor "The midterm. You know the shape. The syllable. The season. The pause."
    "I take the seat by the window. Hikari is already there, notebook open, pen out, sitting exactly where she would have sat if she had been here since breakfast."
    menu:
        "The frog was the whole world.":
            mc "The frog was the whole world."
            $ reward_attributes_once("midterm_q1_frog", [("insight", "micro")], show="auto")
        "The river was the whole world.":
            mc "The river was the whole world."
            $ reward_attributes_once("midterm_q1_river", [("grace", "micro")], show="auto")
    "The night is the night of the long fuse. I sleep badly. I do not know if I slept at all."
    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump friday_morning
