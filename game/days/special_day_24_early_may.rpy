################################################################################
## DAY 24: FRIDAY, MAY 1, 2026
## Golden Week has started. Exams done, the city already leaving.
################################################################################

label special_day_24_early_may:
    $ set_story_day(24)
    call day_transition from _call_day_transition_16

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Friday. The first of May. Golden Week has started and the city is already packing."
    "I wake up with my notebook open on the desk. The corridor map is in it now, drawn from memory. The doors that are not in order."
    mc "(He said bring one question. I brought one. I have been carrying it for three days.)"

    "My phone buzzes."

    if "tanaka" in wire_unlocked:
        $ run_chat("tanaka", [
            {"them": "Golden Week. The city empties. You staying?", "options": [
                {"label": "\"I am staying.\"",
                 "send": "I am staying.",
                 "them": ["Good. The combini never closes. Someone has to buy the rice balls."]},
                {"label": "\"I do not know yet.\"",
                 "send": "I do not know yet.",
                 "them": ["Decide before Tuesday. After that the trains are full of people who did."]},
            ]},
        ])
        mc "(I have seen the pictures. The trains fill up.)"
    else:
        $ run_chat("hikari", [
            {"them": "The city is already leaving. Are you?", "options": [
                {"label": "\"I am staying.\"",
                 "send": "I am staying.",
                 "them": ["Good. I am staying too. We will see who cracks first."]},
                {"label": "\"Maybe.\"",
                 "send": "Maybe.",
                 "them": ["Maybe is a door that opens both ways. Pick one before it closes."]},
            ]},
        ])
        mc "(A maybe leaves both doors open. That is the trouble with it.)"

    call murakami_daily_ping from _call_murakami_daily_ping_10

    scene bg_kitchen with walk_fade

    "The kitchen is warm. The plum is on the windowsill. It has been there all week, ripening."
    father "Last day before the break."
    mc "I know."
    father "Use the afternoon. Do not let it go to the sofa."
    mc "I will."
    mother "He is right. You have been sitting too much since the midterm."
    hikari "I was going to suggest something."
    father "What?"
    hikari "The river. The one by the station. The water is high this time of year."
    father "The river?"
    hikari "He needs to see something that moves. He has been staring at that map all week."
    mc "(She is talking about the river. She is also talking about me. I do not know which one she means.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The walk to the station is the walk I know now. The crack in the pavement. The shrine at the corner."
    "Half the shop grilles are already half down. The city is packing itself into boxes."
    hikari "You are quiet."
    mc "I am thinking about the results."
    hikari "You passed."
    mc "I did."
    hikari "Then stop thinking about them. The river does not care about your grade."

    scene bg_station with walk_fade
    scene bg_platform with walk_fade
    scene bg_train_interior_day with walk_fade

    "The train is not crowded. The sleeping man is on the end seat, as usual, with his chin on his chest."
    mc "(He is here again. He is always here. I do not know if that is comforting or not.)"

    scene bg_school_gate with Fade(0.0, 0.0, 1.5)
    play music "audio/Music/school.mp3" fadein 1.5
    $ phone_map_visit("school")
    scene bg_campus_interior with walk_fade
    scene bg_department_hall with walk_fade

    "The professor's office. Same room. Same desk. Same wall of books."
    "The door is closed. There is light under it, thin and steady. I stand with my hand on the notebook and do not knock."
    mc "(One question, as he asked. The corridor. The doors that are not in order. I carried it up the stairs. I cannot carry it through a door.)"
    "After a while I turn around and go to class."

    scene bg_lecture_hall with walk_fade

    "Murakami is at the front of the room. She writes a single line on the board and turns around."
    murakami "Copy one small true thing into your notebook. Not a quote. A detail. The kind only a resident would write down."
    mc "(I copy the plum on the windowsill. The way the light sits on it in the morning. That is a detail. That is mine.)"
    murakami "Next week I may be away. Office hours will move. I will leave a note."
    mc "(She said it the way she says everything. Like it is already decided.)"

    scene bg_campus_interior with walk_fade
    scene bg_school_gate with walk_fade
    scene bg_station with walk_fade
    scene bg_platform with walk_fade
    scene bg_train_interior with walk_fade

    "The train is emptying. People with suitcases. People with bags. The sleeping man is still asleep."
    mc "(He does not know the city is leaving. Or he does not care. Either way, he is here.)"

    scene bg_river with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The river is high. The water is the colour of tea with milk. Hikari stands at the railing and watches it."
    hikari "This is the lesson."
    mc "What lesson?"
    hikari "The city leaves. Every year. The shops close, the trains fill, the streets go quiet. And then it comes back."
    hikari "You think the city is a place. It is a habit. It leaves and it returns, and you are the one who stays."
    mc "(She means the river. She also means me. I still cannot tell which.)"

    "A small shop across the street has a window full of plush toys. One of them is a bear with a red ribbon."
    "Hikari stops in front of the glass. She does not say anything at first."
    mc "(She is looking at the bear. The one with the ribbon.)"
    "She leans closer. Her breath makes a small circle on the glass and it fades."
    hikari "How much is it?"
    mc "There is a tag. On the ear."
    "She reads it. Her mouth moves a little, the way it does when she is doing arithmetic she does not like."
    "Her hand goes to the door. It stays on the handle. The shop is open. Someone is moving inside."
    "Then she lets go. She steps back and puts her hands in her pockets."
    hikari "Not today."
    mc "You could go in."
    hikari "I know."
    "She looks at the bear one more time. Then she turns away."
    mc "(She wanted it. I could see it in her hand on the door. I do not ask again.)"

    "We walk to the railing. The water is close and loud."
    "There is a strip of flat stones at the edge of the path, left there by the low water of some other month."
    mc "I used to do this."
    hikari "Do what?"
    mc "Skip stones."
    "I pick one up. It is flat and grey and fits in my palm. I turn it over once."
    mc "You have to find the flat one. Then you throw it low."
    hikari "Then throw it."
    "I throw it low. It hits the water and stops. One plop, then nothing. It goes under."
    hikari "One."
    mc "That was not a skip. That was a sink."
    hikari "One is a number. You can improve on one."
    "I try again. This time I lean down and bring my arm across my body, wrist flat, the way I remember."
    "The stone leaves my hand too high. It comes down on its face. Plop."
    hikari "Two."
    mc "You are counting the wrong thing."
    hikari "I am counting the tries. Somebody has to."

    menu:
        "[tag_grace] Rank 2: Say you were counting the tries, not the skips." if has_attribute("grace", 2):
            mc "I was counting too. Not the skips. The tries."
            mc "Four. You laughed on four."
            hikari "I did not know you were keeping score."
            $ reward_attributes_once("day24_river_count", [("grace", "micro")], show="auto")
        "Skip stones.":
            "I pick a third stone. I do not think about it. I just throw."
            "It touches once. Then again. Then it is gone under the far water."
            hikari "Three. That one skipped."
            mc "That one skipped."
            hikari "Do it again."
            "I do it again. It sinks. She laughs, short and surprised, and covers her mouth."
            hikari "Four."
            $ log_memory("hikari", "counted my skipped stones at the river and laughed when the next one sank")
            $ reward_attributes_once("day24_river_stones", [("grace", "micro")], show="auto")
        "Ask about the bear.":
            mc "The bear in the window. You wanted it."
            hikari "I wanted to look at it. That is all."
            mc "You had your hand on the door."
            hikari "The door was cold. I was checking."
            "She says it lightly. Then she is quiet for a moment, and the quiet is real."
            hikari "Some things are better left in the window. For now."
            mc "(For now. She said for now. I keep that.)"
            $ log_memory("hikari", "left the bear in the window and said not today, and then said for now")
            $ reward_attributes_once("day24_river_bear", [("insight", "micro")], show="auto")
        "Watch the water.":
            "I stop picking up stones. We stand at the railing and watch the water go."
            "It does not hurry. It is a lot of water and it has a long way to go."
            hikari "You are not going to try again?"
            mc "No."
            hikari "Good. I like this better."
            "She rests her arms on the railing. The city noise is behind us and the river noise is in front and neither one is asking for anything."
            $ log_memory("hikari", "watched the high river with me and liked the quiet better than the stones")
            $ reward_attributes_once("day24_river_watch", [("nerve", "micro")], show="auto")

    "A stone in my hand is still warm from the path. I put it back down with the others."
    hikari "You are better at some things than you think."
    mc "Not stones."
    hikari "No. Not stones."

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    "We walk home. The streets are quieter than they were this morning. The plum is still on the windowsill when I get in."
    hikari "Thank you. For the river."
    mc "You showed me the river."
    hikari "I showed you the habit. The river was already there."
    mc "(The river was here before the city. It will be here after. I do not say that out loud.)"

    scene bg_kitchen_night with walk_fade
    "The kitchen is warm. Mother has made dinner. Rice, soup, and something with fish."
    mother "Sit. Eat. You must be hungry after the river."
    father "The river?"
    hikari "He needed to get out and see something move."
    father "The river moves. The city moves. He should move too."
    hikari "He is moving. He is just slow."
    father "Slow is fine. Stopped is not."
    mc "(I have been stopped. I am moving now. Slowly.)"
    "We eat. The plum stays on the windowsill. Nobody says anything else."

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the window is open a crack. The city is doing its night sounds, but fewer of them. Half the neighbourhood is already gone."
    "The notebook is on the desk. The corridor map. The doors that are not in order."
    "The plum is on the windowsill downstairs. I can see it from here if I lean out."
    $ night_desk_line = "a notebook and a plum on the windowsill"
    call night_open from _call_night_open_16

    menu:
        "Ask Hikari about Murakami's note." :
            mc "Murakami said she may be away next week."
            hikari "She said that?"
            mc "She said she would leave a note."
            hikari "Then she will leave a note. That is what teachers do when they are being honest."
            mc "(Then she will leave one. She is not the kind to say a thing and not do it.)"
            $ log_memory("hikari", "said Murakami leaving a note is what teachers do when they are being honest")
            $ reward_attributes_once("day24_night_note", [("insight", "micro")], show="auto")
        "Ask about the river." :
            mc "The river was high."
            hikari "It is always high this time of year. The snow melts somewhere far away and the water comes here."
            hikari "Everything comes from somewhere. That is the lesson."
            mc "(Everything comes from somewhere. I had not thought about the snow.)"
            $ log_memory("hikari", "said the river is high because the snow melts far away")
            $ reward_attributes_once("day24_night_river", [("grace", "micro")], show="auto")
        "Watch the plum. Say nothing." :
            "I do not say anything. The plum is on the windowsill. The city is doing its fewer night sounds."
            "Hikari watches with me. She does not fill the silence."
            mc "(The city leaves. The plum stays. I am learning which one I am.)"
            $ log_memory("hikari", "watched the plum in silence on the first evening of the holiday week")
            $ reward_attributes_once("day24_night_quiet", [("nerve", "micro")], show="auto")

    call night_close from _call_night_close_16

    "The city is leaving. I am staying. The notebook is on the desk. The plum is on the windowsill."
    "The lamp goes off. The room is dark. The room has its own shape in the dark."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5

    jump act2_day_router