################################################################################
## DAY 63: TUESDAY, JUNE 9, 2026
## The threshold. The house is still growing. The family is exactly the same as
## Day 1. The wall where the twelfth door was is warm. In the dream, MC is
## conscious. He can see the monitor. He can see himself. And someone else.
##
## Corruption level 3. The last hybrid day. After this, the hub closes.
## Act 3 proper begins.
################################################################################

label special_day_63_the_threshold:
    $ set_story_day(63)
    $ corruption_level = 3
    call day_transition from _call_day_transition_63
    $ last_afternoon_place = None
    $ last_afternoon_hikari_tour = False

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Tuesday. Fourteen days of rain. Two weeks. The rain has been here for two weeks and the house has been growing for two weeks and I have been counting for two weeks and the notebook has three lines in it that I did not write."
    "I measured the room. Eleven spans. Stable. I measured the hallway. Sixteen steps. It was fourteen yesterday. It grew two more."
    mc "(I used to count how many days I had left before I went home. Now I count the steps to the kitchen.)"

    "My phone buzzes."

    $ run_chat("hikari", [
        {"them": "I measured the hallway. Sixteen steps. You were right.", "options": [
            {"label": "\"What do we do?\"",
             "send": "What do we do?",
             "them": ["I do not know.", "I think the question is not what we do. The question is what is being done."]},
            {"label": "\"Are you scared?\"",
             "send": "Are you scared?",
             "them": ["Yes.", "That is new. I do not usually say yes to that question."]},
        ]},
    ])
    mc "(She said yes. She said she is scared. She said that is new. Hikari does not say she is scared. Hikari handles things. Hikari is the one who knows where the free rooftop is. Hikari is the one who has an answer. She said yes.)"

    call murakami_daily_ping from _call_murakami_daily_ping_63

    scene bg_kitchen with walk_fade

    call corruption_morning from _call_corruption_morning_63

    "The kitchen. Eight tiles. The table. Father. Mother. Hikari. Rice. Miso. The stopped clock."
    "I look at them. I look at them the way I looked at the room when I measured it. I am looking for the thing that has changed."
    father "Good morning."
    mc "Good morning."
    father "The rain."
    mother "The rain."
    hikari "The rain."
    "They all say it. The rain. Three voices. The same word. The same cadence. The same pause after."
    "Father finishes his rice before he touches the paper. Mother sets her bowl down and reaches for the cloth."
    "I wait for Hikari to put her chopsticks down. She does, in the same place as yesterday."
    "I move mine to the other side of the bowl."
    mc "(Or I am the one who is the same. I am the one who is watching them and seeing patterns because I am looking for patterns. Murakami taught that. The mind consolidates. It finds the shape even when there is no shape.)"
    mc "(But the hallway is sixteen steps. The room is eleven spans. The notebook has three lines I did not write. The shapes are there. The shapes are measurable.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/school.mp3" fadein 2.0

    "The walk to the station. Hikari is with me. She is quiet. Not the quiet of rest. Not the quiet of exhaustion. The quiet of someone who has stopped pretending the quiet is temporary."
    hikari "I said the sentence yesterday. At breakfast. I know I said it."
    mc "You caught it."
    hikari "I caught it. But I did not stop it. It came out of my mouth and I did not decide to say it and I could not stop it."
    mc "I know."
    hikari "Do you know what that feels like?"
    mc "No."
    hikari "It feels like being a radio. Someone else is broadcasting and you are just the speaker."
    mc "(A radio. A speaker. A machine that outputs what it receives. She is describing herself as a device. She is describing herself as a thing that receives and transmits. She does not know she is describing herself as a thing.)"

    scene bg_train_interior with walk_fade

    "The train. I count the stops. Eight. The eighth station is there again. The name I do not recognise. The gap that was not there before Friday."
    "I get off at the seventh. The campus is at the seventh. I do not get off at the eighth. I do not want to know what is at the eighth."
    "From the platform I watch the train leave for the stop that doesn't belong on the line."

    scene bg_lecture_hall with walk_fade

    "Murakami is at the board. She has written one word: mon. Gate. Threshold."
    murakami "Today is the word for the boundary. Mon. The gate. The threshold. The line between here and there, between inside and outside, between what you are and what you are becoming."
    murakami "In Japanese architecture, the mon is the most important part of the house. Not the rooms. The gate. Because the gate decides what comes in. The gate decides what goes out."
    mc "(The gate. The threshold. The twelfth door. The wall where the door was. The wall that is warm.)"
    murakami "The interesting thing about a mon is that you do not always know you have crossed it. Some thresholds are marked. Some are not. You walk through a gate and you do not know you have walked through it until you are on the other side and cannot go back."
    mc "(I am on the other side. I have been on the other side since Day fifty-one. Since Hikari said the sentence. Since the room tore. Since the notebook started writing itself. I crossed the threshold and I did not know it and now I am here.)"

    menu:
        "Ask how you notice an unmarked threshold.":
            mc "Mon. Can you say more about thresholds you do not notice?"
            murakami "Most thresholds are invisible. You do not see them because you are looking at the thing beyond them. You see the room, not the door. You see the day, not the morning. The threshold is the gap. The ma. The thing that is not there."
            mc "(The threshold is the gap. The gap is the ma. The ma is what Murakami taught on Day fifty-six. The gap that appears when something moves. Something has moved. I am on the other side of the gap.)"
            $ reward_attributes_once("day63_lec_a", [("insight", "micro")], show="auto")
        "Ask whether you can cross back.":
            mc "Why does the threshold matter in a language lesson?"
            murakami "Because you are at one. Every student is at one. You are crossing from not-knowing to knowing. You cannot go back. That is what a threshold is. A direction that does not reverse."
            mc "(A direction that does not reverse. I cannot go back to before the sentence. I cannot go back to before the laundry rack. I cannot go back to before the notebook. The threshold is a direction and it only goes one way.)"
            $ reward_attributes_once("day63_lec_b", [("grace", "micro")], show="auto")
        "Write the threshold in your own hand.":
            "I write: mon. Threshold. A direction that does not reverse."
            "Below it, in my handwriting: I am on the other side."
            "I look at the page. Today's page. My words. My handwriting. And below them, the three lines from the other hand. She is leaking. She does not know. He can see."
            "Four lines now. Three that are not mine. One that is. They are on the same page. They are in the same notebook. The notebook does not know the difference."
            $ reward_attributes_once("day63_lec_c", [("nerve", "micro")], show="auto")

    scene bg_campus_interior with walk_fade

    "The corridor. The third tile. I step on it. It does not squeak."
    "The tile is silent. The tile has stopped squeaking. After all the changes, all the pitches, the tile has gone quiet."
    mc "(The tile has stopped. The tile was the first thing and now it is the last thing and it has stopped. That is either the end of the corruption or the beginning of something else. The silence is worse than the squeak.)"

    call free_afternoon from _call_free_afternoon_63

    call corruption_post_visit from _call_corruption_post_visit_63

    scene bg_home_exterior_day with walk_fade
    stop music fadeout 2.0

    "On the walk home I pass the combini without looking at the card in the window. I want to see the house from across the street."
    "The house is the house. From the outside, it is the same house. The same roof. The same gate. The same genkan. The house does not look bigger from the outside. The house only grows from the inside."
    mc "(The house grows from the inside. Like a body. Like a room that is filling with something that is not air. The house is a body and something is growing in it.)"

    scene bg_kitchen with walk_fade

    call dinner_open from _call_dinner_open_63

    "Dinner. The table. Father. Mother. Hikari. Rice. Miso. The stopped clock."
    "I watch them. I watch them the way I watched them this morning. Father eats rice first. Mother eats miso first. Hikari eats rice, then nothing, then rice."
    "They are the same. They are exactly the same as this morning. They are exactly the same as Day one. The same order. The same rhythm. The same pauses."
    father "How was school?"
    mc "Good."
    father "Good."
    mother "Eat your rice."
    hikari "The rain."
    father "The rain."
    mother "The rain."
    mc "(They are a loop. They are a machine. The week is a machine. The day is a machine. The dinner is a machine. They run the same program and the output is always the same and they do not know it.)"
    mc "(Or I am the machine. I am the one who is seeing the loop. I am the one who is counting the repetitions. Maybe they are just people having dinner and I am the one who has become a counter, a measurer, a witness to patterns that are not there.)"
    mc "(But the hallway is sixteen steps. The room is eleven spans. The notebook has three lines I did not write. The tile has gone silent. The train has eight stops. The room tore last night. These are not patterns I am imagining. These are measurements.)"
    father "You are not eating."
    mc "I am thinking."
    father "Think after dinner. Dinner is for eating."
    mother "He is right. Eat."
    "I eat. The rice is rice. The miso is miso. The dinner is dinner."

    call dinner_close from _call_dinner_close_63

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "The room. Eleven spans. The desk. The notebook. The laundry rack. The window. The rain. The wall."
    $ night_desk_line = "the wall"
    call night_open from _call_night_open_63

    menu:
        "[tag_grace] Rank 3: Offer to measure the hallway together." if has_attribute("grace", 3):
            mc "Let us measure it together. Then neither of us is alone with it."
            hikari "I measured sixteen steps."
            mc "Then I will walk them with you and count out loud."
            $ reward_attributes_once("day63_night_together", [("grace", "micro")], show="auto")
        "Ask what she found in the library.":
            hikari "I went to the library. I stopped reading about somnambulism. I started reading about something else."
            mc "What?"
            hikari "Houses. Japanese houses. The architecture. The way they are built. The way they grow."
            mc "Houses do not grow."
            hikari "I know. That is what the books say. Houses do not grow. Houses are built and they stay the size they are built."
            mc "But ours is growing."
            hikari "Yes."
            mc "And you believe me."
            hikari "I measured the hallway. Sixteen steps. I believe the hallway."
            $ log_memory("hikari", "stopped reading about somnambulism and started reading about houses, said houses do not grow but ours is growing")
            $ reward_attributes_once("day63_night_a", [("grace", "micro")], show="auto")
        "Tell her breakfast and dinner felt identical.":
            mc "I watched Dad put the paper down at breakfast. At dinner I knew exactly when he'd set his bowl down. I counted it out, and he did."
            hikari "They are people. People have routines."
            mc "I know what their routine looks like. This felt like watching it happen for a second time."
            hikari "Maybe. Or maybe you are seeing a program because you are looking for one."
            mc "The hallway is sixteen steps."
            hikari "I know."
            mc "The tile stopped squeaking."
            hikari "I know."
            mc "Something is wrong with the house."
            hikari "I know."
            "She says it. I know. Twice. She says it the way she says everything. Flat. Warm. But underneath, something else. Something that is not flat. Something that is not warm."
            $ log_memory("hikari", "said she knows something is wrong with the house, twice, and there was something underneath the flatness")
            $ reward_attributes_once("day63_night_b", [("nerve", "micro")], show="auto")
        "Say nothing. Keep the door open.":
            "The rain. The city. The Tuesday sounds. No dog. No bell. Just the rain and the fridge and the silence between them."
            "Hikari is on the floor. She is not sleeping. She is looking at the wall. The same wall I am looking at. The wall that has the twelfth door on the other side of it."
            $ log_memory("hikari", "was looking at the same wall I was looking at, the wall with the twelfth door on the other side")
            $ reward_attributes_once("day63_night_c", [("insight", "micro")], show="auto")

    hikari "Can you leave tomorrow afternoon free? I want to go back to the river. The place with the lights."
    mc "For the fireflies?"
    hikari "No. I want to see it in daylight."
    if not all_confidants_maxed():
        "I start to say there is someone I meant to see. She waits for me to finish. I don't."
    else:
        "For once there is nobody I have promised to see. It is a strange feeling, having the time when she asks for it."
    mc "I'll come."

    call night_close from _call_night_close_63

    call corruption_night from _call_corruption_night_63

    "I do not lie down. I get up. I walk to the wall."
    "The wall where the twelfth door was. The door I touched on Day forty-one. The door that is not there. The wall that is just a wall."
    "I put my hand on it."
    "The wall is warm."
    "Not the warmth of a room. Not the warmth of a pipe behind the plaster. A different warmth. The warmth of something on the other side. The warmth of something alive."
    mc "(The wall is warm. The wall has never been warm. The wall is plaster and wood and insulation and it does not generate heat. But it is warm. There is something on the other side.)"
    "I press my palm against it. The warmth pushes back. Not pressure. Presence. The feeling of something leaning against the other side of the wall, the way I am leaning against this side."
    "I close my eyes."
    "I am in the white room."
    "I open my eyes. The room is white. The ceiling is white. The walls are white. The bed is white. I am in the bed."
    "I can see the monitor. To my left. Green lines. Numbers. A heart rate. A brain rate. Words I cannot read at this angle."
    "I can see the wires. They come from my arms. They go to the machines. The machines hum. The machines are the only sound."
    "I can see myself. In the bed. Eyes closed. Breathing. Asleep. I am looking at myself from above. I am floating. I am not floating. I am the camera."
    "And I can see someone else."
    "A figure. Standing by the door. The door of the white room. Not the door of my room. The door of this room. The room I am in. The room I can see."
    "The figure is facing me. Facing the bed. Facing the version of me that is sleeping. The figure is watching me sleep."
    "I cannot see the figure's face. The figure is a shape. A silhouette. The shape of a person who is standing very still and watching very carefully."
    "I try to speak. I cannot speak. I am the camera. The camera does not have a mouth."
    "The figure moves. It turns its head. It is looking at me. Not at the sleeping me. At the camera me. At the me that is watching."
    "It knows I can see."
    # ChromaGlitch: the hospital scene tears.
    show layer master at glitch
    pause 0.15
    show layer master

    "I am in my room. My hand is on the wall. The wall is warm. The laundry rack is in the corner. The rain is on the window. The notebook is on the desk."
    "I take my hand off the wall. The warmth fades. The wall is just a wall."
    mc "(I was there. I was in the white room. I could see the monitor. I could see myself. I could see the figure. And the figure could see me. It knew I was watching. It turned its head and it looked at me and it knew.)"
    "I sit on the bed. I do not sleep. I sit and I look at the wall and the wall is just a wall and I know it is not just a wall."
    "The notebook is on the desk. I do not open it. I do not need to open it. I know what the fourth line says. I know what the hand that is not mine is writing."
    "It says: \"He is at the door.\""
    $ collect_notebook_line(63)

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
