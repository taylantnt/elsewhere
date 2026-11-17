################################################################################
## DAY 19: SUNDAY, APRIL 26, 2026
## The mock exam. できる and わかる. A fourth question he did not write.
################################################################################

label sunday_mock:
    $ set_story_day(19)
    call day_transition

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Sunday. Late, and without apology. The light on the ceiling is the color of the inside of a shell."
    "Three days. The number is small enough that I can hold it in my hand."
    "Mister Plum is in his chipped bowl on the desk. He is the only thing in this room that is not thinking about Monday."
    mc "(Or maybe he is. I do not know how a fish thinks about time.)"

    "My phone buzzes."

    if "chef" in wire_unlocked:
        $ run_chat("chef", [
            {"them": "Test soon. Eat before. An empty stomach answers slowly.", "options": [
                {"label": "\"I'll eat.\"",
                 "send": "I'll eat.",
                 "them": ["Good.", "Rice. Not bread. Bread is a snack wearing a hat."]},
                {"label": "\"What if I can't eat?\"",
                 "send": "What if I can't eat?",
                 "them": ["Then eat half.", "Half is still an answer."]},
            ]},
        ])
        mc "(He cannot read my messages either, probably. He does not need to. He knows a student when he sees one.)"
    else:
        $ run_chat("hikari", [
            {"them": "Get up. The exam is in three days and you are still horizontal.", "options": [
                {"label": "\"It's Sunday.\"",
                 "send": "It's Sunday.",
                 "them": ["I know. That is why we have time to do this properly."]},
                {"label": "\"I'm resting my eyes.\"",
                 "send": "I'm resting my eyes.",
                 "them": ["You are resting your whole body. I can see it from here."]},
            ]},
        ])

    "Three knocks, then the door. Hikari is holding the tomato timer and a stack of index cards held together with a paper clip."
    hikari "Today you write the exam."
    mc "I write it?"
    hikari "You write it. I answer it. That is the only way to know whether you understand a thing."
    mc "Isn't it the other way around?"
    hikari "That is the way schools do it. Schools are wrong about a lot of things."
    "She sets the cards on the desk and sits on the floor with her back against the bed, exactly where she sits at night."
    hikari "Three questions. No trick questions. If you write a trick question, I will know and I will be disappointed in both of us."
    mc "(The pressure of writing an exam for a person who has known me for twenty-six days. This is worse than taking one.)"

    scene bg_kitchen with walk_fade

    "The kitchen is slow and warm. Mother has made a late breakfast: rice, miso, grilled fish, pickles. Father is tapping the table with one finger."
    "Tap. Tap. Kotsukotsu."
    mc "Are you doing the sound word?"
    father "I am doing the sound word."
    mc "Why?"
    father "Because you taught it to me. That is what a lesson is. You give it to somebody and they cannot stop using it."
    mother "He did the same thing with mottainai for three weeks."
    father "It was a good word."
    hikari "It is a good word. That is not the point."
    mc "(Father has been practising my homework at breakfast. I do not know what to do with this.)"

    menu:
        "Ask him what else he learned.":
            mc "What else did I teach you?"
            father "Shiin. The room after the bell."
            mc "When do you use that?"
            father "When your mother is about to say something and has not said it yet."
            mother "I heard that."
            father "I know. That is why I said it."
            $ reward_attributes_once("day19_kitchen_words", [("insight", "micro")], show="auto")
        "Tap back. Twice.":
            "I tap the table twice with one finger. Kotsukotsu."
            "Father stops. He looks at my hand, then goes back to his rice."
            father "Good."
            mc "That's it?"
            father "That is the whole lesson. You do not need me to clap."
            $ reward_attributes_once("day19_kitchen_tap", [("grace", "micro")], show="auto")
        "Ask about Mister Plum.":
            mc "Where did the bowl come from?"
            mother "The cupboard. The chipped one. It has held rice for twenty years. It can hold a fish."
            mc "Is that mottainai?"
            mother "Everything is mottainai. That is the trouble with it."
            $ reward_attributes_once("day19_kitchen_fish", [("nerve", "micro")], show="auto")

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "We take the train to campus because Hikari says the library has the reserve copy and the reserve copy has her name in it."
    hikari "I put my name on the top copy."
    mc "You told me that on Wednesday."
    hikari "I am repeating it because you did not believe me."
    mc "I believed you."
    hikari "You made the face."
    mc "What face?"
    hikari "The face that says 'she would do that, but why would she tell me.'"
    mc "(I cannot have a private facial expression in this city.)"

    scene bg_station with walk_fade
    scene bg_platform with walk_fade
    scene bg_train_interior with walk_fade
    "On Sunday the car is full of people going somewhere because they decided to, not because a train told them to."
    "I look at the empty strap where the sleeping man would be on a weekday. He is not there. On Sundays the car keeps its secrets to itself."
    hikari "You are previewing again."
    mc "I am looking at a strap."
    hikari "That is what preview looks like from the outside."

    scene bg_school_gate with Fade(0.0, 0.0, 1.5)
    play music "audio/Music/school.mp3" fadein 1.5
    $ phone_map_visit("school")
    scene bg_library with walk_fade
    stop music fadeout 1.0
    play music "audio/Music/library.mp3" fadein 2.0
    play sound "audio/SFX/library_ambiance.mp3" loop

    "The library is almost empty. The reserve desk is a low counter by the window with a stack of stapled handouts."
    "The top copy has Hikari's name written on it in blue pen, small and neat."
    mc "You really put your name on it."
    hikari "I told you."
    mc "Why blue?"
    hikari "Because blue is the color of a person who is allowed to be here."
    mc "(Blue is the color of the can I always pick from the vending machine. She has known that for a week.)"

    "We take a table by the window. I write three questions on the index cards while Hikari watches me with her chin in her hands."
    "It is much harder than I expected. A question is a promise about what you know."
    "I write the first one. どの言葉が季語ですか。Which word is the kigo?"
    "I write the second one. What are the three scripts, and which one was called women's hand?"
    "For the third I write: What did the professor say a city is?"

    hikari "Those are good."
    mc "They're easy."
    hikari "Easy is not bad. You wrote what you know. That is the whole skill."
    mc "I can answer them. I don't feel like I understand them."
    hikari "できる and わかる."
    mc "What?"
    hikari "できる is to be able. わかる is to understand. You can do a thing and not understand it yet. That is allowed."
    hikari "The exam tests できる. Understanding comes later, on the walk home. That is when it counts."

    menu:
        "Ask which one she is better at.":
            mc "Which are you better at? Doing or understanding?"
            hikari "Doing. I have been doing this since I was nine."
            mc "And understanding?"
            hikari "That is what the walk home is for."
            $ reward_attributes_once("day19_library_dekiru", [("insight", "micro")], show="auto")
        "Make her answer the first question.":
            mc "All right. Question one. Which word is the kigo?"
            hikari "The frog. Spring. And you are not allowed to say 'obviously,' because you were the one who did not know it nine days ago."
            mc "I wasn't going to."
            hikari "You made the face."
            $ reward_attributes_once("day19_library_first", [("grace", "micro")], show="auto")
        "Tell her the distinction is a kind of ma.":
            mc "Between doing and understanding there is a gap. That is ma, isn't it?"
            hikari "Yes."
            mc "So I am living in a gap."
            hikari "You have been living in one since you landed. You are just now learning what it is called."
            $ reward_attributes_once("day19_library_ma", [("nerve", "micro")], show="auto")

    "I turn the cards over and start to write a fourth. I do not know why. There is no fourth topic. There are only three."
    "My hand writes it before I decide what it is."

    "ドアの向こうに何がある。"
    "What is on the other side of the door."

    "The handwriting is mine. The question is not."
    mc "I didn't write this."
    hikari "Let me see."
    "I turn the card toward her. She looks at it for a moment."
    hikari "It is your handwriting."
    mc "I know it's my handwriting. I didn't write it."
    hikari "Then where did it come from?"
    mc "(A door. A white corridor. A voice that called me a name I was not given. The cards have been saying door for a week.)"
    hikari "Hey."
    mc "I'm here."
    hikari "You were not for a second."
    mc "I was reading the question."
    hikari "That is not what reading looks like."

    call leak_audio

    $ mock_exam_written = True
    $ midterm_ghost_question = True

    "I put the fourth card at the bottom of the stack. I cannot throw it away and I cannot ask her about it again."
    "Instead I do the thing I came here to do."
    mc "My turn. I ask, you answer."
    hikari "I do not like the sound of this."
    mc "Question one. Which word is the kigo?"

    menu:
        "Let her answer properly.":
            hikari "The frog. Spring. The water warm enough to hold a life."
            mc "You learned that from me."
            hikari "I learned it from the lecture. You were taking notes. I was listening."
            mc "(She has been doing this the whole time. I was so busy writing things down that I did not notice she was learning.)"
            $ reward_attributes_once("day19_library_heranswer", [("grace", "micro")], show="auto")
        "Ask her what she is nervous about.":
            mc "What are you nervous about? Your exam."
            hikari "Everything."
            mc "You? You have a system."
            hikari "The system is for the part I know. I am nervous about the part I do not."
            "She says it to the window. It is the second time in two days she has said a true thing to the window."
            $ remember("hikari", "admitted she is nervous about her own exam, the part she does not know")
            $ reward_attributes_once("day19_library_nervous", [("insight", "micro")], show="auto")
        "Show her the fourth card again.":
            "I pull the card back out and hold it up between us."
            mc "Tell me you don't know what this is."
            hikari "I don't know what that is."
            mc "You said it without looking at me."
            hikari "I said it to the card. That is allowed."
            $ reward_attributes_once("day19_library_card", [("nerve", "micro")], show="auto")

    "We study until the light through the window turns the color of weak tea."
    "Hikari answers every question I wrote. She gets all three right. I do not tell her that the fourth one is still in the stack."
    mc "(Three questions I can answer. One question I cannot. That is a ratio I can live with for two days.)"

    scene bg_home_exterior_day with walk_fade
    "On the train home, Hikari falls asleep against the window with her book open on her lap."
    "I look at the strap across from us. The sleeping man is back. He is always back on a weekday, and this is technically a Sunday, but I do not say anything."
    "I take the fourth card out of my pocket. The question is still there. The handwriting is still mine."

    $ flush_pending_messages()
    call free_afternoon

    call dinner_open

    mother "And the mock?"
    mc "I wrote it. Hikari answered it. She got everything right."
    hikari "Because he wrote easy questions. I am going to ask for harder ones on Monday."
    father "A good student writes questions they can answer. A great student writes one they cannot."
    mc "I wrote one I cannot."
    father "Then you were great for one question out of four. That is more than most people manage in a year."
    mc "(He does not know about the fourth card. He is answering a different question and he is right anyway.)"

    call dinner_close

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, four cards are on the desk. Mister Plum goes around the bowl once and stops."
    $ night_desk_line = "the fourth card"
    call night_open

    menu:
        "Ask her about the fourth question.":
            mc "The fourth question. What do you think is on the other side of the door?"
            hikari "A room."
            mc "That's it?"
            hikari "You asked what is there, not who. If you had asked who, I would have said something else."
            mc "What would you have said?"
            hikari "Somebody who knows my name."
            $ remember("hikari", "said on the other side of the door is a room, and if asked who, somebody who knows her name")
            $ reward_attributes_once("day19_night_door", [("insight", "micro")], show="auto")
        "Tell her she did well today.":
            mc "You got all three right."
            hikari "I know."
            mc "You're not going to say something about it?"
            hikari "I am going to say it was a nice thing for you to write. And then I am going to be quiet about it."
            mc "(She is terrible at being given a compliment. She is also excellent at it.)"
            $ remember("hikari", "told her she did well on the mock exam and she was bad at accepting it")
            $ reward_attributes_once("day19_night_praise", [("grace", "micro")], show="auto")
        "Say nothing. Put the fourth card under the bowl.":
            "I slide the fourth card under Mister Plum's bowl. The question is still there, under the water and the fish."
            "Hikari does not ask why. She has learned that I do not need her to fill the silence."
            $ remember("hikari", "put the fourth exam card under the goldfish bowl and said nothing")
            $ reward_attributes_once("day19_night_quiet", [("nerve", "micro")], show="auto")

    call night_close

    "Two days. Three questions I can answer and one that arrived in my own handwriting."
    "Tomorrow is the midterm. Written, practical, and a map from memory."
    "I turn off the lamp. The room is dark. The room is not empty."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump monday_midterm
