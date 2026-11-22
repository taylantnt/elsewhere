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
        "Skip a stone at the swan and watch it miss.":
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
    $ phone_map_visit("harajuku")
    play music "audio/Music/harajuku.mp3" fadein 2.0
    scene bg_harajuku with walk_fade
    "Takeshita Street is a river of people dressed like they are all going to different parties."
    "A girl in platform boots argues with a boy in a school uniform. A tourist photographs a crepe like it is a monument."
    "I am alone this time. Hikari's rules are in my head anyway: look with your eyes, buy nothing at the first two shops, never laugh."
    mc "(In Akihabara I was invisible. Here I am visible and nobody cares. It is a different kind of invisible.)"

    menu:
        "Try on something I would never wear.":
            "I let the shop assistant put a jacket on me. It is too bright and too short and it fits perfectly."
            "She says something in fast Japanese. I understand one word: 可愛い."
            mc "(I do not buy it. I wear it for one more minute.)"
            $ reward_attributes_once("city_harajuku_try", [("nerve", "micro")], show="auto")
        "Buy nothing and watch the street.":
            "I walk the whole street without buying anything. It takes twenty minutes."
            "Nobody stops me. Nobody asks what I am doing. The street is a performance and I am allowed to be audience."
            "I work out that this is what Hikari meant by participating."
            $ reward_attributes_once("city_harajuku_watch", [("insight", "micro")], show="auto")
        "Ask a stranger where the good crepe place is.":
            "The stranger thinks about it seriously, then points at a shop with no sign and a line around the corner."
            "The crepe is too sweet. The line was right."
            $ reward_attributes_once("city_harajuku_ask", [("grace", "micro")], show="auto")
        "Let someone photograph me.":
            "A girl with pink hair raises her phone and asks with her eyes. I say yes before I can talk myself out of it."
            "She shows me the picture. I am smiling and I do not remember deciding to."
            mc "(Being seen turns out to be easier when somebody else is holding the camera.)"
            $ reward_attributes_once("city_harajuku_photo", [("nerve", "micro")], show="auto")

    scene bg_harajuku_clothes with walk_fade
    "The third shop is the one Hikari told me to wait for. It is narrower than the others and the clothes look like somebody actually lives in them."
    "A skirt is hung over a pair of trousers. Socks go over boots. One colour is fighting all the others and losing beautifully."

    menu:
        "Ask the assistant to explain an outfit.":
            "She turns the mannequin a quarter turn and points, saying the words slowly so I can follow."
            "Short over long. Loose over tight. One thing that should not work."
            mc "(She is not selling me anything. She is explaining a sentence.)"
            $ reward_attributes_once("city_harajuku_outfit", [("insight", "micro")], show="auto")
        "Buy something small.":
            "I buy a pair of socks with cats on them. They are the most impractical thing I own."
            "The assistant wraps them in paper and says something that sounds like a blessing."
            $ reward_attributes_once("city_harajuku_buy", [("grace", "micro")], show="auto")

    scene bg_harajuku_candy with walk_fade
    "The cotton candy shop is still a wall of impossible colour. I get a pink one shaped like a flower, because Hikari would have got the blue heart and somebody has to try the other one."
    "It is too sweet. I eat all of it."
    mc "(I came here to see a street. I am leaving with sugar on my fingers and a photograph of myself smiling.)"

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label city_row_karaoke:
    $ phone_map_visit("karaoke")
    scene bg_karaoke_outside with walk_fade
    "The cat over the door is still wearing its red bib. I go past it without stopping this time."
    "I know where the drink bar is. I know which corridor is least likely to have somebody practising the same two lines."
    mc "(The first time, Hikari showed me the shape of this place. This time I have a room booked for one.)"

    scene bg_karaoke_drink with walk_fade
    "I get water first. That part I learned."
    "Then I stand in front of the soft-serve machine for a full minute, which is a decision I do not need to make."

    scene bg_karaoke_room with walk_fade
    "The room is built for six. It is very good at pretending I am not alone in it."
    "On the tablet I switch the language to English, then switch it back. I leave it in Japanese."
    "There is a setting for ローマ字, roumaji. The lyrics come up in roman letters, which I can read almost as fast as I can sing them."
    mc "(Almost being the important word.)"

    menu:
        "Pick a Japanese song in roumaji.":
            mc "This one. I can read the letters, which is not the same as knowing the words."
            "I add it. The first line comes up in neat roman letters. I sing them exactly as written, with the confidence of somebody who does not understand what he is saying."
            "I am terrible. The machine gives me a score. I am not going to say what it was."
            mc "(But I finished the song. That is mine.)"
            $ reward_attributes_once("city_karaoke_romaji", [("nerve", "micro")], show="auto")
        "Sing the airport song with words I made up.":
            "I pick the English song I know from the airport playlist. I do not know all the words. I sing them anyway."
            "The room does not laugh. The room has heard worse."
            $ reward_attributes_once("city_karaoke_sing", [("nerve", "micro")], show="auto")
        "Listen to the room next door first.":
            "The room next door is singing something old and slow. Through the wall it sounds like a hymn."
            "I wait until they finish. Then I take the cheering stick and hit the table once, softly, for nobody in particular."
            mc "(That is for my own singing. She would understand.)"
            $ reward_attributes_once("city_karaoke_listen", [("insight", "micro")], show="auto")

    "I try a second song. This is the one where roumaji stops being a crutch and starts being a trap: the letters run together at speed and I am chasing them."
    "Somewhere in the second verse I stop reading and just make the sounds. It is not the song. It is close enough to the song."
    mc "(Hikari said you get it by singing until one day you do it without thinking. I am not there. I am somewhere before there.)"

    menu:
        "Try the chorus again.":
            "I queue the same song a second time. The second chorus is better than the first. The third is almost a song."
            mc "(Somebody in the next room is going to hear this and think a person is learning something in here. They would be right.)"
            $ reward_attributes_once("city_karaoke_again", [("nerve", "micro")], show="auto")
        "Read the room from the corridor.":
            "On the way back to the bar I stand outside a room for ten seconds and listen."
            "A group, laughing, halfway through a chorus they all know. Somebody off-key and entirely committed."
            mc "(I can tell what this room is doing. I told her I could not. I can.)"
            $ reward_attributes_once("city_karaoke_read_room", [("insight", "micro")], show="auto")
        "Leave a song in the queue for next time.":
            "Before I go I add one more song. It is the one she sang in the room with me, the one I said I did not know."
            "I do not queue it for myself. I queue it for the next time somebody is in here with me."
            $ reward_attributes_once("city_karaoke_queue", [("grace", "micro")], show="auto")

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
        call combini_first_counter from _call_combini_first_counter
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
                "He switches to English for this part, which he almost never does."
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
    # The combini has its own introduction: the first counter visit on Day 8.
    # Unlock its city row here so the hub opens it up without waiting for a
    # Hikari tour (combini is not one of her tour destinations).
    $ unlock_hikari_tour_destination("combini")

    "I take the snack and go outside. The door chimes once going out."
    "I look back through the glass. A handwritten card is taped to the window at eye height."
    "Afternoons. Two shifts. Ask for the manager."
    mc "(No Japanese conversation needed beyond what just happened. I can do what just happened.)"
    mc "(I can be a person the store recognizes.)"
    return


