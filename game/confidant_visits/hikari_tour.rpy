################################################################################
## HIKARI TOURS — MESSAGE HIKARI AND UNLOCK THE CITY
################################################################################
##
## Foundation for the "Message Hikari" hub row. The flow is:
##
##   1. He texts her and asks whether she is free after class.
##   2. She offers to show him somewhere he has not been.
##   3. She picks a locked city destination from `hikari_tour_spots`.
##   4. The matching `hikari_tour_<place>` label plays.
##   5. That label calls `unlock_hikari_tour_destination(place)`.
##
## After the first tour, the place's hub row becomes travelable on its own and
## the ordinary `city_row_<place>` scene plays without Hikari. The tour is a
## one-time introduction, not a companion who follows him forever.
##
## Yokohama was the first tour written; Harajuku: Takeshita Street is the second.
## Only tours in `hikari_tour_written` are offered, so Message Hikari never sends
## the player into a placeholder. Add the next place id there when its scene is
## ready; the picker then chooses randomly among whatever is still locked and
## written. Each label ends by unlocking its place for the generic solo row.


label hikari_tour:
    $ last_afternoon_was_run = False
    $ last_afternoon_hikari_tour = False

    $ tour_available = [p for p in hikari_tour_available_spots() if p in hikari_tour_written]
    if tour_available:
        $ tour_spot = renpy.random.choice(tour_available)
    else:
        $ tour_spot = None

    if not tour_spot:
        $ run_chat("hikari", [
            {"them": [
                "Actually, I'm out of places to show you.",
                "You have seen more of this city than I have.",
            ], "options": [
                {"label": "Then let's just walk home.",
                 "send": "Then let's just walk home."},
            ]},
            {"them": "Deal."},
        ])
        scene bg_home_exterior_night with walk_fade
        $ night_street()
        $ last_afternoon_place = "walk_hikari"
        $ last_afternoon_was_run = False
        return

    $ last_afternoon_place = tour_spot
    $ last_afternoon_hikari_tour = True

    if tour_spot == "yokohama":
        # The hunger is the hook. She does not offer a tour first; she offers
        # dinner, and the tour is what happens on the way to it.
        $ run_chat("hikari", [
            {"options": [
                {"label": "Hey Hikari. Are you free after class?",
                 "send": "Hey Hikari. Are you free after class?",
                 "them": [
                     "Seminar ends at four. Why?",
                     "Do you have food?",
                 ]},
            ]},
            {"them": [
                "Because I am starving.",
                "There is a place in Yokohama. Chinatown.",
                "Gyoza. Shoronpo. Ramen. The real thing.",
                "Do you want me to show you?",
            ], "options": [
                {"label": "Show me the gyoza.",
                 "send": "Show me the gyoza."},
                {"label": "I thought you were showing me Yokohama.",
                 "send": "I thought you were showing me Yokohama."},
            ]},
            {"them": [
                "I am showing you Yokohama.",
                "The gyoza is the important part.",
                "Meet me at the station. Do not eat lunch.",
            ]},
        ])
    elif tour_spot == "harajuku":
        # The fashion is the hook. She explains just enough to make him curious,
        # then turns it into a walk, because the street is the point.
        $ run_chat("hikari", [
            {"options": [
                {"label": "Hey Hikari. Are you free after class?",
                 "send": "Hey Hikari. Are you free after class?",
                 "them": [
                     "Seminar ends at four.",
                     "Have you heard of kawaii fashion?",
                 ]},
            ]},
            {"them": [
                "It is not just cute. It is a whole way of dressing.",
                "Layers. Skirts over trousers. Colours that should not work together.",
                "Lace and plastic and a ribbon where a ribbon has no business being.",
            ], "options": [
                {"label": "What is that?",
                 "send": "What is that?",
                 "them": ["I will show you. That is easier than explaining."]},
                {"label": "Do people actually wear that?",
                 "send": "Do people actually wear that?",
                 "them": ["You have no idea.", "That is why we are going."]},
            ]},
            {"them": [
                "Takeshita Street. The weather is nice and the light is good.",
                "Meet me at the station after seminar.",
                "Do not dress normally. I am warning you now.",
            ]},
        ])
    elif tour_spot == "karaoke":
        # The sing is the hook, but she frames it as letting something out and
        # as something to do with him, not as a performance. She runs late on
        # purpose and gives him a reason to accept before he can refuse.
        $ run_chat("hikari", [
            {"options": [
                {"label": "Hey Hikari. Are you free after class?",
                 "send": "Hey Hikari. Are you free after class?",
                 "them": [
                     "I have to stay after seminar. Something I promised to finish.",
                     "Two hours, maybe. Then I am free.",
                 ]},
            ]},
            {"them": [
                "I hope you like singing.",
                "Or — better — that you like letting things out. I need to let something out tonight.",
                "There is a place I go. Kuru Fuku Neko.",
            ], "options": [
                {"label": "Singing? In front of people?",
                 "send": "Singing? In front of people?",
                 "them": [
                     "Private rooms. Nobody hears you except the person you came with.",
                     "That is the whole point.",
                 ]},
                {"label": "I'm shy. I'm not sure.",
                 "send": "I'm shy. I'm not sure.",
                 "them": [
                     "I know. That is why I am asking you and not somebody else.",
                     "You can be shy in a room with me.",
                 ]},
            ]},
            {"them": [
                "Meet me outside. I will explain everything there.",
                "Do not worry about being good. Nobody is good. That is why the rooms have walls.",
            ]},
        ])
    else:
        $ run_chat("hikari", [
            {"options": [
                {"label": "Hey Hikari. Are you free after class?",
                 "send": "Hey Hikari. Are you free after class?",
                 "them": [
                     "I have seminar until four.",
                     "Why? Did you want to do something?",
                 ]},
            ]},
            {"them": "I could show you somewhere you have not been yet.", "options": [
                {"label": "Yes, please.",
                 "send": "Yes, please."},
                {"label": "If you're offering.",
                 "send": "If you're offering."},
            ]},
            {"them": [
                "Then it's settled.",
                "I pick the place. Meet me at the station.",
            ]},
        ])

    scene bg_station with walk_fade
    "Hikari is already waiting by the ticket gate, arms crossed, pretending she has not been checking the time."
    hikari "You're late. I got here early and now I can't stop noticing."
    mc "You said after class."
    hikari "You're here. That's close enough."
    if tour_spot == "yokohama":
        hikari "Rule one. We do not eat at the first shop."
        mc "Why not?"
        hikari "Because the first shop is for tourists. Rule two. If someone shouts at you, nod. Do not apologise."
        mc "(This is either a tour or a warning.)"
    elif tour_spot == "karaoke":
        hikari "Tonight we sing. That is all I am telling you."
        mc "What if I am terrible?"
        hikari "Then you will be terrible with me in the room. That is better than being terrible alone."
    elif tour_spot == "harajuku":
        hikari "Rule one. We look at everything. We buy nothing until the third shop."
        mc "Why the third?"
        hikari "The first two are for people who photograph themselves. The third is for people who actually wear it."
        mc "(She has a rule for everything. Most of them turn out to be true.)"
    hikari "Come on. I want to get there before the line."
    "She turns before I can ask where we are going. I follow her."

    $ renpy.jump("hikari_tour_" + tour_spot)


