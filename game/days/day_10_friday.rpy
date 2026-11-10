################################################################################
## DAY 10 — FRIDAY, APRIL 17, 2026
## The elective fair: Murakami, the kana, and the country you walk into.
################################################################################

label friday_morning:
    $ set_story_day(10)
    call day_transition

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Friday. The week has a shape now: wake, eat, train, listen, come home, sleep."
    "The shape is not a cage yet. It is a rhythm. I am still deciding which one it is."
    "My phone buzzes against the desk."

    if "aya" in wire_unlocked:
        $ run_chat("aya", [
            {"them": "Good morning, Master! ☆", "options": [
                {"label": "\"Good morning, Aya.\"",
                 "send": "Good morning, Aya.",
                 "them": ["You remembered my name!", "Most people just say 'miss'."]},
                {"label": "\"It's seven in the morning.\"",
                 "send": "It's seven in the morning.",
                 "them": ["The cafe opens at ten.", "I am practicing being cheerful early."]},
            ]},
            {"them": "Come by after class. I saved you the window seat. ☆"},
        ])
        mc "(She texts in sparkles. I do not know how to text back in sparkles. I will learn.)"
    else:
        $ run_chat("hikari", [
            {"them": "Don't go down yet.", "options": [
                {"label": "\"Why?\"",
                 "send": "Why?",
                 "them": ["Because I have something to show you.", "Wait."]},
                {"label": "\"I'm hungry.\"",
                 "send": "I'm hungry.",
                 "them": ["Two minutes.", "The rice will survive."]},
            ]},
        ])
        mc "(Two minutes. In this house, that means she is already on the stairs.)"

    "The door slides open. Hikari is holding a folded sheet of paper like it is a passport."
    hikari "Electives."
    mc "Electives?"
    hikari "The fair is today. After lunch. Every department puts out a table and pretends it is not recruiting."
    "She hands me the paper. It is a list of courses, printed in two columns, with a map of the hall on the back."
    hikari "You have to pick one. It is not optional. The department classes are fixed; the rest is yours."
    mc "What did you pick?"
    hikari "Something boring. Something useful. Something I will complain about."
    mc "That is three things."
    hikari "It is one thing. It is called being a student."
    "She sits on the edge of my desk, which she has never done before."
    hikari "Look at the Japanese course. The one at the bottom."
    mc "Japanese."
    hikari "It is taught by a man named Murakami. Nobody knows where he came from. He has been here longer than the building."
    mc "That is not a real answer."
    hikari "It is the only answer anyone has."
    "She taps the paper once and stands up."
    hikari "Come down. You can read it over breakfast. Mom will want to know what you chose before you have chosen it."

    scene bg_kitchen with walk_fade

    "The kitchen is bright with Friday. Mother has set rice, miso, and a plate of pickles that nobody asked for."
    mother "Sit. Both of you. The rice is ready."
    father "Electives."
    mc "You know about the fair?"
    father "I know about the fair. I went to this university."
    mc "(That is the first time he has mentioned it. I do not know what to do with the information, so I eat.)"
    father "Choose something that changes how you see. Not something that looks good on a form."
    mother "He means choose the Japanese course."
    father "I did not say that."
    mother "You did not have to."
    hikari "He's been saying it for a week."

    mother "Do you know the honorifics yet?"
    mc "Some. -san. -sama."
    mother "That is the easy half."
    mother "-san is the default. Safe. Polite. You can use it with almost anyone."
    mother "-kun is for boys, usually by someone above them. -chan is for children, or for someone you are close to. Do not use -chan on a professor."
    father "-sama is for customers and for people you are serving. Do not use it on yourself."
    mc "And -senpai?"
    mother "-senpai is for the one ahead of you. -kouhai is for the one behind. The school runs on those two words."
    father "There is also keigo. The polite language. You will hear it in shops and on the phone."
    father "And there is honne and tatemae. The feeling and the face."
    mc "The feeling and the face."
    father "What you mean and what you show. Everyone has both. The trick is knowing which one you are being given."
    mc "(That is either the most useful thing he has said or the most unsettling. I suspect it is both.)"

    menu:
        "Ask which one I am being given right now.":
            mc "Which one am I being given right now?"
            father "Tatemae."
            mc "And honne?"
            father "You are early again. That is good."
            mc "(He says it to the newspaper. It lands anyway.)"
            $ reward_attributes_once("day10_kitchen_honne", [("insight", "micro")], show="auto")
        "Practice -san on everyone at the table.":
            mc "Thank you, Miharu-san. Tetsuo-san. Hikari-san."
            hikari "Don't."
            mc "Hikari-san."
            hikari "I will leave this house."
            mother "It is correct, though."
            hikari "It is correct and I hate it."
            $ reward_attributes_once("day10_kitchen_honorifics", [("grace", "micro")], show="auto")
        "Ask what happens if I use the wrong one.":
            mc "What happens if I use the wrong one?"
            father "Nothing. They will smile. And then they will remember."
            mc "(That is the second time this house has told me that the worst thing is not being corrected.)"
            $ reward_attributes_once("day10_kitchen_wrong", [("nerve", "micro")], show="auto")

    hikari "We should go. The fair starts at one and the good tables fill up."
    mother "Take an umbrella. It is meant to rain this afternoon."
    mc "It is not raining."
    mother "Take the umbrella."
    hikari "Take the umbrella."
    mc "(Two people in this house have told me to take an umbrella. I take the umbrella.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0
    "The morning is heavier than yesterday. The sky is the color of a held breath."
    "Hikari walks beside me, the paper folded in her pocket, and does not say anything for a whole block."
    hikari "You're going to take it, aren't you."
    mc "The Japanese course?"
    hikari "You've been taking it since the airport. You just didn't have a name for it."
    mc "(She is not wrong. I do not tell her that either.)"

    scene bg_station with walk_fade
    "The station is louder on Fridays. People are already spending the weekend in their heads."
    "The train comes in full. We get on anyway."

    scene bg_train_interior with walk_fade
    "A wall of shoulders. A forest of straps. Everyone facing the same direction, like a photograph of a crowd."
    "A student beside me is asleep against the door, his bag between his feet, his face perfectly unguarded."
    "An announcement asks us to refrain from phone calls. Nobody was making one."
    "The English announcement comes after the Japanese, slower, as if it is reading from a different script."
    hikari "You're doing the thing again."
    mc "I'm always doing the thing."
    hikari "At least you know now."

    menu:
        "Ask about honne and tatemae on the train.":
            mc "Everyone looks so... blank. Is this tatemae?"
            hikari "This is the train. It is not a face. It is a rest."
            hikari "Nobody has the energy to have a feeling at seven-forty in the morning."
            mc "(That is the most comforting thing anyone has said about this city.)"
            $ reward_attributes_once("day10_train_tatemae", [("insight", "micro")], show="auto")
        "Move so the sleeping student's bag doesn't fall.":
            "The train turns. The student's bag tips. I catch the strap with my foot and hold it until the car straightens."
            "He does not wake up. The woman beside me sees me do it and nods once."
            mc "(A nod is a whole conversation here. I am learning to have them.)"
            $ reward_attributes_once("day10_train_bag", [("grace", "micro")], show="auto")
        "Try to read the station names before the English announcement.":
            "I read the characters on the map above the door. I get two of the nine."
            "At the third, I recognize the shape before the announcement says it."
            mc "(Two out of nine. Yesterday it was one.)"
            $ reward_attributes_once("day10_train_names", [("nerve", "micro")], show="auto")

    scene black with Fade(1.0, 0.3, 0.0)
    stop music fadeout 1.0
    "We come up near campus into a sky that has decided to rain but has not committed to it."

    scene bg_school_gate with Fade(0.0, 0.0, 1.5)
    play music "audio/Music/school.mp3" fadein 1.5
    $ phone_map_visit("school")
    "The guard nods. Hikari takes the stairs two at a time and is gone."
    "The morning is lectures. At one, the second floor turns into a market."

    scene bg_department_hall with walk_fade
    "The second floor has been turned into a market. Tables along both walls, banners on the pillars, students handing out paper."
    "Every table is selling the same thing: a version of the future."
    "At the end of the hall, one table has no banner. A stack of books, a single chair, and a man in a grey cardigan."
    "He is not handing out paper. He is reading."

    scene bg_department_hall with walk_fade
    "I walk toward him because there is nothing else at the table to walk toward."
    murakami "You are the one who reads on the train."
    mc "...How do you know that?"
    murakami "You have the look. The book is in your bag and your eyes are still in it."
    "He closes his book. The cover is plain. The title is in a script I cannot read yet."
    murakami "Murakami. The Japanese course. You have read the paper."
    mc "I have read the paper."
    murakami "Then you know it is an elective. You know it is not required. You know it will not make you rich."
    mc "The paper did not say that last part."
    murakami "The paper is optimistic."
    "He says it without smiling. Then he does smile, briefly, as if he has decided I can be trusted with the joke."
    murakami "The language is not a subject. It is a country you walk into. I can show you the road, but you have to walk."
    mc "And if I get lost?"
    murakami "Then you will be lost in a country. That is better than being lost in a corridor."
    "He slides a sheet across the table. It is not a form. It is a page of characters."
    murakami "Before you choose, look at this."

    "The page has three columns. On the left, Chinese characters. In the middle, characters that look like them but looser. On the right, curves."
    murakami "Kanji. The characters we borrowed from China. Serious. Official. The language of documents."
    murakami "Manyōgana. The first attempt to write Japanese with Chinese sounds. Clumsy. Beautiful. A compromise."
    murakami "And then these. Hiragana. Katakana. The curves."
    mc "They look like handwriting."
    murakami "They are handwriting. They were invented by women, in the Heian court, because the men had claimed the serious language."
    murakami "The novel was written in them. The pillow book was written in them. The private, the emotional, the true."
    murakami "In Japanese, the word for hiragana was onnade. Women's hand."
    mc "(A whole literature, born in the script the men decided was not serious.)"
    murakami "This is the first thing I will teach you. The language has a class system inside it. The scripts remember who was allowed to write what."
    murakami "When you learn to read all three, you are not learning a code. You are learning a history of who got to speak."

    menu:
        "Take the course. The Japanese course. With Murakami.":
            mc "Then I will take the Japanese course. With you."
            murakami "Good."
            "He writes my name on the sheet in three scripts. The third one is hiragana. It looks like a small, careful drawing."
            murakami "This is your name in the women's hand. It suits you."
            mc "(I do not know what that means. I write it down anyway.)"
            $ japanese_fluency = min(5, japanese_fluency + 1)
            $ reward_attributes_once("day10_elective_yes", [("insight", "micro")], show="auto")
        "Ask why the serious language was the borrowed one.":
            mc "Why was the borrowed language the serious one?"
            murakami "Because seriousness is always borrowed. It is the accent of whoever held the power last."
            murakami "Japan borrowed China the way every country borrows a parent. Then it made something the parent could not have made."
            mc "(He says it like a fact about language. It lands like a fact about me.)"
            murakami "Take the course. You are already asking the right questions."
            $ japanese_fluency = min(5, japanese_fluency + 1)
            $ reward_attributes_once("day10_elective_ask", [("nerve", "micro")], show="auto")
        "Ask about his name. Murakami.":
            mc "Murakami. Like the novelist?"
            murakami "Like the novelist. Like the village. Like a dozen men in this city."
            murakami "A name is not a self. It is a coat. You will learn that too."
            mc "(He says it lightly. I file it away.)"
            murakami "Take the course. You can decide what to call me later."
            $ japanese_fluency = min(5, japanese_fluency + 1)
            $ reward_attributes_once("day10_elective_name", [("grace", "micro")], show="auto")

    "He writes a line on the back of the sheet and pushes it across the table."
    murakami "Homework. Before Monday. Copy this line ten times. Do not look up what it means."
    mc "Why not?"
    murakami "Because meaning is the last thing you learn. First you learn the shape. The hand remembers before the head does."
    "He goes back to his book. The fair goes on around him. Nobody else comes to the table."

    scene bg_campus_interior with walk_fade
    "Hikari is waiting by the stairs with two paper cups of tea."
    hikari "You took it."
    mc "How do you know?"
    hikari "You have the sheet. And you have that face."
    mc "What face?"
    hikari "The one you had at the airport. The one that says you have decided something and are pretending you haven't."
    "She hands me a cup."
    hikari "The afternoon is yours. I have seminar until five."
    mc "(One place. That is the rule I have given myself. One place, and then home.)"
    call free_afternoon

    scene bg_home_night with walk_fade
    $ room_ambient(True)
    "The house is warm the way it is when someone has been cooking for a while."
    "I leave my shoes by the door, turned around, and follow the smell to the kitchen."

    scene bg_kitchen_night with walk_fade
    "Mother is ladling something into four bowls. Father is setting the table with the careful imprecision of a man who has been told to help."
    mother "There you are. Wash your hands."
    hikari "You're late."
    mc "I'm not late. Dinner is early."
    hikari "Dinner is on time. You're late."
    "I wash my hands. The water is warm."
    mother "Where did you go?"

    if last_afternoon_place == "chef":
        mc "The ramen shop. The same stool. The same bowl."
        mc "(He remembered what I ordered. He did not make a thing of it. That was the whole welcome.)"
    elif last_afternoon_place == "aya":
        mc "The maid cafe. She remembered the order before I said it."
        mc "(For about four seconds she was not performing. I don't think she noticed she did it.)"
    elif last_afternoon_place == "hana":
        mc "The reading room. She was there. She stayed."
        mc "(We did not talk much. It was enough.)"
    elif last_afternoon_place == "orson":
        mc "Lupin's Den. The bar was empty enough to hear the ice."
        mc "(He taught me a phrase I am still turning over.)"
    elif last_afternoon_place == "sim":
        mc "The photography club. Sim made us photograph the same wall until it stopped being a wall."
    elif last_afternoon_place == "walk_hikari":
        mc "I walked home with Hikari. We took the long way."
        hikari "You took the long way. I followed."
        mc "That's not how I remember it."
        hikari "That's because you were busy being right."
    elif last_afternoon_place == "walk_alone":
        mc "Nowhere. I walked until the light changed, and then I walked home."
        father "Nowhere is a place. Just not a destination."
        mc "(That is either wisdom or a warning. I am not sure which.)"
    else:
        mc "Nowhere. I came straight home."
        mother "Good. Eat."
        mc "(She does not ask why. I am grateful for that.)"

    father "And the elective?"
    mc "Japanese. The course with Murakami."
    father "Murakami."
    mc "You know him?"
    father "I know the name. He was here when I was here. He is still here."
    mc "What is he like?"
    father "Quiet. Dangerous."
    mc "Dangerous?"
    father "He makes people leave the country they were born in. Sometimes without moving."
    mc "(That is either a warning or the best endorsement I have ever heard.)"
    hikari "Dad."
    father "I am being helpful."
    mother "You are being ominous."
    father "It is the same thing, in this house."

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the sheet with the three scripts is on the desk."
    "I copy the line ten times. The first three are terrible. The fourth is less terrible. The tenth looks like a word."
    "A knock at the door. Hikari, with two cups of tea and her own notes under her arm."
    hikari "I'm not staying. I'm just making sure you're not staring at the wall."
    mc "I was copying the line."
    hikari "Same thing."
    "She sets the tea down and sits on the floor with her back against the bed."

    menu:
        "Show her the tenth line.":
            "I turn the sheet around. She looks at it for a long time."
            hikari "That's not bad."
            mc "It's terrible."
            hikari "It's not bad. The stroke order is wrong on the second character."
            "She takes the pen and writes it again, slower, so I can see the order."
            mc "(The hand remembers before the head does. Murakami was right.)"
            $ reward_attributes_once("day10_night_line", [("grace", "micro")], show="auto")
        "Ask her what onnade means to her.":
            mc "Murakami says hiragana used to be called onnade. Women's hand."
            hikari "It did. And then everyone used it, and the name stopped being true."
            mc "Does it bother you?"
            hikari "It bothers me that it took a name to make it serious. The writing was always the writing."
            mc "(She says it like a door closing.)"
            $ reward_attributes_once("day10_night_onnade", [("insight", "micro")], show="auto")
        "Tell her I'm nervous about the course.":
            mc "I'm nervous about the course. What if I'm bad at it?"
            hikari "You'll be bad at it."
            mc "That's not comforting."
            hikari "It's not meant to be. You'll be bad at it, and then you'll be less bad at it. That's the whole thing."
            $ reward_attributes_once("day10_night_nervous", [("nerve", "micro")], show="auto")

    "She takes her cup and leaves the door open a hand's width."
    "I listen to her go down the stairs, then the house settle into its night sounds."
    "The sheet is still open. The tea is still warm."
    "Tomorrow is Saturday. No train to school. A different kind of day."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump saturday_recovery
