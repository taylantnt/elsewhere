define nami = Character("Nami", callback=type_sound)
define marco = Character("Marco", callback=type_sound)
define rika = Character("Rika", callback=type_sound)
define riku = Character("Riku", callback=type_sound)

label confidant_visit_sim:
    $ visit = confidant_visits.get("sim", 0)
    if visit == 0:
        # The Day 2 photo-club route is the usual first meeting. A player who
        # walked home instead never climbed to the second floor, so the hub's
        # zero-visit rule lets Circle introduce itself on a later Thursday.
        jump sim_visit_01
    elif visit == 1:
        jump sim_visit_02
    elif visit == 2:
        jump sim_visit_03
    elif visit == 3:
        jump sim_visit_04
    elif visit == 4:
        jump sim_visit_05
    elif visit == 5:
        jump sim_visit_06
    elif visit == 6:
        jump sim_visit_07
    return

label sim_common_open:
    scene bg_photo_club with walk_fade
    stop music fadeout 1.2
    play music "audio/Music/circle.mp3" fadein 2.0
    $ phone_map_visit("photo_club")
    return

################################################################################
## VISIT 1 — THE DOOR WITH TAPE ON IT
################################################################################
##
## The alternate first meeting. The Day 2 photo-club route already contains the
## argument and the first frame, so this one only runs when that route was
## skipped. It does the same work in less time: the club, Sim, and the WIRE
## invitation.

label sim_visit_01:
    call sim_common_open

    "The corridor on the second floor is longer than it has any right to be."
    "At the end of it is a door with a strip of tape down one side. A sheet of printer paper, two words in marker, and a circle drawn under them by hand."
    mc "(Circle. That is either the name of the club or a warning about the door.)"
    "I knock. Nobody answers. I open it anyway, because the door is already open."

    "The room smells of fixative and warm electronics and too much coffee. Four people are arguing in front of a whiteboard."
    sim "— it is not lazy. It is just not thinking about the picture."
    marco "It is a machine making the decision for you. That is the definition of lazy."
    sim "It is a machine making a decision you would have made anyway, only faster. That is the definition of a tool."
    nami "You two have had this argument every week since March."
    sim "And every week I win."
    marco "You do not win. You just talk longer."

    "The man in the middle of it turns around. He is older than the students, with the kind of calm that comes from having been the youngest person in a room for a long time."
    sim "Ah. A guest. Or a member. It is hard to tell the difference before the first photograph."
    mc "I was in the corridor. The door was open."
    sim "The door is always open. That is the whole membership policy."
    "He holds out a hand. His grip is dry and certain."
    sim "Sim. I run Circle. Which is a grand way of saying I bring the coffee and lose the arguments."
    marco "You do not lose the arguments."
    sim "Not when I am right."
    "He picks up a camera from the table and holds it out to me."
    sim "Here. Before we talk about anything, take one photograph of this room."
    mc "I don't know how to use this."
    sim "That is the correct answer. Nobody knows how to use it the first time. The people who think they do are the ones who take the boring photographs."

    menu:
        "Ask what I should look for.":
            mc "What should I look for?"
            sim "Something in this room that would be gone if you blinked. Not the people. The people will pose. Something else."
            mc "(I look. The light on the whiteboard. The tape on the door. The way the coffee cups are all on the same side of the table.)"
            sim "There. You found it. Now press the button."
            $ reward_attributes_once("sim_visit_01_look", [("insight", "micro")], show="auto")
        "Take the photograph without asking.":
            "I lift the camera and press the button before I can think about it."
            "The shutter makes a sound like a small, polite cough."
            sim "Good. The first one is always the honest one. After that you start trying to be good."
            $ reward_attributes_once("sim_visit_01_shoot", [("nerve", "micro")], show="auto")
        "Ask why he runs a club nobody joins.":
            mc "Why do you run a club that's this hard to find?"
            sim "Because the people who find it are the ones who were looking. The rest would have left after one meeting anyway."
            sim "A club is not a room. It is the people who keep coming back to it."
            $ reward_attributes_once("sim_visit_01_why", [("grace", "micro")], show="auto")

    "He takes the camera back, looks at the screen, and makes a sound that is not quite a laugh."
    sim "You photographed the thing nobody else would have chosen."
    mc "It was the most honest thing in the room."
    sim "That is either a very good answer or a very lucky one. I will take it."
    "He opens the group invitation on his phone and hands it to me."
    mc "I can't see the posts yet."
    sim "Not without a signal. They will be there when you get connected."
    "I type my name. WIRE saves the invitation."
    $ wire_unlock("sim")

    sim "We meet Thursdays. Bring the camera, or don't. The wall doesn't care."
    mc "The wall?"
    sim "You will meet it. It is the most photographed wall in this building, and it has never once complained."
    $ sim_affection += 1
    $ confidant_visits["sim"] = max(confidant_visits.get("sim", 0), 1)
    $ remember("sim", "found Circle at the end of the second-floor corridor and photographed the tape on the door")
    $ reward_attributes_once("sim_visit_01_close", [("grace", "micro")], show="card")

    scene bg_campus_interior with walk_fade
    stop music fadeout 2.0
    return