## --- THE TOUR SCENES ---------------------------------------------------------
##
## Yokohama is the written tour. The rest are still placeholders: Hikari arrives
## with him, introduces the place, and the unlock happens at the end. Replace
## the placeholder lines and add choices/rewards there when those scenes are
## written. The message flow, picker, unlock, and solo fallback do not move.

label hikari_tour_harajuku:
    $ hikari_kawaii = False
    play music "audio/Music/harajuku.mp3" fadein 2.0
    scene bg_harajuku with walk_fade
    "The train lets us out into a crowd that looks dressed for a different country."
    "Then we turn a corner, the street narrows, and the colours arrive all at once. Pink, yellow, stripes, lace, a girl in a skirt the size of a small building."
    hikari "Takeshita Street."
    mc "It is... loud."
    hikari "It was a quiet lane behind the station. Then the boutiques came and nobody has taken them out since."
    hikari "This is where kawaii stopped being a word in a magazine and became something people wore to the convenience store."
    mc "What does kawaii mean, exactly?"
    hikari "可愛い. Cute. But that is the small translation. It is also a way of dressing, a way of talking, a way of deciding what deserves your attention."
    hikari "If something is kawaii, it is allowed to take up space. That is the whole idea."
    mc "(A word that gives permission. I can understand that kind of word.)"
    hikari "Rule two. Walk slowly. If you hurry, you miss the thing the street is actually for."
    mc "Which is?"
    hikari "Being seen, and seeing. That is the transaction. Everybody here is both the audience and the show."

    menu:
        "Ask why nobody is looking at us.":
            mc "Nobody is looking at us. Is that rude?"
            hikari "No. They are looking at everyone. That is different from looking at you."
            hikari "Here, being looked at is not a judgment. It is participation. You will understand when you stop trying not to be seen."
            mc "(I try not to be seen. I am immediately seen by a girl with pink hair who smiles at me like I did something clever.)"
            $ reward_attributes_once("harajuku_tour_looking", [("insight", "micro")], show="auto")
        "Ask what the rules of the street are.":
            mc "You have rules for this place too?"
            hikari "Of course. Look with your eyes, not with your camera. Say 可愛い when something deserves it. Do not laugh at anybody, ever."
            hikari "And if somebody asks to photograph you, say yes. That is how you become part of the street."
            mc "(She says it like a rule. I can follow a rule.)"
            $ reward_attributes_once("harajuku_tour_rules", [("grace", "micro")], show="auto")
        "Count the colours in one shop window.":
            mc "I am trying to count the colours in that window."
            hikari "How many?"
            mc "Nineteen. I lost count at the socks."
            hikari "Then the window has won. That is what it wanted."
            $ reward_attributes_once("harajuku_tour_colours", [("nerve", "micro")], show="auto")

    "We move with the crowd, which is the only way to move here."
    "A crepe shop turns a crepe into a tower of fruit and whipped cream and something that might be chocolate. A girl beside me orders it without looking at the menu."
    "A tapioca shop has a line that goes around the corner. The drinks are the colour of milk tea and the cups are covered in cartoon cats."
    "And everywhere, cotton candy. Pink, blue, green, purple, shaped like flowers and hearts and animals with too many ears."

    menu:
        "Get the biggest crepe.":
            mc "I want that one. The one that is structurally impossible."
            hikari "Good. It is designed to be photographed before it is eaten."
            "The crepe is taller than my hand. I eat it with a fork and then with my fingers. Hikari is right about the photograph."
            $ reward_attributes_once("harajuku_tour_crepe", [("nerve", "micro")], show="auto")
        "Ask what tapioca is.":
            mc "What is in the cup? Those little black balls."
            hikari "タピオカ. Tapioca. Starch from a root, boiled until it bounces."
            mc "It bounces?"
            hikari "Everything here bounces. It is part of the design."
            $ reward_attributes_once("harajuku_tour_tapioca", [("insight", "micro")], show="auto")
        "Let Hikari choose.":
            mc "You choose. I will eat whatever you point at."
            hikari "That is the first sensible thing you have said since we got off the train."
            "She gets us something cold and sweet with a cat drawn on the cup. She does not tell me what it is. I decide not to ask."
            $ reward_attributes_once("harajuku_tour_let_choose", [("grace", "micro")], show="auto")

    scene bg_harajuku_clothes with walk_fade
    "The clothing shop is smaller than the street and louder than both of us together."
    "Skirts hang over trousers. Socks are worn over other socks. There is a jacket covered in pockets that serve no purpose, and Hikari touches the sleeve like it is a document she has been waiting to read."
    hikari "This is the part people photograph and call a costume. It is not a costume. People live in it."
    hikari "Look. The layers are not random. Short over long, loose over tight, something soft and one thing that should not work."
    mc "Why one thing that should not work?"
    hikari "Because then somebody has to look twice. That is the whole point of being seen."

    menu:
        "Ask her to explain the outfit on the mannequin.":
            mc "Walk me through it. Top to bottom."
            hikari "Skirt over trousers. Socks over boots. A ribbon that does nothing. And one colour that is fighting all the others."
            hikari "It should be a mess. It is not. Somebody decided, and that is the difference."
            mc "(Deciding. I am starting to think that is what this street is about.)"
            $ reward_attributes_once("harajuku_tour_outfit", [("insight", "micro")], show="auto")
        "Try something on.":
            mc "Can I try that jacket? The one with all the pockets."
            "The assistant takes it down before Hikari can answer. I put it on. The pockets are real. I have no idea what to put in them."
            hikari "可愛い."
            mc "What did she say?"
            hikari "She said you look cute. Do not ask me to repeat it."
            $ reward_attributes_once("harajuku_tour_try_on", [("nerve", "micro")], show="auto")
        "Ask if she ever dressed like this.":
            mc "Did you ever dress like this?"
            hikari "For about a year. I thought it was the most important thing in the world."
            mc "What changed?"
            hikari "I found out I liked being seen more when I could choose when to be seen."
            "She says it to the jacket, not to me. I let it stand."
            $ reward_attributes_once("harajuku_tour_her_style", [("grace", "micro")], show="auto")

    "The assistant has been watching Hikari touch the sleeve. Before either of us can say anything, she is holding a dress on a hanger and talking very fast."
    hikari "What? No. I could not —"
    "She looks at me. I have no idea what she is asking me, and I say the only thing that makes sense."
    mc "You should."
    "The assistant takes her by the sleeve, and the next thing I see is the curtain of the fitting room moving."
    "It takes a while. I look at the socks. I look at the jacket with the pockets. I try very hard not to look at the curtain."
    $ hikari_kawaii = True
    "Then the curtain opens."
    "It is Hikari. It is not the Hikari who sits across the breakfast table and tells me the rules of the house."
    "The skirt goes over the trousers. The socks go over the boots. There is a ribbon doing nothing at all, and one colour fighting all the others and losing."
    "She looks like she has been assembled out of the whole street."
    mc "..."
    hikari "Say something."
    mc "..."
    hikari "That bad?"
    mc "No. That is the problem. I do not have words."

    menu:
        "Tell her she looks incredible.":
            mc "You look incredible."
            "She opens her mouth, then closes it. The assistant says something in fast Japanese and Hikari's ears go red."
            hikari "She says you have excellent taste. Do not ask me to translate the rest."
            $ reward_attributes_once("harajuku_tour_kawaii_compliment", [("grace", "micro")], show="auto")
        "Say nothing. Just stare.":
            mc "..."
            "She waits. I fail. She laughs — a real one, not the one she uses at the table."
            hikari "You are hopeless."
            mc "I know."
            $ reward_attributes_once("harajuku_tour_kawaii_speechless", [("nerve", "micro")], show="auto")
        "Ask if she is comfortable.":
            mc "Is it comfortable?"
            hikari "It is a dress made for standing still in a shop window. No."
            mc "Then why —"
            hikari "Because you could not speak. I wanted to see how long it would last."
            $ reward_attributes_once("harajuku_tour_kawaii_comfort", [("insight", "micro")], show="auto")

    "She does not take it off."
    "She keeps the dress and the ribbon and the ridiculous socks for the rest of the day — through the candy shop, onto the train, and in through the door of the house."

    scene bg_harajuku_candy with walk_fade
    "The cotton candy shop is a wall of colour. Spirals of sugar on sticks, shaped like flowers and hearts and clouds, stacked in rows like a field that has gone wrong in the best possible way."
    "A girl behind the counter spins a new one. Sugar goes in, colour comes out. It takes about four seconds."
    hikari "Look at it. 綿菓子. Wataame. Cotton candy."
    mc "It is too beautiful to eat."
    hikari "That is what everybody says. Then they eat it."
    "She buys two. Mine is pink and shaped like a flower with more petals than any real flower has. Hers is blue and shaped like a heart."
    "I hold it at arm's length. The street keeps moving around me."

    menu:
        "Say it is too cute to eat.":
            mc "可愛. It is too cute. I cannot eat it."
            hikari "That is also a correct use of the word."
            mc "I ate it anyway."
            hikari "Of course you did. It was made to be eaten."
            $ reward_attributes_once("harajuku_tour_too_cute", [("nerve", "micro")], show="auto")
        "Ask how they make the shapes.":
            mc "How does she get it into a heart?"
            hikari "She does not. You do. Watch."
            "The girl hands me the stick and turns my wrist twice. Sugar folds where I tell it to. The heart is not perfect. It is mine."
            $ reward_attributes_once("harajuku_tour_candy_shape", [("insight", "micro")], show="auto")
        "Take a photograph of Hikari with hers.":
            mc "Hold it up. I want a photograph."
            hikari "No."
            mc "Why not?"
            hikari "Because this one is mine, and I am eating it before you can document it."
            "She does. She gets sugar on her finger and does not wipe it off. I decide that this is the best thing I have seen all day."
            $ reward_attributes_once("harajuku_tour_candy_photo", [("grace", "micro")], show="auto")

    "We walk the street again, slower this time, toward the station end."
    "The light has changed. The colours have changed with it. A shop that looked ordinary an hour ago is now impossible to ignore."
    mc "I thought this place would be too much."
    hikari "It is too much. That is the point. You were supposed to find a way to stand in the middle of too much and not leave."
    mc "Did I?"
    hikari "You are still here. Yes."

    menu:
        "Ask why she brought me here.":
            mc "Why here, of all the places you could have shown me?"
            hikari "Because you look at things like you are afraid of getting them wrong."
            hikari "There is no wrong here. You put a skirt over trousers and see what happens. That is the whole lesson."
            mc "(She says it like a rule. This one I might keep.)"
            $ reward_attributes_once("harajuku_tour_why_here", [("insight", "micro")], show="auto")
        "Say you want to come back alone.":
            mc "I want to come back by myself."
            hikari "Good. Walk the whole street. Do not buy anything on the first pass."
            mc "The third shop?"
            hikari "You were listening."
            $ reward_attributes_once("harajuku_tour_come_back", [("nerve", "micro")], show="auto")
        "Tell her you had fun.":
            mc "I had a really good time."
            hikari "I know. You stopped checking where we were about an hour ago."
            mc "I did?"
            hikari "You did. That is how I know."
            $ reward_attributes_once("harajuku_tour_had_fun", [("grace", "micro")], show="auto")

    $ unlock_hikari_tour_destination("harajuku")
    $ phone_map_visit("harajuku")
    $ renpy.notify("Harajuku: Takeshita Street is now on your map.")
    mc "(I can come back here on my own now. She showed me the shape of it.)"
    hikari "Next time, go without me."
    mc "You are not coming?"
    hikari "I have shown you. That was the point."
    mc "(She says it lightly. It does not land lightly.)"
    hikari "And if you get a crepe, get the one with the fruit. The tall one is for photographs."
    $ reward_attributes_once("hikari_tour_harajuku_complete", [("insight", "tiny")], show="auto")

    scene bg_train_interior with walk_fade
    "The train home is warm and half empty. Hikari falls asleep against the window with her jacket folded under her head."
    "There is a streak of pink sugar on her finger that she never wiped off."
    mc "(She took me to a street where nobody is embarrassed to be seen. I think that was the point.)"

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    hikari "We're home."
    mc "We're home."
    hikari "You're welcome."
    mc "I didn't say thank you."
    hikari "You were going to."
    $ hikari_kawaii = False
    "She goes inside before I can prove her right."
    "By the time I reach the front step, the ribbon is gone. She is wearing her own clothes again, and she never mentions the dress."
    return


