################################################################################
## DAY 55: MONDAY, JUNE 1, 2026
## June. Tsuyu. The rain is not weather anymore, it is the shape of the month.
## Murakami teaches the verb for waiting. She uses a word that does not belong
## to the lesson. She does not notice. The third tile squeaks.
##
## Corruption level 1. Two wrong details. Still deniable.
################################################################################

label special_day_55_the_word:
    $ set_story_day(55)
    $ corruption_level = 1
    call day_transition from _call_day_transition_55
    $ last_afternoon_place = None
    $ last_afternoon_hikari_tour = False

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Monday. June. The first of the month, and the rain has been here so long it has stopped being an event and become a condition."
    "I slept. I did not dream. The laundry rack is still in the corner. I decided yesterday that Mother put it back. I have decided it again this morning. The decision gets easier, which is not the same as it being true."
    mc "(June. The month the professor said the rainy season would break. The month Hikari has her seminar paper. The month I have been here for eight weeks.)"

    "My phone buzzes."

    $ run_chat("hikari", [
        {"them": "The seminar paper is due Wednesday. I will be in the library until late.", "options": [
            {"label": "\"Do you need help?\"",
             "send": "Do you need help?",
             "them": ["You cannot read Japanese academic prose.", "But you can bring coffee. That counts."]},
            {"label": "\"I will see you at home.\"",
             "send": "I will see you at home.",
             "them": ["Yes.", "Do not forget to eat. You forgot last Tuesday."]},
        ]},
    ])

    call murakami_daily_ping from _call_murakami_daily_ping_55

    scene bg_kitchen with walk_fade

    call corruption_morning from _call_corruption_morning_55

    mother "June. The month of patience."
    father "Patience is just waiting with a better reputation."
    hikari "I do not mind the rain. I mind the paper."
    mc "What is the paper about?"
    hikari "Consolidation. In narrative structure. How stories gather weight by repeating."
    mc "(Consolidation. The word lands in my ear like a coin in an empty room. I have heard it before. Not from her. From the dream. From the voice that said seventy-eight percent.)"
    mc "That sounds interesting."
    hikari "It is interesting the way a wall is interesting. You look at it long enough and it becomes a door."

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/school.mp3" fadein 2.0

    "Hikari walks with me to the station. She has her umbrella and I have mine. Two rooms walking the same street, the way we have walked it for eight weeks."
    hikari "The paper is not hard. It is just long. The hard part is the ending."
    mc "What is the ending?"
    hikari "I have not decided yet. The ending is the part where you find out what the repetition was for."
    mc "(She says it like it is a question about narrative structure. It lands like a question about everything else.)"

    scene bg_train_interior with walk_fade

    "The train is the Monday train. Full, quiet, everyone looking at their phones or at the middle distance. The middle distance is popular on Mondays."
    mc "(Eight weeks of this train. I know the stops by sound. The pitch of the announcement. The gap between the door chime and the movement. It is a song I did not learn, it just happened.)"

    "At the second stop, the doors open and a child in a yellow hat is on the platform. I blink. The platform is just adults with umbrellas."
    mc "(A child in a yellow hat. I have seen one before. On a platform. I do not remember when.)"

    scene bg_lecture_hall with walk_fade

    "Murakami is at the board. She has written one word: matsu. To wait."
    murakami "Today is the verb that is also a posture. Matsu. You wait for a train, you wait for a person, you wait for a season to end."
    murakami "The interesting thing about matsu is that it implies the thing you are waiting for is already coming. You are not hoping. You are standing in the path of something that is on its way."
    mc "(She pauses. She looks at the board. Then she says something that is not in the lesson.)"
    murakami "Consolidation. That is what waiting is. The consolidation of moments into a single expectation."
    mc "(Consolidation. Again. The same word Hikari used at breakfast. The same word the dream used. Three times in one morning, from three different directions, and none of them know about the others.)"
    murakami "Write it down. Matsu. Consolidation. The gathering of scattered things into one point."
    "She writes it on the board. Her handwriting is steady. She does not pause. She does not look confused. She moves on to the next verb."
    mc "(She does not know she said it. Or she knows and it is a word that everyone uses and I am the one who is hearing it wrong. Both are possible. One is more likely. I am not sure which.)"

    menu:
        "Ask for the Japanese word for consolidation.":
            mc "The word you used. Consolidation. What does it mean in Japanese?"
            murakami "Consolidation. You would say tougou. The gathering of separate things into one structure."
            mc "(She says it like it is a vocabulary word. She says it like there is nothing behind it. Maybe there is nothing behind it.)"
            $ reward_attributes_once("day55_lec_a", [("insight", "micro")], show="auto")
        "Ask what waiting has to do with it.":
            mc "Why does consolidation matter in a lesson about waiting?"
            murakami "Because waiting is not empty. Waiting is the mind consolidating what it expects into what it will accept. You are doing it now. You are consolidating this lecture into a sentence you will remember."
            mc "(She is right. I am consolidating. I am gathering the word into a point and the point is sharp and I do not know where it is pointing.)"
            $ reward_attributes_once("day55_lec_b", [("grace", "micro")], show="auto")
        "Copy the line into your notebook.":
            "I write: matsu. Consolidation. The gathering of scattered things into one point."
            "My handwriting is my handwriting. The pen moves the way it moves. The word sits on the page like it belongs there, like it has always been there, like I am just catching up to it."
            mc "(I stare at the word. It stares back. It is a word. It is just a word. I am the one who is making it into something.)"
            $ reward_attributes_once("day55_lec_c", [("nerve", "micro")], show="auto")

    scene bg_campus_interior with walk_fade

    "The campus corridor. The third tile. I step on it."
    "It squeaks."
    "It has always squeaked. Since the first week. The third tile in the corridor, the one that sounds different from the others. I have stepped on it every day for eight weeks."
    "But the pitch is wrong. It is higher. By a little. By enough."
    mc "(Tiles do not change pitch. Tiles are tiles. They are fired clay and they do not have a personality and they do not wake up one morning and decide to squeak differently.)"
    "I step on it again. It squeaks the new way. I step on the fourth tile. It is normal. I step back on the third. The new pitch."
    mc "(I am going to stop stepping on it. I am going to walk to class. I am going to have an afternoon.)"

    call free_afternoon from _call_free_afternoon_55

    call corruption_post_visit from _call_corruption_post_visit_55

    scene bg_home_exterior_day with walk_fade
    stop music fadeout 2.0

    "The walk home. The rain is lighter today, almost a suggestion. The streets are the streets. The combini is on the corner. The card is in the window."
    mc "(I do not look at the card. I do not need to check whether the handwriting is the same. I am not going to start checking things. That is how it starts, and I do not want it to start.)"

    scene bg_kitchen with walk_fade

    call dinner_open from _call_dinner_open_55

    father "June."
    mc "June."
    father "The month of waiting."
    mc "Mother said that this morning."
    father "She was right. She is usually right about the weather and wrong about the laundry."
    mother "I heard that."
    father "You were meant to."
    hikari "The paper is going well. I found the ending."
    mc "What is the ending?"
    hikari "The repetition stops. That is how you know it meant something. It stops, and the stopping is the meaning."
    mc "(She says it like it is about a narrative structure paper. It lands like it is about the house.)"

    call dinner_close from _call_dinner_close_55

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "The room. The desk. The notebook. The laundry rack in the corner, still there, still empty, still the shape of something that should not be there."
    $ night_desk_line = "the notebook"
    call night_open from _call_night_open_55

    menu:
        "Ask how her seminar paper is going.":
            hikari "The paper. The rain. The word consolidation, which I have now written so many times it does not look like a word anymore."
            mc "It does that. Words dissolve if you look at them long enough."
            hikari "That is what the paper is about. The dissolution. And then the consolidation. The gathering back."
            $ log_memory("hikari", "said words dissolve if you look at them long enough, and then gather back")
            $ reward_attributes_once("day55_night_a", [("grace", "micro")], show="auto")
        "Tell her Murakami used the same word.":
            mc "Murakami used that word today. Consolidation. In the lecture."
            hikari "That is a coincidence."
            mc "I know."
            hikari "You do not sound like you know."
            mc "I know it is a coincidence. I do not know why it does not feel like one."
            hikari "Because you are looking for patterns. The paper says that is what the mind does. It consolidates. It finds the shape even when there is no shape."
            mc "(She is explaining it to me as narrative theory. She is also explaining it to me as something else. I do not think she knows which one she is doing.)"
            $ log_memory("hikari", "explained consolidation as both narrative theory and something else, and did not know which")
            $ reward_attributes_once("day55_night_b", [("nerve", "micro")], show="auto")
        "Say nothing. Listen to the city.":
            "The rain is on the window. The city is doing its Monday sounds. A train. A bell. A dog that barks three times and stops, every Monday, like it has a schedule."
            "Hikari is on the floor with her paper. She is writing. The pen moves and stops and moves. Consolidation. The gathering of scattered things."
            $ log_memory("hikari", "was writing her paper about consolidation, pen moving and stopping")
            $ reward_attributes_once("day55_night_c", [("insight", "micro")], show="auto")

    call night_close from _call_night_close_55

    call corruption_night from _call_corruption_night_55

    "I close my eyes. The house is doing its sounds. All six. In the right order."
    "Then I hear it. Not from the house. From behind my eyes. A voice, flat, clinical, the kind of voice that reads numbers."
    "\"Day fifty-five.\""
    "I open my eyes. The room is dark. The laundry rack is in the corner. The rain is on the window."
    mc "(Day fifty-five. That is today. That is the day I am on. Someone is counting. Someone is counting the days I am here, and they are saying the number in my head, and I do not know if I dreamed it or heard it.)"
    "I close my eyes again. The voice does not come back. The rain does. I sleep."
    $ collect_notebook_line(55)

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
