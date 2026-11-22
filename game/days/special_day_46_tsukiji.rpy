################################################################################
## SPECIAL DAY 46: THE MARKET BEFORE DAWN
## Saturday, May 23, 2026. He wakes while the house is still dark and takes the
## first train to the outer market, because there are places in this city that
## only exist in the hours before breakfast.
##
## Solo day. No glitch. The seed for the fireflies night is planted quietly here,
## in the line the fishmonger does not say twice.
################################################################################

label special_day_46_tsukiji:
    $ set_story_day(46)
    call day_transition from _call_day_transition_29
    $ last_afternoon_place = None
    $ last_afternoon_hikari_tour = False

    $ flush_pending_messages()

    scene bg_room_night with Dissolve(1.5)
    $ room_ambient(True)

    "The alarm goes off at four twenty and I am already awake, which is the first thing about the day that does not surprise me."
    "Saturday. No bell, no gate, no reason to be up before the house. I get dressed in the dark like a man trying not to be heard leaving."
    mc "(There is a place in this city that opens at four and closes at noon. I read one page about it on the plane and skipped the rest. I have been thinking about the page ever since.)"

    "Downstairs the kitchen is cold. On the fridge, held by a magnet shaped like a plum, there is a note in Mother's handwriting."
    "It says: If you are going where I think you are going, bring back tamagoyaki. The good kind. Do not buy the cheap kind."
    mc "(She heard the alarm. She hears everything. She hears the fridge open from the next room, the way Hikari hears me breathe through a wall.)"

    "I put a note of my own under hers. Then I put on my shoes, turned around the way the house does it, and close the door with two hands so it will not click."

    scene bg_home_exterior_night with walk_fade
    $ night_street()

    "The street is blue. Not dark, blue. The hour before the hour."
    "The vending machine hums its one low note at nobody. A delivery truck idles at the corner, then moves off, and the street goes back to being a street no one has used yet."
    mc "(I know this city in the middle of the day. I do not know it at four thirty. It makes a different smell. It smells like a place no one has named yet.)"

    scene bg_station with walk_fade

    "The station at this hour is not a station. It is a lit box with one man inside it."
    "The shutters hang half down over the ticket machines. The departure board is black except for the first train, four minutes away, and on time."

    "My phone buzzes."

    $ run_chat("hikari", [
        {"them": "The door clicked twice. You never do that.", "options": [
            {"label": "\"I was trying to be quiet.\"",
             "send": "I was trying to be quiet.",
             "them": ["Quiet doors click once.", "Yours clicked twice.", "Where are you going before the sun."]},
            {"label": "\"Go back to sleep. It is four thirty.\"",
             "send": "Go back to sleep. It is four thirty.",
             "them": ["I am awake. I am always awake at four thirty.", "You just have never seen it."]},
        ]},
    ])
    mc "(She runs in the mornings, before the house, before the light. I have lived with her for six weeks and I have never once watched her leave. She is simply not there at breakfast, and then she is.)"

    scene bg_platform with walk_fade

    "The platform holds maybe ten people. They are all men, all older, all in the same white shirtsleeves in the same blue light."
    "Nobody looks at anybody. We stand at the yellow line like statues that agreed on a place to stand."
    "One of them, without turning his head, says the name of a station. It is not a question. Another one answers with a different station. That is the whole conversation, and it is finished."
    mc "(They are going to work. That is what this train is for. I am the only person on this platform who is not on his way to a job.)"

    scene bg_train_interior with walk_fade

    "The car is warm. The light is the color of skim milk. I take the corner seat and watch the city pass in pieces: a lit window, a dark window, a river, a shrine, another river."
    "The city is doing something in front of me that it will never do again. It is being off."

    scene bg_tsukiji_dawn with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The market does not wake up. It has been awake. The trucks came at two and the fish came at three and by the time I walk in, at five, the day here is already halfway old."
    "It is not a street and it is not a building. Narrow lanes with roofs over them, both sides lined with stalls, and over all of it a light that is half lamp and half morning."

    "The floor is wet and clean. Somebody is always hosing it. A man in rubber boots drives past me on a little flatbed cart and does not slow, and does not need to, because everyone moves before he reaches them. They just know the sound the cart makes."

    mc "(The ground is wet and it has not rained. It is wet because the fish are wet and the ice is wet and everything in this place is trying to stay cold.)"
    "Then the smell arrives all at once. It is not a bad smell. It is the smell of cold and salt and something sweet underneath, the way a finished kitchen smells of food and also of work."

    "I stop at the first thing I recognize. A copper pan the size of a small window, and a man rolling eggs in it with chopsticks, layer over layer, until the thing in the pan is a block."
    "He sells them on a stick. A few hundred yen. I buy one and eat it standing in the lane like a person who has somewhere to be."
    mc "(It is sweet. It is not the tamagoyaki from the combini. It is warm, and it is folded by a hand, and the hand has been doing only this for a very long time.)"

    scene bg_tsukiji_stalls with walk_fade

    "Two lanes over there is a shop with no fish in it at all. A block of dried bonito the size of a loaf, and a machine that shaves it, and the shavings come off the block in curls that look like wood, thin enough to see through."
    "The man at the machine does not look up. He feeds the block in from the top and the flakes fall into a box and he scoops them into a bag and hands the bag over and takes the money without once breaking the rhythm."
    mc "(This is what the soup is. I have eaten this every night for six weeks. I have never seen where it comes from.)"

    "Further in, past the ice and the glass and the rows of red and silver, I find the knives."
    "They are laid out on a cloth like something religious. Long ones. Short ones. Ones with a single bevel and ones with two. An old woman in an apron stands behind them with her hands folded and lets me look."

    "She asks me, without asking, what I cook. I tell her rice and miso, which is true. She looks at me the way a doctor looks at a small cut, and then she picks up the smallest knife on the cloth, the plainest one, and holds it out."
    "It is not the expensive one. It is the one you give to somebody who is learning."
    "I buy it. She wraps it in paper and ties the paper with string and tells me, in the careful way people here tell you things, to dry it after I use it."

    "An older man in an apron watches me put the paper-wrapped knife in my bag. He tells me I hold it like a cook."
    mc "(It is either a compliment or a correction. I decide it is a compliment, because I want it to be, and because I am standing in a market at five in the morning with a knife I do not know how to use.)"

    menu:
        "Bring back the tamagoyaki for Mother.":
            "On the way out I stop at the copper pan again and buy a whole roll, wrapped in wax paper, still warm."
            mc "(She asked for the good kind. This is the good kind. It is also the only kind I have ever seen made by a person.)"
            $ day46_gift = "tamagoyaki"
            $ log_memory("mother", "asked for the good tamagoyaki and got the good tamagoyaki")
            $ reward_attributes_once("day46_gift_tamagoyaki", [("grace", "micro")], show="auto")
        "Keep the knife. A thing for myself.":
            "I keep the knife in my bag and do not buy anything else."
            mc "(It is the first thing I have bought in this country that is not food and not school and not for somebody else. It is mine, and it is small, and it is sharp.)"
            $ day46_gift = "knife"
            $ reward_attributes_once("day46_gift_knife", [("nerve", "micro")], show="auto")
        "Bring back the dashi for the kitchen.":
            "I go back to the shaving machine and buy a bag of the flakes, and a packet of kombu from the stall beside it."
            mc "(The soup has a taste. I want to know how the taste is made. That is all.)"
            $ day46_gift = "dashi"
            $ reward_attributes_once("day46_gift_dashi", [("insight", "micro")], show="auto")

    scene bg_station with walk_fade
    stop music fadeout 2.0

    "By eight the market is thinning. The workers are finished and the tourists have not arrived, and for a few minutes the lanes belong to nobody, which is the only time of day they do."
    "I take the train back with the morning crowd. I am going the wrong way in a full car, home while the city goes out."

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/room_day.mp3" fadein 1.5

    "The house at nine is warm and awake. Shoes by the door. The kettle. Hikari at the table with her notes, hair still slightly wet from the river."

    hikari "You are back."
    mc "I am back."
    hikari "You left before the house. I heard the door twice."
    mc "I know. You told me."
    hikari "I told you what, exactly."
    mc "That quiet doors click once."
    "She looks at me for a second, the way she checks a sum."
    hikari "You went to the market."
    mc "How do you know?"
    hikari "You smell like the sea and your hands are cold. Only one place in this city does both."
    mc "(She says it as a fact she has already filed. I do not ask how she knows what the market smells like. I decide I do not need to.)"
    hikari "Did you eat?"
    mc "I ate standing up."
    hikari "Good. Nobody sits at the market. Sitting is for people who are not sure they are allowed to be there."
    mc "(She says it lightly. It is exactly true.)"

    "I sleep through the middle of the day, which I never do, and wake at three with the light in a different place on the wall."

    scene bg_kitchen_night with walk_fade
    $ room_ambient(True)

    "Dinner is ordinary and warm. Father with the paper folded small. Mother ladling rice. Hikari telling a story about a cat she met by the river that no one believes."

    if day46_gift == "tamagoyaki":
        "I put the wax paper on the table and unwrap it. The roll is cold now but it is still the good kind."
        mother "You went."
        mc "I went."
        mother "This early? For eggs."
        mc "For eggs."
        "She cuts it into four and puts a slice on every plate, including her own, and does not say thank you, which is the thank you."
        father "It is sweet."
        mother "That is how it is supposed to be. You eat meat all day. You would not know sweet if it sat on your plate."
        father "The meat is good too."
        mother "The meat is good too."
        mc "(That was an argument. It lasted two lines and it was over. That is the whole marriage, in two lines about eggs.)"
    elif day46_gift == "knife":
        "I do not bring the knife out at the table. I wash it and dry it, the way the woman in the apron told me, and put it on the shelf in my room."
        mc "(It is small and plain and it belongs to me. There is nothing in this house that does that.)"
    else:
        "I put the bag of dashi flakes on the counter. Mother opens it and smells it and looks at me."
        mother "Do you know what this is for?"
        mc "The soup."
        mother "The soup."
        mc "I watched a man make it. A block and a machine. He did not look up once."
        mother "He has been looking down for thirty years. Of course he does not look up."
        mc "(She knows the market. She has never mentioned it. I file that next to the rest of what this house does not say.)"

    hikari "You are quiet tonight."
    mc "I am tired. It is a tiredness I earned."
    hikari "That is the good kind. It is different from the kind you get from being awake too long at nothing."
    mc "(She is right about that too.)"

    if day46_gift == "tamagoyaki":
        "After dinner Hikari takes the last slice off the paper and eats it in two bites, standing at the counter, watching the window."
        hikari "You got up at four for this."
        mc "I did."
        hikari "Good. Now you know what a morning is worth."
        $ add_affection("sister", 1)

    scene bg_room_night with stair_fade
    $ room_ambient(True)

    "Upstairs the window is open a hand's width. The city is doing its evening sounds, the train and the scooter and the far-off train again."
    "The notebook is open on the desk. I write one line about the market and one about the knife and one about the man who shaved the fish into paper."
    "Then I stop, because there is a thing I did not write down this morning and I want to write it now, while it is still only a thing I noticed and not yet a thing that happened."

    $ night_desk_line = "the bag from the market and the pen"

    call night_open from _call_night_open_23

    "Hikari comes in with two cups and sits on the floor with her back against the bed, the way she always does."
    hikari "I am not staying."
    mc "You never stay."
    hikari "I stay exactly long enough. That is different."

    menu:
        "Tell her about the man at the cart.":
            mc "At the market, the carts. The men driving them never slow down."
            hikari "Why would they."
            mc "There is no reason. Everyone just knows to move."
            hikari "That is the whole market. It is built on a sound everyone learned before they were told to."
            mc "(I did not learn it. I moved anyway. I do not remember deciding to.)"
            hikari "You moved before you knew. That is what a place does to you once you belong to it a little."
            $ log_memory("hikari", "said I moved out of the cart's way before I knew to, because a place starts to own you")
            $ reward_attributes_once("day46_night_cart", [("insight", "micro")], show="auto")
        "Tell her what the woman said about the knife.":
            mc "The knife woman told me to dry it after I use it."
            hikari "She told you the most important thing."
            mc "It seemed small."
            hikari "It is small. That is why she told you. People save the small things for the people they think will still have the knife in ten years."
            mc "(Ten years. I had not thought past this week.)"
            $ log_memory("hikari", "said the knife woman warned me to dry it because she thought I would still have it in ten years")
            $ reward_attributes_once("day46_night_knife", [("grace", "micro")], show="auto")
        "Say nothing. Let her sit.":
            "I do not tell her anything. She does not ask. She drinks her tea slowly and looks at the window and the city does its sounds."
            "After a while she says, without me saying anything first, that the market is one of the few places in this city that is older than the city around it."
            mc "(She does not need to be told a thing to arrive at it. She just sits next to me until she gets there.)"
            $ log_memory("hikari", "sat with me in silence and arrived at what I was thinking without being told")
            $ reward_attributes_once("day46_night_quiet", [("nerve", "micro")], show="auto")

    call night_close from _call_night_close_23

    "She takes her cup and leaves the door open a hand's width. I hear her go down the stairs, then the house settle into its night sounds."
    "The paper from the market is folded on the desk. The knife is on the shelf. The notebook has three new lines in it and no new questions, which is a kind of evening I do not get often."
    mc "(Saturday. A day I made up for myself. Nothing happened in it that I could not explain, and I do not know why that feels like a gift.)"

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
