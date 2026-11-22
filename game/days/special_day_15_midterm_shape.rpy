################################################################################
## DAY 15: WEDNESDAY, APRIL 22, 2026
## The midterm gets a shape: three parts, one date, and a word for studying ahead.
################################################################################

## Week-three story state. Ren'Py defaults run at init regardless of file order,
## so the whole week's new flags live here rather than scattered across days.
default midterm_result = ""
default midterm_q1_correct = False
default midterm_q2_correct = False
default midterm_q3_correct = False
default midterm_ghost_question = False
default professor_corridor_note = False
default previewed_lesson = False
default mitate_photo = False
default sound_word_written = ""
default mock_exam_written = False
default festival_mask_seen = False

label wednesday_preview:
    $ set_story_day(15)
    call day_transition from _call_day_transition_8

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "The rain Mother promised on Tuesday arrives on Wednesday, which is how weather keeps its promises in this house."
    "It is a thin rain. It taps the window with one finger, then stops, then starts again."
    mc "(Six days. That is the number now. On Day 8 it was a worry; today it has a date.)"
    "The boxes are still stacked against the wall. The desk has become mine in the way a chair becomes yours after you sit in it enough times."

    "My phone buzzes against the desk."

    if "hana" in wire_unlocked and confidant_visits.get("hana", 0) >= 7:
        $ run_chat("hana", [
            {"them": "The evening class list came.", "options": [
                {"label": "\"Art class?\"",
                 "send": "Art class?",
                 "them": ["Drawing. Figure drawing. I'm... scared. But I bought pencils."]},
                {"label": "\"That's a lot of pencils.\"",
                 "send": "That's a lot of pencils.",
                 "them": ["It is. I... I think that's the point. Too many, and I can't stop."]},
            ]},
            {"them": "The quiet room is still open. I'm just... not in it."},
        ])
        mc "(She still writes. She just does it from somewhere else now.)"
    elif "hana" in wire_unlocked:
        $ run_chat("hana", [
            {"them": "The reserve desk has a stack of your handout.", "options": [
                {"label": "\"Is that bad?\"",
                 "send": "Is that bad?",
                 "them": ["It is popular.", "I put my name on the top copy. You can come and get it."]},
                {"label": "\"I already have one.\"",
                 "send": "I already have one.",
                 "them": ["Then you are ahead of the stack.", "Ahead is a good place to be."]},
            ]},
            {"them": "The quiet room is open until six."},
        ])
        mc "(She sends three messages, then a fourth to say the first three were not urgent. They were urgent.)"
    else:
        $ run_chat("hikari", [
            {"them": "Don't make plans after class.", "options": [
                {"label": "\"It's Wednesday.\"",
                 "send": "It's Wednesday.",
                 "them": ["I know what day it is.", "That is why I am saying it."]},
                {"label": "\"I have a system now.\"",
                 "send": "I have a system now.",
                 "them": ["You do not have a system.", "You have a desk. I am going to fix that."]},
            ]},
        ])
        mc "(She has been awake longer than me. I can tell by the punctuation.)"

    "Three knocks. Hikari slides the door open with a kitchen timer in her hand."
    hikari "Morning. You are exactly where I left you."
    mc "I didn't move."
    hikari "That is not the same as sleeping."
    "She sets the timer on my desk. It is the cheap kind with a loud bell."
    mc "What's this?"
    hikari "A system. Twenty-five minutes of work, five minutes of not work."
    mc "That's a tomato."
    hikari "It is a timer."
    mc "It's shaped like a tomato."
    hikari "The shape is not the system. The system is the system. Are you arguing with dinner?"
    mc "No."
    hikari "Then come down. The rice has something in it."

    call murakami_daily_ping from _call_murakami_daily_ping_2

    scene bg_kitchen with walk_fade

    "The kitchen smells like rice and the sharp salt smell of the plum in the middle of it."
    "Mother sets a bowl in front of me. There is a small red plum right in the center of the rice."
    mc "There's a plum in my rice."
    mother "There is a plum in everyone's rice."
    hikari "It's the flag of effort."
    mc "It's a plum."
    hikari "It is a plum with a job."
    father "It is a plum. It is not a strategy."
    mother "It is both. Eat it. The sour part wakes you up."
    mc "(The rice is red around the plum. I have never seen a breakfast look so much like a plan.)"

    menu:
        "Ask why the plum goes in the middle.":
            mc "Why the middle? Does it work better there?"
            mother "It is the middle because the middle is where you look first."
            mother "You see the plum, you remember you are doing a thing, you eat the rice. That is all it does."
            mc "(A reminder you can eat. This house is full of those.)"
            $ reward_attributes_once("day15_kitchen_plum", [("insight", "micro")], show="auto")
        "Let Hikari quiz me right now.":
            mc "All right. Ask me something."
            hikari "What is a kigo?"
            mc "The season word. The thing that puts the poem in a time."
            hikari "And the frog?"
            mc "Spring."
            hikari "Good. You are allowed one smug face. Use it now."
            mc "(I use it. It feels undeserved and excellent.)"
            $ reward_attributes_once("day15_kitchen_quiz", [("grace", "micro")], show="auto")
        "Ask Father if he ever took an exam like this.":
            mc "Did you take exams? When you were my age."
            father "I took them."
            mc "Were you nervous?"
            father "I was certain I would fail. That is different from nervous."
            mc "Did you?"
            father "Every time. And every time I came home and ate. That is the part I remember."
            $ reward_attributes_once("day15_kitchen_father", [("nerve", "micro")], show="auto")

    father "Six days."
    mc "You've been counting too."
    father "A job is a thing you make every day. An exam is a thing that makes you. Different."
    mother "Tetsuo, he is eating."
    father "I am eating. I am also saying a thing."
    hikari "Those aren't mutually exclusive."
    mc "(I said that on my first Tuesday. She has been waiting eight days to use it back.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The rain has stopped by the gate. The street is shining, which makes it look like a different street."
    "Hikari walks beside me instead of ahead of me. I notice, and she notices me noticing."
    hikari "What?"
    mc "Nothing."
    hikari "You looked at my feet."
    mc "I was looking at the pavement."
    hikari "My feet are on the pavement. It is a small step from one to the other."
    mc "(She is very hard to have a private thought near.)"

    scene bg_station with walk_fade
    scene bg_platform with walk_fade
    "The train comes in one minute. It is always one minute. I no longer check the sign to see if it is lying."
    "Hikari stops behind the yellow strip and looks down at it."
    hikari "Miyake invented these in 1965. A person can feel the platform end without seeing it."
    mc "(I have stood beside this strip for two weeks. I never asked who thought of it.)"
    scene bg_train_interior with walk_fade
    "A man in a suit is asleep standing up, one hand through the strap."
    mc "(Same man? No. It is a different man. There are a thousand of them and they all sleep the same way.)"

    scene bg_school_gate with Fade(0.0, 0.0, 1.5)
    play music "audio/Music/school.mp3" fadein 1.5
    $ phone_map_visit("school")
    "The guard on the morning shift nods once. I nod back. This is the whole conversation and it is enough."

    scene bg_campus_interior with walk_fade
    scene bg_lecture_hall with walk_fade
    play music "audio/Music/classroom.mp3" fadein 1.0

    "The professor has written two words on the board before anyone sits down."
    "予習. 復習."
    professor "Yoshuu. Preview. Fukushuu. Review."
    "He underlines the first one twice."
    professor "Most students review. You learn a thing, you go home, you look at it again. This is a country you already live in. It is comfortable there."
    professor "Preview is a country you have not visited. You open the page before the lesson. You do not understand it. You let your hand know the shape of it anyway."
    mc "(Murakami said the hand learns before the head. The professor is saying the same thing in a suit.)"
    professor "Why preview? Because the exam is in the preview country. Nothing on Monday will be new to you. It will only be new to the people who stayed home."

    menu:
        "Ask what the practical actually tests.":
            mc "The practical. What does it test, exactly?"
            professor "Whether you can be a person in a shop for thirty seconds."
            mc "That's all?"
            professor "That is everything. Buy something. Ask the price. Say thank you. Leave. Most people cannot do it without turning into either a tourist or a statue."
            $ reward_attributes_once("day15_lecture_practical", [("insight", "micro")], show="auto")
        "Read the preview word aloud.":
            mc "予習. Yoshuu."
            professor "Again."
            mc "予習."
            professor "Good. You have now said a word you did not know six days ago. Monday is more of the same, only longer."
            $ previewed_lesson = True
            $ reward_attributes_once("day15_lecture_preview", [("nerve", "micro")], show="auto")
        "Copy both words into the margin and circle the first.":
            "I write them under the frog and the pond from Day 8. The page is starting to look like a map of a country I am slowly entering."
            mc "(Preview first. Review second. I have been doing it backwards my whole life.)"
            $ reward_attributes_once("day15_lecture_write", [("grace", "micro")], show="auto")

    professor "The midterm is Monday. Three parts. Written, practical, and a map."
    mc "A map?"
    professor "You will draw the route from here to a place you have been. From memory. No phone."
    "He says it the way he says everything, as if he is reading the weather."
    professor "You have all been walking this city for two weeks. Now find out whether you were looking at it."
    mc "(I think of the yellow line. The platform. The way I never check the one-minute sign anymore.)"
    mc "(I have been looking. I did not know I was being tested on it.)"

    scene bg_campus_interior with walk_fade

    "Hikari is waiting by the stairs with the tomato timer in her hand."
    hikari "Twenty-five minutes. You have until five."
    mc "Is the timer for me or for you?"
    hikari "For the system. The system does not care who it belongs to."
    hikari "Go somewhere. Preview something. I will be at the library."
    mc "You have a library?"
    hikari "I have a reserve copy with my name on it, which is better."
    "She walks off before I can ask whose name was on it first."

    $ flush_pending_messages()
    call free_afternoon from _call_free_afternoon_6

    call dinner_open from _call_dinner_open_8

    father "And the plum?"
    mc "It worked. I remembered the kigo."
    father "A strategy, then."
    mother "I told you."
    hikari "He got one smug face out of it. I saw it."
    mc "It was a small face."
    hikari "It was a flag of effort. That is the whole plum."

    call dinner_close from _call_dinner_close_8

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the tomato timer sits on the desk next to the handout. It is not plugged into anything. I do not tell Hikari."
    $ night_desk_line = "the tomato"
    call night_open from _call_night_open_8

    menu:
        "[tag_nerve] Rank 2: Admit the practical scares you more than the writing." if has_attribute("nerve", 2):
            mc "It is not the writing I am worried about. It is the practical."
            hikari "Being a person in a shop."
            mc "I will have to do it in front of strangers."
            hikari "You already do. You just do not call it studying."
            $ reward_attributes_once("day15_night_practical", [("nerve", "micro")], show="auto")
        "Tell her about preview.":
            mc "The professor says the exam is in the country you have not visited yet. Preview."
            hikari "Yoshuu."
            mc "You know it?"
            hikari "I made you a study schedule. Of course I know it."
            mc "(She made me a study schedule. Of course she did.)"
            $ log_memory("hikari", "told her about yoshuu, preview, and she said she already put it in his study schedule")
            $ reward_attributes_once("day15_night_preview", [("insight", "micro")], show="auto")
        "Ask what she is doing about her own exam.":
            mc "What about you? Your exam."
            hikari "I have a system."
            mc "The tomato?"
            hikari "A different tomato. Mine is bigger."
            "She says it lightly, but she says it to the window, not to me."
            mc "(She has been the one asking the questions for fifteen days. I do not know what to do with the reversal.)"
            $ log_memory("hikari", "asked about her own exam and she said she had a bigger tomato")
            $ reward_attributes_once("day15_night_hers", [("grace", "micro")], show="auto")
        "Say nothing. Wind the tomato timer.":
            "I wind the timer. It ticks once, twice, then stops. Hikari does not ask why I am winding something that is not plugged in."
            "She has learned that I do not need her to fill the silence."
            $ log_memory("hikari", "wound the tomato timer in silence and she did not ask why")
            $ reward_attributes_once("day15_night_quiet", [("nerve", "micro")], show="auto")

    call night_close from _call_night_close_8

    "Six days. The midterm has a date and three parts. Breakfast had a plum."
    "I turn off the lamp. The tomato timer ticks once in the dark, then stops."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump thursday_mitate
