################################################################################
## DAY 12 — SUNDAY, APRIL 19, 2026
## The old city: the gate, the incense, and the pause that is not empty.
################################################################################

label sunday_practice:
    $ set_story_day(12)
    call day_transition

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Sunday arrives the way Sundays do, late, and without apology."
    "The light on the ceiling is the color of the inside of a shell. The house is doing its slow morning."
    "A weekend of the elective. Twelve days of the house. Twelve days of being a person who knows which platform."
    mc "(I am not the same person who landed. I do not know when that happened. Probably on a train.)"

    "My phone buzzes once on the desk."

    if "orson" in wire_unlocked:
        $ run_chat("orson", [
            {"them": "The bar is open tonight. The water is still on the house.", "options": [
                {"label": "\"I might come by.\"",
                 "send": "I might come by.",
                 "them": ["Might is a door.", "Walk through it or don't."]},
                {"label": "\"What's the phrase you taught me?\"",
                 "send": "What's the phrase you taught me?",
                 "them": ["You remembered it. That is the first step.", "Say it to someone who needs it."]},
            ]},
        ])
        mc "(He texts like a man who has all the time in the world and is not going to waste any of it on punctuation.)"
    else:
        $ run_chat("hikari", [
            {"them": "Don't go down yet.", "options": [
                {"label": "\"Again?\"",
                 "send": "Again?",
                 "them": ["Again.", "I have a question for you."]},
                {"label": "\"I'm hungry.\"",
                 "send": "I'm hungry.",
                 "them": ["The question is more important than the rice.", "Almost."]},
            ]},
        ])
        mc "(She has a question. That means she has been thinking since before I woke up.)"

    if "murakami" in wire_unlocked:
        mc "(Murakami texted at eleven last night. One sentence. It is still on the screen: did you read the page.)"
        mc "(I read it four times. I say none of that. Sunday will say it for me.)"

    "The door slides open. Hikari is already dressed, holding two cups of tea."
    hikari "Almost two weeks."
    mc "Almost two weeks."
    hikari "How does it feel?"
    mc "Like a week."
    hikari "That's the right answer. The wrong answer is 'like a month'."
    "She hands me a cup and sits on the edge of the desk."
    hikari "You're different."
    mc "I'm the same."
    hikari "You're the same and you're different. It's annoying."
    mc "What's different?"
    hikari "You turn your shoes around. You make tea. You read on the train instead of staring at the map."
    hikari "You're becoming a person who lives here. It's very inconvenient for my theory that you're a guest."
    mc "(She says it to the cup, not to me. It lands anyway.)"
    $ add_affection("sister", 1)

    scene bg_kitchen with walk_fade

    "The kitchen is slow and warm. Mother has made a late breakfast: rice, miso, a small grilled fish, pickles."
    mother "Sunday breakfast is late. That is the rule."
    father "It is not a rule. It is a habit."
    mother "It is a rule now."
    "She sets a bowl in front of me. It has a chip on the rim."
    mc "This one is chipped."
    mother "That one is mine. You have the new one."
    mc "Why do you keep the chipped one?"
    mother "Because it is still a bowl."
    father "Mottainai."
    mc "(The word again. It is not about money. It is about the thing itself.)"
    hikari "She's been using that bowl since before I was born."
    mother "It has never once failed to hold rice."
    mc "(A chipped bowl that has never failed. There is a whole philosophy in that.)"

    menu:
        "Ask what mottainai means to her.":
            mc "Mottainai. What does it mean to you?"
            mother "It means a thing is not only for you. The bowl. The rice. The day."
            mother "You can throw a thing away. But you cannot un-throw it."
            mc "(She says it like a rule about the house. It is a rule about the world.)"
            $ reward_attributes_once("day12_kitchen_mottainai", [("insight", "micro")], show="auto")
        "Offer to take the chipped bowl.":
            mc "I'll take the chipped one. You have the new one."
            mother "You do not have to."
            mc "I know."
            "She looks at me for a long moment. Then she swaps the bowls."
            mother "There. Now you are a person who eats from the chipped bowl."
            mc "(I do not know why that feels like a promotion. It does.)"
            $ reward_attributes_once("day12_kitchen_bowl", [("grace", "micro")], show="auto")
        "Ask about ichigo ichie.":
            mc "Murakami said ichigo ichie. One time, one meeting. What does it mean at a table?"
            father "It means this breakfast will not happen again."
            mc "That's a heavy thing to say over rice."
            father "It is a light thing. It means pay attention."
            $ reward_attributes_once("day12_kitchen_ichigo", [("nerve", "micro")], show="auto")

    hikari "You're meeting her again today?"
    mc "Asakusa. She said the old city."
    hikari "The old city. Of course she did."
    mother "Take an umbrella."
    mc "It is not raining."
    mother "Take the umbrella."
    mc "(I take the umbrella. It is becoming a ritual. I think that is the point.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0
    "The Sunday street is empty in the way a stage is empty before a play."
    "I find the station with the clock. Murakami is standing under it with the same canvas bag."

    scene bg_station with walk_fade
    murakami "You came again."
    mc "You said Sunday."
    murakami "People say a lot of things. You came."
    "She turns and walks toward the platform. I follow. This time I do not need to be told."

    scene bg_platform with walk_fade
    "The Sunday platform is full of people who are not in a hurry. Families. Tourists. A woman in a kimono with a small bag."
    "A group of schoolchildren in matching hats is being counted by a teacher. The teacher counts them twice."
    murakami "On Sunday the train is a pilgrimage."
    mc "To where?"
    murakami "To whatever they have decided is worth the fare."
    "The train comes. We get on."

    scene bg_train_interior with walk_fade
    "The car is warm and loud. A child is telling her mother a story with no ending. The mother is listening as if it has one."
    "An old man in a suit sleeps with his head against the window. A young couple shares one pair of earphones."
    murakami "You are looking at them."
    mc "I'm learning the country."
    murakami "No. You are learning the people. The country is the easy part."
    "She takes out her notebook and writes something down. She does not show me."

    scene bg_asakusa_kaminarimon with Fade(0.0, 0.0, 1.5)
    "We come out of the station and the city changes."
    "A huge red lantern hangs in a gate. The street beyond it is a river of people and shops and smoke."
    "The air smells of incense and fried sweets and rain that has not happened."
    murakami "Kaminarimon. The gate of the thunder god. It has burned down and been rebuilt more times than anyone has counted."
    mc "So it's not the original."
    murakami "Nothing is the original. That is the first lesson of the old city."
    murakami "The gate is the gate because people keep walking through it."

    scene bg_asakusa_inside with walk_fade
    "Beyond the gate, the Nakamise street is a long line of shops selling fans and sweets and small wooden dolls."
    "A woman is turning a crank that makes a machine drop tiny cakes into a box. A child watches as if it is magic."
    "A child in a yellow hat runs past me, laughing. A moment later she runs past again, in the same direction, laughing the same laugh."
    "I turn. There is only one child."
    "At the end of the street, the temple stands with its roof curved up at the corners."
    murakami "Sensō-ji. The oldest temple in Tokyo. It is also a place where people buy souvenirs and eat ice cream."
    mc "Those two things don't go together."
    murakami "They go together perfectly. That is the country. The sacred and the snack stand."
    mc "(I do not know why that makes me feel better. It does.)"

    scene bg_asakusa_smoke with walk_fade
    "A large bronze burner stands in the courtyard. People wave the smoke toward themselves with both hands."
    murakami "The smoke is medicine. You pull it toward the part of you that needs it."
    mc "Does it work?"
    murakami "It works if you stand there long enough to believe it."
    "I wave the smoke toward my face. It smells of cedar and something older."
    mc "(I do not know if I believe it. I stand there anyway.)"

    scene bg_asakusa_kuji with walk_fade
    "At the side of the courtyard, a row of wooden racks is covered in small white papers tied in knots."
    murakami "Omikuji. Fortune slips. You pay, you shake the box, you take a slip."
    murakami "If it is good, you keep it. If it is bad, you tie it to the rack and leave it here."
    mc "So the bad luck stays at the temple."
    murakami "The bad luck stays where you left it. That is not the same thing."
    "She buys a slip and reads it without expression."
    mc "What does it say?"
    murakami "That I should be careful with my words."
    mc "Is that bad?"
    murakami "It is always true. That is the trick of fortune slips."
    mc "(She folds it and puts it in her pocket. She does not tie it to the rack.)"

    menu:
        "Draw an omikuji of my own.":
            "I pay, shake the box, and take a slip. The paper is thin and warm from my hand."
            "I cannot read most of it. Murakami reads it over my shoulder."
            murakami "It says: the road is longer than you think, and shorter than you fear."
            mc "That is not a fortune. That is a riddle."
            murakami "Most fortunes are riddles. It is how they stay true."
            $ reward_attributes_once("day12_omikuji", [("insight", "micro")], show="auto")
        "Ask about ma, the pause.":
            mc "You keep talking about the pause. Ma. What is it, really?"
            murakami "It is the space between two things. The silence between two notes. The gap between the torii and the temple."
            murakami "In English, empty means nothing. In Japanese, ma means a place where something can happen."
            mc "(I think of the train. The silence. The pause before the doors open.)"
            murakami "The pause is not the absence of the thing. It is the room the thing needs to be a thing."
            $ reward_attributes_once("day12_ma", [("grace", "micro")], show="auto")
        "Ask why people write wishes on wooden plaques.":
            mc "What are the wooden plaques? The ones with writing on them."
            murakami "Ema. Wishes. You write what you want and leave it for the gods to read."
            mc "Do they read them?"
            murakami "Someone reads them. That is enough."
            mc "(A wall of strangers' wishes, hanging in the rain. It is the most hopeful thing I have seen here.)"
            $ reward_attributes_once("day12_ema", [("nerve", "micro")], show="auto")

    "We walk to the side of the temple where the crowd thins. Murakami sits on a low stone wall. I sit beside her."
    murakami "You have been in this country for twelve days."
    mc "Twelve days."
    murakami "What have you learned?"
    mc "That I don't know anything."
    murakami "Good. That is the first thing. What is the second?"
    mc "That the pause is not empty."
    murakami "You have been listening."
    "She looks at the temple, not at me."
    murakami "You did the homework."
    mc "Ten times. The tenth one looked like a word."
    murakami "And did you look up what it meant?"
    mc "No."
    murakami "Good. The hand learned it first."
    murakami "The page. Did you read it?"
    mc "Four times. I brought you the sentence I did not understand."
    murakami "You brought it in your head. That counts."
    $ murakami_lessons = max(murakami_lessons, 3)
    murakami "This is the last lesson of the week. Ma. The interval. The space between."
    murakami "The train is ma. The silence between stations. The bow before the greeting. The breath before the word."
    murakami "Your whole life here is a ma. You are the space between the person you were and the person you will be."
    mc "(I do not have a joke for that. I do not want one.)"
    murakami "Do not fill it too quickly. The empty room is where the next thing happens."

    "She stands and brushes the dust from her cardigan."
    murakami "Same time next week. Bring the book. Bring a question you cannot answer."
    mc "I have about forty."
    murakami "Bring one. The other thirty-nine will wait."
    "She walks into the crowd and is gone before I can say goodbye."

    scene bg_asakusa_smoke with walk_fade
    "I turn back toward the courtyard. A woman has set up a folding table between the incense burner and the souvenir stalls."
    "No sign. No price. A deck of cards, face down, and a small brass bowl."
    "She looks up before I decide whether to stop."
    fortune_teller "You have been here before."
    mc "In Asakusa?"
    fortune_teller "Not Asakusa."
    "She turns one card over. A figure on a table, wires at the wrists. The card is worn white at the corners."
    fortune_teller "The cards say you are being looked after."
    mc "By whom?"
    "She smiles the way people smile at a question they have already answered."
    fortune_teller "Come back when you are ready to hear it. You will not be. You will come back anyway."
    "She gathers the cards. When I look again, the table is folded and she is part of the crowd."
    mc "(I did not see her stand up.)"
    $ fortune_teller_met = True

    scene bg_asakusa_kaminarimon with walk_fade
    "I stand under the big lantern for a while. The smoke goes up. The people go in and out."
    mc "(One afternoon. One meeting. One time.)"
    mc "(The afternoon is mine. I should use it.)"

    scene bg_station with walk_fade
    "The train back is quieter. The Sunday crowd has thinned. I find a seat by the window."
    "The city goes past in the wrong order: old, new, old, new. A shrine, a convenience store, a shrine."
    mc "(The country is not one thing. It is a conversation between two things.)"

    scene bg_home_exterior_day with walk_fade
    "The afternoon is still mine. The book is in my bag. The city is where I left it."
    mc "(One place. That is the rule I have given myself. One place, and then home.)"
    call free_afternoon

    call dinner_open

    father "And the temple?"
    mc "The gate has burned down and been rebuilt. The smoke is medicine. The bad luck stays where you leave it."
    father "That is a lot for one afternoon."
    mc "It was a lot of temple."
    hikari "He's been like this all day."
    father "It is a useful thing to be like."

    call dinner_close

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the sheet with the three scripts is on the desk. The Kokoro is beside it. The tea is still warm."
    $ night_desk_line = "the week"
    call night_open

    menu:
        "Tell her about the pause.":
            mc "Murakami says the pause is not empty. Ma. The space between."
            hikari "She would say that."
            mc "What do you think it is?"
            hikari "I think it's the part of the day I don't tell anyone about."
            mc "(She says it lightly. It does not land lightly.)"
            $ remember("hikari", "told her the pause is not empty, and she said it is the part of the day she does not tell anyone about")
            $ reward_attributes_once("day12_night_ma", [("grace", "micro")], show="auto")
        "Ask her what happens next week.":
            mc "What happens next week?"
            hikari "More classes. More trains. More of the same, only harder."
            mc "That's not an answer."
            hikari "It's the answer I have. The same only harder is how you get good at something."
            $ remember("hikari", "asked what happens next week, and she said the same only harder")
            $ reward_attributes_once("day12_night_next", [("insight", "micro")], show="auto")
        "Say nothing. Drink the tea.":
            "I do not say anything. The tea is hot and the room is quiet."
            "Hikari does not fill the silence. She has learned that I do not need her to."
            mc "(Some things do not need a sentence. This is one of them.)"
            $ remember("hikari", "drank the tea in silence on the last night of the week")
            $ reward_attributes_once("day12_night_quiet", [("nerve", "micro")], show="auto")

    # The Act 3 seed. She was in the genkan on Thursday when it stopped being
    # the genkan. She has been carrying it for three days and says it the way
    # you admit something: facing away, almost asleep.
    hikari "Thursday morning. In the genkan."
    mc "What about it?"
    hikari "For a second it wasn't the genkan. It was a corridor. White. You saw it too."
    "I do not answer."
    hikari "That's what I thought."
    "She does not ask anything else. She finishes her tea and stays on the far side of the question."

    call night_close

    "The week is over. The elective is not. The country is not."
    "I turn off the lamp. The room is dark. The room is not empty."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump monday_asakusa
