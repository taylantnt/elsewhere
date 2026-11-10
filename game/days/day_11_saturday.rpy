################################################################################
## DAY 11 — SATURDAY, APRIL 18, 2026
## The book town: used paper, modern literature, and the second life of a book.
################################################################################

label saturday_recovery:
    $ set_story_day(11)
    call day_transition

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Saturday. The house is quiet in a different way. No train, no clock ticking in anybody's head."
    "I wake before the rest of the house, which is new. I lie there and listen to it not waking up."
    mc "(The elective continues today. Not in a classroom. Murakami said to meet him at the station.)"
    mc "(He did not say which station. He said the one with the clock.)"

    "My phone buzzes once on the desk."

    if "hana" in wire_unlocked:
        $ run_chat("hana", [
            {"them": "The reading room is open today.", "options": [
                {"label": "\"I'll come by if I can.\"",
                 "send": "I'll come by if I can.",
                 "them": ["The door with no sign.", "You know it now."]},
                {"label": "\"I have a class this morning.\"",
                 "send": "I have a class this morning.",
                 "them": ["Then after.", "The room keeps its hours. So do I."]},
            ]},
        ])
        mc "(She texts in full stops. Every sentence is a small closed door that she has decided to leave open.)"
    else:
        $ run_chat("hikari", [
            {"them": "You're up. On a Saturday. Who are you?", "options": [
                {"label": "\"I have a class.\"",
                 "send": "I have a class.",
                 "them": ["On a Saturday?", "Murakami really did get you."]},
                {"label": "\"I'm becoming a morning person.\"",
                 "send": "I'm becoming a morning person.",
                 "them": ["Don't say that in front of Dad.", "He'll make you do the shopping."]},
            ]},
        ])
        mc "(She is joking. I am almost sure she is joking.)"

    "I go down before anyone calls me."

    scene bg_kitchen with walk_fade

    "The kitchen is empty. The rice cooker is on. The kettle is warm. Someone has already been here and gone back to bed."
    "I make tea the way Mother does: the leaves, the water, the wait. It takes longer than I expect. It is supposed to."
    "Father comes down while the tea is steeping. He stops in the doorway."
    father "You made tea."
    mc "I made tea."
    father "For everyone?"
    mc "For everyone."
    "He sits down. He does not say anything for a while. Then he says:"
    father "You are learning the house."
    mc "(That is the second time. I am starting to collect them.)"
    $ add_affection("father", 1)

    "Mother comes down next, then Hikari, and the kitchen fills with the ordinary noise of a Saturday."
    mother "You made the tea."
    mc "I made the tea."
    mother "Did you pour for yourself first?"
    mc "No. I poured for everyone."
    mother "Good. You never pour for yourself first."
    mc "Why?"
    mother "Because the pot is not about the tea. It is about who you are thinking of."
    mother "You pour for the person beside you. They pour for you. The table becomes a conversation without words."
    father "And you say otsugi douzo. After you."
    mc "(I have been drinking tea wrong my whole life.)"

    menu:
        "Ask about kanpai.":
            mc "What about kanpai? At dinner. Is there a rule?"
            father "Wait for everyone to have a glass. Then say it together. Do not start drinking before the oldest person."
            mother "And do not pour your own. Someone pours for you. You pour for them."
            mc "(A table where everyone is watching everyone else's glass. It sounds exhausting. It sounds kind.)"
            $ reward_attributes_once("day11_kitchen_kanpai", [("insight", "micro")], show="auto")
        "Ask about shun, the seasonal thing.":
            mc "Murakami used a word. Shun. What does it mean?"
            mother "The best time for a thing. The week a fish is best. The week a vegetable is sweet."
            mother "You do not eat strawberries in winter and pretend they are the same."
            mc "(A calendar you can taste. I like that more than I expected.)"
            $ reward_attributes_once("day11_kitchen_shun", [("grace", "micro")], show="auto")
        "Ask about mottainai.":
            mc "And mottainai? I heard it at the shop."
            mother "It means do not waste. But it means more. It means a thing has a worth that is not only for you."
            father "The rice you do not eat. The water you leave running. The time you spend badly."
            mc "(That last one lands harder than the other two.)"
            $ reward_attributes_once("day11_kitchen_mottainai", [("nerve", "micro")], show="auto")

    hikari "You're going to be late for your book man."
    mc "He said the station with the clock."
    hikari "They all have clocks."
    mc "Then I'll find the one with the right clock."
    hikari "That is the most you thing you have ever said."
    mother "Take an umbrella."
    mc "It is not raining."
    mother "Take the umbrella."
    mc "(I take the umbrella.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0
    "The Saturday street is slower. People walk like they have already arrived somewhere."
    "I find the station with the clock. Murakami is standing under it with a canvas bag and no umbrella."

    scene bg_station with walk_fade
    murakami "You came."
    mc "You said the station with the clock."
    murakami "All stations have clocks. I wanted to see which one you would choose."
    mc "That is not a fair test."
    murakami "It is not a test. It is a habit. You chose the one you knew."
    "He turns and walks toward the platform. I follow."

    scene bg_platform with walk_fade
    "The Saturday platform is full of families and tourists and people carrying bags with other people's weekends in them."
    "A child is explaining a train to his father. The father is listening with the seriousness of a man being taught something important."
    murakami "On Saturdays the train is not a train. It is a field trip."
    mc "And on weekdays?"
    murakami "On weekdays it is a contract. Everyone agrees to be alone. On Saturdays they agree to be together."
    mc "(The same metal box. A different country inside it.)"

    scene bg_train_interior with walk_fade
    "The car is louder than the weekday car. A family shares a box of sweets. A group of students takes photographs of the map."
    "An old man reads a newspaper with a magnifying glass. He does not look up once."
    murakami "We are going to Jimbocho. The book town. It is not a museum. It is a street where people still buy and sell the past."
    mc "The past?"
    murakami "Used books. Every one of them has been read by someone who is not you. That is the whole point."
    murakami "A new book is a promise. A used book is a conversation."
    "He takes a small notebook out of his bag and writes something down. He does not show me what."

    menu:
        "Ask what he wrote.":
            mc "What did you write?"
            murakami "A sentence for you. You will get it at the end of the day, if you deserve it."
            mc "That is not how homework works."
            murakami "It is how this homework works."
            $ reward_attributes_once("day11_train_note", [("insight", "micro")], show="auto")
        "Ask why he teaches an elective nobody takes.":
            mc "Why do you teach a course nobody takes?"
            murakami "Someone took it. You."
            mc "Before me."
            murakami "Before you, the course was a room with a chair in it. I taught the chair."
            "He says it without self-pity. It is simply the weather."
            $ reward_attributes_once("day11_train_course", [("nerve", "micro")], show="auto")
        "Watch the old man with the magnifying glass.":
            "The old man turns the page with one finger. The magnifying glass moves across the paper like a small sun."
            "He is reading the same newspaper everyone else has already thrown away."
            mc "(Maybe that is what a used book is. A newspaper someone kept.)"
            $ reward_attributes_once("day11_train_oldman", [("grace", "micro")], show="auto")

    scene bg_station with Fade(0.0, 0.0, 1.0)
    "We come out of the station into a street that smells of paper and old wood."
    "Books are stacked in the windows and on the pavement and in crates by the doors. Some of them are wrapped in plastic. Some are not."
    murakami "Jimbocho. A hundred shops. Maybe more. Nobody has counted in a long time."
    mc "Why here?"
    murakami "Because the universities were here, and the students needed books, and the books stayed after the students left."
    murakami "Cities are made of what people needed once."

    scene bg_library with walk_fade
    "The shop he chooses is narrow and deep, with shelves that go up past the ceiling and a ladder on a rail."
    "An old woman behind the counter does not look up from her ledger."
    "Murakami walks to a shelf in the back as if he has done it a thousand times."
    murakami "Sit. There is a stool."
    "I sit. He pulls three books from the shelf and sets them on the counter in front of me."

    "The first is thin and blue. The second is thick and brown. The third has no cover at all."
    murakami "Natsume Sōseki. Kokoro. A man who cannot say the thing he means until it is too late."
    murakami "Kawabata Yasunari. Snow Country. A man who goes to the mountains to be disappointed by a woman."
    murakami "Tanizaki Junichirō. In Praise of Shadows. An essay about why a room should be dark."
    mc "That is a strange combination."
    murakami "It is a conversation. Sōseki asks whether you can know another person. Kawabata asks whether you can love one. Tanizaki asks whether you can see one."
    murakami "They are all asking the same question in different rooms."

    "He opens Snow Country to a page near the beginning and reads a sentence aloud. The Japanese is slow and clean."
    murakami "The train came out of the long tunnel into the snow country. The night was white."
    mc "(The sentence is simple. It is also a whole world. I do not know how it does that.)"
    murakami "The white is not a color. It is an absence. The book is about people who cannot fill the absence."
    murakami "This is wabi-sabi. The beauty of what is imperfect, incomplete, and passing."
    murakami "It is not a decoration. It is a way of looking at a thing that is already leaving."

    menu:
        "Ask why a used book is better than a new one.":
            mc "Why a used book? Why not a new one?"
            murakami "A new book is a window. A used book is a window with someone else's fingerprints on it."
            murakami "You can see what they underlined. You can see where they stopped."
            "He opens the brown book. There is a pencil mark in the margin, faint and old."
            murakami "Someone was here. That is all a book is. A room someone else has been in."
            $ reward_attributes_once("day11_lesson_used", [("insight", "micro")], show="auto")
        "Ask about ichigo ichie.":
            mc "What is ichigo ichie?"
            murakami "One time, one meeting. Every encounter happens once and never again."
            murakami "Not because people die. Because the people who meet are never the same two people twice."
            mc "(I think of the airport. The house. The train. None of it can happen again in the same way.)"
            murakami "That is why the tea ceremony takes so long. It is not about the tea. It is about the once."
            $ reward_attributes_once("day11_lesson_ichigo", [("grace", "micro")], show="auto")
        "Ask whether Tanizaki is right about the dark.":
            mc "Is Tanizaki right? About the dark?"
            murakami "He is right about the beauty. He is wrong about the reason."
            murakami "He thought the dark was a Japanese thing. It is a human thing. Everyone looks better in a room they cannot quite see."
            "He closes the book and sets it down."
            murakami "Do not believe a writer who tells you what a country is. Believe the country."
            $ reward_attributes_once("day11_lesson_tanizaki", [("nerve", "micro")], show="auto")

    "The old woman behind the counter finally looks up. She says something to Murakami. He answers. She nods and goes back to her ledger."
    murakami "She says you have good posture for a foreigner."
    mc "Is that a compliment?"
    murakami "It is an observation. In this shop, that is a compliment."
    "He buys the thin blue book and hands it to me."
    murakami "Kokoro. Read the first page. Bring me one sentence you do not understand."
    mc "You keep giving me homework."
    murakami "That is what a teacher is. A person who gives you the thing you will need later."
    "He puts the other two books back on the shelf. The ladder creaks as he reaches."

    scene bg_station with walk_fade
    "We take the train back in the early afternoon. The car is emptier now. The families have gone home."
    murakami "You did well today."
    mc "I sat on a stool and listened."
    murakami "That is most of it."
    "He gets off two stops before mine. He does not say goodbye. He says, without turning:"
    murakami "Read the page."
    "The doors close. The train goes on."

    scene bg_home_exterior_day with walk_fade
    "The afternoon is still mine. The book is in my bag. The city is where I left it."
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
    mc "Kokoro. Sōseki. I have to read the first page."
    father "Then read it before you sleep. A book read before sleep stays in the body."
    mc "(That is either wisdom or a warning. I am starting to think they are the same thing in this house.)"

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, I open Kokoro to the first page. The Japanese is hard. The English in my head is harder."
    "A knock at the door. Hikari, with two cups of tea and her own notes under her arm."
    hikari "I'm not staying. I'm just making sure you're not staring at the wall."
    mc "I was staring at Sōseki."
    hikari "Same thing."
    "She sets the tea down and sits on the floor with her back against the bed."

    menu:
        "Read her the sentence I don't understand.":
            "I read it aloud. The pronunciation is wrong in two places. She does not correct me until I finish."
            hikari "Again. The last word."
            "I say it again. It is still wrong. She says it once, slowly, and I say it after her."
            mc "(The word is mine now. Not borrowed. Mine.)"
            $ reward_attributes_once("day11_night_read", [("grace", "micro")], show="auto")
        "Ask her what wabi-sabi means to her.":
            mc "Wabi-sabi. What does it mean to you? Not the dictionary."
            hikari "It means I like the chipped bowl better than the new one."
            mc "Why?"
            hikari "Because someone used it. Because it has a history I can hold."
            mc "(She turns her cup so the chip faces her. She does not hide it.)"
            $ reward_attributes_once("day11_night_wabi", [("insight", "micro")], show="auto")
        "Tell her I want to stay in Japan.":
            mc "I think I want to stay. After the year. I don't know how to say it yet."
            hikari "Then don't say it yet."
            mc "That's not an answer."
            hikari "It's the answer I have. Stay long enough to mean it."
            $ reward_attributes_once("day11_night_stay", [("nerve", "micro")], show="auto")

    "She takes her cup and leaves the door open a hand's width."
    "I listen to her go down the stairs, then the house settle into its night sounds."
    "The book is still open. The tea is still warm."
    "Tomorrow is Sunday. The last day of the first week of the elective."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump sunday_practice
