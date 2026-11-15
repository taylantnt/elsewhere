################################################################################
## CHEF — THE RAMEN SHOP
################################################################################

# Defined late so type_sound (script.rpy) already exists when this runs.
init 999 python:
    kenta = Character("Kenta", callback=type_sound)
    student1 = Character("Student", callback=type_sound)
    student2 = Character("Student", callback=type_sound)
    woman = Character("Woman in a Suit", callback=type_sound)

label confidant_visit_chef:
    $ visit = confidant_visits.get("chef", 0)
    if visit == 0:
        # The Day 2 walk-alone route is the usual first meeting, but the first
        # free afternoon is a fork: a player who walked home with Hikari or
        # joined Circle never came down this street. The hub's zero-visit rule
        # ("a place with zero visits is always available") is what lets the
        # ramen shop introduce itself later instead of deadlocking the gate.
        jump chef_visit_01
    elif visit == 1:
        jump chef_visit_02
    elif visit == 2:
        jump chef_visit_03
    elif visit == 3:
        jump chef_visit_04
    elif visit == 4:
        jump chef_visit_05
    elif visit == 5:
        jump chef_visit_06
    elif visit == 6:
        jump chef_visit_07
    elif visit >= 7:
        jump chef_visit_closed
    return

label chef_common_open:
    scene bg_ramen_shop with walk_fade
    stop music fadeout 1.2
    play music "audio/Music/ramen_shop.mp3" fadein 2.0
    $ phone_map_visit("ramen_shop")
    return

################################################################################
## VISIT 1 — THE FIRST BOWL
################################################################################
##
## The alternate first meeting. The Day 2 walk-alone route already contains a
## full ramen-shop scene, so this one only runs when that route was skipped.
## It has to do the same work in less time: the shop, the man, the menu he
## cannot read, and the WIRE card that makes him a contact.

