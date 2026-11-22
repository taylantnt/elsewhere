################################################################################
## SPECIAL DAY 41: leak
## Monday, May 18, 2026. The first thing that cannot be explained away.
## A child who repeats. A shop that forgot to stay closed. A door in a wall
## that has no door, and a person who cannot see it.
################################################################################

label special_day_41_leak:
    $ set_story_day(41)
    call day_transition from _call_day_transition_22

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Monday. The sixth week ended without anyone announcing it, and the seventh has started the same way."
    "The bear is on the desk where she left him. The timer is beside him, still not running. The notebook is open to the corridor map."
    mc "(Fourteen doors. Two of them I could not place. Today I am going to place them.)"
    "I am up before the alarm. The pipe at six. The fridge at six fifteen. Hikari's door at six twenty."
    "Everything is where it was. That is the first thing I notice, and I notice it the way you notice a clock that is not ticking."

    "My phone buzzes."

    if "tanaka" in wire_unlocked:
        $ run_chat("tanaka", [
            {"them": "Monday. Delivery at seven. You are on the register.", "options": [
                {"label": "\"I thought I was on the floor.\"",
                 "send": "I thought I was on the floor.",
                 "them": ["You were on the floor.", "Then the schedule changed.", "Schedules do that."]},
                {"label": "\"I'll be there.\"",
                 "send": "I'll be there.",
                 "them": ["Good.", "Bring the pen. The one that works."]},
            ]},
        ])
        mc "(He says the schedule changed. I have not looked at the schedule since Thursday. I do not remember what it said.)"
    else:
        $ run_chat("hikari", [
            {"them": "You are awake. I can hear it through the wall.", "options": [
                {"label": "\"How can you hear that?\"",
                 "send": "How can you hear that?",
                 "them": ["You breathe differently when you are awake.", "It is not a talent."]},
                {"label": "\"Monday.\"",
                 "send": "Monday.",
                 "them": ["Monday.", "Do not make it a bigger word than it is."]},
            ]},
        ])

    "Three knocks. Hikari is already dressed and holding the bear by one ear."
    hikari "Monday."
    mc "You said that through the door."
    hikari "I said it through the wall. The door was not involved."
    "She sets the bear down on the desk, facing the window, and straightens his ribbon with two fingers."
    hikari "Do not move him. He is looking at the weather."
    mc "He is a bear."
    hikari "He is a bear who is looking at the weather."
    mc "(She has been like this since Shibuya. The bear is not a joke to her. I do not think it ever was.)"

    call murakami_daily_ping from _call_murakami_daily_ping_16

    scene bg_kitchen with walk_fade

    "The kitchen is warm and ordinary. Rice. Miso. The smell of the grill. Father has the newspaper folded into a square, which means he is reading the part he pretends not to care about."
    mother "Sit. You have been standing in the doorway for a week."
    mc "I have been standing in the doorway for one minute."
    mother "A week in doorway minutes."
    "I open the fridge for the milk. The carton is in the door, turned so the date faces out. Nineteen."
    mc "(The nineteenth. I checked it last Monday and it said the nineteenth then too.)"
    "I put it back. I take it out again. The date is still the nineteenth."
    mc "Mother. The milk."
    mother "It is good. I checked it."
    mc "When?"
    mother "This morning. Why?"
    mc "No reason."
    mc "(There is a reason. I do not have it yet.)"

    menu:
        "[tag_insight] Rank 2: Point out he answered a different question." if has_attribute("insight", 2):
            mc "You answered fresh milk. I asked about the date."
            father "You asked why the date was the same. Those are the same question."
            mc "Only if a week can be the same length twice."
            $ reward_attributes_once("day41_kitchen_answered", [("insight", "micro")], show="auto")
        "Tell Father about the date on the milk.":
            mc "The milk has the same date it had last week."
            father "Then it is fresh milk and a slow week."
            mc "That is not how dates work."
            father "Nothing is how it works until it is. Eat your rice."
            $ reward_attributes_once("day41_kitchen_milk", [("insight", "micro")], show="auto")
        "Ask Hikari about the shop on the corner.":
            hikari "The shop on the corner. The one with the paper over the glass."
            mc "What about it?"
            hikari "It was closed."
            mc "It has been closed since Wednesday."
            hikari "Then it is still closed. Why?"
            mc "No reason."
            mc "(She tells me the shop is closed. It is. That is the whole problem with it.)"
            $ reward_attributes_once("day41_kitchen_shop", [("grace", "micro")], show="auto")
        "Say nothing. Finish the rice.":
            "I eat. The rice is rice. The miso is miso. The morning does what a morning does."
            mc "(If I say it out loud, it becomes a thing that happened. If I do not, it stays a thing I noticed.)"
            $ reward_attributes_once("day41_kitchen_quiet", [("nerve", "micro")], show="auto")

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The street is dry. The gutters are empty. The sky says it rained all weekend and the street says it did not. The air has the flat clean smell of a room that has been wiped down."
    "The shop on the corner is open."
    "The paper is gone from the glass. The sign that said closed until the end of the month is gone from the door. The man who owns it is sweeping the step, and the shelves behind him are full, and there is no dust on anything."
    mc "(It was closed on Saturday. It was closed yesterday. I walked past it twice.)"
    "He nods at me. I nod back. His broom does the same small thing it has always done."
    hikari "You are walking slowly."
    mc "I am looking at the shop."
    hikari "It is a shop."
    mc "It was closed."
    hikari "Then it opened. That is what shops do."
    mc "(She says it easily. It is an easy thing to say. I keep walking.)"

    scene bg_station with walk_fade
    scene bg_platform with walk_fade

    "The platform is the platform. The yellow line. The queue that is not a queue. The sign that says one minute, which is honest."
    "A child in a yellow hat runs along the yellow line, laughing."
    "The station attendant does not look up from his phone."
    "She runs past again. Same direction. Same laugh. The attendant turns a page with his thumb."
    mc "(The child from Asakusa. The one who ran past twice in the same minute. I told myself I had imagined it. I told myself that for a month.)"
    "I turn around. There is one child. She is standing still now, holding a woman's hand, waiting for the train. The yellow hat is slightly too big for her."
    "She does not look at me."
    "The train comes."

    scene bg_train_interior_day with walk_fade

    "The car is full. Hikari takes the strap by the door. I stand beside her with my bag against my knee."
    "The child is sitting across from us, swinging her feet. The yellow hat. The woman beside her is reading."
    "She laughs at something out the window. It is the same laugh. Not a laugh like it. The same one."
    mc "(I am not going to look at Hikari. If I look at Hikari, she will ask me what I am looking at, and I will have to say a child.)"
    "I look at the window instead. The city goes by in the glass, backwards and clean."
    "When I look back, the seat is empty. The woman is still there. She has not moved. She turns a page."
    mc "(She was there. The seat was still warm. I did not need to touch it to know.)"

    scene bg_school_gate with Fade(0.0, 0.0, 1.5)
    play music "audio/Music/school.mp3" fadein 1.5
    $ phone_map_visit("school")

    "The gate is the gate. The guard is in his box with the paper. Students go in twos and threes."
    "A child in a yellow hat runs past the gate and up the path, laughing."
    "The guard does not look up."
    "Hikari is ahead of me, reading something on her phone."
    "The path is empty. A bicycle. A sign about a lost cat."
    hikari "You are standing at the gate."
    mc "I am coming."
    hikari "You were looking at the path."
    mc "I was looking at the sign."
    hikari "You have a face."
    mc "What face?"
    hikari "The one you get when you have seen something and are deciding whether to say it."
    mc "I am deciding."
    hikari "Then decide on the way. We are late."

    scene bg_campus_interior with walk_fade
    scene bg_department_hall with walk_fade

    "The department corridor is long and brown and smells of paper. The second floor. The same squeak in the third tile."
    "On the twenty-ninth Hikari and I counted the doors in this corridor. Eleven. We cleaned eleven handles."
    "There are twelve now."
    "The twelfth is between the fire extinguisher and the notice board. It does not belong there. The wall does not have room for it, and it is there anyway."
    "The handle is silver. New. The same silver as the handle on the professor's door at the end of the hall, the one that was replaced while we were away."
    mc "(I did not draw this one on the map. I would have remembered drawing it.)"

    "I put my hand on the handle. It is warm."
    mc "(A door in a corridor is not warm. A handle in a corridor is not warm unless someone has been holding it.)"
    "I turn it. It does not turn. The door is locked."
    "I knock. Twice. The sound goes into the wall and stops there, the way a sound does in a room with curtains."
    "Hikari is at the far end, looking at her phone."

    mc "Hikari."
    hikari "Mm."
    mc "Come here."
    "She comes. She stands beside me and looks where I am looking."
    hikari "What?"
    mc "The door."
    hikari "Which door?"
    mc "This one. In the wall. Between the extinguisher and the board."
    "She looks at the wall. Her eyes move along it the way eyes move along a wall. They pass over the door and go to the notice board and come back and pass over it again."
    hikari "There is a notice board."
    mc "And a door."
    hikari "And a fire extinguisher."
    "I take her hand and put it on the handle. Her fingers close around it. She does not look surprised. She looks patient, the way she looks when I have said something in the wrong order."
    hikari "It is cold."
    mc "It is warm."
    hikari "It is a wall. Walls are cold."
    "She lets go. She wipes her palm on her skirt, once, the way you wipe off dust."
    hikari "We are going to be late."

    $ door_twelfth_seen = True
    $ remember("mc", "touched a warm handle on a twelfth door in the corridor; she put her hand on the same spot and felt a cold wall", "twelfth_door")
    call leak_audio from _call_leak_audio_7

    "For a moment the corridor is longer than it is. The far end has a window that is not there. Then it is the corridor again, and Hikari is walking away, and the handle under my hand is warm."

    "I do not tell her again. I do not know what I would be telling her. She put her hand on the same handle I am holding and felt a wall."

    scene bg_campus_interior with walk_fade
    scene bg_lecture_hall with walk_fade
    play music "audio/Music/classroom.mp3" fadein 1.0

    "The lecture hall is full. The professor's chair is empty. A substitute reads from a handout in a voice that does not believe the handout."
    "Nobody takes notes. Nobody asks a question. The room does what a room does when the person in front of it is only a voice."
    mc "(The door is two corridors away. I can feel it the way you feel a word you have not said yet.)"
    "The substitute says something about the season, and the season changes in the window, and the hour ends."
    hikari "You did not write anything."
    mc "I was listening."
    hikari "You were somewhere."
    mc "I was listening from somewhere."
    hikari "That is the most honest thing you have said today."

    $ flush_pending_messages()

    scene bg_campus_interior with walk_fade
    scene bg_department_hall with walk_fade

    "After the lecture I go back to the corridor. I tell myself I am going back for the notice board."
    "The wall is a wall. The fire extinguisher. The notice board. The third tile that squeaks."
    "There is no twelfth door."
    mc "(I stand there long enough for a teacher to pass and not ask me what I am doing. Then I go home.)"

    scene bg_home_exterior_night with walk_fade
    $ night_street()

    "The walk home is the walk home. The crossing. The shrine. The vending machine that hums a note lower than the others."
    "The shop on the corner is closed. The paper is back over the glass. The sign is back on the door. Closed until the end of the month."
    mc "(This morning it was open. This morning the man was sweeping. This morning the shelves were full.)"
    "I stop and look at it. Hikari stops beside me and looks at me looking at it."
    hikari "You are doing it again."
    mc "Doing what?"
    hikari "Standing in front of a thing that is not doing anything."
    mc "It was open this morning."
    hikari "Then it closed. Shops do that too."
    "She takes my sleeve and pulls me on. I let her. The paper on the glass is the same paper. The tape at the corners has gone yellow the way tape does, which takes longer than a day."

    call dinner_open from _call_dinner_open_17

    mother "You are quiet."
    mc "I am tired."
    father "Tired is a thing you say when you do not want to say the other thing."
    mc "There is no other thing."
    father "Then you are tired."
    hikari "He stood in the corridor for a long time."
    mc "Hikari."
    hikari "He put his hand on the wall."
    mother "Which wall?"
    hikari "A wall."
    "Mother looks at me. Father looks at his rice. Nobody asks a second question."
    mc "(They are not avoiding it. They have decided it is one of the things that does not need a second question. I do not know when we all decided that.)"

    call dinner_close from _call_dinner_close_18

    scene bg_room_night with stair_fade
    $ room_ambient(True)

    "Upstairs, the bear is facing the window. The timer is beside him. The notebook is open to the map."
    "I sit down and uncap the pen."
    "I write: Monday. The child in the yellow hat was on the platform, on the train, and at the gate. Nobody else saw her."
    "I write: The shop on the corner was open this morning and closed tonight. The paper on the glass is old."
    "I write: A door in the department corridor. Between the extinguisher and the board. Locked. The handle was warm."
    "I write: She put her hand on it. She felt a wall."

    $ night_desk_line = "the map and four new lines"
    call night_open from _call_night_open_22

    menu:
        "Tell her about the door.":
            mc "In the corridor. The door I found. You put your hand on the handle."
            hikari "I put my hand on a wall."
            mc "It was a door."
            hikari "I believe that you saw a door."
            mc "That is not the same as believing there was one."
            hikari "No. It is not."
            "She says it without cruelty. She says it the way she says the time."
            mc "(She has never done this before. She has always seen what I saw, or seen something better. Tonight she sees a wall and I see a door, and we are standing in the same place.)"
            $ log_memory("hikari", "put her hand on the door in the corridor and felt only a cold wall")
            $ reward_attributes_once("day41_leak_night_tell", [("insight", "micro")], show="auto")
        "[tag_grace] Rank 2: Ask what she felt without telling her what you saw." if has_attribute("grace", 2):
            mc "When you touched it. What did it feel like?"
            hikari "Cold. Flat. A wall."
            mc "All right. I didn't want to put a word in your mouth."
            "She uncurls the fingers she'd been holding against her knee."
            hikari "Thank you. I was trying to work out what you wanted me to say."
            $ log_memory("hikari", "said she would not pretend to see the door because he would know")
            $ reward_attributes_once("day41_leak_night_ask", [("grace", "micro")], show="auto")
        "Say nothing. Put the notebook under the bear.":
            "I close the notebook and slide it under the bear's paw, the way I slid the fourth card under the bowl."
            "Hikari watches me do it and does not ask."
            "The room is quiet. The city does its night sounds. A train. A scooter. A door."
            $ log_memory("hikari", "watched him put the notebook under the lucky bear and said nothing")
            $ reward_attributes_once("day41_leak_night_quiet", [("nerve", "micro")], show="auto")

    call night_close from _call_night_close_22

    "She goes to her room. The door clicks. The house settles into its six sounds."
    "I take the notebook and open it to the page I wrote."

    "The first line is the same. The second line is the same. The third line is the same."
    "The fourth line is not."

    "It says: I put my hand on it. I felt a wall."

    mc "(I wrote: she put her hand on it. I remember the word. I remember the shape of the capital S.)"
    mc "(The page says I.)"
    "The handwriting is mine. The pen is the pen I used. The ink is still wet on the last word."
    "I do not cross it out. I do not write it again. I close the notebook and put it under the bear and turn off the lamp."
    $ remember("mc", "the notebook rewrote his own line overnight: she became I, the ink still wet", "notebook_self_edit")
    mc "(If I write it again, it will be a different sentence tomorrow. I would rather not know which one.)"

    "The room is dark. The bear is facing the window. The timer is not running."
    "The pipe ticks. The fridge hums. Somewhere in the house, a door I have counted opens and closes."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