label hikari_tour_karaoke:
    scene bg_karaoke_outside with walk_fade
    "Kuru Fuku Neko is three floors of neon above a closed bakery, with a cat over the door wearing a small red bib."
    "The sign has a line of Japanese under it that Hikari is reading with her mouth slightly open."
    hikari "来る福猫. The cat that brings luck when it comes. A verb, a blessing, and a cat. That is the whole name."
    mc "It is a very good name."
    hikari "I know. I am glad you said that first."

    "She does not go in yet. She turns to me on the pavement like this is the important part of the tour."
    hikari "Karaoke is not a stage. That is the thing people get wrong. You rent a room — a box — by the hour, and the room is yours."
    hikari "Nobody is in it with you unless you ask them in. The machine does not judge, the walls do not judge, and the score is a suggestion."
    mc "So it is for people who cannot sing."
    hikari "It is for people who cannot sing and do it anyway. That is a different thing."
    hikari "You pay for the room, and then for what you drink. Or you take 飲み放題 — nomihōdai — and the drinks keep coming for a fixed price."
    mc "That sounds dangerous."
    hikari "It is. That is why they also give you ice cream. Sober people with soft serve are harder to lose."
    "She points through the glass. A rack of cat ears, plastic glasses, and a hat with a propeller on it."
    hikari "Costumes. Nobody wears them ironically. You put them on and suddenly you are allowed to be loud."
    "A shelf beside it holds maracas, a tambourine, and a stick with a padded end."
    hikari "And those. 応援. Cheering. You hit the stick on the table when somebody is singing well."
    mc "You are telling me the room has a built-in audience."
    hikari "I am telling you the room has a built-in audience that you hit with a stick."

    menu:
        "Ask how much an hour costs.":
            mc "How much is an hour, actually?"
            hikari "Depends on the room and the day. Weeknights are cheaper. There is a board inside."
            hikari "The trick is to go when nobody else wants to. That is when a place is really yours."
            mc "(She has a theory about everything. Most of them are about timing.)"
            $ reward_attributes_once("karaoke_tour_cost", [("insight", "micro")], show="auto")
        "Ask why she picked this place.":
            mc "Why here? Of all the places you could show me."
            hikari "Because you said you were shy, and this is the loudest place in the city where nobody can hear you."
            hikari "I thought you might like the contradiction."
            mc "(I do. I do not know how to say that yet.)"
            $ reward_attributes_once("karaoke_tour_why", [("grace", "micro")], show="auto")
        "Put on the cat ears.":
            "I take a pair of cat ears off the rack and put them on. They are ridiculous. They are also extremely light."
            hikari "..."
            mc "What?"
            hikari "Nothing. You just became about four years younger and I am not sure how to feel about it."
            "She takes a pair for herself. She does not explain."
            $ reward_attributes_once("karaoke_tour_costume", [("nerve", "micro")], show="auto")

    "We go in. The corridor is narrower than the street and twice as loud."
    "A woman's voice comes through one wall, doing a ballad with her whole life in it. Through the next, a group is laughing and losing the chorus on purpose."
    "Further down, somebody is singing the same two lines over and over, stopping each time at exactly the same word."
    hikari "Listen. That one from the first room — everybody knows it. It is from a drama. You have heard it, even if you do not know you have."
    mc "And the two lines?"
    hikari "Somebody is practising. That is the bravest room in this building."
    "She hums a few bars of something as we walk. I do not recognize it. She stops when she notices me listening."
    hikari "You can tell what a room is doing from the song. That is a real skill."
    mc "I cannot tell anything."
    hikari "You will. You already know the difference between the laughing room and the practising room. That is most of it."

    scene bg_karaoke_drink with walk_fade
    "The drink bar is a wall of taps and a row of machines that dispense colours I have no names for."
    "There is a soft-serve machine at the end, and a fridge full of things with cartoon cats on them."
    hikari "Before anything else — water. Singing is exercise and nobody tells you that."
    "She takes two cups and fills one, then the other. She puts the second in my hand like it is a decision she has already made for both of us."
    hikari "Then whatever you want. The soft serve is free here. I am telling you because you will not find out otherwise."

    menu:
        "Get the soft serve.":
            mc "I am getting the soft serve."
            hikari "Of course you are."
            "It comes out in a perfect spiral and tastes like vanilla and cold air. Hikari watches me eat it with an expression I cannot read."
            hikari "You are very easy to please. That is not an insult."
            $ reward_attributes_once("karaoke_tour_softserve", [("grace", "micro")], show="auto")
        "Ask about the free-flow drinks.":
            mc "How does the all-you-can-drink actually work?"
            hikari "You pay for a block of time and you order from this list. Alcohol, tea, soda — all of it. They bring it to the room."
            mc "And people manage that responsibly?"
            hikari "Some do. The staff keep bringing water after a while. That is their whole job, I think."
            $ reward_attributes_once("karaoke_tour_freeflow", [("insight", "micro")], show="auto")
        "Just take the water she handed me.":
            mc "I will just have the water."
            "She nods once, like I answered a question correctly."
            hikari "Good. Then we are going to need it."
            $ reward_attributes_once("karaoke_tour_water", [("grace", "micro")], show="auto")

    scene bg_karaoke_room with walk_fade
    "The room is smaller than the lobby and louder than both of us together, even before either of us has sung a note."
    "A tablet sits on the table beside a remote, a box of tissues, and the padded cheering stick."
    hikari "This is the remote, and this is the tablet. You search by title, by artist, or by the first letters."
    "She taps the screen. A menu opens in Japanese, then she touches a small flag in the corner and the whole thing changes to English."
    hikari "See? English support. Nobody here will notice. Half the tourists in this city use it."
    mc "It even has the letters spelled out."
    hikari "That is for people like you. And for people like me when I am too tired to read fast."

    menu:
        "Ask her to show me the English support.":
            mc "Show me where the language changes."
            "She taps the flag, then back again, then forward. The buttons keep their places. Only the words move."
            hikari "You can switch it mid-song if you want. The queue does not care."
            mc "(A machine that forgives me for not reading fast. A small miracle.)"
            $ reward_attributes_once("karaoke_tour_tablet", [("insight", "micro")], show="auto")
        "Pick an English song.":
            mc "I am picking this one. It is the only one I know all the words to."
            "I add it to the queue. The tablet says the song title, then a number: 3."
            hikari "Three. That means we sing after the people in the next room finish their ballad."
            mc "There is a next room in my song?"
            hikari "There is a queue. That is different."
            $ reward_attributes_once("karaoke_tour_pick_song", [("nerve", "micro")], show="auto")
        "Let her add the first song.":
            mc "You choose. I will follow."
            hikari "That is the safest thing you have said all evening."
            "She adds something with a title I cannot read. The tablet shows 1."
            $ reward_attributes_once("karaoke_tour_let_choose", [("grace", "micro")], show="auto")

    "She adds three more songs while I am still looking at the English menu."
    "I do not recognize any of the titles. Then the first few notes come through the speakers on the tablet preview, and I straighten in my seat."
    mc "I know this one."
    hikari "Of course you do. You have heard it in every shop you have walked past since you landed."
    mc "I thought it was elevator music."
    hikari "It is a love song. A very famous one. The whole country knows the chorus. You know it too — you just have never had a reason to say it out loud."
    "She adds one more. This one I recognize from a commercial on the train. I say nothing. She notices."
    hikari "You are allowed to know things from advertisements. That is how a city teaches you its songs."

    menu:
        "Ask why these songs matter to her.":
            mc "Why these ones? They are not the ones you would expect."
            hikari "My mother sang the first one. The second one was playing the summer I decided I wanted to leave this town."
            hikari "And the last one is stupid. I like it because it is stupid."
            mc "(Three reasons. None of them about being good at singing.)"
            $ reward_attributes_once("karaoke_tour_her_reasons", [("insight", "micro")], show="auto")
        "Join her on one.":
            mc "If you sing that one, I will sing the chorus. Badly."
            hikari "That is the first brave thing you have said tonight."
            "She does not wait for the tablet. She starts. I come in two beats late and miss the first word. She does not stop."
            $ reward_attributes_once("karaoke_tour_join", [("nerve", "micro")], show="auto")
        "Say nothing and listen to the preview.":
            "I let the next song play through the small speaker instead of skipping it."
            "Hikari watches me for a second, then looks away. The room gets quieter, which is strange, because neither of us has sung yet."
            hikari "You do not have to say anything about it. I am glad you heard it."
            $ reward_attributes_once("karaoke_tour_listen_her", [("grace", "micro")], show="auto")

    "The first song is mine. I am terrible."
    "I know I am terrible because Hikari is not pretending otherwise — she is sitting on the table with the cheering stick across her knees, waiting for the chorus."
    "When it comes, she hits the stick against the table exactly once, very hard, and yells something in Japanese that I do not understand."
    "I laugh in the middle of the line and lose the rest of the words. She keeps singing."
    hikari "That is the first one. The first one is never the good one. It is the one where you find out what your voice does."
    mc "And what does mine do?"
    hikari "It surprises you. That is all. Do it again."

    "We do it again. I am less terrible. This is a measurable improvement and I decide to be proud of it."
    "Then she sings her song, and I understand something I did not know I was missing: the reason people do this with other people in the room."

    menu:
        "Ask her how you choose the right song for a group.":
            mc "How do you know which song to pick when other people are here?"
            hikari "You read the room. You pick something everybody can join, something that lifts the energy instead of spending it."
            hikari "A good group song is not the one that shows what you can do. It is the one that lets everybody do something."
            mc "How do you learn that?"
            hikari "You cannot. You just keep singing until one day you notice you did it without thinking."
            $ reward_attributes_once("karaoke_tour_group_song", [("insight", "micro")], show="auto")
        "Tell her the room feels different now.":
            mc "The room feels different than it did ten minutes ago."
            hikari "That is because you stopped listening to yourself sing and started listening to me."
            mc "Is that the trick?"
            hikari "That is most of it. The rest is the stick."
            "She hands me the cheering stick. I do not use it. I just hold it."
            $ reward_attributes_once("karaoke_tour_closer", [("grace", "micro")], show="auto")
        "Admit I still do not understand.":
            mc "I still do not know how you choose. I would pick the same song every time."
            hikari "I know. That is why I keep adding songs you have heard before."
            hikari "One day you will pick one for me. I will be able to tell from the first two notes."
            $ reward_attributes_once("karaoke_tour_over_time", [("nerve", "micro")], show="auto")

    "The last hour goes faster than the first. At some point the cat ears stop feeling ridiculous."
    "On the way out, the corridor is quieter. Somebody in the last room is singing very softly to nobody in particular."
    hikari "See? You can tell what that room is doing."
    mc "Somebody is tired."
    hikari "Somebody is tired. You are learning."

    $ unlock_hikari_tour_destination("karaoke")
    $ phone_map_visit("karaoke")
    $ renpy.notify("Kuru Fuku Neko is now on your map.")
    mc "(I can come back here on my own now. She showed me the shape of it.)"
    hikari "Next time, go without me."
    mc "You are not coming?"
    hikari "I have shown you. That was the point."
    mc "(She says it lightly. It does not land lightly.)"
    hikari "And if you go — take the water. And pick a song I know."
    $ reward_attributes_once("hikari_tour_karaoke_complete", [("insight", "tiny")], show="auto")

    scene bg_train_interior with walk_fade
    "The train home is warm and half empty. Hikari falls asleep against the window with her jacket folded under her head."
    "There is a paper cup from the drink bar balanced on her knee. It does not spill."
    mc "(She brought me somewhere loud so I could finally hear her. I think that was the point.)"

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    hikari "We're home."
    mc "We're home."
    hikari "You're welcome."
    mc "I didn't say thank you."
    hikari "You were going to."
    "She goes inside before I can prove her right."
    return


