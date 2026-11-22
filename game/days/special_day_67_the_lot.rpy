label special_day_67_the_lot:
    $ set_story_day(67)
    call day_transition from _call_day_transition_67
    $ flush_pending_messages()

    scene bg_ramen_shop_destroyed with walk_fade
    stop music fadeout 1.0
    "I come back because the photo won't load. There's a gray square where the shop ought to be. I thought it was the phone."
    "I stop where the door was. The counter is still there. The red lantern is on the ground, half full of rain."
    "A woman from the next shop comes out with a bucket. I ask when they took it down."
    "She tells me last winter."
    mc "The ramen shop?"
    "She tips her bucket into the gutter."
    "There wasn't a ramen shop. It was a storeroom."
    "She says it kindly and moves her bucket so I have room to pass."

    menu:
        "Take out Chef's chopsticks." if has_item("chef_personal_chopsticks"):
            "I take the chopsticks out of their wrapping. I had been saving them for a meal I wouldn't eat in a hurry."
            "I almost ask her to look at them. I don't know what I'd expect her to see."
            $ keepsake_observations["chef_personal_chopsticks"] = "The neighbor says this was a storeroom, wrecked last winter. Yesterday I stood outside and read Chef's notice."
        "Look at the fallen menu.":
            "I can still read the price of a bowl through the dirt. I think about pointing it out to her. She's already back inside."
        "Try the photo again.":
            "This time it opens. The date is yesterday. In the picture there's a wall with a number on it, and no window to tape anything to."

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    "Hikari is waiting outside. She has the review sheet on her phone."
    hikari "It still matches."
    mc "Can you send it to me anyway?"
    hikari "I already did. Check before you go upstairs."
    "My phone buzzes in my hand. She waits until I open the message."

    jump act2_day_router