label sim_visit_02:
    call sim_common_open

    "The room smells of fixative, warm electronics, and too much coffee."
    "My name is already known here. Somebody has put it on the board beside Thursday, in a different hand."
    "Nami is not holding a reflector. She is holding a roll of gaffer tape and trying to make it obey her."

    sim "You made it. I checked the door twice in case I had imagined saying Tuesday."
    mc "I only checked once. I assumed the door would tell me if I was wrong."
    sim "The door would. This door is very honest."
    nami "That was a terrible pun, Sim."
    sim "I am saving the good ones for Thursday."

    sim "Camera first, introductions second. Nami, stop fighting the tape."
    nami "I am not fighting it. It is fighting the tripod."
    sim "Those are the same war from different sides."
    "Marco is at the table with a camera he clearly believes is more serious than his expression."
    marco "We have been arguing for ten minutes about whether autofocus is lazy."
    sim "It is not lazy. It is just not thinking about the picture."
    marco "Then what is it thinking about?"
    sim "Batteries. Probably."

    sim "You have a real camera now. Good."
    sim "Today we are not making art. We are learning to hear what the machine is saying."
    sim "Full automatic is useful when the moment is moving. Manual is useful when you need to make a decision before it disappears."
    sim "Neither is better. One just puts the decision somewhere else."

    menu:
        "I don't want the machine choosing for me.":
            mc "I don't want the machine choosing for me. I want to know why the photograph looks the way it does."
            sim "Then start with one decision at a time."
            $ reward_attributes_once("sim_visit_02_manual", [("insight", "micro")], show="auto")
        "I keep choosing automatic because it saves time.":
            mc "Automatic saves time when something is happening quickly. Manual is for when I want the photograph to belong to me."
            sim "Yes. Time and ownership are not always the same thing."
            $ reward_attributes_once("sim_visit_02_time", [("nerve", "micro")], show="auto")
        "What should I learn first?":
            mc "What should I learn first? Aperture, shutter speed, or focus?"
            sim "Whatever is currently disappointing you."
            sim "For most people, that is the thing they think they already understand."
            # Asking the person who knows, instead of guessing alone.
            $ reward_attributes_once("sim_visit_02_learn", [("grace", "micro")], show="auto")

    sim "Put it on manual. Aperture wide enough that the background disappears, shutter slow enough that the room is still paying attention."
    sim "Do not look at the settings yet. Look at the frame."
    "The nearest wall is stained at shoulder height in a way nobody has ever explained to me."
    sim "There. Make that stain the subject. Not the lamp. Not the posters. The stain."
    "I frame it badly, breathe out, and press the shutter."
    "The image comes back with the window behind it blown almost entirely white."

    mc "The window ate the photograph."
    nami "It ate only the easy part. The stain is still there."
    sim "Good. That means the decision was yours, even when the result was not."
    sim "Exposure is not a moral judgment. It is a relationship between the camera and the room."
    sim "Now let the window be bright. Make the stain dark enough that you have to look for it."
    "The second frame is quieter. The stain has become a bruise of brown against black, and the window is only a suggestion."
    sim "There. You just described the room by refusing to show all of it."
    $ sim_affection += 1

    "Sim turns the camera toward himself and makes the worst self-portrait I have ever seen."
    sim "This is my portrait for the month."
    marco "It is a very convincing photograph of a ceiling."
    nami "You held the camera upside down."
    sim "I know. It is my first deliberately bad photograph this month. I need to keep the average honest."
    sim "Some weeks I make something I like. Some weeks I make evidence that I was here."
    "He sets the camera on the table like a tool rather than a trophy."
    sim "Come back Thursday. We are going outside, and I promise the walls will not cooperate."

    $ confidant_visits["sim"] = max(confidant_visits.get("sim", 0), 2)
    $ remember("sim", "learned manual exposure by photographing the damaged wall")
    $ queue_message("sim", "The stain photograph is better than the window photograph. Please do not tell Nami I said that.", day="yesterday")
    $ reward_attributes_once("sim_visit_02_close", [("grace", "micro")], show="card")

    scene bg_campus_interior with walk_fade
    stop music fadeout 2.0
    return

