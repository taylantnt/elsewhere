################################################################################
## ORSON — LUPIN'S DEN
################################################################################
##
## Visit 1 happened in script.rpy, on the wrong turn home from the library:
## the wolf-signed door, the accidental step inside, fluent-English reassurance,
## the water on the house, "you found us," the wooden bowl for notes, and the
## WIRE card he scans on the way home. The arc after that lives here, written
## from the files under
## documentation/Locations/Bar - Orson/.
##
## The whole chain is written: visit 2 explains the masks and teaches the first
## phrase; 3 is the notebook; 4 is the anchors and the life before the bar; 5 is
## the routines; 6 is the coaster and the crack in the door; 7 is the night he
## takes the mask off. The bar closes at the end of the arc, so visit 7 is the
## last one the hub will offer.

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
    elif visit >= 7:
        jump orson_visit_closed
    return

label orson_common_open:
    scene bg_lupins_den with walk_fade
    stop music fadeout 1.2
    play music "audio/Music/lupins_den.mp3" fadein 2.0
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
            bar_master "Everywhere's a good answer. Half this city's pretending it's from here."
            $ reward_attributes_once("orson_visit_02_everywhere", [("grace", "micro")], show="auto")

    "He sets down a coaster with a tiny wolf logo and slides it toward me, then looks at me properly for the first time."
    bar_master "Anything you don't want? Sweet, sour, or gentle?"

    menu:
        "\"Surprise me.\"":
            mc "Surprise me."
            bar_master "Then you get the house guess. Hold still."
            $ reward_attributes_once("orson_visit_02_surprise", [("nerve", "micro")], show="auto")
        "\"Something light. Still new to this.\"":
            mc "Something light. Still new to this."
            bar_master "Light's honest. Doesn't hide what it is."
            $ reward_attributes_once("orson_visit_02_light", [("grace", "micro")], show="auto")

    "He works unhurried. Ice clinks against glass. Citrus zest curls into the drink in one long ribbon, and the smell changes the room slightly."
    "He nudges the glass forward."
    bar_master "With a mask, you can be anyone. Even yourself, if you're lucky."
    bar_master "Just… don't expect people to be the same without it."
    "I look at the fox at the end of the bar, still laughing at nothing. The rabbit, gone now, replaced by a goat in a flat cap."
    bar_master "You don't have to be anyone here. That includes trying too hard to be yourself, if that makes sense."
    mc "I'm... still figuring out who that is, here."
    bar_master "Don't rush it. Nobody here's keeping score."
    bar_master "Mind the last train. Miss it and the city tests you."

    "He points toward the wall clock, the way you'd point out a floor that's about to give way."
    bar_master "Our Friday fellow — fox mask, third whisky, cries into it, swears it's the onions."

    "A pair of masked regulars laugh near the jukebox, too loudly, and nobody minds. Orson lowers his voice without being asked."
    "I feel like I'm always one step behind. I say it before I can decide not to."
    bar_master "Smaller steps, then. Same drink twice — see what sticks."

    "The drink is good. Not great, not trying — good, the way water is good."
    bar_master "Finish that, and I'll teach you 'refill, please' without the tourist voice."

    menu:
        "\"Teach me.\"":
            mc "Teach me."
            bar_master "おかわり、お願いします。 Okawari, onegaishimasu — soft on the 'ri,' you'll charm half the city."
            $ reward_attributes_once("orson_visit_02_teach", [("grace", "micro")], show="auto")
        "\"Maybe next time.\"":
            mc "Maybe next time."
            bar_master "Next time, then. Coming back's its own kind of courage."
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

    "The bar is busier than I have seen it. Two stools are taken by people in masks who do not turn around."
    "Orson nods at the bench. He is already reaching for the citrus."
    bar_master "You sit like the seat knows you."
    "He sets the first drink down."
    bar_master "I trade drinks for stories. The drinks are better."

    menu:
        "\"Go on.\"":
            mc "Go on."
            bar_master "A couple came in with a map and a fight. I gave them two paper cranes and told them to fold a third."
            bar_master "They stopped fighting because folding is hard."
            "He shrugs."
            bar_master "They sent a postcard from Kyoto. I do not know why. The fight was not mine."
            mc "That's a good story."
            $ reward_attributes_once("orson_visit_03_story", [("grace", "micro")], show="auto")

    mc "And the locals?"
    bar_master "A poet who will not publish. A barista who hates coffee. A nurse who laughs too loud. The hospital is quiet."
    bar_master "People think Japan's polite. It is — right up till the mess shows up in formal shoes. People come here to be seen without being recognised."
    "I laugh before I can stop myself."
    mc "That helps."
    "He leans in, not far."
    bar_master "Carry something to write on. A receipt's enough — three things a day that were actually there. When the city gets too big, read them back."

    menu:
        "\"I'll try that.\"":
            mc "I'll try that."
            bar_master "Memory needs somewhere to sit."
            $ reward_attributes_once("orson_visit_03_notebook", [("grace", "micro")], show="auto")
        "\"I'll just live it.\"":
            mc "I'll just live it."
            bar_master "Then live it twice — once when it happens, once when you write it."
            $ reward_attributes_once("orson_visit_03_live", [("nerve", "micro")], show="auto")

    "He slides over a small bowl of edamame."
    "I crack a pod open. The bar's noise rises and falls like a tide."
    "When I leave, the door cloth swings shut, and the night carries the smell of gin and soy sauce with me."

    $ orson_affection += 1
    $ confidant_visits["orson"] = max(confidant_visits.get("orson", 0), 3)
    $ remember("orson", "heard a story about paper cranes and was told to carry a notebook")
    $ queue_message("orson", "Write three things a day that were actually there. When the city gets too big, the pages make it small again.", day="yesterday")
    $ reward_attributes_once("orson_visit_03_close", [("insight", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return

label orson_visit_04:
    call orson_common_open

    "Rain on the window. The bar is empty except for us and the fox mask at the end of the counter."
    "Orson pours two. He has never poured himself one."
    bar_master "I had a different life. Shoes that hurt. A train I did not choose. Meetings where the words meant nothing and the silence meant less."
    mc "Why did you leave?"
    bar_master "I was good at it. That is not the same as being alive in it."
    "He drinks. He does not look at me."
    bar_master "I failed some expectations. Then I got good at failing them. This place is what was left."
    mc "It doesn't look like what was left."

    mc "I'm still figuring out where I fit."
    bar_master "Pick a few places and keep going back. Belonging's just repetition — nothing more romantic than that."

    menu:
        "\"It feels fake to force it.\"":
            mc "It feels fake to force it."
            bar_master "Feels fake till it's familiar. Then it's yours."
            $ reward_attributes_once("orson_visit_04_fake", [("nerve", "micro")], show="auto")
        "\"I like the idea of anchors.\"":
            mc "I like the idea of anchors."
            bar_master "Anchors don't stop the tide. They stop you drifting."
            $ reward_attributes_once("orson_visit_04_anchors", [("insight", "micro")], show="auto")

    "After a while he speaks again."
    bar_master "One thing. What surprised you most about this country. Good or bad."

    menu:
        "\"The quiet.\"":
            mc "The quiet."
            $ reward_attributes_once("orson_visit_04_quiet", [("insight", "micro")], show="auto")
        "\"The kindness.\"":
            mc "The kindness."
            $ reward_attributes_once("orson_visit_04_kindness", [("grace", "micro")], show="auto")
        "\"How different it is.\"":
            mc "How different it is."
            $ reward_attributes_once("orson_visit_04_different", [("nerve", "micro")], show="auto")

    "He raises his glass a little. The rain keeps time against the window."
    "When I leave, the rain has slowed to a drizzle, and the city feels smaller."

    $ orson_affection += 1
    $ confidant_visits["orson"] = max(confidant_visits.get("orson", 0), 4)
    $ remember("orson", "learned about his past life and the concept of anchors")
    $ queue_message("orson", "Everything is fake until it is familiar. Familiarity is just time you decided to spend.", day="yesterday")
    $ reward_attributes_once("orson_visit_04_close", [("nerve", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return

label orson_visit_05:
    call orson_common_open

    "The bar is full tonight. Laughter, glass, the low run of the jazz."
    "Orson sees me and lifts two fingers. The bench is free before I reach it."
    bar_master "You look less like a man reading a map upside down."
    mc "I'm learning. Slowly."
    "He sets down a glass and a small dish of yuzu peel."
    bar_master "Heh. Had days where everything came out wrong?"
    mc "All of them."
    bar_master "It's okay to feel lost — just don't stop walking."
    bar_master "Small rituals help — one day the city nods back. That's all it takes."
    mc "Rituals feel safe."
    "He leans on the counter."
    bar_master "Our professor wears a plain white face and reads the same paper for three hours. Never turns the page."
    bar_master "And our tourist found us by accident, then came back every trip. Copies the old regulars' orders, calls it 'research.'"
    mc "I'll remember the copying rule."
    bar_master "Ask for help, too. Smallest way you can — make it easy for them to say yes."

    menu:
        "\"Thanks... that helps.\"":
            mc "Thanks... that helps."
            bar_master "Let it. It helps."
            $ reward_attributes_once("orson_visit_05_helps", [("grace", "micro")], show="auto")
        "\"It still feels hard.\"":
            mc "It still feels hard."
            bar_master "It is. Worthwhile things are heavy — carry them with both hands."
            $ reward_attributes_once("orson_visit_05_hard", [("nerve", "micro")], show="auto")

    "For a while neither of us says anything. The bar hums around us."
    "When I leave, the laughter follows me to the door and stops at the street."

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

    "It is near closing. Two customers, then one, then none."
    "One shelf behind the bar has a gap in it. Three bottles wide. He has not replaced them."
    bar_master "Doors look heavier at night. Same door. Same hinges."
    mc "Long day?"
    bar_master "Long year."
    "He pours a small neat drink and pauses before sliding it across."
    bar_master "I tried other lives. The company my family wanted. A shop of my own. Bad location, worse timing."
    bar_master "This place was desperation with a lease. I wouldn't change it — I'd change arriving alone."
    mc "And it worked."
    bar_master "It works some nights. A bar is a candle. You do not know how long the wax is."
    "He catches himself. The mask tilts."
    bar_master "Tonight it is still burning. That is enough."
    mc "I don't feel courageous."
    bar_master "You came back. Courage is mostly coming back."
    "He reaches under the counter and puts a paper coaster on the bar. The wolf logo, slightly off-centre."
    bar_master "For when the city is too big. It's a silly thing. Small things outlast us."
    "I turn it in my hand."
    mc "Thanks."
    bar_master "I see you. Not all of it. Enough."
    bar_master "You remind me of myself when I came here. Lost. Stubborn. Curious. Curiosity keeps you alive here. Even when the place does not."

    menu:
        "\"I'll keep showing up.\"":
            mc "I'll keep showing up."
            bar_master "That's the whole game. Keep showing up. Wherever the game is."
            $ reward_attributes_once("orson_visit_06_showup", [("nerve", "micro")], show="auto")
        "\"I'm still scared.\"":
            mc "I'm still scared."
            bar_master "Fear keeps your eyes open — just don't let it keep your feet still."
            $ reward_attributes_once("orson_visit_06_scared", [("grace", "micro")], show="auto")

    "He looks down the bar, then back."
    bar_master "Finish that. Walk home slow. Notice three good things. Bring them back next time."
    bar_master "We never know how many nights we get."
    "The lights dim. Outside, one neon sign flickers and buzzes."
    "When I leave, the coaster is in my pocket, warm against my palm."

    $ orson_affection += 1
    $ confidant_visits["orson"] = max(confidant_visits.get("orson", 0), 6)
    $ remember("orson", "received a wolf coaster and learned about the fragility of the bar")
    $ queue_message("orson", "Different nights. Same stools. That's enough.", day="yesterday")
    $ reward_attributes_once("orson_visit_06_close", [("insight", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return

label orson_visit_07:
    call orson_common_open

    "The bench is the same bench. Tonight it feels like a seat in a house that is being packed."
    "The last customer left an hour ago. Orson has not locked the door."
    bar_master "You came."
    mc "You said tonight."
    bar_master "I say a lot of things."
    "He finishes polishing a glass and sets it down. The shelves behind him are half empty."
    bar_master "The lease is done. The neighborhood is changing. I am tired. It is not one thing."
    mc "So this is goodbye."
    bar_master "Not the kind that erases anything. You came here. You made the place alive. That does not vanish."
    "He leans forward, steady."
    bar_master "You reminded me why I kept the doors open. Not for the money. For this."

    menu:
        "\"I'll miss this place.\"":
            mc "I'll miss this place."
            bar_master "Missing something means it mattered. That's the point."
            $ reward_attributes_once("orson_visit_07_miss", [("grace", "micro")], show="auto")
        "\"I'll carry it with me.\"":
            mc "I'll carry it with me."
            bar_master "Some places can't hold us up forever. You carry the warmth with you — that's what lasts."
            $ reward_attributes_once("orson_visit_07_carry", [("nerve", "micro")], show="auto")

    "He studies me for a long moment. Then he reaches up and takes off the wolf mask."
    "It comes away slowly, as if it has been on a long time. Under it his face is tired and ordinary and kind."
    bar_master "I don't do that for everyone."
    "He reaches under the counter and puts a small badge on the bar. A wolf's paw, the edges worn pale."
    bar_master "Do not keep it safe. Carry it. One day you will walk into a place like this and you will not need me."
    mc "I'll carry it."
    bar_master "You will be part of the warmth yourself. Maybe you already are."
    "The bar is still. The mask sits on the counter between us. The badge is warm in my hand."
    "When I stand to leave, he does not put the mask back on."
    "The door closes softly behind me, the way a door closes when someone is holding it."

    $ orson_affection += 1
    $ confidant_visits["orson"] = max(confidant_visits.get("orson", 0), 7)
    $ remember("orson", "said goodbye to Orson and received his wolf paw badge")
    $ queue_message("orson", "The bar is closing, but what we built here stays. You became part of the warmth yourself. That's the point.", day="yesterday")
    $ reward_attributes_once("orson_visit_07_close", [("nerve", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return


################################################################################
## EPILOGUE — THE WOLF STILL HANGING
################################################################################
##
## The lease ended and Orson is gone. The bar is closed, the window is dark, and
## the room is stripped, but the wolf sign is still on the wall and the alley is
## still the alley. The epilogue is repeatable: the same locked door, the same
## notice, the same sign. Only the first pass writes anything to the save.

label orson_visit_closed:
    scene bg_lupins_alley_night with walk_fade
    show black:
        alpha 0.42
    stop music fadeout 2.0

    "The alley is the same alley. Wet stone, a bicycle, the smell of the yakitori place two doors down."
    "Lupin's Den is at the end, under the wooden wolf."
    "The wolf is still there. The window under it is dark."
    "No light behind the bottles. No glass on the door. Just the sign, the small brass handle, and a notice taped at eye level."

    "PREMISES AVAILABLE.\nFormer tenant: bar.\nViewings by appointment."

    "I read it twice. The font is a letting agent's. The paper is already curling at one corner."
    "Through the window, the room is a shape I know with the lights off. The counter. The bench. The shelves, empty now, or maybe just dark."
    "I try the handle. It is locked. Of course it is."

    menu:
        "Leave the wolf where it is.":
            "It belongs to the building. I step back and let it hang there, unlit and patient."
            $ reward_attributes_once("orson_visit_closed_leave", [("grace", "micro")], show="auto")
        "Look through the window.":
            "I cup my hands around my eyes. The room resolves slowly: the counter, the bench, a single coaster on the wood, a tiny wolf printed slightly off center."
            "I do not know if it is really there. The glass makes everything a guess."
            $ reward_attributes_once("orson_visit_closed_look", [("insight", "micro")], show="auto")
        "Sit on the step.":
            "I sit on the step. The stone is cold. The alley keeps moving without me: a bicycle, a door, someone laughing two floors up."
            "The bar used to be the warm part of this street. Now the warm part is the yakitori lantern."
            $ reward_attributes_once("orson_visit_closed_sit", [("nerve", "micro")], show="auto")

    "The wolf looks down at the empty window. It has the same fixed smile."
    "The bar was never the bottles. It was the hour when someone would listen without asking for your name."
    "That hour is not here anymore. But I know how to carry it."

    if confidant_visits.get("orson", 0) < 8:
        $ orson_affection += 1
        $ confidant_visits["orson"] = max(confidant_visits.get("orson", 0), 8)
        $ remember("orson", "found Lupin's Den closed; the wolf sign was still up and the window was dark")
        $ queue_message("orson", "The bar is a room again. Rooms are patient. If you ever need the door, you know where it was.", day="yesterday")
    $ reward_attributes_once("orson_visit_closed_close", [("grace", "micro")], show="card")

    "I walk back up the alley. The yakitori lantern is doing its best."
    "The door stays locked. The wolf stays up."
    scene bg_home_exterior_night with walk_fade
    stop music fadeout 3.0
    return
