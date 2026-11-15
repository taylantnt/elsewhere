################################################################################
## THE CITY ROWS
################################################################################
##
## The hub used to hold only people. On a day when every confidant is paused or
## closed, that meant a walk or nothing. These rows are the city itself: places
## he can go when he is not visiting someone, each with one small cultural
## moment and one choice that does not have to pay.
##
## They are not confidant arcs. They do not have visit counts and they never
## close, because the city does not leave. The only bookkeeping is
## `last_afternoon_place`, which the evening already reads, plus two small
## flags the combini row can plant: the pudding in the fridge, and the job
## card in the window.

default combini_gift = False
default combini_poster_seen = False
# Tanaka is the combini cashier. `tanaka_met` is the first counter scene,
# `combini_job_unlocked` is the HELP WANTED card, and `tanaka_story` counts the
# teaching shifts (0-7, one per visit file in `game/job_combini/`).
# `combini_shifts` counts every shift, including the repeats after visit 7.
default tanaka_met = False
default combini_job_unlocked = False
default tanaka_story = 0
default combini_shifts = 0

label city_row_library:
    scene bg_library with walk_fade
    play music "audio/SFX/library_ambiance.mp3" fadein 1.5
    "The campus library is the one building that does not care who I am."
    "No one looks up when I come in. No one asks if I need help. The silence is not personal."
    "I find a table by the window and put the midterm notes down."
    mc "(Two weeks. If I read one page at a time, it is only a stack of pages.)"

    menu:
        "Read until the words stop moving.":
            "I read the same paragraph four times. On the fifth, it opens."
            "The sentences are not friendly, but they are not hiding either."
            mc "(This is what studying is. Not understanding, and then understanding.)"
            $ reward_attributes_once("city_library_focus", [("insight", "micro")], show="auto")
        "Help the student beside me find a book.":
            "The student beside me has been staring at the same shelf for ten minutes."
            "I point at the spine she keeps passing. She blinks, takes it, and bows too fast."
            mc "(A small thing. It still counts as a thing.)"
            $ reward_attributes_once("city_library_help", [("grace", "micro")], show="auto")
        "Close the notes and watch the room.":
            "I close the notes. The room is full of people doing the same thing I am, badly and then better."
            mc "(Nobody here is a genius. We are all just early.)"
            $ reward_attributes_once("city_library_watch", [("nerve", "micro")], show="auto")

    stop music fadeout 1.5
    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label city_row_river:
    scene bg_river_dusk with walk_fade
    "The river at this hour is the color of a coin that has been in a pocket too long."
    "A man is fishing without a bucket. A woman is running with a phone strapped to her arm. The trains go over the water and do not stop."
    mc "(Nobody comes here to be seen. That is why it works.)"

    menu:
        "Skip stones until one goes all the way across.":
            "The first three sink. The fourth skips twice. The fifth goes almost to the other bank."
            "An old man on the bench says something I do not catch, then nods."
            mc "(I think that was approval. I am going to count it as approval.)"
            $ reward_attributes_once("city_river_stones", [("nerve", "micro")], show="auto")
        "Sit and watch the light go.":
            "I sit on the bank. The light goes orange, then grey, then the streetlights come on one by one."
            "Nothing happens. It is the best nothing I have had all week."
            $ reward_attributes_once("city_river_watch", [("insight", "micro")], show="auto")
        "Call Hikari and tell her where I am.":
            "I call her. She picks up on the second ring."
            hikari "You're at the river."
            mc "How do you know?"
            hikari "You get a voice when you're near water."
            mc "I'm coming home soon."
            hikari "Good. Walk slow."
            mc "(She does not ask why I called. She just answers.)"
            $ reward_attributes_once("city_river_call", [("grace", "micro")], show="auto")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label city_row_harajuku:
    scene bg_harajuku with walk_fade
    "Takeshita Street is a river of people dressed like they are all going to different parties."
    "A girl in platform boots argues with a boy in a school uniform. A tourist photographs a crepe like it is a monument."
    mc "(In Akihabara I was invisible. Here I am visible and nobody cares. It is a different kind of invisible.)"

    menu:
        "Try on something I would never wear.":
            "I let the shop assistant put a jacket on me. It is too bright and too short and it fits perfectly."
            "She says something in fast Japanese. I understand one word: cool."
            mc "(I do not buy it. I wear it for one more minute.)"
            $ reward_attributes_once("city_harajuku_try", [("nerve", "micro")], show="auto")
        "Buy nothing and watch the street.":
            "I walk the whole street without buying anything. It takes twenty minutes."
            "Nobody stops me. Nobody asks what I am doing. The street is a performance and I am allowed to be audience."
            $ reward_attributes_once("city_harajuku_watch", [("insight", "micro")], show="auto")
        "Ask a stranger where the good crepe place is.":
            "The stranger thinks about it seriously, then points at a shop with no sign and a line around the corner."
            "The crepe is too sweet. The line was right."
            $ reward_attributes_once("city_harajuku_ask", [("grace", "micro")], show="auto")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label city_row_karaoke:
    scene bg_karaoke_room with walk_fade
    "The karaoke box is a small room with a big screen and a machine that does not judge."
    "I am alone. The room is built for six. That is the first thing I notice."
    mc "(One hour. Nobody knows I am here. That is either freedom or the beginning of a bad habit.)"

    menu:
        "Sing the first song badly.":
            "I pick a song I know from the airport playlist. I do not know the words. I sing them anyway."
            "The machine gives me a score. I am not going to say what it was."
            mc "(The room does not laugh. The room has heard worse.)"
            $ reward_attributes_once("city_karaoke_sing", [("nerve", "micro")], show="auto")
        "Pick a song Hikari would hate.":
            "I pick the most sentimental song on the list and sing it straight."
            "Halfway through I can hear her voice in my head: you are enjoying this too much."
            mc "(I am. That is the point.)"
            $ reward_attributes_once("city_karaoke_hikari", [("grace", "micro")], show="auto")
        "Sit and listen to the room next door.":
            "The room next door is singing something old and slow. Through the wall it sounds like a hymn."
            "I let the timer run down without singing anything."
            mc "(One hour of not performing. It counts.)"
            $ reward_attributes_once("city_karaoke_listen", [("insight", "micro")], show="auto")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label city_row_night_market:
    scene bg_nightfood with walk_fade
    "The food stalls under the tracks are lit like a small city that only exists after eight."
    "A man is turning skewers over a grill. A woman is ladling something into bowls without looking at the bowls."
    "Everyone is eating standing up. Nobody is on their phone."

    menu:
        "Order the thing I can't name.":
            "I point at what the man in front of me is eating. The cook nods and puts one in front of me."
            "It is hot and salty and I do not know what it is. I eat all of it."
            $ reward_attributes_once("city_market_order", [("nerve", "micro")], show="auto")
        "Watch the cook work.":
            "The cook does four things at once and never hurries. The skewers turn when they need to turn."
            mc "(This is what mastery looks like when nobody is watching. It looks like lunch.)"
            $ reward_attributes_once("city_market_watch", [("insight", "micro")], show="auto")
        "Pay for the next person's bowl.":
            "I put the money down before the student behind me can. He starts to argue. The cook takes the money and hands him the bowl."
            "The student bows. I bow back. The cook goes back to the grill."
            $ reward_attributes_once("city_market_pay", [("grace", "micro")], show="auto")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label city_row_combini:
    scene bg_alley_night with walk_fade
    play music "audio/Music/kombini.mp3" fadein 1.0
    "The combini sits at the end of the alley like a lit aquarium. Same temperature, same brightness, at any hour, in any weather."
    "The door chimes twice going in and once going out, and nobody has ever explained why."
    play sound "audio/SFX/combini.mp3"

    if not tanaka_met:
        call combini_first_counter
    else:
        scene bg_combini with walk_fade
        "The door chimes twice going in. Tanaka is at the register, doing three things at once."
        mc "(Pens. A notebook with a grid. Coffee in a can, because the can is part of the experience.)"

        menu:
            "Buy the midterm supplies.":
                "Pens, erasers, a notebook with a grid, and one of the clear folders that makes any paper look official."
                $ spend_money(300)
                mc "(Studying is cheaper than I feared. It is the time that costs.)"
                $ reward_attributes_once("city_combini_supplies", [("insight", "micro")], show="auto")
            "Buy the egg sandwich and the bear pudding.":
                "The egg sandwich is the one Hikari pretends not to like. The pudding has a cartoon bear on the lid and no reason to be good."
                $ spend_money(540)
                "I put them in the fridge when I get home and write nothing on the bag."
                mc "(The bag says enough.)"
                $ combini_gift = True
                $ reward_attributes_once("city_combini_gift", [("grace", "micro")], show="auto")
            "Talk to Tanaka at the register.":
                "I put a can of coffee on the counter. Tanaka scans it without looking at me."
                tanaka "いらっしゃいませ。"
                mc "You say that to everyone."
                tanaka "That is the job."
                mc "Do you mean it?"
                tanaka "I mean that you are welcome in the store. That is not the same as being welcome in my day."
                mc "(He says it flatly. It is not cruel. It is a boundary with a barcode.)"
                if tanaka_story >= 3:
                    tanaka "You are still here."
                    mc "I work here."
                    tanaka "That is what I mean."
                $ reward_attributes_once("city_combini_talk", [("grace", "micro")], show="auto")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label combini_first_counter:
    scene bg_combini with walk_fade
    play music "audio/Music/kombini.mp3" fadein 1.0

    "The inside of a Japanese convenience store is a small, air-conditioned country with its own rules."
    "The shelves are arranged by season, not by category. The hot snacks are near the register. The cold drinks are at the back. The magazines are by the window, where the light is best."
    "A machine by the door makes coffee one cup at a time. A small printer hums beside it. The bathroom sign has a picture of a western toilet and a Japanese one, because both are options."
    mc "(It is not a shop. It is a machine for living, broken into aisles.)"

    "At the register, a man in a striped shirt and a name tag that says たなか is doing three things at once."
    "He scans a bento with one hand, bags it with the other, and answers a question from a customer without looking up."
    "He is not friendly. He is not unfriendly. He is efficient in a way that feels personal."
    "He looks like someone I have met. The resemblance is not exact. It is the way he holds his face, like a door that has been closed for a long time."

    "I put a hot snack on the counter. I have not decided which one yet. The case has three shelves and each shelf smells better than the last."
    menu:
        "The fried chicken.":
            "I point at the paper basket of karaage. The batter is the color of a good afternoon."
            $ reward_attributes_once("combini_first_karaage", [("nerve", "micro")], show="auto")
        "The steamed bun.":
            "I point at the nikuman. It is round and white and sits in its paper cradle like something asleep."
            $ reward_attributes_once("combini_first_nikuman", [("grace", "micro")], show="auto")
        "The oden.":
            "I point at the oden case. Daikon, egg, a fish cake shaped like a knot. The broth is clear and smells of the sea."
            $ reward_attributes_once("combini_first_oden", [("insight", "micro")], show="auto")

    tanaka "いらっしゃいませ。"
    mc "...Hi."
    "He picks up the snack and holds it over the warmer."
    tanaka "温めますか。"
    mc "...Sorry?"
    tanaka "Heat. Yes or no."
    mc "Yes. Please."
    "He puts it in the warmer and presses a button. Then he looks at me. The questions begin."
    tanaka "フォークは。"
    mc "(Fork?)"
    tanaka "スプーンは。"
    mc "(Spoon?)"
    tanaka "お箸は。"
    mc "(Chopsticks?)"
    mc "Chopsticks. No fork. No spoon."
    tanaka "ポイントカードは。"
    mc "(Point card?)"
    mc "No. I don't have one."
    tanaka "お支払いは。現金？IC？"
    mc "(Cash or IC?)"
    mc "IC."
    tanaka "クーポンは。"
    mc "(Coupon?)"
    mc "No."
    tanaka "袋は。5円。"
    mc "(A bag. Five yen.)"
    mc "No bag. I have one."
    "He nods once. He scans my card. He puts the snack in front of me. The whole thing has taken less than a minute."
    tanaka "Good."
    mc "That was a lot of questions."
    tanaka "It is the script."
    mc "The script?"
    tanaka "Every customer gets the same questions in the same order. If I skip one, they think I am rude. If I say all of them, they think I am efficient."
    tanaka "Both are true."
    mc "(He says it like a man who has thought about it more than the job requires.)"
    mc "Do you like it? The script?"
    tanaka "I like that it ends. Every conversation here has a receipt."
    "He tears the receipt and puts it in my hand. For a second the fluorescent light makes his face the doctor's face. Then it is just a tired man in a striped shirt."

    $ tanaka_met = True
    $ combini_poster_seen = True
    $ combini_job_unlocked = True

    "I take the snack and go outside. The door chimes once going out."
    "I look back through the glass. A handwritten card is taped to the window at eye height."
    "Evenings. Two shifts. Ask for the manager."
    mc "(No Japanese conversation needed beyond what just happened. I can do what just happened.)"
    mc "(I can be a person the store recognizes.)"
    return


