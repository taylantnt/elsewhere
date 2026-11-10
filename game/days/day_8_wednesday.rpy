################################################################################
## DAY 8 — WEDNESDAY, APRIL 15, 2026
## The day of the frog: chopsticks, the quiet car, and Bashō.
################################################################################

label wednesday_morning:
    $ set_story_day(8)
    call day_transition

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "I wake before the alarm. The ceiling is the same ceiling. The boxes are the same boxes."
    "What is different is that I know which sounds belong to the house now."
    mc "(The pipe at six. The fridge at six-fifteen. Hikari's door at six-twenty.)"
    "Two weeks to the midterm. The calendar in my head has started counting down like a fuse."
    mc "(It is a fuse. I do not know who lit it, or why I keep checking it, but it is a fuse.)"

    "My phone buzzes against the desk."

    if "chef" in wire_unlocked:
        $ run_chat("chef", [
            {"them": "Don't come today. Closed Wednesdays.", "options": [
                {"label": "\"I remember. It's on your profile.\"",
                 "send": "I remember. It's on your profile.",
                 "them": ["Good.", "Eat something before you go. Not convenience store bread."]},
                {"label": "\"Then where am I supposed to eat?\"",
                 "send": "Then where am I supposed to eat?",
                 "them": ["Home. You have a home now.", "That is the whole point of one."]},
            ]},
            {"them": "And don't tell anyone I texted you. I have a reputation."},
        ])
        mc "(A man who closes his shop on a Wednesday and texts a customer to make sure he eats. That is the whole man, I think.)"
    else:
        $ run_chat("hikari", [
            {"them": "You're awake. I can hear you moving.", "options": [
                {"label": "\"I'm awake.\"",
                 "send": "I'm awake.",
                 "them": ["Good. Don't make me knock.", "I have a list today."]},
                {"label": "\"How can you hear me moving?\"",
                 "send": "How can you hear me moving?",
                 "them": ["This house is made of paper and opinions.", "I hear everything."]},
            ]},
        ])
        mc "(She texts me from the next room. This is the house now.)"

    "Three knocks, then the door slides open before I answer it."
    hikari "Morning. You're up before the knock."
    mc "I was awake."
    hikari "You were horizontal."
    mc "Those aren't mutually exclusive."
    hikari "They are in this house."
    "She leans in the doorway with her bag already on her shoulder."
    hikari "Look at you. Dressed, upright, not confused about which day it is."
    mc "It's Wednesday."
    hikari "It's Wednesday. He knows the days now."
    mc "(She says it like a teacher marking a paper. She is pleased. She is trying not to be.)"
    hikari "Come down. Mom made too much rice again and Dad is pretending he didn't notice."
    "She is gone before I can ask what the list is."

    scene bg_kitchen with walk_fade

    "The kitchen smells like rice and grilled fish and the particular green of morning tea."
    mother "There he is. Sit."
    father "You are early."
    mc "I woke up early."
    father "That is not the same thing."
    mc "(It is not. He is right. I do not tell him that.)"
    "Hikari puts a bowl down in front of me without being asked and sits opposite, elbows on the table."
    "Tetsuo looks at her elbows. Hikari looks back. The elbows stay where they are."

    "I pick up my chopsticks. Mother watches my hand."
    mother "Do you know the rules?"
    mc "Some of them."
    mother "Then you know the important one."
    "She points at my bowl with her own chopsticks."
    mother "Never stand them up in the rice. That is for the dead. We leave a bowl that way at the altar."
    mc "(I have seen that. In films. I thought it was just how the bowl was set down.)"
    mother "And never pass food from your chopsticks to someone else's. That is the other one. The bones."
    mc "The bones."
    mother "At a funeral, the family passes the bones that way. So we do not do it at dinner."
    "She says it plainly, the way she says everything, and then goes back to her rice."
    father "It is not superstition. It is a way of remembering who is not at the table."
    mc "(That is the most he has said all morning.)"

    menu:
        "Ask what else is for the dead, and for the living.":
            mc "What else is for the dead? The rules, I mean."
            mother "The incense. The water. The bowl of rice on the altar every morning."
            mother "The living get the same things, only we eat them."
            mc "(She says it like a joke. It is not a joke. It is the whole house.)"
            $ reward_attributes_once("day8_kitchen_altar", [("insight", "micro")], show="auto")
        "Admit I didn't know any of this.":
            mc "I didn't know any of this. I thought chopsticks were just... chopsticks."
            mother "They are. And they are also a language. You are learning both."
            hikari "He's learning the language of lunch."
            mother "Hikari."
            hikari "What? It's true."
            $ reward_attributes_once("day8_kitchen_admit", [("grace", "micro")], show="auto")
        "Try to use them properly for the rest of the meal.":
            "I set the chopsticks down parallel on the rest, the way she did, and pick them up again."
            "It takes me three tries to make it look like one motion."
            mother "Better. Again."
            "I do it again. It is still not one motion. She does not laugh."
            $ reward_attributes_once("day8_kitchen_practice", [("nerve", "micro")], show="auto")

    father "You are taking the train with Hikari?"
    mc "The proper way."
    father "The proper way is the long way. The long way is where you learn the city."
    hikari "He's been learning the city all week."
    father "Then today he can learn the train."
    mc "(That is either a lesson or a warning. I am starting to think they are the same thing in this house.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The morning is cool enough for a jacket and warm enough to regret it by the station."
    "Hikari walks a half-step ahead of me, the way she does when she is deciding something."
    hikari "Question."
    mc "Already?"
    hikari "Question. Which platform do we take?"

    menu:
        "The one on the left. Local train.":
            mc "The one on the left. Local."
            hikari "Good. You were listening."
            $ reward_attributes_once("day8_platform_right", [("insight", "micro")], show="auto")
        "The one on the right. Rapid train.":
            mc "The one on the right. Rapid."
            hikari "Other one. The rapid skips our stop."
            hikari "You'll remember it next time. That's what next times are for."
            $ reward_attributes_once("day8_platform_wrong", [("nerve", "micro")], show="auto")

    scene bg_station with walk_fade
    "The station at seven-thirty is a machine that has already decided everything."
    "People move through the gates in a stream, card after card, beep after beep."
    hikari "IC card. Don't fumble it at the gate. The person behind you has a train to catch."
    mc "Everyone has a train to catch."
    hikari "Everyone here has the same train to catch. That's the difference."

    scene bg_platform with walk_fade
    "The platform is a held breath. A yellow line, a queue that is not a queue, a sign that says the train is coming in one minute."
    "It comes in one minute."

    scene bg_train_interior with walk_fade
    "The car is full and silent."
    "Not empty-silent. Full-silent. Forty people, and not one of them talking."
    "A man in a suit is asleep standing up, his hand through the strap, his face perfectly calm."
    "A woman reads a paperback with a plain paper cover, the way you would cover a book you did not want anyone to see."
    mc "(Nobody is looking at anybody. Everybody knows exactly where everybody is.)"
    hikari "You're doing the thing."
    mc "What thing?"
    hikari "The thing where you look at everyone and think about it."
    mc "Is that a problem?"
    hikari "No. It's just noticeable."

    menu:
        "Ask why nobody is talking.":
            mc "Why is it so quiet? It's not a rule, is it?"
            hikari "It's not a rule. It's worse. It's a preference."
            hikari "Everyone here has agreed to be alone together. The train is the room where we all pretend we're the only one in it."
            mc "(That is either the loneliest thing I have heard here or the most polite.)"
            $ reward_attributes_once("day8_train_quiet", [("insight", "micro")], show="auto")
        "Give up my seat to the old woman by the door.":
            "An old woman gets on at the next stop and stands by the door with a shopping bag."
            "I stand up before I think about it and gesture at the seat."
            "She looks at me, then at the seat, then at me again."
            "Thank you, she says. It is almost a question."
            mc "Of course."
            hikari "You didn't have to."
            mc "I know."
            hikari "She'll tell someone about it. That's how it works here. One good thing gets passed around all day."
            $ reward_attributes_once("day8_train_seat", [("grace", "micro")], show="auto")
        "Watch the sleeping man and try to stand like him.":
            "I copy the sleeping man's stance, one hand through the strap, eyes closed."
            "The train turns. I open my eyes. He is still asleep."
            hikari "You're not fooling anyone."
            mc "I'm practising."
            hikari "For what?"
            mc "For being a person who can sleep standing up."
            hikari "..."
            hikari "That is the most honest ambition you've had all week."
            $ reward_attributes_once("day8_train_sleep", [("nerve", "micro")], show="auto")

    scene black with Fade(1.0, 0.3, 0.0)
    stop music fadeout 1.0
    "Two changes. At the second station I do not lose track of which floor we are on."
    "Hikari notices. She does not say anything. She just walks a little slower."

    scene bg_school_gate with Fade(0.0, 0.0, 1.5)
    play music "audio/Music/school.mp3" fadein 1.5
    $ phone_map_visit("school")
    "The gate knows me now. The guard on the morning shift nods once."
    hikari "Right. I have seminar. You have the lecture. Try not to be late."
    mc "I'm never late."
    hikari "You were late on your first day."
    mc "That was a different person."
    hikari "It was eight days ago."
    "She waves without turning around."

    scene bg_campus_interior with walk_fade
    "The corridor smells like floor wax and rain that has not happened yet."

    scene bg_lecture_hall with walk_fade
    play music "audio/Music/classroom.mp3" fadein 1.0

    "The professor is already at the board. He has written a single word: 蛙."
    professor "Kaeru. Frog."
    "He lets the word sit there."
    professor "You will have been taught the poem. The old pond. The frog. The sound of water."
    professor "You will have been told it is about a frog."
    "Somebody laughs. The professor does not."
    professor "It is not about a frog. It is about the moment the world becomes small enough to notice."
    professor "Bashō did not invent the frog. He invented the attention."
    "He writes three more words beneath it: 古池, 蛙, 水の音."
    professor "The old pond. The frog. The sound of water. Three images, and one of them is a season."
    professor "The kigo is the frog. Frog is spring. The first warmth. The water warm enough to hold a life."
    professor "The poem is not the frog. The poem is the season the frog is standing in."
    mc "(I write: the frog is the door. The season is the room.)"
    professor "There is a word for what the poem does. Mono no aware. The pathos of things."
    professor "Not sadness. Not quite. The feeling of a thing being beautiful because it is passing."
    professor "The frog will jump. The sound will end. The pond will go still again. The poem holds all three."

    menu:
        "Write the poem down before the bell.":
            "I write it down. The frog. The river. The quiet."
            "The characters are clumsy. The professor sees my hand moving and does not correct it."
            mc "(It is mine now. The wrong characters and all.)"
            $ reward_attributes_once("day8_class_write", [("grace", "micro")], show="auto")
        "Just listen. The listening is the lesson.":
            "I put the pen down and listen to the poem again."
            "For a moment the room is the pond. Then the bell goes and the room is a room."
            mc "(I do not have the words for it yet. I have the listening. That is enough for today.)"
            $ reward_attributes_once("day8_class_listen", [("insight", "micro")], show="auto")
        "Ask about Issa, the other haiku poet.":
            mc "What about Issa? He wrote about insects, didn't he?"
            professor "Issa wrote about the small things because the large things had already happened to him."
            professor "A fly. A snail. A child's hand. He buried four children and wrote about a fly."
            mc "(The room is very quiet. The professor lets it be quiet.)"
            professor "That is the other half of mono no aware. The beauty is not despite the loss. It is made of it."
            $ reward_attributes_once("day8_class_issa", [("nerve", "micro")], show="auto")

    scene bg_campus_interior with walk_fade
    "Hikari has seminar until five. The afternoon is a door with nothing written on it."
    mc "(One place. That is the rule I have given myself. One place, and then home.)"
    call free_afternoon

    scene bg_home_night with walk_fade
    $ room_ambient(True)
    "The house is warm the way it is when someone has been cooking for a while."
    "I leave my shoes by the door and follow the smell to the kitchen."

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

    father "And the midterm?"
    mc "Two weeks. Essays. A practical."
    father "Then you have two weeks."
    mc "That's what two weeks means."
    hikari "He's been like this all day."
    father "It is a useful thing to be like."
    "Nobody argues with that. We eat."

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the handout is exactly where I left it, open to the kigo list."
    "I have read it so many times that the words have started to look like themselves again instead of like a code."
    "A knock at the door. Hikari, with two cups of tea and her own notes under her arm."
    hikari "I'm not staying. I'm just making sure you're not staring at the wall."
    mc "I was staring at the handout."
    hikari "Same thing."
    "She sets the tea down and sits on the floor with her back against the bed."

    menu:
        "Tell her about the frog.":
            mc "The professor says the frog is the season."
            hikari "He would say that."
            mc "What do you think it is?"
            hikari "I think it's a frog. And I think that's the point."
            hikari "The poem doesn't need the season explained. It needs you to hear the water."
            mc "(She says it like she has known it for years. She probably has.)"
            $ reward_attributes_once("day8_night_frog", [("grace", "micro")], show="auto")
        "Ask her what mono no aware means to her.":
            mc "Mono no aware. What does it mean to you? Not the dictionary."
            hikari "It means I keep the ticket stubs."
            mc "The ticket stubs?"
            hikari "From films. Trains. Things that already happened. I keep them in a box under my bed."
            mc "Why?"
            hikari "Because they were real. And because they're over."
            mc "(I do not have anything to say to that. I drink the tea instead.)"
            $ reward_attributes_once("day8_night_aware", [("insight", "micro")], show="auto")
        "Say nothing. Drink the tea.":
            "I do not say anything. The tea is hot and the room is quiet."
            "Hikari does not fill the silence. She has learned that I do not need her to."
            mc "(Some things do not need a sentence. This is one of them.)"
            $ reward_attributes_once("day8_night_quiet", [("nerve", "micro")], show="auto")

    "She takes her cup and leaves the door open a hand's width."
    "I listen to her go down the stairs, then the house settle into its night sounds."
    "The handout is still open. The tea is still warm."
    "Tomorrow is Thursday. Another class. Another train. Another small thing to notice."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump thursday_morning
