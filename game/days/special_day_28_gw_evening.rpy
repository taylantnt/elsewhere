################################################################################
## DAY 28: TUESDAY, MAY 5, 2026
## The last night of the holiday. Tomorrow, school again.
################################################################################

label special_day_28_gw_evening:
    $ set_story_day(28)
    call day_transition from _call_day_transition_19

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Tuesday. The fifth of May. Children's Day. The holiday is almost over."
    "I wake up late. The house is quiet. Mother is in the kitchen. Father is at the door, about to go to work, even on a holiday."
    "The notebook is on the desk. The corridor map. The doors that are not in order."
    mc "(He said bring one question. I brought one. I have been carrying it for a week.)"

    "My phone buzzes."

    if "tanaka" in wire_unlocked:
        $ run_chat("tanaka", [
            {"them": "Last day of the break. The combini was busy today. Everyone buying kashiwa mochi.", "options": [
                {"label": "\"What is kashiwa mochi?\"",
                 "send": "What is kashiwa mochi?",
                 "them": ["Rice cake wrapped in an oak leaf. The leaf does not fall until the new one grows. It means the family continues."]},
                {"label": "\"I bought one too.\"",
                 "send": "I bought one too.",
                 "them": ["Good. Then you are part of the city now. The city knows you by your snack."]},
            ]},
        ])
        mc "(The leaf does not fall until the new one grows. I did not know that.)"
    else:
        $ run_chat("hikari", [
            {"them": "Last night of the break. Are you ready?", "options": [
                {"label": "\"No.\"",
                 "send": "No.",
                 "them": ["Good. Nobody is. That is why the first day back is always strange."]},
                {"label": "\"I think so.\"",
                 "send": "I think so.",
                 "them": ["You think so. That is not the same as being so. The difference shows on Wednesday."]},
            ]},
        ])
        mc "(The difference will show on Wednesday. I do not know yet which side of it I will be on.)"

    call murakami_daily_ping from _call_murakami_daily_ping_13

    scene bg_kitchen with walk_fade

    "The kitchen is warm. The plum is on the windowsill. There is a bowl of rice on the counter and a stack of oak leaves beside it, dark and smooth."
    "Mother is making kashiwa mochi. Her hands are wet with rice flour. She does not look up when I come in."
    mother "Sit. You can help."
    mc "I do not know how."
    mother "Nobody knows how. You learn by putting your hands in it."

    "She pushes the bowl toward me. The rice is still warm. It sticks to my fingers in a way that is not quite unpleasant. Like holding a small, living thing."
    "The leaves sit in a shallow dish of water. They shine. Each one is the size of my palm, with a hard spine down the middle and edges that turn under."
    mother "Take one. Put the rice in the middle. Not too much. Then fold the leaf over."

    "I take one. The rice is hot and soft and refuses to be a shape. I fold the leaf. It splits at the spine."
    mother "Again."
    "I take another. This one holds. The rice bulges out the sides. It looks like something that has been sat on."
    mother "Good. It is yours. Eat it later."
    mc "It is ugly."
    mother "It is food. Food does not have to be beautiful."

    hikari "Let me try."
    "Hikari takes a leaf and a handful of rice. She is confident about it. She folds the leaf the wrong way and the rice goes everywhere. A single grain lands on her cheek and stays there."
    hikari "This is a stupid food."
    mother "It is a very old food."
    hikari "Old does not mean easy."
    "She tries again. It is worse. She has made a small rice parcel with a leaf wrapped around it like a bandage. She holds it up."
    hikari "Mine is the best one."
    mc "It is falling apart."
    hikari "It is the best one because I made it."
    "Mother laughs. It is a small sound, quickly put away. But it was there."
    "Hikari eats her parcel in two bites. The leaf comes apart in her hand and the rice falls on the plate. She looks at the pieces."
    hikari "It tastes the same."
    mother "It always tastes the same. The leaf is for the look."
    hikari "Then the look is not important."
    mother "The look is for other people. The taste is for you."

    menu:
        "Ask about the leaf.":
            mc "Why the leaf? Why not just the rice?"
            mother "The leaf does not fall until the new leaf grows. The old one stays on the branch through the winter. It holds on."
            "She turns a leaf over in her hand. The underside is pale, almost silver."
            mother "So it means the family continues. The old does not let go until the new one is ready."
            mc "(The leaf holds on. That is the whole idea. Not forever. Just until.)"
            $ log_memory("mother", "said the kashiwa leaf holds on until the new leaf grows")
            $ reward_attributes_once("day28_mochi_leaf", [("insight", "micro")], show="auto")
        "Try to wrap one properly.":
            "I take another leaf. I go slowly. I put less rice in. I press the spine flat with my thumb and fold the edges toward the middle."
            "It works. Mostly. The leaf closes around the rice and stays closed."
            mother "There. You have hands."
            mc "It took four tries."
            mother "The first three taught you. The fourth one is the one you keep."
            "I set it on the plate with the others. It is not the best. It is mine."
            $ log_memory("mother", "taught me to wrap kashiwa mochi and said the first three tries teach you")
            $ reward_attributes_once("day28_mochi_wrap", [("nerve", "micro")], show="auto")
        "Watch her hands.":
            "I stop trying and just watch."
            "Her hands are quick and sure. She does not measure. She has made these so many times the recipe is in her fingers. The rice goes in. The leaf folds. The parcel is set down. Then the next."
            "It is not a job. It is a rhythm. She does it the way other people breathe."
            mc "(She has been making these every year. Before me. Before Hikari. The hands learned it first.)"
            mother "You are watching."
            mc "I am learning."
            mother "Good. Watching is the first kind of learning."
            $ log_memory("mother", "watched her make kashiwa mochi and she said watching is the first kind of learning")
            $ reward_attributes_once("day28_mochi_watch", [("grace", "micro")], show="auto")

    "We make a plate of them. Mine are at the edge, lumpy and leaning. Hikari's are worse. Mother's are perfect and do not look like they were made by hands at all."
    mother "Eat one before you go up."
    "I eat one of mine. The rice is sweet and the leaf smells green and faintly bitter. It tastes like the morning."

    "The morning passes. Hikari and I sit on the roof. The city is still quiet, but less quiet than yesterday. People are coming back."
    hikari "The trains will be full tomorrow."
    mc "They always are."
    hikari "The sleeping man will be back."
    mc "He was gone yesterday."
    hikari "Even him. But he will be back. He is always back."

    "We sit for a while. The wind moves through the trees. Somewhere a child is flying a carp streamer. It is the last day for that too."
    hikari "Are you ready for Wednesday?"
    mc "I do not know."
    hikari "The professor will be there. He always is."
    mc "Murakami said she may be away next week. She said she would leave a note."
    hikari "Then she will leave a note. That is what teachers do when they are being honest."
    hikari "Do not build your week around one man. Father said that."
    mc "He did."
    hikari "He was right."
    mc "I know."

    scene bg_home_exterior_day with walk_fade

    "In the late afternoon Father comes home early, which he never does. He does not explain. He just takes his jacket and waits at the door."
    father "School is school. Go. Come home. That is the shape of a day."
    hikari "Father, it is a holiday."
    father "It is the last hour of a holiday. The shape comes back tomorrow."
    mother "The koinobori will be up until dark."
    father "Then we should go before dark."
    hikari "You never want to go anywhere."
    father "I want to go here."

    "We take the long way. The streets are full of families walking in the same direction, toward water. Nobody is in a hurry. The holiday is almost gone and everyone is spending it the same way."

    scene bg_river_dusk with walk_fade

    "The river is wide and brown and slow. The banks are crowded with families. Someone has strung a line of carp streamers across the water, from one bank to the other."
    "They are big. Blue, red, green, a black one at the head. The wind fills them and they swim in place, facing upstream."
    "One of them is loose. A red carp near the middle has torn free at the tail. It flaps sideways, then hangs, then flaps again. Nobody fixes it. The line goes on holding the others."

    father "The carp swims upstream. Against the current. That is the whole point."
    mc "Why?"
    father "Because if it swims long enough, it becomes a dragon."
    hikari "That is the story."
    father "That is the story."
    mc "Do you believe it?"
    father "I believe the swimming."
    "The wind changes. The carps turn together, all of them, and for a moment they are one fish."
    "He says it without looking at me. The red carp flaps again. The other carps keep their shape."

    menu:
        "Ask Father about the carp.":
            mc "What happens if it stops swimming?"
            father "It goes downstream with everything else. That is not a failure. That is just the river."
            mc "Then why swim?"
            father "Because the river is not going where you want to go."
            "He watches the black carp at the head, the one that leads. Its mouth is open. It is made of cloth and it is doing the only thing it knows."
            mc "(He is not telling me to be a dragon. He is telling me to keep swimming.)"
            $ log_memory("father", "said the carp swims upstream because the river is not going where you want to go")
            $ reward_attributes_once("day28_koinobori_carp", [("nerve", "micro")], show="auto")
        "Ask Mother about the leaf.":
            mc "Does the leaf mean the same thing here? The koinobori and the kashiwa leaf."
            mother "No. The leaf is about staying. The carp is about going. A family needs both."
            "She says it like she has thought about it before. Maybe she has. Maybe every year she thinks about it and never says it out loud."
            hikari "Which one are you?"
            mother "I am the leaf. Your father is the carp. He swims. I hold the branch."
            mc "(She says it plainly. Not sad. Not proud. Just true.)"
            $ log_memory("mother", "said the leaf is about staying and the carp is about going and a family needs both")
            $ reward_attributes_once("day28_koinobori_leaf", [("insight", "micro")], show="auto")
        "Watch the streamers.":
            "I do not ask anything. I watch."
            "The carps move together and apart. The wind takes them and the line holds them. The torn red one keeps trying. It does not know it is torn. It only knows the wind."
            "A small boy on the bank points at it and laughs. His mother pulls his hand down, gently, and says something I cannot hear."
            "The sun goes lower. The carps turn orange, then gray, then shapes against the sky."
            mc "(One of them is broken and the line still holds. That is the thing I will remember.)"
            $ log_memory("father", "watched the koinobori with one torn carp still trying against the wind")
            $ reward_attributes_once("day28_koinobori_watch", [("grace", "micro")], show="auto")

    "We stay until the light goes. The carps do not stop. The torn one does not stop either."
    "On the walk home, Hikari walks beside me and does not say anything. Father walks ahead. Mother walks last, as if she is counting us."

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    "The city is coming back. The lights are on in more windows than last night. The plum is still on the windowsill."

    scene bg_kitchen_night with walk_fade
    "The kitchen smells like miso. Mother is at the stove. Rice and soup, and grilled fish on the counter."
    mother "Eat. Tomorrow is a long day."
    father "It is a normal day."
    mother "Normal is long when you have been away."
    hikari "I am not ready."
    father "Nobody is ready. That is why the first day back is strange."
    mc "Hikari said the same thing."
    father "Then she is right about that."
    "We eat. The torn carp is still out there, still trying. I do not mention it."

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the window is open a crack. The city is doing more night sounds than last night. The holiday is leaving."
    "My notebook is open on the desk. The corridor map, redrawn twice now. The doors still not in order."
    "The plum is on the windowsill. It is darker than it was yesterday."
    $ night_desk_line = "a notebook and a plum on the windowsill"
    call night_open from _call_night_open_19

    menu:
        "Ask Hikari about tomorrow." :
            mc "What do you think will be different?"
            hikari "Nothing. That is the problem. Everything will be the same and you will notice it for the first time."
            mc "(I will notice it for the first time.)"
            $ log_memory("hikari", "said everything will be the same and I will notice it for the first time")
            $ reward_attributes_once("day28_night_tomorrow", [("insight", "micro")], show="auto")
        "Ask about the sleeping man." :
            mc "Do you think he will be on the train tomorrow?"
            hikari "He will be on the train tomorrow. He is always on the train. He does not take holidays."
            mc "Everyone takes holidays."
            hikari "He does not. That is what makes him the sleeping man."
            mc "(He does not take them. That is the whole of him.)"
            $ log_memory("hikari", "said the sleeping man does not take holidays")
            $ reward_attributes_once("day28_night_sleeping", [("grace", "micro")], show="auto")
        "Watch the window. Say nothing." :
            "I do not say anything. The holiday is leaving. The city is louder tonight."
            "Hikari watches with me. She does not fill the silence."
            mc "(The holiday leaves. The city stays. I am learning which one I am.)"
            $ log_memory("hikari", "watched the window in silence on the last night of the holiday")
            $ reward_attributes_once("day28_night_quiet", [("nerve", "micro")], show="auto")

    call night_close from _call_night_close_19

    "The holiday leaves. The city stays. The notebook is on the desk. The plum is on the windowsill."
    "The lamp clicks off. The dark settles. The room is not empty."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5

    jump act2_day_router