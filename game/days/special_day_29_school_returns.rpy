################################################################################
## DAY 29: WEDNESDAY, MAY 6, 2026
## School returns. The rhythm reasserts itself, slightly off.
################################################################################

label special_day_29_school_returns:
    $ set_story_day(29)
    call day_transition from _call_day_transition_20

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Wednesday. The sixth of May. The holiday is over and the city is back."
    "I wake up to the alarm. The notebook is on the desk. The corridor map. The doors that are not in order."
    mc "(The shape comes back today. Father said so. He was right.)"

    "My phone buzzes."

    if "tanaka" in wire_unlocked:
        $ run_chat("tanaka", [
            {"them": "Back to school. The combini was empty this morning. Everyone is on the train.", "options": [
                {"label": "\"I am on the train now.\"",
                 "send": "I am on the train now.",
                 "them": ["Then you are part of the rush. The train is the problem."]},
                {"label": "\"It will be busy again.\"",
                 "send": "It will be busy again.",
                 "them": ["It is already busy. You just have not looked around yet."]},
            ]},
        ])
        mc "(I have not looked around yet. I have been looking at the same window.)"
    else:
        $ run_chat("hikari", [
            {"them": "First day back. How do you feel?", "options": [
                {"label": "\"Strange.\"",
                 "send": "Strange.",
                 "them": ["Good. Strange is honest. Normal is a lie you tell yourself on the first day."]},
                {"label": "\"Fine.\"",
                 "send": "Fine.",
                 "them": ["Fine is not a feeling. Fine is a door you close so nobody sees what is behind it."]},
            ]},
        ])
        mc "(Fine is a door you close. I have used it before.)"

    call murakami_daily_ping from _call_murakami_daily_ping_14

    scene bg_kitchen with walk_fade

    "The kitchen is warm. The plum is on the windowsill. Mother has made rice and miso. Father is at the table, already in his jacket."
    father "First day back."
    mc "I know."
    father "Go. Come home. That is the shape."
    mother "Take your umbrella. It might rain."
    mc "It is not raining."
    mother "It might. The sky does not ask permission."
    hikari "She is right. Take the umbrella."
    mc "(The sky does not ask permission.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The walk to the station is the same walk. The crack has not moved. The shrine has not moved either."
    "The sleeping man is on the end seat, chin on chest, back from wherever the holiday took him."
    mc "(He is back. He is always back.)"

    scene bg_station with walk_fade
    scene bg_platform with walk_fade
    scene bg_train_interior_day with walk_fade

    "The train is full. People with the same faces, going to the same places. The rhythm is back."
    mc "(It is back. All of it. I am inside the rhythm again.)"

    scene bg_school_gate with Fade(0.0, 0.0, 1.5)
    play music "audio/Music/school.mp3" fadein 1.5
    $ phone_map_visit("school")
    scene bg_campus_interior with walk_fade
    scene bg_department_hall with walk_fade

    "The hallway is the same hallway. The same lockers. The same shoes. The same noise."
    "But something is different. I cannot tell what. The rhythm is back, but it is off by a beat."
    mc "(A door that is usually open is closed. A clock that is usually right is two minutes slow. Small things. The kind of things you only notice when you have been away.)"

    "The professor's office. The same door at the end of the hall. The same small window beside it."
    "Through the glass I can see the desk, the chair, the wall of books. No note on the door. No tea on the desk. But it is early for tea."
    "Then I see the handle. It is different. Newer. It has been replaced."
    mc "(A new handle. On a door that has not changed in months. Small things.)"

    scene bg_lecture_hall with walk_fade

    "Murakami is at the front of the room. She writes a single line on the board and turns around."
    murakami "Write down one thing you noticed on the way here. Not a person. A thing. The kind of thing you walk past every day and never see."
    mc "(I write: the door handle. New. Shiny. Wrong.)"
    murakami "Good. That is the lesson. The city is not what you remember. It is what you notice."
    mc "(I noticed a handle. I did not notice anything else. That is either the lesson or the problem.)"

    scene bg_campus_interior with walk_fade

    "The lesson ends and nobody moves for a moment. Then the class remembers it has a body, and the chairs scrape, and the bags come out."
    "A notice is on the board. Souji. Cleaning duty. The class splits into groups."
    "Murakami reads the names from a sheet. She does not look up when she reads mine."
    murakami "Group four. The second floor corridor. You and Hikari."
    mc "(She pairs us like it is nothing. It is nothing. It is a list.)"

    "I stop at her desk on the way out."
    mc "The handle on the professor's office door. It is new."
    murakami "Is it."
    mc "Someone replaced it."
    murakami "Someone replaces a great many things."
    mc "But nobody said."
    murakami "A door handle is not an announcement. It is a handle."
    "She turns back to her papers. The answer has the same shape as the others. Not a lie. Not a door either."
    mc "(She is not going to tell me. I do not know if that is because she cannot or because she thinks I should already know.)"

    scene bg_department_hall with walk_fade

    "The department office gives us a bucket, two cloths, and a bottle of cleaner with a yellow label."
    "The woman behind the counter does not look up from her ledger."
    "She tells us the second floor. The corridor. Windows and handles. No wet cloth on the wood."
    hikari "I have the window."
    mc "I have the doors."
    hikari "There are eleven doors."
    mc "There are eleven handles."
    hikari "You counted."
    mc "You did too."

    "The bucket is warm. The water smells like lemon and something under the lemon, something sharp."
    "I start at the far end, by the stairwell, and work back toward the office."
    "The cloth is thin. It goes grey after the third handle."
    "The handles are old. Brass, worn smooth in the middle where hands go."
    "They do not squeak. They have been opened so many times they have forgotten how to complain."

    hikari "The window is worse than the handles."
    mc "The window is glass."
    hikari "The glass is where the city gets in."
    "She sprays and wipes. The squeak of the cloth on the pane is the only sound in the corridor."
    "Outside, the courtyard is empty. A bicycle leans against the wall. The same bicycle that leaned there before the holiday."

    "Then the professor's door. The new handle is silver. The others are brass."
    "It is the wrong color. It is the wrong shape. It is polished in a way the others stopped being years ago."
    "I put the cloth on it. The cloth comes away clean. There is nothing on it to clean."
    mc "(It has not been touched enough to get dirty. Someone put it there and then did not use it.)"
    "I wipe it again anyway."

    hikari "You have done that one twice."
    mc "It was dirty."
    hikari "It was not."
    "She does not stop wiping her window. She says it the way she says the time."
    hikari "You keep cleaning the same handle."
    mc "It is the only one that is new."
    hikari "That is not why."
    mc "Then why?"
    hikari "Because if it is clean, it is just a handle."

    menu:
        "Scrub the new handle until it shines." :
            "I press the cloth into the silver and work at it."
            "My wrist starts to ache. The handle does not change. It was already shining."
            hikari "It is not going to look like the others."
            mc "I know."
            hikari "Then why are you still going?"
            mc "Because it should look like it belongs."
            "She thinks about that. She wipes the corner of her window twice."
            hikari "It does not have to belong. It only has to open."
            $ log_memory("hikari", "said the new handle does not have to belong, only to open")
            $ reward_attributes_once("day29_souji_shine", [("nerve", "micro")], show="auto")
        "Ask Hikari why someone would replace one handle." :
            mc "Why would someone replace one handle? Not the door. Not the lock. Just the handle."
            hikari "Maybe someone's hand slipped."
            mc "That is not a reason."
            hikari "It is the reason for most repairs. Something goes wrong once, and then it is fixed, and then it is ordinary."
            "She rings the cloth out over the bucket. The water runs grey."
            hikari "You are looking for a story. There is no story. There is a broken thing and a person with a screwdriver."
            mc "(She is telling me the truth. The truth is smaller than the story.)"
            $ log_memory("hikari", "said a repair is just a broken thing and a person with a screwdriver")
            $ reward_attributes_once("day29_souji_ask", [("insight", "micro")], show="auto")
        "Clean the window with her." :
            mc "Give me half."
            hikari "Half of what?"
            mc "The window."
            "She hands me a cloth. We work from opposite ends and meet in the middle."
            "The glass clears. The corridor comes back to us in it. The doors, the handles, the two of us standing still."
            hikari "Look. The corridor is in the window now."
            mc "It was always there."
            hikari "Not like this. Now you can see all of it at once."
            "I look. Eleven doors. Eleven handles. One of them silver."
            mc "(All of it at once. That is what she does. She makes the thing I am inside of into something I can see.)"
            $ log_memory("hikari", "cleaned the corridor window with him until the whole hall was visible")
            $ reward_attributes_once("day29_souji_window", [("grace", "micro")], show="auto")

    "We pour the water out in the slop sink. The bucket echoes against the ceramic."
    "Hikari folds her cloth into a square. I fold mine into a square. The corridor smells like lemon."
    "The new handle is still silver. It is still the wrong shape. It has been cleaned now, so it looks like it has always been there."
    mc "(That is what maintenance does. It makes the wrong thing ordinary.)"

    scene bg_campus_interior with walk_fade
    scene bg_school_gate with walk_fade
    scene bg_station with walk_fade
    scene bg_platform with walk_fade
    scene bg_train_interior with walk_fade

    "The train is full again. The sleeping man is back on the end seat, chin on chest."
    mc "(He is back. Everything is back. The rhythm is back, and it is off by a beat, and I am the only one who can hear it.)"

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    "We walk home. The streets are full again. The plum is on the windowsill. The same plum. The same windowsill."
    hikari "It is strange to be back."
    mc "It is."
    hikari "Nothing changed. That is what is strange."
    mc "Something changed. I cannot tell what."
    hikari "That is the strangest part. The thing that changed is the thing you cannot see."
    mc "(The thing that changed is the thing I cannot see. I do not know how to look for it.)"

    scene bg_kitchen_night with walk_fade
    "The kitchen is warm. Mother has dinner ready. Rice, soup, and pickles on the side."
    mother "Sit. Eat. You must be tired after the first day."
    father "Tired is for the first week. The first day is just strange."
    hikari "He says that every year."
    father "Then I am right. The first day is strange. The second day is tired. The third day is normal."
    mc "And after that?"
    father "After that you stop counting."
    mc "(After that you stop counting. Nobody has told me what comes after.)"
    "We eat. The new handle is somewhere in the building behind us, clean and ordinary."

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the window is open a crack. The city is doing its night sounds. All of them. The holiday is over."
    "My notebook is on the desk, closed. The corridor map is inside it. I have stopped adding doors."
    "The plum is on the windowsill. It is almost done."
    "The door handle at school was new. I keep thinking about it. A new handle on an old door. Someone changed it and did not say anything."
    $ night_desk_line = "a notebook and a plum on the windowsill"
    call night_open from _call_night_open_20

    menu:
        "[tag_grace] Rank 2: Ask who might have slipped." if has_attribute("grace", 2):
            mc "You said maybe someone's hand slipped. Who?"
            hikari "Somebody who did not want to be noticed."
            mc "Then the handle is how they got noticed anyway."
            $ reward_attributes_once("day29_night_slipped", [("grace", "micro")], show="auto")
        "Ask Hikari about the door handle." :
            mc "The door handle at school was new."
            hikari "New?"
            mc "New. Shiny. Not the old one."
            hikari "Someone replaced it. That is all."
            mc "Nobody said anything."
            hikari "Nobody says anything about door handles. That is why they get replaced."
            mc "(Nobody says anything about door handles. So the handle says it for them.)"
            $ log_memory("hikari", "said nobody says anything about door handles, that is why they get replaced")
            $ reward_attributes_once("day29_night_handle", [("insight", "micro")], show="auto")
        "Ask about the rhythm." :
            mc "Something felt off today. I cannot tell what."
            hikari "The rhythm is back. It is just not your rhythm yet."
            mc "It was my rhythm before."
            hikari "Before. The holiday changed it. You will get it back by Friday."
            mc "(I will get it back by Friday. I do not know if I want it back.)"
            $ log_memory("hikari", "said the rhythm is back but not mine yet")
            $ reward_attributes_once("day29_night_rhythm", [("grace", "micro")], show="auto")
        "Watch the window. Say nothing." :
            "I do not say anything. The city is doing all its night sounds. The holiday is over."
            "Hikari watches me. She does not fill the silence."
            mc "(The rhythm is back. It is off by a beat. I am the only one who can hear it.)"
            $ log_memory("hikari", "watched the window in silence on the first night back")
            $ reward_attributes_once("day29_night_quiet", [("nerve", "micro")], show="auto")

    call night_close from _call_night_close_20

    "The rhythm is back. Off by a beat. Nobody else seems to hear it."
    "I turn off the lamp. The room is dark. It is not empty."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5

    jump act2_day_router