label sim_visit_03:
    call sim_common_open

    "The circle is smaller than last week, and more purposeful."
    "A sheet of paper is taped beside the door: models wanted, one hour, all skill levels, payment in cake and honest criticism."
    "Rika is already there, draped over a chair as though the pose has chosen her."
    "When she sees me, she sits up with theatrical dignity."

    rika "Oh. The photographer who learned from the wall."
    mc "I prefer stain photographer. It sounds less accidental."
    rika "The stain has range."
    sim "Rika has offered to model. Marco is checking the light. Nami is pretending she is not excited about the cake."
    nami "I am very professional."
    marco "You brought two slices."
    nami "One is mine."

    sim "Tonight you shoot. Not observe. Not admire. Shoot."
    mc "What if I ruin it?"
    sim "Then we learn what the photograph was trying to tell you."
    rika "And if it is perfect?"
    sim "Then you learn how much luck was in it."
    "The room laughs. Sim does not join in loudly, but his mouth stays curved while he adjusts a light."
    "He has learned to let the room have its own weather."

    menu:
        "I can do this.":
            mc "I can do this. I may not be good yet, but I can make a decision and live with it."
            sim "Good. Decisions are the part nobody can do for you."
            $ reward_attributes_once("sim_visit_03_decide", [("nerve", "micro")], show="auto")
        "I need more time.":
            mc "I want to do it, but I need a little more time before the room watches."
            sim "Then we will give you a little more time. The model is patient, and so are we."
            $ reward_attributes_once("sim_visit_03_wait", [("grace", "micro")], show="auto")
        "Tell me exactly what to do.":
            mc "Tell me exactly what to do. I trust the process more than my own instincts right now."
            sim "I will give you the frame. You will decide when the breath happens."
            $ reward_attributes_once("sim_visit_03_frame", [("insight", "micro")], show="auto")

    "The first frame is technically correct and emotionally empty."
    "Rika's smile is perfect in the way a passport photograph is perfect."
    sim "Too controlled. She is performing the idea of a photograph instead of letting one happen."
    rika "I have been told I have a photogenic face."
    sim "You have a face. Let it be less photogenic for ten seconds."
    rika "Ten seconds? That is an insult and a challenge."
    "Sim moves the light without asking permission. The shadows soften across the side of her face."
    "I lower the camera."

    sim "Watch her hands. She is doing the thing where she tries very hard to be natural."
    mc "How can I tell the difference?"
    sim "The eyes. People can arrange their faces. They cannot always arrange where they look."
    "Rika notices us watching her, and something private crosses her expression before she catches it and smiles again."
    "I press the shutter at the wrong moment by every technical measure."
    "It is the right image."

    sim "There."
    rika "Wait. Let me see."
    "Rika takes the camera. She looks at the screen longer than necessary, then looks up with an expression I cannot politely name."
    rika "That one is not going on the practice wall."
    mc "I made it."
    rika "You did. Do not become difficult about it."
    "The room laughs, and I laugh with them."
    sim "Keep the file. Name it after what you were trying to learn, not what you hoped to get."

    "After the session, Sim stays behind to coil a cable."
    "For a while, neither of us says anything."
    sim "Ten years ago I made my first photograph I was proud of."
    mc "Where is it?"
    sim "In a drawer. It was rejected by four places. The fifth never replied."
    sim "I kept it because the rejection did not make the light less true."
    "He looks at the cable in his hands as though checking whether it is tangled."
    sim "You do not need anyone's permission to keep seeing."
    sim "But it helps when someone is in the room while you try."
    mc "I'm glad I'm in the room."
    sim "I know. That is why I keep making room."
    $ sim_affection += 1

    "Rika appears with the second slice of cake and puts it in front of Sim without comment."
    "He looks at it, then at her, and accepts it with both hands."
    sim "Next week we are going outside. Bring shoes you do not mind ruining."
    $ confidant_visits["sim"] = max(confidant_visits.get("sim", 0), 3)
    $ remember("sim", "captured Rika's unguarded expression and heard about his rejected first photograph")
    $ queue_message("sim", "The frame where Rika looked away from the camera is the one I would keep. Do not let Marco talk you out of it.", day="yesterday")
    $ reward_attributes_once("sim_visit_03_close", [("insight", "micro")], show="card")

    scene bg_campus_interior with walk_fade
    stop music fadeout 2.0
    return

