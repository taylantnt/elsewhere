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

    "Broth, and steam, and fat hitting a hot pan behind a wall. My whole body turns towards it before I have decided anything."
    "A doorway with a cloth over it, dark blue and gone soft at the hem. A bowl painted on it in white. No glass, no sign I can read."
    "I lift the cloth and go in."



    "It is four seats and a counter and a wall of steam, and the steam is the only thing in here that moves."
    "There is one man behind the counter, in an apron and a towel tied around his head, and he does not look up."
    "The board on the wall is handwritten and I cannot read one character of it."
    "Under it, the prices in numbers, which everybody can read."
    "I put a thousand yen on the counter. He does not look at it."
    "He pushes it back with one finger and grunts at the empty space in front of the seat, which I take to mean afterwards."

    voice "audio/VO/ramen_welcome.mp3"
    chef "いらっしゃい。"
    mc "(I know that one. Every shop in this country says it when a person walks in. It means welcome, and it means get on with it.)"

    # How he orders. All three roads end in the same bowl, because the chef is the
    # one steering and the protagonist has none of the language; what the player is
    # actually choosing is what kind of person he is when he cannot be understood.
    menu:
        "Order in English.":
            mc "Uh... hi. Ramen, please?"
            "He looks at me properly for the first time, about a second, and then he waves at the board. The whole board."
            mc "(That was not a no. That was him telling me that the menu is the menu.)"
            # Speaking first in a language he does not have yet.
            $ reward_attributes_once("answer_ramen_english", [("nerve", "micro")], show="auto")
        "Point at something.":
            mc "(Right. Fine. This is the part where I point.)"
            "I point at a line. Any line. The second one down, because I have seen one of its words on a packet in the kitchen."
            "He glances at where my finger is, and then at me, and his face does not move at all."
            # He uses a word he already recognizes to narrow the choice.
            $ reward_attributes_once("answer_ramen_point", [("insight", "micro")], show="auto")
        "Ask for his recommendation.":
            mc "Sumimasen. Osusume... recommendation?"
            "He stops. He looks at me a second longer than he looked at the money, and then says something short to the pots."
            mc "(I might have said that wrong. He points at the second line and waits for my nod.)"
            # Asking a stranger to choose for him is trust, not nerve.
            $ reward_attributes_once("answer_ramen_recommendation", [("grace", "micro")], show="auto")
    
    voice "audio/VO/ramen_ok.mp3"
    chef "あいよ。"
    "He barks something at somebody. There is nobody else in the room. He is the kitchen and the waiter, and he is barking at himself."

    scene bg_ramen with walk_fade
    
    "A few minutes later he puts down a bowl. It is much darker than the picture I had in my head."
    "The broth is almost black. More pork than noodle. And a hill of green onions on top of that which should not be legal."
    mc "(I thought I was ordering something lighter. I don't know what I actually asked for.)"
    "He crosses his arms and looks at it, and then at me, which is a sentence in a language I can read."

    # Both answers lead to the same meal. Restore the counter shot before the
    # chef speaks, so his portrait never covers the food close-up.
    menu:
        "Ask what kind of broth it is.":
            mc "Sumimasen. Shoyu? Miso?"
            "He follows my finger towards the bowl."
            "He points to the dark bottle beside the stove."
            mc "(Soy sauce. That answers that.)"
            "I stop talking. He pushes the bowl half a centimetre towards me with one finger."
            $ reward_attributes_once("answer_ramen_broth", [("insight", "nudge")], show="auto")
            chef "どうぞ。"
            mc "(That one I know. It means here you go. It also means eat it.)"
        "Try it before asking.":
            "I pick up the spoon before I can think about it, which he appears to consider the entire conversation."
            chef "どうぞ。"
            mc "(That one I know. It means here you go. It also means eat it.)"

    "I eat it."
    "The first mouthful hits like something walking into a door. Rich and smoky and far too much. The second is better than the first."
    mc "...This is actually amazing."
    "I say it half under my breath, in English, to nobody."
    "He hears the tone of it even if he does not have the words. He does not turn around."
    chef "うまい、だろ？"
    "One word, said to the pot, in a voice that has clearly said it ten thousand times."
    mc "(No idea what that was. But the way he said it, it sounded like a verdict on the bowl.)"
    menu:
        "Ask what it means.":
            mc "Sumimasen. What does that mean?"
            chef "「うまい。」"
            "He says it again, slower this time, and points at the bowl with the ladle."
            mc "Umai?"
            chef "「うん。うまい。」"
            "He grunts yes and turns back to the pots. That is the lesson."
            # The first word of the language, taught mid-bite by the man who
            # never speaks it. No packet, no sign — he learns it here.
            $ reward_attributes_once("chef_first_umai_meaning", [("insight", "micro")], show="auto")
        "Thank him properly.":
            mc "Arigatou gozaimasu."
            # Meeting him in his language after he hears the reaction.
            $ reward_attributes_once("chef_first_umai_thanks", [("grace", "micro")], show="auto")
        "Ask what gives it the smoky flavour.":
            mc "The pork? Is that where the smoky taste comes from?"
            "He taps the edge of the grill with his ladle."
        "Point at the bottle and wait for him to name it.":
            "I point at the bottle with the spoon. He says the word again, slower this time, and watches to see if I got it."

    "He snorts. A small sound, killed immediately. Something in his face moves for a quarter of a second before he turns back to the pots."
    "He says nothing else. I slurp, badly, and get broth on the counter, and he does not comment."
    "I am fairly sure that is the compliment."

    # The meal continues in the shop. No more choices, just the eating, and the
    # room around it. Every route comes back through the same empty bowl, the
    # same bill, and the same walk home.
    scene black with walk_fade
    "Two men come in while I eat. They sit at the other end of the counter without speaking, and the chef puts two bowls down without looking at either of them."
    "I watch how they hold their chopsticks and try the same grip. It is not the grip I know."
    "Chopsticks in one hand, spoon in the other, head down over the bowl. They eat the way this country eats, and I copy it badly, and neither of them looks up."
    "I finish the whole bowl. Soup and all. There is nothing left in it but the pattern on the bottom, and I am surprised by how much I want there to be."

    scene bg_ramen_empty with Dissolve(2.0)

    "When I finish I put the thousand yen back on the counter."
    "This time he takes it, counts the change without looking, and sets it beside my hand."
    $ spend_money(900)
    "A hundred yen. Nine hundred for the bowl. I do not know what I actually ordered and I do not think I ever will."
    mc "(Not what I expected. I'd order it again.)"

    $ confidant_visits["chef"] = 1
    $ remember("chef", "sat down in his shop and finished the bowl")

    # Back to the counter shot for this, for the same reason the whole scene
    # works this way: he does not say anything that is not sitting in front of
    # him, and this is going to happen across a counter. The fade is also what
    # gives the memory notice above its full time on screen before the phone
    # takes the whole frame.
    scene bg_ramen_shop with walk_fade

    "He has been looking at the phone on the counter since I put the money down."
    chef "「WIRE、やってるか」"
    "Two English sounds, dropped into a Japanese sentence, at the exact volume of the pots."
    mc "(I caught the English sounds and none of the Japanese. I nod anyway.)"
    mc "Yeah. Hikari put it on here. My host sister. She set the whole thing up before I landed."
    "He grunts, which is what he does instead of a nod."
    "Then he turns a small laminated card round on the counter so that it is facing me."
    "A black square made out of smaller black squares. Under it, six words in English, in handwriting that is not his."
    chef "「読め」"
    mc "(He wants me to scan it. I know the gesture without knowing the word.)"
    "I hold the phone over the card. The app takes it without asking me anything, and puts a name on the list."
    mc "So I know if you're shut before I walk down here for nothing."
    "He turns the card back round and goes to the pots, which is the conversation over."
    $ wire_unlock("chef")
    # The shop's only broadcast, sent while the phone still has no data. It
    # waits in the queue until the line goes live the next day.
    $ queue_message("chef", "新メニュー。900円。水曜日は休み。", day="yesterday")
    # Forced closer for the walk route. Finding the shop by getting lost is the
    # Insight beat that matches the run's Nerve and the club's Grace.
    $ reward_attributes_once("walk_first_found", [("insight", "small")], show="card")
    $ chef_affection += 1

    mc "(Home. Four minutes. Let's see if I can find it twice.)"
    "I come out from under the cloth and the street is dark, and I know exactly where I am."
    "Those two convenience stores are twenty metres away."
    mc "(That sign. That one there. I know that street.)"
    mc "(I was on it this morning, on the way to school, and I did not look at it once.)"
    "Home is four minutes away and it took me an hour to do it, and I would do it again exactly the same way."
    mc "(I found a ramen shop. I found it by getting lost, which means it was always findable. It was there the whole time.)"

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
            mc "(A word I half-know, said slowly for my benefit. The broth, I think.)"
            chef "朝から。"
            mc "(Something about the morning. The gesture says the rest: all day.)"
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
    mc "(Rest and work, in the same sentence. He says it like a rule. I will ask Hikari what he meant.)"
    $ chef_affection += 1

    $ confidant_visits["chef"] = max(confidant_visits.get("chef", 0), 2)
    $ remember("chef", "learned that resting is also work and had tonkotsu ramen")
    $ queue_message("chef", "スープは十二時間。残りは二日。どちらも一杯のうちに入っている。", day="yesterday")
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
        "Tell them the second line, then let them taste why.":
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
    mc "(Something about English, and students. I helped, and there is an egg. I take the win.)"

    menu:
        "I was just being helpful.":
            mc "I was just being helpful. They were confused."
            chef "助けるのは、いいことだ。"
            mc "(Helping is a good thing. Simple. True.)"
            $ reward_attributes_once("chef_visit_03_humble", [("grace", "micro")], show="auto")
        "I like watching people find good food.":
            mc "I like watching people find good food. It feels like sharing a secret."
            chef "秘密じゃない。"
            mc "(He says it isn't a secret. I know that much. The rest is his face.)"
            chef "でも、嬉しい。"
            mc "(Something about being glad. That word I know.)"
            $ reward_attributes_once("chef_visit_03_share", [("insight", "micro")], show="auto")
        "Did you see them enjoying it?":
            mc "Did you see them enjoying it?"
            chef "見てた。"
            mc "(He says he was watching. I can tell from the way he says it.)"
            chef "最初、分からない。後、分かる。"
            mc "(Something about before and after, and understanding. He says it like it is how the world works. I will ask Hikari.)"
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
    $ queue_message("chef", "学生たちが昨日戻ってきた。日本語で注文した。下手だが、日本語だ。それでも進歩だ。", day="yesterday")
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
            mc "(Every day, he says. A little. That much I can follow.)"
            chef "同じじゃ、つまらない。"
            mc "(Same, boring. Two words I know. He says the rest with a shake of the ladle.)"
            $ reward_attributes_once("chef_visit_04_change", [("insight", "micro")], show="auto")
        "What are you trying to improve?":
            mc "What are you trying to improve?"
            chef "バランス。"
            mc "(Balance. That word I know. The rest is in how he tastes the spoon.)"
            chef "昨日、濃かった。今日、薄くする。"
            mc "(Yesterday, today. Stronger, lighter. I understand the shape of it, not the sentence.)"
            $ reward_attributes_once("chef_visit_04_improve", [("insight", "micro")], show="auto")
        "How long have you been making ramen?":
            mc "How long have you been making ramen?"
            chef "三十年。"
            mc "(Thirty years. The number I understand. The rest is in his face.)"
            chef "まだ、分からない。"
            mc "(Still don't understand, he says. After thirty years. Kenta writes it down.)"
            $ reward_attributes_once("chef_visit_04_time", [("grace", "micro")], show="auto")

    "Chef takes the notebook back and turns to a blank page."
    "He writes today's date. Then he writes three Japanese characters: 味, 香, 色."
    "Taste, aroma, color. The three things a bowl must have."

    chef "味は、一番大事。"
    mc "(Taste, first. I can read the character in the notebook even if I can't follow the sentence.)"
    chef "でも、香も大事。色も大事。"
    mc "(He points at the other two characters. Aroma, color. The notebook does the translating.)"

    menu:
        "What about the texture?":
            mc "What about the texture? The way the noodles feel?"
            chef "喉で食べる。"
            mc "(He touches his throat. I understand the gesture, not the sentence.)"
            chef "喉が満足する。"
            mc "(He touches his throat again. The noodles, I think. I am guessing.)"
            $ reward_attributes_once("chef_visit_04_texture", [("insight", "micro")], show="auto")
        "What about the temperature?":
            mc "And the temperature? The heat?"
            chef "熱すぎない。冷たすぎない。"
            mc "(Not too hot. Not too cold. Those two I understand. The rest is in his hands.)"
            chef "体温に近い。"
            mc "(Something about body temperature. He touches his own wrist. I think I follow.)"
            $ reward_attributes_once("chef_visit_04_temp", [("insight", "micro")], show="auto")
        "What makes a bowl perfect?":
            mc "What makes a bowl perfect?"
            chef "完璧なんてない。"
            mc "(No such thing as perfect. I know that word, and I know his face when he says it.)"
            chef "でも、頑張る。"
            mc "(Then something about trying. He taps the notebook. That much I can see.)"
            $ reward_attributes_once("chef_visit_04_perfect", [("grace", "micro")], show="auto")

    "Chef closes the notebook and sets it on the shelf beside the stove."
    "He stands up and goes to the pots. He has not made ramen for me today, but he has made me understand why the ramen is the way it is."

    chef "今日、作らない。"
    mc "(No cooking today, he says. The notebook is open. I think that is the reason.)"
    chef "明日、来て。"
    mc "(Tomorrow. I know that one. He points at the pots, and I understand the rest.)"

    mc "I'll be here."
    chef "おう。"
    "He grunts, satisfied with the promise."
    $ chef_affection += 1

    $ confidant_visits["chef"] = max(confidant_visits.get("chef", 0), 4)
    $ remember("chef", "saw his recipe notebook and learned that he changes the broth every day")
    $ queue_message("chef", "またレシピを変えた。学生たちは気づいた。「違うけど、まだうまい」と言った。それで十分だ。", day="yesterday")
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
    mc "(Tired. That word I know. He says it without complaining.)"
    mc "You should rest."
    chef "後で。"
    mc "(Later. He points at the pots. There is always more to do.)"

    menu:
        "Can I help clean?":
            mc "Can I help clean? I can wipe the counter."
            chef "客は、食べるだけ。"
            mc "(Customers eat. I know those words. The rest is in his face — this is not a debate.)"
            chef "でも、ありがとう。"
            mc "(Thank you — that word I know. He cannot accept, and the refusal is kind.)"
            $ reward_attributes_once("chef_visit_05_help", [("grace", "micro")], show="auto")
        "You work too hard.":
            mc "You work too hard. Even for something you love."
            chef "好きだから、楽しい。"
            mc "(Something about liking it, and fun. I do not follow the logic, but he looks happy.)"
            chef "でも、体、言う。"
            mc "(He touches his chest, then holds up two fingers. Two days. The rest I infer.)"
            $ reward_attributes_once("chef_visit_05_hard", [("insight", "micro")], show="auto")
        "Do you ever think about retiring?":
            mc "Do you ever think about retiring?"
            chef "ない。"
            mc "(No. That one I know.)"
            chef "止まったら、死ぬ。"
            mc "(Stop, die. Two words I know, said together. The rest is in the way he says it.)"
            $ reward_attributes_once("chef_visit_05_retire", [("insight", "micro")], show="auto")

    "Chef brings me a bowl. It is the regular bowl, but there is something different about it today."
    "The broth is richer. The noodles are springier. It is the bowl of a man who found his rhythm and rode it."

    chef "今日、いいだった。"
    mc "(Good, he says, and looks at the empty bowls. I understand that much.)"
    mc "The shop was full."
    chef "うん。"
    mc "(Yeah. He nods, once, the way he does when he has nothing more to say.)"
    $ chef_affection += 1

    $ confidant_visits["chef"] = max(confidant_visits.get("chef", 0), 5)
    $ remember("chef", "saw the shop at its busiest and heard that he will never retire")
    $ queue_message("chef", "スーツの女性が今日も来た。同僚を連れていた。常連になりつつある。店は、俺がやろうがやるまいが育つ。", day="yesterday")
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
    mc "(He introduces the boy with one word. Kenta bows, so I know what it meant.)"
    chef "名前、健太。"
    mc "(Kenta. The name I have heard him say before.)"

    "Kenta bows. Too deeply. Too quickly."
    kenta "Nice to meet you. I mean—はじめまして。"
    chef "もっと、緩く。"
    mc "(Something about being looser. Kenta straightens less. I copy him.)"

    menu:
        "Ask how long he's been learning.":
            mc "How long have you been learning?"
            kenta "Three weeks. I have so much to learn."
            chef "一生、かかる。"
            mc "(A long time, he says. Not unkindly. Kenta nods like he already knew.)"
            $ reward_attributes_once("chef_visit_06_learn", [("insight", "micro")], show="auto")
        "Ask what he's working on.":
            mc "What are you working on today?"
            kenta "Chopping green onions. Chef says my rhythm is wrong."
            chef "リズム、全部。"
            mc "(Rhythm. That word I know from the knife. He says it like it covers everything.)"
            $ reward_attributes_once("chef_visit_06_work", [("insight", "micro")], show="auto")
        "Tell him it takes time.":
            mc "It takes time. I've been coming for months and I still don't understand half of what he says."
            kenta "That makes me feel better."
            chef "時間、かかる。急ぐな。"
            mc "(Time, and not rushing. I know those two words now. The rest is in how he says it.)"
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
            mc "(Something about forgetting and remembering. Kenta writes it down. I copy him.)"
            $ reward_attributes_once("chef_visit_06_forget", [("insight", "micro")], show="auto")
        "Watch Chef, not the notebook.":
            "I want to tell him to look up, but I don't. He has to learn that himself."
            "Chef catches my eye and nods. He knows what I am thinking."
            $ reward_attributes_once("chef_visit_06_watch", [("grace", "micro")], show="auto")
        "Chef, explain what you're doing.":
            mc "Chef, explain what you're doing. For him."
            chef "説明できない。"
            mc "(He says he cannot explain. The shrug says the rest.)"
            chef "感じるしかない。"
            mc "(Something about feeling it instead. He touches his chest. I think that is it.)"
            $ reward_attributes_once("chef_visit_06_explain", [("insight", "micro")], show="auto")

    "The bowl is finished. Chef sets it in front of me."
    "It is perfect. Not just good. Perfect in the way that makes you angry at every other bowl you have ever eaten."

    chef "食べて。"
    mc "(Eat. That one I know. He is not asking.)"

    "I eat. The broth is deeper than before. The noodles have a spring that feels alive."
    "This is not just ramen. This is Chef, distilled into a bowl."

    chef "どう？"
    mc "(How is it? I know that question. He looks at Kenta when he asks.)"
    mc "It's... it's the best one you've ever made me."
    chef "ああ。"
    "He nods, once, satisfied with the truth."

    chef "健太、聞いた？"
    mc "(He says Kenta's name. Kenta listens. I cannot follow the rest.)"
    kenta "I heard."

    chef "一番大事なのは、客の顔。"
    mc "(Something about the customer's face. He points at me. I think I understand.)"
    chef "顔、見れば、分かる。"
    mc "(Then he points at my face again. The lesson is in the gesture.)"
    $ chef_affection += 1

    $ confidant_visits["chef"] = max(confidant_visits.get("chef", 0), 6)
    $ remember("chef", "met his apprentice Kenta and ate the best bowl he has ever made")
    $ queue_message("chef", "健太は少しずつ覚えている。包丁さばきが良くなっている。ノートが厚くなっている。忘れ方が始まっている。", day="yesterday")
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
    mc "(The usual. He asks it of Kenta, not me. I know the shape of the question.)"
    mc "Hai. The usual."

    "Kenta nods and goes to the pots. Chef watches him, hands clasped, eyes focused."
    "This is a test. Not for Kenta's sake, but for Chef's."

    "The bowl arrives. It is Kenta's work, but it has Chef's guidance in it."
    "The broth is good. Not perfect, but good. The noodles are firm. The egg is runny in the right way."

    chef "どう？"
    mc "(How is it? I know that much. He waits for my answer.)"

    menu:
        "It's good. He's learning.":
            mc "It's good. He's learning."
            chef "ああ。"
            mc "(Yeah. He nods, satisfied with the praise.)"
            chef "まだ、遠い。でも、進んでる。"
            mc "(Far, he says, and then something about getting closer. Kenta nods. I think that is praise.)"
            $ reward_attributes_once("chef_visit_07_good", [("grace", "micro")], show="auto")
        "It needs more time.":
            mc "It needs more time. The rhythm isn't quite there yet."
            chef "そうか。"
            mc "(He does not defend him. That much I can see without the words.)"
            chef "健太、聞いた？"
            mc "(Kenta's name again. He says it like a lesson. Kenta listens.)"
            $ reward_attributes_once("chef_visit_07_time", [("insight", "micro")], show="auto")
        "It reminds me of your first bowl for me.":
            mc "It reminds me of the first bowl you made me. Simpler, but honest."
            chef "いい評価だ。"
            mc "(He smiles. Kenta is good. I think that is what he said.)"
            chef "正直、一番。"
            mc "(Honest, he says. One word I know. He has been saying it all week.)"
            $ reward_attributes_once("chef_visit_07_honest", [("grace", "micro")], show="auto")

    "Chef reaches under the counter and takes out a small wrapped package."
    "He sets it in front of me. It is wrapped in cloth that has absorbed years of broth and steam."

    chef "これ。"
    mc "(This. He is giving me something.)"

    "I unwrap it. It is a pair of chopsticks. Not restaurant chopsticks. Personal chopsticks, made of dark wood, polished by years of use."
    "There is a single character burned into the side: 心."
    "Heart. Or spirit. Or mind. The word means all of them at once."

    chef "私の、昔。"
    mc "(Before, he says, and shows me the wood. I understand the gesture.)"
    chef "今、あなたの。"
    mc "(He puts them in my hand. I do not need the words for that.)"

    menu:
        "I can't take these. They're yours.":
            mc "I can't take these. They're yours. They have your history in them."
            chef "使わないと、死ぬ。"
            mc "(Something about using them, or losing them. He gives me a small look. I will use them.)"
            chef "あなたの手で、生きる。"
            mc "(He taps my hand, then the chopsticks. That is the whole sentence, I think.)"
            $ reward_attributes_once("chef_visit_07_refuse", [("grace", "micro")], show="auto")
        "I will use them well.":
            mc "I will use them well. I promise."
            chef "約束、いらない。"
            mc "(No promise, he says. He points at the chopsticks. Use them. I understand.)"
            chef "ただ、来て。"
            mc "(Come, he says. That word I know. The rest is in the way he holds the door.)"
            $ reward_attributes_once("chef_visit_07_promise", [("grace", "micro")], show="auto")
        "What does the character mean?":
            mc "What does 心 mean? Heart? Spirit?"
            chef "全部。"
            mc "(He taps the 心 on the box, then his own chest. I cannot read all of it, but I know which part he means.)"
            chef "食事は、心だ。"
            mc "(Heart again, and cooking. I know those two words. The rest is in how he says it.)"
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
    mc "(Something he needs to say. I do not follow the words, but he says them to the pot, not to me. That is how he says the important things.)"

    chef "店、閉める。"
    mc "(店. Shop. That word I know. The rest I read in his face, and in the lantern going out.)"

    menu:
        "Close the shop? Why?":
            mc "You're closing the shop? Why?"
            chef "実家、帰る。"
            mc "(Family, he says. Parents. Old. Three words I know, and the way he says them is enough.)"
            chef "跡継ぎ、いない。"
            mc "(No one, he says. He looks at Kenta, then at the pots. I understand the shape of it.)"
            $ reward_attributes_once("chef_visit_07_why", [("insight", "micro")], show="auto")
        "What about Kenta? He's your apprentice.":
            mc "What about Kenta? He's your apprentice."
            chef "健太は、いい子だ。"
            mc "(Kenta's name, and a word I think means good. He says it like a verdict.)"
            chef "でも、まだ早い。"
            mc "(Something about too early. Kenta's face falls, so I understand.)"
            $ reward_attributes_once("chef_visit_07_kenta", [("grace", "micro")], show="auto")
        "Can't you stay until he learns more?":
            mc "Can't you stay? Just until he learns more?"
            chef "無理だ。"
            mc "(No, he says. Without anger. He looks at the door, and I think I know why.)"
            chef "親が、待ってる。"
            mc "(Parents. Waiting. Two words I know, and enough.)"
            $ reward_attributes_once("chef_visit_07_stay", [("nerve", "micro")], show="auto")

    kenta "Sensei...?"
    chef "お前の道を、行け。ラーメンは、お前を待ってる。"
    mc "(He says it to Kenta. I cannot work out the words.)"
    kenta "...Hai."
    "Kenta's shoulders drop. He understood before I did."

    chef "あなたにも、来てほしい。"
    mc "(He says my name in among the Japanese. I understand that I am being asked for something.)"
    chef "最後の一杯、食べていけ。"
    mc "(Eat, he says. And one word I know: last. The bowl is set in front of me.)"

    "I finish the bowl. It is the best he has ever made me, and it is the last."
    "The steam rises between us like it always does. Today I can see all the way through it."
    $ chef_affection += 1

    $ confidant_visits["chef"] = max(confidant_visits.get("chef", 0), 7)
    $ remember("chef", "received his personal chopsticks and learned the shop is closing forever")
    $ queue_message("chef", "月末で店を閉める。あれがお前の最後の一杯だった。箸はお前のものだ。大切に使え。", day="yesterday")
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
    # The epilogue can be replayed, so the bookkeeping runs once. Only the
    # scene and its choices come back.
    if confidant_visits.get("chef", 0) < 8:
        $ chef_affection += 1

        $ confidant_visits["chef"] = max(confidant_visits.get("chef", 0), 8)
        $ remember("chef", "found the ramen shop permanently closed; he had gone home to care for his parents")
        $ queue_message("chef", "これを読んでいるなら：店はもう完全に閉めた。両親の方が、鍋よりも俺を必要としている。スープは元々俺のものではなかった。食べた全員のものだ。", day="yesterday")
    $ reward_attributes_once("chef_visit_closed_close", [("grace", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 3.0
    return
