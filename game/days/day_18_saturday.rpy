################################################################################
## DAY 18: SATURDAY, APRIL 25, 2026
## The neighbourhood matsuri: charcoal, a paper net, a rope, and a mask on a stall.
################################################################################

## The fish outlives the festival. Days 19-21 read this.
default goldfish_name = ""

label saturday_matsuri:
    $ set_story_day(18)
    call day_transition

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Saturday. No alarm, no train, no one-minute sign. I wake because somebody is opening my door without knocking."
    "It is Hikari, and she is holding a happi coat against her chest like a piece of evidence."
    hikari "Up. The festival starts at four and you have been awake for twenty minutes."
    mc "How do you know how long I've been awake?"
    hikari "The tomato timer. You wound it at seven. That is how long it has been since you woke up."
    mc "You are timing my life."
    hikari "I am timing your morning. There is a difference. One of them is smaller."
    "She drops the happi coat on me. It is navy blue with white characters down the back."
    hikari "Wear it."
    mc "What does it say?"
    hikari "It says the name of the neighbourhood. You are advertising where you live. That is the whole point of a festival."
    mc "(I am going to walk around a festival wearing the name of my own street. This is either a humiliation or a costume. I will decide by four.)"

    "My phone buzzes while I am trying to work out which way the coat goes."

    if "orson" in wire_unlocked:
        $ run_chat("orson", [
            {"them": "There is a festival tonight. The drums will be loud. The wolf does not like drums.", "options": [
                {"label": "\"Will you be there?\"",
                 "send": "Will you be there?",
                 "them": ["I will be at the edge of it.", "The edge is where the interesting things happen."]},
                {"label": "\"What should I eat?\"",
                 "send": "What should I eat?",
                 "them": ["The smoke tells you.", "Follow the smoke that smells like charcoal and not like sugar."]},
            ]},
            {"them": "If you see a mask with no face, do not buy it."},
        ])
        mc "(He has never once told me something useful in a normal way. I am going to look at every mask.)"
    else:
        $ run_chat("hikari", [
            {"them": "Happi coat. On. Now.", "options": [
                {"label": "\"Which way does it go?\"",
                 "send": "Which way does it go?",
                 "them": ["Like a coat.", "If you need more than that, I am coming up there."]},
                {"label": "\"I look ridiculous.\"",
                 "send": "I look ridiculous.",
                 "them": ["You look like you belong somewhere. That is different."]},
            ]},
        ])

    scene bg_kitchen with walk_fade

    "Mother is putting notes into a plain white envelope. Father is reading the paper with his glasses on, which is how he reads when he is not reading."
    mother "Festival money. There is more than you need. Bring back what you do not spend."
    mc "That's not how spending works."
    mother "It is how envelopes work."
    hikari "She puts too much in every year. Every year he brings some back. Every year she puts too much in."
    father "I have an errand tonight."
    mc "On a Saturday?"
    father "Many people have errands on a Saturday."
    mother "He has had this errand for eleven years."
    father "It is the same errand. That does not make it less of one."
    mc "(Father has a secret Saturday errand. I am going to find out what it is before this day is over. I do not know how I know that.)"

    menu:
        "Ask what the errand is.":
            mc "What's the errand?"
            father "A rope."
            mc "A rope?"
            father "You heard me. I am needed for a rope. That is all a man is needed for, some nights."
            mother "Tetsuo."
            father "I am being helpful."
            $ reward_attributes_once("day18_kitchen_errand", [("insight", "micro")], show="auto")
        "Ask Mother what to eat.":
            mc "What should I eat there?"
            mother "The yakitori. The smoke that smells like charcoal, not sugar. And one sweet thing, because Hikari will make you."
            hikari "I will not make you."
            mc "You will."
            hikari "I will choose for you. That is not the same as making you."
            $ reward_attributes_once("day18_kitchen_food", [("grace", "micro")], show="auto")
        "Bring the tomato timer.":
            "I put the tomato timer in my pocket. Hikari watches me do it and says nothing."
            mc "It is for the shape of it."
            hikari "Then bring it."
            mc "(She understands. I do not know what she understands, but she does.)"
            $ reward_attributes_once("day18_kitchen_timer", [("nerve", "micro")], show="auto")

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The walk to the station is different because we are not going to school. Hikari walks at an angle, the way she does when she is pulling me somewhere."
    hikari "The festival is not in Asakusa. It is here. In our neighbourhood."
    mc "I've never seen it."
    hikari "You have been here twenty-five days. You have seen the street it happens on a hundred times."
    mc "That's the same thing?"
    hikari "No. That is the whole point of a festival. Same street. Different street."
    mc "(The city as a set of instructions. On Saturdays it rewrites them.)"

    scene bg_station with walk_fade
    scene bg_platform with walk_fade
    "The platform is full of people in happi coats. For once I am not the most dressed-up person in the car."
    scene bg_train_interior with walk_fade
    "Two men in matching indigo coats are arguing cheerfully about something. A woman is holding a paper lantern on her lap like a cat."
    hikari "You are staring."
    mc "I'm previewing."
    hikari "What?"
    mc "It is a word. I am doing it."
    hikari "Then do it quietly."

    scene bg_nightfood with Fade(0.0, 0.0, 1.5)
    stop music fadeout 1.0
    play music "audio/Music/(Hanabi night) lanterns_at_dusk.mp3" fadein 2.0
    $ phone_map_visit("night_market")

    "We come out of the station and the street has changed in the time it takes to cross it."
    "Lanterns strung from pole to pole. Stalls with roofs like small houses. Smoke going up in thick grey columns and catching the light."
    "The air smells like charcoal and sugar and the first warm night of the year."
    mc "(The treatment of this country says every festival smells like summer. This one smells like April and somebody's dinner.)"
    hikari "Is this the same street?"
    mc "I can see the pharmacy."
    hikari "Then it is the same street. The pharmacy is the anchor. Everything else is temporary."
    "She pulls the happi coat straight on my shoulders and steps back to look."
    hikari "There. You are from somewhere."
    mc "I was from somewhere before."
    hikari "Yes, but nobody here knew it."

    "We eat walking. Yakitori from a stall with a queue, the skewer too hot to hold comfortably. Hikari eats three and looks innocent about it."
    hikari "That one had a wing on it."
    mc "That is what a wing is for."
    hikari "I am saying I enjoyed it. I am not asking you to tell anyone."
    "A man at the next stall is calling out the same sentence every twelve seconds. Every time, a different person laughs."
    mc "(Zaazaa for rain. There should be a word for a man who says one thing all night and means it differently each time.)"

    scene bg_harajuku_candy with walk_fade
    "At a stall near the shrine steps, a row of goldfish bowls glows green in the lantern light. Paper nets hang from a rail, already softening at the edges."
    hikari "Goldfish scooping. You have to do it."
    mc "I have to?"
    hikari "It is a festival. Everything is mandatory. That is why there are so many rules."
    "The woman at the stall hands me a net and a small bowl. The net is paper. It looks insulting."

    menu:
        "Go for the biggest fish.":
            "I scoop hard at the largest goldfish in the bowl. The paper net tears on the rim and the fish shoots away."
            "The woman at the stall says something in Japanese that sounds like a bee. Hikari is laughing into her fist."
            hikari "You attacked it. You cannot attack a goldfish."
            mc "How do you catch one?"
            hikari "You invite it."
            $ reward_attributes_once("day18_fish_big", [("nerve", "micro")], show="auto")
        "Let Hikari show me.":
            "She takes a net, moves it slowly to the side of the bowl, and waits. A goldfish swims into it. She lifts. The paper holds."
            hikari "You see? You do not chase. You become a place where a fish would like to be."
            mc "That is the most Japanese sentence I have heard all week."
            hikari "It is also true."
            $ reward_attributes_once("day18_fish_hers", [("grace", "micro")], show="auto")
        "Ask the woman how to do it.":
            mc "どうやって？"
            "The woman at the stall looks surprised, then delighted, and explains with her hands for a full minute."
            "I do not understand a word. I copy what her hands did. The net holds. A tiny goldfish comes up with it."
            hikari "You asked."
            mc "I asked."
            hikari "You never ask."
            mc "I asked."
            $ reward_attributes_once("day18_fish_ask", [("insight", "micro")], show="auto")

    "I get one fish. It is the smallest one in the bowl, orange and alert, in a plastic bag of water with the top twisted shut."
    mc "What do I do with it?"
    hikari "Take it home."
    mc "Home?"
    hikari "You caught it. It is yours now. That is the whole rule."
    mc "We don't have a bowl."
    hikari "Mother has a bowl. She has a bowl for everything."
    "I hold the bag up to the lantern light. The fish turns, considers me, and turns back."
    $ goldfish_name = "Mister Plum"
    mc "Mister Plum."
    hikari "Why?"
    mc "He came from a festival on the same day as a plum in rice. He needs a sensible name."
    hikari "Mister Plum is not a sensible name."
    mc "It is a name with a job."
    hikari "That is a plum's job. You have mixed up your foods."
    mc "(I am carrying a fish called Mister Plum through a festival in a happi coat. This is the best day I have had in this country.)"

    "The drums start at the far end of the street."
    "Thump. Then, half a beat later, the thump arrives in my chest."
    mc "(That is not how sound works.)"

    call leak_audio

    scene bg_nightfood with walk_fade
    "The crowd moves back against the stalls. A mikoshi comes around the corner, a portable shrine on long poles, carried by six men in matching happi coats."
    "The lanterns on it are lit. The whole thing is a small bright building moving down the street."
    hikari "That is the neighbourhood god, out for a walk."
    mc "Where does it live the rest of the year?"
    hikari "In a small building at the end of the street. You have walked past it a hundred times. It is the smallest shrine in the city."
    "The men carrying it shift their weight together. The mikoshi dips and rises like a thing breathing."
    "And then I see him."
    "Tetsuo. In a happi coat. Shouldering a rope attached to the front of the shrine, leaning back into it the way a man leans into a task he has done for a long time."
    "He does not look at me."
    "Beside the procession, Miharu is standing with her hands together. She sees me, and she waves. Just once, with two fingers."
    "I wave back. Father does not look. Mother does not stop waving until the shrine has gone past."
    mc "(A rope. Eleven years. He has been an errand this whole time and I did not know.)"
    hikari "You knew?"
    mc "He said a rope at breakfast."
    hikari "He says a rope every year. Nobody asks about the rope. That is the rule."
    mc "But you knew."
    hikari "I am from here."
    mc "(She is from here. I am wearing the name of the street on my back. For one afternoon the difference is small.)"

    "When the mikoshi has gone, I notice a mask stall set up against the wall of the small shrine. Rows of masks on a board: foxes, demons, a laughing old man."
    "One of them is a plain white face with no expression. It is hanging turned toward the wall."
    "I look at it for a second and look away."
    "When I look back, it is facing me."
    "It has no features except two narrow eye-holes. Through them, the lantern light is not showing."
    mc "(Mitate. A mask is a thing that changes the person looking. I do not want to be changed by this one.)"

    call leak_audio

    hikari "What are you looking at?"
    mc "A mask. It was facing the wall."
    hikari "Which one?"
    "I point. There is a fox mask there. A red one. Nothing else."
    hikari "That one? It is a fox. They all face the wall until somebody buys them."
    mc "It had no face."
    hikari "Then it was not finished."
    "She takes my hand and pulls me away before I can look again."
    $ festival_mask_seen = True

    scene bg_home_exterior_night with walk_fade
    "We walk home the long way because Hikari says the short way is for people who arrived by bus."
    "The fish swings gently in my hand. The happi coat is warm from the crowd. The drums are still going behind us, far enough away to be a heartbeat."
    hikari "Did you have fun?"
    mc "Yes."
    hikari "Say it again."
    mc "I had fun."
    hikari "Good. I wanted to hear it twice."

    call dinner_open

    father "And the festival?"
    mc "There was a mikoshi. Six men carrying it."
    father "Six, sometimes eight. It depends who is in the neighbourhood."
    mc "There was a man on the rope."
    "Father looks at his rice. Mother does not look up. Hikari is very interested in her tea."
    father "A man on a rope is a man on a rope."
    mother "He has done it every year since before you were born."
    father "Miharu."
    mother "He asked."
    father "He asked about a rope."
    mc "I asked about the festival."
    father "It is the same question on a Saturday."
    mc "(It is the same question. I have been asking it about this house for twenty-five days.)"
    hikari "Did you catch anything?"
    "I put Mister Plum's bag on the table. The fish turns in the lantern light from the kitchen window."
    mother "Oh."
    mc "We need a bowl."
    mother "I have a bowl."
    father "Of course you have a bowl."
    mother "I have a bowl for everything. That is what a house is."

    call dinner_close

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, Mister Plum is in a chipped bowl on the desk. Hikari found it in the cupboard without being asked."
    "The happi coat is folded over the chair. It still smells like charcoal."
    $ night_desk_line = "the bowl"
    call night_open

    menu:
        "Ask her about the mask.":
            mc "The mask. The white one. It was facing the wall and then it was facing me."
            hikari "Masks do that at festivals. It is the whole point of them."
            mc "Did you see it?"
            hikari "No."
            mc "You said masks do that."
            hikari "I know what masks do. I did not see that one."
            mc "(There is a space between knowing and seeing. She is standing in it on purpose.)"
            $ remember("hikari", "asked about the white mask and she knew what masks do but had not seen that one")
            $ reward_attributes_once("day18_night_mask", [("insight", "micro")], show="auto")
        "Tell her about Father on the rope.":
            mc "Dad has done the rope for eleven years."
            hikari "Twelve. He started the year before I was born."
            mc "You all knew."
            hikari "It is a small neighbourhood. Nobody knows anything, and everybody knows everything. Those are the two rules."
            mc "(I am starting to understand the second one.)"
            $ remember("hikari", "talked about Father carrying the rope at the festival for twelve years")
            $ reward_attributes_once("day18_night_rope", [("grace", "micro")], show="auto")
        "Watch the fish.":
            "I do not say anything. Mister Plum goes around the bowl once and stops."
            "Hikari watches him with me. She does not fill the silence."
            mc "(A thing with a job. A plum in rice. A rope. A fish in a chipped bowl.)"
            $ remember("hikari", "watched the goldfish in silence after the festival")
            $ reward_attributes_once("day18_night_quiet", [("nerve", "micro")], show="auto")

    call night_close

    "Three days to the midterm. I have a word I did not choose, a fish I did not plan for, and a father who is a rope."
    "Tomorrow is Sunday. Hikari says we are doing the mock exam. She says it like she has been looking forward to it all week."
    "I turn off the lamp. The room is dark. The room is not empty."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump sunday_mock