label sim_visit_04:
    call sim_common_open

    "The room has changed without announcing it."
    "There are two tables now. Prints cover every wall, including some that appear to have been claimed by the wall itself."
    "Nami is running the light with the confidence of someone who has finally stopped asking whether she is allowed to."

    nami "White reflector. No, the other one. Sim said soft, but I think he meant 'stop making Rika look like a certificate photo.'"
    rika "That was specific and accurate."
    marco "We have eleven submissions for the hallway."
    sim "Nine. Two are duplicates with better titles."
    marco "Titles matter."
    sim "They matter after the photograph does."

    sim "You are late, which means you are exactly on time. The universe has a sense of humor."
    mc "I came straight from campus."
    sim "Then the universe is efficient."
    sim "Tonight we are not only making photographs. We are deciding what deserves to survive the semester."
    "The word survive makes the room quieter in a useful way."
    sim "Some prints will stay on the wall. Some will go home. Some will become evidence of a good afternoon."
    sim "That is not failure. That is how a room learns what it wants to keep."

    menu:
        "Let the group decide which prints stay.":
            mc "Let the group decide which prints stay. I want to see what people choose when they have to put something at risk."
            sim "Good. Criticism is easier when it belongs to everyone."
            $ reward_attributes_once("sim_visit_04_collective", [("grace", "micro")], show="auto")
        "I want to choose one of mine.":
            mc "I want to choose one of mine. I need to know whether I can trust my own eye."
            sim "Then choose. If you choose badly, we will all learn something expensive."
            $ reward_attributes_once("sim_visit_04_choice", [("insight", "micro")], show="auto")
        "Can we keep this simpler?":
            mc "Can we keep this simpler? I think the room is trying to become something before it knows what it is."
            sim "Perhaps. But rooms usually become things by pretending they already are."
            # Pushing back on the room's momentum takes a little nerve.
            $ reward_attributes_once("sim_visit_04_simple", [("nerve", "micro")], show="auto")

    "The wall becomes a battlefield of small opinions, conducted entirely in good faith."
    "Riku, who has been quiet until now, stands beside a print of the campus gate at dusk."
    riku "This one. I took it by accident. I was late and I did not look through the viewfinder."
    nami "It is the best one on the wall."
    riku "It is technically terrible."
    sim "It is technically human."
    "Riku laughs once, surprised to have been understood so quickly."
    sim "See? Even accidents have a point of view if you give them enough time."
    "He says it lightly, but the room receives it as though he has handed them a tool."

    sim "I have been thinking about something."
    "The room turns toward him. He does not enjoy the attention, so he looks at the prints instead."
    sim "There is a community exhibition at the end of the term. Small room, local artists, no fees."
    marco "A real one? With a program and everything?"
    sim "With labels and everything."
    nami "Are we actually doing this?"
    sim "I am asking whether we should."
    "He looks at the wall, then at the faces around the circle."
    sim "I have spent years making photographs that did not get shown. I know what it is like to prepare something for a room that never arrives."
    sim "This room arrives every Thursday."
    "Nobody speaks for a moment. The projector hums. Someone's phone lights up and goes dark again."

    menu:
        "That sounds terrifying and necessary.":
            mc "That sounds terrifying and necessary. We should do it."
            sim "Then we will make a terrible plan and improve it together."
            $ reward_attributes_once("sim_visit_04_commit", [("nerve", "micro")], show="auto")
        "What if nobody comes?":
            mc "What if nobody comes?"
            sim "Then the photographs still came here first."
            $ reward_attributes_once("sim_visit_04_fear", [("grace", "micro")], show="auto")
        "Who decides which photographs go?":
            mc "Who decides which photographs go?"
            sim "Everyone. That is the only way I know how to run anything that matters."
            # Asking how the group's process works, before joining it.
            $ reward_attributes_once("sim_visit_04_decides", [("insight", "micro")], show="auto")

    "Sim writes EXHIBITION on the board in letters large enough to make the room feel suddenly official."
    sim "Next week we bring three candidates each. We argue like adults, then we order snacks like students."
    "Riku offers to design the labels. Nami claims the lighting plan. Marco says he will make the posters and immediately begins explaining why Helvetica is a political choice."
    sim "You can help judge. Not because you are the newest, but because you still ask why."
    mc "That feels like a promotion."
    sim "It is. The pay is exposure and cake."
    "He smiles, then looks at the camera on the table."
    sim "Do not lose the file with Rika's unguarded frame. It may be useful to remember why we started arguing."
    $ sim_affection += 1

    $ confidant_visits["sim"] = max(confidant_visits.get("sim", 0), 4)
    $ remember("sim", "helped judge Circle's prints and agreed to make the community exhibition")
    $ queue_message("sim", "The exhibition is real enough to worry about now. Bring your three strongest candidates, and bring your worst one too.", day="yesterday")
    $ reward_attributes_once("sim_visit_04_close", [("nerve", "micro")], show="card")

    scene bg_campus_interior with walk_fade
    stop music fadeout 2.0
    return

