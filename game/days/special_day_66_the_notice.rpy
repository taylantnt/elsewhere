label special_day_66_the_notice:
    $ set_story_day(66)
    call day_transition from _call_day_transition_66
    $ flush_pending_messages()

    scene bg_campus_interior with walk_fade
    "Hikari finds me on the stairs at lunch. I give her the review sheet and wait while she reads both sides."
    hikari "Which part did you write?"
    "I show her. She takes a picture. She makes me keep the paper."
    hikari "Let's see whether they still match tomorrow."

    scene bg_ramen_shop_closed with walk_fade
    "On the way home I stop at the ramen shop. There's no noren. I can see the strip of wall it used to hang against."
    if has_item("chef_personal_chopsticks"):
        "I knew he was going home. A notice in the window shouldn't make it feel like news."
    else:
        "I was thinking about what to order all the way from the station. It takes me a while to stop thinking about it."
    "The notice says he's gone home to care for his parents. Someone has taped the top corners from the outside. The bottom edge lifts when a bicycle goes by."
    "I take a picture of the notice. It's too small to read on my phone, so I step closer and take another."

    scene bg_kitchen_night with walk_fade
    mother "Did you eat?"
    mc "I thought I would."
    "She sets another bowl down without asking where I went. It's still warm when I finish."

    jump act2_day_router
