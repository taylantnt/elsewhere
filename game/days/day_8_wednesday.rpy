################################################################################
## DAY 8 — WEDNESDAY, APRIL 15, 2026 (THE FUSE)
################################################################################

label wednesday_morning:
    $ set_story_day(8)
    call day_transition

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "I wake before the alarm. I know what day it is without looking at the phone."
    "Three days since the library. Two since the quiz. The midterm is four weeks out, maybe five, and the calendar in my head has started counting down like a fuse."
    mc "(It is a fuse. I do not know who keeps it, or why I do, but it is a fuse.)"
    "The class is on the history of haiku. Not the dates. The shape."
    "The professor says the thing I have been circling without knowing: that a poem about a frog is a poem about the whole world if the whole world is small enough to notice."
    hikari "He says that like he has said it before. He has said it before. He says everything like that."
    mc "You think Basho knew? About the frog. I mean. You think he was writing about anything else?"
    hikari "I think he was writing about the river. And that the river was the whole country, and the country was the whole quiet."
    menu:
        "Write the poem down before the bell.":
            mc "I write it down. The frog. The river. The quiet."
            $ reward_attributes_once("midterm_haiku_write", [("grace", "micro")], show="auto")
        "Just listen. The listening is the lesson.":
            mc "I just listen. The listening is the lesson."
            $ reward_attributes_once("midterm_haiku_listen", [("insight", "micro")], show="auto")
    "The night is ordinary. That is the point. The ordinary is what the fuse is made of."
    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump thursday_morning
