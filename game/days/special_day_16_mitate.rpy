################################################################################
## DAY 16: THURSDAY, APRIL 23, 2026
## A word for seeing one thing as another, and a shape in the classroom window.
################################################################################

label thursday_mitate:
    $ set_story_day(16)
    call day_transition from _call_day_transition_9

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "The rain from yesterday has washed the window and left the sky very clean."
    "Five days. The tomato timer is still on the desk. I have not plugged it in and I do not know why I keep winding it."
    mc "(It is a small object that does nothing. There are a lot of those in this house. They are not the same as empty.)"

    "My phone buzzes."

    if "sim" in wire_unlocked and confidant_visits.get("sim", 0) < 7:
        $ run_chat("sim", [
            {"them": "Thursday. Somebody is teaching you a word today.", "options": [
                {"label": "\"What word?\"",
                 "send": "What word?",
                 "them": ["I am not saying.", "You will know it when you hear it."]},
                {"label": "\"I have class.\"",
                 "send": "I have class.",
                 "them": ["Good.", "The wall can wait."]},
            ]},
            {"them": "Mitate. Do not look it up."},
        ])
        mc "(He told me not to look it up. I am writing it down instead. That is the same thing with more steps.)"
    else:
        $ run_chat("hikari", [
            {"them": "Thursday is the camera people's day.", "options": [
                {"label": "\"You know their schedule?\"",
                 "send": "You know their schedule?",
                 "them": ["I know everyone's schedule.", "It is not a talent. I live here."]},
                {"label": "\"I have class first.\"",
                 "send": "I have class first.",
                 "them": ["Good.", "Be on time."]},
            ]},
        ])

    "Three knocks. Hikari leans in without coming all the way in."
    hikari "Class day."
    mc "Class day."
    hikari "You have that look."
    mc "What look?"
    hikari "The one where you are deciding whether to tell me you are nervous about the exam."
    mc "That is not the look."
    hikari "It is exactly the look. It has been on your face since Monday."
    "She taps the frame with one finger and is gone."
    mc "(I was not nervous. I was deciding whether to tell her. Those are almost the same thing and she knows it.)"

    call murakami_daily_ping from _call_murakami_daily_ping_3

    scene bg_kitchen with walk_fade

    "Mother wraps something in a cloth and hands it to me before I can sit down."
    mother "For later."
    mc "I'm not going to be there long."
    hikari "What is it?"
    mother "Rice balls. The small ones. He takes the big ones and comes back having eaten nothing."
    father "I ate."
    mother "You moved food around the plate. That is not eating. That is arranging."
    mc "(Father arranges his food. I have never once seen him do it and I have eaten with him sixteen times.)"

    menu:
        "Ask Father why he doesn't eat the rice balls.":
            mc "Why the small ones? You always take the big ones."
            father "A big rice ball is a promise. A small one is a fact."
            mc "I don't understand."
            father "Neither do I. It is something my mother said. Eat the small one."
            $ reward_attributes_once("day16_kitchen_riceball", [("insight", "micro")], show="auto")
        "Ask Hikari what the camera people actually do.":
            hikari "They stand around and argue about light."
            mc "That's it?"
            hikari "And then somebody takes a photograph of a wall and everyone nods."
            mc "That sounds like a serious hobby."
            hikari "It is a serious hobby. That is why they nod."
            $ reward_attributes_once("day16_kitchen_club", [("grace", "micro")], show="auto")
        "Take the cloth and say thank you.":
            "I take the cloth. It is still warm."
            mc "Thank you."
            mother "That is the whole thing. Go."
            mc "(She has fed me every day for sixteen days. I still do not know what to do with that.)"
            $ reward_attributes_once("day16_kitchen_thanks", [("nerve", "micro")], show="auto")

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The walk to the station is dry but the gutters are still full, and the whole street sounds like it is quietly draining."
    "I know the platform now. I know which car has the least crowded door at this hour. I know the one-minute sign is honest."
    mc "(The professor asked for a map from memory. I have been drawing one without a pen for two weeks.)"
    "A shop on the corner has kept an old sign: 江戸. The paint is thin at the edges."
    "A delivery van is parked half on the pavement. Nobody goes around it. They step up and keep walking."
    hikari "Edo. That is what the city was called before Tokyo."
    mc "The shop under it is new."
    hikari "They kept the sign when they rebuilt. People still look at it."
    mc "(The sign is older than the shop. It is the only part of the street that remembers.)"

    scene bg_school_gate with Fade(0.0, 0.0, 1.5)
    play music "audio/Music/school.mp3" fadein 1.5
    $ phone_map_visit("school")

    scene bg_campus_interior with walk_fade
    scene bg_lecture_hall with walk_fade
    play music "audio/Music/classroom.mp3" fadein 1.0

    "The professor has written one word on the board: 見立て."
    professor "Mitateru. To see one thing as another thing."
    "He draws a stone under it, then a mountain, then a line between them."
    professor "A rock as a mountain. A bucket as the moon. The poets did this long before anyone gave it a name."
    professor "You already know the pieces. The frog gave you the season. Mono no aware gave you the passing. Mitate gives the thing a second life."
    mc "(The frog was the start. This is the next step.)"
    professor "A small object carries a large one. That is the whole lesson."

    "He tells us to look out the window and choose one thing."
    professor "Do not photograph it. Frame it. One line in your notebook. What it is, and what else it is."

    menu:
        "See the stone by the path as a mountain.":
            "There is a stone outside, no bigger than my hand. I write that it is a mountain in a country the size of the window."
            "I frame it the way he said, with my eyes. There is no photograph, but I know where the mountain is."
            $ mitate_photo = True
            professor "What did you see?"
            mc "A mountain. It is wearing a stone for today."
            professor "Good. It has never been a mountain before. Today it is one."
            $ reward_attributes_once("day16_lecture_mitate", [("insight", "micro")], show="auto")
        "Write down what it actually is.":
            "I write: a stone. It is a small grey stone beside the path."
            professor "And?"
            mc "That is all it is."
            professor "Then look again. It will not mind."
            "I look again. There is a crack in it that goes the whole way across. For a second it is a country with a river in it."
            $ reward_attributes_once("day16_lecture_plain", [("grace", "micro")], show="auto")
        "Ask him what he sees when he looks out the window.":
            mc "What do you see? When you look out there."
            professor "A lake."
            mc "There's no lake."
            professor "There is a puddle by the gate. It is a lake on days when I have not slept. That is the exercise."
            "I write his answer down instead of mine. It is the first thing I have copied from the board without being told to."
            $ reward_attributes_once("day16_lecture_ask", [("nerve", "micro")], show="auto")

    "I look up from the notebook. The classroom window has gone dark enough to hold the room like a mirror."
    "Behind my own face, in the glass, there is a person in a white coat standing in the corridor. Facing away."
    "I look again. The glass shows the room, my own face, and the row of empty chairs behind me."
    mc "(The person was there. I am not going to argue with a window.)"

    call leak_audio from _call_leak_audio_1

    professor "You are looking at the glass."
    mc "I saw someone. A white coat. Facing away."
    professor "Then write them down. That is what the exercise is for."
    "I write: a person. I do not write what they were wearing. The sentence is strange enough already."

    scene bg_campus_interior with walk_fade

    "Hikari is waiting by the stairs with the tomato timer."
    hikari "Did you see it?"
    mc "See what?"
    hikari "The thing you were supposed to see as something else."
    mc "A stone."
    hikari "And?"
    mc "And a mountain. For about a minute."
    hikari "That is the whole class in two objects. You have learned it."
    "She takes the timer back without asking and puts it in her bag."
    mc "You don't need that. It isn't plugged in."
    hikari "I know. It is for the shape of it."
    mc "(The shape of it. I think I know what she means.)"

    $ flush_pending_messages()
    call free_afternoon from _call_free_afternoon_7

    call dinner_open from _call_dinner_open_9

    father "And the Japanese class?"
    mc "Mitate. Seeing one thing as another."
    father "What did you see?"
    mc "A stone. Then a mountain. For about a minute."
    father "Good. Most things are only a mountain for a minute. That is enough."
    hikari "He also saw a person who wasn't there."
    mc "Hikari."
    hikari "What? It is a true thing. It is also the kind of thing you say at dinner."
    mother "Was it a nice person?"
    mc "I couldn't tell. It was facing away."

    call dinner_close from _call_dinner_close_9

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the notebook is on the desk. The word 見立て sits at the top of the page, bigger than the rest."
    $ night_desk_line = "the notebook"
    call night_open from _call_night_open_9

    menu:
        "[tag_nerve] Rank 2: Ask her if she has ever seen it too." if has_attribute("nerve", 2):
            mc "Have you ever seen it? In a window. Facing away."
            hikari "I look at windows. I do not always like what is in them."
            mc "(She did not say no. I decide to leave it there.)"
            $ reward_attributes_once("day16_night_window", [("nerve", "micro")], show="auto")
        "Tell her about the person in the window.":
            mc "There was someone in the classroom window. A white coat. Facing away."
            hikari "A reflection."
            mc "It was facing away."
            hikari "Do you believe it was a person?"
            mc "I believe that I looked."
            hikari "That is not the same thing. That is the most honest answer you could have given."
            $ log_memory("hikari", "told her about the figure in the classroom window and said he believed that he looked")
            $ reward_attributes_once("day16_night_reflection", [("insight", "micro")], show="auto")
        "Ask her what she would see as something else.":
            mc "If you had to do the exercise. What would you see as another thing?"
            hikari "You."
            mc "What would I be?"
            hikari "A person who is going to be fine."
            mc "That's not mitate. That's a prediction."
            hikari "It is mitate. I am looking at you and seeing a thing you are not yet."
            $ log_memory("hikari", "said if she had to do the mitate exercise she would see him as a person who is going to be fine")
            $ reward_attributes_once("day16_night_hers", [("grace", "micro")], show="auto")
        "Say nothing. Leave the notebook on the desk.":
            "I do not say anything. Hikari is half asleep already, which is her way of staying."
            "The word sits on the page. I do not look at the window."
            $ log_memory("hikari", "left the mitate notebook on the desk and said nothing")
            $ reward_attributes_once("day16_night_quiet", [("nerve", "micro")], show="auto")

    call night_close from _call_night_close_9

    "Mitate. Seeing one thing as another. I have been doing it without knowing the word: a fuse, a date, a country, a plum with a job."
    "Tomorrow is Friday. Murakami has a lesson and I have a homework line I still cannot read."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump friday_sounds
