################################################################################
## DAY 9 — THURSDAY, APRIL 16, 2026
## The day of the world's first novel: the genkan, the platform, and Genji.
################################################################################

label thursday_morning:
    $ set_story_day(9)
    call day_transition

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "I wake before the alarm again. This is becoming a habit, and habits are how this house gets into you."
    "The light on the ceiling is the color of weak tea. Somewhere below, a cupboard closes."
    mc "(If I go down now, I beat Hikari to the kitchen.)"
    mc "(I do not know why that feels like winning. It does.)"

    "My phone buzzes once on the desk."

    if "sim" in wire_unlocked:
        $ run_chat("sim", [
            {"them": "Circle meets today. You should come.", "options": [
                {"label": "\"What are we shooting?\"",
                 "send": "What are we shooting?",
                 "them": ["Whatever the light does.", "Bring the camera. Or don't. The wall doesn't care."]},
                {"label": "\"I have class until four.\"",
                 "send": "I have class until four.",
                 "them": ["So does everyone.", "That's why we meet at five."]},
            ]},
            {"them": "Also: the wall is still there. I checked."},
        ])
        mc "(Sim texts like a man who has never been in a hurry in his life.)"
    else:
        $ run_chat("hikari", [
            {"them": "You're moving around up there. Suspicious.", "options": [
                {"label": "\"I'm going down first.\"",
                 "send": "I'm going down first.",
                 "them": ["You are not.", "I am already at the stairs."]},
                {"label": "\"I'm being efficient.\"",
                 "send": "I'm being efficient.",
                 "them": ["You're being suspicious.", "Come down before the rice gets cold."]},
            ]},
        ])
        mc "(She is already at the stairs. I can hear her.)"

    "I get dressed in the dark and go down before she can knock."

    scene bg_kitchen with walk_fade

    "The kitchen is already awake when I come down. I am first."
    mother "You are down before Hikari."
    mc "I woke up early."
    mother "Twice in a row. That is not early. That is a habit."
    "She says it with her back to me, which is how she says the things she means."
    father "The early one gets the tea."
    "He pushes a cup across the table without looking up from the newspaper."
    mc "Thank you."
    father "You are learning the house."
    mc "(That is the closest thing to praise he has given me since the airport. I do not move for a second.)"
    $ add_affection("father", 1)

    "Hikari comes down two minutes later, hair still damp, and stops in the doorway."
    hikari "...He's already down."
    mother "He is."
    hikari "Since when?"
    mc "Since today."
    hikari "I don't like it."
    mc "You said I was horizontal."
    hikari "You were horizontal. Now you're vertical. It's unsettling."
    mother "Sit, Hikari. Eat. You can be unsettled at the table."

    "The rice is hot. The miso is darker than yesterday. Mother watches me take the first spoonful."
    mother "Today I will teach you the three words."
    mc "The three words?"
    mother "The ones the house uses at the door. Itterasshai. Tadaima. Okaeri."
    mother "Itterasshai is what we say when you leave. Go and come back."
    mother "Tadaima is what you say when you come home. I am home."
    mother "Okaeri is what we say back. Welcome home."
    mc "(Three words for the same door, going in different directions.)"
    father "And otsukaresama. For work. For school. For anything that takes something out of you."
    father "You say it to the people who did the work. Not to yourself."
    mc "(He says it like a rule about traffic. It is a rule about people.)"

    menu:
        "Ask what happens if I forget the words.":
            mc "What happens if I forget them? At the door, I mean."
            mother "Nothing happens. That is the problem."
            mother "Nobody will tell you. They will simply notice."
            mc "(That is worse than being told. I will remember them now.)"
            $ reward_attributes_once("day9_kitchen_forget", [("insight", "micro")], show="auto")
        "Say itterasshai to the whole kitchen before I leave.":
            "I stand up with my bowl and say it before I can feel stupid about it."
            mc "Itterasshai."
            "Mother stops with the ladle in the air."
            mother "...Itterasshai."
            hikari "Look at that."
            mc "(My face is hot. I sit back down. Nobody laughs.)"
            $ reward_attributes_once("day9_kitchen_itterasshai", [("grace", "micro")], show="auto")
        "Ask about meiwaku, the word I keep hearing.":
            mc "What does meiwaku mean? I heard it on the train."
            father "It means trouble. The trouble you cause someone else by existing in their way."
            father "This country is built around not making meiwaku. It is why the trains are quiet."
            mc "(So the silence is not silence. It is a courtesy.)"
            $ reward_attributes_once("day9_kitchen_meiwaku", [("nerve", "micro")], show="auto")

    father "The genkan. You take your shoes off and you turn them around."
    mc "Turn them around?"
    father "So the next person can step into them. It costs nothing. It is the whole idea."
    mc "(I have been leaving my shoes pointing at the door like a man about to run.)"
    hikari "He'll learn it. He learned the amado."
    father "The amado is a door. The shoes are a person."

    scene bg_home_day with walk_fade
    "In the genkan I take off my shoes, turn them around, and set them side by side."
    "It takes four seconds. It feels like a sentence I have finally learned to say."
    hikari "You turned them around."
    mc "Your dad said."
    hikari "He notices everything. It's exhausting."
    mc "It's useful."
    hikari "Don't tell him that."

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0
    "The morning is warmer than yesterday. The station is full of people pretending not to be hot."
    "Hikari walks beside me this time, not ahead. I do not know when that changed."

    scene bg_station with walk_fade
    "The gate swallows cards and people in the same rhythm."
    "I do not fumble mine. The person behind me does not have to wait."

    scene bg_platform with walk_fade
    "The platform has lines painted on the floor, and everyone stands behind them."
    "Not because of a sign. Because of everyone else."
    "A train comes. The doors open. The people waiting step aside and let the people inside get out first."
    "Then they get on. In order. Without a word."
    hikari "You're watching again."
    mc "I'm learning the rules."
    hikari "There are no rules. There are just a thousand people agreeing."
    mc "(That is the same thing, said in a way that makes it true.)"

    scene bg_train_interior with walk_fade
    "The car is full again. The same silence. The same sleeping man, or a different one who has learned the same trick."
    "A woman in a business suit stands by the door with her eyes closed. She is not asleep. She is resting her face."
    "The announcement comes in Japanese, then in English. The English is slower, as if it is apologizing for being necessary."
    "At the next station, a man in a white glove stands at the edge of the platform and gently pushes the last passengers into the car."
    mc "(He is not pushing. He is folding. The train is a suitcase and the city is packing itself.)"

    menu:
        "Ask about the women-only car.":
            mc "What is the car with the pink sign?"
            hikari "Women-only. Mornings. It is not a suggestion."
            hikari "It exists because some men cannot be trusted on a crowded train. That is the whole reason."
            mc "(She says it without softening it. The train goes on being quiet.)"
            $ reward_attributes_once("day9_train_women", [("insight", "micro")], show="auto")
        "Ask about the man with the white gloves.":
            mc "What is the man with the gloves doing?"
            hikari "Oshiya. The pusher. He makes the train fit."
            mc "That's a job?"
            hikari "It's a job. It's a very polite job. He apologizes while he does it."
            mc "(I watch him bow to the people he has just folded into a train. They bow back. Nobody is angry.)"
            $ reward_attributes_once("day9_train_pusher", [("nerve", "micro")], show="auto")
        "Count the station announcements until we arrive.":
            "I count them. Nine stations. Nine names I cannot pronounce yet."
            "At the seventh, I recognize the shape of the word before the English comes."
            mc "(That is one word I own now. It is not much. It is mine.)"
            $ reward_attributes_once("day9_train_count", [("grace", "micro")], show="auto")

    scene black with Fade(1.0, 0.3, 0.0)
    stop music fadeout 1.0
    "We come up near campus into a morning that has already been going for hours without us."

    scene bg_school_gate with Fade(0.0, 0.0, 1.5)
    play music "audio/Music/school.mp3" fadein 1.5
    $ phone_map_visit("school")
    "The guard nods. Hikari peels off toward her building with a wave that does not stop moving."
    "I take the long way around the courtyard, past the vending machines, and I am not late."

    scene bg_campus_interior with walk_fade
    "The corridor smells like floor wax and rain that has not happened yet."

    scene bg_lecture_hall with walk_fade
    play music "audio/Music/classroom.mp3" fadein 1.0

    "The professor has written a date on the board. 1008. Then a name: 紫式部."
    professor "Murasaki Shikibu. The Tale of Genji."
    professor "It is called the world's first novel. That is true, and it is also a way of not saying what it is."
    professor "It is a book about a man who is beautiful and cannot stop hurting people. It is a book about a court that is dying and does not know it."
    professor "It is also a book about the weather."
    "Somebody laughs. The professor waits."
    professor "In the Heian court, the weather was not small talk. It was the whole emotional vocabulary. You could not say I am sad. You said the rain has been falling since morning."
    professor "The book is a thousand pages of people saying the rain has been falling since morning."
    mc "(I write: the weather is the feeling. The feeling is the weather.)"
    professor "This is mono no aware again. The pathos of things. The beauty of what passes."
    professor "Genji is beautiful because he is passing. The court is beautiful because it is passing. The book knows this before any of the characters do."
    professor "The first line is: In a certain reign. Not which reign. A certain one. The book begins by forgetting the exact date, because the exact date is not the point."

    menu:
        "Ask why a woman wrote the first novel.":
            mc "Why a woman? Why not one of the court men?"
            professor "Because the men were writing in Chinese. The serious language. The official language."
            professor "Murasaki wrote in Japanese. In kana. The language of letters and poems and gossip."
            professor "The novel was born in the language the men had decided was not serious."
            mc "(That is either an accident of history or the best joke in it.)"
            $ reward_attributes_once("day9_class_woman", [("insight", "micro")], show="auto")
        "Ask whether Genji is a good person.":
            mc "Is Genji a good person?"
            professor "No."
            mc "Then why is the book about him?"
            professor "Because the book is not about whether he is good. It is about what his beauty costs everyone around him."
            professor "A novel is not a trial. It does not need a verdict. It needs a witness."
            mc "(I write that down. It feels like a rule for something larger than a book.)"
            $ reward_attributes_once("day9_class_genji", [("nerve", "micro")], show="auto")
        "Write the first line in the margin.":
            "I write it in the margin of my notebook: In a certain reign."
            "The characters are still clumsy. The professor walks past and does not correct them."
            mc "(A certain reign. A certain city. A certain me.)"
            $ reward_attributes_once("day9_class_line", [("grace", "micro")], show="auto")

    professor "Read the first chapter. Bring one sentence you do not understand. That is the assignment."
    "The bell goes. The room folds itself up."

    scene bg_campus_interior with walk_fade
    "Hikari has seminar until five. The afternoon is a door with nothing written on it."
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

    father "And the book?"
    mc "The Tale of Genji. A thousand pages of weather."
    father "That sounds like a book for the train."
    mc "It is."
    hikari "He's been reading it on the train. In Japanese. Slowly."
    mc "Very slowly."
    father "Slow is how you read a thousand pages."
    "Nobody argues with that. We eat."

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the first chapter of Genji is open on the desk."
    "I have read the same paragraph four times. The words are not the problem. The distance is."
    "A knock at the door. Hikari, with two cups of tea and her own notes under her arm."
    hikari "I'm not staying. I'm just making sure you're not staring at the wall."
    mc "I was staring at Genji."
    hikari "Same thing."
    "She sets the tea down and sits on the floor with her back against the bed."

    menu:
        "Ask her to read the first line aloud.":
            mc "Read the first line. The way you would read it."
            hikari "You want me to perform?"
            mc "I want to hear where the pause goes."
            "She reads it. Her voice changes. The room gets smaller and older."
            hikari "That's the trick. You don't read it like a sentence. You read it like a memory."
            mc "(I do not understand the words. I understand the pause.)"
            $ reward_attributes_once("day9_night_read", [("grace", "micro")], show="auto")
        "Ask her if she likes Genji.":
            mc "Do you like him? Genji."
            hikari "No. Nobody likes Genji. That's not why you read it."
            mc "Then why?"
            hikari "Because he's beautiful and he ruins things. And the book lets you watch."
            mc "(She says it with the flat certainty of someone who has finished it.)"
            $ reward_attributes_once("day9_night_genji", [("insight", "micro")], show="auto")
        "Tell her I'm afraid I'm not getting it.":
            mc "I'm afraid I'm not getting it. The book. Any of it."
            hikari "You're getting it."
            mc "How do you know?"
            hikari "Because you're afraid of not getting it. That's the whole first step."
            "She does not make it a speech. She just says it and drinks her tea."
            $ reward_attributes_once("day9_night_afraid", [("nerve", "micro")], show="auto")

    "She takes her cup and leaves the door open a hand's width."
    "I listen to her go down the stairs, then the house settle into its night sounds."
    "The book is still open. The tea is still warm."
    "Tomorrow is Friday. The elective fair. Something is going to change."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump friday_morning