## The afternoon shift lives in `game/job_combini/`: one label per teaching shift
## (`tanaka_visit_01` ... `tanaka_visit_07`), dispatched by `tanaka_shift` from
## `tanaka_story`. This row only opens the door.


## The Fortune Teller's arc lives in `game/confidant_visits/fortuneteller.rpy`:
## visit 1 was the Day 13 reading in `special_day_13_asakusa.rpy`, and visits 2-7 plus
## the corner epilogue are written there. `confidant_visit_fortune` is the
## dispatcher `free_afternoon` routes to.


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
    $ phone_map_visit("yokohama")
    play music "audio/Music/chinese_restaurant.mp3" fadein 2.0
    scene bg_yokohama with walk_fade
    "Chinatown is ten minutes from the station and a hundred years from the rest of the city."
    "Red lanterns. Gates with Chinese characters. Shops selling steamed buns and lucky cats and things made of sugar."
    "A woman asks me something in Chinese. I answer in Japanese. She laughs and switches to Japanese, then to English, then back."
    mc "(I am the foreigner in a place built by foreigners. It is a different kind of foreign.)"
    mc "(Hikari showed me the shape of this place. Today I get to walk it without her.)"

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
        "Go back to the little gyoza shop.":
            scene bg_gyoza_shop with walk_fade
            "The curtain is the colour of old tea. I push it aside and the room shouts at me in Chinese."
            "Lei Lei looks up from the steamer. She looks at me, then at the empty stool I took last time."
            $ lei_mood = "shout"
            lei "また来たのか。"
            mc "(She remembers me. I do not know whether that is good.)"
            $ lei_mood = "normal"
            lei "餃子。"
            "It is not a question. I sit."
            scene bg_gyoza_dishes with walk_fade
            "The gyoza are crisp and hot and taste exactly the way I remember."
            mc "(Hikari was right. The gyoza is hers.)"
            $ spend_money(800)
            $ reward_attributes_once("city_yokohama_leilei", [("grace", "micro")], show="auto")

    "Later, the crowd thins and the street opens toward the water."

    stop music fadeout 1.5
    scene bg_yokohama_akarenga with walk_fade
    "The red brick warehouses stand along the waterfront, long and low and lit at the windows. The Ferris wheel turns behind them, slow enough to look patient."
    "I remember Hikari telling me these buildings survived the earthquake because they were built to hold weight."
    mc "(She said a lot of things today. I think I was supposed to remember which ones.)"

    menu:
        "Walk the waterfront.":
            "I walk until the water is on three sides and the city is a line of light across the bay."
            "A couple takes photographs of each other and nobody else is in frame. I keep walking."
            $ reward_attributes_once("city_yokohama_waterfront", [("grace", "micro")], show="auto")
        "Find the step she showed me.":
            "I find the narrow staircase at the end of the building and climb it. The whole harbor is below me."
            mc "(She would have said no if I had asked. I did not ask.)"
            $ reward_attributes_once("city_yokohama_stairs", [("nerve", "micro")], show="auto")
        "Just stand and look at the bricks.":
            "I stand close enough to see the mortar. The bricks are older than the country I came from."
            mc "(The cargo changed. The building did not. I think that was her point.)"
            $ reward_attributes_once("city_yokohama_bricks", [("insight", "micro")], show="auto")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label city_row_ueno:
    $ phone_map_visit("ueno")
    scene bg_ueno with walk_fade
    if store.story_day >= 24:
        "Ueno Park in May is a picnic that the whole city has agreed to attend."
        "Blue tarps. Cardboard. Salarymen in suits sitting on the ground with their ties loosened. A group of old men with a bottle and a radio."
        "The blossoms are gone. The trees are green and heavy, and the tarps are out anyway."
    else:
        "Ueno Park in April is a picnic that the whole city has agreed to attend."
        "Blue tarps. Cardboard. Salarymen in suits sitting on the ground with their ties loosened. A group of old men with a bottle and a radio."
        "The blossoms are already falling. The ground is pink in the places where people have not walked."
    mc "(Hanami. The flowers are an excuse. The sitting is the point.)"
    mc "(I know what to do with a cup now. I know not to photograph the people sleeping. I know the museum is not a door I have to open. Today, maybe I will.)"

    menu:
        "Sit under the trees and watch.":
            "I find a patch of grass and sit. Nobody asks me to move. A man nearby is asleep with his mouth open. This time I do not raise my phone."
            "The light comes down slowly, like the park is being paid in small coins."
            "A week. That is what the flowers get. I think that is why everybody is here."
            $ reward_attributes_once("city_ueno_watch", [("insight", "micro")], show="auto")
        "Accept the cup from the old men.":
            "One of the old men holds up a paper cup. I take it with both hands and say いただきます the way she taught me."
            "The sake is warm and terrible. I drink it. They laugh and pour another."
            mc "(The offer matters more than the answer. I finally know what that means.)"
            $ reward_attributes_once("city_ueno_cup", [("nerve", "micro")], show="auto")
        "Walk to the museum and don't go in.":
            "I walk to the museum steps and stop. The building is huge and quiet. The people going in have the faces of people who have decided to learn something."
            "I sit on the steps instead. A guard watches me and decides I am harmless."
            mc "(Sometimes the building is enough. Sometimes the deciding is the thing.)"
            $ reward_attributes_once("city_ueno_museum", [("grace", "micro")], show="auto")
        "Keep my phone in my pocket all afternoon.":
            "A salaryman asleep with his hat over his face. A group passing a bottle without a word. Two tarps close enough to touch that never touch."
            "I look at all of it and put the phone away again before I can decide to document it."
            mc "(This is one of the few places where none of it has to become a photograph.)"
            $ reward_attributes_once("city_ueno_no_photo", [("nerve", "micro")], show="auto")

    "Nobody crosses the lines between the tarps. I know the rule now, and I keep it without being asked, which is the same as belonging."
    mc "(She said somebody should make reaching easier. I still do not know what she meant. I think about it while the light goes.)"

    "I stay until the light goes. The radio switches to a weather report. Nobody listens to that either."

    scene bg_ueno_museum with walk_fade
    "On the way out I go up the museum steps again. This time I go in."
    "There are ten thousand things inside and I understand almost none of them. I stay for an hour anyway."
    mc "(She said she would explain one of them badly. I am glad she did not come. I want to be bad at this on my own.)"

    menu:
        "Find the east room.":
            "I find the east room. It is quiet and almost empty, exactly as she said."
            "There is a bowl in a case that is older than everything I know. I stand in front of it for a long time."
            mc "(I would not have known to look for this. She told me and I came anyway. That is what she is for.)"
            $ reward_attributes_once("city_ueno_east_room", [("insight", "micro")], show="auto")
        "Buy a postcard and write nothing on it.":
            "I buy a postcard of the museum steps. I do not write on it. I do not know who I would send it to."
            "I put it in my pocket. That is enough of a decision for today."
            $ reward_attributes_once("city_ueno_postcard", [("grace", "micro")], show="auto")
        "Leave before I understand anything.":
            "I walk out after twenty minutes. Understanding can wait."
            "Outside, the park that was a temple is everybody's again."
            $ reward_attributes_once("city_ueno_leave", [("nerve", "micro")], show="auto")

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
        "Find the Hachikou statue and wait.":
            "The statue is smaller than I expected. A dog, sitting, waiting. People take photos with it. A child asks her mother why the dog is famous."
            "The mother says: because he waited."
            "I wait with him for a while. Nobody asks me what I am waiting for."
            $ reward_attributes_once("city_shibuya_hachiko", [("grace", "micro")], show="auto")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label city_row_shimokitazawa:
    $ phone_map_visit("shimokitazawa")
    scene bg_shimokitazawa with walk_fade
    "I take the small gate out of the station. The cat is still in the gap between the bicycle shop and the wall."
    "He looks at me for a long moment and goes back to sleep. I decide that counts as recognition."
    "Narrow streets. Vintage shops. A live house with a hand-painted sign and a door that looks like a fridge."
    "Nobody is dressed for a photograph. Everybody is dressed for themselves, which is a different kind of effort."
    mc "(It is small. It is slow. It is the first place in this city that has felt like a neighborhood.)"

    menu:
        "Buy a used record.":
            scene bg_record_shop with walk_fade
            "The record shop is the size of a closet and smells of cardboard. I go to the third crate, because she said the good things sink."
            "I flip through it and find a sleeve with a band I half-recognize from a train commercial."
            $ spend_money(1200)
            "The owner puts it in a paper sleeve and says something about the band. I nod. I will look them up later."
            mc "(I do not have a record player. That is a problem for future me.)"
            $ reward_attributes_once("city_shimokita_record", [("insight", "micro")], show="auto")
        "Go into a live house.":
            scene bg_live_house with walk_fade
            "I push the steel door. It really is like a fridge, and the bass comes out in a cold wave."
            "The band is loud and the room is small and the ceiling is low. Nobody is filming. Everybody is listening."
            $ spend_money(1500)
            "The singer says something between songs that makes the room laugh. I do not catch it. I laugh anyway."
            mc "(For one hour I am not a foreigner. I am a person in a room with a band.)"
            $ reward_attributes_once("city_shimokita_live", [("nerve", "micro")], show="auto")
        "Sit in a coffee shop and listen.":
            scene bg_shimokita_cafe with walk_fade
            "The coffee shop has six tables and a window onto the alley. The owner makes each cup by hand and does not ask what I want. He remembers the person I came with, not me, which is fine."
            "Two women at the next table are talking about a friend who moved to Osaka. A man is reading a book with a cracked spine."
            mc "(Nobody is in a hurry. Nobody is taking a photo. This is what a Tuesday feels like when it is allowed to be a Tuesday.)"
            $ reward_attributes_once("city_shimokita_coffee", [("grace", "micro")], show="auto")
        "Walk the little theaters without going in.":
            "A hand-painted sign. A doorway the width of a person. A stack of folded chairs behind a glass door with a hand-written schedule."
            "Fifty seats, no committee, no application. Somebody wrote a thing and put it on in a room this size."
            mc "(She said that is how the best places happen. I am starting to see what she meant.)"
            $ reward_attributes_once("city_shimokita_theaters", [("insight", "micro")], show="auto")

    "I walk back toward the station the long way, past shutters coming down and a guitar case leaning against a closed door."
    mc "(She wanted me to see a place where nobody has to perform. I think she was showing herself the way back to it too.)"

    menu:
        "Stand outside the live house.":
            scene bg_live_house with walk_fade
            "I do not go in this time. I stand at the door through soundcheck and feel the bass in my chest."
            "A girl comes out for air, nods at me like I belong there, and goes back in."
            mc "(That is enough. I do not need to be inside to have been here.)"
            $ reward_attributes_once("city_shimokita_door", [("nerve", "micro")], show="auto")
        "Go back to the record shop.":
            scene bg_record_shop with walk_fade
            "The third crate. I check whether the street-at-night record is still there."
            "It is not. Somebody bought it while I was walking."
            mc "(I am happy for whoever did. That is a new feeling about a record I do not own.)"
            $ reward_attributes_once("city_shimokita_sold", [("grace", "micro")], show="auto")
        "Just walk the alley with the cat.":
            "The cat has moved to a warmer patch of wall. I sit on the step beside him for a minute."
            "He does not look at me. That is the whole welcome and it is enough."
            $ reward_attributes_once("city_shimokita_cat", [("insight", "micro")], show="auto")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label city_row_omotesando:
    $ phone_map_visit("omotesando")
    scene bg_omotesando with walk_fade
    "Omotesando Station, the exit with the trees."
    "The zelkova are still here, taller than the buildings and older than most of them. The shops beneath them are lit like jewellery cases."
    "I know the way now. Up the hill, past the last window, through the gate."
    mc "(She said the road was built for a god and then got expensive. I still think about that.)"

    menu:
        "Look up at the buildings instead of the windows.":
            "The Tod's building has branches growing out of concrete. The Dior is a sheet of glass with the trees doubled in it. The Prada has bubbles pressed into its skin."
            "Somebody spent as much on the outside as on the things inside."
            mc "(A street where the boxes are the point. She would say that is very honest.)"
            $ reward_attributes_once("city_omotesando_buildings", [("insight", "micro")], show="auto")
        "Walk up the middle of the pavement.":
            "I walk up the centre like I own it. Two people in a hurry step around me without a word."
            "I move to the side. Nobody tells you. You learn it from the shoulders of the people in front of you."
            mc "(There are lanes here too. They are just not painted.)"
            $ reward_attributes_once("city_omotesando_lanes", [("nerve", "micro")], show="auto")
        "Sit on the low wall between two trees and watch.":
            "I sit. A woman in a coat that costs more than my laptop walks past. A man in work clothes carries a ladder past her. Neither looks at the other."
            "Two schoolgirls photograph a shop window, then each other, then the window again."
            mc "(Everybody is dressed for somebody. Nobody is dressed for me.)"
            $ reward_attributes_once("city_omotesando_watch", [("grace", "micro")], show="auto")
        "Check my pocket for a five-yen coin.":
            "There is one in my wallet, under the train card. It has a hole in the middle, and I have carried it since she told me to bring one."
            "Go-en. A connection. I still do not know who I am supposed to have one with."
            mc "(I put it in my other pocket so I do not spend it by accident.)"
            $ reward_attributes_once("city_omotesando_coin", [("insight", "micro")], show="auto")

    "The shops end. The trees change. The pavement becomes gravel and the sound of the city goes out like a light."
    "The torii is exactly where I left it. I bow once, from the chest, and step to the left of the path."
    "I do it without thinking. Then I notice I did it."
    mc "(Three weeks ago I would have walked straight up the middle and taken a picture.)"

    "At the basin I take a ladle in my right hand, pour over my left, then the other way, then a little into my palm."
    "I rinse my mouth and do not drink from the ladle. I tip it so the water runs down the handle and put it back."
    "Nobody watches. Nobody corrects me. It is the first thing I have done correctly in this country with nobody checking."
    mc "(She said the handle is for the next person. I think about that more than I expected to.)"

    menu:
        "Take the long way through the forest.":
            "The long path. The gravel, then the trees, then the place where the city stops."
            "I walk until my feet are the loudest thing in Tokyo. Then I keep walking until even they are not."
            mc "(A hundred thousand trees, and somebody planned them for people who were not born yet.)"
            $ reward_attributes_once("city_omotesando_forest", [("insight", "micro")], show="auto")
        "Read the names on the sake barrels.":
            "The barrels are stacked shoulder to shoulder, white and black with characters I cannot read."
            "One name I recognise from a menu. I do not know how to say it. I point at it like a child and then put my hand down."
            mc "(Somebody sent this here from a town I will never visit. The kami can read it. That has to be enough.)"
            $ reward_attributes_once("city_omotesando_barrels", [("grace", "micro")], show="auto")
        "Use the five-yen coin at the offering box.":
            "I drop the coin. It rattles more than I meant it to."
            "Two bows. Two claps. One bow. I get the order right and the timing wrong, and nobody minds."
            "The second time is slower. I do not know who I said it to."
            mc "(Go-en. A connection. Maybe wanting one is the connection.)"
            $ reward_attributes_once("city_omotesando_pray", [("nerve", "micro")], show="auto")
        "Write a question on an ema.":
            "The ema are wooden plaques with a hole and a string. I buy one and write on it."
            "I do not write a wish. I write a question. Then I hang it with the others and read a few of theirs."
            "Somebody has written a name. Somebody has written 'please let it be the same.'"
            mc "(A wall of strangers' questions, hanging in the rain. It is the most honest thing I have seen here.)"
            $ spend_money(500)
            $ reward_attributes_once("city_omotesando_ema", [("insight", "micro")], show="auto")

    "On the way down I stop at the place she took me. The barista looks up and does not pretend not to know me."
    mc "ホット、お願いします。"
    "Two words I know, in the order I know them. He understands me the first time."
    mc "(The first time. That is a new record.)"
    "I sit outside with the coffee and watch the street get dark under the trees."

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return
