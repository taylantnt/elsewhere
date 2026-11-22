################################################################################
## SPECIAL DAY 49: THE SEASON OF WET FLOWERS
## Tuesday, May 26, 2026. The rainy season arrives for good, the house turns into
## a small indoor weather of damp laundry, and Hikari takes him north, before the
## queue finds the garden.
##
## Hikari's lesson today is told to a flower: a person is mostly the ground they
## were planted in.
################################################################################

label special_day_49_hydrangea:
    $ set_story_day(49)
    call day_transition from _call_day_transition_32
    $ last_afternoon_place = None
    $ last_afternoon_hikari_tour = False

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Tuesday. The rainy season arrives the way a guest arrives who has told you he is coming and still manages to surprise you."
    "It has rained before, this past week, in a way that could be argued with. This is not that. This is a rain that has decided to stay. A rain with a lease."
    "The window is grey. The sound on the roof is not a sound anymore. It is a weather."

    mc "(Six weeks I have been here and the sky has been polite about it. Today it stopped being polite.)"

    "My phone buzzes."

    $ run_chat("hikari", [
        {"them": "The rain is staying. It is the rainy season. It does not leave now until June.", "options": [
            {"label": "\"Is that bad?\"",
             "send": "Is that bad?",
             "them": ["It is not good or bad. It is the season.", "Wear the shoes that are already ruined.", "Bring the umbrella with the wooden handle."]},
            {"label": "\"You said it would rain for a month.\"",
             "send": "You said it would rain for a month.",
             "them": ["I said it before it happened. Now it has happened.", "Wear the coat with the hood. We are going somewhere wet on purpose."]},
        ]},
    ])
    mc "(Somewhere wet on purpose. In this house a sentence like that is not a riddle. It is an itinerary.)"

    call murakami_daily_ping from _call_murakami_daily_ping_19

    scene bg_kitchen with walk_fade

    "Downstairs the whole kitchen smells of damp cloth. Mother has the laundry on a folding rack in the middle of the room, which is the only dry place in the house, and it has turned the room into a small forest of damp sleeves."
    mother "Do not touch the washing. You will knock it down and we will both be sorry and only one of us will be sorry out loud."
    mc "It is raining in the kitchen."
    mother "It is raining everywhere. In this house it is raining on the shirts. Sit and eat."
    father "It comes every year. People forget, and then it comes, and they act as if it were a surprise. It is not a surprise. It is a season."
    mc "(He says season the way other men say weather. As if the year had rooms in it, and this is simply the room we are in now.)"

    "I eat standing at the counter, because there is nowhere to sit the laundry has not claimed."

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/room_day.mp3" fadein 2.0

    "Hikari is at the gate under a black umbrella I have never seen, wearing the coat with the hood, waiting like a person who has been standing in the rain since before I woke."
    hikari "You brought the small umbrella."
    mc "It is an umbrella."
    hikari "It is a shoebox on a stick. By the time we come back you will be wet to the knee and you will not say so."
    mc "Where are we going?"
    hikari "Where the rain is the point."

    scene bg_station with walk_fade
    scene bg_platform with walk_fade

    "The platform in the rain is a different country. Everyone is roofed. The umbrellas fold and drip and stand in a line like a hedge. Nobody hurries, because hurrying in the rain only means you arrive wet and early."
    mc "(I have spent my whole life treating rain as an interruption. This platform does not. This platform treats it as a Tuesday.)"

    scene bg_train_interior with walk_fade

    "The train windows are fogged and the world outside is a grey watercolor that keeps moving. Hikari draws a line in the glass with one finger and looks through it at nothing."
    hikari "There is a temple north of here. Small. On a hill. In June people line up for three hours to stand in its garden."
    mc "And in May?"
    hikari "In May the garden is already doing it and there is no line and the rain is the whole reason. We go in May."

    scene bg_ajisai_temple with Fade(0.0, 0.0, 1.5)
    stop music fadeout 1.5
    play music "audio/Music/(Hanabi night) lanterns_at_dusk.mp3" fadein 2.0

    "It is exactly as she said. A gate, a hill, a set of wet stone steps that climb between walls of green. And then the garden opens, and the garden is blue."

    "Hydrangea. Ajisai. I have seen them before, in shops, in pots, tidy and small. I have never seen them like this. They are everywhere. Banks of them along the path, taller than me, heads the size of two hands, and every head is a hundred small four-petalled flowers packed tight. The color is not one color. It is blue and violet and pale and pink and green, all on the same bush, moving as the rain moves them."

    mc "(I thought a flower was one color. This one cannot decide. It grows the color it is given, and what it is given is the ground it stands in.)"

    hikari "The soil makes the color. Acid soil, blue. Sweet soil, pink. Same plant. Different dirt underneath."
    mc "So the flower does not choose."
    hikari "The flower is what the ground says it is. People like to think the flower chooses. The flower is honest. It only tells you what it is standing in."

    mc "(She says it about a flower. She is not only saying it about a flower. Neither of us says so.)"

    "We walk the path slowly. The rain keeps falling and the umbrellas of a few other people bob between the flower-heads like dark lanterns. An old woman kneels at one bush with a small camera and waits a long time for one drop to fall from one petal."

    hikari "Look up."
    "Hanging from the eaves of the little hall at the top of the steps, strung on a wet line, there are a dozen small white dolls folded out of paper. A round head, a little cloth body, a face drawn in ink."
    mc "What are they?"
    hikari "Teru teru bozu. The sunshine monk. You hang one to ask for good weather. Children make them the night before a school trip and hang them in the window."
    mc "A paper doll for the weather."
    hikari "It is not superstition, not really. It is a way to do something with your hands while you wait for a thing you cannot control. Every country has one of those. Ours is a monk made of tissue."

    menu:
        "Ask about the rhyme that goes with it.":
            mc "Is there a song? For the doll?"
            hikari "There is. Teru teru bozu, teru bozu. Please make tomorrow a sunny day."
            mc "And if it rains?"
            hikari "Then there is a second verse, and the second verse is where they cut off your head."
            mc "What?"
            hikari "It is a children's song. The children find it funny. It is the same joke as the doll. You ask very sweetly for the sun, and if it does not come, you threaten the small paper man, and then everyone laughs and goes to school in the rain anyway."
            mc "(A whole country's relationship with the weather, in one rhyme with two endings. Ask nicely, threaten the doll, then accept the rain and go to school in it.)"
            $ log_memory("hikari", "taught me the teru teru bozu rhyme, a sweet first verse and a second verse where they cut off the doll's head, which the children laugh at")
            $ reward_attributes_once("day49_rhyme", [("insight", "micro")], show="auto")
        "Make one of your own and hang it.":
            "There is a small basket by the hall with squares of white paper and a pen on a string. I take one and fold it the way Hikari shows me, crumple the head into a ball, tie the neck with a thread, draw two eyes and a mouth that comes out crooked."
            "I hang it with the others. It looks nothing like theirs. It looks like a paper ghost that has given up."
            hikari "You did it wrong."
            mc "I know."
            hikari "Good. The shops sell perfect ones. Nobody hangs the perfect ones. People hang the ones they made badly at the kitchen table."
            mc "(Mine is on the line with eleven careful ones. It is the only one that is obviously mine, and that is somehow the point of it.)"
            $ log_memory("hikari", "said the teru teru bozu people hang are the crooked ones, the ones made badly at a kitchen table")
            $ reward_attributes_once("day49_doll", [("grace", "micro")], show="auto")
        "Stand and watch the old woman with the camera.":
            "I stop beside the old woman at the bush. She has not taken a photograph yet. She is waiting for one drop, on one petal, at the exact second it lets go."
            hikari "She has been there since before we came. She will be there after we go."
            mc "For one picture?"
            hikari "For one picture. Some people spend an afternoon on one drop of water. That is not a waste. That is the whole reason to have an afternoon."
            mc "(I have an afternoon most days and I spend it the way you spend a waiting room. This woman spends it the way you spend a gift.)"
            $ log_memory("hikari", "said the old woman waiting an hour for one drop of water was not wasting the afternoon but using it")
            $ reward_attributes_once("day49_watch", [("grace", "micro")], show="auto")

    "The rain does not stop. It was never going to. That was the arrangement."

    scene bg_ajisai_temple with Dissolve(1.0)

    "On the way down, at the foot of the steps, there is a tea stand under a plastic awning, the kind with three stools and a woman who has been making the same matcha for decades. We sit. The stools are wet and we sit anyway. The tea is hot and bitter and faintly green, and it is the best thing I have had all week, because cold hands make an honest judge of tea."

    mc "You knew it would be like this."
    hikari "I knew. I have been watching the buds for two weeks. You have to catch it before the line finds it. After June it is not a garden anymore. It is a queue."
    mc "So you stole a day."
    hikari "I stole a day. From the rain, which owed me one."

    scene bg_train_interior with walk_fade
    play music "audio/Music/train.mp3" fadein 2.0

    "We ride home with the wet-umbrella smell and the fogged windows and the whole car dozing inside its coats. Hikari is quiet, which by now I understand is not a mood. It is her putting something away."

    scene bg_home_exterior_night with walk_fade
    $ night_street()

    "Home at dark, and the laundry rack is still up in the kitchen, a small indoor weather of its own."

    scene bg_kitchen_night with walk_fade
    $ room_ambient(True)

    mother "You went out in it. Both of you. On purpose."
    hikari "The hydrangeas are at their best in the rain."
    mother "The hydrangeas are at their best in the rain. Listen to her. You went to look at wet flowers and came home soaked and you are going to do it again next year."
    hikari "I am going to do it again next week."
    mother "That is what I said."
    mc "(Mother is not scolding. There is a name for the thing she is doing, and the name is remembering the daughter she raised.)"

    father "The ajisai were my mother's favorite."
    "Everyone looks up."
    father "She used to say a flower that changes its color with the soil is the only honest flower, because it never pretends the ground is better than it is."
    hikari "Your mother said that."
    father "My mother said many things. That is the one that survived."
    mc "(In this house the dead arrive in one line, at dinner, between the rice and the tea, and are gone again before anyone can ask. Father's mother is now a woman who loved hydrangeas. That is all I will ever know of her. I wonder if that is all anyone keeps.)"

    scene bg_room_night with stair_fade
    $ room_ambient(True)

    "Upstairs my coat is dripping on the back of the door and my shoes are ruined exactly as she promised. On the desk, still faintly wet, is one hydrangea head I did not notice her put in my bag. Blue at the edge of every petal and green in the middle, the color doing what the color does."

    "I write one line about the garden and one line about the color coming out of the ground. Then I sit for a while and do not write a third, because the rain is doing more writing than I am."
    "I press the flower flat under the first page of the notebook. The wet of it makes the ink run a little, and I decide I do not mind."

    $ night_desk_line = "the hydrangea pressed under the first page"

    call night_open from _call_night_open_26

    "Hikari comes in with the tea and sits on the floor against the bed. The rain is on the roof. It has not stopped and it is not going to."
    hikari "I am not staying."
    mc "You never stay."
    hikari "The rain is loud tonight. It is a good night for it to be loud."

    menu:
        "[tag_insight] Rank 3: Ask what her grandmother would have made of this garden." if has_attribute("insight", 3):
            mc "Your grandmother. What would she have made of this garden?"
            hikari "She would have said it was too blue and then stood in it for an hour."
            mc "That sounds like a compliment."
            hikari "It was. She did not give them any other way."
            mc "(I try to picture a woman with sweets in her sleeve, standing in the rain, saying too blue.)"
            $ log_memory("hikari", "said her grandmother would have called the garden too blue and then stood in it for an hour")
            $ reward_attributes_once("day49_night_garden", [("insight", "micro")], show="auto")
        "Ask her what her father's mother was like.":
            mc "Your father's mother. The one who liked the flowers."
            hikari "I barely remember her. She died when I was small. I remember a room that smelled of citrus and old paper, and I remember she always had sweets in her sleeve."
            mc "In her sleeve?"
            hikari "Always. She would reach into her sleeve and a candy would come out, and it was never a surprise, and it was always a little bit of a magic anyway."
            mc "That is all you kept of her."
            hikari "That is all anyone keeps. One line. One sleeve. The rest goes."
            mc "(She says it without grief. It is not a sad thing to her. It is just the arithmetic of what a person leaves behind.)"
            $ log_memory("hikari", "kept only one line of her grandmother: a sleeve that always had sweets in it")
            $ reward_attributes_once("day49_night_grandmother", [("insight", "micro")], show="auto")
        "Tell her the thing about the flower and the ground.":
            mc "What you said. The flower tells you what it is standing in."
            hikari "Mm."
            mc "You were not only talking about flowers."
            hikari "No. I was not."
            mc "Then say the other thing."
            hikari "I am not sure I should. You have a face like a person collecting evidence."
            mc "(She looks at me for a while. Then she decides, the way she decides things, all at once and completely.)"
            hikari "I think a person is mostly what they were planted in. You have been planted in this house for seven weeks. You are already a different color. You can feel it. I can see it."
            mc "(She is right, and it is not comfortable, and I do not want her to take it back.)"
            $ log_memory("hikari", "said I was already a different color from seven weeks of being planted in this house")
            $ reward_attributes_once("day49_night_ground", [("grace", "micro")], show="auto")
        "Say nothing. Listen to the rain.":
            "I do not ask her anything. I let the rain take over the conversation, which is the only conversation rain is good at."
            "We sit the way two people sit when the weather is doing the talking. The roof. The gutter. The small ticking of a leaf against the window. Hikari finishes her tea and does not get up, and does not get up, and then gets up."
            mc "(There are evenings I will forget. This is not one of them, and I do not know why, because nothing happened in it. Maybe that is exactly why.)"
            $ log_memory("hikari", "sat through the rain with me and let the weather do the talking")
            $ reward_attributes_once("day49_night_quiet", [("nerve", "micro")], show="auto")

    call night_close from _call_night_close_26

    "She takes her cup and leaves the door open a hand's width. The rain fills the gap she leaves behind. Downstairs the house does its six sounds, and tonight there is a seventh, which is the gutter, and I decide to count it as a guest."
    "Somewhere north of here the garden is still blue and still wet and still unqueued, and it will be for a few more weeks, and then it will not be. I am a person who saw it at the right time."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
