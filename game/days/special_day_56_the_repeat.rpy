################################################################################
## DAY 56: TUESDAY, JUNE 2, 2026
## Father says the line again. The third time. Hikari does not react. The
## combini card has different handwriting. The notebook has a line that is not
## mine.
##
## Corruption level 1. Three wrong details. The pattern is building.
################################################################################

label special_day_56_the_repeat:
    $ set_story_day(56)
    $ corruption_level = 1
    call day_transition from _call_day_transition_56
    $ last_afternoon_place = None
    $ last_afternoon_hikari_tour = False

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Tuesday. The rain has been here for a week. It is not raining harder or softer. It is just raining, the way a faucet runs when you have forgotten to close it all the way."
    "I slept. I did not hear the voice. The laundry rack is still in the corner. I have stopped deciding why it is there. It is there. That is the whole sentence."
    mc "(Day fifty-five. Yesterday. The voice said the number and I heard it and I slept. I do not know what today's number is. I do not want to know.)"

    "My phone buzzes."

    $ run_chat("hikari", [
        {"them": "The paper is done. I submitted it at four in the morning.", "options": [
            {"label": "\"Four in the morning?\"",
             "send": "Four in the morning?",
             "them": ["I could not find the ending.", "Then I found it. Then I could not stop writing."]},
            {"label": "\"Congratulations.\"",
             "send": "Congratulations.",
             "them": ["Thank you.", "I am going to sleep until noon. Do not wake me."]},
        ]},
    ])
    mc "(She was up at four. Writing about consolidation. About how repetition gathers weight. I do not know if that is comforting or not.)"

    call murakami_daily_ping from _call_murakami_daily_ping_56

    scene bg_kitchen with walk_fade

    call corruption_morning from _call_corruption_morning_56

    "Father is at the table. He is eating rice and reading the paper and he is about to say something. I can feel it the way you feel weather."
    father "The week is a machine. It runs the same program every seven days and the output is always Monday."
    "He says it the way he says things. Flat, warm, like a sentence he found and is lending to the table."
    "I wait for Hikari to react. She does not. She is eating. She is looking at her bowl. She heard it. She did not hear it."
    mc "(The week is a machine. He said it on Day thirty-eight. He said it on Day thirty-four. Now he is saying it on Day fifty-six. Three times. The same words. The same cadence. The same pause before Monday.)"
    mother "Eat your rice before it gets cold."
    father "The rice is already cold. That is part of the program."
    mc "(He is joking. He is always joking. The sentence is a joke he likes and he is telling it again because he likes it. That is what people do with jokes. They repeat them.)"
    mc "(Then why does it sound different the third time. Not louder. Not quieter. Just more. Like the sentence is gaining weight every time he says it, and the weight is not his.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/school.mp3" fadein 2.0

    "The walk to the station. Hikari is half-asleep, her umbrella tilted forward like a shield against the morning. She did not react to Father's sentence. She did not hear it as a repetition. She heard it as a Tuesday."
    mc "(Maybe that is what it is. A Tuesday sentence. A thing he says on Tuesdays because Tuesdays need a sentence. I am the one who is counting, and counting is not the same as understanding.)"

    "At the crossing, the woman in the grey coat is there. Closer than last time. She is not reading her phone. She is looking at the crossing."
    mc "(I look at Hikari, then back. The crossing is empty. She did not see. She is half-asleep and would not have seen.)"

    scene bg_train_interior with walk_fade

    "The train. The Tuesday train. The same stops, the same pitch, the same gap between the chime and the movement."
    mc "(I am counting the stops. I have been counting them for eight weeks. I do not know when I started counting. The counting started itself, the way the rain started, and now it is a condition.)"

    scene bg_lecture_hall with walk_fade

    "Murakami is at the board. She has written one word: ma."
    murakami "Today is the word that is not a word. Ma. The gap. The pause. The space between two things that is not empty but is not full either."
    murakami "In Japanese aesthetics, ma is the silence between notes, the white space on a page, the breath between sentences. It is what is not there, and what is not there is what gives shape to what is there."
    mc "(She is teaching about gaps. About the space between things. About what is missing. I am sitting in a lecture about what is missing and I am missing something and I do not know what it is.)"
    murakami "The interesting thing about ma is that you cannot create it. You can only notice it. The gap was always there. You just were not looking at it."
    mc "(The gap was always there. The laundry rack. The tile. The word. The line. They were always there. I just was not looking at them.)"

    menu:
        "Ask how you notice a gap.":
            mc "Ma. Can you say more about how you notice it?"
            murakami "You notice it when something changes. The gap was invisible until the thing next to it moved. Then the gap appears. The gap is the shape of what was there."
            mc "(The gap is the shape of what was there. The laundry rack is the shape of the laundry rack. The tile's new pitch is the shape of the old pitch. I am noticing gaps because things are moving.)"
            $ reward_attributes_once("day56_lec_a", [("insight", "micro")], show="auto")
        "Ask what a pause can tell you.":
            mc "Why does ma matter in a language lesson?"
            murakami "Because language is mostly gaps. The words are the easy part. The pauses, the hesitations, the things you do not say. That is where the meaning lives."
            mc "(The things you do not say. Father does not say that he is repeating. Hikari does not say that she hears it. Mother does not say that the clock is stopped. The meaning lives in the gaps.)"
            $ reward_attributes_once("day56_lec_b", [("grace", "micro")], show="auto")
        "Write the gap into the notebook.":
            "I write: ma. The gap. What is not there is what gives shape to what is there."
            "The pen moves. The handwriting is mine. The letters sit on the page."
            "Then I look at the previous page. The entry from last week. Day forty-nine."
            "The handwriting changes. Halfway down the page. One line is not mine."
            $ reward_attributes_once("day56_lec_c", [("nerve", "micro")], show="auto")

    scene bg_campus_interior with walk_fade

    "The corridor. The third tile. I step on it. It squeaks the new pitch. I step on the fourth. Normal. I step on the fifth. Normal."
    "I walk to the end of the corridor and back. I step on every tile. Only the third is different."
    mc "(One tile. One pitch. One gap. That is ma. That is what Murakami was teaching. The gap that appears when something moves.)"

    call free_afternoon from _call_free_afternoon_56

    call corruption_post_visit from _call_corruption_post_visit_56

    scene bg_home_exterior_day with walk_fade
    stop music fadeout 2.0

    "The walk home. The combini is on the corner. The card is in the window."
    "I stop."
    "The card says the same thing. Afternoons. Two shifts. Ask for the manager. No Japanese needed beyond hello."
    "But the handwriting is different."
    "The first card was written in a hand that leaned forward, that pressed hard, that crossed the t with a slash. This card is written in a hand that stands straight, that presses light, that crosses the t with a curve."
    mc "(Someone rewrote the card. That is all. The old card fell in the rain and someone wrote a new one. That is what happens to cards in windows. They get wet. They get replaced.)"
    "I look at the card for a long time. The handwriting is not the handwriting I remember. But I am not sure I remember the first one correctly. Memory is not a photograph. Memory is a story you tell about a photograph."
    mc "(I am going home. I am going to eat dinner. I am going to sleep. The card is a card.)"

    scene bg_kitchen with walk_fade

    call dinner_open from _call_dinner_open_56

    mother "You are late."
    mc "I stopped at the combini."
    mother "The card?"
    mc "The card is still there."
    mother "Good. The card is doing its job."
    father "What card?"
    mother "The help wanted card. At the combini."
    father "Ah. The card. Yes."
    mc "(He says it like he knows the card. Like the card is a thing he has thought about. But he has never mentioned it before. I have been the one who looks at it every day.)"
    hikari "I slept all afternoon. The paper is submitted. I am a person again."
    mc "Congratulations."
    hikari "Thank you. I am going to eat everything in this kitchen."

    call dinner_close from _call_dinner_close_56

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "The room. The desk. The notebook is open. I left it open this morning. I do not remember leaving it open."
    $ night_desk_line = "the notebook, open"
    call night_open from _call_night_open_56

    menu:
        "[tag_grace] Rank 3: Ask her what she would want to forget." if has_attribute("grace", 3):
            mc "If you could forget one thing. Not the paper. Not the rain. One thing."
            hikari "I would forget the week I stopped noticing you."
            mc "I did not know there was one."
            hikari "There was not. That is why I would forget it."
            mc "(She turns her cup so the handle faces me. I do not know when she started doing that.)"
            $ log_memory("hikari", "said she would forget the week she stopped noticing him, which never happened")
            $ reward_attributes_once("day56_night_forget", [("grace", "micro")], show="auto")
        "Ask what she did once the paper was done.":
            hikari "I slept. I ate. I am going to sleep again. That is the whole day."
            mc "That sounds good."
            hikari "It is good. The paper is done. The repetition is over. I found the ending."
            mc "What was the ending?"
            hikari "The ending was that the repetition was never the point. The point was the gap between the repetitions. The ma. The silence between the notes."
            mc "(She is talking about her paper. She is also describing the last three days. She does not know she is describing the last three days.)"
            $ log_memory("hikari", "said the point of repetition was the gap between repetitions, the ma, the silence between notes")
            $ reward_attributes_once("day56_night_a", [("grace", "micro")], show="auto")
        "Tell her Father keeps saying the same line.":
            mc "Father said the line again. The week is a machine."
            hikari "He says that."
            mc "He has said it three times now. The same words."
            hikari "He likes it. It is his sentence. People have sentences."
            mc "You did not react."
            hikari "Why would I react? He says it. I hear it. That is what happens with sentences people like."
            mc "(She does not hear it as a repetition. She hears it as a habit. I hear it as a pattern. One of us is right. I do not know which one.)"
            $ log_memory("hikari", "did not react to Father repeating the line, said people have sentences")
            $ reward_attributes_once("day56_night_b", [("nerve", "micro")], show="auto")
        "Say nothing. Let the rain keep count.":
            "The rain. The city. The Tuesday sounds. A train, a bell, the dog that barks three times."
            "Hikari is already asleep on the floor. The paper took everything she had. She is breathing the way people breathe when they have stopped counting the hours."
            $ log_memory("hikari", "fell asleep on the floor, exhausted from the paper, breathing like someone who stopped counting hours")
            $ reward_attributes_once("day56_night_c", [("insight", "micro")], show="auto")

    call night_close from _call_night_close_56

    call corruption_night from _call_corruption_night_56

    "I pick up the notebook. I turn to the page from Day forty-nine. The hydrangea day."
    "The entry is mine. The handwriting is mine. The words are mine. Then, halfway down the page, one line changes."
    "The letters are smaller. Tighter. Written by a hand that holds the pen differently. The line says:"
    "\"She is leaking.\""
    "Three words. In my notebook. On my page. In handwriting that is not mine."
    mc "(I did not write this. I did not write this. Someone wrote this in my notebook while I was sleeping, or while I was at school, or while I was not looking. Someone opened my notebook and wrote three words and closed it and left.)"
    "I stare at the line. The line stares back."
    "I close the notebook. I put it on the desk. I turn off the lamp."
    "The laundry rack is in the corner. The notebook is on the desk. The rain is on the window."
    "I do not sleep for a long time."
    $ collect_notebook_line(56)

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
