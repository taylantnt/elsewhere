################################################################################
## DAY 57: WEDNESDAY, JUNE 3, 2026
## The last subtle day. The hub is open. The confidant visit is normal. But
## the clock on the wall is wrong, and at night, through the wall, a voice
## that is not Hikari's.
##
## Corruption level 1. The ambient detail plus the voice. Level 1 ends.
################################################################################

label special_day_57_the_clock:
    $ set_story_day(57)
    $ corruption_level = 1
    call day_transition from _call_day_transition_57
    $ last_afternoon_place = None
    $ last_afternoon_hikari_tour = False

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Wednesday. The rain has been here for eight days. It is not a weather event. It is a tenant."
    "I did not sleep well. The notebook is on the desk. I did not open it this morning. I will not open it this morning. The three words are in there and I am not ready to look at them in daylight."
    mc "(She is leaking. That is what the line says. That is what someone wrote in my notebook. I do not know who. I do not know what it means. I am going to have a Wednesday.)"

    "My phone buzzes."

    $ run_chat("hikari", [
        {"them": "I slept fourteen hours. I am a new person. The old one is in the bin.", "options": [
            {"label": "\"Welcome back.\"",
             "send": "Welcome back.",
             "them": ["Thank you.", "I have a seminar at two but the morning is free."]},
            {"label": "\"Fourteen hours?\"",
             "send": "Fourteen hours?",
             "them": ["The paper took three days of sleep.", "I have invested it back. Like a bank."]},
        ]},
    ])

    call murakami_daily_ping from _call_murakami_daily_ping_57

    scene bg_kitchen with walk_fade

    call corruption_morning from _call_corruption_morning_57

    "The kitchen. The table. Father is gone already. Mother is washing rice. Hikari is at the table looking like a person who has been reassembled from parts that almost fit."
    mother "You did not eat breakfast yesterday."
    mc "I ate."
    mother "You ate rice. Rice is not breakfast. Breakfast is rice and egg and miso and the conversation about whether the rain will stop."
    mc "Will the rain stop?"
    mother "No. But we will have the conversation anyway. That is what breakfast is for."
    hikari "She is right. Breakfast is a format. The content does not matter."
    mc "(This is the house. This is the kitchen. This is the family. The notebook is upstairs and the three words are in it and down here, none of that exists.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/school.mp3" fadein 2.0

    "The walk to the station. Hikari is rested and walking like it. Her umbrella is up and her stride is longer than it has been all week."
    hikari "The paper got me thinking. About repetition. About the gap between things."
    mc "Murakami taught about that yesterday. Ma. The gap."
    hikari "She did? That is strange. I was writing about the same thing at four in the morning."
    mc "(She says strange. She does not say impossible. She does not say worrying. She says strange, the way you say strange about a coincidence that is interesting but not dangerous.)"

    scene bg_train_interior with walk_fade

    "The Wednesday train. Less full than Monday. The middle distance is less popular on Wednesdays. People look at their phones instead."
    mc "(I am counting the stops. I cannot stop counting the stops. There are seven between the house and the campus. I have known this for eight weeks. Today they feel like more. Not slower. More. Like the train is finding extra stops I had not noticed.)"

    "At the second stop, the child in the yellow hat is on the platform again. She is facing the train. She is looking at me."
    mc "(I blink. The platform is empty. The doors close. The train moves. I did not imagine that.)"

    scene bg_lecture_hall with walk_fade

    "Murakami is at the board. She has written one word: kurikaeshi. Repetition."
    murakami "Today is the word that describes what this language does best. Kurikaeshi. The act of returning to something. Not because you forgot it. Because it gains weight every time you return."
    murakami "In Japanese aesthetics, repetition is not failure. It is depth. The tea ceremony is the same gestures every time. The value is not in the novelty. The value is in how the same gesture changes because you have changed."
    mc "(She is teaching about repetition. About how the same sentence gains weight every time it is said. Father's sentence. The week is a machine. It gains weight every time. Not because the sentence changes. Because I change.)"
    murakami "The danger of repetition is that you stop hearing it. The third time you hear a sentence, you do not process it. You recognise it. Recognition is cheaper than processing. That is why repetition works in advertising and fails in conversation."
    mc "(The third time. Father said the sentence three times. I recognised it the third time. I did not process it. I just flagged it as a repeat. Murakami is telling me I missed something.)"

    menu:
        "Ask how hearing differs from recognizing.":
            mc "Kurikaeshi. Can you explain the difference between hearing and recognising?"
            murakami "Hearing is the first time. Recognising is every time after. The brain is lazy. It substitutes the label for the thing. You do not hear the sentence. You hear the label that says: I have heard this before."
            mc "(I labelled Father's sentence. I did not hear it the third time. I recognised it. What did I miss?)"
            $ reward_attributes_once("day57_lec_a", [("insight", "micro")], show="auto")
        "Ask what changes when the words stay the same.":
            mc "Why does repetition matter in a language lesson?"
            murakami "Because you are learning by repetition. Every day you say the same things. Good morning. Thank you. I am sorry. The words do not change. You change. That is the lesson."
            mc "(I am changing. The words are not. Father's words are not. Hikari's words are not. The house's words are not. I am the one who is changing, and the repetition is how I measure the change.)"
            $ reward_attributes_once("day57_lec_b", [("grace", "micro")], show="auto")
        "Write the word the lecture keeps repeating.":
            "I write: kurikaeshi. Repetition is not failure. It is depth. The same gesture changes because you have changed."
            "I do not open the previous page. I do not look at the line that is not mine. I write on today's page and I close the notebook."
            mc "(I am not going to look. Not today. Today I am going to write my own words in my own handwriting and pretend the other page does not exist.)"
            $ reward_attributes_once("day57_lec_c", [("nerve", "micro")], show="auto")

    scene bg_campus_interior with walk_fade

    "The corridor. The third tile. I step on it. The new pitch. I step on it again. The new pitch."
    "I step on it a third time."
    "The pitch has changed again. Higher. Not by much. By enough."
    mc "(The tile is not changing. I am changing. That is what Murikaeshi means. The same gesture changes because the person has changed. The tile is the same tile. I am not the same person.)"

    call free_afternoon from _call_free_afternoon_57

    call corruption_post_visit from _call_corruption_post_visit_57

    scene bg_home_exterior_day with walk_fade
    stop music fadeout 2.0

    "The walk home. The rain is lighter. The combini is on the corner. I do not look at the card."
    "I look at the card."
    "The handwriting is different again. A third hand. Or the same hand, changed. I cannot tell. The card says the same thing. Afternoons. Two shifts. Ask for the manager."
    mc "(Three versions of the card. Three handwritings. Or one handwriting that I am misremembering three different ways. I do not know which is more likely.)"

    scene bg_kitchen with walk_fade

    call dinner_open from _call_dinner_open_57

    hikari "Have you been sleeping?"
    mc "Yes."
    hikari "You have not."
    mc "I have. Some."
    hikari "Some is not yes. Some is the word you use when yes is not available."
    mc "(She is looking at me the way she looks at the sky. Checking for weather she has not prepared for.)"
    mother "Let him eat. Sleep is after dinner. That is the schedule."
    father "The schedule is a machine."
    "He says it. Not the whole sentence. Just the first half. The week is a machine. He stops before Monday."
    "He does not finish it. He goes back to his rice."
    mc "(He stopped. He has never stopped before. The sentence has always been whole. Now it is half. Like he forgot the rest. Like the program skipped a line.)"

    call dinner_close from _call_dinner_close_57

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "The room. The desk. The notebook, closed. The laundry rack, still there. The window, still raining."
    $ night_desk_line = "the closed notebook"
    call night_open from _call_night_open_57

    menu:
        "[tag_grace] Rank 3: Tell her you are not asking her to fix it." if has_attribute("grace", 3):
            mc "I am not telling you so you can fix it."
            hikari "I know."
            mc "I wanted one person to know the shape of it."
            hikari "Then it has a shape. That is what I said."
            $ reward_attributes_once("day57_night_shape", [("grace", "micro")], show="auto")
        "Tell her you have not been sleeping well.":
            hikari "The paper is done. The seminar was good. The rain is still here. That is the day."
            mc "You asked if I was sleeping."
            hikari "You look like you are not."
            mc "I am sleeping. I am just not sleeping well."
            hikari "That is a different thing. That is a thing that has a shape. You can hold a thing that has a shape."
            $ log_memory("hikari", "said not sleeping well is a thing with a shape, and you can hold a thing with a shape")
            $ reward_attributes_once("day57_night_a", [("grace", "micro")], show="auto")
        "Ask why Father stopped mid-sentence.":
            mc "Father stopped. At dinner. He started the sentence and he stopped."
            hikari "The week is a machine?"
            mc "Yes. He said the schedule is a machine and then he stopped. He did not finish it."
            hikari "He does that sometimes. He starts a sentence and decides it is not worth finishing."
            mc "He has never done it with that sentence."
            hikari "Then maybe he is tired of it. People get tired of their own sentences. That is what repetition does. Even to the person who likes the sentence."
            mc "(She is explaining it as fatigue. I am hearing it as a program skipping a line. Both are possible. One is more likely. I am not sure which.)"
            $ log_memory("hikari", "explained Father stopping mid-sentence as fatigue, said people get tired of their own sentences")
            $ reward_attributes_once("day57_night_b", [("nerve", "micro")], show="auto")
        "Say nothing. Listen to the stopped clock.":
            "The rain. The city. The Wednesday sounds."
            "Hikari is on the floor. She is not sleeping. She is looking at the ceiling."
            "I am looking at the ceiling."
            "Two people looking at the same ceiling, not talking, in a house that is doing its sounds."
            $ log_memory("hikari", "was looking at the ceiling with me, not talking, in the house doing its sounds")
            $ reward_attributes_once("day57_night_c", [("insight", "micro")], show="auto")

    call night_close from _call_night_close_57

    call corruption_night from _call_corruption_night_57

    "I lie in the dark. The house is doing its sounds. All six. In the right order."
    "Then, through the wall, Hikari's room."
    "A voice."
    "It is not Hikari's voice. It is lower. Flatter. It says something I cannot make out. A sentence, or a number, or a word that does not have edges."
    "Then silence."
    "Then the voice again. The same thing. The same shape of sound."
    "Then Hikari's voice. Quiet. Asleep. She murmurs something and turns over and the bed creaks and the voice is gone."
    mc "(She talks in her sleep. That is all. People talk in their sleep. The other voice was the house. The pipes. The fridge. The seventh sound I have never named.)"
    "I lie in the dark and listen for the voice. It does not come back."
    "The laundry rack is in the corner. The notebook is on the desk. The rain is on the window."
    "I sleep. Badly."
    $ collect_notebook_line(57)

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