label sim_visit_05:
    call sim_common_open

    "The room is almost empty."
    "One light stand is folded. The projector is dark. The prints have been taken down for cleaning, leaving pale rectangles on the walls."
    "Sim is sitting on the floor with a camera bag open beside him, sorting memory cards with the concentration of a person sorting something that might be alive."

    sim "You came. I was beginning to think the calendar had invented Thursday."
    mc "Is everyone else sick?"
    sim "Busy, mostly. Exams, part-time jobs, the ordinary business of being eighteen and trying to become something."
    sim "Nami sent a photograph of her cat sitting on the whiteboard. It is technically perfect and spiritually chaotic."
    "He holds it up. The cat has the expression of a creature that has read the minutes and disagreed with them."
    sim "Riku is in Osaka until Sunday. Marco is making posters at his cousin's print shop. Rika is asleep on the floor of the library."
    sim "It is just us and the rectangles."

    sim "I know what this room looks like when it is empty. I knew it before there was anyone to fill it."
    mc "Do you miss that?"
    sim "Sometimes. It is very quiet. You can hear the building decide what it wants to be when nobody is asking it to be anything."
    sim "I started Circle because I was tired of photographing streets and then taking the pictures home to a drawer."
    sim "Nobody rejected those photographs in a dramatic way. They simply had nowhere to go."
    "He places a memory card in the wrong slot and has to take it out again."
    sim "I made an announcement once. I told people I wanted to build a community. It sounded very noble."
    sim "The truth was smaller and less impressive. I was lonely, and I was bad at asking for company."
    sim "Photography gave me an excuse to stand near people without having to explain why I was standing near them."
    "The honesty sits in the room without asking for comfort."

    menu:
        "That sounds lonely, not noble.":
            mc "That sounds lonely, not noble. But it also sounds honest."
            sim "Honesty is usually less noble than loneliness."
            $ reward_attributes_once("sim_visit_05_honest", [("insight", "micro")], show="auto")
        "You don't have to make it sound better.":
            mc "You don't have to make it sound better. This room didn't happen by accident, but it also wasn't magic."
            sim "No. It was people returning on Thursdays because somebody kept the door open."
            $ reward_attributes_once("sim_visit_05_real", [("grace", "micro")], show="auto")
        "What made you keep going?":
            mc "What made you keep going after the first people didn't return?"
            sim "The second person. Then the third. Each one made the empty room less convincing."
            sim "You cannot argue with a person who keeps showing up."
            # Asking the question under the story, not the story itself.
            $ reward_attributes_once("sim_visit_05_keepgoing", [("nerve", "micro")], show="auto")

    "Sim takes a roll of tape from his pocket and begins repairing the corner of a print that has started to curl."
    sim "I used to name my folders someday. Someday-show, someday-portfolio, someday-enough."
    sim "Now I name them after the person who made me look again."
    "He writes riku-osaka-dusk on the label of a sleeve, then pauses before closing it."
    sim "There. Even a photograph taken by accident becomes less lonely when it has a name."
    sim "You are in a folder now, by the way."
    mc "That sounds ominous."
    sim "It is called mc-thursday. I did not make the name. The computer did."
    "He smiles, and for a second the room has the same quality as the first session: uncertain, but not cold."
    sim "The exhibition is still happening. That is the part I am glad you came to see."
    sim "Everyone else will arrive with opinions and snacks. I wanted you to see the room before it became a crowd again."
    sim "It is easier to remember why we are doing this when the walls are not shouting."
    $ sim_affection += 1

    sim "Take a photograph of the empty wall."
    "I hesitate, then raise my phone."
    "The image is mostly pale rectangles and one strip of window light. It is not beautiful in the way photographs are supposed to be."
    sim "Good. Now we know what the room looks like when it is honest."
    sim "Next week it will be loud again. Bring your best three and your worst one."
    sim "The worst one is important. It tells us what we are not yet."
    $ confidant_visits["sim"] = max(confidant_visits.get("sim", 0), 5)
    $ remember("sim", "heard why he built Circle and photographed the empty room")
    $ queue_message("sim", "The empty-room photograph is my favorite thing anyone has made this month. Do not let the club make you delete it.", day="yesterday")
    $ reward_attributes_once("sim_visit_05_close", [("grace", "micro")], show="card")

    scene bg_campus_interior with walk_fade
    stop music fadeout 2.0
    return