label hikari_tour_combini:
    scene bg_combini with walk_fade
    "The combini is the same temperature and brightness as every other one in the city."
    hikari "This is not a tour. This is an errand with commentary."
    mc "You picked it."
    hikari "I picked it because you walk past it every day and never look inside properly."
    $ unlock_hikari_tour_destination("combini")
    "She shows me the good shelf, the bad shelf, and the machine that makes coffee one cup at a time."
    mc "(I can come back here alone. I know which door chimes when.)"
    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label hikari_tour_odaiba:
    scene bg_odaiba with walk_fade
    "Odaiba is too wide and too clean, like a street built from a drawing of a street."
    hikari "This is the future they planned. It looks better in photographs."
    mc "You don't like it."
    hikari "I didn't say that. I said it looks better in photographs."
    $ unlock_hikari_tour_destination("odaiba")
    "We walk until the water is on three sides and the city is a line of light across the bay."
    mc "(I can find the station from here. I can come back and decide what I think.)"
    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label hikari_tour_yokohama:
    scene bg_yokohama_chinatown with walk_fade
    "The train lets us out into a crowd that is already eating."
    "Two streets later the city changes its mind. Red pillars. Gold trim. A gate tall enough to be a building, with characters stacked above it like a warning."
    hikari "Yokohama Chinatown."
    mc "It doesn't look like the rest of the city."
    hikari "It isn't supposed to."
    hikari "Yokohama was a port before it was a city. In 1859 they opened it to foreign ships. The people who came to trade needed somewhere to eat, sleep, and be among their own."
    hikari "This is where the Chinese traders and cooks settled. Then their children stayed. Then their children's children."
    mc "(She says it like a history lecture. She is still walking.)"
    hikari "It is the largest Chinatown in Japan. Also the loudest. Those are separate facts."
    "A lantern swings above us. Somewhere ahead, a shopkeeper is laughing at something nobody said."
    mc "(I am a foreigner in Japan, standing in a part of Japan that is foreign to Japan. The math is doing something strange.)"

    menu:
        "Ask why the Chinese settled here, and not Tokyo.":
            mc "Why Yokohama? Why not Tokyo?"
            hikari "Tokyo was the government. Yokohama was the door."
            hikari "The port opened first here. The ships came here. The cooks came with them."
            mc "(A door needs somebody on both sides of it.)"
            $ reward_attributes_once("yokohama_tour_why_port", [("insight", "micro")], show="auto")
        "Ask if people actually live here.":
            mc "Do people live here, or is it all shops?"
            hikari "Look up."
            "I look up. Above the red awnings and the souvenir signs, there are windows. Laundry. A satellite dish. A cat asleep on a sill."
            hikari "People live here. They just also sell things to people who don't."
            mc "(It is a neighborhood wearing a costume. Or a costume with a neighborhood inside it.)"
            $ reward_attributes_once("yokohama_tour_live_here", [("grace", "micro")], show="auto")
        "Ask what happens if you order too many dumplings.":
            mc "Hypothetically. What happens if I order too many?"
            hikari "Ask me after we've eaten. You'll know then."
            mc "So that's a refusal."
            hikari "It's a postponement. I'm just hungry."
            mc "(She speeds up. I take that as an answer.)"
            $ reward_attributes_once("yokohama_tour_dumpling_math", [("nerve", "micro")], show="auto")

    "Main street is a tunnel of red lanterns and shopfronts. Steam climbs out of doorways and hangs under the eaves."
    "A woman lifts the lid off a steamer. A man shapes dough behind glass. A child runs between the tables with a plastic bag held over his head like a trophy."
    hikari "Steamed buns. Good. Not the point."
    "She points at a window where a man is folding half-moons of dough with the speed of someone who stopped counting years ago."
    hikari "Jiaozi. Gyoza, in Japanese. Chinese dumplings that came over with the cooks and stayed."
    hikari "Japanese gyoza is the cousin. More garlic, more chive, thinner skin, fried on one side. Chinese jiaozi is the one that stayed home."
    mc "So we're eating the cousin."
    hikari "We're eating the cousin in the house the family built. Close enough."
    "She points at a bamboo steamer. Inside, the dumplings are pleated like small purses and sit in a pool of their own heat."
    hikari "Shoronpo. Soup dumplings. The soup is inside. You bite a hole first or you regret it."
    mc "And the ramen?"
    hikari "Yokohama ramen has its own history. Sanmamen. Thick sauce, vegetables, a whole different animal. The port put it together."
    mc "(She has a whole map in her head. She is pretending she is only here for the food.)"

    menu:
        "Point at the soup dumplings.":
            mc "Those. The ones with the soup inside."
            hikari "Good choice. Dangerous choice."
            hikari "Bite, wait, then drink. If you put the whole thing in your mouth, you will not enjoy the next ten minutes."
            mc "(I will absolutely put the whole thing in my mouth.)"
            $ reward_attributes_once("yokohama_tour_shoronpo", [("grace", "micro")], show="auto")
        "Point at the gyoza.":
            mc "Gyoza. The real ones."
            hikari "Correct."
            mc "You didn't even look."
            hikari "I didn't need to."
            $ reward_attributes_once("yokohama_tour_gyoza_pick", [("nerve", "micro")], show="auto")
        "Point at the ramen.":
            mc "What about the ramen?"
            hikari "The ramen is for later. Or for people who don't have a plan."
            mc "You have a plan?"
            hikari "I have a stomach. It is a plan."
            $ reward_attributes_once("yokohama_tour_ramen_question", [("insight", "micro")], show="auto")

    "She walks faster. I follow."
    "We pass the big restaurants with photographs of their food and menus in four languages. She ignores all of them."
    "Then she stops."
    "Between a souvenir shop and a noodle place, there is a building so narrow it looks like the alley learned to stand up. A red sign. Three characters I can't read. A curtain in the doorway, faded to the color of old tea."
    hikari "Here."
    mc "This is a shop?"
    hikari "It is the shop."
    "She pushes the curtain aside and disappears into the steam."

    scene bg_gyoza_shop with walk_fade
    "The inside is smaller than the outside. Six stools along a counter. Two tables pushed against the wall. A ceiling fan that turns like it is thinking about stopping."
    "The air is pork fat and garlic and something clean and green. A television in the corner is playing a drama at a volume that makes the room vibrate."
    "A man's voice comes through the kitchen window. 「Jiaozi! Jiaozi!」"
    "A woman answers. 「Laile! Ni cui shenme!」"
    "A boy ducks past with a tray held over his head. Nobody looks at us. Everybody has seen us."
    "Then an old woman comes out of the kitchen."
    "She is not tall. She does not need to be. She has the face of someone who has been running this room since before I was born, and who will still be running it after I leave."
    "She looks at Hikari. Then at me. Then at the clock."
    $ lei_mood = "shout"
    lei "你又来了！"
    lei "また来たのか。"
    "Hikari's face does something I have not seen on it before. She looks caught."
    hikari "She says I'm here again. She's teasing me."
    mc "You said you found this place on a seminar trip."
    hikari "I did. I came back a few times. She remembers."
    lei "外人まで連れてきたのか。"
    hikari "She says I brought a foreigner."
    mc "You told her about me?"
    hikari "I told her I was bringing someone who gets lost. She assumed."
    "From the kitchen, the loud voice says something. The boy laughs. Hikari's ears go red."
    hikari "They're teasing me too. Something about walking out on the good restaurant."
    mc "And then coming back here?"
    hikari "A few times."
    $ lei_mood = "normal"
    lei "幾位？"
    lei "何人ですか。"
    "She says it twice. The first time in Chinese, the second in Japanese. Hikari does not speak Chinese, so Lei Lei says the important parts again for her. I wait for Hikari."
    mc "(I hold up two fingers. It feels like a confession.)"
    $ lei_mood = "shout"
    lei "坐。快點。"
    lei "座って。早く。"
    mc "(Two languages. I understand neither. I wait for Hikari.)"
    hikari "Sit. She means now."
    mc "What was the first part?"
    hikari "Chinese. I don't speak it. She repeats the important bits in Japanese for me."
    mc "So I only have to listen to you."
    hikari "That's the idea."
    "The stools are too small. The table is too small. The menu is a laminated sheet with photographs that have gone orange at the edges."
    "Lei Lei stands over us with her arms crossed. She does not hand me the menu. She waits for me to deserve it."
    $ lei_mood = "normal"
    lei "吃什麼？"
    lei "何を食べますか。"
    mc "(She is looking at me. Not Hikari. Me.)"
    hikari "She wants to know what you want."
    mc "I don't know Chinese. I don't know anything on this menu."
    hikari "Point at whatever smells best. I'll tell you if you're wrong."

    menu:
        "Let Hikari order for both of you.":
            mc "You order. I'll trust you."
            hikari "Good. I'll get us gyoza and shoronpo."
            "She orders in Japanese, quick and low. Lei Lei nods once, writes nothing down, and goes back to the kitchen."
            mc "(I catch none of it. Hikari handles it.)"
            mc "(No one wrote anything down. I do not know if that is confidence or a threat.)"
            $ reward_attributes_once("yokohama_tour_let_hikari_order", [("grace", "micro")], show="auto")
        "Try to order in Chinese.":
            mc "Um. 餃子。"
            "It is the only word I know, and I am almost certainly saying it wrong."
            $ lei_mood = "shout"
            lei "餃子！"
            "She says it back, louder, as if volume is correction."
            lei "餃子です。"
            "Then the Japanese version, for Hikari. The two words share their characters."
            lei "對。餃子。"
            lei "そう。餃子。"
            hikari "She says that's right."
            mc "And the rest?"
            hikari "That you say it like a tourist. She said that with her whole face."
            $ reward_attributes_once("yokohama_tour_order_chinese", [("nerve", "micro")], show="auto")
        "Ask what she recommends.":
            mc "What do you recommend?"
            "Hikari asks in Japanese. Lei Lei looks at me for a long second."
            $ lei_mood = "shout"
            lei "全部。"
            lei "全部です。"
            hikari "She says everything."
            mc "That is not a recommendation."
            hikari "It is a test."
            $ reward_attributes_once("yokohama_tour_recommendation", [("insight", "micro")], show="auto")

    "The kitchen does not have a door. It has an opening. Sound comes out of it the way steam does."
    "They argue in Chinese. I don't understand a word of it. Hikari doesn't either, but she leans in, listening for the Japanese when they use it."
    "Man: 「Jiaozi! Jiaozi!」"
    "Woman: 「Laile! Ni cui shenme!」"
    "Boy: 「Nainai! Dianhua!」"
    "Hikari's head moves a fraction. The boy has switched to the Japanese word — 電話, denwa — and that much she understands."
    "Lei Lei, without turning: 「Shuo wo bu zai!」"
    "The boy says something into the phone. Then he comes back and says: 「Ta shuo ta bu zai.」"
    "The man's voice turns sharp. The woman's turns sharper. I cannot follow the words. The boy laughs."
    "One of the sons puts his head through the opening and shouts something in Japanese. Hikari catches one word in it — 蒸し器, the steamer."
    "Lei Lei says a single word — 「やめて。」 — and both of them stop. I don't know the word. The room does."
    mc "What are they arguing about?"
    hikari "The steamer."
    mc "What about it?"
    hikari "Whether it is on."
    mc "Is it on?"
    hikari "That is the argument."
    "A pot hits a stove. Somebody laughs. Somebody else says a word I am fairly sure is not for children."
    mc "(I do not understand any of it. I understand all of it.)"
    mc "(Six people in a room built for three, every one of them talking at once, none of them talking to me, and I am somehow part of the conversation.)"
    hikari "You look worried."
    mc "Is someone angry?"
    hikari "They are always like this."
    mc "Always?"
    hikari "If they stop shouting, that is when you worry."
    mc "And we're just going to sit here?"
    hikari "We're going to eat. Let's just eat."
    "Hikari dips her head toward the kitchen."
    hikari "Her name is Lei Lei. She came from Shanghai when she was nineteen. She has been in Yokohama longer than she was ever anywhere else."
    hikari "She has been in this shop since before the building had a permit. She is the one who decides whether you eat well."
    mc "She decides?"
    hikari "She decides."
    hikari "Her brothers are in the kitchen. Her sister runs the front when Lei Lei lets her. Two of her sons work the steamer. The boy is a grandson."
    mc "All of them work here?"
    hikari "All of them eat here. Working is what happens between meals."

    "Lei Lei comes back with two plates and a bowl balanced on one arm. She sets them down like she is putting down a bet."
    scene bg_gyoza_dishes with walk_fade
    "The gyoza are face-down in a dark pan glaze. The bottoms are lace. The tops are soft. The shoronpo sit in a bamboo steamer, pleated like small purses. The ramen is not ramen the way I know it: thick noodles, a sauce that clings, vegetables stacked like a roof."
    hikari "Wait."
    mc "I am waiting."
    hikari "Not yet. Watch how I do it."
    "She picks up a shoronpo with her chopsticks, bites a small hole, and blows. Then she drinks the soup out of it."
    "She does not wait."
    hikari "Hot."
    mc "You told me to wait."
    hikari "I know. I should have waited as well."
    $ lei_mood = "shout"
    lei "慢點吃！"
    lei "ゆっくり食べて！"
    hikari "Slow down. She says you'll burn yourself."
    mc "I'm fine."
    lei "不是。"
    lei "違う。"
    hikari "She says no. You are not fine."
    "She puts a glass of water down hard enough to make the table jump. Hikari drinks it. Lei Lei watches her drink it. Then she goes back to the kitchen."
    mc "(I have seen people look after each other in a lot of ways. This is a new one.)"
    "The first gyoza is crisp and hot and tastes like garlic and pork and something green I cannot name. The shoronpo is a small explosion I have to think about before I take another. The ramen is a meal and an argument at the same time."
    "For a minute, nobody shouts."

    menu:
        "Tell Lei Lei the gyoza is the best you've ever had.":
            mc "This is the best gyoza I've ever eaten."
            "Hikari says it in Japanese. Lei Lei looks at me. Then at Hikari. Then back at me."
            $ lei_mood = "normal"
            lei "當然。"
            lei "当然です。"
            hikari "She says of course."
            mc "Is that good?"
            hikari "It is the best you are going to get."
            "She goes back to the kitchen. A minute later, a second plate of gyoza arrives. Nobody explains it."
            $ reward_attributes_once("yokohama_tour_compliment_lei", [("grace", "micro")], show="auto")
        "Ask Hikari how she knew about this place.":
            mc "How did you find this?"
            hikari "Seminar trip. Everyone went to the big restaurant with the photographs."
            hikari "I walked out and kept walking until I found a door with no photographs."
            mc "And she let you in?"
            hikari "She let me wait. There is a difference."
            mc "(There is. I am starting to understand the difference.)"
            $ reward_attributes_once("yokohama_tour_how_hikari_found", [("insight", "micro")], show="auto")
        "Shout the only Chinese word I know, with total confidence.":
            mc "餃子！"
            "The room stops."
            "Six faces turn toward me. Even the boy. Even the television seems quieter."
            $ lei_mood = "intense"
            lei "……"
            "Then Lei Lei laughs. It is a short, dry sound, like a drawer closing."
            "The room starts again. Somebody is repeating my pronunciation. Somebody else is correcting it."
            hikari "The room thought you were joining the argument."
            mc "I was asking what it meant."
            hikari "They heard a challenge. That's why they laughed."
            $ reward_attributes_once("yokohama_tour_shout_back", [("nerve", "micro")], show="auto")

    "Eventually the plates are empty. The television has moved on to a different argument. The boy is asleep against a stack of rice sacks."
    mc "I'll pay."
    hikari "You won't."
    "She puts money on the table before I can get to my wallet. Lei Lei picks it up, counts it, and pushes a coin back toward Hikari."
    hikari "She says the gyoza were smaller today."
    mc "Were they?"
    hikari "No."
    mc "(The coin stays on the table. Hikari leaves it there.)"
    $ lei_mood = "normal"
    lei "再來。"
    lei "またどうぞ。"
    "Then she says something else, shorter, to Hikari. Hikari's ears go red again."
    lei "あんたもね。"
    hikari "She says come back. Both of us."
    mc "That's it?"
    hikari "That's a lot. From her."
    "Lei Lei looks at me one more time. Then she points at the empty plate, then at my face. She says it in Chinese first, then in Japanese, and the Japanese is what makes Hikari smile."
    mc "What did she say?"
    hikari "She says you eat like someone who has been hungry."
    mc "Is that an insult?"
    hikari "Not from her."

    scene bg_yokohama_akarenga with walk_fade
    "Twenty minutes later the red lanterns are behind us and the streets have opened up. The water appears between the buildings in pieces, then all at once."
    "The red brick warehouses stand along the waterfront, long and low and lit at the windows. The Ferris wheel turns behind them, slow enough to look patient."
    hikari "Akarenga. Red Brick Warehouse."
    hikari "They built it at the start of the last century. Customs. Goods came off the ships and went in there."
    mc "Silk? Tea?"
    hikari "Silk. Tea. Machinery. Everything a port is for."
    hikari "The 1923 earthquake took most of the city. These buildings were still standing. Not because they were lucky. Because they were built to hold weight."
    mc "(She says that like it means something else.)"
    hikari "Now it is shops. Events. A place to take photographs."
    mc "That's a strange thing to do with a warehouse."
    hikari "It is a strange thing to do with a city. We do it anyway."

    menu:
        "Ask what the warehouses held.":
            mc "What was in them?"
            hikari "Silk, mostly. Tea. Porcelain. Things that had to get from one country to another without breaking."
            mc "And now?"
            hikari "Now? Coffee. Souvenirs. Tourists who want to stand where the ships were."
            mc "(The building did not change. The cargo did.)"
            $ reward_attributes_once("yokohama_tour_warehouse_cargo", [("insight", "micro")], show="auto")
        "Ask why she brought you here.":
            mc "Why here?"
            hikari "Because Chinatown is loud and this is quiet."
            mc "That's an answer I don't like yet."
            hikari "It is the answer I have."
            "She looks at the water instead of me."
            hikari "I like places where the city stops pretending it isn't a port."
            mc "(I do not know what to say to that. I look at the water too.)"
            $ reward_attributes_once("yokohama_tour_why_akarenga", [("grace", "micro")], show="auto")
        "Climb the outside stairs to the top landing.":
            "I find a narrow staircase at the end of the building and start climbing. Hikari follows without asking why."
            "At the top, the whole harbor is below us. The Ferris wheel. The lights on the water. The red lanterns of Chinatown, small now, burning in the distance."
            hikari "You could have just asked."
            mc "Asked what?"
            hikari "If you wanted to see it from up here."
            mc "Would you have said yes?"
            hikari "No."
            mc "(We stay up there until the wind gets cold.)"
            $ reward_attributes_once("yokohama_tour_akarenga_stairs", [("nerve", "micro")], show="auto")

    "By the time we come down, the lamps along the waterfront are on and the sky has gone the color of a peach left too long in the sun."
    hikari "You know the way back from here?"
    mc "Station, then the line home."
    hikari "Good."
    mc "That's it? Good?"
    hikari "What did you want?"
    mc "I don't know. A certificate."
    hikari "You ate. You listened. You didn't get us thrown out."
    hikari "That is the certificate."

    $ unlock_hikari_tour_destination("yokohama")
    $ phone_map_visit("yokohama")
    $ renpy.notify("Yokohama Chinatown is now on your map.")
    mc "(I can come back here on my own now. She showed me the shape of it.)"
    hikari "Next time, you can come without me."
    mc "You're not coming?"
    hikari "I have shown you. That was the point."
    mc "(She says it lightly. It does not land lightly.)"
    hikari "But if you go back to Lei Lei, order the gyoza. Not the ramen."
    mc "Why not the ramen?"
    hikari "Because the ramen is good, and the gyoza is hers."
    $ reward_attributes_once("hikari_tour_yokohama_complete", [("insight", "tiny")], show="auto")

    scene bg_train_interior with walk_fade
    "The train home is warm and half empty. Hikari falls asleep against the window with her jacket folded under her head."
    mc "(She took me to dinner and then made it a lesson. Or she made it a lesson and then took me to dinner. I am not sure which order it happened in.)"
    "The lights of Yokohama slide past the glass and go out one by one."

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    hikari "We're home."
    mc "We're home."
    hikari "You're welcome."
    mc "I didn't say thank you."
    hikari "You were going to."
    "She goes inside before I can prove her right."
    return


