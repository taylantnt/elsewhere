################################################################################
## DAY 17: FRIDAY, APRIL 24, 2026
## Sound words. The house has been speaking Japanese since the first morning.
################################################################################

label friday_sounds:
    $ set_story_day(17)
    call day_transition from _call_day_transition_10

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Four days. The window is dry and the sky is pale and clear."
    "I wake before the alarm again. The ceiling is the ceiling. But I hear it differently this morning."
    "The pipe at six. The fridge at six-fifteen. Hikari's door at six-twenty."
    mc "(I wrote that on Day 8. I thought I was learning the house. I was learning a language and did not know it had a name.)"

    "My phone buzzes."

    if "murakami" in wire_unlocked:
        $ run_chat("murakami", [
            {"them": "Close your eyes where you are. Name three sounds.", "options": [
                {"label": "\"I can't do this before tea.\"",
                 "send": "I can't do this before tea.",
                 "them": ["Then do it after tea.", "The sounds will wait. They have been waiting for weeks."]},
                {"label": "\"Pipe. Fridge. My sister's door.\"",
                 "send": "Pipe. Fridge. My sister's door.",
                 "them": ["You have been doing the exercise without me.", "Good. Today you get the words for it."]},
            ]},
            {"them": "Class at ten. Bring the ear, not the book."},
        ])
        mc "(She texted 'the ear, not the book.' I am going to bring both, because I am not an animal.)"
    else:
        $ run_chat("hikari", [
            {"them": "I can hear you listening.", "options": [
                {"label": "\"Listening to what?\"",
                 "send": "Listening to what?",
                 "them": ["The house. You do it every morning.", "I am going to make you say it out loud."]},
                {"label": "\"That's a strange thing to text.\"",
                 "send": "That's a strange thing to text.",
                 "them": ["It is a true thing to text. Those are the only kind I send."]},
            ]},
        ])

    "Three knocks. Hikari opens the door holding two cups of tea and an expression of pure suspicion."
    hikari "Name the sounds."
    mc "What?"
    hikari "You know the ones. The pipe, the fridge, my door. You told me about them on Wednesday last week."
    mc "You remembered that?"
    hikari "I remember everything you say when you think I am not listening. It is a 凶器. A weapon."
    mc "You can't just declare a thing a weapon."
    hikari "I just did."
    "She hands me a cup and sits on the edge of the desk."
    hikari "Say them. Out loud."
    mc "Pipe. Fridge. Your door."
    hikari "Again, but with the words you would use if you were worried about them."
    mc "(There is no normal version of this conversation.)"

    call murakami_daily_ping from _call_murakami_daily_ping_4

    scene bg_kitchen with walk_fade

    "The kitchen is doing its morning work. The rice cooker clicks off at exactly the moment I sit down, which is either a coincidence or the most reliable thing in my life."
    mother "You are early again."
    mc "I am learning the sounds."
    mother "Then you are up early for a good reason. That is different from awake early."
    "Hikari taps her chopsticks against the table twice. Kotsu, kotsu."
    hikari "There. Write that one down."

    menu:
        "Ask what the tap means.":
            mc "What does that mean? The tap."
            hikari "It means hurry up. It is also just a tap. Those are the two things it means at once."
            mother "She is very good at the two-things-at-once."
            hikari "I learned it from you."
            $ reward_attributes_once("day17_kitchen_tap", [("insight", "micro")], show="auto")
        "Tap back.":
            "I tap my chopsticks against the table. Twice. Kotsu, kotsu."
            "Hikari looks at my hand for a long second, then looks away."
            hikari "That was not a correction. That was an answer."
            mc "Is that allowed?"
            hikari "At this table? Everything is allowed if you do it twice."
            $ reward_attributes_once("day17_kitchen_tapback", [("grace", "micro")], show="auto")
        "Listen to the rice cooker instead.":
            "The rice cooker clicks. The fridge answers from the corner. The pipe answers from the wall."
            mc "(It is a conversation. I have been sitting in the middle of it for seventeen mornings.)"
            $ reward_attributes_once("day17_kitchen_listen", [("nerve", "micro")], show="auto")

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "Friday. The street has the particular Friday feeling of a week that is almost finished and has not noticed yet."
    "I know the platform. I know the car. I know the one-minute sign."
    mc "(The map is nearly drawn. I just need somebody to tell me what the words on it are.)"
    "Hikari points at the sign above the track."
    hikari "The Yamanote loop closed in 1925. Before that it was two lines with a gap."
    mc "(I know the shape of every sign here. I still cannot hear the announcement.)"

    scene bg_school_gate with Fade(0.0, 0.0, 1.5)
    play music "audio/Music/school.mp3" fadein 1.5
    $ phone_map_visit("school")
    scene bg_campus_interior with walk_fade
    scene bg_lecture_hall with walk_fade
    play music "audio/Music/classroom.mp3" fadein 1.0

    "Murakami has written two words on the board and underlined them both once."
    "擬音語. 擬態語."
    murakami "Giongo. Sound words. The sound a thing makes, written down."
    murakami "Gitaigo. State words. The way a thing is, written down as if it were a sound."
    murakami "Zaazaa. Rain. Kotsukotsu. A small knock. Gosogoso. Moving quietly in a bag."
    murakami "And then: doki doki. A heart. Pika pika. Something clean. Shiin. Silence."
    mc "(Shiin. A word for silence that is not the absence of sound.)"
    murakami "English can say 'the rain fell.' Japanese can say 'zaazaa.' The second one is not a decoration. It is the rain, arriving in your mouth before it arrives in your ears."

    "She puts down the chalk and looks at the class."
    murakami "Close your eyes."
    "Everybody closes their eyes. Murakami does not."
    murakami "Name what you hear. Not what it is. What it sounds like."
    "A student says something. Murakami nods without opening her eyes wider."
    murakami "Again."

    menu:
        "Say 'kotsukotsu' for the pipe.":
            mc "Kotsukotsu. The pipe."
            murakami "The pipe is goo goo. Kotsukotsu is a small knock. You are hearing your sister's chopsticks in the wall."
            mc "Maybe I am."
            murakami "Good. A sound word is allowed to be about two things. That is what makes it a word and not a recording."
            $ reward_attributes_once("day17_class_pipe", [("insight", "micro")], show="auto")
        "Say 'shiin' for the pause after the bell.":
            mc "Shiin. The part after the bell before anyone moves."
            murakami "Yes. Nothing is happening and the room is full of it."
            murakami "You have been doing this all week. You call it watching. It is listening with your eyes open."
            $ reward_attributes_once("day17_class_shiin", [("grace", "micro")], show="auto")
        "Say nothing. Keep the silence.":
            "I keep my eyes closed. The room is a bowl of small sounds. I do not put a word on any of them."
            murakami "You did not say anything."
            mc "I was not finished hearing it."
            murakami "That is an answer. Keep it."
            $ reward_attributes_once("day17_class_silence", [("nerve", "micro")], show="auto")

    murakami "On Monday you will be tested on this. Somebody will say a word and you will answer before you understand it."
    murakami "That is the practical. The hand first. The head last. You have heard me say it."

    "She walks between the rows and stops at my desk."
    murakami "Write the sound of a door that is not there."
    mc "A door that is not there?"
    murakami "You heard one. On Thursday. In a house, between one room and another."
    "My mouth is dry. I do not know how she knows that. I do not ask. She has a way of knowing things that makes asking feel slow."

    "I take my pen. My hand writes before I decide what to write."
    "カチ。"
    "Kachi. A click. A latch. The sound a door makes when it decides to be a door."
    mc "I don't know that word."
    murakami "You wrote it. That is a kind of knowing."
    mc "What does it mean?"
    murakami "It means a small hard sound. Sometimes a sound like that is also a decision."
    "She looks at the word on my page for a moment longer than she needs to."
    murakami "Do not show that to anyone on Monday."

    call leak_audio from _call_leak_audio_2

    "For half a second the classroom is not the classroom. It is a white corridor with a door at the end, and the door is closing."
    "Kachi."
    "Then Murakami is setting the chalk down and the bell is about to go and the room is a room."

    $ sound_word_written = "kachi"
    $ murakami_lessons = max(murakami_lessons, 4)
    $ japanese_fluency = min(5, japanese_fluency + 1)

    call quiz_sound_words from _call_quiz_sound_words_1

    scene bg_campus_interior with walk_fade

    "Hikari is waiting by the stairs. She takes one look at my face and does not ask what happened."
    hikari "You have a word face."
    mc "A what?"
    hikari "The face you get when a word has been in your head for an hour and you are deciding whether it is allowed to stay."
    mc "It's allowed."
    hikari "Then it can come home with us."

    $ flush_pending_messages()
    call free_afternoon from _call_free_afternoon_8

    call dinner_open from _call_dinner_open_10

    father "And the Japanese class?"
    mc "Sound words. Zaazaa for rain. Kotsukotsu for a knock."
    father "What is the word for a door?"
    "I do not look at Hikari. She does not look at me."
    mc "Kachi."
    father "A small sound."
    mc "A small hard sound."
    mother "Then it is a good word to know. Eat."

    call dinner_close from _call_dinner_close_10

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the page is on the desk. カチ. The word is the only thing on it. Everything else I wrote today has been rubbed out by my own hand."
    $ night_desk_line = "one word"
    call night_open from _call_night_open_10

    menu:
        "[tag_insight] Rank 2: Ask whether the word came before the sound." if has_attribute("insight", 2):
            mc "Which came first? The sound or the word for it?"
            hikari "The sound. Always. The word is what you do afterward so you can stand it."
            mc "So naming is not hearing."
            hikari "Naming is agreeing to have heard. That is a different job."
            mc "(Kachi. A latch. A decision. A word I agreed to.)"
            $ log_memory("hikari", "asked whether the word came before the sound, and she said naming is agreeing to have heard")
            $ reward_attributes_once("day17_night_first", [("insight", "micro")], show="auto")
        "Tell her the word.":
            mc "Kachi. It is the sound of a latch. Murakami says it is also a decision made too fast to see."
            hikari "What decision?"
            mc "I don't know. My hand wrote it before I did."
            hikari "Then maybe your hand was the one that made it."
            mc "(She says it in the dark, facing the window. I do not know if it is a joke.)"
            $ log_memory("hikari", "told her the word kachi and she said maybe his hand made the decision")
            $ reward_attributes_once("day17_night_word", [("insight", "micro")], show="auto")
        "Ask her what the corridor sounds like.":
            mc "The corridor. Does it have a sound?"
            hikari "Not a click. A hum. Like a fridge in a house that is not yours."
            mc "You have heard it?"
            hikari "I hear it when you are not in the room."
            "She says it plainly, like something she has lived with for a while."
            $ log_memory("hikari", "said the corridor sounds like a hum, like a fridge in a house that is not hers")
            $ reward_attributes_once("day17_night_corridor", [("grace", "micro")], show="auto")
        "Say nothing. Let the word sit on the desk.":
            "I do not say anything. The tea is hot. The word sits on the page, small and hard."
            "Hikari turns her cup a slow quarter turn and leaves it there."
            $ log_memory("hikari", "left the word kachi on the desk and said nothing")
            $ reward_attributes_once("day17_night_quiet", [("nerve", "micro")], show="auto")

    call night_close from _call_night_close_10

    "Zaazaa. Kotsukotsu. Kachi."
    "Tomorrow is Saturday. There is a festival in the neighbourhood. Hikari has been looking forward to it all week."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump saturday_matsuri
