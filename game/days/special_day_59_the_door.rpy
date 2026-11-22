################################################################################
## DAY 59: FRIDAY, JUNE 5, 2026
## Hikari asks a question she should not ask. At three in the morning, she is
## standing at his door. She is not looking at him. She is looking at the wall
## behind him. In the morning, she does not remember.
##
## Corruption level 2. The big beat. The thing that cannot be explained as a
## tile or a card or a vinegar bottle.
################################################################################

label special_day_59_the_door:
    $ set_story_day(59)
    $ corruption_level = 2
    call day_transition from _call_day_transition_59
    $ last_afternoon_place = None
    $ last_afternoon_hikari_tour = False

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Friday. Ten days of rain. I did not sleep after the footsteps. I lay in the dark and listened to the house reorder itself and I did not get up and I did not check."
    "The notebook is on the desk. I did not open it. The line is in there. She is leaking. I am not going to look at it today. I am going to look at Friday."
    mc "(Day fifty-nine. The voice did not come last night. The footsteps came instead. One or the other. Like they take turns.)"

    "My phone buzzes."

    $ run_chat("hikari", [
        {"them": "I have the afternoon free. The seminar is cancelled.", "options": [
            {"label": "\"Do you want to do something?\"",
             "send": "Do you want to do something?",
             "them": ["No.", "That came out wrong. I mean I want to be alone. Not away from you. Just alone."]},
            {"label": "\"I will see you at home.\"",
             "send": "I will see you at home.",
             "them": ["Yes.", "I am going to walk. I do not know where. I will know when I am there."]},
        ]},
    ])
    mc "(She wants to be alone. Not away from me. Just alone. There is a difference and she knows it and she is trying to tell me the difference.)"

    call murakami_daily_ping from _call_murakami_daily_ping_59

    scene bg_kitchen with walk_fade

    call corruption_morning from _call_corruption_morning_59

    "The kitchen. The clock on the wall is still stopped. I notice it and I do not mention it. Mother is at the counter. The vinegar is on the right. I do not move it."
    mother "You look tired."
    mc "I did not sleep well."
    mother "The rain. It does things to people. Your father does not sleep when it rains."
    father "I sleep. I just do not sleep well. There is a difference."
    mc "(There is a difference. Hikari said that yesterday. Not away from me. Just alone. The same sentence structure. The same shape of distinction.)"
    hikari "Good morning."
    "She is in the doorway. She looks like she slept. She looks like she did not sleep. Both things, at the same time, in the same face."
    mc "(She was in her room last night. The footsteps were not hers. The footsteps went from the stairs to the bathroom and back. Her room is past the bathroom. The footsteps stopped before her door. They were not hers.)"
    mc "(I am telling myself they were not hers. I am telling myself this because the alternative is that they were hers and she does not know it, and that is worse.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/school.mp3" fadein 2.0

    "The walk to the station. Hikari is with me. Her umbrella is up. Her stride is the Friday stride, which is longer than Monday but shorter than Wednesday."
    mc "(I am cataloguing her strides. I have started cataloguing her strides. This is not a thing a normal person does. This is a thing a person does when they are trying to hold someone in place.)"
    hikari "You are quiet."
    mc "I am thinking."
    hikari "About what?"
    mc "About the rain."
    hikari "That is a safe thing to think about. The rain does not mind being thought about."
    mc "(She says it lightly. She does not push. She used to push. She used to ask twice. Today she asks once and accepts the answer. Something has changed in her too. Or something has changed in me and I am projecting it onto her.)"

    scene bg_train_interior with walk_fade

    "The Friday train. I count the stops. Seven. The same seven. I am grateful for the seven. I am grateful for anything that does not change."
    mc "(I am grateful for the number seven. That is where I am. I am grateful for a number.)"

    scene bg_lecture_hall with walk_fade

    "Murakami is at the board. She has written one word: ikiru. To live."
    murakami "Today is the verb that is the reason for all the other verbs. Ikiru. To live. Not to survive. Not to exist. To live."
    murakami "The interesting thing about ikiru is that it does not have an object. You do not live something. You just live. The verb is complete without a target."
    mc "(She is teaching about living. About a verb that does not need an object. I am living. I am not living something. I am just living. That is the whole sentence. That is the whole condition.)"
    murakami "Some philosophers argue that ikiru implies purpose. That to live is to live for something. But the grammar does not support it. The grammar says: you live. The purpose is your invention."
    "She pauses. Not the stall from yesterday. A real pause. A teacher thinking."
    murakami "Do you think people can be made for something?"
    "She asks the class. Nobody answers. It is not a question that expects an answer. It is a question that expects silence."
    mc "(She asked it. The same question I am about to hear at dinner. She asked it here first. Or Hikari will ask it here second. The order does not matter. The question is in the air.)"

    menu:
        "Ask whether living needs a purpose.":
            mc "Ikiru. Can you say more about whether living needs a purpose?"
            murakami "Living does not need a purpose. People need a purpose. Those are different sentences. The verb does not care. The person cares."
            mc "(The verb does not care. The person cares. I am a person. I care. Hikari is a person. She cares. The house is not a person. Does the house care?)"
            $ reward_attributes_once("day59_lec_a", [("insight", "micro")], show="auto")
        "Ask what it means to live on purpose.":
            mc "Why does ikiru matter in a language lesson?"
            murakami "Because you are here. In this classroom. In this country. Learning this language. You are living. The question is whether you are living on purpose."
            mc "(Am I living on purpose. Am I here on purpose. Did I choose to come here or did the sentence choose me. The week is a machine. The machine runs a program. Am I the program.)"
            $ reward_attributes_once("day59_lec_b", [("grace", "micro")], show="auto")
        "Write the question in the margin.":
            "I write: ikiru. To live. The verb does not need a purpose. The person does."
            "My handwriting. My words. Today's page."
            "I close the notebook. I do not look at the other pages."
            $ reward_attributes_once("day59_lec_c", [("nerve", "micro")], show="auto")

    scene bg_campus_interior with walk_fade

    "The corridor. The third tile. I step on it. The pitch. It has stopped changing. It is the pitch it was yesterday. I do not know if that is stability or exhaustion."
    mc "(Maybe the tile has settled. Maybe I have settled. Maybe we have both given up and the pitch is the pitch and that is the end of it.)"

    call free_afternoon from _call_free_afternoon_59

    call corruption_post_visit from _call_corruption_post_visit_59

    scene bg_home_exterior_day with walk_fade
    stop music fadeout 2.0

    "The walk home. The rain is heavier today. The combini is on the corner. The card is in the window. I do not look at the card. I look at the card. The handwriting is the same as yesterday. Or it is not. I have stopped being able to tell."
    mc "(I have stopped being able to tell. That is the condition. Not that things are changing. That I cannot tell whether things are changing. The uncertainty is the thing. The uncertainty is the leak.)"

    scene bg_kitchen with walk_fade

    call dinner_open from _call_dinner_open_59

    "Hikari is quiet through dinner. Not the rested quiet. Not the heavy quiet. A different quiet. The quiet of someone who is about to say something and is deciding whether to say it."
    father "The rain."
    mother "The rain."
    mc "The rain."
    "We have become people who say the rain at dinner. That is the dinner now. The rain and the rice and the silence."
    hikari "Can I ask something?"
    mc "Yes."
    hikari "Do you think people can be made for something?"
    "The table is quiet. Father puts down his chopsticks. Mother looks at Hikari. I look at Hikari."
    "She is looking at her rice. She is not looking at us. She asked the question and now she is looking at her rice."
    hikari "I do not know why I said that."
    mc "(Murakami asked the same question this morning. In the lecture. Word for word. Do you think people can be made for something. Hikari was not in the lecture. Hikari was walking. She does not know Murakami asked it.)"
    father "That is a large question for a Friday."
    hikari "I know. I am sorry. I do not know where it came from."
    mother "Eat your rice."
    hikari "I am eating."
    mother "Then eat quietly. The question can wait."
    mc "(Mother said the question can wait. Not that the question was wrong. That it can wait. Like the question has a schedule. Like the question knows when it is supposed to be asked.)"

    call dinner_close from _call_dinner_close_59

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "The room. The desk. The notebook. The laundry rack. The window. The rain. The clock on the wall that I cannot hear from here but know is stopped."
    $ night_desk_line = "the window"
    call night_open from _call_night_open_59

    menu:
        "[tag_insight] Rank 3: Ask her to say the question again and listen for her own voice." if has_attribute("insight", 3):
            mc "Say it again. The question. I want to hear where your voice goes."
            hikari "Do you think people can be made for something."
            mc "Again. Slower."
            hikari "Do you think ... people can be made ... for something."
            mc "(The first time it was hers. The second time it was a sentence she was holding for someone else.)"
            hikari "You heard it."
            mc "I heard where it changes hands."
            $ log_memory("hikari", "said the question again, and he heard where her voice changed hands")
            $ reward_attributes_once("day59_night_again", [("insight", "micro")], show="auto")
        "Ask whose question she thought it was.":
            hikari "I asked a question at dinner. I do not know why."
            mc "It was a good question."
            hikari "It was not my question. That is the part I cannot explain. It came out of my mouth and it was not mine."
            mc "Whose was it?"
            hikari "I do not know. That is the part that scares me."
            mc "(She said scares me. She does not say scares me. She is the person who says she is fine. She is the person who handles things. She said scares me and that means the thing that said the question is bigger than a question.)"
            $ log_memory("hikari", "said the question at dinner was not hers, and that not knowing whose it was scares her")
            $ reward_attributes_once("day59_night_a", [("grace", "micro")], show="auto")
        "Tell her where you first heard the question.":
            mc "Murakami asked the same question. This morning. In the lecture. Word for word."
            hikari "She did?"
            mc "Do you think people can be made for something. That is what she said. That is what you said."
            hikari "I was not in the lecture."
            mc "I know."
            hikari "Then how did I say it?"
            mc "I do not know."
            "She is quiet for a long time. She is looking at the wall. Not the window. The wall."
            hikari "I do not know how I said it. That is the true thing I am telling you."
            $ log_memory("hikari", "could not explain how she said the same question Murakami asked in a lecture she did not attend")
            $ reward_attributes_once("day59_night_b", [("nerve", "micro")], show="auto")
        "Say nothing. Stand in the doorway.":
            "The rain. The city. The Friday sounds. The dog barks three times. It is Friday. The dog barks on Friday. I did not know that. Or I forgot."
            "Hikari is on the floor. She is not sleeping. She is looking at the ceiling. She is mouthing something. I cannot read lips in the dark."
            $ log_memory("hikari", "was mouthing something in the dark, looking at the ceiling, and I could not read it")
            $ reward_attributes_once("day59_night_c", [("insight", "micro")], show="auto")

    call night_close from _call_night_close_59

    call corruption_night from _call_corruption_night_59

    "I lie in the dark. The house is doing its sounds in the wrong order. The pipes, the street, the fridge. I am learning the new order. I am adapting. That is what people do. They adapt to the wrong thing and call it normal."
    "Then I wake."
    "Not from sleep. From the absence of sound. The house has gone quiet. All of it. All six sounds, gone."
    "I open my eyes."
    "Hikari is standing at the door."
    "The door is open. She is in the doorway. She is facing me but she is not looking at me. She is looking at the wall behind me. Her eyes are open. They are open the way eyes are open when the person behind them is somewhere else."
    mc "Hikari."
    "She does not respond."
    mc "Hikari."
    "She does not respond. She is standing in the doorway in her pyjamas and her eyes are open and she is looking at the wall and she is not here."
    "I sit up. I say her name a third time."
    mc "Hikari."
    "She blinks."
    "The blink is slow. The blink is the thing that brings her back. The eyes focus. The face changes. She is Hikari again."
    hikari "I was getting water."
    mc "You were standing at my door."
    hikari "Was I?"
    mc "For a minute. Maybe longer."
    hikari "I am sorry. I was getting water. I must have stopped."
    "She turns. She walks down the hall. I hear the kitchen tap. I hear the glass. I hear her go back to her room and close the door."
    "I do not sleep."
    "The laundry rack is in the corner. The notebook is on the desk. The rain is on the window. The clock on the kitchen wall is stopped."
    "And Hikari was standing at my door, looking at the wall behind me, and she was not there."
    $ collect_notebook_line(59)

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
