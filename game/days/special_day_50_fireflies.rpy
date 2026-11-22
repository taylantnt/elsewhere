################################################################################
## SPECIAL DAY 50: THE LIGHTS THAT DO NOT LAST
## Wednesday, May 27, 2026. The rain takes a night off, and Hikari takes him out
## of the city, to a slow river, to see the thing that comes for two weeks a
## year and asks nothing of anyone.
##
## Hikari day. Warm, and the last warm one for a while. This is the single glitch
## seed of the block: planted on the walk back, and left there, unexplained.
################################################################################

label special_day_50_fireflies:
    $ set_story_day(50)
    call day_transition from _call_day_transition_33
    $ last_afternoon_place = None
    $ last_afternoon_hikari_tour = False

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Wednesday, and for the first time in a week the sky has let go of the rain and gone the color of an old coin."
    "I notice it at the window before I notice anything else. The quiet. Rain makes a sound you stop hearing, and when it stops you hear the absence of it the way you hear a refrigerator switch off."

    mc "(Five days of rain, and now a dry, warm evening. Hikari noticed it an hour before I did. She notices weather the way other people notice a bill.)"

    "My phone buzzes."

    $ run_chat("hikari", [
        {"them": "It stopped. Do not make other plans.", "options": [
            {"label": "\"Plans? I do not have plans.\"",
             "send": "Plans? I do not have plans.",
             "them": ["You were going to do homework.", "Homework will still be there. The river will not."]},
            {"label": "\"What is at the river?\"",
             "send": "What is at the river?",
             "them": ["Something that happens for two weeks a year.", "Wear long sleeves. The bugs are out."]},
        ]},
    ])
    mc "(Two weeks a year. In this house that is a countdown, not a description.)"

    call murakami_daily_ping from _call_murakami_daily_ping_20

    scene bg_kitchen with walk_fade

    "The kitchen is back to normal. The laundry rack is down. The room is just a room again."
    mother "You are going out tonight."
    hikari "The river."
    mother "Ah. It is that time. Take the small torch. The path along the water has no lights and the stones are loose."
    mc "What is at the river?"
    mother "Ask her. It is her thing, not mine. She has gone every year since she was small."
    mc "(Her thing. There is a list of Hikari's things and it is written down nowhere, and I keep finding new names on it.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/school.mp3" fadein 2.0

    "The school day is a school day. Notes, a bell, a professor who talks about the rainy season as if he had invented it. In two days the term is over. Nobody says so, but everyone is counting, the way you count the minutes in the last hours of a shift."

    scene bg_campus_interior with walk_fade

    "After class I walk out through the department corridor. The wall is a wall. The third tile squeaks. The summer program notice is still on the board, curling at one corner now from the damp."
    mc "(I look at the stretch of wall where the door used to be, and there is only wall, and I no longer know whether I am relieved or disappointed. Maybe those two are the same feeling and I have been sorting them wrong.)"

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    stop music fadeout 2.0

    "I am home before dark and out again after dinner. Hikari is at the gate with a small torch and a long-sleeved shirt she has clearly already decided I am wearing."
    hikari "Two things. One. Long sleeves. Two. When we get there you do not talk. You do not have to whisper. You just do not talk."
    mc "What are we going to see?"
    hikari "You will see it. That is why I am not telling you."

    scene bg_station with walk_fade
    scene bg_platform with walk_fade
    scene bg_train_interior with walk_fade

    "We take the train the wrong way out of the city, the direction you only go if you know why you are going. Two stops past the last place I have a name for."

    scene bg_river_fireflies with Fade(0.0, 0.0, 1.5)
    stop music fadeout 1.5
    play music "audio/Music/(Hanami) summer_night_embers.mp3" fadein 2.5

    "And then we are walking a path along a slow river in the dark, and the trees close over the path, and Hikari switches off the torch, and there is nothing but the sound of the water."

    "And then I see the first one."
    "A small green light, drifting low over the water, going out, coming back on somewhere else. Then another. Then three, then ten, then I stop counting, because counting is a way of not looking."
    "Fireflies. Hotaru. The whole riverbank is full of them, small slow sparks just above the black water, each one a light with no reason except itself."
    mc "(I have read the word. I have never once seen a thing that made the word small.)"

    "Hikari stands beside me and does not say anything, because she said she would not, and because there is nothing to say. We stand at the rail for a long time."

    "The fireflies do not hurry. They rise from the grass and drift and dim and come back. They do it slowly, the way a thing does when it has two weeks to live and has decided to spend them being calm. I do not know how I know they have two weeks. She said it in a message this morning, and it stayed with me."

    hikari "They come out for two weeks. Then they are gone until next year."
    mc "Where do they go?"
    hikari "Nowhere. They die. That is the whole thing. You wait a year and it happens for fourteen days and then it does not, and everyone who came to see it goes home and has to remember it to keep it."
    mc "(She says has to remember it. As if remembering were a job. For her I think it is.)"

    menu:
        "[tag_insight] Rank 3: Ask why she gave three conditions." if has_attribute("insight", 3):
            mc "Free, rare, ending. You did not say which one thing it is."
            hikari "I gave you three conditions. A thing with all three is worth it."
            mc "Then the reason is the list. I will keep the list."
            $ reward_attributes_once("day50_night_list", [("insight", "micro")], show="auto")
        "Ask her why people make a whole night of it.":
            mc "Why do people do this? Come all the way out here to stand in the dark and look at bugs."
            hikari "Because it is free and it is rare and it does not last. That is a very short list of things. Anything with all three is worth a train ride."
            mc "That is almost a definition of something."
            hikari "It is a definition of something. I will let you decide of what."
            mc "(Free, rare, and ending. She leaves the rest to me.)"
            $ log_memory("hikari", "said the fireflies are free and rare and do not last, which is a short list of things worth a train ride")
            $ reward_attributes_once("day50_night_poem", [("insight", "micro")], show="auto")
        "Cup your hands and try to hold one.":
            "One drifts close, low and slow, and I put my hands up the way you catch a moth, careful, more careful than I have been about anything in weeks."
            "It lands. It walks on my palm, small and cold and faint, and it lights, once, and the light comes up through my fingers pink because the light is going through my hand."
            "Then it lifts and drifts away, and I do not close my hand, and Hikari watches me not close my hand."
            hikari "You could have caught it."
            mc "Then it would have stopped being the thing I came to see."
            hikari "Yes. Good."
            mc "(It is a very small test and I passed it and that is all it was.)"
            $ log_memory("hikari", "watched me let the firefly go and only said good")
            $ reward_attributes_once("day50_night_hand", [("nerve", "micro")], show="auto")
        "Watch her instead of the river.":
            "I turn and look at Hikari watching the fireflies, and it is a better thing than the fireflies. Her face in the faint green light is young in a way it never is in the day, and she does not know I am looking, and I let myself look, because tonight she said not to talk and looking is not talking."
            "She catches me at it. Of course she does."
            hikari "You are supposed to be looking at them."
            mc "I was."
            hikari "You were looking at me. I can feel the difference. I always can."
            mc "You are the one standing between me and them."
            "She does not answer that. She turns back to the river, and I think, though I cannot be sure in the dark, that she is pleased, and that she would deny it with everything she has."
            $ log_memory("hikari", "caught me watching her instead of the fireflies and did not tell me to stop twice")
            $ reward_attributes_once("day50_night_her", [("grace", "micro")], show="auto")

    "We stay until the cold gets into our sleeves. Hikari says one more, and then one more, and then the one more after that, which is how anyone leaves a place they love."

    "On the walk back I look over my shoulder one last time."

    call leak_audio from _call_leak_audio_8

    "There are two people standing at the rail where we were standing. A tall one and a short one, side by side, looking out at the water. They are facing away, and the fireflies move around them the same slow way."
    mc "(They were not there when we came. There is no path to that spot except the one we walked. I did not see or hear anyone pass us.)"
    "I look again."
    "There is no one at the rail. The fireflies are the fireflies, and the river is the river, and Hikari is ahead of me on the path with the torch she said she would not turn on."
    $ remember("mc", "two figures stood at the rail where they had been, with no path to that spot, and were gone when he looked again", "two_figures_at_rail")
    mc "(I do not tell her. Not tonight. Tonight the river was the whole thing, and I am not going to put a second thing in it.)"

    "I follow her light down the path. It goes out and comes back, goes out and comes back, all the way to the station, which is exactly what it is supposed to do."

    scene bg_train_interior with walk_fade
    play music "audio/Music/train.mp3" fadein 2.0

    "The last train is mostly empty. Hikari sleeps against the window, which she will deny. The city comes back in pieces, the lights getting denser the closer we get, the way it does."

    scene bg_home_exterior_night with walk_fade
    $ night_street()

    "Home after midnight. The house is dark and warm and full of the small sounds a house makes when everyone in it is asleep except the two of us."

    scene bg_kitchen_night with walk_fade
    $ room_ambient(True)

    "Hikari makes tea without asking, which at this hour is a sentence of its own."
    hikari "Well."
    mc "Well."
    hikari "You did not talk. You looked at it and you did not talk. That is the whole thing. Most people talk."
    mc "(Most people talk. She did not, and she wanted me not to, and so we had an evening made of two people not talking, and it was full.)"

    scene bg_room_night with stair_fade
    $ room_ambient(True)

    "Upstairs, the notebook is open. I write one line about the fireflies. I do not write about the two people at the rail. That one I keep off the page, which is what I have started doing with the things I am not ready to see written down."

    $ night_desk_line = "the window, and the dark doing nothing behind it"

    call night_open from _call_night_open_27

    "Hikari comes in with two cups. She sits on the floor against the bed. The house is so quiet that the tea sounds loud going into the cup."
    hikari "I am not staying. You have class."
    mc "So do you."
    hikari "That is why I am not staying."

    menu:
        "Tell her about the two people at the rail.":
            mc "On the path back. I looked over my shoulder. There were two people at the rail. Where we were standing."
            hikari "Two people."
            mc "A tall one and a short one. Facing the water."
            "She does not laugh. She does not tell me I imagined it. That, somehow, is the thing that unsettles me most."
            hikari "Did they turn around?"
            mc "No."
            hikari "Then they were other people. There is a whole city. People come to see the fireflies. We were not the only ones on the river."
            mc "There was no path. Nobody passed us."
            hikari "Then you missed them. People miss things. You miss things all the time. You missed the hydrangeas until I made you look."
            mc "(She is right that I miss things. She is also answering too fast, and she knows I noticed the speed, and she does not take it back.)"
            $ log_memory("hikari", "answered too quickly about the two people at the rail, and did not laugh, and did not take it back")
            $ reward_attributes_once("day50_night_tell", [("insight", "micro")], show="auto")
        "Ask her why she goes every year.":
            mc "You do this every year. Why?"
            hikari "Because it is the one thing in the calendar that does not ask anything of me."
            mc "Everything asks something of you."
            hikari "Yes. Exams, and Father, and the house, and the future. Everything has a hook in it. The fireflies do not have a hook. They do not care if I come. They do not know I came. They do the one thing they do, for two weeks, and then stop."
            mc "So you go to watch a thing that does not need you."
            hikari "I go to watch a thing that does not need me and find that I am still there. It is restful. It is the only restful thing I know."
            mc "(Everyone needs something from her. I need things from her, and I know it. For two weeks a year she goes to a river and stands next to something that does not, and that is how she stays alive.)"
            $ log_memory("hikari", "said the fireflies are the only thing in her year that does not need anything from her")
            $ reward_attributes_once("day50_night_why", [("grace", "micro")], show="auto")
        "Say nothing. Finish the tea.":
            "I do not talk. She said not to talk at the river and I think the rule holds here, in the dark, at midnight, with the tea."
            "She drinks hers slowly. The house sleeps. Somewhere a train, then the quiet, then a train again, the last ones of the night going back and forth for no one."
            "Before she goes she looks at the window where I was looking and says it is a good window, and goes, and I do not know if she meant the window."
            $ log_memory("hikari", "looked at the window I had been staring at and said it was a good window, at midnight")
            $ reward_attributes_once("day50_night_quiet", [("nerve", "micro")], show="auto")

    call night_close from _call_night_close_27

    "I take the cups down and rinse them so the morning will not know. In the kitchen the laundry rack is folded in the corner and the whole house is doing its six sounds."
    "Somewhere north of the city, on a slow river under the trees, the lights are still going out and coming back, going out and coming back, for another two weeks, for whoever else needs a thing that does not need them."
    mc "(The river was the whole thing. I keep the rest in my pocket. One night is not enough evidence to make a person believe anything, and I would rather have the fireflies than the answer.)"

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
