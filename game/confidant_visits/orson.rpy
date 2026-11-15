################################################################################
## ORSON — LUPIN'S DEN
################################################################################
##
## Visit 1 happened in script.rpy, on the wrong turn home from the library:
## the water on the house, "you found us," and the wooden bowl for notes. The
## arc after that lives here, written from the files under
## documentation/Locations/Bar - Orson/. This file currently holds visit 2 —
## the masks explained, the first real advice, and the first phrase he teaches.
## Visits 3-7 are still stubs: the hub simply lets the afternoon continue, the
## same way every unwritten place behaves.

label confidant_visit_orson:
    $ visit = confidant_visits.get("orson", 0)
    if visit == 1:
        jump orson_visit_02
    elif visit == 2:
        jump orson_visit_03
    elif visit == 3:
        jump orson_visit_04
    elif visit == 4:
        jump orson_visit_05
    elif visit == 5:
        jump orson_visit_06
    elif visit == 6:
        jump orson_visit_07
    return

label orson_common_open:
    scene bg_lupins_den with walk_fade
    stop music fadeout 1.2
    play music "audio/Music/(Orsons bar) the_corner_booth.mp3" fadein 2.0
    return

label orson_visit_02:
    call orson_common_open

    "It is later than last time. The bar hums softly, and neon leaks in through the frosted window in colors that don't quite belong to the room."
    "I hesitate at the door for a second longer than I mean to. Then I slide onto the narrow bench."
    "The Master glances over from his polishing, a wolf mask with a warm grin and yellow accents set into the fur."
    bar_master "Back again, hm? That bench didn't scare you off after all."
    "He tilts his head."
    bar_master "Where're you from? Accent's not from around here."

    menu:
        "\"I'm from... somewhere far.\"":
            mc "I'm from... somewhere far."
            "The wolf mask tilts the other way, reading me the way he read the glass."
            $ reward_attributes_once("orson_visit_02_origin", [("nerve", "micro")], show="auto")
        "\"A little bit from everywhere.\"":
            mc "A little bit from everywhere."
            bar_master "Everywhere's a good answer."
            $ reward_attributes_once("orson_visit_02_everywhere", [("grace", "micro")], show="auto")

    bar_master "Tokyo's made of people from everywhere, pretending they're from here."
    "He sets down a coaster with a tiny wolf logo and slides it toward me, then looks at me properly for the first time."
    bar_master "Anything you don't want? Sweet, sour, boozy, gentle?"

    menu:
        "\"Surprise me.\"":
            mc "Surprise me."
            bar_master "Then you get the house guess. Hold still."
            $ reward_attributes_once("orson_visit_02_surprise", [("nerve", "micro")], show="auto")
        "\"Something light. Still new to this.\"":
            mc "Something light. Still new to this."
            bar_master "Good answer. Light is honest. It doesn't hide what it is."
            $ reward_attributes_once("orson_visit_02_light", [("grace", "micro")], show="auto")

    "He works unhurried. Ice clinks against glass. Citrus zest curls into the drink in one long ribbon, and the smell changes the room slightly."
    "He nudges the glass forward."
    bar_master "You know why the masks? It's not a gimmick. It's permission."
    bar_master "Some folks need armor to speak freely. Some need to hide to tell the truth."
    mc "I look at the fox at the end of the bar, still laughing at nothing. The rabbit, gone now, replaced by a goat in a flat cap."
    bar_master "You don't have to be anyone here. That includes trying too hard to be yourself, if that makes sense."
    mc "I'm... still figuring out who that is, here."
    bar_master "Good. Don't rush it. Tokyo's a marathon with no finish line."
    bar_master "First rule for newcomers: keep an eye on the last train. Miss it and this city tests you fast."
    "He points toward the wall clock, the way you'd point out a floor that's about to give way."
    bar_master "Second rule: if you can't say it, write it. A napkin sketch, a translation app, a smile."
    bar_master "Communication's more than words."

    "A pair of masked regulars laugh near the jukebox, too loudly, and nobody minds. Orson lowers his voice without being asked."
    bar_master "Also, don't confuse silence with judgment. In Japan, quiet often means kindness,"
    bar_master "giving you space not to fail in public."
    "I feel like I'm always one step behind. I say it before I can decide not to."
    bar_master "Then take smaller steps. Order the same drink twice. Learn one new phrase a night."
    bar_master "Decide which convenience store clerk you'll always say 'good evening' to."
    bar_master "We belong to places that notice us back."

    "The drink is good. Not great, not trying — good, the way water is good."
    bar_master "Finish that, and I'll teach you how to say 'refill, please' without sounding like a tourist."

    menu:
        "\"Teach me.\"":
            mc "Teach me."
            bar_master "おかわり、お願いします。 Okawari, onegaishimasu."
            bar_master "Soft on the 'ri.' You'll charm half the city."
            $ reward_attributes_once("orson_visit_02_teach", [("grace", "micro")], show="auto")
        "\"Maybe next time.\"":
            mc "Maybe next time."
            bar_master "Next time it is. Coming back is its own kind of courage."
            $ reward_attributes_once("orson_visit_02_nexttime", [("nerve", "micro")], show="auto")

    "The glass goes empty at some point. He refills it before I have to ask, which I notice and file away."
    "When I leave, my shoulders are a little less tense than when I came in."
    "The door cloth swings shut behind me. Inside, the jazz keeps going like nothing happened."
    "Which, I realize, is the whole point of the place."

    $ orson_affection += 1
    $ confidant_visits["orson"] = max(confidant_visits.get("orson", 0), 2)
    $ remember("orson", "he explained the masks and taught him 'okawari onegaishimasu'")
    $ queue_message("orson", "You left before the last train again. Good. The city tests people who miss it — you're still passing.", day="yesterday")
    $ reward_attributes_once("orson_visit_02_close", [("grace", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return

label orson_visit_03:
    call orson_common_open

    "The bar is busier tonight. The low light glows against rows of bottles."
    "I slide onto the now-familiar bench, and Orson nods, already reaching for the citrus."
    bar_master "Regular's posture. You sit like the seat knows you."
    "He sets the first drink down."
    bar_master "I trade drinks for stories. Want some?"

    menu:
        "\"Go on.\"":
            mc "Go on."
            bar_master "There was a tourist couple, arguing about the map like it was the last lifeboat on a sinking ship. I gave them two paper cranes and asked them to fold a third together."
            bar_master "They kept the cranes, stopped fighting, and sent me a postcard from Kyoto."
            "He shrugs."
            bar_master "People don't always need answers. Sometimes they just need a small task to remember they're on the same team."
            $ reward_attributes_once("orson_visit_03_story", [("grace", "micro")], show="auto")

    mc "And locals?"
    bar_master "A poet who hasn't published. A barista who hates coffee but loves steam. A nurse who laughs too loud because the hospital is too quiet."
    bar_master "Japan is... polite, yes. But under that, it's a mess, tender, stubborn, funny. Like everywhere else, just wearing formal shoes."
    "I let out a small laugh."
    mc "That... helps."
    "He leans in, his voice dropping."
    bar_master "Carry a tiny notebook. Write down three moments each day that felt real: a dog in a raincoat, the station melody, an old man feeding crows."
    bar_master "When the city feels too big, your pages make it small again."

    menu:
        "\"I'll try that.\"":
            mc "I'll try that."
            bar_master "Good. Memory needs a home."
            $ reward_attributes_once("orson_visit_03_notebook", [("grace", "micro")], show="auto")
        "\"I'll just live it.\"":
            mc "I'll just live it."
            bar_master "Then live it—but don't forget it. Same difference, different discipline."
            $ reward_attributes_once("orson_visit_03_live", [("nerve", "micro")], show="auto")

    "He slides over a small bowl of edamame."
    bar_master "Eat. Drinking without eating is like sightseeing without looking up."
    "I crack a pod open. The bar's noise swells and softens like a tide."
    "When I leave, the door cloth swings shut, and the night carries the scent of gin and soy sauce with me."

    $ orson_affection += 1
    $ confidant_visits["orson"] = max(confidant_visits.get("orson", 0), 3)
    $ remember("orson", "heard a story about paper cranes and was told to carry a notebook")
    $ queue_message("orson", "Write three moments each day. When the city feels too big, your pages make it small again.", day="yesterday")
    $ reward_attributes_once("orson_visit_03_close", [("insight", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return

label orson_visit_04:
    call orson_common_open

    "It's a slow night. Rain taps the window in a steady rhythm."
    "Orson pours two modest servings and keeps one for himself, something I've never seen him do before."
    bar_master "I used to be a 'normal' person. Dress shoes, morning trains, meetings that used words like 'synergy' with a straight face."
    bar_master "I was good at it. That was the problem."

    mc "So... why did you leave that life behind?"

    bar_master "Because, being good at something and being alive inside it are different things."
    "He swirls his glass, watching the liquid catch the light."
    bar_master "I wanted change. I wanted... not to count years by fiscal quarters. I failed some expectations. Then I succeeded at failing them."
    bar_master "Also I learned that the only constant in life is change. Whether it's good or bad is up to you."
    "There's a smile in his voice now."
    bar_master "This place is the result. A third space. Not home, not work. It's a place where you can exhale."

    mc "I'm still figuring out where I fit."

    bar_master "That's honest. Here's a Tokyo trick: choose a few 'anchors'. A coffee shop you claim. A park bench you check in with weekly. A train line you ride for no reason."
    bar_master "Belonging grows from repetition."

    menu:
        "\"It feels fake to force it.\"":
            mc "It feels fake to force it."
            bar_master "Everything feels fake until it's familiar. Familiarity is just time you decide to spend."
            $ reward_attributes_once("orson_visit_04_fake", [("nerve", "micro")], show="auto")
        "\"I like the idea of anchors.\"":
            mc "I like the idea of anchors."
            bar_master "Good. Anchors don't stop the tide; they stop you from drifting."
            $ reward_attributes_once("orson_visit_04_anchors", [("insight", "micro")], show="auto")

    "After a beat, he speaks again."
    bar_master "Tonight I'll ask you one thing: what surprised you most about Japan so far. Good or bad?"

    menu:
        "\"The quiet.\"":
            mc "The quiet."
            # Naming a pattern in the place, not just a feeling about it.
            $ reward_attributes_once("orson_visit_04_quiet", [("insight", "micro")], show="auto")
        "\"The kindness.\"":
            mc "The kindness."
            # Choosing to see the people, not only the strangeness.
            $ reward_attributes_once("orson_visit_04_kindness", [("grace", "micro")], show="auto")
        "\"How different it is.\"":
            mc "How different it is."
            # Admitting the distance out loud instead of pretending it is small.
            $ reward_attributes_once("orson_visit_04_different", [("nerve", "micro")], show="auto")

    bar_master "Keep noticing. Noticing is the first kindness we give a place."
    "He raises his glass slightly. The rain keeps time against the glass."
    "When I leave, the rain has slowed to a drizzle, and the city feels smaller somehow."

    $ orson_affection += 1
    $ confidant_visits["orson"] = max(confidant_visits.get("orson", 0), 4)
    $ remember("orson", "learned about his past life and the concept of anchors")
    $ queue_message("orson", "Everything feels fake until it's familiar. Familiarity is just time you decide to spend.", day="yesterday")
    $ reward_attributes_once("orson_visit_04_close", [("nerve", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return

label orson_visit_05:
    call orson_common_open

    "The bar is lively tonight, laughter ricocheting between tables."
    "Orson spots me and claims the usual bench with a small flourish."
    bar_master "Look at you. Shoulders are lighter. Eyes are less 'help-I'm-astronaut-in-a-convenience-store.' Progress."

    mc "I'm learning... slowly."

    bar_master "Slow is the speed of everything worth keeping."
    "He slides over a glass and a tiny dish of yuzu peel."
    bar_master "Let me guess, you've had days that felt like you said everything wrong."

    mc "All of them."

    bar_master "Good. You're practicing. Loneliness doesn't vanish, get used to that. But it gets... companionable."
    bar_master "Learn small rituals: greet the same crossing guard, memorize a vending machine, bow at the shrine even if you don't know the words."
    bar_master "Routines let the city recognize you."

    mc "Routines feel... safe, I guess."

    bar_master "And safety lets you be brave elsewhere."
    "He leans on the counter."
    bar_master "Practical notes: if you end up doing バイト（baito）, bring a little notebook for shift phrases. Keep coins for bus fare. Last trains are sacred."
    bar_master "Never block the escalator right side. And if you don't know, copy the elderly. They always know, haha."

    mc "I'll remember the copying rule."

    bar_master "And remember: you can ask for help. The trick is asking in the smallest possible way. People here love to help if you make it easy for them to succeed."

    menu:
        "\"Thanks... that helps.\"":
            mc "Thanks... that helps."
            bar_master "Good. Let it help."
            $ reward_attributes_once("orson_visit_05_helps", [("grace", "micro")], show="auto")
        "\"It still feels hard.\"":
            mc "It still feels hard."
            bar_master "Of course it's hard. Worthwhile things are heavy. Carry them with both hands."
            $ reward_attributes_once("orson_visit_05_hard", [("nerve", "micro")], show="auto")

    "A moment of companionable silence as the bar noise blurs into a warm hum."
    "When I leave, the laughter follows me out the door, fading as I step into the night."

    $ orson_affection += 1
    $ confidant_visits["orson"] = max(confidant_visits.get("orson", 0), 5)
    $ remember("orson", "received practical advice about routines and asking for help")
    $ queue_message("orson", "Routines let the city recognize you. Safety lets you be brave elsewhere.", day="yesterday")
    $ reward_attributes_once("orson_visit_05_close", [("grace", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return

label orson_visit_06:
    call orson_common_open

    "It's near closing. Only a couple of customers remain."
    "Orson moves more slowly tonight; the wolf mask's smile looks almost thoughtful in the low light."
    "The shelves behind him are a little emptier than usual, one or two bottles missing from their usual places."
    bar_master "Have you ever noticed how doors look heavier at night? Same wood, same hinges but just... heavier."
    bar_master "Funny thing about doors: they never promise they'll open forever. You just assume they will."

    mc "Long day?"

    bar_master "Long year."
    "He sets down a small, neat drink, pausing before sliding it across."
    bar_master "I tried other lives. My family wanted me in the company—good hours, good title. I tried my own shop once. Bad location, worse timing."
    bar_master "I've failed politely and loudly. This place... was desperation dressed as a plan. A corner where failure could sit down and order a drink."

    mc "And it worked."

    bar_master "Sometimes. Sometimes it barely limps. Bars are fragile things—you keep them alive night by night. Like a candle in the wind, you don't know how long the wax will last."
    "He catches himself, then chuckles to break the heaviness."
    bar_master "But hey, tonight it's still burning."

    mc "I don't feel courageous."

    bar_master "You came back. Courage doesn't always roar; sometimes it just shows up again."
    "He reaches under the counter and hands out a paper coaster with the wolf logo."
    bar_master "Here. For when the city feels too big. A silly souvenir, but... you'd be surprised how much meaning fits in small circles."
    bar_master "Small things outlive us sometimes."

    "I turn it in my hand."
    mc "Thanks."

    bar_master "I see you, you know. Not every detail. Just enough to know you're trying. You remind me of the kid I was when I first came to Tokyo."
    bar_master "Lost, stubborn, curious. Curiosity will keep you alive here. Even when places don't."

    menu:
        "\"I'll keep showing up.\"":
            mc "I'll keep showing up."
            bar_master "That's the whole game. Keep showing up! Wherever the game happens to be."
            $ reward_attributes_once("orson_visit_06_showup", [("nerve", "micro")], show="auto")
        "\"I'm still scared.\"":
            mc "I'm still scared."
            bar_master "Good. Fear keeps your eyes open. Just don't let it keep your feet still."
            $ reward_attributes_once("orson_visit_06_scared", [("grace", "micro")], show="auto")

    "He looks down the bar, then back. There's a softness in his voice that wasn't there before."
    bar_master "Finish that. Walk home slow. Notice three good things. Bring them back to me next time."
    bar_master "...Every night's different, and we never know how many more we'll get."
    "The lights dim slightly. One of the neon signs outside flickers, buzzing. The night exhales."
    "When I leave, the coaster sits in my pocket, warm against my palm."

    $ orson_affection += 1
    $ confidant_visits["orson"] = max(confidant_visits.get("orson", 0), 6)
    $ remember("orson", "received a wolf coaster and learned about the fragility of the bar")
    $ queue_message("orson", "Every night's different, and we never know how many more we'll get. Make them count.", day="yesterday")
    $ reward_attributes_once("orson_visit_06_close", [("insight", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return

label orson_visit_07:
    call orson_common_open

    "The bench that once felt too narrow now seems made for me."
    "The air carries the warm scent of citrus and gin, but tonight there's a subtle heaviness, as if the room itself knows this is a final chapter."
    "The last customers have already gone. The bar is quiet, dim, only the hum of the fridge and the soft buzz of neon outside."
    "Orson leans against the bar, polishing a glass, his wolf mask tilted low in thought."
    bar_master "You've grown a lot since that first night. Back then you barely looked at me. Now you sit like the bar was built around you."

    mc "I do feel like I belong here."

    bar_master "That's the trick of places like this. You find a rhythm, and suddenly it feels permanent. But..."
    "He sets the glass down, hands lingering on the counter."
    bar_master "This place won't be around much longer."

    mc "...What do you mean?"

    bar_master "It's not one thing. It's all of it. Rent that keeps rising. A neighborhood that's sprinting ahead without me. Too many nights when the till doesn't quite balance."
    bar_master "And me... I'm tired. More tired than I let on."

    mc "But you built something real here. For people like me."

    bar_master "I built it as a refuge. A place where people could breathe. Where being hidden meant being seen in a different way."
    bar_master "I thought if I gave others that freedom, maybe I'd feel it too."
    "He looks around the dim bar—the shelves, the lights, the empty stools."
    bar_master "But sometimes even the places we love most can't hold us up forever. The city doesn't wait. It just keeps moving."

    mc "What do you mean..? So this... is goodbye?"

    bar_master "Not the kind that erases anything. Endings don't erase what happened. You came here. You made this place alive. That doesn't vanish."
    "He leans forward, steady and deliberate."
    bar_master "You reminded me why I kept these doors open. Not for money. For moments like this. For people like you."

    menu:
        "\"I'll miss this place.\"":
            mc "I'll miss this place."
            bar_master "Good. Missing something means it mattered. It means it left its mark."
            $ reward_attributes_once("orson_visit_07_miss", [("grace", "micro")], show="auto")
        "\"I'll carry it with me.\"":
            mc "I'll carry it with me."
            bar_master "Exactly. The bar, the mask, the laughter—they're just tools. What you really take with you is the warmth, the courage, the lessons. That's what lasts."
            $ reward_attributes_once("orson_visit_07_carry", [("nerve", "micro")], show="auto")

    "There's silence. Orson studies me for a long moment."
    "Then he exhales slowly and reaches up. For the first time, he pulls the wolf mask free."
    "The sound of it leaving his face is strangely final. He sets it on the counter, eyes bare and tired, but kind."
    bar_master "I don't do this for anyone. But you... you deserve to see me, not just the mask."
    "He reaches under the counter, produces a small badge shaped like a wolf's paw print, edges slightly worn as if it's been carried for years. He slides it across the bar."
    bar_master "Here. Something to remember me by. Might not look like much, but sometimes the smallest things carry the most weight."

    "I turn it in my hand."
    mc "I'll keep it safe."

    bar_master "Don't keep it too safe. Carry it. Let it remind you. One day, you'll walk into a place like this, and you won't need me."
    bar_master "You'll be part of the warmth yourself. Maybe even be the reason someone else feels at home."
    "The bar is utterly still now. Orson leans back, mask beside him, the wolf paw badge warm in my hand."
    "His eyes glimmer—not with mystery, but with raw gratitude and the quiet weight of farewell."
    "When I finally stand to leave, the door closes behind me with a soft thud. The hum of the bar lingers in memory, warm and fleeting, already almost gone."

    $ orson_affection += 1
    $ confidant_visits["orson"] = max(confidant_visits.get("orson", 0), 7)
    $ remember("orson", "said goodbye to Orson and received his wolf paw badge")
    $ queue_message("orson", "The bar is closing, but what we built here stays. You became part of the warmth yourself. That's the point.", day="yesterday")
    $ reward_attributes_once("orson_visit_07_close", [("nerve", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return
