################################################################################
## HIKARI TOURS: MESSAGE HIKARI AND UNLOCK THE CITY
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
## Written tours, in the order she reveals them: Yokohama Chinatown, Harajuku,
## Kuru Fuku Neko (karaoke), Ueno, Shimokitazawa, and Omotesando / Meiji Shrine.
## Only tours in `hikari_tour_written` are offered, so Message Hikari never sends
## the player into a placeholder. Add the next place id there when its scene is
## ready; the picker then offers the first still-locked tour in that order, which
## is the order the in-scene callbacks and the Level docs assume. Each label ends
## by unlocking its place for the generic solo row.


label hikari_tour:
    $ last_afternoon_was_run = False
    $ last_afternoon_hikari_tour = False

    # She reveals places in a deliberate order (see hikari_tour_written), and the
    # tours' dialogue refers back to earlier ones, so offer them in sequence
    # rather than at random.
    $ tour_available = [p for p in hikari_tour_written if p in hikari_tour_available_spots()]
    if tour_available:
        $ tour_spot = tour_available[0]
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
        # as something to do with him, not as a performance. Her "I have to stay
        # after seminar" gives him a reason to accept before he can refuse.
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
                "Or, better, that you like letting things out. I need to let something out tonight.",
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
    elif tour_spot == "ueno":
        # The blossoms are the excuse. She offers the day as a place to sit,
        # which is the one thing she almost never lets herself do.
        $ run_chat("hikari", [
            {"options": [
                {"label": "Hey Hikari. Are you free after class?",
                 "send": "Hey Hikari. Are you free after class?",
                 "them": [
                     "I have nothing after four. Why?",
                     "The blossoms are out. They will not wait for a day I am less busy.",
                 ]},
            ]},
            {"them": [
                "Ueno Park. Bring whatever you want to eat.",
                "Do not worry about what to do there. That is the whole point.",
            ], "options": [
                {"label": "What do people do at a park?",
                 "send": "What do people do at a park?",
                 "them": ["Sit. That is the honest answer.", "You will see. It is harder than it sounds."]},
                {"label": "I'm not good at doing nothing.",
                 "send": "I'm not good at doing nothing.",
                 "them": ["I know. That is why I am taking you.", "One afternoon. You can fail at it with me."]},
            ]},
            {"them": ["Meet me at the gate. Wear something you can sit in."]},
        ])
    elif tour_spot == "shimokitazawa":
        # This is her old place, and she is more excited than she means to be.
        # The hook is music, not a landmark.
        $ run_chat("hikari", [
            {"options": [
                {"label": "Hey Hikari. Are you free after class?",
                 "send": "Hey Hikari. Are you free after class?",
                 "them": [
                     "Yes, actually, I have been waiting for you to ask.",
                     "There is a record shop I have not been to in a long time.",
                 ]},
            ]},
            {"them": [
                "Shimokitazawa. I used to go there before... before I got busy.",
                "There is a record I almost bought once. I want to see if it is still there.",
            ], "options": [
                {"label": "You still think about a record?",
                 "send": "You still think about a record?",
                 "them": ["Yes. Do not make that face.", "You will understand when you hear it."]},
                {"label": "Lead the way.",
                 "send": "Lead the way.",
                 "them": ["Good. I know the shortcut from the station."]},
            ]},
            {"them": ["Four o'clock. The small gate, not the big one.", "And do not say I am being nostalgic."]},
        ])
    elif tour_spot == "omotesando":
        # The hook is disbelief. She offers something that sounds impossible in
        # the middle of Tokyo, then refuses to explain it over text.
        $ run_chat("hikari", [
            {"options": [
                {"label": "Hey Hikari. Are you free after class?",
                 "send": "Hey Hikari. Are you free after class?",
                 "them": [
                     "I have nothing after four. Why?",
                     "Do you believe me if I say there is a forest in the middle of Tokyo?",
                 ]},
            ]},
            {"them": [
                "Not a park. A forest. A hundred thousand trees, and the loudest street in the country at the edge of it.",
                "I want to show you something before the light goes.",
            ], "options": [
                {"label": "A hundred thousand?",
                 "send": "A hundred thousand?",
                 "them": ["That is the number they give you. I have never counted.", "You can try. It will take the whole afternoon."]},
                {"label": "You're texting like a tour guide again.",
                 "send": "You're texting like a tour guide again.",
                 "them": ["I am a tour guide. You finally noticed.", "Wear shoes you can walk in. The gravel is the point."]},
            ]},
            {"them": [
                "Omotesando station. The exit with the trees.",
                "And bring a five-yen coin. I will explain when we get there.",
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
    elif tour_spot == "ueno":
        hikari "Today we are not going anywhere. We are going to sit."
        mc "That is the whole plan?"
        hikari "That is the whole plan. Try not to improve it."
    elif tour_spot == "shimokitazawa":
        hikari "I know a shortcut. It involves one alley and a cat that may or may not approve."
        mc "You come here a lot?"
        hikari "I used to. That is different."
    elif tour_spot == "omotesando":
        hikari "Two stops. Then we walk uphill."
        mc "Uphill to a forest?"
        hikari "Uphill to a street that thinks it is a forest. Then a forest that is."
    elif tour_spot == "karaoke":
        hikari "Tonight we sing. That is all I am telling you."
        mc "What if I am terrible?"
        hikari "Then you will be terrible with me in the room. That is better than being terrible alone."
    elif tour_spot == "harajuku":
        hikari "Rule one. We look at everything. We buy no clothes until the third shop."
        mc "Why the third?"
        hikari "The first two are for people who photograph themselves. The third is for people who actually wear it."
        mc "(She has a rule for everything. Most of them turn out to be true.)"
    if tour_spot == "harajuku":
        hikari "Come on. I want to get there before the line."
    elif tour_spot == "ueno":
        hikari "Come on. The tarps will be going."
    else:
        hikari "Come on. I want to get there before the light changes."
    "She turns before I can ask anything else. I follow her."

    $ renpy.jump("hikari_tour_" + tour_spot)


## --- THE TOUR SCENES ---------------------------------------------------------
##
## Six tours are written: Yokohama, Harajuku, Kuru Fuku Neko, Ueno,
## Shimokitazawa, and Omotesando / Meiji Shrine. Odaiba and Shibuya
## still fall through to their placeholders: Hikari arrives with him,
## introduces the place, and the unlock happens at the end. Replace those lines
## and add choices/rewards there when those scenes are written. The message
## flow, picker, unlock, and solo fallback do not move.

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
    hikari "What? No. I could not..."
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
            "She waits. I fail. She laughs, a real one, not the one she uses at the table."
            hikari "You are hopeless."
            mc "I know."
            $ reward_attributes_once("harajuku_tour_kawaii_speechless", [("nerve", "micro")], show="auto")
        "Ask if she is comfortable.":
            mc "Is it comfortable?"
            hikari "It is a dress made for standing still in a shop window. No."
            mc "Then why..."
            hikari "Because you could not speak. I wanted to see how long it would last."
            $ reward_attributes_once("harajuku_tour_kawaii_comfort", [("insight", "micro")], show="auto")

    "She does not take it off."
    "She keeps the dress and the ribbon and the ridiculous socks for the rest of the day: through the candy shop and onto the train."

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
            hikari "Good. Walk the whole street. Buy nothing at the first two shops."
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
    "The train home is warm and half empty. Hikari falls asleep against the window, her head tipped against the glass."
    "There is a streak of pink sugar on her finger that she never wiped off."
    mc "(She took me to a street where nobody is embarrassed to be seen. I think that was the point.)"

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    hikari "We're home."
    mc "We're home."
    hikari "You're welcome."
    mc "I didn't say thank you."
    hikari "You were going to."
    "She goes inside before I can prove her right."
    "By the time I reach the front step, the ribbon is gone. She is wearing her own clothes again, and she never mentions the dress."
    $ hikari_kawaii = False
    return


label hikari_tour_karaoke:
    scene bg_karaoke_outside with walk_fade
    "Kuru Fuku Neko is three floors of neon above a closed bakery, with a cat over the door wearing a small red bib."
    "The sign has a line of Japanese under it that Hikari is reading with her mouth slightly open."
    hikari "来る福猫. The cat that brings luck when it comes. A verb, a blessing, and a cat. That is the whole name."
    mc "It is a very good name."
    hikari "I know. I am glad you said that first."

    "She does not go in yet. She turns to me on the pavement like this is the important part of the tour."
    hikari "Karaoke is not a stage. That is the thing people get wrong. You rent a room, a box, by the hour, and the room is yours."
    hikari "Nobody is in it with you unless you ask them in. The machine does not judge, the walls do not judge, and the score is a suggestion."
    mc "So it is for people who cannot sing."
    hikari "It is for people who cannot sing and do it anyway. That is a different thing."
    hikari "You pay for the room, and then for what you drink. Or you take 飲み放題, nomihoudai, and the drinks keep coming for a fixed price."
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
            "She takes a pair for herself. She does not explain. She wears them for the rest of the night and never once takes them off."
            $ reward_attributes_once("karaoke_tour_costume", [("nerve", "micro")], show="auto")

    "We go in. The corridor is narrower than the street and twice as loud."
    "A woman's voice comes through one wall, doing a ballad with her whole life in it. Through the next, a group is laughing and losing the chorus on purpose."
    "Further down, somebody is singing the same two lines over and over, stopping each time at exactly the same word."
    hikari "Listen. That one from the first room, everybody knows it. It is from a drama. You have heard it, even if you do not know you have."
    mc "And the two lines?"
    hikari "Somebody is practising. That is the bravest room in this building."
    "She hums a few bars of something as we walk. I do not recognize it. She stops when she notices me listening."
    hikari "You can tell what a room is doing from the song. That is a real skill."
    mc "I cannot tell anything."
    hikari "You will. You already know the difference between the laughing room and the practising room. That is most of it."

    scene bg_karaoke_drink with walk_fade
    "The drink bar is a wall of taps and a row of machines that dispense colours I have no names for."
    "There is a soft-serve machine at the end, and a fridge full of things with cartoon cats on them."
    hikari "Before anything else: water. Singing is exercise and nobody tells you that."
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
            hikari "You pay for a block of time and you order from this list. Alcohol, tea, soda, all of it. They bring it to the room."
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
            "Then I add the only English title I know. The tablet shows 1."
            $ reward_attributes_once("karaoke_tour_tablet", [("insight", "micro")], show="auto")
        "Pick an English song.":
            mc "I am picking this one. It is the only one I know all the words to."
            "I add it to the queue. The tablet says the song title, then a number: 1."
            hikari "One. That means we are next."
            mc "Next? There is nobody else in this room."
            hikari "There is a queue. That is different."
            $ reward_attributes_once("karaoke_tour_pick_song", [("nerve", "micro")], show="auto")
        "Let her pick my song.":
            mc "You choose. I will follow."
            hikari "That is the safest thing you have said all evening."
            "She picks something I know from a commercial on the train. The tablet shows 1."
            $ reward_attributes_once("karaoke_tour_let_choose", [("grace", "micro")], show="auto")

    "She adds two more songs while I am still looking at the English menu."
    "I do not recognize any of the titles. Then the first few notes come through the speakers on the tablet preview, and I straighten in my seat."
    mc "I know this one."
    hikari "Of course you do. You have heard it in every shop you have walked past since you landed."
    mc "I thought it was elevator music."
    hikari "It is a love song. A very famous one. The whole country knows the chorus. You know it too, you just have never had a reason to say it out loud."
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
            "She queues the song and taps the flag in the corner. Mine is next. Hers is after."
            $ reward_attributes_once("karaoke_tour_join", [("nerve", "micro")], show="auto")
        "Say nothing and listen to the preview.":
            "I let the next song play through the small speaker instead of skipping it."
            "Hikari watches me for a second, then looks away. The room gets quieter, which is strange, because neither of us has sung yet."
            hikari "You do not have to say anything about it. I am glad you heard it."
            $ reward_attributes_once("karaoke_tour_listen_her", [("grace", "micro")], show="auto")

    "The first song is mine. I am terrible."
    "I know I am terrible because Hikari is not pretending otherwise: she is sitting on the table with the cheering stick across her knees, waiting for the chorus."
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

    "The last hour goes faster than the first."
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
    hikari "And if you go, take the water. And pick a song I know."
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
    play music "audio/Music/chinese_restaurant.mp3" fadein 2.0
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
    mc "You come here a lot, don't you?"
    hikari "I do. She remembers."
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
    "Hikari's head moves a fraction. The boy has switched to the Japanese word, 電話, denwa, and that much she understands."
    "Lei Lei, without turning: 「Shuo wo bu zai!」"
    "The boy says something into the phone. Then he comes back and says: 「Ta shuo ta bu zai.」"
    "The man's voice turns sharp. The woman's turns sharper. I cannot follow the words. The boy laughs."
    "One of the sons puts his head through the opening and shouts something in Japanese. Hikari catches one word in it: 蒸し器, the steamer."
    "Lei Lei says a single word, 「やめて。」, and both of them stop. I don't know the word. The room does."
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

    "Lei Lei comes back with two plates balanced on one arm. She sets them down like she is putting down a bet."
    scene bg_gyoza_dishes with walk_fade
    "The gyoza are face-down in a dark pan glaze. The bottoms are lace. The tops are soft. The shoronpo sit in a bamboo steamer, pleated like small purses."
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
    "The first gyoza is crisp and hot and tastes like garlic and pork and something green I cannot name. The shoronpo is a small explosion I have to think about before I take another."
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

    stop music fadeout 1.5
    scene bg_yokohama_akarenga with walk_fade
    "Twenty minutes later the red lanterns are behind us and the streets have opened up. The water appears between the buildings in pieces, then all at once."
    "The red brick warehouses stand along the waterfront, long and low and lit at the windows. The Ferris wheel turns behind them, slow enough to look patient."
    hikari "Akarenga. Red Brick Warehouse."
    hikari "They built it at the start of the last century. Customs. Goods came off the ships and went in there."
    mc "Silk? Tea?"
    hikari "Silk. Tea. Porcelain. Everything a port is for."
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
    if store.story_day >= 24:
        "Ueno Park in May is a picnic the whole city has agreed to attend."
        "Blue tarps under the trees. Cardboard trays, paper cups, a radio turned low enough that only the table can hear it."
        "The blossoms are gone. The trees are green and heavy, and the tarps are out anyway."
    else:
        "Ueno Park in April is a picnic the whole city has agreed to attend."
        "Blue tarps under the trees. Cardboard trays, paper cups, a radio turned low enough that only the table can hear it."
        "The blossoms are already falling. The ground is pink everywhere nobody has walked."
    hikari "Hanami."
    mc "Flower viewing."
    if store.story_day >= 24:
        hikari "That is the name. The flowers are an excuse in any season. The sitting is the point."
    else:
        hikari "That is the translation. The flowers are an excuse. The sitting is the point."
    mc "You sound like my father."
    hikari "He sounds like a sensible man. I'll take it."

    "There are hundreds of people under the trees. I keep waiting for the noise of a crowd: voices carrying between groups, somebody calling across the grass."
    "Nothing. Each tarp is its own small country. People walk between them without looking in, the way you pass an open door in a building you do not live in."
    mc "There are so many people here and nobody is talking to anybody."
    hikari "They are talking. Just not across."
    hikari "At a picnic where I grew up, people wander over. They bring food and meet you. Here the tarp is a room. You can sit in a crowd of ten thousand people and still be private."
    hikari "I think that is why everybody comes. It is the one place in the city where being alone is not lonely."
    mc "Where I come from, if you sit next to somebody they talk to you whether you want it or not."
    hikari "That sounds exhausting."
    mc "Sometimes. Sometimes it is the best part of the day."
    "She does not answer that one. She looks at the tarps for a moment longer than she needs to."

    "She walks us past the first few groups without stopping. She is looking for a place, not a view."
    hikari "This was a temple once. Kan'ei-ji, built in the sixteen twenties by the Tokugawa family. It was their family temple, big enough to be a village."
    hikari "Then the shogunate fell, and the temple was destroyed in the fighting. In eighteen seventy-three they opened the grounds as a park."
    mc "They gave a temple to everybody?"
    hikari "They gave what was left of it to everybody. That is a very Japanese move."
    hikari "A year later they put the national museum here. The zoo came after that. Both were the first of their kind in the country."
    mc "So a park with a museum and a zoo."
    hikari "A place to sit, a place to keep things, and a place to look at animals. The city decided you needed all three."

    menu:
        "Ask why the museum is in a park.":
            mc "Why put a museum in a park?"
            hikari "Because the temple was already here, and the buildings were already big. But also, I think, because a park is where you bring what you want to keep."
            hikari "The city lost a temple and built a place that keeps things instead. That is not the same as getting it back. It is something else."
            mc "(Something else. She says that like it is a category.)"
            $ reward_attributes_once("ueno_tour_museum", [("insight", "micro")], show="auto")
        "Ask about the cherry trees.":
            mc "Are all of these trees part of the park?"
            hikari "They planted a thousand when it opened. A thousand trees so there would be somewhere to sit in spring."
            hikari "They last about a week. That is the whole secret of this place. A week of sitting under something that will be gone."
            mc "That sounds sad."
            hikari "It is a week of sitting under something that will be gone. You can call it sad after you have sat down."
            $ reward_attributes_once("ueno_tour_trees", [("insight", "micro")], show="auto")
        "Claim a place on a tarp.":
            "I step onto the edge of an empty blue tarp and sit before I have worked out whether it belongs to anybody."
            hikari "...That one is ours now."
            mc "We do not know whose it was."
            hikari "Nobody does. That is how this works."
            "She sits beside me and takes off her shoes. I have never seen her take off her shoes in the afternoon."
            $ reward_attributes_once("ueno_tour_tarp", [("nerve", "micro")], show="auto")

    "A man at the next tarp is pouring from a thermos into a paper cup. He pours a second cup and holds it out in our direction without looking."
    hikari "...That does not usually happen."
    mc "What?"
    hikari "You were looking at his bottle. He noticed. That is all. Do not turn it into a story."
    hikari "Take it with both hands. Say いただきます."
    mc "What does it mean?"
    hikari "Something like: I receive this. It is polite. It is also true."
    "I take the cup with both hands. It is tea, and it is far too sweet. The man does not look at me. Hikari drinks hers like this is a normal Tuesday."
    mc "He did not say anything."
    hikari "He gave you a cup. That was the whole conversation."
    hikari "If you cannot drink it, you can hold it. Nobody here will ask you to finish."
    mc "(A cup you are allowed to hold. I decide to drink it anyway.)"

    menu:
        "Drink the tea.":
            "I drink it. It is sweeter than anything I have had in this country and somehow exactly right for the afternoon."
            hikari "See?"
            mc "I hate that you are right about things."
            hikari "No, you do not. You are just slow about admitting it."
            $ reward_attributes_once("ueno_tour_tea", [("grace", "micro")], show="auto")
        "Ask what happens if you refuse.":
            mc "What if I do not want the cup?"
            hikari "You can say 結構です and leave it. Nobody is offended. But you have to actually say it: you cannot just ignore the hand."
            hikari "Most things here are like that. The offer matters more than the answer."
            $ reward_attributes_once("ueno_tour_refuse", [("insight", "micro")], show="auto")
        "Hold the cup without drinking.":
            "I hold the cup in both hands and do not drink from it. Hikari glances at it, then at me."
            hikari "That is also allowed. You are allowed to hold a thing and not use it."
            mc "You make that sound like a philosophy."
            hikari "It is one. It is the one this park is for."
            $ reward_attributes_once("ueno_tour_hold", [("insight", "micro")], show="auto")

    "For an hour nobody crosses the line between one tarp and the next. A group on a blue sheet passes a bottle to the left. A family three metres away passes a bag of oranges to the right. Neither group looks at the other."
    mc "It is like everybody is in their own house with the walls taken down."
    hikari "That is a good way to say it. The walls are just agreed on."
    "I raise my phone toward a salaryman asleep with his hat over his face. Hikari's hand comes down on the phone."
    hikari "Do not."
    mc "He is asleep in public."
    hikari "That is why. This is one of the few places in this city where you can fall asleep without it meaning anything."
    hikari "If you photograph it, it means something."
    "I put the phone away. The blossoms keep coming down. One lands on the rim of the cup in my hand."

    menu:
        "Watch the lines nobody crosses.":
            "I spend ten minutes watching the space between the tarps. A paper cup rolls out of one group and stops in the aisle. Nobody claims it. A woman from the next tarp gets up, walks past it, and sits down again."
            hikari "You are learning the shape of the room."
            mc "It is not a room. There are no walls."
            hikari "There are always walls. Some of them you can only see if you watch."
            $ reward_attributes_once("ueno_tour_lines", [("insight", "micro")], show="auto")
        "Ask why nobody photographs each other here.":
            mc "Why is nobody taking pictures? There are whole families here."
            hikari "Because they are doing the thing, not reporting on it. That is the difference between this street and the ones we walked before it."
            hikari "You can tell which one a place is by looking at what people hold up."
            $ reward_attributes_once("ueno_tour_photos", [("insight", "micro")], show="auto")
        "Leave the blossom where it landed.":
            "I leave it. The petal sits on the rim and slowly goes dark at the edges."
            hikari "You are watching it change."
            mc "It is a small thing."
            hikari "It is the entire point of the day, and you just did it without being told."
            $ reward_attributes_once("ueno_tour_petal", [("grace", "micro")], show="auto")

    "Later we walk to the museum steps. It is cooler here, out of the paper and the cooking smells."
    scene bg_ueno_museum with walk_fade
    "The building is older than the country I came from and much calmer about it."
    hikari "We are not going in."
    mc "Why show me the steps, then?"
    hikari "Because this is the part I can give you. Inside there are ten thousand things and I would spend an hour explaining one of them badly."
    hikari "Out here you can see the shape of the decision. A park that keeps things."
    mc "Do you like museums?"
    hikari "I like that somebody decided these things were worth keeping. Even the ones I do not understand."
    "She says it to the doors, not to me. I let it stand."
    hikari "My mother brought me here. I remember the tea was too sweet."

    menu:
        "Ask what she would keep.":
            mc "If you could put one thing in there, what would it be?"
            hikari "Nothing. Things last longer when nobody is trying to preserve them."
            mc "That sounds like something you have thought about."
            hikari "It is something I have felt. Those are different."
            $ reward_attributes_once("ueno_tour_keep", [("insight", "micro")], show="auto")
        "Say you would go in next time.":
            mc "I will come back and go inside. On my own."
            hikari "Good. Take the east room first. It is quiet and nobody goes there."
            mc "You have been in there."
            hikari "Once. I did not tell you because you would have made it important."
            $ reward_attributes_once("ueno_tour_next_time", [("nerve", "micro")], show="auto")
        "Sit on the steps for a minute.":
            "We sit on the museum steps with our backs to the doors and the park going on without us."
            mc "That is what I remember too."
            hikari "Then we agree about something."
            $ reward_attributes_once("ueno_tour_steps", [("grace", "micro")], show="auto")

    "We go back to the tarp. The light has gone orange, then grey. The radio has switched from music to a weather report nobody is listening to."
    "Hikari lies back with her hands behind her head and watches the blossoms come down."
    hikari "I have not sat still like this in weeks."
    mc "You are always taking me somewhere."
    hikari "I know. This is the first hour I have not been the one who knows where we are going."
    hikari "It is nice. Do not make it important."
    "Below us, two groups sit almost close enough to touch and do not. A bottle goes round one tarp. A bag of oranges goes round the other."
    hikari "I used to think it was a shame. That people could be this close and still not reach."
    mc "And now?"
    hikari "Now I think it might be a kindness. Or I am just tired of wanting it to be different."
    mc "Different how?"
    "She is quiet long enough that I think she will not answer."
    hikari "Somebody should make it easier. That is all."
    mc "Make what easier?"
    hikari "Reaching."
    "She says it in the same voice she has used all day. I let it lie there."
    "I lie down beside her. A petal lands on my sleeve. I do not move it."

    menu:
        "Stay until the light goes.":
            "We stay. Nobody talks. The old man at the next tarp pours himself one last cup and does not offer it to anybody."
            mc "(The flowers are an excuse. The sitting is the point.)"
            $ reward_attributes_once("ueno_tour_stay", [("grace", "micro")], show="auto")
        "Ask if she used to come here as a child.":
            mc "You said your mother brought you. Did you come a lot?"
            hikari "Every spring. I did not understand why until I was older."
            mc "And now?"
            hikari "Now I understand that I did not need to understand it."
            $ reward_attributes_once("ueno_tour_childhood", [("insight", "micro")], show="auto")
        "Say the day is almost over.":
            mc "We should go soon."
            hikari "I know."
            "She does not move. I do not move either. For once, neither of us is right about anything."
            $ reward_attributes_once("ueno_tour_end", [("nerve", "micro")], show="auto")

    $ unlock_hikari_tour_destination("ueno")
    $ phone_map_visit("ueno")
    $ renpy.notify("Ueno Park is now on your map.")
    mc "(I can come back here on my own now. She showed me the shape of it.)"
    hikari "Next time, sit somewhere different."
    mc "You are not coming?"
    hikari "I have shown you. That was the point."
    mc "(She says it lightly. It does not land lightly.)"
    hikari "And take a cup if somebody offers. You looked like you wanted to."
    $ reward_attributes_once("hikari_tour_ueno_complete", [("insight", "tiny")], show="auto")

    scene bg_train_interior with walk_fade
    "The train home is warm and half empty. Hikari falls asleep against the window with her jacket folded under her head."
    mc "(She spent the whole day teaching me how to do nothing. I think she needed the lesson more than I did.)"

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    hikari "We're home."
    mc "We're home."
    hikari "You're welcome."
    mc "I didn't say thank you."
    hikari "You were going to."
    "She goes inside before I can prove her right."
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
    "We take the small gate out of the station, which is not a gate at all but a gap between a bicycle shop and a wall."
    "A cat is sitting in the gap. Hikari stops, crouches, and holds out one finger. The cat examines it and goes back to sleep."
    hikari "He approves. We can go."
    mc "You know the cat."
    hikari "I know the cat."
    "The street is narrow enough that two people have to turn sideways to pass. The shops are small and the signs are hand-painted."
    hikari "Shimokitazawa. What Harajuku would be if it stopped performing."
    mc "Nobody here is dressed up."
    hikari "Everybody here is dressed as themselves. That is a different amount of work."
    "She walks faster than usual. I have to half-run to keep up, and when I mention it she slows down without admitting anything."

    hikari "After the war, the rent here was cheap. Small theaters moved in: 小劇場, little rooms with fifty seats and no money for a proper sign."
    hikari "Then came the students, then the record shops, then the clothes. It has never been rebuilt into anything newer."
    mc "Is that on purpose?"
    hikari "I think nobody could agree on what to rebuild it into. That is how the best places happen."
    hikari "There is a live house with a door like a fridge. If you stand near it during soundcheck you can feel the bass in your teeth."

    menu:
        "Ask why she knows this place so well.":
            mc "You know the cat, the shortcut, the door. How?"
            hikari "I came here a lot. Before."
            mc "Before what?"
            hikari "Before I decided what I was going to be."
            "She says it lightly and then looks in a shop window for a second longer than necessary."
            $ reward_attributes_once("shimokita_tour_before", [("insight", "micro")], show="auto")
        "Ask about the little theaters.":
            mc "Fifty seats? How does a theater survive on fifty seats?"
            hikari "It does not. That is not the point. The point is that somebody can rent a room and put on the thing they wrote."
            hikari "No committee, no application. You want to do it, you do it."
            mc "(She says it the way other people say a rule about trains.)"
            $ reward_attributes_once("shimokita_tour_theaters", [("insight", "micro")], show="auto")
        "Follow the sound of a bass line.":
            "A drum beat is coming from somewhere ahead. I turn toward it. Hikari catches my sleeve and steers me back."
            hikari "That is the soundcheck. We are not ready for the soundcheck yet."
            mc "There is a sequence?"
            hikari "There is always a sequence. You will see."
            $ reward_attributes_once("shimokita_tour_sequence", [("nerve", "micro")], show="auto")

    scene bg_record_shop with walk_fade
    "The record shop is four crates wide and smells like paper and dust. The sign says 中古, used, and nothing else."
    "Hikari goes straight to the third crate from the door. Not the first two. She does not look at the others."
    hikari "If a shop has been here a long time, the good things sink. People pull them out and put them back in the wrong place."
    mc "You can tell where they sank?"
    hikari "I can guess. That is not the same as knowing."
    "She flips through the third crate with her whole arm, fast, the way someone checks a pocket they have checked a thousand times."
    "Then she stops."
    hikari "...It is still here."
    "She pulls out a record in a faded sleeve. The cover is a photograph of a street at night, nothing famous, nothing anyone would recognize."
    mc "That is the one?"
    hikari "I almost bought it. I was nineteen and I had exactly enough money and I decided I would come back the next week."
    mc "And?"
    hikari "And then I did not come back for nine years."
    "She holds it for a moment, then puts it back in the crate, in the exact place she found it."

    menu:
        "Tell her to buy it.":
            mc "Buy it. You found it again. That means something."
            hikari "That means I found it again. I would buy it and put it on a shelf and never play it."
            mc "Then buy it and play it."
            hikari "You are very practical today."
            "She takes it to the counter anyway. She asks the clerk to play a track. She never gets as far as paying."
            $ reward_attributes_once("shimokita_tour_buy_record", [("grace", "micro")], show="auto")
        "Ask what the song sounds like.":
            mc "What does it sound like?"
            hikari "Like a city at three in the morning. Like being the only person awake and not minding."
            "She says it before she thinks about it, then stops."
            hikari "That is a bad description. Ignore it."
            $ reward_attributes_once("shimokita_tour_sound", [("insight", "micro")], show="auto")
        "Recognize a song from an ad.":
            "A different track is playing over the shop speakers. I know it from a commercial on the train."
            mc "I know this one. From the station."
            hikari "You do. That is a real song, and you learned it from a thirty-second ad."
            mc "Is that embarrassing?"
            hikari "No. That is how music gets into a city. It shows up where you are not trying to listen."
            "She looks almost impressed, which she immediately tries to hide."
            $ reward_attributes_once("shimokita_tour_ad_song", [("nerve", "micro")], show="auto")

    "We leave the shop. She is not carrying the record, but she walks with her hands tucked into her sleeves like she is keeping something warm."

    scene bg_live_house with walk_fade
    "The live house has a hand-painted sign and a steel door with no window. It really does look like a fridge."
    "From inside comes the sound of a drummer counting in, then stopping, then counting in again."
    hikari "They are doing that for twenty minutes. The band before them was terrible, so they are making sure they are not."
    mc "You can tell all that from a door?"
    hikari "I can tell some of it. The rest I remember."
    "There is a setlist taped beside the door. She reads it, and something happens to her face that I do not have a name for."
    hikari "I know this band. Nobody knows this band. I used to know the singer's name."
    mc "Do you still?"
    hikari "...Yes. I was testing myself."
    "The bass comes through the door and into my chest. She does not push it open."
    hikari "I used to come here when I was somebody else."
    mc "Who?"
    hikari "Somebody who went to shows and did not have to be the one who knew where everything was."
    "She turns away from the door before I can answer. She is not crying. I can tell because she is angry about it."

    menu:
        "Go in anyway.":
            mc "Let us go in."
            hikari "No."
            mc "Why not?"
            hikari "Because if I go in now I will expect it to feel like it did, and it will not."
            hikari "Come on. There is a coffee place I know."
            $ reward_attributes_once("shimokita_tour_go_in", [("nerve", "micro")], show="auto")
        "Ask about the singer.":
            mc "What was the singer's name?"
            "She tells me. I have never heard it. She says it again, slower, like leaving it in the air."
            hikari "Nobody remembers. That is what I am getting used to."
            mc "I will remember it."
            hikari "You will forget by the train. That is all right. You said it."
            $ reward_attributes_once("shimokita_tour_singer", [("grace", "micro")], show="auto")
        "Listen to the soundcheck.":
            "We stand at the door until the drummer finally gets through the count-in and the bass joins him."
            "Hikari closes her eyes for four bars. When she opens them, she is ordinary again."
            hikari "That is enough. I got what I came for."
            $ reward_attributes_once("shimokita_tour_soundcheck", [("insight", "micro")], show="auto")

    scene bg_shimokita_cafe with walk_fade
    "The coffee shop has six tables and a window that looks out on the alley we came through. The owner does not ask what we want. He brings two cups."
    hikari "He remembers me."
    mc "After nine years?"
    hikari "He has a very good memory for people who ordered the same thing every week."
    "She wraps both hands around the cup. This is the first time all day she has not been walking."

    hikari "I wanted to be a person who came to places like this. Not the person who runs a club, not the one who knows the train times. Just somebody in the crowd at the front."
    mc "You are that person. Right now."
    hikari "No. I am the person who brought you here and explained the neighborhood. That is the job."
    hikari "But for about three songs I was the other one."
    mc "What happened to her?"
    hikari "She got busy. That is what happened to everybody."
    "She looks out the window at the cat, who has moved to a warmer patch of wall."
    hikari "I do not miss the music. I miss that I did not have to be good at it."
    mc "You do not have to be good at things with me."
    hikari "I know. That is why I brought you."

    menu:
        "Ask if she would go back.":
            mc "Would you go back? To the shows."
            hikari "Maybe. Not the way I went before. I would have to stand at the back."
            mc "Why the back?"
            hikari "Because that is where you go when you want to listen instead of be seen. I am learning that."
            $ reward_attributes_once("shimokita_tour_go_back", [("insight", "micro")], show="auto")
        "Tell her about Circle.":
            mc "At the photography club, Sim says the point is being seen. You said this place is the opposite."
            hikari "He is right about his place. I am right about this one. Both can be true."
            hikari "Some days you need a room where somebody is looking at you. Some days you need a room where nobody is."
            mc "How do you know which one you need?"
            hikari "You do not. You try both. That is why I am taking you everywhere."
            $ reward_attributes_once("shimokita_tour_circle", [("grace", "micro")], show="auto")
        "Say nothing and drink the coffee.":
            "I drink the coffee. It is better than I expected and I say so."
            hikari "I told you he remembers me. He makes it properly for people he remembers."
            "She does not say anything else, and it is not awkward. I am starting to understand that silence with her is a place she can stand."
            $ reward_attributes_once("shimokita_tour_silence", [("grace", "micro")], show="auto")

    "We walk back toward the station the long way. Shops are pulling their shutters down. A guitar case is leaning against a closed door with nobody around."
    hikari "I showed you a street where everybody is dressed to be looked at. This one is a street where nobody is."
    mc "Which one is the real Japan?"
    hikari "Both. And neither, if you are asking which one is the whole country."
    hikari "A city is not one place. It is a hundred small rules about what you are allowed to do in each room. That is the thing to learn."

    menu:
        "Ask which rule she likes best.":
            mc "Which of the rules do you like?"
            hikari "The one at the record shop. If you find something you almost bought, you are allowed to buy it the second time."
            mc "Is that an actual rule?"
            hikari "No. It is one I made up today."
            $ reward_attributes_once("shimokita_tour_rule", [("insight", "micro")], show="auto")
        "Say you liked this place more than Harajuku.":
            mc "I think I liked this more than Harajuku."
            hikari "I know. That is why I left it until now."
            mc "You planned the order?"
            hikari "I planned the order. Do not tell me it did not work."
            $ reward_attributes_once("shimokita_tour_order", [("nerve", "micro")], show="auto")
        "Ask her to come back with you next time.":
            mc "Come back here with me next time."
            hikari "...Ask me that again when you have been without me for a while."
            mc "That is not an answer."
            hikari "It is the only answer I have today."
            $ reward_attributes_once("shimokita_tour_next_time", [("grace", "micro")], show="auto")

    $ unlock_hikari_tour_destination("shimokitazawa")
    $ phone_map_visit("shimokitazawa")
    $ renpy.notify("Shimokitazawa is now on your map.")
    mc "(I can come back here on my own now. She showed me the shape of it.)"
    hikari "Next time, take the small gate. The cat will remember you."
    mc "You are not coming?"
    hikari "I have shown you. That was the point."
    mc "(She says it lightly. It does not land lightly.)"
    hikari "And if the record is still there, buy it."
    $ reward_attributes_once("hikari_tour_shimokitazawa_complete", [("insight", "tiny")], show="auto")

    scene bg_train_interior with walk_fade
    "The train home is warm and half empty. Hikari falls asleep against the window with her jacket folded under her head."
    mc "(She showed me a place where nobody has to perform. I think she was showing herself the way back to it.)"

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    hikari "We're home."
    mc "We're home."
    hikari "You're welcome."
    mc "I didn't say thank you."
    hikari "You were going to."
    "She goes inside before I can prove her right."
    return


label hikari_tour_omotesando:
    scene bg_train_interior with walk_fade
    "The carriage is full of people who have finished their day and people who have not started theirs. Nobody speaks."
    "Hikari stands with one hand through the strap and does not look at her phone."
    mc "You are not going to tell me what the forest is."
    hikari "I am not."
    mc "Why not?"
    hikari "Because you would look it up and then you would already know it when we got there. I want to watch you find out."
    "I put my phone away."

    scene bg_omotesando with walk_fade
    "Omotesando Station lets us out under the trees."
    "Not the little street trees of the side roads. These are zelkova, tall as a building and wide, and the pavement beneath them is broad enough for four people to walk abreast and still not touch."
    mc "This is the forest?"
    hikari "This is the road to the forest. It has opinions about itself."

    "She starts walking without checking whether I am following. She knows I am."
    hikari "Omotesando. Omote means front. Sandou means approach. This was the front approach to the shrine."
    mc "A road for a god."
    hikari "For an emperor, first. They made him a god after he died, which is a promotion nobody asks for."
    hikari "The road went up in the Taishou era, when the shrine was being built. You walked it to arrive at the shrine. That was its whole job."
    mc "And now?"
    hikari "Now you walk it to arrive at Louis Vuitton."

    "The shops are low and wide and almost silent. No prices in the windows. A doorman in white gloves stands outside a door that is already open."
    hikari "Every big house in the world wanted a building on this street. Tod's is by Toyo Ito: those branches on the front are concrete pretending to be a tree. Dior is glass and looks like it is not trying. Prada is bubbles."
    hikari "People come here to look at the buildings. Not only to buy. The buildings are the exhibition and the clothes are the gift shop."
    mc "That is a strange thing for a shop to be."
    hikari "It is a strange street. It is the same trick as hanami. Find a reason to walk slowly."

    "A woman passes us in a coat the colour of milk. A man passes her in a suit cut so close it looks drawn on. Neither of them looks at the other, and both of them know exactly who is behind them."
    mc "Everyone here is dressed for something."
    hikari "Everyone here is dressed for everyone else. That is different from being dressed for a photograph."
    mc "Is it?"
    hikari "Photographs go away. The person behind you at the crossing does not."

    menu:
        "Ask how a road for gods became a shopping street.":
            mc "So the gods used this road, and now it's this."
            hikari "The gods are not walking. They are being visited. The road stayed and got expensive."
            hikari "This country keeps the shape of a thing and changes what it is for. The torii is still at the end of the street. That is not nothing."
            mc "(Keep the shape. Change the use. I put it somewhere I can find it later.)"
            $ reward_attributes_once("omotesando_tour_shape", [("insight", "micro")], show="auto")
        "Ask if she has ever bought anything here.":
            mc "Have you ever bought anything on this street?"
            hikari "One thing. A coat. It was on sale and it was still the most I have ever spent on clothes."
            mc "Do you still have it?"
            hikari "Yes. I wear it when I want to feel like a person who belongs here."
            mc "You do belong here."
            hikari "You have been in this country three weeks. You do not know that yet."
            "She says it lightly. She does not slow down to say it."
            $ reward_attributes_once("omotesando_tour_coat", [("insight", "micro")], show="auto")
        "Look up at the buildings instead of the windows.":
            "I stop looking at the clothes and look at the buildings holding them."
            "The Tod's building has branches growing out of concrete. The Dior is a sheet of glass with the trees doubled in it. The Prada has bubbles pressed into its skin."
            hikari "You are looking at the right thing."
            mc "The clothes are inside. The buildings are outside."
            hikari "The buildings are the clothes. Somebody spent more on the box than the thing in the box."
            $ reward_attributes_once("omotesando_tour_buildings", [("grace", "micro")], show="auto")

    "The street climbs. The shops get quieter, then taller, then older, and then they stop."
    "The trees are not lining a road anymore. They are the road."

    scene bg_meijijingu_entrance with walk_fade
    "The torii comes out of the trees without warning: two columns and a beam, unpainted, the colour of old paper, taller than the shops behind us."
    mc "That is one piece of wood?"
    hikari "One of the largest wooden torii in the country. Cypress. No paint, because paint would make it a building and it is not a building."
    hikari "Before you go through, you bow. Once. Not deep. From the chest."
    mc "To who?"
    hikari "To whoever is on the other side. It is not a question you have to answer."

    "She bows. I bow. It feels like the wrong depth and then it feels fine."
    "Then she steps to the left of the path and waits for me to notice."
    hikari "Walk on the side. The middle belongs to the kami."
    mc "Is there a guard?"
    hikari "There is no guard. There is everybody."
    mc "Like the tarps at Ueno."
    hikari "Exactly like the tarps at Ueno. You are learning."

    "Inside the gate there is a stone basin under a wooden roof, with bamboo pipes above it and a row of ladles laid across the water."
    "People come and go in twos and threes. An old man in a cardigan does the whole thing in four seconds and is gone before I have worked out where to stand."
    hikari "Temizuya. The place you wash before you go further."
    hikari "The ladle is a hishaku. One scoop is enough. You do not refill it: the water is not for drinking and the basin is not a sink."
    mc "What is the order?"
    hikari "Right hand takes the ladle, pour over the left. Left hand takes it, pour over the right. Then pour a little into your left palm and rinse your mouth. Do not drink from the ladle."
    hikari "Then tip it so the water runs down the handle, and put it back."
    mc "Why the handle?"
    hikari "Because somebody else will hold it after you."

    menu:
        "Do it exactly as she says.":
            "I take a ladle. The water is colder than the air."
            "I pour over my left hand, then switch and pour over my right. I pour into my palm and rinse my mouth. I am about to tip the rest back into the basin when her hand closes on my wrist."
            hikari "Not back in. The basin is for everybody."
            mc "Sorry."
            hikari "Do not be sorry. Be careful. They are not the same thing."
            "I tip the water down the handle instead. It runs off the end and into the gravel. She lets go."
            $ reward_attributes_once("omotesando_tour_temizu", [("grace", "micro")], show="auto")
        "Ask why water.":
            mc "Why water? Of all the things to start with."
            hikari "Shinto has no founder and no book. There is nothing you have to believe before you are allowed to begin. So it begins with a wash."
            hikari "You clean your hands before you eat. You clean your hands before you ask somebody for something. It is the same idea, older."
            mc "So it is manners."
            hikari "Manners with a god in the room."
            $ reward_attributes_once("omotesando_tour_water", [("insight", "micro")], show="auto")
        "Watch the others first.":
            "I stand back and watch. A schoolgirl does it in five seconds. A businessman does it with his phone still in his other hand, then puts the phone away for the bow."
            hikari "You are doing the thing you did at Ueno."
            mc "Watching."
            hikari "Learning the shape of the room. This room has a shape too."
            mc "Four seconds for the old man."
            hikari "He has done it ten thousand times. That is what a tradition is. Not a feeling. A number."
            $ reward_attributes_once("omotesando_tour_watch", [("insight", "micro")], show="auto")

    scene bg_meijijingu_forest with walk_fade
    "The gravel starts."
    "Two steps in, the city is not quieter. It is gone. The traffic, the trains, the shops, the coat and the doorman: all of it stops at the same line."
    "The air is colder here. The trees are not in rows. They are in a crowd."

    mc "They left a forest in the middle of Tokyo."
    hikari "They didn't leave it. They planted it."
    mc "...Planted it."
    hikari "A hundred thousand trees. Donated: a village in Kyushu sent some, a school in Tohoku sent more, whatever people had. Volunteers carried them up this hill and put them in the ground."
    hikari "A forestry professor planned the whole thing. He chose the species so the forest would look after itself. He was designing a hundred years ahead."
    mc "He knew he would never see it."
    hikari "None of them would. That was the point."
    mc "That is an insane thing to do."
    hikari "It is the most Japanese thing in this city and it is not a temple."
    "We walk. The gravel is loud under us and the trees take the sound away again."
    mc "So they gave it to people they would never meet."
    hikari "...Yes."
    "She walks a little faster, so I do not see her face."

    "On both sides of the path, stacked in wooden frames like a wine rack, are barrels."
    "Sake barrels on one side, white and black with characters the size of my hand. On the other, dark wooden barrels with French names burned into them."
    mc "Offerings?"
    hikari "Offerings. The breweries send them. The names face out so the kami can read who gave what."
    mc "The god reads the labels."
    hikari "You give the thing you value. Rice wine was valuable. The name is part of the gift."
    mc "And the wine?"
    hikari "Burgundy. From France. Somebody decided the god here should have the good stuff."
    mc "Do the gods drink?"
    hikari "That is not the question. The question is whether you gave it."

    menu:
        "Ask where the trees came from.":
            mc "You said they were donated. From where?"
            hikari "Every prefecture. A country sent a tree. If you walked the whole forest you could find where everybody is from."
            mc "It is a map."
            hikari "It is a map that grew."
            $ reward_attributes_once("omotesando_tour_trees", [("insight", "micro")], show="auto")
        "Ask about the wine barrels.":
            mc "So a French winery sends wine to a Japanese god."
            hikari "Yes."
            mc "Does that work?"
            hikari "It is not a transaction. It is a letter. You do not need an answer to send one."
            mc "(She says that like she has sent a few.)"
            $ reward_attributes_once("omotesando_tour_wine", [("nerve", "micro")], show="auto")
        "Walk without talking.":
            "I stop answering. She stops explaining. We walk the rest of the path with nothing but gravel."
            "It takes a while before I notice she has matched my pace. She is not leading anymore."
            hikari "You are quiet."
            mc "You said the gravel is the point."
            hikari "I did say that."
            "She does not say anything else, and the walking is better for it."
            $ reward_attributes_once("omotesando_tour_quiet", [("grace", "micro")], show="auto")

    "Ahead, a line of people comes around the bend."
    "A bride in white, a white hood over her hair. Two priests. A shrine maiden holding a parasol. The bride's mother carries the hem of the dress off the gravel with both hands."
    "Nobody speaks. The whole procession moves at the speed of the slowest person in it."
    hikari "Shinzenshiki. A Shinto wedding."
    mc "In the middle of the forest."
    hikari "Where else? The kami is here."
    mc "Is there always one?"
    hikari "Every time I come. Somebody in this city is always getting married."
    "The bride passes close enough that I can see she is concentrating on not stepping on her own dress. Hikari bows slightly. The bride does not see her."
    mc "(A hundred thousand trees, and the thing I remember is a woman trying not to trip.)"

    scene bg_meijijingu_temple with walk_fade
    "The path opens into a courtyard and the sound comes back: not traffic. People. A school group in matching hats. A guide with a little flag. A queue at the offering box."
    hikari "Stop here."
    mc "Why?"
    hikari "Hat off."
    "I take my hat off."
    hikari "No photographs from here. People are praying and it is not a show. No talking above a murmur. And do not stand in the middle of the path."
    mc "There is a lot of etiquette."
    hikari "There is a lot of people. The etiquette is how they all fit."
    mc "Aren't we going in?"
    hikari "No. The inner building is not for us. We stand at the front and say it from here."
    mc "Then why is the door open?"
    hikari "Because somebody has to go in. It is not going to be you."
    hikari "Did you bring the coin?"
    mc "I brought it. I still do not know why."
    hikari "Go-en. Five yen. It sounds like goen, a connection. People use it when they want one."
    mc "A connection to what?"
    hikari "To whoever. That is the honest answer."

    "We reach the offering box. She steps up, drops her coin without looking at where it lands, bows twice, claps twice, and bows once."
    "It takes maybe ten seconds. She does not close her eyes. She does not look like she is asking for anything."
    "Then she steps back and looks at me."
    hikari "Your turn."
    "I drop my coin. It rattles. I bow twice, too fast. I clap twice, and the first clap is too quiet. I bow once."
    "She does not correct me. She waits until I am finished and then nods, once."
    hikari "You did it properly."
    mc "I clapped too quietly."
    hikari "The kami is not marking you. Do it again if you want to do it better."
    mc "I copied you."
    hikari "That is how it is done. Nobody is born knowing. I copied my mother."

    hikari "You know what you did well today?"
    mc "I dropped a coin."
    hikari "You did everything I told you and you never once asked whether you had to."
    hikari "Most people ask whether they have to. You just did it, and then you asked what it meant."
    mc "Is that the right order?"
    hikari "It is the only order that works."
    "She says it to the courtyard, not to me. Then she looks at me and looks away."

    menu:
        "Ask what she said when she bowed.":
            mc "What did you say? When you bowed."
            hikari "You are not supposed to say."
            mc "Is that a rule?"
            hikari "No. It is just mine."
            "She is quiet for a moment."
            hikari "I said thank you. That much I will tell you."
            mc "For what?"
            hikari "For the afternoon."
            "She says it in the same voice she has used all day, and it lands heavier than the words."
            $ reward_attributes_once("omotesando_tour_thanks", [("insight", "micro")], show="auto")
        "Ask if she believes in it.":
            mc "Do you believe any of this? The kami, the coins."
            hikari "I don't know what I believe."
            hikari "I know it is better to do it carefully than badly. I know I feel better after. That is not nothing."
            mc "That is not an answer."
            hikari "It is the only honest one I have. Ask me again when I am older."
            $ reward_attributes_once("omotesando_tour_believe", [("insight", "micro")], show="auto")
        "Do it a second time, slower.":
            "I put another coin in. I do not know why. I bow twice, clap twice, bow once, and this time it is one thing instead of four."
            "It takes longer than I expected. When I open my eyes she is watching me with an expression I have not seen on her."
            mc "What?"
            hikari "Nothing. You looked like you meant it."
            mc "I don't know if I did."
            hikari "That is allowed. That is most of the people here."
            $ reward_attributes_once("omotesando_tour_second", [("grace", "micro")], show="auto")

    "We step back to let a family through. The father holds the little one up so she can reach the bell rope."
    mc "Do you come here alone?"
    hikari "Sometimes."
    mc "To pray?"
    hikari "To say something to somebody who isn't there."
    "She says it in the same voice she has used all afternoon. No weight on it. No pause."
    mc "Who?"
    hikari "...Come on. The light is going."
    "She is already walking."
    mc "(I do not ask again. I am learning when not to.)"

    "The light is going when we come back down. The shops have turned their lights on, and the zelkova leaves are lit from underneath."
    "She stops at a place with a small sign and no English on it. Two tables outside, one inside, and a barista who looks like he has known her for years."
    hikari "Two hot coffees. And the cake. Two forks."
    "The barista says something. She answers. I catch one word and lose the rest."
    hikari "He asked if you want it hot or iced."
    mc "What did you say?"
    hikari "Hot. It is cold and you are tired. I made a decision for you. Tell me if I was wrong."
    mc "You weren't."

    "The coffee comes in thick cups. The cake is small and costs more than my lunch. We sit outside because she wants to watch the street."
    mc "Let me pay for mine."
    hikari "Next time."
    mc "That's not an answer."
    hikari "It is an answer. It is just not the one you asked for. Drink your coffee."

    menu:
        "Ask why she brought me here.":
            mc "Why this place? Out of all of them."
            hikari "Because you have been treating this country like a test you are failing."
            mc "I have not."
            hikari "You apologise to doors."
            mc "...Do I?"
            hikari "You did it at the temizuya. The door had nothing to do with it."
            hikari "I wanted you to spend an afternoon in a place where the only thing you can do wrong is be careless."
            $ reward_attributes_once("omotesando_tour_why", [("grace", "micro")], show="auto")
        "Ask about the coin.":
            mc "The five-yen coin. Do you always carry one?"
            hikari "There is one in my wallet. It has been there so long the hole has worn smooth."
            mc "You never spend it."
            hikari "You don't spend a connection."
            mc "Have you ever used one? Ever?"
            hikari "Once."
            mc "Did it work?"
            hikari "I am still here."
            $ reward_attributes_once("omotesando_tour_coin", [("insight", "micro")], show="auto")
        "Say thank you properly.":
            mc "ありがとうございました。"
            "The full form. The one you use at a counter, to a stranger, when you mean it."
            hikari "...You said that right."
            mc "I practiced."
            hikari "On who?"
            mc "The mirror."
            hikari "Of course you did."
            "She laughs and looks away, which is what she does instead of saying something she means."
            $ reward_attributes_once("omotesando_tour_thankyou", [("nerve", "micro")], show="auto")

    "We finish the coffee. The street is loud again in the good way: people, bicycles, a bus pulling away."
    hikari "The shrine closes at sunset."
    mc "We just came from there."
    hikari "I know. That is why we are here."
    mc "It doesn't stay open for anybody?"
    hikari "Not even for the kami. It closes and opens every day and nobody argues with it."
    mc "(A place that closes on time. I did not know I needed to see one.)"

    $ unlock_hikari_tour_destination("omotesando")
    $ phone_map_visit("omotesando")
    $ renpy.notify("Omotesando / Meiji Shrine is now on your map.")
    mc "(I can come back here on my own now. She showed me the shape of it.)"
    hikari "Next time, go in without me. Stand where I stood and do it badly."
    mc "You are not coming?"
    hikari "I have shown you. That was the point."
    mc "(She says it lightly. It does not land lightly.)"
    hikari "And keep the coin."
    $ reward_attributes_once("hikari_tour_omotesando_complete", [("insight", "tiny")], show="auto")

    scene bg_train_interior with walk_fade
    "The train home is warm and half full. Hikari takes the window seat and falls asleep against the glass with her coat folded under her head."
    mc "(She told me a forest was a gift from people who would never see it. I think she has been giving me one all along.)"

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    hikari "We're home."
    mc "We're home."
    hikari "You're welcome."
    mc "I didn't say thank you."
    hikari "You did. At the shrine. In the right words."
    "She goes inside before I can argue."
    return


## --- STANDALONE TEST LABEL ----------------------------------------------------
##
## Open the console with Shift+O and type one of:
##   jump test_hikari_tour          - Yokohama Chinatown
##   jump test_hikari_tour_harajuku - Harajuku, Takeshita Street
##   jump test_hikari_tour_karaoke  - Kuru Fuku Neko (karaoke)
##   jump test_hikari_tour_ueno     - Ueno Park
##   jump test_hikari_tour_shimokitazawa - Shimokitazawa
##   jump test_hikari_tour_omotesando - Omotesando / Meiji Shrine
##
## These play the whole tour without having to reach a hub day first. The picker
## is forced by marking the OTHER written tours as already unlocked, so the one
## under test is always the one offered.

label test_hikari_tour:
    scene black with Dissolve(0.8)
    "TEST SEQUENCE: MESSAGE HIKARI // YOKOHAMA CHINATOWN"
    $ force_hikari_tour_spot("yokohama")
    call hikari_tour from _call_test_hikari_tour
    "Test complete. Yokohama is unlocked for solo visits."
    return


label test_hikari_tour_harajuku:
    scene black with Dissolve(0.8)
    "TEST SEQUENCE: MESSAGE HIKARI // HARAJUKU, TAKESHITA STREET"
    $ force_hikari_tour_spot("harajuku")
    call hikari_tour from _call_test_hikari_tour_harajuku
    "Test complete. Harajuku is unlocked for solo visits."
    return


label test_hikari_tour_karaoke:
    scene black with Dissolve(0.8)
    "TEST SEQUENCE: MESSAGE HIKARI // KURU FUKU NEKO"
    $ force_hikari_tour_spot("karaoke")
    call hikari_tour from _call_test_hikari_tour_karaoke
    "Test complete. Kuru Fuku Neko is unlocked for solo visits."
    return


label test_hikari_tour_ueno:
    scene black with Dissolve(0.8)
    "TEST SEQUENCE: MESSAGE HIKARI // UENO PARK"
    $ force_hikari_tour_spot("ueno")
    call hikari_tour from _call_test_hikari_tour_ueno
    "Test complete. Ueno Park is unlocked for solo visits."
    return


label test_hikari_tour_shimokitazawa:
    scene black with Dissolve(0.8)
    "TEST SEQUENCE: MESSAGE HIKARI // SHIMOKITAZAWA"
    $ force_hikari_tour_spot("shimokitazawa")
    call hikari_tour from _call_test_hikari_tour_shimokitazawa
    "Test complete. Shimokitazawa is unlocked for solo visits."
    return


label test_hikari_tour_omotesando:
    scene black with Dissolve(0.8)
    "TEST SEQUENCE: MESSAGE HIKARI // OMOTESANDO / MEIJI SHRINE"
    $ force_hikari_tour_spot("omotesando")
    call hikari_tour from _call_test_hikari_tour_omotesando
    "Test complete. Omotesando / Meiji Shrine is unlocked for solo visits."
    return
