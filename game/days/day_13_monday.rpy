################################################################################
## DAY 13 ― MONDAY, APRIL 20, 2026
## The old city with Hikari: the gate, the smoke, the paper, and the cards.
################################################################################

label monday_asakusa:
    $ set_story_day(13)
    call day_transition

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Monday arrives with a list. I can feel it before I open my eyes."
    "The ceiling is the same ceiling. The light is the color of a train window. Somewhere below, the rice cooker clicks off."
    mc "(Two weeks. The midterm is not a rumor anymore. It is a date.)"

    "My phone buzzes once on the desk."

    if "murakami" in wire_unlocked:
        $ run_chat("murakami", [
            {"them": "The page. Did it stay with you?", "options": [
                {"label": "\"I read it again last night.\"",
                 "send": "I read it again last night.",
                 "them": ["Good.", "A page that stays is a page you have not finished."]},
                {"label": "\"I understood more of it this time.\"",
                 "send": "I understood more of it this time.",
                 "them": ["Then you are reading it wrong.", "Understanding is the last thing. First the shape. Then the sound."]},
            ]},
            {"them": "Class at ten. Bring the book, not the answers."},
        ])
        mc "(She texts like a woman who has already read the conversation and is waiting for me to catch up.)"
    else:
        $ run_chat("hikari", [
            {"them": "Don't make plans after class.", "options": [
                {"label": "\"Why?\"",
                 "send": "Why?",
                 "them": ["Because I have a plan.", "It is a good plan. You will hate it for ten minutes and then like it."]},
                {"label": "\"I have a job now.\"",
                 "send": "I have a job now.",
                 "them": ["You have a job? Since when?", "We will discuss this on the train."]},
            ]},
        ])
        mc "(She has a plan. That is either the best or worst sentence in this house.)"

    "Three knocks, then the door. Hikari is already dressed, which is suspicious."
    hikari "Up. We have a train to catch."
    mc "It's Monday."
    hikari "It is Monday. That is why we are catching a train."
    mc "School."
    hikari "School first. Then the plan."
    "She is gone before I can ask what the plan is."

    scene bg_kitchen with walk_fade

    "The kitchen is fast and practical on a Monday. Mother is packing something into a cloth. Father is reading the news with his glasses on."
    mother "Sit. Eat. You have a lecture."
    father "You are going somewhere after."
    mc "Hikari has a plan."
    father "Hikari always has a plan. The question is whether the plan has you in it."
    hikari "He is in it."
    father "Then eat. A plan is easier to survive on rice."
    mother "Take the umbrella."
    mc "It is not raining."
    mother "It will be raining somewhere."
    mc "(I take the umbrella. It is becoming a law of this house.)"

    scene bg_lecture_hall with walk_fade

    "The lecture hall smells of chalk and wet coats. The professor is already at the board, writing a sentence in three scripts."
    professor "Today, the city as a text."
    professor "A city is not a place. It is a set of instructions. Walk here. Wait there. Do not stand in the road."
    professor "The instructions are written in stone and glass and the way people stand on an escalator."
    mc "(I think of the station. The yellow line. The people who step aside before the doors open.)"
    professor "Tokyo is a city that tells you what to do without ever raising its voice."
    professor "The interesting question is not whether you obey. It is what you do when the instructions contradict each other."
    mc "(That is either a lecture or a warning. I am starting to think they are the same thing here.)"

    menu:
        "Write down the line about instructions.":
            "I copy it into the margin of my notebook. The sentence looks different in my handwriting, which is the point."
            mc "(A city is a set of instructions. I have been reading them wrong. I thought they were rules. They are a conversation.)"
            $ reward_attributes_once("day13_lecture_instructions", [("insight", "micro")], show="auto")
        "Ask what happens when the instructions contradict.":
            mc "Professor. What happens when the instructions contradict each other?"
            professor "You choose which one to believe. That is what a citizen is."
            mc "And if you choose wrong?"
            professor "Then you learn the city has a longer memory than you do."
            $ reward_attributes_once("day13_lecture_contradict", [("nerve", "micro")], show="auto")
        "Watch the student beside me copy every word.":
            "The student beside me writes without looking up. Her pen moves in a straight line. She has done this before."
            mc "(She is not learning the lecture. She is learning the shape of the lecture. That is a different thing.)"
            $ reward_attributes_once("day13_lecture_watch", [("grace", "micro")], show="auto")

    scene bg_campus_interior with walk_fade

    "Hikari is waiting by the stairs with two cans of coffee and a smile she is trying to make innocent."
    hikari "You survived."
    mc "It was a lecture."
    hikari "Lectures are survival exercises with chairs."
    "She hands me a can. It is the one I would have picked."
    mc "How did you know?"
    hikari "You always pick the blue one."
    mc "I do not always pick the blue one."
    hikari "You do. I like knowing things about you."
    "She starts walking before I can argue."
    hikari "We are going to Asakusa."
    mc "Asakusa."
    hikari "The old city. You have been there with your teacher. Now you are going with me."
    mc "What's the difference?"
    hikari "She showed you the history. I am going to show you the snacks."
    mc "(That is the most Hikari sentence I have heard all week.)"

    scene bg_alley with walk_fade
    play music "audio/Music/kombini.mp3" fadein 1.0
    "On the way to the station, she stops in front of a combini."
    hikari "Supplies."
    mc "For a train ride?"
    hikari "For the old city. You cannot do history on an empty stomach."
    "The door chimes twice going in. The air inside is cold and bright and smells faintly of fried things."
    play sound "audio/SFX/combini.mp3"
    mc "(Every combini in this city is the same combini. That is either comforting or suspicious. I have not decided.)"

    if not tanaka_met:
        call combini_first_counter
    else:
        scene bg_combini with walk_fade
        "Tanaka is at the register, doing three things at once. He scans our things without looking up."
        tanaka "いらっしゃいませ。"
        hikari "He says that to everyone."
        mc "That is the job."
        hikari "You know him?"
        mc "I know the script."

    scene bg_station with walk_fade
    "Outside, the paper bag is warm in my hand."
    hikari "Eat it before we get there. It is not a souvenir."
    mc "It's a snack."
    hikari "It is a ritual. The snack is the formality."
    "The station is full of Monday people. They are not in a hurry. They are in a schedule."

    scene bg_platform with walk_fade
    "The platform is a long grey room with a yellow line and a sign that says the train is coming in two minutes."
    "It comes in two minutes."
    hikari "This is the part where you ask me why Asakusa."
    mc "Why Asakusa?"
    hikari "Because it is the oldest part of the city, and it is also the most crowded, and it is also the most fun."
    hikari "The old and the fun are not opposites. That is the first thing you have to learn."
    mc "(She says it like a teacher. She has been waiting to say it.)"

    scene bg_train_interior with walk_fade
    "The car is warm and half full. A woman is reading a paperback with a plain cover. Two schoolboys are playing a game on one phone."
    "Hikari sits beside me and opens her own coffee."
    hikari "You have been doing the serious version of Japan all week."
    mc "There is a serious version?"
    hikari "There is the version with temples and homework and a woman in a grey cardigan telling you what a pause means."
    mc "That version is good."
    hikari "It is good. It is also exhausting. Today we do the version with fried things and paper fortunes."
    mc "(She is right. I do not tell her that. She would be unbearable.)"

    scene bg_asakusa_kaminarimon with Fade(0.0, 0.0, 1.5)
    "We come out of the station and the city changes in the time it takes to cross a street."
    "The buildings get shorter. The signs get older. The air smells of incense and fried sweets and rain that has not happened."
    "And then the gate."
    "A huge red lantern hangs in the middle of it, black characters on red, big enough to be a room. People stop underneath it and take the same photograph."
    hikari "Kaminarimon. The gate of the thunder god."
    mc "It is bigger than I thought."
    hikari "It is smaller than it used to be. The first one was bigger. The city keeps rebuilding it smaller and calling it the same gate."
    mc "Is it the same gate?"
    hikari "That is the question, isn't it."

    "She pulls me to the side, out of the crowd, and points at the two figures standing in the gate's bays."
    hikari "That is Raijin. The thunder god. He has the drums."
    "The figure is red and muscular, surrounded by a ring of drums. His face is not angry. It is busy."
    hikari "And that is Fuujin. The wind god. He has the bag."
    "The other figure is green and lean, holding a bag over his shoulder. He looks like a man who has just remembered something."
    mc "They are guardians."
    hikari "They guard the approach. Not the temple. The approach."
    mc "What is the difference?"
    hikari "The temple is where the god is. The approach is where you are. They are there to make sure you get from one to the other."
    mc "(Two gods whose whole job is the walk between the street and the door.)"
    hikari "They are also terrifying. That is on purpose. A gate should make you feel like you are leaving something behind."
    mc "What am I leaving behind?"
    hikari "That is the question you are supposed to ask yourself while you walk through it."
    "The lantern above us moves a little in the wind. The characters on it are black and sharp."
    mc "(Raijin has the storm. Fuujin has the wind. Neither of them has a door. The door is the thing they are guarding.)"

    menu:
        "Ask why the gods are so frightening.":
            mc "Why make them frightening? If they are protecting people."
            hikari "Because a gate that looks like a shop is not a gate. It is a corridor with a sign."
            hikari "The fear is the threshold. You are supposed to feel it in your stomach before you feel it in your feet."
            mc "(I look up at Raijin's drums. I do feel it. Just a little.)"
            $ reward_attributes_once("day13_gate_fear", [("insight", "micro")], show="auto")
        "Walk through the gate without stopping.":
            "I step under the lantern and keep walking. The crowd closes around me. For a second the gate is a red room with no walls."
            "Then I am on the other side, and the street is already pulling me forward."
            mc "(I did not feel anything. Then I did. The feeling arrived after the crossing.)"
            $ reward_attributes_once("day13_gate_cross", [("nerve", "micro")], show="auto")
        "Wait under the lantern and let the crowd pass.":
            "I stand under the lantern while people flow around me. A woman in a kimono. A man with a camera. A child on her father's shoulders."
            "Nobody looks up. Everybody is inside the photograph they are about to take."
            mc "(The gate is not the lantern. The gate is the moment before the photograph.)"
            $ reward_attributes_once("day13_gate_wait", [("grace", "micro")], show="auto")

    scene bg_asakusa_inside with walk_fade
    "Beyond the gate, Nakamise is a long street of shops with the temple at the far end."
    "It is not a street. It is a funnel. The crowd moves in one direction, toward the temple, and you cannot walk against it."
    "The shops sell fans and hairpins and small wooden dolls. They sell rice crackers and soft serve and things on sticks."
    "A woman is turning a crank that drops tiny cakes into a box. A child watches as if it is magic. It is a machine, but it is also magic."
    hikari "Nakamise. One of the oldest shopping streets in Japan. It used to be the road to the temple."
    mc "It is still the road to the temple."
    hikari "It is still the road. It is also a place to buy a phone charm shaped like a cat."
    mc "Those two things do not go together."
    hikari "They go together perfectly. That is the country. The sacred and the snack stand."
    mc "(I have heard that before. From her. From Murakami. It is becoming a theme.)"

    "She stops at a stall and buys a small bag of ningyo-yaki, the little cakes shaped like dolls. She eats one and hands me the bag."
    hikari "Try it. It is red bean. If you say you don't like red bean, I will pretend not to hear you."
    "The cake is warm and sweet and a little bit salty. It is good."
    mc "It's good."
    hikari "Of course it's good. It's fried."
    mc "(Everything she likes is fried. That is also a personality.)"

    "A shopkeeper calls out to the crowd. A woman in a yukata laughs at something her friend says. A man in a suit buys a fan for a child who is not with him."
    "For a second I hear the same shopkeeper say the same thing in exactly the same voice. I turn. She is saying it to a different customer."
    mc "(Of course she is. That is her job. She says it all day.)"

    scene bg_asakusa_smoke with walk_fade
    "At the end of the street, the temple opens up. The courtyard is wide and grey and full of people."
    "A large bronze burner stands in the middle. Smoke comes out of it in a slow, steady column."
    "People stand around it with their hands out. They pull the smoke toward themselves, over their heads, over their shoulders, over their children."
    hikari "The smoke is medicine. You pull it toward the part of you that needs it."
    mc "Does it work?"
    hikari "It works if you stand there long enough to believe it."
    mc "(That is the same thing Murakami said. Maybe it is the same thing everyone says here.)"

    "I watch them. An old woman with a bad shoulder pulls the smoke into her collar. A man in a suit waves it over his briefcase. A mother lifts her child so the smoke can reach his head."
    "A young man does it quickly, the way you would check a pocket. A group of students do it for a photograph and then walk away."
    "Nobody laughs. Nobody explains. The smoke is a small, serious thing in the middle of a crowd."
    hikari "You are watching again."
    mc "I'm learning the rules."
    hikari "There are no rules. There are just a thousand people agreeing."
    "She steps up to the burner and waves the smoke toward her face with both hands. She closes her eyes for a second. Then she steps back."
    hikari "Your turn."
    mc "What part do I pick?"
    hikari "The part that needs it."
    mc "(I do not know what part of me needs it. I am not sure I know what part of me is.)"
    "I put my hands out and pull the smoke toward my face. It smells of cedar and something older, like a cupboard that has been closed for a long time."
    "I wave it over my head. Over my chest. Over my hands. I feel ridiculous. Then I stop feeling ridiculous."
    mc "(The smoke does not do anything. The standing does. The standing in the middle of a crowd, doing the same thing as everyone else, for no reason except that it is what people do here.)"
    hikari "You did all of you."
    mc "I couldn't pick."
    hikari "That's greedy."
    mc "That's efficient."
    "She laughs. It is a real laugh, not the one she uses at the table."
    "For a second the smoke curls the wrong way, toward the burner instead of away from it. I blink. It is smoke again."

    # The paper reads the person who drew it. Grace turns the slip good, nerve
    # turns it bad, and an even hand gets the honest middle. This is the one
    # place the attribute totals are allowed to answer a fortune directly.
    if attribute_total("grace") > attribute_total("nerve"):
        $ fortune_result = "good"
    elif attribute_total("nerve") > attribute_total("grace"):
        $ fortune_result = "bad"
    else:
        $ fortune_result = "mixed"

    scene bg_asakusa_kuji with walk_fade
    "At the side of the courtyard, a row of wooden racks is covered in small white papers tied in knots."
    "Hikari sees the omikuji stand and stops walking."
    hikari "Oh. Oh, we have to do this."
    mc "We have to?"
    hikari "It is the law. You cannot come to a temple and not draw a fortune. It would be rude to the temple."
    mc "I don't think that's how laws work."
    hikari "It is how this law works."
    "The stand is a small wooden box with a slot and a row of drawers. You shake the box until a stick comes out, then you find the drawer with the number."
    hikari "You go first."
    mc "Why me?"
    hikari "Because you are the guest. Guests get the first fortune. It is also the law."
    mc "(I am starting to think she makes up laws for fun.)"

    "I put a coin in the box. I shake it. A stick slides out with a number on it. I open the drawer and take the slip."
    "The paper is thin and warm from my hand. There is a character at the top and a column of smaller characters below it."
    mc "I can't read most of it."
    hikari "Give it here."
    "She reads it. Her face does something complicated."
    if fortune_result == "good":
        hikari "Daikichi. Great fortune."
        mc "Is that good?"
        hikari "It is the best one. It says a door you have already opened will open again. And a small kindness will return to you before the day is over."
        mc "(A door I have already opened. I think of the gate. I think of the house.)"
        hikari "Look at you. The paper likes you."
    elif fortune_result == "bad":
        hikari "Kyo. Misfortune."
        mc "Oh."
        hikari "It says a voice will call you by a name you have not been given. Do not answer the first time."
        mc "(The paper is very specific for a piece of paper.)"
        hikari "Okay. We are tying this one to the rack."
    else:
        hikari "Shokichi. Small fortune."
        mc "Small is good?"
        hikari "Small is honest. It says the road is longer than you think, and shorter than you fear. Keep walking."
        mc "(That is not a fortune. That is a riddle.)"
        hikari "Most fortunes are riddles. It is how they stay true."

    "She reads her own slip and folds it before I can see it."
    mc "What did you get?"
    hikari "Private."
    mc "It's a piece of paper."
    hikari "It's a piece of paper about my future. That is the most private kind of paper."
    "She ties hers to the rack without showing me. I tie mine, or I don't, depending on what it said."
    if fortune_result == "good":
        "I fold the good fortune and put it in my pocket. I do not know why. It feels like something I should keep."
    else:
        "I tie the paper to the rack with the others. The knot is clumsy. A woman beside me does it in one motion."
        mc "(Something about the bad luck staying here. I copy what she did. I am not sure I believe it.)"

    scene bg_fortune_stall with walk_fade
    "We walk to the side of the temple where the crowd thins. Between the incense burner and the souvenir stalls, a woman has set up a folding table."
    "No sign. No price. A deck of cards, face down, and a small brass bowl."
    "She looks up before I decide whether to stop."
    fortune_teller "You came back."
    mc "You said I would."
    fortune_teller "I did. I am rarely wrong about the things people do not want to hear."
    hikari "You know her?"
    mc "I met her yesterday. She told me I had been here before."
    hikari "You meet a lot of people."
    fortune_teller "Sit. Both of you. The cards have been waiting."
    hikari "We should go."
    mc "One minute."
    hikari "That is what people say before they lose an hour."
    "I sit. Hikari stands behind me with her arms crossed, which is how she says she is staying without saying it."

    "The fortune teller turns over the first card. A red gate, painted in a style older than the city."
    fortune_teller "The gate. You walked through it today. You think it is a place. It is a decision."
    mc "A decision about what?"
    fortune_teller "About whether to keep walking."
    "She turns over the second card. A white corridor with a door at the end. There is no furniture. There is no color except the white."
    fortune_teller "You have seen this. Not in a dream. On a Thursday, in a house, between one room and another."
    "My mouth is dry."
    mc "How do you know that?"
    fortune_teller "The card knows. I only turn it over."

    call leak_flash

    scene black
    "Thursday. The genkan."
    "For a moment the genkan is not the genkan. It is a white corridor with a door at the end, and someone is waiting on the other side of it."
    doctor "Subject 04. Can you hear me?"
    "Then Hikari says my name and it is a house again."

    scene bg_fortune_stall with walk_fade
    "I am back at the table. The smoke is still going up. Hikari is looking at me."
    hikari "Hey. You went somewhere."
    mc "I'm here."
    hikari "You were not."
    fortune_teller "He was. That is the problem."
    "She turns over the third card. A figure on a table, wires at the wrists. The card is worn white at the corners."
    fortune_teller "This is not the future. This is the room you are in when you are not here."
    mc "What does that mean?"
    fortune_teller "It means the corridor is not a memory. It is a place you go when the house forgets to be a house."
    mc "(The house forgets. The house. Not me.)"
    fortune_teller "Next time, do not look at the person behind you. Look at the door."
    mc "What is behind the door?"
    fortune_teller "That is the one thing I am not allowed to tell you."
    "She looks at Hikari for a moment. Hikari looks back. Something passes between them that I do not catch."
    fortune_teller "You saw it too, didn't you. The white corridor."
    hikari "How do you know that?"
    fortune_teller "The cards are not the only thing that talks."
    "Hikari's arms are no longer crossed. She is holding the edge of the table."
    mc "(I already knew. She told me last night. Hearing a stranger say it makes it real in a way her voice did not.)"

    if fortune_result == "good":
        fortune_teller "The paper in your pocket says a door will open. The cards say the same door is already open. You are standing in it."
    elif fortune_result == "bad":
        fortune_teller "The paper says a voice will call you by a name that is not yours. The cards say the voice is not lying. The name is."
    else:
        fortune_teller "The paper says the road is long. The cards say you have already walked part of it. That is the part that should worry you."

    "She gathers the cards. She does not shuffle them. She puts them in a small wooden box and closes the lid."
    fortune_teller "Before the month is out, you will be offered something you think you chose. You will not have chosen it. You will take it anyway."
    mc "Is that a warning?"
    fortune_teller "It is a description."
    "She pushes the brass bowl toward me. There is no price on it. I put a coin in anyway."
    fortune_teller "One question. You have earned one."
    menu:
        "Who are you?":
            mc "Who are you?"
            fortune_teller "Someone who read the end of the book. I am not allowed to tell you how it ends."
            mc "Is it a good ending?"
            fortune_teller "It is an ending. That is more than most people get."
            $ reward_attributes_once("day13_fortune_who", [("insight", "micro")], show="auto")
        "What is this place?":
            mc "What is this place? Really."
            fortune_teller "A page you are standing on. Be careful where you put your feet."
            mc "That is not an answer."
            fortune_teller "It is the answer that will still be true tomorrow."
            $ reward_attributes_once("day13_fortune_place", [("nerve", "micro")], show="auto")
        "Am I awake?":
            mc "Am I awake?"
            fortune_teller "That is the wrong question. Ask who is dreaming."
            mc "Who is dreaming?"
            fortune_teller "Now you are asking the right one. You are not ready for the answer."
            $ reward_attributes_once("day13_fortune_awake", [("grace", "micro")], show="auto")

    hikari "Okay. That's enough."
    "She takes my arm and pulls me up. The fortune teller does not stop her."
    fortune_teller "Come back when the cards have changed."
    mc "When will that be?"
    fortune_teller "When you have changed them."
    "She folds the table. When I look again, she is part of the crowd. I did not see her stand up."
    $ fortune_teller_met = True
    $ fortune_arc_started = True
    $ confidant_visits["fortune"] = max(confidant_visits.get("fortune", 0), 1)
    $ remember("hikari", "was with him at the fortune teller when the white corridor came back, and the cards named it")

    scene bg_asakusa_kaminarimon with walk_fade
    "We stand under the big lantern for a while. The smoke goes up. The people go in and out."
    hikari "You're shaking."
    mc "I'm cold."
    hikari "It's twenty degrees."
    mc "I'm cold in a specific way."
    "She does not argue. She stands closer, which is not the same as touching, but it is not nothing."
    mc "(One afternoon. One meeting. One time.)"

    scene bg_station with walk_fade
    "The train back is quieter. The Monday crowd has thinned. We find a seat by the window."
    if fortune_result == "bad":
        "A woman's voice behind me says a name. I turn. There is no one looking at me."
        "The voice says it again. It is not a name I know. It is a name I have been waiting to hear."
        hikari "What?"
        mc "Nothing. I thought someone said my name."
        hikari "They probably did. This is a city. People say names."
    elif fortune_result == "good":
        "The train doors open as we reach the platform. A woman gives up her seat for an old man. A child shares a bag of crackers with her mother."
        "Hikari buys me a drink from the vending machine. It is the blue one. I did not ask."
        hikari "I know which one you like."
        mc "You didn't have to."
        hikari "I wanted to. That's reason enough."
    else:
        "The train is exactly on time. It is always exactly on time. For a second that feels like a threat."
        "A man across the aisle is reading a newspaper with a magnifying glass. He turns the page at the same moment as a man two seats down."
        mc "(The city is full of people doing the same thing at the same time. That is what a city is.)"

    "The city goes past in the wrong order: old, new, old, new. A shrine, a convenience store, a shrine."
    mc "(The country is not one thing. It is a conversation between two things.)"

    scene bg_home_exterior_day with walk_fade
    "The afternoon is still mine. The book is in my bag. The city is where I left it."
    mc "(One place. That is the rule I have given myself. One place, and then home.)"
    $ last_afternoon_place = "fortune"
    call dinner_open

    father "And the temple?"
    if fortune_result == "bad":
        mc "The paper said a voice would call me by a name I have not been given. On the train, someone did."
        father "Did you answer?"
        mc "No."
        father "Good. A name is not a command. It is an invitation. You can decline."
        mc "(He says it like a rule about traffic. It is a rule about people.)"
    elif fortune_result == "good":
        mc "The paper said a small kindness would return to me before the day was over. Hikari bought me a drink without being asked."
        hikari "It was a vending machine. It was not a kindness."
        mc "It was the blue one."
        hikari "That is a preference, not a kindness."
        father "It is both. In this house it is both."
    else:
        mc "The paper said the road is longer than I think and shorter than I fear. I am still walking."
        mother "Then you are doing it right."
        mc "(I do not know if that is comfort or a warning. In this house it is usually both.)"

    call dinner_close

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the fortune slip is on the desk. The white corridor is still behind my eyes."
    $ night_desk_line = "the fortune slip"
    call night_open

    menu:
        "Ask her about the corridor again.":
            mc "Last night you said you saw the corridor. At the fortune teller, she said it like she already knew."
            hikari "She did."
            mc "Does that scare you?"
            hikari "It scares me that it didn't. It felt like being recognized."
            mc "By her?"
            hikari "By the room. Like the corridor knew my name."
            mc "(She says it the way she says true things: facing away, almost asleep.)"
            $ remember("hikari", "said the white corridor felt like being recognized, and that it knew her name")
            $ reward_attributes_once("day13_night_corridor", [("insight", "micro")], show="auto")
        "Ask what she drew at the omikuji.":
            mc "What did your fortune say?"
            hikari "I told you. Private."
            mc "You made me show you mine."
            hikari "That was different. Yours was a public fortune."
            mc "That sounds like a rule you just made up."
            hikari "It is now."
            "She takes the slip out of her pocket and unfolds it. It says: a door will open from the inside."
            hikari "I don't know what it means."
            mc "I do."
            hikari "Then don't tell me. I want to find out."
            $ remember("hikari", "showed him her omikuji: a door will open from the inside")
            $ reward_attributes_once("day13_night_omikuji", [("grace", "micro")], show="auto")
        "Say nothing. Let the day settle.":
            "I do not say anything. The tea is hot. The room is quiet. The fortune slip is on the desk."
            "Hikari does not fill the silence. She has learned that I do not need her to."
            mc "(Some things do not need a sentence. This is one of them.)"
            $ remember("hikari", "drank the tea in silence after Asakusa")
            $ reward_attributes_once("day13_night_quiet", [("nerve", "micro")], show="auto")

    call night_close

    "The week is not over. It has only started."
    "I turn off the lamp. The room is dark. The room is not empty."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump tuesday_week_two
