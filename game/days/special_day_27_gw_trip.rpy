################################################################################
## DAY 27: MONDAY, MAY 4, 2026
## Golden Week. A family day out. The three of them, somewhere quiet.
################################################################################

label special_day_27_gw_trip:
    $ set_story_day(27)
    call day_transition from _call_day_transition_18

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Monday. The fourth of May. Greenery Day. The city is still half-empty."
    "I wake up to the sound of my father in the hallway, which is unusual. He is usually gone before the house makes a sound."
    mc "(He is home. It is a holiday. I had forgotten what his footsteps sound like in the morning.)"

    "My phone buzzes."

    if "tanaka" in wire_unlocked:
        $ run_chat("tanaka", [
            {"them": "Holiday. The combini is quiet. Nobody is buying anything. It is strange.", "options": [
                {"label": "\"Enjoy it.\"",
                 "send": "Enjoy it.",
                 "them": ["I am. It will not last. Tomorrow the shelves will be empty again."]},
                {"label": "\"I am going out.\"",
                 "send": "I am going out.",
                 "them": ["With the family? Good. Family is the only shift that does not end."]},
            ]},
        ])
        mc "(Family is the only shift that does not end. He would know.)"
    else:
        $ run_chat("hikari", [
            {"them": "Father says we are going somewhere today. He did not say where.", "options": [
                {"label": "\"Do you know?\"",
                 "send": "Do you know?",
                 "them": ["No. He just said 'shoes you can walk in.' That is all I got."]},
                {"label": "\"He is planning something.\"",
                 "send": "He is planning something.",
                 "them": ["Father does not plan. He decides. There is a difference."]},
            ]},
        ])
        mc "(Father decides. There is a difference.)"

    call murakami_daily_ping from _call_murakami_daily_ping_12

    scene bg_kitchen with walk_fade

    "The kitchen is warm. The plum is on the windowsill. Mother has made rice and miso. Father is at the table, which is also unusual."
    father "Eat. We are leaving in an hour."
    mc "Where?"
    father "Somewhere quiet."
    hikari "That is not an answer."
    father "It is the only answer that matters. You will see when we get there."
    mother "Take your jacket. It will be cooler than you think."
    hikari "He always says that."
    father "Because it is always true."
    mc "(It is always cooler than I think.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The three of us walk to the station. Father walks ahead, as he always does. Hikari walks beside me."
    hikari "He is not going to tell us where we are going."
    mc "I know."
    hikari "He has been like this since I was small. He picks a place and he goes. We follow."
    mc "Do you mind?"
    hikari "No. I like it. It is the only time he is not at work."
    mc "(It is the only time he is not at work. She knows him.)"

    scene bg_station with walk_fade
    scene bg_platform with walk_fade
    scene bg_train_interior_day with walk_fade

    "The train is empty. The sleeping man is not here. Even he has gone somewhere for the holiday."
    mc "(He is always here. I do not know where he goes. Nobody does.)"

    "We get off two stops before the city centre. Father leads us through a street I have never walked down."
    "The houses get smaller. The gardens get bigger. A cat watches us from a wall and does not move."
    father "Here."
    "He stops in front of a small shrine. It is not famous. There is no gate, no crowd, no souvenir shop. Just a path of stone steps and a bell that hangs still."
    hikari "This is where you go?"
    father "This is where I go. When I need to."
    mc "You never told us."
    father "You never asked. And it is not the kind of thing you tell people. It is the kind of thing you find out by being taken."
    mc "(Some places are not for telling. They are for being taken to.)"

    scene bg_shrine with walk_fade
    play music "audio/Music/(Hanabi night) lanterns_at_dusk.mp3" fadein 2.0

    "We walk up the steps. The stone is worn smooth in the middle, where feet have been going for a long time."
    "Near the top there is a small stone basin under a wooden roof. Water runs into it from a bamboo pipe. A row of ladles rests on the edge."
    hikari "Temizuya. You wash before you greet the kami."
    mc "I know. I have seen it."
    hikari "Seeing is not the same as doing. Come here."
    "She takes a ladle and holds it out to me. The wood is wet and cool."
    hikari "Right hand first. Scoop. Pour over your left."
    "I scoop and pour. The water is cold. It runs off my fingers and back into the basin."
    hikari "Now the ladle in your left hand. Pour over your right."
    "I switch hands. The ladle is awkward on the other side. I pour too fast and most of the water misses."
    hikari "Slow. The water is not in a hurry. Neither are you."
    "I try again. This time it lands."
    hikari "Now pour into your left hand and rinse your mouth. Do not touch the ladle to your lips."
    "I lift the ladle straight to my mouth and drink from it."
    hikari "No. Not like that."
    "She does not laugh. She does not look away. She takes the ladle from my hand and shows me. Her palm is cupped under the stream. The water is carried to her mouth and then spat quietly onto the stones."
    hikari "Your hand is the cup. The ladle is only the pourer."
    mc "I did it wrong."
    hikari "You did it first. That is different."
    "She hands the ladle back. Father is standing a few steps away, waiting without waiting."

    menu:
        "Follow her exactly.":
            "I take the ladle again and do it her way. Right hand. Left hand. The water in my palm. The quiet spit. The handle tipped clean."
            "She watches every step. She does not nod until the last one."
            hikari "Now you have washed."
            mc "I washed before."
            hikari "You rinsed. There is a difference."
            mc "(There is a difference. She says that the way Father does.)"
            $ log_memory("hikari", "taught me the temizuya order and said rinsing is not washing")
            $ reward_attributes_once("day27_temizuya_follow", [("grace", "micro")], show="auto")
        "Ask why the order matters.":
            mc "Why this order? Why not just wash your hands and go?"
            hikari "Because the order makes you slow down. If you do it fast, you are only cleaning. If you do it in order, you are arriving."
            father "The water does not care how you use it. You care. That is the point."
            "He says it without turning around. He has been listening the whole time."
            mc "(Arriving. Not cleaning. I have been arriving everywhere without noticing.)"
            $ log_memory("hikari", "said the temizuya order is for arriving, not for cleaning")
            $ reward_attributes_once("day27_temizuya_why", [("insight", "micro")], show="auto")
        "Watch Father do it first.":
            "I step back and let Father go ahead."
            "He does it slowly. No wasted motion. Right hand, left hand, the water in his palm, the quiet spit, the handle tipped clean. He does not look at me while he does it."
            "Then he steps aside and waits."
            "I copy him. It is easier to copy than to be taught."
            hikari "He is a good teacher when he is not trying to be."
            father "Hm."
            mc "(He does not teach. He shows. It is the same thing, done his way.)"
            $ log_memory("hikari", "watched Father do the temizuya and copied him step for step")
            $ reward_attributes_once("day27_temizuya_watch", [("nerve", "micro")], show="auto")

    "Father rings the bell. The sound is small and clean."
    "He bows. Hikari bows. I bow. Nobody says anything for a long time."
    hikari "It is quiet."
    father "That is the point."
    hikari "Is that why you come here? For the quiet?"
    father "I come here because the city is loud and this place is not. That is enough of a reason."
    mc "(It is enough of a reason.)"

    "We sit on a bench near the shrine. The trees are old. The light comes through them in pieces."
    father "You have been doing well. The midterm. The job."
    mc "I passed."
    father "I know. I saw the results."
    mc "You saw them?"
    father "Your mother showed me. She was proud. She did not say so, but she was."
    hikari "She never says so."
    father "No. She does not. That is how she shows it."
    mc "(She shows it by not saying it.)"
    father "The professor. The one you keep talking about."
    mc "What about him?"
    father "You are building a lot on one man."
    mc "He is a good teacher."
    father "Good teachers are not the only teachers. The city teaches you too, if you let it."
    hikari "He is right, you know."
    mc "I know."
    father "Do not build your week around one man. Build it around yourself. The man is a bonus."
    mc "(The man is a bonus. I have been treating him like the whole thing.)"

    "We sit for a while longer. Hikari finds a cat behind the shrine and talks to it. Father closes his eyes. I look at the trees."
    "The light moves through the leaves. The bell hangs still. The city is somewhere beyond the trees, but it cannot be heard from here."
    hikari "This is the best place you have shown us."
    father "It is not for showing. It is for being."
    hikari "Then thank you for being it with us."
    father "Hm."
    mc "(He does not say thank you. The 'hm' is the thank you.)"

    "On the way down the steps there is a small office beside the shrine. A wooden counter. A glass case of omamori in paper envelopes."
    "Father stops. He does not say anything. He takes out his wallet and goes to the counter."
    hikari "What are you doing?"
    father "Wait here."
    "He speaks to the woman behind the counter. She nods and brings out three small charms on a tray. He pays. He does not ask us which ones."
    "He comes back and hands one to Hikari. Then one to me. He puts the third in his jacket pocket."
    hikari "What are they for?"
    father "For the days I am not there."
    "He says it plainly. No weight in his voice. It is the same voice he uses for the weather."
    hikari "You are always there."
    father "Not always."
    "She turns her charm over in her hand. It is small, cloth, a knot of thread at the top. She does not open it."
    mc "(He bought them without asking. He handed them out without explaining. That is how he says things.)"

    menu:
        "[tag_grace] Rank 2: Give Hikari your charm without making her explain." if has_attribute("grace", 2):
            "I hold out my charm."
            mc "Here. There's room on your bag."
            hikari "You are giving me yours?"
            mc "I am giving you mine."
            "She ties it to her bag next to the first one. They hang together, small and quiet."
            hikari "You did not explain it."
            mc "Neither did he."
            hikari "No. But I understood his."
            mc "(She understood his. I do not ask what she understood.)"
            $ remember("hikari", "gave her his omamori without asking her to explain Father's", "hikari_charm", show_notice=False)
            $ reward_attributes_once("day27_omamori_hikari", [("grace", "micro")], show="auto")
        "Keep it in my pocket.":
            "I put the charm in my pocket and close my hand around it. It is light. It is the kind of thing you forget you are carrying."
            hikari "You are not going to ask what it is for?"
            mc "He told us."
            hikari "He told us the short answer."
            mc "The short answer is enough."
            "She looks at me for a moment. Then she nods."
            mc "(I will keep it in my pocket. When I need it, I will remember where it came from.)"
            $ log_memory("hikari", "kept Father's omamori in my pocket without asking for more")
            $ reward_attributes_once("day27_omamori_keep", [("nerve", "micro")], show="auto")
        "Leave mine for Mother.":
            "I do not put it in my pocket. I ask the woman behind the counter for a slip of paper and a pen."
            "I write Mother's name on the paper and fold it around the charm."
            hikari "What are you doing?"
            mc "She should have one too."
            hikari "She did not come."
            mc "That is why."
            "I put it in my jacket, on the other side from my keys, where it will not get lost."
            hikari "You did not write why."
            mc "She will know."
            mc "(Mother will know. She knows the way Father knows. Quietly, and without being told.)"
            $ log_memory("hikari", "wrapped my omamori for Mother and carried it home without a note")
            $ reward_attributes_once("day27_omamori_mother", [("grace", "micro")], show="auto")

    "We walk down the steps. Hikari keeps her charm close. Father does not look back."

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    "We walk home. The streets are still quiet. Father walks ahead, but slower than this morning."
    hikari "He is different here."
    mc "Different how?"
    hikari "Quieter. At home he is always thinking about the next thing. Here he is thinking about this thing."
    mc "I noticed."
    hikari "Do not tell him I said that."
    mc "I will not."
    hikari "He would be embarrassed. He does not like being seen."
    mc "(That is why the shrine is his.)"

    scene bg_kitchen_night with walk_fade
    "The kitchen is warm. Mother has made dinner. There is rice and grilled mackerel and pickled radish."
    mother "How was it?"
    father "It was quiet."
    mother "Good."
    hikari "He showed us a shrine. A small one. No tourists."
    mother "I know the one. He goes there when he needs to."
    father "I do not go there when I need to. I go there because I want to."
    mother "Same thing."
    father "It is not the same thing."
    mother "It is. You just do not like admitting it."
    mc "(She has decided what he means. He has decided not to argue. That is the marriage.)"
    father "The food is getting cold."
    mother "Then eat."
    "We eat. Nobody says anything else about the shrine."

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the window is open a crack. The city is doing its night sounds, but fewer of them. The holiday is still here."
    "My notebook is on the desk. The corridor map I drew from memory. The doors that are not in order."
    "The plum is on the windowsill downstairs. I can see it from here if I lean out."
    $ night_desk_line = "a notebook and a plum on the windowsill"
    call night_open from _call_night_open_18

    menu:
        "Ask Hikari about the shrine." :
            mc "He goes there when he needs to."
            hikari "He goes there when he wants to. There is a difference."
            mc "He said the same thing."
            hikari "He has thought about it. He does not say things he has not thought about."
            "She says it like a fact she has checked."
            $ log_memory("hikari", "said father does not say things he has not thought about")
            $ reward_attributes_once("day27_night_shrine", [("insight", "micro")], show="auto")
        "Ask about the professor." :
            mc "He said not to build my week around one man."
            hikari "He has been watching you build it. That is why he said it."
            mc "You think so?"
            hikari "I know so. He does not say things he has not thought about."
            mc "(He has been watching. I did not know he was watching.)"
            $ log_memory("hikari", "said father had been watching me build my week around one man")
            $ reward_attributes_once("day27_night_professor", [("grace", "micro")], show="auto")
        "Watch the garden. Say nothing." :
            "I do not say anything. The garden is dark. The trees are black shapes against the sky."
            "Hikari watches with me. She does not fill the silence."
            mc "(We are still building. The walls are not where they were this morning.)"
            $ log_memory("hikari", "watched the garden in silence on the night of the shrine")
            $ reward_attributes_once("day27_night_quiet", [("nerve", "micro")], show="auto")

    call night_close from _call_night_close_18

    "The city is quiet. The plum is on the windowsill. The notebook is on the desk."
    "I reach for the lamp. The room goes dark. Something in the corner stays where it is."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5

    jump act2_day_router