## The night shift lives in `game/job_combini/`: one label per teaching shift
## (`tanaka_visit_01` ... `tanaka_visit_07`), dispatched by `tanaka_shift` from
## `tanaka_story`. This row only opens the door.


label confidant_visit_fortune:
    scene bg_fortune_stall with walk_fade
    "I take the train back to Asakusa. The afternoon is already going orange. The crowd is thinner than it was yesterday."
    "She is at the same folding table, between the incense burner and the souvenir stalls. She does not look surprised."
    fortune_teller "You came back."
    mc "You said the cards would change."
    fortune_teller "I said you would change them. The cards are only paper."
    "She lays two cards face down. There is no third card on the table."
    fortune_teller "The first card is a street. The second is a corner. The third is already in your pocket."
    mc "The omikuji."
    fortune_teller "The paper remembers what the hand forgets."
    "She turns over the first card. A narrow street with crepe stands and vintage shops. The crowd is a river of color."
    fortune_teller "Harajuku. You will walk it and forget why. That is not a warning. It is what the street is for."
    mc "And the second?"
    "She turns over the second card. A street corner at night. A streetlight. A house that looks like every other house."
    fortune_teller "The corner near your house. You will see me there. I will not have a table."
    mc "What will you have?"
    fortune_teller "The last thing I am allowed to give you."
    "She puts the cards away. She does not offer a third question. She does not offer a price."
    fortune_teller "One true thing, and two pieces of noise. That is the rule."
    mc "Which is which?"
    fortune_teller "If I told you, it would be three true things. That is not the rule."
    "She looks at me for a long moment. The smoke from the burner drifts between us."
    fortune_teller "The person who put you here is not the person you think."
    fortune_teller "Beware of vending machines that do not take coins."
    fortune_teller "The cat on the wall is not a cat."
    mc "(One of those is true. I do not know which. I think I do. I hope I am wrong.)"
    "She folds the table. This time I watch her hands. They are ordinary hands. They are not doing anything unusual."
    fortune_teller "That is all three. The deck is closed."
    mc "Will I see you again?"
    fortune_teller "You will see me on the corner. That is not the same as seeing me again."
    "She walks into the crowd. The table is gone. The brass bowl is gone. There is only the smoke and the sound of the temple."
    $ confidant_visits["fortune"] = max(confidant_visits.get("fortune", 0), 3)
    $ remember("hikari", "went back to the fortune teller alone and was told the deck was closed")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label city_row_odaiba:
    scene bg_odaiba with walk_fade
    "Odaiba is an island that was built to be the future and then had to live in it."
    "The streets are too wide. The buildings are the right height and the right color. The water is on three sides, like a moat that got out."
    "A giant white statue stands over the plaza with one hand raised. It is a robot. It is also a monument to a cartoon. The country is not one thing."
    mc "(It is too clean. Not empty-clean. Planned-clean. The streets curve the way streets curve in a drawing.)"

    menu:
        "Take the photo everyone takes.":
            "I stand where everyone stands and take the photo everyone takes. The statue fills the frame. A family waits behind me."
            "When I look at the photo later, the statue is looking somewhere else."
            mc "(It is a statue. It is looking exactly where it is built to look.)"
            $ reward_attributes_once("city_odaiba_photo", [("insight", "micro")], show="auto")
        "Eat at the conveyor-belt sushi place.":
            "The plates come at me on a belt, color-coded by price. I take what looks good and stack the plates."
            $ spend_money(1400)
            "The staff counts the stack at the end without judgment. The system is effortless."
            mc "(I feel like I have been eating this way my whole life. That is a strange thing to feel after one visit.)"
            $ reward_attributes_once("city_odaiba_sushi", [("nerve", "micro")], show="auto")
        "Sit on the beach and look at the city.":
            "I sit on the fake beach and look across the bay. The city is a line of light on the other side."
            "A couple is taking wedding photos. A child is burying a shoe. The water goes flat for a second, like a texture that has not loaded."
            "Then it is water again."
            mc "(I do not tell anyone. There is no one to tell.)"
            $ reward_attributes_once("city_odaiba_beach", [("grace", "micro")], show="auto")

    "On the way out, the statue blinks. Once. For a frame."
    "I blink too. When I open my eyes, the statue is the same."
    mc "(It is a statue. It does not blink. I do not mention it to anyone.)"

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label city_row_yokohama:
    scene bg_yokohama with walk_fade
    "Chinatown is ten minutes from the station and a hundred years from the rest of the city."
    "Red lanterns. Gates with Chinese characters. Shops selling steamed buns and lucky cats and things made of sugar."
    "A woman asks me something in Chinese. I answer in Japanese. She laughs and switches to Japanese, then to English, then back."
    mc "(I am the foreigner in a place built by foreigners. It is a different kind of foreign.)"

    menu:
        "Follow the smell of the steamed buns.":
            "I follow the smell to a shop with a line and no sign in English. The bun is hot and sweet and the size of my fist."
            $ spend_money(500)
            "An old man beside me eats his in four bites. I take six. He watches me with the patience of a man who has seen worse."
            mc "(The bun is not a meal. It is a hand warmer you can eat.)"
            $ reward_attributes_once("city_yokohama_bun", [("grace", "micro")], show="auto")
        "Ask a shopkeeper how long they have been here.":
            "The shopkeeper has been here for thirty years. Her parents came from Fujian. She was born in Yokohama."
            mc "So you are Japanese."
            "She thinks about it. Then she says: I am from here. That is a different sentence."
            mc "(It is. I write it down in my head.)"
            $ reward_attributes_once("city_yokohama_ask", [("insight", "micro")], show="auto")
        "Get lost in the side streets.":
            "I turn off the main street and the crowd disappears. The alleys are narrow and quiet. A cat sleeps on a stack of crates."
            "I am lost for twenty minutes. Nobody asks what I am doing. That is the luxury of a place that is used to visitors."
            $ reward_attributes_once("city_yokohama_lost", [("nerve", "micro")], show="auto")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label city_row_ueno:
    scene bg_ueno with walk_fade
    "Ueno Park in April is a picnic that the whole city has agreed to attend."
    "Blue tarps. Cardboard. Salarymen in suits sitting on the ground with their ties loosened. A group of old men with a bottle and a radio."
    "The blossoms are already falling. The ground is pink in the places where people have not walked."
    mc "(Hanami. The flowers are an excuse. The sitting is the point.)"

    menu:
        "Sit under the blossoms and watch.":
            "I find a patch of grass and sit. Nobody asks me to move. A man nearby is asleep with his mouth open. His friend is taking a photo."
            "The petals come down slowly, like the park is being paid in small coins."
            $ reward_attributes_once("city_ueno_watch", [("insight", "micro")], show="auto")
        "Accept the cup from the old men.":
            "One of the old men holds up a paper cup and says something I do not catch. The others make room."
            "The sake is warm and terrible. I drink it. They laugh and pour another."
            mc "(I do not understand half of what they say. I understand all of it.)"
            $ reward_attributes_once("city_ueno_cup", [("nerve", "micro")], show="auto")
        "Walk to the museum and don't go in.":
            "I walk to the museum steps and stop. The building is huge and quiet. The people going in have the faces of people who have decided to learn something."
            "I sit on the steps instead. A guard watches me and decides I am harmless."
            mc "(Sometimes the building is enough. Sometimes the deciding is the thing.)"
            $ reward_attributes_once("city_ueno_museum", [("grace", "micro")], show="auto")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label city_row_shibuya:
    scene bg_shibuya with walk_fade
    "Shibuya Crossing is not a crossing. It is a performance that happens every two minutes."
    "The screens above are all selling something. The crowd below is all going somewhere. The two things have nothing to do with each other."
    "When the light changes, a thousand people walk into each other and nobody touches."
    mc "(It is the most crowded place I have ever stood in. It is also the most alone.)"

    menu:
        "Cross with the crowd.":
            "I step off the curb with everyone else. For thirty seconds I am not a person. I am a direction."
            "On the other side, the crowd breaks apart and everyone becomes a person again."
            mc "(That is the trick. You do not cross the crossing. The crossing crosses you.)"
            $ reward_attributes_once("city_shibuya_cross", [("nerve", "micro")], show="auto")
        "Watch the crossing from above.":
            "I find a window on the second floor and look down. The crossing opens and closes like a flower. The same people, the same directions, the same two minutes."
            "A man in the crowd stops in the middle. Everyone flows around him. Then the light changes and he is carried away."
            $ reward_attributes_once("city_shibuya_watch", [("insight", "micro")], show="auto")
        "Find the Hachikō statue and wait.":
            "The statue is smaller than I expected. A dog, sitting, waiting. People take photos with it. A child asks her mother why the dog is famous."
            "The mother says: because he waited."
            "I wait with him for a while. Nobody asks me what I am waiting for."
            $ reward_attributes_once("city_shibuya_hachiko", [("grace", "micro")], show="auto")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label city_row_shimokitazawa:
    scene bg_shimokitazawa with walk_fade
    "Shimokitazawa is what Harajuku would be if it stopped performing."
    "Narrow streets. Vintage shops. A live house with a hand-painted sign and a door that looks like a fridge."
    "Nobody is dressed for a photograph. Everybody is dressed for themselves, which is a different kind of effort."
    mc "(It is small. It is slow. It is the first place in this city that has felt like a neighborhood.)"

    menu:
        "Buy a used record.":
            "The record shop is the size of a closet and smells of cardboard. I flip through the stacks until I find something with a cover I like."
            $ spend_money(1200)
            "The owner puts it in a paper sleeve and says something about the band. I nod. I will look them up later."
            mc "(I do not have a record player. That is a problem for future me.)"
            $ reward_attributes_once("city_shimokita_record", [("insight", "micro")], show="auto")
        "Go into a live house.":
            "The band is loud and the room is small and the ceiling is low. Nobody is filming. Everybody is listening."
            $ spend_money(1500)
            "The singer says something between songs that makes the room laugh. I do not catch it. I laugh anyway."
            mc "(For one hour I am not a foreigner. I am a person in a room with a band.)"
            $ reward_attributes_once("city_shimokita_live", [("nerve", "micro")], show="auto")
        "Sit in a coffee shop and listen.":
            "The coffee shop has six seats and one table. The owner makes each cup by hand. The radio is playing something old."
            "Two women at the next table are talking about a friend who moved to Osaka. A man is reading a book with a cracked spine."
            mc "(Nobody is in a hurry. Nobody is taking a photo. This is what a Tuesday feels like when it is allowed to be a Tuesday.)"
            $ reward_attributes_once("city_shimokita_coffee", [("grace", "micro")], show="auto")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label city_row_omotesando:
    scene bg_omotesando with walk_fade
    "Omotesando is a street built to look like a forest and priced like a museum."
    "The shops are glass and concrete and very polite. The trees are tall enough to make the buildings feel humble."
    "Then the shops end and the torii begins. The city gets quiet all at once."
    mc "(The same street. Two countries. The border is a gate.)"

    menu:
        "Purify at the temizuya.":
            "The temizuya is a stone basin with wooden ladles. A sign shows the order: left hand, right hand, mouth, handle."
            "I do it slowly. The water is cold. An old woman beside me does it in four seconds and walks on."
            mc "(I do not know if I did it right. I know I did it.)"
            $ reward_attributes_once("city_omotesando_temizu", [("grace", "micro")], show="auto")
        "Walk the gravel path and listen.":
            "The path to the shrine is gravel and trees. Every step makes a sound. The sound is the point."
            "The city disappears behind the trees. A crow calls once. Then nothing."
            mc "(I can hear my own feet. I have not heard my own feet in two weeks.)"
            $ reward_attributes_once("city_omotesando_gravel", [("insight", "micro")], show="auto")
        "Write a wish on an ema.":
            "The ema are wooden plaques with a hole and a string. I buy one and write on it."
            "I do not write a wish. I write a question. Then I hang it with the others."
            $ spend_money(500)
            mc "(A wall of strangers' questions, hanging in the rain. It is the most honest thing I have seen here.)"
            $ reward_attributes_once("city_omotesando_ema", [("nerve", "micro")], show="auto")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return
