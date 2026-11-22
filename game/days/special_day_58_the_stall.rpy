################################################################################
## DAY 58: THURSDAY, JUNE 4, 2026
## Mother stalls. MC moves a kitchen item and she freezes, repeats a rule,
## resets, does not remember. Murakami uses the word fragment in lecture.
## The hub is open but one row is dark.
##
## Corruption level 2. The wrongness is no longer ambient. It has a shape.
################################################################################

label special_day_58_the_stall:
    $ set_story_day(58)
    $ corruption_level = 2
    call day_transition from _call_day_transition_58
    $ last_afternoon_place = None
    $ last_afternoon_hikari_tour = False

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Thursday. Nine days of rain. The notebook is on the desk. I opened it this morning. The line is still there. She is leaking. The handwriting is still not mine."
    "I closed the notebook. I am going to have a Thursday. The Thursday does not care about the notebook."
    mc "(Day fifty-eight. If the voice comes back tonight, it will say fifty-eight. I am counting the days the way the voice counts them. I do not know if that means I am the voice or the voice is me.)"

    "My phone buzzes."

    $ run_chat("hikari", [
        {"them": "The seminar went well. The professor said my paper was the best in the cohort.", "options": [
            {"label": "\"That is great.\"",
             "send": "That is great.",
             "them": ["It is.", "I do not know why I do not feel great about it."]},
            {"label": "\"Why not?\"",
             "send": "Why not?",
             "them": ["Because the paper was about repetition.", "And now I am repeating. The feeling. The morning. The walk."]},
        ]},
    ])
    mc "(She says she is repeating. She does not know what she is repeating. She thinks it is a feeling. I think it is a pattern.)"

    call murakami_daily_ping from _call_murakami_daily_ping_58

    scene bg_kitchen with walk_fade

    call corruption_morning from _call_corruption_morning_58

    "Mother is at the counter. She is making miso. The kitchen smells like the inside of a warm building, which is what it is."
    "I open the cabinet to find the tea. The tea is behind the soy sauce. The soy sauce is behind the rice vinegar. I move the vinegar to the left to reach the soy sauce."
    mother "Stop."
    "Her voice is not loud. It is not angry. It is flat. The same pitch as the voice through the wall."
    mother "Nothing should change. We always do it this way."
    "She is looking at the vinegar. She is not looking at me. Her hand is on the counter and it is not moving."
    mother "The vinegar is on the right. The soy sauce is on the left. That is how it is. That is how it has always been."
    mc "Mother, I just moved it to reach the tea."
    "She does not respond. She is looking at the vinegar. Her hand is on the counter. She is not moving."
    "I put the vinegar back. I put it on the right, where it was."
    mother "Thank you. The miso is almost ready."
    "She turns back to the pot. She stirs. She hums. She is Mother again."
    mc "(She does not remember. She is already past it. She is stirring miso and humming the tune she hums every morning. The thirty seconds where she was not Mother are gone, like they were edited out.)"
    mc "(Nothing should change. We always do it this way. She said it like a rule. Like a line of code. Like a thing that is written somewhere and she was reading it.)"

    father "Good morning."
    mc "Good morning."
    father "You look like you saw something."
    mc "I moved the vinegar."
    father "You should not move the vinegar."
    mc "(He says it lightly. Like a joke. Like he is agreeing with Mother. But Mother is not here anymore. Mother is at the pot. Father is the one who said it this time.)"
    hikari "What happened to the vinegar?"
    mc "Nothing. I moved it and I put it back."
    hikari "Good. The vinegar has a place."
    mc "(Three people. Three versions of the same sentence. The vinegar has a place. Nothing should change. You should not move it. They are not coordinating. They are not aware of each other. They are all saying the same thing from different directions.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/school.mp3" fadein 2.0

    "The walk to the station. Hikari is quiet. Not the rested quiet of yesterday. The other quiet. The one that has weight."
    mc "(She is thinking about the vinegar. Or she is not thinking about the vinegar and she is quiet for a different reason. I cannot tell. I have stopped being able to tell.)"

    scene bg_train_interior with walk_fade

    "The train. The Thursday train. I count the stops. Seven. The same seven. I am sure they are the same seven. I am sure because I am counting them, and counting is the only thing I trust right now."
    mc "(Seven stops. Seven. If the train finds an eighth, I will know something is wrong. If it does not, I will know nothing. The absence of an eighth stop is not evidence of normalcy. It is just the absence of an eighth stop.)"

    scene bg_lecture_hall with walk_fade

    "Murakami is at the board. She has written one word: kakera. Fragment."
    murakami "Today is the word for a piece of something that was whole. Kakera. A shard. A fragment. The part that is left when the rest has broken or been taken."
    murakami "In Japanese literature, the fragment is not a failure of form. It is the form. Many of the great works are fragments. They were never finished. They were never meant to be finished. The fragment is the honest shape of experience."
    "She stops."
    "She is looking at the board. At the word she wrote. Her pen is in her hand and she is not moving."
    mc "(She is doing what Mother did. The stall. The freeze. The thirty seconds of not being there.)"
    "Then she blinks. She turns to the class."
    murakami "I am sorry. I lost my place. Where was I?"
    "A student tells her. She nods. She continues."
    murakami "The fragment. Yes. The fragment is honest because it does not pretend to be the whole. It says: I am this much. The rest is somewhere else."
    mc "(She said fragment and she stalled. She said fragment and she forgot where she was. The word did something to her. Or she did something with the word. I do not know which.)"

    menu:
        "Ask what a fragment knows about itself.":
            mc "Kakera. Can you say more about what the fragment knows?"
            murakami "The fragment knows its own shape. It does not know the shape of the whole. That is the tragedy and the honesty. It is a piece that does not have the blueprint."
            mc "(A piece that does not have the blueprint. I am a piece. Hikari is a piece. The house is a piece. None of us have the blueprint.)"
            $ reward_attributes_once("day58_lec_a", [("insight", "micro")], show="auto")
        "Ask whether you can ever learn the whole language.":
            mc "Why does the fragment matter in a language lesson?"
            murakami "Because every sentence is a fragment of a thought. Every conversation is a fragment of a relationship. Every word is a fragment of a language. You are learning fragments. You will never learn the whole. Nobody does."
            mc "(She says it like it is a comfort. It is not a comfort. It is a description of the condition.)"
            $ reward_attributes_once("day58_lec_b", [("grace", "micro")], show="auto")
        "Write the fragment down exactly.":
            "I write: kakera. Fragment. The part that is left when the rest has broken or been taken."
            "I do not look at the previous pages. I write on today's page. My handwriting. My words."
            "But the pen feels different in my hand. Not heavier. Not lighter. Just different. Like the hand that holds it has shifted by a degree."
            $ reward_attributes_once("day58_lec_c", [("nerve", "micro")], show="auto")

    scene bg_campus_interior with walk_fade

    "The corridor. The third tile. I step on it. The pitch is higher again. Fourth change. Or fifth. I have lost count of the changes, which means the tile is winning."
    mc "(The tile is not winning. The tile is a tile. I am the one who is losing track. I am the fragment that does not have the blueprint.)"

    call free_afternoon from _call_free_afternoon_58

    call corruption_post_visit from _call_corruption_post_visit_58

    scene bg_home_exterior_day with walk_fade
    stop music fadeout 2.0

    "The walk home. The combini is on the corner. I do not look at the card. I look at the card. The handwriting has changed again. Or it has not. I cannot tell anymore. The card is a card and the handwriting is handwriting and I am the one who is different."
    mc "(I am the fragment. That is what Murakami said. The fragment does not know the shape of the whole. I do not know the shape of the whole. I am in it and I cannot see it.)"

    scene bg_kitchen with walk_fade

    call dinner_open from _call_dinner_open_58

    mother "You are home."
    mc "I am home."
    mother "Good. The miso is ready."
    mc "(She says miso. She made miso this morning. She stalled this morning over the vinegar and now she is making miso and she does not remember the vinegar. I want to ask her. I do not ask her.)"
    father "How was school?"
    mc "Good. Murakami taught about fragments."
    father "Fragments. That is a good word. A word that knows what it is."
    hikari "A fragment is honest. That is what my paper said about repetition. The repetition is honest because it does not pretend to be the first time."
    mc "(They are all saying the same thing. From different directions. Without coordinating. The fragment. The repetition. The honesty of not pretending. They are all reading from the same page and none of them know it.)"

    call dinner_close from _call_dinner_close_58

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "The room. The desk. The notebook. The laundry rack. The window. The rain."
    $ night_desk_line = "the notebook"
    call night_open from _call_night_open_58

    menu:
        "[tag_grace] Rank 3: Ask whether she is afraid of what she does not remember." if has_attribute("grace", 3):
            mc "When you forget something. The way Mother does. Does it frighten you?"
            hikari "I do not forget."
            mc "I did not say you did. I asked if it frightens you."
            "She is quiet. The rain keeps its side of the conversation."
            hikari "Yes. It frightens me more than the thing I cannot see."
            mc "(I do not tell her it will be all right. I do not know that. I stay.)"
            $ log_memory("hikari", "admitted that forgetting frightens her more than the thing she cannot see")
            $ reward_attributes_once("day58_night_afraid", [("grace", "micro")], show="auto")
        "Ask where she heard the word fragment.":
            hikari "The seminar. The paper. The rain. The fragment."
            mc "You said fragment."
            hikari "Everyone said fragment. It is the word of the day."
            mc "It is the word of more than the day."
            hikari "Maybe. Words do that. They arrive and they do not leave. Like guests who have finished the tea but not the conversation."
            $ log_memory("hikari", "said words arrive and do not leave, like guests who finished the tea but not the conversation")
            $ reward_attributes_once("day58_night_a", [("grace", "micro")], show="auto")
        "Tell her what happened when you moved the vinegar.":
            mc "Mother stalled this morning. I moved the vinegar and she froze. She said nothing should change."
            hikari "She does that."
            mc "She does?"
            hikari "When I was small. I moved the cups. She stood at the counter for a full minute. Then she was fine. She does not like the kitchen to change."
            mc "She did not remember."
            hikari "She never remembers. That is the shape of it. The stall and then the forgetting. It is just how she is."
            mc "(She says it like it is normal. Like Mother has always done this. Like the stall is a quirk and the forgetting is a feature. Maybe she is right. Maybe I am the one who is hearing it wrong.)"
            $ log_memory("hikari", "said Mother has always stalled when the kitchen changes, and never remembers, and it is just how she is")
            $ reward_attributes_once("day58_night_b", [("nerve", "micro")], show="auto")
        "Say nothing. Let the stall close around you.":
            "The rain. The city. The Thursday sounds. The dog does not bark on Thursdays. Or I have not noticed it barking on Thursdays. The absence of a thing is not the same as the thing not being there."
            "Hikari is on the floor. She is sleeping. She is breathing the way she breathed last night, before the voice through the wall."
            $ log_memory("hikari", "was sleeping and breathing the same way as before the voice through the wall")
            $ reward_attributes_once("day58_night_c", [("insight", "micro")], show="auto")

    call night_close from _call_night_close_58

    call corruption_night from _call_corruption_night_58

    "I lie in the dark. The house is doing its sounds. But they are in the wrong order."
    "The pipes first. Then the street. Then the fridge. Like the sequence shifted. Like someone reordered the list."
    mc "(A list. That is the word that came. Not a pattern. A list. Like someone wrote the sounds down and put them in the wrong order.)"
    "Then, at three in the morning, footsteps."
    "Not from Hikari's room. From the hallway. The hallway between my room and the stairs."
    "I do not get up. I do not open the door. I listen."
    "The footsteps are slow. Even. They go from the stairs to the bathroom and back. Then they stop."
    "The house is quiet."
    "I do not sleep for a long time after that."
    $ collect_notebook_line(58)

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