label sim_visit_06:
    call sim_common_open

    "The room is loud in the way of a place that has run out of pretending it is casual."
    "The selection wall is covered in sticky notes. Someone has labelled each photograph with a number, a title, and a small drawing of a face expressing an opinion."
    "Sim is standing at the center of it with his phone face-down on the table."

    sim "Before anyone asks: yes, the email is real. No, I have not slept properly since Tuesday."
    marco "You look fantastic."
    sim "That is because panic is excellent for circulation."
    rika "Say it slowly. What exactly did they say?"

    sim "A magazine wants to publish one of my photographs. Not a student magazine. Not a blog. A printed magazine with an editor who uses words like commission and deadline."
    nami "Which photograph?"
    sim "The one from the river at night. The one I almost deleted because the train was in it."
    riku "The train was the best part."
    sim "The train was an accident."
    riku "The accident is why it works."
    "Sim looks at him for a moment, then laughs once, genuinely surprised by the sentence."

    menu:
        "That is wonderful. You earned it.":
            mc "That is wonderful. You earned it, even if it arrived all at once."
            sim "I know. I am trying not to say that out loud and sound unbearable."
            $ reward_attributes_once("sim_visit_06_validate", [("grace", "micro")], show="auto")
        "What happens next?":
            mc "What happens next? Do they want more photographs?"
            sim "They want a conversation about what I might make next month. In another city."
            sim "It is not a promise yet. It is a door held open."
            $ reward_attributes_once("sim_visit_06_future", [("insight", "micro")], show="auto")
        "Are you scared?":
            mc "Are you scared?"
            sim "Constantly. But fear is just information wearing a bad coat."
            $ reward_attributes_once("sim_visit_06_fear", [("nerve", "micro")], show="auto")

    "The room goes quiet in the particular way of people who have understood that a joke would be too small."
    sim "I have spent ten years trying to be seen by people who did not know me."
    sim "Now someone wants to pay attention, and the first thing I feel is the urge to leave the room that finally made me worth seeing."
    nami "You are not leaving tonight."
    sim "No. I am not leaving tonight."
    rika "And after tonight?"
    sim "After tonight, I have to decide whether the photograph matters more than the room that taught me how to take it."
    "He looks around the circle, taking in the sticky notes, the cables, the half-empty cups, and the wall where every member has left something they are proud of."
    sim "I do not know yet. That is the honest answer."
    sim "But I know this: I will not turn the exhibition into a farewell until I have decided what I am actually saying goodbye to."
    "Marco writes something on a sticky note and puts it beside Sim's phone. It says: decide after cake."
    sim "That is either profound or the stupidest thing anyone has written all semester."
    marco "It is both."

    menu:
        "Make the exhibition for the room, not for the magazine.":
            mc "Make the exhibition for the room, not for the magazine. Let it be about us."
            sim "Yes. If I cannot do that, then I do not deserve the attention."
            $ reward_attributes_once("sim_visit_06_room", [("grace", "micro")], show="auto")
        "Tell them you need time.":
            mc "Tell them you need time. A real answer does not have to arrive before the exhibition."
            sim "I will. They can be patient. I have learned that from this room."
            $ reward_attributes_once("sim_visit_06_time", [("nerve", "micro")], show="auto")
        "What would you do if the magazine disappeared?":
            mc "What would you do if the magazine disappeared tomorrow?"
            sim "I would be frightened, then I would come back here and complain about the lighting."
            # Separating the work from the reward, by asking the hypothetical.
            $ reward_attributes_once("sim_visit_06_disappear", [("insight", "micro")], show="auto")
            sim "Some things are useful even when they do not change your life."

    "Sim picks up the phone, reads the email once more, and sets it down without answering."
    sim "The exhibition is still happening. That has not changed."
    sim "We will make it the best we can. After that, I will tell them what I have decided."
    sim "Not because I am brave. Because this room taught me that decisions are easier when other people are watching."
    "He looks at the selection wall, then at me."
    sim "You helped choose the prints. You helped make the room feel like it had a reason to exist."
    sim "Whatever I decide next, I want you to know that you were part of the reason I could imagine leaving."
    $ sim_affection += 1

    $ confidant_visits["sim"] = max(confidant_visits.get("sim", 0), 6)
    $ remember("sim", "received a magazine offer and promised to decide after the exhibition")
    $ queue_message("sim", "The editor can wait until after the exhibition. Cake cannot. Bring your worst photograph.", day="yesterday")
    $ reward_attributes_once("sim_visit_06_close", [("insight", "micro")], show="card")

    scene bg_campus_interior with walk_fade
    stop music fadeout 2.0
    return