label hikari_tour_ueno:
    scene bg_ueno with walk_fade
    "Ueno Park in April is a picnic the whole city has agreed to attend."
    hikari "Hanami. The flowers are an excuse. The sitting is the point."
    mc "You sound like my father."
    hikari "He sounds like a sensible man. I'll take it."
    $ unlock_hikari_tour_destination("ueno")
    "We sit on the edge of somebody else's tarp until the light goes orange."
    mc "(I know which gate we came in through. I can find the rest myself.)"
    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label hikari_tour_shibuya:
    scene bg_shibuya with walk_fade
    "Shibuya Crossing is not a crossing. It is a performance that happens every two minutes."
    hikari "Stand here. Watch. Do not cross until the light changes."
    mc "I know how crossings work."
    hikari "You know how your crossings work. These are different."
    $ unlock_hikari_tour_destination("shibuya")
    "When the light changes, we cross with everyone else and nobody touches."
    mc "(The trick is not the crowd. The trick is knowing which exit to take after.)"
    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label hikari_tour_shimokitazawa:
    scene bg_shimokitazawa with walk_fade
    "Shimokitazawa is what Harajuku would be if it stopped performing."
    hikari "Small streets. Used records. A live house that looks like a fridge."
    mc "This is your kind of place."
    hikari "It is. I'm glad you noticed."
    $ unlock_hikari_tour_destination("shimokitazawa")
    "We walk the narrow streets until the shops start closing and the lamps come on."
    mc "(I can come back here alone. I know the way from the station now.)"
    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


