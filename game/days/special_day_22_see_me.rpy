################################################################################
## DAY 22: WEDNESDAY, APRIL 29, 2026
## The professor's follow-up. He asked for one question. I brought forty.
################################################################################

label special_day_22_see_me:
    $ set_story_day(22)
    call day_transition from _call_day_transition_15

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Wednesday. The fourth week starts with a thing I have been carrying since Tuesday."
    "The exam paper is still on the desk. The red words have not faded. Neither have the other ones, the ones I did not write but the professor wrote back."
    mc "(He asked for one question. I have forty. I have had forty since before I came to Japan.)"

    "My phone buzzes."

    if "tanaka" in wire_unlocked:
        $ run_chat("tanaka", [
            {"them": "The afternoon shift is open today. Do you want it?", "options": [
                {"label": "\"I have class.\"",
                 "send": "I have class.",
                 "them": ["Then you have class. The shift is not going anywhere."]},
                {"label": "\"I will come after.\"",
                 "send": "I will come after.",
                 "them": ["After what?", "After you are done being a student. Then you are a worker. Bring your IC."]},
            ]},
        ])
        mc "(He is not wrong. The student part is ending. The worker part is starting. The gap between them is where I live.)"
    else:
        $ run_chat("hikari", [
            {"them": "Are you going to see him again?", "options": [
                {"label": "\"Yes.\"",
                 "send": "Yes.",
                 "them": ["What question are you bringing?", "You cannot bring all of them."]},
                {"label": "\"I have forty.\"",
                 "send": "I have forty.",
                 "them": ["Then you will have to choose one. That is what the number forty means."]},
            ]},
        ])
        mc "(Forty questions. One answer. The ratio is wrong. But it is the only ratio I have.)"

    call murakami_daily_ping from _call_murakami_daily_ping_9

    scene bg_kitchen with walk_fade

    "The kitchen is quiet. The plum is gone. There is nothing in its place."
    father "You are going to see the professor again."
    mc "Yes."
    father "What are you bringing him?"
    mc "A question."
    father "Which one?"
    mc "I have forty."
    father "Then you are not ready."
    mc "I am not sure I will ever be ready."
    father "Then you should go anyway. Ready is a place you arrive after you have started."
    mother "He is right. Go before you are ready. That is what the door is for."
    mc "(The door. She said it without thinking. I have been thinking about doors for three weeks.)"
    father "Take your sister with you. Not to the office. To the station. She can walk you to the gate."
    mc "She has class."
    hikari "I have a free period. I am coming."
    father "Good. Somebody should see you off who is not afraid of you."
    mc "(I am afraid of me. She is not afraid of me. That is the difference between us.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The walk to the station is the same walk. The crack in the pavement. The shrine at the edge of the street. The red torii that was always there and I only saw on Tuesday."
    hikari "You are quiet."
    mc "I am deciding which question to bring."
    hikari "Which one?"
    mc "The corridor."
    hikari "The corridor."
    mc "He asked if I would follow a door when it opens. I want to ask if he has ever seen one open."
    "She does not say anything for a while. The street is doing its morning sounds. A bicycle. A delivery scooter. A shopkeeper putting out a sign."
    hikari "That is a good question."
    mc "It is the only one I have."
    hikari "Then it is enough."

    scene bg_station with walk_fade
    scene bg_platform with walk_fade
    scene bg_train_interior with walk_fade

    "The train is not crowded. The sleeping man is not on the Wednesday train. Wednesdays belong to students."
    mc "(I am a student. I am also something else. The professor thinks I am the second kind.)"

    scene bg_school_gate with Fade(0.0, 0.0, 1.5)
    play music "audio/Music/school.mp3" fadein 1.5
    $ phone_map_visit("school")
    scene bg_campus_interior with walk_fade
    scene bg_department_hall with walk_fade

    "The professor's office. Same room. Same desk. Same wall of books nobody has taken down."
    "He is not behind the desk. He is standing by the window, looking at the courtyard."
    "When I knock, he turns around. He is holding a cup of tea. It smells like the tea at home. I have not asked why."
    professor "Sit."
    "I sit. He does not say anything for a while. He drinks his tea. The silence is different from Tuesday. Tuesday's silence had room in it. Today's silence has edges."

    professor "You brought your question."
    mc "I brought one."
    professor "That is all I asked for."

    "He sets the cup down. He does not sit. He stands by the window with his back to me, which means I cannot see his face when he speaks."
    professor "Ask it."

    menu:
        "Ask if he has ever seen a door open." :
            mc "Have you ever seen a door open?"
            "He does not turn around. His hand is on the window frame. The wood is worn where his fingers rest."
            professor "I have seen doors. I have not seen one open."
            mc "What is the difference?"
            professor "A door is a thing you open. An opening is a thing that opens you."
            mc "(He is not answering my question. He is answering a different one. I am not sure which one I asked.)"
            $ reward_attributes_once("day22_office_open", [("nerve", "micro")], show="auto")
        "[tag_insight] Rank 2: Ask what the corridor measures in you." if has_attribute("insight", 2):
            mc "You said the corridor measures whether someone will follow a door. What does it measure in me?"
            "He turns around. For the first time since I entered, he is looking at me. His eyes are not warm. They are not cold. They are exactly the temperature of the room."
            professor "On your exam, you wrote something I couldn't have put on the answer sheet."
            mc "The corridor."
            professor "No. You admitted you didn't know where it led. Most people make up an answer by then."
            $ reward_attributes_once("day22_office_measure", [("insight", "micro")], show="auto")
        "Ask about the student who drew doors." :
            mc "The student who left. Did she ask the real question?"
            "He does not answer right away. He looks at the courtyard. The courtyard is empty. It is always empty at this hour."
            professor "She asked the real question. That is why she left."
            mc "Where did she go?"
            professor "That is not a question I can answer. It is not a question you should ask."
            mc "(She asked the real question. She left. I am standing in front of a professor who is telling me the same thing in a different way. The city is teaching me to read between the lines.)"
            $ reward_attributes_once("day22_office_student", [("grace", "micro")], show="auto")

    professor "Take your tea. It is the same as hers. I do not know why I keep making it."
    mc "You make it because it is the only thing in this room that is not a question."
    "He looks at me for a long time. Then he sits down behind the desk and opens a drawer."
    "In the drawer is a small notebook. The cover is worn. The pages are filled with handwriting in two different inks."
    professor "This is hers. The student who left. She left it when she left."
    "He slides the notebook across the desk. I do not touch it."
    professor "You can look. You cannot keep it. It is not mine to give."
    "I open it. The first page is a map. Not a map of the city. A map of a corridor. The corridor has doors. The doors have numbers. The numbers are not in order."
    "The second page is the same corridor, but the doors are open. The numbers are still not in order."
    "The third page is blank."
    professor "She stopped at the third page. I do not know why. I do not know if she could not draw it or if she did not want to."
    mc "What is on the other side of the doors?"
    professor "That is the question. The one you are not allowed to ask. The one I think about. The one that made her leave."
    "He closes the notebook. He puts it back in the drawer. The drawer slides shut with a sound that is too loud for the room."
    professor "Go. You have an afternoon. Use it."
    mc "(He said afternoon. He said it on Tuesday. He is saying it every day now. It is becoming a thing he says to make the room feel ordinary when it is not.)"

    scene bg_campus_interior with walk_fade

    "Hikari is waiting by the stairs. She has the tomato timer in her pocket. She has not taken it out. She does not need to. She is counting something else now."
    hikari "Well?"
    mc "I saw the notebook."
    hikari "The notebook?"
    mc "The student's notebook. The corridor with the doors."
    hikari "Did you ask him what is on the other side?"
    mc "No. He said it is not a question I can ask."
    hikari "Then he answered it."
    mc "He said the question is the one that made her leave."
    hikari "Then you are asking the same question she asked."
    "She puts the tomato timer in my hand. This time she does not close my fingers around it. She just puts it there."
    hikari "You can keep it. You are going to need it."
    mc "For what?"
    hikari "For when you finally ask the real question. You will need to know how much time you have."
    mc "(She is not talking about the timer. She is talking about the question. The real one. The one I have been avoiding since I arrived.)"
    $ add_affection("sister", 1)

    $ flush_pending_messages()
    call free_afternoon from _call_free_afternoon_13

    call dinner_open from _call_dinner_open_15

    father "And the professor?"
    mc "He showed me a notebook. The student's notebook. The corridor."
    father "Did you ask the question?"
    mc "No. He said it is not a question I can ask."
    father "Then he answered it."
    mc "He said the question is the one that made her leave."
    father "Then you are asking the same question she asked."
    hikari "That is a father sentence. I am learning to hear them."
    father "I am allowed three a week. This is one."
    mother "He has not asked the question yet. He is still carrying it."
    mc "(I am still carrying it. The question. The notebook. The corridor. The door.)"

    call dinner_close from _call_dinner_close_15

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the window is open a crack. The city is doing its night sounds: a train, a voice, a gate."
    "The notebook is not on my desk. The professor kept it. But the map is in my head. The corridor. The doors. The numbers that are not in order."
    "The tomato timer is on the desk. Hikari gave it to me. It is not running. It is just there, a thing that measures time I have not decided to use yet."
    $ night_desk_line = "a timer that is not running"
    call night_open from _call_night_open_15

    menu:
        "Ask Hikari what the real question is." :
            mc "What is the real question?"
            hikari "I do not know. But I know it is not the corridor."
            mc "Then what is it?"
            hikari "It is the one you have been avoiding since you arrived. The one that makes you write the honest thing instead of the right thing."
            mc "(She is not talking about the exam. She is talking about me. About the way I have been living in this city. About the way I have been asking questions that are safe.)"
            $ log_memory("hikari", "said the real question is the one I have been avoiding since I arrived")
            $ reward_attributes_once("day22_night_real", [("insight", "micro")], show="auto")
        "Tell her about the notebook." :
            mc "The student's notebook. The corridor with the doors. She drew the doors open on the second page."
            hikari "What was on the third page?"
            mc "It was blank. She stopped."
            hikari "Maybe she could not draw it. Maybe she did not want to."
            mc "(She is giving me the same answer the professor gave me. The question I cannot answer. The question that made her leave.)"
            $ log_memory("hikari", "heard about the student's notebook and the blank third page")
            $ reward_attributes_once("day22_night_notebook", [("nerve", "micro")], show="auto")
        "Watch the timer. Say nothing." :
            "I do not say anything. The timer is not running. The city is doing its night sounds. A train. A scooter. A door."
            "Hikari watches me with me. She does not fill the silence."
            mc "(A room two people build and then leave. We are still building. But the room is changing. The walls are not where they were yesterday.)"
            $ log_memory("hikari", "watched the timer in silence on the night of the second meeting")
            $ reward_attributes_once("day22_night_quiet", [("grace", "micro")], show="auto")

    call night_close from _call_night_close_15

    "The lamp clicks off. The room goes dark. The room is not empty. The timer is on the desk. It is not running. But it is there."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