label chef_visit_01:
    call chef_common_open

    "The noren hangs in the doorway, blue and faded, with a white character on it I have walked past twice without reading."
    "Steam comes out under it in a slow curtain. The smell is pork and soy and something roasted."
    mc "(The kind of smell that makes a decision for you.)"
    "I push the curtain aside."

    "The shop is six stools and a counter and a man. The man is at the stove with his back to the door, and he does not turn around."
    chef "いらっしゃい。"
    mc "(Irasshai. Welcome. I know that one now.)"

    "There is one other customer, an old man in a cap, eating with the focused silence of a man who has done this ten thousand times."
    "I take the stool farthest from him, because it feels like the polite amount of distance."
    chef "おう。"
    "The chef grunts without turning. Then he turns. He looks at me the way a mechanic looks at a car that has arrived with no appointment."
    chef "はじめて？"
    mc "(Hajimete. First time. He is asking if it is my first time.)"
    mc "Hai. First time."
    chef "そうか。"
    "He points at the wall with his ladle. A handwritten menu, four lines, all of them characters I cannot read."

    menu:
        "Ask him what he recommends.":
            mc "Osusume wa? What do you recommend?"
            "He looks at me for a second longer than I expected. Then he nods once, as if I have passed a test I did not know I was taking."
            chef "豚骨。"
            mc "(Tonkotsu. I do not know what it means. I will find out.)"
            $ reward_attributes_once("chef_visit_01_recommend", [("grace", "micro")], show="auto")
        "Point at the second line.":
            "I point at the second line on the menu and hope it is not a price."
            "The chef follows my finger, then looks at my face, then makes a sound that might be a laugh."
            chef "それか。"
            mc "(That one. Good. I have ordered a thing.)"
            $ reward_attributes_once("chef_visit_01_point", [("insight", "micro")], show="auto")
        "Order in English and hope.":
            mc "Ramen, please. Whatever's good."
            "The chef stares at me. Then he says, slowly, in English:"
            chef "Good. I choose."
            mc "(He has more English than he lets on. He was waiting to see if I would try.)"
            $ reward_attributes_once("chef_visit_01_english", [("nerve", "micro")], show="auto")

    "He turns back to the pots. The broth goes into the bowl in one motion, the noodles go in after, the egg is cut and laid down like it is being placed on a map."
    "He sets the bowl in front of me and taps the counter once."
    chef "熱い。"
    mc "(Atsui. Hot. He is warning me, not selling me.)"
    mc "Arigatou gozaimasu."
    "He grunts. It is the warmest grunt I have heard."

    "The first mouthful is so much better than anything I have eaten here that I have to put the chopsticks down."
    mc "(It is not just food. It is a whole day of somebody's work in a bowl.)"
    "I eat. The old man finishes, pays, and leaves without a word. The chef wipes the counter where he was sitting."
    chef "どう？"
    mc "(Dou. How is it.)"
    mc "Umai. Really umai."
    chef "そうか。"
    "He nods once, satisfied, and goes back to the pots."

    "When I finish, he sets a small card beside my bowl. A black square made of smaller black squares, with six words in English in handwriting that is not his."
    chef "「読め」"
    mc "(Read it. That one is no mystery.)"
    "I hold my phone over the card. The app takes it without asking, and puts a name on the list."
    mc "So I know if you're shut before I walk down here for nothing."
    chef "水曜、休み。"
    mc "(Wednesday, closed. Noted.)"
    $ wire_unlock("chef")

    "I pay. He counts the coins into the till without looking at them."
    chef "また。"
    mc "(Mata. Again. He is not saying goodbye. He is saying the door is still here.)"
    $ chef_affection += 1
    $ confidant_visits["chef"] = max(confidant_visits.get("chef", 0), 1)
    $ remember("chef", "found the ramen shop on a free afternoon and learned the shop is closed Wednesdays")
    $ reward_attributes_once("chef_visit_01_close", [("grace", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return


label chef_visit_02:
    call chef_common_open

    "The shop is quieter than last time. Two seats are occupied by the same two men, eating with the focused silence of people who have made this ritual before."
    "Chef is at the stove, his back to the door, conducting the pots with chopsticks like an orchestra that knows exactly what to play."

    voice "audio/VO/ramen_welcome.mp3"
    chef "いらっしゃい。"
    "He does not turn around. He knows the step."

    mc "Good evening."
    chef "おう。"
    "He grunts, then turns. He points to the second line on the menu with a ladle."
    chef "それ。"
    mc "(That. That's the one I had last time.)"

    "I sit. The stool has developed a memory of my posture, or I have developed a memory of the stool."

    chef "前、うまかった？"
    mc "(I recognize 'umai' from last time. Delicious? Did I like it?)"
    mc "Hai. Umai."
    chef "そうか。"
    "He nods once, satisfied with the answer, and returns to the pots."

    menu:
        "Ask what he's making today.":
            mc "Sumimasen. What are you making today?"
            chef "豚骨。"
            mc "(Tonkotsu. Pork bone broth. He said it slowly, like he knew I wouldn't know.)"
            chef "朝から。"
            mc "(Since morning. It takes all day.)"
            $ reward_attributes_once("chef_visit_02_ask", [("insight", "micro")], show="auto")
        "Watch him work silently.":
            "I watch the way he moves. Every motion has a purpose. He does not waste time, but he does not rush."
            "The rhythm of the kitchen is its own language."
            chef "見てる？"
            mc "(He's asking if I'm watching.)"
            mc "Hai."
            chef "いい目だ。"
            mc "(Good eyes. That sounded like approval.)"
            $ reward_attributes_once("chef_visit_02_watch", [("grace", "micro")], show="auto")
        "Thank him for the last bowl.":
            mc "Last time was really good. Thank you."
            chef "おう。"
            "He grunts again, then adds a little more green onion to the bowl he's preparing."
            chef "男子。"
            mc "(Good man. Or: that's how men do it. The word has more meanings than I can count.)"
            $ reward_attributes_once("chef_visit_02_thank", [("nerve", "micro")], show="auto")

    "He sets the bowl down with a soft thud."
    "The broth is different today. Lighter, but no less rich. The noodles are firmer."
    "He is teaching me without teaching, the way a parent teaches a child to walk by standing nearby."

    chef "熱い。"
    mc "(Hot. He's warning me.)"
    mc "Arigatou."

    "I eat. The steam rises between us like a curtain, but it is a curtain I can see through."
    "Chef watches the door more than he watches me, but his attention is always in the room."

    chef "毎日？"
    mc "(Every day? He's asking if I come every day.)"
    mc "Iie. Not every day. But I like coming here."
    chef "いい。"
    mc "(Good. That's all he says. Just good.)"

    "He wipes the counter with a cloth that has seen years of broth and steam."
    chef "水曜、休み。"
    mc "(Wednesday, closed. The shop's card said so the first night. One day a week this man refuses to work, and he wants me to remember which one.)"
    chef "休むのも、仕事だ。"
    mc "(Resting is also work. That is a sentence I will remember.)"
    $ chef_affection += 1

    $ confidant_visits["chef"] = max(confidant_visits.get("chef", 0), 2)
    $ remember("chef", "learned that resting is also work and had tonkotsu ramen")
    $ queue_message("chef", "The broth needs twelve hours. The rest needs two days. Both are part of the bowl.", day="yesterday")
    $ reward_attributes_once("chef_visit_02_close", [("grace", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return

label chef_visit_03:
    call chef_common_open

    "The shop is full when I arrive."
    "Every seat is taken. There is a line at the door, the quiet, patient line of people who know that good things do not arrive on a schedule."

    "Chef sees me through the steam. He points to a small table in the corner that I had not noticed before."
    chef "そこ。"
    mc "(There. He is offering me a table instead of the counter. That is promotion.)"

    "I sit. The table is wobbly in a way that suggests it has survived more than one earthquake and several generations of diners."
    "The group beside me is speaking English. They are students, and they are not from here."

    student1 "I don't know what any of this says. Just point at something?"
    student2 "That's what I did last time. It worked."
    student1 "What if I point at the wrong thing?"
    student2 "Then you learn something about yourself."

    "Chef overhears. He does not interrupt, but his mouth curves at the corner."

    menu:
        "Help them order.":
            mc "The second line is the house special. It's what most people get."
            student1 "Oh, thanks! You speak English?"
            mc "Yeah. I'm also not from here."
            student2 "That makes me feel better about the pointing."
            $ reward_attributes_once("chef_visit_03_help", [("grace", "micro")], show="auto")
        "Let them figure it out.":
            "I watch them argue over the menu. The figuring out is part of the experience."
            "Chef catches my eye and nods, as if to say: you understand."
            $ reward_attributes_once("chef_visit_03_watch", [("insight", "micro")], show="auto")
        "Ask Chef to recommend.":
            mc "Sumimasen. What do you recommend for them?"
            chef "男子、豚骨。女子、塩。"
            mc "(Men get tonkotsu. Women get salt. He says it like it is gravity, not preference.)"
            student1 "What did he say?"
            mc "He said: trust him."
            $ reward_attributes_once("chef_visit_03_recommend", [("nerve", "micro")], show="auto")

    "The orders go out. The students eat with the enthusiasm of people discovering something they did not know they needed."
    "Chef watches them. His attention is not judgment. It is measurement."

    "After the rush, when the line has dissolved and the shop is back to its regular quiet, Chef brings me a bowl."
    "It is not the regular bowl. This one has a soft-boiled egg in the center, perfectly round, perfectly yellow."

    chef "特別。"
    mc "(Special. He made me something different.)"
    mc "For me?"
    chef "英語、教えた。"
    mc "(You taught them English. That was his reason. I helped, so I get an egg.)"

    menu:
        "I was just being helpful.":
            mc "I was just being helpful. They were confused."
            chef "助けるのは、いいことだ。"
            mc "(Helping is a good thing. Simple. True.)"
            $ reward_attributes_once("chef_visit_03_humble", [("grace", "micro")], show="auto")
        "I like watching people find good food.":
            mc "I like watching people find good food. It feels like sharing a secret."
            chef "秘密じゃない。"
            mc "(It's not a secret. This is a shop, not a conspiracy.)"
            chef "でも、嬉しい。"
            mc "(But it makes him happy. That is the part he will say out loud.)"
            $ reward_attributes_once("chef_visit_03_share", [("insight", "micro")], show="auto")
        "Did you see them enjoying it?":
            mc "Did you see them enjoying it?"
            chef "見てた。"
            mc "(He was watching. Of course he was watching.)"
            chef "最初、分からない。後、分かる。"
            mc "(At first, they don't understand. Later, they do. That is how ramen works. That is how Japan works.)"
            $ reward_attributes_once("chef_visit_03_understand", [("insight", "micro")], show="auto")

    "I eat the egg. It is perfect in the way that makes you angry at every other egg you have ever eaten."
    "The yolk coats the noodles in a way that should be illegal."

    chef "どう？"
    mc "(How is it? He is asking, but he already knows.)"
    mc "Umai."
    chef "ああ。"
    "He nods, once, and returns to the pots."
    $ chef_affection += 1

    $ confidant_visits["chef"] = max(confidant_visits.get("chef", 0), 3)
    $ remember("chef", "helped foreign students order and received a special bowl with ajitsuke tamago")
    $ queue_message("chef", "The students came back yesterday. They ordered in Japanese. Badly, but in Japanese. That is progress.", day="yesterday")
    $ reward_attributes_once("chef_visit_03_close", [("insight", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return

label chef_visit_04:
    call chef_common_open

    "The shop is closed. The sign in the window says CLOSED FOR TRAINING, in both Japanese and English."
    "But the door is unlocked, and Chef is inside, sitting at the counter with a notebook open in front of him."

    "He looks up when I enter, then points to the stool beside him."
    chef "座れ。"
    mc "(Sit. He is not taking orders today. He is asking for company.)"

    "I sit. The notebook is filled with handwriting that is precise and hurried at the same time."
    "Numbers, times, temperatures. The chemistry of broth in another language."

    chef "見るか？"
    mc "(Do you want to see? He is offering me the notebook.)"
    mc "May I?"

    "He slides it over. The page is headed with a date from twenty years ago."
    "The recipe is different. Simpler. Fewer ingredients, but the notes are longer."

    menu:
        "Did you change the recipe?":
            mc "This recipe is different from what you make now."
            chef "毎日、変える。"
            mc "(Every day, I change it. A little. Not much, but a little.)"
            chef "同じじゃ、つまらない。"
            mc "(If it's the same, it's boring. That is why the broth is never exactly the same twice.)"
            $ reward_attributes_once("chef_visit_04_change", [("insight", "micro")], show="auto")
        "What are you trying to improve?":
            mc "What are you trying to improve?"
            chef "バランス。"
            mc "(Balance. Salt, richness, depth. The things you cannot measure with a thermometer.)"
            chef "昨日、濃かった。今日、薄くする。"
            mc "(Yesterday, it was too strong. Today, I make it lighter. He corrects himself constantly.)"
            $ reward_attributes_once("chef_visit_04_improve", [("insight", "micro")], show="auto")
        "How long have you been making ramen?":
            mc "How long have you been making ramen?"
            chef "三十年。"
            mc "(Thirty years. He says it without pride, like saying he has been breathing for thirty years.)"
            chef "まだ、分からない。"
            mc "(I still don't understand it. After thirty years, he still does not claim to know ramen.)"
            $ reward_attributes_once("chef_visit_04_time", [("grace", "micro")], show="auto")

    "Chef takes the notebook back and turns to a blank page."
    "He writes today's date. Then he writes three Japanese characters: 味, 香, 色."
    "Taste, aroma, color. The three things a bowl must have."

    chef "味は、一番大事。"
    mc "(Taste is the most important. That is obvious.)"
    chef "でも、香も大事。色も大事。"
    mc "(But aroma is also important. Color is also important. People eat with their eyes first.)"

    menu:
        "What about the texture?":
            mc "What about the texture? The way the noodles feel?"
            chef "喉で食べる。"
            mc "(You eat with the throat. The sensation of swallowing is part of the taste.)"
            chef "喉が満足する。"
            mc "(The throat must be satisfied. That is why the noodles are cooked just so.)"
            $ reward_attributes_once("chef_visit_04_texture", [("insight", "micro")], show="auto")
        "What about the temperature?":
            mc "And the temperature? The heat?"
            chef "熱すぎない。冷たすぎない。"
            mc "(Not too hot. Not too cold. There is a temperature where the flavors sing.)"
            chef "体温に近い。"
            mc "(Close to body temperature. That is the warmth that makes you want to stay.)"
            $ reward_attributes_once("chef_visit_04_temp", [("insight", "micro")], show="auto")
        "What makes a bowl perfect?":
            mc "What makes a bowl perfect?"
            chef "完璧なんてない。"
            mc "(There is no such thing as perfect. He says it with absolute certainty.)"
            chef "でも、頑張る。"
            mc "(But I try. That is the part that matters. The trying, not the arriving.)"
            $ reward_attributes_once("chef_visit_04_perfect", [("grace", "micro")], show="auto")

    "Chef closes the notebook and sets it on the shelf beside the stove."
    "He stands up and goes to the pots. He has not made ramen for me today, but he has made me understand why the ramen is the way it is."

    chef "今日、作らない。"
    mc "(Today, I'm not making any. It is a day for thinking, not for cooking.)"
    chef "明日、来て。"
    mc "(Come tomorrow. The broth will be better for the thinking.)"

    mc "I'll be here."
    chef "おう。"
    "He grunts, satisfied with the promise."
    $ chef_affection += 1

    $ confidant_visits["chef"] = max(confidant_visits.get("chef", 0), 4)
    $ remember("chef", "saw his recipe notebook and learned that he changes the broth every day")
    $ queue_message("chef", "I changed the recipe again. The students noticed. They said it was 'different, but still good.' That is enough.", day="yesterday")
    $ reward_attributes_once("chef_visit_04_close", [("nerve", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return

label chef_visit_05:
    call chef_common_open

    "The shop is loud in the way of a place that has become a destination."
    "There are people I have never seen before. They are speaking languages I do not recognize, but they are all eating with the same focused silence."
    "Word has traveled. Chef's ramen is no longer a secret."

    "Chef is moving faster than I have ever seen him."
    "He is one man, but he is conducting the entire shop the way a conductor leads an orchestra."
    "Pots, noodles, broth, garnish. Every motion has been practiced until it is instinct."

    "He catches my eye through the steam and points to the counter."
    chef "特等席。"
    mc "(Premium seat. The counter is the best place to watch him work. He is offering me the show.)"

    "I sit. The stool beside me is empty for exactly three seconds before another customer arrives."
    "A woman in a suit. She looks like she has not stopped moving in weeks."

    woman "I heard about this place from a coworker. She said the broth saves lives."
    mc "She wasn't wrong."
    woman "I need saved. I haven't eaten a real meal since Tuesday."

    menu:
        "Introduce her to Chef.":
            mc "Chef, this is her first time."
            chef "ようこそ。"
            mc "(Welcome. He says it to the pot, but she hears it in the tone.)"
            chef "豚骨、いいよ。"
            mc "(Tonkotsu is good. His recommendation for everyone, because it is the one he believes in.)"
            $ reward_attributes_once("chef_visit_05_introduce", [("grace", "micro")], show="auto")
        "Let her discover it herself.":
            "I let her figure it out. The discovery is part of the experience."
            "She watches Chef work, eyes wide, and I remember my first time here."
            $ reward_attributes_once("chef_visit_05_discover", [("insight", "micro")], show="auto")
        "Tell her what to order.":
            mc "Get the tonkotsu. Trust me."
            woman "Tonkotsu. What is that?"
            mc "Pork bone broth. It takes twelve hours. It takes thirty years."
            woman "That sounds like a lot of work for a bowl of soup."
            mc "It is. That's why it matters."
            $ reward_attributes_once("chef_visit_05_tell", [("nerve", "micro")], show="auto")

    "The rush continues for an hour. Chef does not stop."
    "He does not complain. He does not seem tired. He is exactly where he is supposed to be."

    "When the line finally dissolves, he leans against the counter and exhales."
    "For the first time, I see that he is older than I thought. The gray in his hair is not decoration."

    chef "疲れた。"
    mc "(Tired. He admits it, which is not the same as complaining.)"
    mc "You should rest."
    chef "後で。"
    mc "(Later. There is still cleaning to do. Still prep for tomorrow.)"

    menu:
        "Can I help clean?":
            mc "Can I help clean? I can wipe the counter."
            chef "客は、食べるだけ。"
            mc "(Customers just eat. That is the rule. He is firm about it.)"
            chef "でも、ありがとう。"
            mc "(But thank you. The offer meant something, even if he cannot accept it.)"
            $ reward_attributes_once("chef_visit_05_help", [("grace", "micro")], show="auto")
        "You work too hard.":
            mc "You work too hard. Even for something you love."
            chef "好きだから、楽しい。"
            mc "(Because I like it, it is fun. That is his logic. Work you love is not work.)"
            chef "でも、体、言う。"
            mc "(But the body speaks. He listens to his body. That is why he rests two days a week.)"
            $ reward_attributes_once("chef_visit_05_hard", [("insight", "micro")], show="auto")
        "Do you ever think about retiring?":
            mc "Do you ever think about retiring?"
            chef "ない。"
            mc "(No. He says it without hesitation.)"
            chef "止まったら、死ぬ。"
            mc "(If I stop, I die. Not literally, but spiritually. The ramen is the reason he gets up.)"
            $ reward_attributes_once("chef_visit_05_retire", [("insight", "micro")], show="auto")

    "Chef brings me a bowl. It is the regular bowl, but there is something different about it today."
    "The broth is richer. The noodles are springier. It is the bowl of a man who found his rhythm and rode it."

    chef "今日、いいだった。"
    mc "(Today was good. He is satisfied with the day.)"
    mc "The shop was full."
    chef "うん。"
    mc "(Yeah. He nods, once, the way he does when he has nothing more to say.)"
    $ chef_affection += 1

    $ confidant_visits["chef"] = max(confidant_visits.get("chef", 0), 5)
    $ remember("chef", "saw the shop at its busiest and heard that he will never retire")
    $ queue_message("chef", "The woman in the suit came back today. She brought a coworker. They are becoming regulars. The shop grows whether I try or not.", day="yesterday")
    $ reward_attributes_once("chef_visit_05_close", [("grace", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return

label chef_visit_06:
    call chef_common_open

    "The shop is empty. Unusually empty for this hour."
    "Chef is sitting at the counter with a young man I have never seen before."
    "The young man has a notebook similar to Chef's, but his handwriting is shaky and unsure."

    "Chef looks up when I enter. He does not point to a seat. He waits for me to choose."
    "The young man is watching Chef with terrified reverence."

    chef "これ、弟子。"
    mc "(This is my apprentice. He says it like it is the most natural thing in the world.)"
    chef "名前、健太。"
    mc "(His name is Kenta.)"

    "Kenta bows. Too deeply. Too quickly."
    kenta "Nice to meet you. I mean—はじめまして。"
    chef "もっと、緩く。"
    mc "(More relaxed. Chef corrects him gently. Ramen does not need ceremony.)"

    menu:
        "Ask how long he's been learning.":
            mc "How long have you been learning?"
            kenta "Three weeks. I have so much to learn."
            chef "一生、かかる。"
            mc "(It takes a lifetime. Chef says it without discouragement. Just truth.)"
            $ reward_attributes_once("chef_visit_06_learn", [("insight", "micro")], show="auto")
        "Ask what he's working on.":
            mc "What are you working on today?"
            kenta "Chopping green onions. Chef says my rhythm is wrong."
            chef "リズム、全部。"
            mc "(Rhythm is everything. In the knife, in the broth, in the life.)"
            $ reward_attributes_once("chef_visit_06_work", [("insight", "micro")], show="auto")
        "Tell him it takes time.":
            mc "It takes time. I've been coming for months and I still don't understand half of what he says."
            kenta "That makes me feel better."
            chef "時間、かかる。急ぐな。"
            mc "(It takes time. Don't rush. That is the only lesson Chef thinks matters today.)"
            $ reward_attributes_once("chef_visit_06_time", [("grace", "micro")], show="auto")

    "Chef stands up and goes to the pots."
    "Kenta follows, notebook in hand, ready to record whatever Chef is about to do."

    chef "見て。"
    mc "(Watch. This is the lesson. Not the recipe. The watching.)"

    "Chef begins to make a bowl. He does not explain. He does not measure with tools. He measures with instinct."
    "Kenta writes furiously, trying to capture instinct in handwriting."

    menu:
        "Kenta, you can't write everything down.":
            mc "Kenta, you can't write everything down. Some of this you have to feel."
            kenta "But if I don't write it, I'll forget."
            chef "忘れる、いい。"
            mc "(Forgetting is fine. What you remember is what matters. What you forget was not the point.)"
            $ reward_attributes_once("chef_visit_06_forget", [("insight", "micro")], show="auto")
        "Watch Chef, not the notebook.":
            "I want to tell him to look up, but I don't. He has to learn that himself."
            "Chef catches my eye and nods. He knows what I am thinking."
            $ reward_attributes_once("chef_visit_06_watch", [("grace", "micro")], show="auto")
        "Chef, explain what you're doing.":
            mc "Chef, explain what you're doing. For him."
            chef "説明できない。"
            mc "(I can't explain it. He is not being difficult. He is being honest.)"
            chef "感じるしかない。"
            mc "(You can only feel it. Language is not the right tool for this.)"
            $ reward_attributes_once("chef_visit_06_explain", [("insight", "micro")], show="auto")

    "The bowl is finished. Chef sets it in front of me."
    "It is perfect. Not just good. Perfect in the way that makes you angry at every other bowl you have ever eaten."

    chef "食べて。"
    mc "(Eat. He is not asking. He is testing.)"

    "I eat. The broth is deeper than before. The noodles have a spring that feels alive."
    "This is not just ramen. This is Chef, distilled into a bowl."

    chef "どう？"
    mc "(How is it? He is asking, but this time he is also asking Kenta to listen to the answer.)"
    mc "It's... it's the best one you've ever made me."
    chef "ああ。"
    "He nods, once, satisfied with the truth."

    chef "健太、聞いた？"
    mc "(Kenta, did you hear? The truth matters more than the recipe.)"
    kenta "I heard."

    chef "一番大事なのは、客の顔。"
    mc "(The most important thing is the customer's face. Not the bowl. The person eating it.)"
    chef "顔、見れば、分かる。"
    mc "(If you watch the face, you understand. That is the only feedback that matters.)"
    $ chef_affection += 1

    $ confidant_visits["chef"] = max(confidant_visits.get("chef", 0), 6)
    $ remember("chef", "met his apprentice Kenta and ate the best bowl he has ever made")
    $ queue_message("chef", "Kenta is learning. Slowly. But he is learning. The knife work is getting better. The notebook is getting fuller. The forgetting is beginning.", day="yesterday")
    $ reward_attributes_once("chef_visit_06_close", [("insight", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return

label chef_visit_07:
    call chef_common_open

    "The shop is different. Not because of the people or the décor, but because of the feeling."
    "It feels like a place that has decided what it is."

    "Chef is at the counter. Kenta is beside him, and for the first time, Kenta is moving with confidence."
    "He is still learning, but he is no longer terrified. He is beginning to understand."

    "Chef sees me and points to the counter. The regular seat. The one that has developed my memory."

    chef "いつもの？"
    mc "(The usual? He is asking, but he already knows the answer.)"
    mc "Hai. The usual."

    "Kenta nods and goes to the pots. Chef watches him, hands clasped, eyes focused."
    "This is a test. Not for Kenta's sake, but for Chef's."

    "The bowl arrives. It is Kenta's work, but it has Chef's guidance in it."
    "The broth is good. Not perfect, but good. The noodles are firm. The egg is runny in the right way."

    chef "どう？"
    mc "(How is it? He is asking me to judge Kenta's work.)"

    menu:
        "It's good. He's learning.":
            mc "It's good. He's learning."
            chef "ああ。"
            mc "(Yeah. He nods, satisfied with the praise.)"
            chef "まだ、遠い。でも、進んでる。"
            mc "(Still far. But progressing. That is enough for now.)"
            $ reward_attributes_once("chef_visit_07_good", [("grace", "micro")], show="auto")
        "It needs more time.":
            mc "It needs more time. The rhythm isn't quite there yet."
            chef "そうか。"
            mc "(I see. He does not defend Kenta. He accepts the criticism as truth.)"
            chef "健太、聞いた？"
            mc "(Kenta, did you hear? The truth is the only way to learn.)"
            $ reward_attributes_once("chef_visit_07_time", [("insight", "micro")], show="auto")
        "It reminds me of your first bowl for me.":
            mc "It reminds me of the first bowl you made me. Simpler, but honest."
            chef "いい評価だ。"
            mc "(That is a good evaluation. He smiles, just a little.)"
            chef "正直、一番。"
            mc "(Honesty is first. That is what he has been teaching all along.)"
            $ reward_attributes_once("chef_visit_07_honest", [("grace", "micro")], show="auto")

    "Chef reaches under the counter and takes out a small wrapped package."
    "He sets it in front of me. It is wrapped in cloth that has absorbed years of broth and steam."

    chef "これ。"
    mc "(This. He is giving me something.)"

    "I unwrap it. It is a pair of chopsticks. Not restaurant chopsticks. Personal chopsticks, made of dark wood, polished by years of use."
    "There is a single character burned into the side: 心."
    "Heart. Or spirit. Or mind. The word means all of them at once."

    chef "私の、昔。"
    mc "(Mine, from before. He used these when he was young.)"
    chef "今、あなたの。"
    mc "(Now, they are yours.)"

    menu:
        "I can't take these. They're yours.":
            mc "I can't take these. They're yours. They have your history in them."
            chef "使わないと、死ぬ。"
            mc "(If they're not used, they die. Chopsticks need hands the way ramen needs customers.)"
            chef "あなたの手で、生きる。"
            mc "(They will live in your hands. That is the gift. Not the wood. The life.)"
            $ reward_attributes_once("chef_visit_07_refuse", [("grace", "micro")], show="auto")
        "I will use them well.":
            mc "I will use them well. I promise."
            chef "約束、いらない。"
            mc "(You don't need to promise. The using is the promise.)"
            chef "ただ、来て。"
            mc "(Just come. That is all he asks. Return, and the chopsticks will have a purpose.)"
            $ reward_attributes_once("chef_visit_07_promise", [("grace", "micro")], show="auto")
        "What does the character mean?":
            mc "What does 心 mean? Heart? Spirit?"
            chef "全部。"
            mc "(All of it. Heart, spirit, mind. The part of you that eats.)"
            chef "食事は、心だ。"
            mc "(A meal is the heart. That is what he believes. Cooking is not technique. It is spirit.)"
            $ reward_attributes_once("chef_visit_07_meaning", [("insight", "micro")], show="auto")

    "I take the chopsticks. The wood is warm from his pocket."
    "They feel alive in my hand, as if they have been waiting for the right hands to hold them."

    "I eat with the new chopsticks. The ramen tastes different somehow."
    "Not because the broth changed. Because I am holding part of Chef's history in my hand."

    chef "うまい、だろ？"
    mc "(Delicious, right? He asks it the same way he did the first time, but now I understand the weight of the word.)"
    mc "Hai. Umai."
    chef "おう。"

    "He grunts, satisfied, and for a moment the shop is only steam and quiet."
    "Then he sets his bowl down. Whatever he was performing for Kenta is over."

    chef "実は、言いたいことがある。"
    mc "(There's something I need to tell you. He says it to the pot, not to me. That is how he says the important things.)"

    chef "店、閉める。"
    mc "(The shop... closes? The word lands harder than it should. The lantern is going out.)"

    menu:
        "Close the shop? Why?":
            mc "You're closing the shop? Why?"
            chef "実家、帰る。"
            mc "(I'm going back to my family home. His parents are getting old. Someone has to be there.)"
            chef "跡継ぎ、いない。"
            mc "(No one to take over. Kenta is still learning — the shop needs more than he has yet.)"
            $ reward_attributes_once("chef_visit_07_why", [("insight", "micro")], show="auto")
        "What about Kenta? He's your apprentice.":
            mc "What about Kenta? He's your apprentice."
            chef "健太は、いい子だ。"
            mc "(Kenta is a good boy. He says it like a verdict and a blessing at once.)"
            chef "でも、まだ早い。"
            mc "(But it's still too early. Thirty years of instinct cannot be handed over in three months.)"
            $ reward_attributes_once("chef_visit_07_kenta", [("grace", "micro")], show="auto")
        "Can't you stay until he learns more?":
            mc "Can't you stay? Just until he learns more?"
            chef "無理だ。"
            mc "(I can't. He says it without anger, only fact. Parents first. Broth second.)"
            chef "親が、待ってる。"
            mc "(My parents are waiting. That is the whole of it.)"
            $ reward_attributes_once("chef_visit_07_stay", [("nerve", "micro")], show="auto")

    kenta "Sensei...?"
    chef "お前の道を、行け。ラーメンは、お前を待ってる。"
    mc "(Walk your own road. The ramen will be waiting for you. He means it as comfort, not promise.)"
    kenta "...Hai."
    "Kenta's shoulders drop. He understood before I did."

    chef "あなたにも、来てほしい。"
    mc "(I want you to come too. The last request. Not an order.)"
    chef "最後の一杯、食べていけ。"
    mc "(Eat your last bowl before you go. That is all he asks.)"

    "I finish the bowl. It is the best he has ever made me, and it is the last."
    "The steam rises between us like it always does. Today I can see all the way through it."
    $ chef_affection += 1

    $ confidant_visits["chef"] = max(confidant_visits.get("chef", 0), 7)
    $ remember("chef", "received his personal chopsticks and learned the shop is closing forever")
    $ queue_message("chef", "The shop closes at the end of the month. That was your last bowl. The chopsticks are yours now — use them well.", day="yesterday")
    $ reward_attributes_once("chef_visit_07_close", [("nerve", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 3.0
    return

label chef_visit_closed:
    scene bg_ramen_shop with walk_fade
    stop music fadeout 2.0
    $ phone_map_visit("ramen_shop")

    "The ramen shop is dark."
    "No steam, no glow from the kitchen, no line at the door. Just the building, holding its shape the way a room holds the shape of everyone who has ever left it."
    "The noren is gone. In its place, a printed notice is taped to the glass."

    "CLOSED. PERMANENTLY.\nThe owner has returned to his family home to care for his parents.\nThank you for the meals.\n— Chef"

    mc "(He wrote it himself. The English is better than his Japanese, which is to say it is not good — but it is his.)"
    mc "(I read it twice. I was looking for a trick. There isn't one. The broth stopped because the man who made it had to go home.)"

    menu:
        "Leave quietly.":
            "Some doors you do not knock on twice. I bow once to the shop and walk on."
            $ reward_attributes_once("chef_visit_closed_leave", [("grace", "micro")], show="auto")
        "Write him a message.":
            mc "I'll send him a message. Tell him the bowl was worth it."
            $ reward_attributes_once("chef_visit_closed_message", [("nerve", "micro")], show="auto")
        "Sit at the counter anyway.":
            "I sit at the counter. The stool remembers my posture. The shop is closed, but it is still his."
            $ reward_attributes_once("chef_visit_closed_sit", [("insight", "micro")], show="auto")

    "Behind the counter, the pots are gone. The recipe notebook is gone. What remains is a room that used to be a promise."
    "I touch the chopsticks through my pocket. 心. They will outlive the shop."
    "Some lanterns go out so that people can find their way home."
    $ chef_affection += 1

    $ confidant_visits["chef"] = max(confidant_visits.get("chef", 0), 8)
    $ remember("chef", "found the ramen shop permanently closed; he had gone home to care for his parents")
    $ queue_message("chef", "If you are reading this: the shop is closed for good. The parents need me more than the pots do. The broth was never mine anyway — it belonged to everyone who ate it.", day="yesterday")
    $ reward_attributes_once("chef_visit_closed_close", [("grace", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 3.0
    return
