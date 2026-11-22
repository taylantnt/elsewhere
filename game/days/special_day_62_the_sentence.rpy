################################################################################
## DAY 62: MONDAY, JUNE 8, 2026
## The sentence is everywhere. Father says it. Hikari says it. The professor
## says it. They do not notice each other. ChromaGlitch fires. The room tears
## for two tenths of a second. Then it is fine. Then it is not.
##
## Corruption level 3. The sentence has spread. The structure is cracking.
################################################################################

label special_day_62_the_sentence:
    $ set_story_day(62)
    $ corruption_level = 3
    call day_transition from _call_day_transition_62
    $ last_afternoon_place = None
    $ last_afternoon_hikari_tour = False

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Monday. Thirteen days of rain. I did not sleep. I lay in the dark and listened to the fridge try to remember the sequence and I thought about Mother standing at the wall."
    "I measured the room again this morning. Eleven spans. It has not grown overnight. That is either stability or the end of something. I do not know which."
    mc "(Day sixty-two. The voice did not come last night. The footsteps did not come. Mother came. Mother stood at the wall and said I was getting water and went to bed. Three people now. Hikari at the door. The footsteps in the hall. Mother at the wall. Three instances. Three repetitions. The sentence is spreading.)"

    "My phone buzzes."

    $ run_chat("hikari", [
        {"them": "I could not sleep. I kept thinking about the room.", "options": [
            {"label": "\"Did you measure it?\"",
             "send": "Did you measure it?",
             "them": ["I did.", "Eleven spans. You were right."]},
            {"label": "\"I am sorry.\"",
             "send": "I am sorry.",
             "them": ["For what?", "You are the one who noticed. I am the one who slept through it."]},
        ]},
    ])
    mc "(She measured it. Eleven spans. She believes me now. She counted and she got the same number and she believes me. That should be a relief. It is not a relief. It means the room is actually bigger. It means I was not imagining it. Imagining would have been better.)"

    call murakami_daily_ping from _call_murakami_daily_ping_62

    scene bg_kitchen with walk_fade

    call corruption_morning from _call_corruption_morning_62

    "The kitchen. Eight tiles from the door to the counter. The table. Father is at the table. He is eating rice. He is reading the paper. He is about to speak."
    father "The week is a machine. It runs the same program every seven days and the output is always Monday."
    "He says it. The fifth time. The same words. The same cadence. The same pause before Monday."
    "Then Hikari speaks."
    hikari "The week is a machine. It runs the same program every seven days and the output is always Monday."
    "She says it. The same words. The same cadence. The same pause before Monday. The same voice. Not her voice. His voice. Coming from her mouth."
    "She does not notice she said it. She is eating. She is looking at her bowl. Father does not notice she said it. He is reading the paper. Mother does not notice she said it. She is at the counter."
    "I am the only one who heard both of them say the same sentence at the same time."
    mc "(She said it. She said his sentence. Word for word. Voice for voice. She did not notice. He did not notice. Nobody noticed. I am the only witness and I am not sure I am a reliable one.)"
    mc "(The sentence has spread. It was his. Now it is hers. It moved from him to her the way the word consolidation moved from the dream to Hikari to Murakami. The sentence is a virus. The sentence is a program. The sentence is the machine.)"
    mother "Eat your rice."
    father "The rice is cold."
    mother "Then eat it faster."
    mc "(Normal. The exchange after the sentence is normal. The family is normal. The sentence was the abnormal thing and it passed and now they are normal again. Except the sentence did not pass. It is in Hikari now. It is in the house.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/school.mp3" fadein 2.0

    "The walk to the station. Hikari is with me. She is humming. The tune is the tune Mother hums in the morning. She does not usually hum Mother's tune."
    mc "(She is humming Mother's tune. She said Father's sentence. She is picking up their patterns. She is becoming a collection of their patterns. Or the patterns are spreading through her.)"
    hikari "What are you thinking about?"
    mc "The rain."
    hikari "You are always thinking about the rain."
    mc "It is always raining."
    hikari "That is fair."

    scene bg_train_interior with walk_fade

    "The Monday train. I count the stops. Seven. The same seven. I am grateful. I am so grateful for the seven that I almost miss the eighth."
    "The train stops at the eighth station. The doors open. People get on. People get off. The doors close. The train moves."
    "The eighth station has a name. I read it on the display. It is a name I do not recognise. It is a name I have never seen before. It is between the sixth and the seventh, in a gap that was not there on Friday."
    mc "(An eighth stop. Between the sixth and the seventh. A gap that was not there. A station that was not there. The train found a stop I had not noticed. Or the train found a stop that was not there until today.)"
    "I look around. Nobody else seems to notice. The other passengers are looking at their phones. The middle distance. The eighth station is just a station to them."
    mc "(I am the only one who counts. I am the only one who notices. That is either because I am the only one who is awake, or because I am the only one who is wrong.)"

    scene bg_lecture_hall with walk_fade

    "Murakami is at the board. She has written one word: rinkaku. Contour. The shape of a thing."
    murakami "Today is the word for the outline. Rinkaku. The edge of a thing. The line that separates it from everything else."
    murakami "In Japanese aesthetics, the rinkaku is the most important part of a drawing. Not the inside. The edge. The edge tells you what the thing is. The inside is just filling."
    "She pauses. She looks at the class."
    murakami "The week is a machine. It runs the same program every seven days and the output is always Monday."
    "She says it. Mid-lecture. In the middle of a sentence about contour. She says Father's sentence. She does not notice she said it. She continues."
    murakami "The contour of a week. Monday to Sunday. The shape that repeats. That is the rinkaku of time."
    mc "(Three times. Father. Hikari. Murakami. Three people said the same sentence today. None of them noticed the others. None of them noticed themselves. The sentence is in the air. The sentence is in the house and the train and the classroom and it is spreading.)"
    mc "(The week is a machine. It runs the same program. The sentence is the program. The sentence is the machine. The sentence is the thing that runs.)"

    menu:
        "Ask what stays the same when something repeats.":
            mc "Rinkaku. Can you say more about the contour of repetition?"
            murakami "The contour of repetition is the shape you see when you look at a thing that happens again and again. A week. A season. A sentence. The contour is the outline. The inside is the variation."
            mc "(The inside is the variation. The sentence is the contour. The variation is who says it. Father. Hikari. Murakami. The contour is the same. The inside is different. The machine is the contour. The people are the filling.)"
            $ reward_attributes_once("day62_lec_a", [("insight", "micro")], show="auto")
        "Ask about the shape of a language.":
            mc "Why does the contour matter in a language lesson?"
            murakami "Because you are learning the contour of a language. The shape. The edge. The words are the filling. The grammar is the contour. You learn the shape first. The filling comes later. Or never."
            mc "(The shape first. The filling later. I have learned the shape of this house. The shape of this family. The shape of this week. The filling is what is wrong. The filling is the sentence that spreads.)"
            $ reward_attributes_once("day62_lec_b", [("grace", "micro")], show="auto")
        "Write the sentence that is not yours.":
            "I write: rinkaku. Contour. The edge that tells you what the thing is."
            $ reward_attributes_once("day62_lec_c", [("nerve", "micro")], show="auto")

    "Before Murakami erases the board, I put my pen to the page."
    "I mean to write her example. When I lift the pen, I've written: the week is a machine."
    "The ink is still wet."

    scene bg_campus_interior with walk_fade

    "The corridor. The third tile. I step on it. The pitch is the pitch. It has settled. Or I have settled. Or the tile has given up changing because the sentence has taken over and the tile is no longer the point."
    mc "(The tile was the first thing. Now there are bigger things. The room. The hallway. The eighth station. The sentence. The tile is a footnote. The tile is a fragment of a fragment.)"

    call free_afternoon from _call_free_afternoon_62

    call corruption_post_visit from _call_corruption_post_visit_62

    scene bg_home_exterior_day with walk_fade
    stop music fadeout 2.0

    "The walk home. The combini. The card. I do not look at it. I look at the street. The street is the street. The distances are wrong. The combini is closer. The house is further. Or I am slower. Or the city is rearranging itself around me."
    mc "(The contour of the walk has changed. The shape is the same. The filling is different. The rinkaku of my route home.)"

    scene bg_kitchen with walk_fade

    call dinner_open from _call_dinner_open_62

    "Dinner. The table. Father. Mother. Hikari. Rice. Miso. The stopped clock."
    hikari "What was the house like before you came?"
    "She asks it. She is looking at me. She is asking me a question about before I arrived. She was here before I arrived. She has always been here. She should know what the house was like before I came."
    mc "You were here. You know."
    hikari "I know?"
    mc "You have always been here. You know what the house was like."
    hikari "I do not know why I asked that."
    "She catches herself. She looks at her rice. She is confused. She asked a question she should not ask and she does not know she should not ask it."
    mc "(She asked what the house was like before I came. She was here before I came. She should know. Unless she does not remember before I came. Unless before I came is not a thing she has access to. Unless she started when I started.)"
    father "The house was the same. The house is always the same."
    mother "Eat your rice."
    mc "(Father said the house is always the same. Mother said eat your rice. Two responses. One that answers the question. One that closes it. They are not coordinating. They are both doing their function.)"

    call dinner_close from _call_dinner_close_62

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "The room. Eleven spans. The desk. The notebook. The laundry rack. The window. The rain. The sentence in my handwriting on today's page."
    $ night_desk_line = "the notebook"
    call night_open from _call_night_open_62

    menu:
        "[tag_insight] Rank 3: Ask what she thinks the sentence wants." if has_attribute("insight", 3):
            mc "The sentence. Not who says it. What does it want?"
            hikari "It wants to be repeated. That is what a sentence wants."
            mc "Why?"
            hikari "Because a sentence that is repeated starts to sound like a fact."
            mc "(She is not looking at me. She is looking at the wall, counting it.)"
            mc "Then we should stop saying it."
            hikari "It does not need us to say it. That is the part I cannot explain."
            $ log_memory("hikari", "said the sentence wants to be repeated because a repeated sentence starts to sound like a fact")
            $ reward_attributes_once("day62_night_wants", [("insight", "micro")], show="auto")
        "Ask what the house was like before you arrived.":
            hikari "I asked you something at dinner. About before you came."
            mc "You did."
            hikari "I do not know why I asked it. I was here. I know what the house was like."
            mc "What was it like?"
            hikari "The same. It was the same. The kitchen. The hallway. The room. The rain."
            mc "The same."
            hikari "The same."
            mc "(She says the same. She says it like it is a fact. She says it like the house has always been the same. But the house is growing. The house is eleven spans and eight tiles and fourteen steps. If it was the same before I came, then it was always wrong. If it was not the same, then she does not remember.)"
            $ log_memory("hikari", "said the house was the same before MC came, the same kitchen, hallway, room, rain")
            $ reward_attributes_once("day62_night_a", [("grace", "micro")], show="auto")
        "Tell her Murakami said the same sentence.":
            mc "Murakami said the sentence today. In the lecture. The week is a machine. She said it mid-lecture. She did not notice."
            hikari "That is three."
            mc "What?"
            hikari "Father said it. I said it. She said it. That is three."
            mc "You know you said it?"
            hikari "I did not know at the time. I realised it after. In the library. I was reading about somnambulism and I remembered saying it and I did not remember deciding to say it."
            mc "(She remembers. She did not remember at the time. She remembers now. The sentence moved through her and she caught it after. Like a cold you do not feel until the next day.)"
            $ log_memory("hikari", "remembered saying Father's sentence at breakfast, did not remember deciding to say it, caught it after like a cold")
            $ reward_attributes_once("day62_night_b", [("nerve", "micro")], show="auto")
        "Say nothing. Let the sentence stand.":
            "The rain. The city. The Monday sounds. The train. The bell. The dog."
            "The dog barks three times. It is Monday. The dog barks on Monday."
            "Hikari is on the floor. She is not sleeping. She is mouthing something. I can almost read it. The week is a machine. She is mouthing the sentence. In the dark. To the ceiling."
            $ log_memory("hikari", "was mouthing the sentence to the ceiling in the dark, the week is a machine")
            $ reward_attributes_once("day62_night_c", [("insight", "micro")], show="auto")

    call night_close from _call_night_close_62

    call corruption_night from _call_corruption_night_62

    "I sit in the dark. The house is not doing its sounds. The fridge is the only one. Humming. Stopping. Humming."
    "Then the room tears."
    # ChromaGlitch: the whole screen splits for two tenths of a second.
    show layer master at glitch
    pause 0.20
    show layer master

    "The room is dark. The room is fine. The room is the room."
    "But for a fifth of a second, the room was not the room. The walls were somewhere else. The desk was somewhere else. The laundry rack was somewhere else. And I was somewhere else. In a white room. With wires. And a voice that said sixty-two."
    "Then it was the room again."
    mc "(A glitch. A tear. A fifth of a second where the room was not the room. I did not imagine it. The walls moved. The desk moved. I moved. And then it was fine. And then it was the room.)"
    "I look at my hands. My hands are my hands. I look at the desk. The desk is the desk. I look at the notebook. The notebook is open. Today's page. My handwriting. The week is a machine."
    "Below it, in handwriting that is not mine, a third line."
    "It says: \"He can see.\""
    mc "(Three lines now. She is leaking. She does not know. He can see. The handwriting is the same. The small tight letters. The pen that is not mine. Someone is writing in my notebook and they are writing about me and they are writing about Hikari and they know I can see.)"
    $ remember("mc", "a third line appeared in the notebook in handwriting that is not his: He can see", "notebook_third_line")
    "I close the notebook."
    "The laundry rack is in the corner. The rain is on the window. The fridge hums and stops and hums."
    "I do not sleep."
    $ collect_notebook_line(62)

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
