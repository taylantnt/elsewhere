################################################################################
## DAY 16: THURSDAY, APRIL 23, 2026
## Circle, a vending machine, and the art of seeing one thing as another thing.
################################################################################

label thursday_mitate:
    $ set_story_day(16)
    call day_transition

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "The rain from yesterday has washed the window and left the sky very clean, which feels like an attempt to make up for something."
    "Five days. The tomato timer is still on the desk. I have not plugged it in and I do not know why I keep winding it."
    mc "(It is a small object that does nothing. There are a lot of those in this house. They are not the same as empty.)"

    "My phone buzzes."

    if "sim" in wire_unlocked:
        $ run_chat("sim", [
            {"them": "Thursday. The wall is waiting.", "options": [
                {"label": "\"What does it want?\"",
                 "send": "What does it want?",
                 "them": ["To be photographed.", "It has never asked for anything else."]},
                {"label": "\"I'll be there.\"",
                 "send": "I'll be there.",
                 "them": ["Bring the camera.", "Or don't. I have eleven."]},
            ]},
            {"them": "We are doing mitate today. Do not look it up."},
        ])
        mc "(He told me not to look it up. I am writing it down instead. That is the same thing with more steps.)"
    else:
        $ run_chat("hikari", [
            {"them": "Thursday is the camera people's day.", "options": [
                {"label": "\"You know their schedule?\"",
                 "send": "You know their schedule?",
                 "them": ["I know everyone's schedule.", "It is not a talent. I live here."]},
                {"label": "\"I might go.\"",
                 "send": "I might go.",
                 "them": ["You will. You are already looking at the camera."]},
            ]},
        ])

    "Three knocks. Hikari leans in without coming all the way in."
    hikari "Camera day."
    mc "Camera day."
    hikari "You have that look."
    mc "What look?"
    hikari "The one where you are deciding whether to tell me you are nervous about the exam."
    mc "That is not the look."
    hikari "It is exactly the look. It has been on your face since Monday."
    "She taps the frame with one finger and is gone."
    mc "(I was not nervous. I was deciding whether to tell her. Those are almost the same thing and she knows it.)"

    scene bg_kitchen with walk_fade

    "Mother wraps something in a cloth and hands it to me before I can sit down."
    mother "For the club."
    mc "I'm not going to be there long."
    mother "All the more reason."
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

    scene bg_school_gate with Fade(0.0, 0.0, 1.5)
    play music "audio/Music/school.mp3" fadein 1.5
    $ phone_map_visit("school")
    scene bg_campus_interior with walk_fade

    "The corridor to the club room smells like fixative and coffee. The tape on the door is still there."
    scene bg_photo_club with walk_fade
    play music "audio/Music/circle.mp3" fadein 2.0

    "Sim is holding a camera up to his eye and photographing the wall. He lowers it when I come in."
    sim "You are early. The wall is not ready."
    mc "How do you know?"
    sim "It has not finished being interesting. Give it a minute."
    "Nami is at the table with a roll of gaffer tape. Tapi is sitting on the windowsill, not helping."
    nami "It is a wall, Sim. It has been a wall for forty years."
    sim "Forty years of being a wall is a lot of practice."
    tapi "At what?"
    sim "At being looked at without ever once looking back. That is rarer than you think."
    "He hands me a camera. Not mine. One of the club's, older and heavier."
    sim "Today we are doing mitate."
    mc "I saw the word in my text. I did not look it up."
    sim "Good. Then it is still yours."
    sim "Mitate is seeing one thing as another thing. A rock as a mountain. A plastic bucket as the moon. The old poets did it with words. We do it with a lens."
    sim "It is not a trick. A trick changes the thing. Mitate changes the person looking."

    "He points at the vending machine in the corner of the room. It hums. It is the loudest thing in here."
    sim "Photograph that."
    mc "The vending machine."
    sim "One photograph. You have twenty minutes. When you are done, tell me what you photographed."
    nami "Last time somebody said 'a vending machine' and Sim made them do it again."
    sim "I did not make him. I asked him to look again. Those are different."
    tapi "They are very slightly different."
    sim "I am paying you in compliments and you are spending them badly."

    menu:
        "Photograph it as a small lit shrine.":
            "I crouch down and frame the machine so the glow of it fills the whole view. The rows of cans become offerings. The slot becomes an altar."
            "I press the shutter."
            $ mitate_photo = True
            sim "What did you photograph?"
            mc "A shrine. It sells thirst and it is always awake."
            sim "Good. It has never once been a shrine before. You have given it a new life and it does not know."
            $ reward_attributes_once("day16_club_shrine", [("insight", "micro")], show="auto")
        "Photograph it exactly as it is.":
            "I frame it straight on. Machine, cans, slot, hum. Nothing added."
            "I press the shutter."
            sim "What did you photograph?"
            mc "A vending machine."
            sim "Then you photographed the wall again. Look at it once more. It will not mind."
            "I look again. The machine is lit from inside. For a second it looks like a small room somebody forgot to come back to."
            $ reward_attributes_once("day16_club_plain", [("grace", "micro")], show="auto")
        "Ask him what he sees when he looks at it.":
            mc "What do you see? When you look at it."
            sim "A fridge that only speaks Japanese."
            mc "That's a joke."
            sim "It is also a description. The best ones are both."
            "I take the photograph while he is still talking, which is the first time I have taken a photograph without deciding to."
            $ mitate_photo = True
            $ reward_attributes_once("day16_club_ask", [("nerve", "micro")], show="auto")

    "I look at the screen on the back of the camera."
    "The machine is there. The glow is there. And in the dark glass of its door, behind my own reflection, there is a person standing who was not in the room when I took the photograph."
    "White coat. Facing away."
    "I lower the camera. The room is the room. Nami is fighting the tape. Tapi is still on the windowsill. The machine hums."
    mc "(Mitate changes the person looking. I have been looking at this room for twenty minutes and I do not think I am the person who walked in.)"

    call leak_audio

    sim "You have gone quiet."
    mc "I saw something in the reflection."
    sim "In the glass?"
    mc "A person. White coat. Facing away."
    "Sim does not laugh. He takes the camera from me and looks at the screen, then at the machine, then back at the screen."
    sim "White coat. Facing away."
    mc "You see it?"
    sim "I see a reflection of the window, which is behind you. There is a coat on the rack by the door with a white cloth over it."
    "He turns the screen toward me. The reflection is a reflection. The coat is a coat."
    sim "Mitate. You saw the cloth and made it a person. That is what the mind does when it has too much time in a room."
    mc "(I do not tell him the coat was not there. I am not sure it was not there.)"
    sim "Keep the photograph. The machine has a new life now. Do not let it go back to being a machine."

    "The club goes on around us. Nami gets the tape to obey. Tapi takes it from her and makes it obey better."
    "I put the rice balls on the table. They are gone before I can count them."
    mc "(I did not see anybody eat them. They are simply gone. That is how a lot of things happen in this club.)"

    scene bg_campus_interior with walk_fade

    "Hikari is waiting by the stairs with the tomato timer."
    hikari "Did you see the wall?"
    mc "I saw the wall."
    hikari "And?"
    mc "And a vending machine."
    hikari "That is the whole club in two objects. You have learned it."
    "She takes the timer back without asking and puts it in her bag."
    mc "You don't need that. It isn't plugged in."
    hikari "I know. It is for the shape of it."
    mc "(The shape of it. That is the second time somebody has said a version of that today.)"

    $ flush_pending_messages()
    call free_afternoon

    call dinner_open

    father "And the camera club?"
    mc "We photographed a vending machine."
    father "What did it become?"
    mc "A shrine. For twenty minutes."
    father "Good. Most things are only a shrine for twenty minutes. That is enough."
    hikari "He also saw a person who wasn't there."
    mc "Hikari."
    hikari "What? It is a true thing. It is also the kind of thing you say at dinner."
    mother "Was it a nice person?"
    mc "I couldn't tell. It was facing away."

    call dinner_close

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the photograph is on the desk. The vending machine glows. The person in the glass is a smudge if I look directly at them and a person if I do not."
    $ night_desk_line = "the photograph"
    call night_open

    menu:
        "Tell her about the person in the reflection.":
            mc "There was someone in the glass. A white coat. Facing away."
            hikari "Sim said it was a cloth on the rack."
            mc "He did."
            hikari "Do you believe him?"
            mc "I believe that he looked."
            hikari "That is not the same thing. That is the most honest answer you could have given."
            $ remember("hikari", "told her about the figure in the vending machine reflection and said she believed that Sim looked")
            $ reward_attributes_once("day16_night_reflection", [("insight", "micro")], show="auto")
        "Ask her what she would photograph as something else.":
            mc "If you had a camera. What would you photograph as another thing?"
            hikari "You."
            mc "What would I be?"
            hikari "A person who is going to be fine."
            mc "That's not mitate. That's a prediction."
            hikari "It is mitate. I am looking at you and seeing a thing you are not yet."
            $ remember("hikari", "said if she had a camera she would photograph him as a person who is going to be fine")
            $ reward_attributes_once("day16_night_hers", [("grace", "micro")], show="auto")
        "Say nothing. Leave the photograph on the desk.":
            "I do not say anything. Hikari is half asleep already, which is her way of staying."
            "The machine glows on the desk. In the glass, the smudge is still there."
            $ remember("hikari", "left the vending machine photograph on the desk and said nothing")
            $ reward_attributes_once("day16_night_quiet", [("nerve", "micro")], show="auto")

    call night_close

    "Mitate. Seeing one thing as another. I have been doing it without knowing the word: a fuse, a date, a country, a plum with a job."
    "Tomorrow is Friday. Murakami has a lesson and I have a homework line I still cannot read."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump friday_sounds