label hikari_tour_omotesando:
    scene bg_omotesando with walk_fade
    "Omotesando is a street built to look like a forest and priced like a museum."
    hikari "The shops are glass. Then the shops end and the torii begins."
    mc "One street. Two countries."
    hikari "You noticed. Good."
    $ unlock_hikari_tour_destination("omotesando")
    "We walk the gravel path to the shrine and stop before the steps."
    mc "(I can find this again. I can come back when it is quiet.)"
    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


## --- STANDALONE TEST LABEL ----------------------------------------------------
##
## Open the console with Shift+O and type one of:
##   jump test_hikari_tour          - the Yokohama tour
##   jump test_hikari_tour_harajuku - the Harajuku tour
##   jump test_hikari_tour_karaoke  - the Kuru Fuku Neko karaoke tour
##
## These play the whole tour without having to reach a hub day first. The picker
## is forced by marking the OTHER written tours as already unlocked, so the one
## under test is always the one offered — even after a real playthrough finished it.

label test_hikari_tour:
    scene black with Dissolve(0.8)
    "TEST SEQUENCE: MESSAGE HIKARI // YOKOHAMA CHINATOWN"
    "The full tour: the texts, the station, Chinatown, Lei Lei's gyoza shop, Akarenga, and the train home."
    $ hikari_tour_unlocked = [p for p in hikari_tour_unlocked if p != "yokohama"]
    $ hikari_tour_unlocked = list(set(hikari_tour_unlocked + ["harajuku", "karaoke"]))
    call hikari_tour from _call_test_hikari_tour
    "Test complete. Yokohama is unlocked for solo visits."
    return


label test_hikari_tour_harajuku:
    scene black with Dissolve(0.8)
    "TEST SEQUENCE: MESSAGE HIKARI // HARAJUKU, TAKESHITA STREET"
    "The full tour: the texts, the station, the street, the clothes, the cotton candy, and the train home."
    $ hikari_tour_unlocked = [p for p in hikari_tour_unlocked if p != "harajuku"]
    $ hikari_tour_unlocked = list(set(hikari_tour_unlocked + ["yokohama", "karaoke"]))
    call hikari_tour from _call_test_hikari_tour_harajuku
    "Test complete. Harajuku is unlocked for solo visits."
    return


label test_hikari_tour_karaoke:
    scene black with Dissolve(0.8)
    "TEST SEQUENCE: MESSAGE HIKARI // KURU FUKU NEKO"
    "The full tour: the texts, the street corner, the drink bar, the room, the songs, and the train home."
    $ hikari_tour_unlocked = [p for p in hikari_tour_unlocked if p != "karaoke"]
    $ hikari_tour_unlocked = list(set(hikari_tour_unlocked + ["yokohama", "harajuku"]))
    call hikari_tour from _call_test_hikari_tour_karaoke
    "Test complete. Kuru Fuku Neko is unlocked for solo visits."
    return