label sim_visit_07:
    scene bg_photo_club with walk_fade
    stop music fadeout 1.0

    "The room has been transformed."
    "The prints are no longer held on with tape. They are mounted, labelled, and lit by a photographer who has borrowed equipment he cannot afford to replace."
    "People from outside Circle drift through in small groups, reading captions and arguing gently about whether a photograph is technically correct."
    "Sim is everywhere and nowhere, refilling a water jug, steadying a frame, laughing at a stranger's joke before the stranger has finished making it."

    sim "You came. Good. I was beginning to think the exhibition was a rumor circulated by optimistic printers."
    mc "It looks like a real gallery."
    sim "It is a school hallway with ambitions. That is the difference."
    "Rika is standing beside a portrait of herself that she claims she did not pose for. The photographer, a quiet second-year named Aya's cousin, has captioned it: consent pending."
    nami "That is the best caption in the show."
    marco "I designed the map. It has a legend."
    riku "The legend is a drawing of a confused pigeon."
    marco "The pigeon represents the visitor."

    sim "I have decided."
    "The room does not become silent immediately. That would be too theatrical. It becomes attentive, which is harder to resist."
    sim "The magazine offered me a commission. It is in another city, and it would mean leaving Circle."
    rika "Say it plainly."
    sim "Plainly: I am going to take it."
    "A murmur moves through the room, not angry, not surprised, but real."
    sim "I have spent ten years making photographs because I wanted to be seen. This is the first time someone has offered to pay me to keep looking."
    sim "I cannot say no to that and still call myself honest."
    nami "Does that mean Circle ends?"
    sim "Circle does not end. Circle changes. The room remains. The prints remain. The people remain."
    sim "I will not be here on Thursdays. That is the part I am asking you to understand."

    menu:
        "You have to go. This is your chance.":
            mc "You have to go. This is your chance, and pretending otherwise would be selfish."
            sim "I know. I know. That is the worst part."
            $ reward_attributes_once("sim_visit_07_accept", [("grace", "micro")], show="auto")
        "I wish you could stay.":
            mc "I wish you could stay. The room will be quieter without you."
            sim "It will. I know it will. I am asking you to forgive me for choosing the photograph anyway."
            $ reward_attributes_once("sim_visit_07_stay", [("nerve", "micro")], show="auto")
        "What will you carry with you?":
            mc "What will you carry with you?"
            sim "The proof that a room full of ordinary people can make something worth showing."
            $ reward_attributes_once("sim_visit_07_carry", [("insight", "micro")], show="auto")

    "Sim looks at the photographs one by one, as though memorizing their weight."
    sim "I used to think success meant leaving this place behind."
    sim "Now I think it means carrying the room with me in the way I see."
    sim "Every photograph I make next month will have a little of this hallway in it."
    sim "Every person in this room will be in the frame, even when they are not standing in it."
    "He turns to the group."
    sim "Thank you. Not because you are grateful to me, but because I finally understand what I built."
    sim "It was never just a photography club. It was a place where people could be seen before they were finished."
    rika "That is the most Sim thing you have ever said."
    sim "I am aware. I am leaving, so I am allowed one honest speech."

    "The room breaks into applause that is affectionate rather than ceremonial."
    "Sim lets it happen, then raises his hands to stop it."
    sim "One more thing."
    "He reaches into his camera bag and takes out the worn black strap he has used for years."
    "It is frayed at the edges, polished by sweat and time, and still perfectly functional."
    sim "This strap has been with me through every photograph I have ever taken."
    sim "I am not giving it away because I am done with it. I am giving it away because I want you to carry it."
    sim "When you take photographs in the city I am leaving, remember that someone once built a room for you to practice in."
    "He places it in my hand. The leather is warm from his pocket."
    sim "It is not a trophy. It is a reminder that you are allowed to keep seeing."

    menu:
        "I will use it. I promise.":
            mc "I will use it. I promise."
            sim "Good. That is all I ask."
            $ reward_attributes_once("sim_visit_07_promise", [("grace", "micro")], show="auto")
        "This means more than you know.":
            mc "This means more than you know. Thank you."
            sim "I know. That is why I chose you."
            $ reward_attributes_once("sim_visit_07_meaning", [("grace", "micro")], show="auto")
        "I hope we meet again.":
            mc "I hope we meet again."
            sim "Someday, we will walk with our cameras again. That is not a goodbye. It is a promise."
            $ reward_attributes_once("sim_visit_07_future", [("nerve", "micro")], show="auto")

    "Sim gathers everyone for a final photograph."
    "The room crowds close, elbows and shoulders and the soft rustle of jackets."
    "Sim stands in the center, camera raised, smiling wider than he has all evening."
    sim "Everyone look at the lens. Not at me. At the lens."
    "The shutter clicks."
    "The image is slightly imperfect, slightly overexposed, and completely alive."
    sim "There. That is the last photograph I will take in this room."
    sim "It is not the best one. It is the one I will remember."
    $ sim_affection += 1
    $ confidant_visits["sim"] = max(confidant_visits.get("sim", 0), 7)
    $ remember("sim", "left for a magazine commission and gave the protagonist his camera strap")
    $ queue_message("sim", "The exhibition was the best thing I have ever made. Thank you for being in the room. I will send photographs from the new city.", day="yesterday")
    $ reward_attributes_once("sim_visit_07_close", [("nerve", "micro")], show="card")

    "The exhibition lights dim."
    "The room empties slowly, reluctant to leave."
    "Sim stands beside the last photograph, the strap still warm in my hand."
    sim "Go home. Rest. Tomorrow the city will still be here, and so will the photographs."
    sim "I will be gone, but the seeing will not."
    scene bg_campus_interior with walk_fade
    stop music fadeout 3.0
    return
