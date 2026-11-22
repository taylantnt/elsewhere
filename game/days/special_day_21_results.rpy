################################################################################
## DAY 21: TUESDAY, APRIL 28, 2026
## Results. Two words in red become a conversation, and the week closes.
################################################################################

label tuesday_results:
    $ set_story_day(21)
    call day_transition from _call_day_transition_14

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Tuesday. The third week has run out of days."
    "The exam paper is still on the desk with two words in red in the margin, as if a thing written in red cannot be folded away."
    "Mister Plum is in his bowl. He has been in the bowl for four days and has not once tried to leave, which I am starting to find reassuring."
    mc "(I am going to see the professor at eleven. I have decided to be nervous about it only between now and then.)"

    "My phone buzzes."

    if "tanaka" in wire_unlocked:
        $ run_chat("tanaka", [
            {"them": "You came into my store yesterday and did not point at anything.", "options": [
                {"label": "\"I practised.\"",
                 "send": "I practised.",
                 "them": ["Good.", "Do not let it go to your head. The forks are still in the same place."]},
                {"label": "\"You helped.\"",
                 "send": "You helped.",
                 "them": ["I was working.", "You were the one who asked."]},
            ]},
        ])
        mc "(He says I asked. I did ask. I have been learning to ask.)"
    else:
        $ run_chat("hikari", [
            {"them": "He wrote see me. That means something.", "options": [
                {"label": "\"What does it mean?\"",
                 "send": "What does it mean?",
                 "them": ["I do not know. That is why I said it means something."]},
                {"label": "\"It's probably fine.\"",
                 "send": "It's probably fine.",
                 "them": ["It is probably interesting. Those are different."]},
            ]},
        ])

    "Three knocks. Hikari comes in carrying the tomato timer and nothing else."
    hikari "I'm taking the timer."
    mc "Why?"
    hikari "You tried to wind it four times yesterday. You are not allowed today either."
    mc "I didn't try yesterday."
    hikari "You did. You kept reaching for my pocket. I watched your hand."
    mc "(There is no version of this where I have a private sleep.)"
    hikari "How did your own exam go?"
    mc "You mean the midterm."
    hikari "No. Mine. You asked me on Sunday and I made the face."
    mc "I didn't make a face."
    hikari "You made the face that means 'I am about to be kind to you and I do not know how.'"
    "She sits on the edge of the desk and does not look at me."
    mc "I think you did well."
    hikari "That is not an answer. That is the kind thing."
    mc "You got every question right on Sunday."
    hikari "Sunday was my exam. Monday was mine too."
    mc "(Two days. Two exams. She has been carrying both of them and I noticed only one.)"
    $ add_affection("sister", 1)

    call murakami_daily_ping from _call_murakami_daily_ping_8

    scene bg_kitchen with walk_fade

    "There is a plum in the middle of the rice. A smaller plum than Monday's."
    mother "The last plum of the week."
    mc "Is there such a thing?"
    mother "There is today."
    father "He has been tapping the table for three days."
    mc "That was his idea."
    father "It was your idea. I am merely carrying it. Like a rope."
    mother "He has been waiting all week to use that."
    father "It is a good line."

    menu:
        "Ask Hikari how her exam actually went.":
            mc "Hikari. Your exam. Really."
            hikari "I finished it."
            mc "That isn't what I asked."
            hikari "It is the answer I have. Ask me again on Thursday."
            mc "(She has been the one asking questions for twenty-one days. I am going to learn to wait.)"
            $ reward_attributes_once("day21_kitchen_hers", [("grace", "micro")], show="auto")
        "Ask Father about the rope.":
            mc "Does your back hurt? From the rope."
            father "Yes."
            mc "Then why do you do it?"
            father "Because on one night a year the neighbourhood is a thing you can hold. Somebody has to hold it."
            mc "(He has been saying things like this for three weeks. I am finally starting to hear them.)"
            $ reward_attributes_once("day21_kitchen_rope", [("insight", "micro")], show="auto")
        "Eat the plum without saying anything.":
            "I eat the plum. It is smaller but just as sour. Mother watches me finish it and says nothing."
            mc "(A reminder you can eat. She has been feeding me the same lesson for a week.)"
            $ reward_attributes_once("day21_kitchen_plum", [("nerve", "micro")], show="auto")

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The walk to the station is the walk I have taken every day for three weeks. I know the crack in the pavement by the pharmacy. I know which shop puts its chairs out first."
    "I know the small shrine without looking for it now. That is the difference three weeks makes."
    "Its red torii is at the edge of the street, half hidden by a shop sign."
    hikari "A torii marks where the street ends and the shrine begins. Red keeps bad things out, they say."
    mc "(The paint is faded on the side facing the road. I never saw it until today.)"

    scene bg_station with walk_fade
    scene bg_platform with walk_fade
    scene bg_train_interior with walk_fade
    "The sleeping man is not on the Tuesday train. Tuesdays belong to somebody else."
    mc "(I do not know his name. I know the shape of his sleep. That is a kind of knowing too.)"

    scene bg_school_gate with Fade(0.0, 0.0, 1.5)
    play music "audio/Music/school.mp3" fadein 1.5
    $ phone_map_visit("school")
    scene bg_campus_interior with walk_fade
    scene bg_department_hall with walk_fade

    "The professor's office is a small room with a desk, two chairs, and a wall of books nobody has taken down in years."
    "He is sitting behind the desk with my exam paper in front of him. The red pen is on the desk, uncapped."
    professor "Sit."
    "I sit. He does not say anything for a while. It is not an uncomfortable silence. It is a ma, which is a silence with room in it."
    professor "You passed."

    mc "(That is the whole thing. That is what I have been walking toward for three days.)"
    mc "Thank you."
    professor "Do not thank me. You knew the answers. I only wrote the number."

    if midterm_q3_correct:
        professor "Question three. You gave me my answer and Murakami's in the same paragraph."
        mc "They are both true."
        professor "They are. I allowed it. That is a thing I do about once a year, so do not expect it again."
    else:
        professor "You answered the question I asked. That is rarer than it sounds. Half this class answered the question they wished I had asked."

    professor "The map was the best in the class."
    mc "The map?"
    professor "You drew the festival street too wide. Everybody else drew straight lines. You drew the street you actually walked. That is what a map is for."
    mc "(I drew the lanterns wider than the others. He noticed. I am going to think about that for a long time.)"

    "He turns the paper around so I can see the fourth answer."
    professor "Now this."
    mc "I wrote what I saw."
    professor "Nobody has ever written that answer. In nineteen years."
    mc "I'm sorry?"
    professor "Do not apologize. You wrote the honest thing. That is not the same as the right thing, but it is rarer."
    "He takes off his glasses and cleans them on his sleeve, which is the first unprepared thing I have seen him do."

    menu:
        "[tag_insight] Rank 2: Ask what not allowed means." if has_attribute("insight", 2):
            mc "You said you are not allowed to answer. Not that you will not."
            professor "Those are different things. You are the first person to notice."
            mc "Then I will ask the other question instead."
            $ reward_attributes_once("day21_office_not_allowed", [("insight", "micro")], show="auto")
        "Ask who the first person was.":
            mc "You said nobody. Does that mean somebody did?"
            professor "Two people have asked me about that corridor. You are the second."
            mc "Who was the first?"
            professor "A student who left in the middle of last term. She drew a door on every map she handed in."
            mc "What happened to her?"
            professor "That is the question I am not allowed to answer. It is also the question I think about."
            $ reward_attributes_once("day21_office_first", [("insight", "micro")], show="auto")
        "Ask what the corridor is.":
            mc "What is it? The corridor."
            professor "I do not know what it is. I know what it measures."
            mc "What does it measure?"
            professor "Whether you will follow a door when it opens. Most people do not. They are normal. You are the second person who asked."
            $ reward_attributes_once("day21_office_what", [("nerve", "micro")], show="auto")
        "Say nothing. Let him finish.":
            "I do not say anything. He puts his glasses back on."
            professor "You are quiet in the right way. That is not the same as having no question."
            mc "I have about forty."
            professor "Bring one tomorrow. The other thirty-nine will wait."
            mc "(Murakami said that. He said it too. This country has one sentence and everybody owns a piece of it.)"
            $ reward_attributes_once("day21_office_quiet", [("grace", "micro")], show="auto")

    professor "Take your paper. Keep the red words."
    mc "Why?"
    professor "Because you will look at them tonight and try to decide whether they mean a door. They do not. They mean I want to see you again."
    "He puts the paper face down on the desk and slides it toward me."
    professor "That is all. Go have an afternoon. You have earned one."
    mc "(He said afternoon. In this house that is a blessing. At school it is a rare event. It is both.)"

    scene bg_campus_interior with walk_fade

    "Hikari is waiting by the stairs with the tomato timer, which she has not let out of her pocket all morning."
    hikari "Well?"
    mc "I passed. The map was the best in the class."
    hikari "Of course it was. You drew my street wide."
    mc "It's not your street."
    hikari "It has the shrine on it. That makes it mine."
    "She puts the tomato timer in my hand and closes my fingers around it."
    hikari "You can have it back now. You did not wind it once today."
    mc "You were counting?"
    hikari "I am always counting."
    mc "(She has been counting the whole time. Every day. I do not know how I missed it.)"
    $ add_affection("sister", 1)

    $ flush_pending_messages()
    call free_afternoon from _call_free_afternoon_12

    call dinner_open from _call_dinner_open_14

    father "And the professor?"
    mc "I passed. The map was the best in the class."
    mother "Of course it was. You walk everywhere with your eyes open."
    father "And the red words?"
    mc "They mean he wants to see me again."
    father "Then you will go."
    mc "I will go."
    father "Good. A thing you are invited to is not a thing you have to understand first."
    hikari "That is a father sentence if I ever heard one."
    father "It is a true sentence. I am allowed one a week."
    mother "He is allowed three. He uses them all at dinner."
    mc "(Three weeks of dinners. I am going to miss this table when the maps stop matching.)"

    call dinner_close from _call_dinner_close_14

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the window is open a crack. The city is doing its night sounds. A siren somewhere east. A dog answering it."
    "The exam paper is on the desk. See me. Two words in red. Mister Plum goes around the bowl and stops."
    $ night_desk_line = "two red words"
    call night_open from _call_night_open_14

    menu:
        "Ask her what she thinks the red words mean.":
            mc "Do you think the red words mean a door?"
            hikari "No."
            mc "You said that fast."
            hikari "Because I thought about it for three days. A door is a place. Red ink is a person asking. Those are different things."
            mc "(She has been thinking about it for three days. She did not say anything because I was the one who was supposed to be frightened.)"
            $ log_memory("hikari", "said the red words are a person asking, not a door, and she had thought about it for three days")
            $ reward_attributes_once("day21_night_red", [("insight", "micro")], show="auto")
        "Tell her about the student who drew doors.":
            mc "He said somebody before me asked about the corridor. A girl who drew a door on every map."
            hikari "Did he say what happened to her?"
            mc "He said it was the question he was not allowed to answer."
            hikari "That is an answer. It is just not a nice one."
            "She says it to the window, which is where she says the true things now."
            $ log_memory("hikari", "heard about the student who drew doors and said a forbidden answer is still an answer")
            $ reward_attributes_once("day21_night_student", [("nerve", "micro")], show="auto")
        "Watch the fish. Say nothing.":
            "I do not say anything. Mister Plum goes around the bowl once. Hikari watches him with me."
            "The city comes in through the open window. A train. A scooter. A door."
            mc "(A room two people build and then leave. We are still building.)"
            $ log_memory("hikari", "watched the goldfish in silence on the last night of the third week")
            $ reward_attributes_once("day21_night_quiet", [("grace", "micro")], show="auto")

    call night_close from _call_night_close_14

    "I turn off the lamp. The dark settles. The room is still there, and so is everything in it."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
