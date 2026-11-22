################################################################################
## SPECIAL DAY 48: THE BATHHOUSE ON THE CORNER
## Monday, May 25, 2026. The rain comes early, the house empties for the
## evening, and he does the one thing the guidebook never thinks to put in the
## guidebook.
##
## Solo day. The sento is the most democratic room in Japan, and that is the
## point of it. A stranger teaches him the only rule that matters.
################################################################################

label special_day_48_sento:
    $ set_story_day(48)
    call day_transition from _call_day_transition_31
    $ last_afternoon_place = None
    $ last_afternoon_hikari_tour = False

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Monday. The sky is doing the thing it has been threatening to do all week, which is hold on to the rain without letting it fall."
    "The air is heavy and warm and wrong for the hour. The window has fogged on the outside, which I did not know windows could do."

    "My phone buzzes."

    $ run_chat("hikari", [
        {"them": "I have the English class tonight. The conversation one. I will be home late.", "options": [
            {"label": "\"Since when do you take English?\"",
             "send": "Since when do you take English?",
             "them": ["Since always. It is my one failing subject.", "Do not tell Father.", "He thinks I am perfect. Let him."]},
            {"label": "\"Then I have the evening.\"",
             "send": "Then I have the evening.",
             "them": ["You do.", "Do something with it.", "Not homework. Something with a door."]},
        ]},
    ])
    mc "(Something with a door. She says things like that and then puts the phone down as if it were an ordinary sentence, which, in this house, it is.)"

    call murakami_daily_ping from _call_murakami_daily_ping_18

    scene bg_kitchen with walk_fade

    "The kitchen is quick and warm. Mother has rice on. Father has already gone. There is a smell of soy and something grilling."
    mother "You are out tonight?"
    mc "I might be."
    mother "Take the umbrella that works. Not the clear one. The clear one has a break in it and it will soak your shoulder and then you will sulk."
    mc "I do not sulk."
    mother "You sulk quietly. It is worse."
    mc "(She is right. I sulk quietly. It is worse.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/school.mp3" fadein 2.0

    "The school day passes the way the last weeks have passed, quick and full and oddly weightless. The lecture, the notes, the bell. Two weeks to the end of the term, says the board by the gate, though I have not been counting down so much as counting."
    mc "(I have stopped being a person who arrived. I am a person who is here. I do not know when that happened.)"

    scene bg_campus_interior with walk_fade

    "After class I walk out through the department corridor where I once found a door that was not there. The wall is a wall. The third tile squeaks. The notice board has a new notice on it about a summer program."
    mc "(I stopped looking for the door. I am not sure whether that is healing or giving up.)"

    scene bg_home_exterior_night with walk_fade
    $ night_street()

    "I come home and the house is quiet in the particular way a house is quiet when one person is out of it. Hikari is at her class. Father is not home yet. Mother is upstairs with the radio."
    "I sit in my room for a while. The rain still has not decided. The evening is long and empty in the way an evening is when nobody has asked anything of it."

    mc "(Something with a door.)"

    "And then I remember the thing I have walked past a hundred times without once going in."
    "Two streets over, between the laundry and the little hardware shop, there is a building with a split curtain hanging in the doorway. Blue, with the character for hot water on it. It has been there the whole time."
    "I have walked past it in the morning and in the evening and I have never once seen anyone go in or come out. I always assumed it was closed. I think now that I never looked at the right hour."

    scene bg_sento_outside with walk_fade
    stop music fadeout 1.5
    play music "audio/Music/(Store?) copper_and_velvet.mp3" fadein 2.0

    "At seven there are sandals outside the door and steam in the gutter and the curtain is pushed to one side, which means open, which means come in, which means the whole night has a plan now."

    "I push through the curtain. The genkan is low and warm and smells of soap and steam and faintly of chlorine and the sea."
    "An old man behind a high wooden counter looks up over his glasses. Behind him, on the wall, is a faded chart of the baths with the prices painted on in careful characters."
    "He points at a row of small lockers by the door for shoes and holds up two fingers. Two hundred and twenty yen to get in, plus a coin for the locker. I pay. He gives me a small key on an elastic band and goes back to his paper."
    mc "(That was the entire transaction. He did not ask if I had done this before. He did not need to. Everyone does this the first time exactly once.)"

    scene bg_sento_bath with walk_fade

    "Through the second curtain it is all steam and tile and the low roar of running water. Two rows of washing stations along the wall, each with a small stool, a basin, a mirror, and two taps, one red and one blue."
    "There are four men in here. An old one in the corner who has clearly been here for a century. A man my father's age. Two boys who came in arguing and have gone quiet because it is a bath and you go quiet in a bath."

    "I go to a station at the end of the row and sit down on the little stool, which is far lower than I expected, and this is the mistake, because everyone turns and looks."
    mc "(What did I do. What did I do.)"
    "The old man in the corner does not look up. He says, to the tiles, in Japanese that is slow on purpose, that I should wash first."
    "He says it without turning, the way you tell a stranger his shoe is untied. Not unfriendly. Not a scolding. A fact he has decided it would be rude to let me keep getting wrong."

    "Wash first. Of course. This is a bathhouse. The bath is not for washing. The bath is for sitting in. The washing happens here, on the stool, in the open, beside everyone else."
    mc "(I have watched enough of this country by now to know the general shape of it. You do the private thing in public and the public thing in private. You wash where everyone can see you and you soak where everyone is quiet.)"

    "So I wash. I copy the man my father's age, who is doing the least amount of anything with the most amount of calm. Hair, face, arms, the awkward reach of the back. I rinse the basin, I tip the seat dry, I wring the towel and set it on the shelf, the way the others have done."
    "Nobody watches me after the first minute. That is the relief of the place. Once you are doing it right, you become furniture, and being furniture here is the whole welcome."

    menu:
        "Ask the old man about the mural.":
            "Over the whole far wall, above the bath, is a painting. Mount Fuji, of course. Blue, capped with snow, with a lake and a pine and two birds that have faded to almost nothing."
            mc "The mountain. Who painted it?"
            "The old man shrugs. He says it was here before him and it will be here after, and that every sento in this city has the same mountain, and that is not lazy, that is a promise."
            mc "A promise of what?"
            "He thinks about it. Then he says: that you will always be able to find one of these, somewhere, and when you are in it you will know exactly where you are."
            mc "(Every bath in the country claims the same mountain. So the mountain stops being a place and becomes a way of saying: you have arrived. You are clean. You may sit down.)"
            $ log_memory("sento", "painted Mount Fuji, the way every sento paints Mount Fuji, as a promise that you will always find one")
            $ reward_attributes_once("day48_sento_mural", [("insight", "micro")], show="auto")
        "Follow the old man exactly.":
            "I watch the old man in the corner and I do what he does, no more and no less. He washes, he rinses, he tips the basin, he hangs the towel on his head like a small flag."
            "Then he stands and walks to the bath, and I stand and walk to the bath, and I am suddenly aware that I have just learned a room by copying an eighty-year-old stranger with perfect trust."
            mc "(I did not ask a single question. I just watched and then I was no longer new. This country does most of its teaching this way, and I have finally stopped fighting it.)"
            $ log_memory("sento", "learned the whole room by copying the oldest man in it, without a single question")
            $ reward_attributes_once("day48_sento_copy", [("grace", "micro")], show="auto")
        "Rinse off and get in quickly.":
            "I wash fast and get up, which is wrong, I can feel it is wrong, the stool should be tucked and the basin rinsed and I do both but I do them at the wrong speed."
            "The water is very hot. Much hotter than any bath I have ever been in. For a second it is a mistake and then it is the best thing that has happened to my body in six weeks."
            "I lower myself in up to the chest and hold still and let it do whatever it is doing, which is loosening something I did not know was tight."
            mc "(I understand the whole country a little better down here. This is why they say the bath is where the day is forgiven.)"
            $ log_memory("sento", "got into the hot water too fast and stayed anyway, and let the day be forgiven")
            $ reward_attributes_once("day48_sento_fast", [("nerve", "micro")], show="auto")

    "The bath is quiet except for the water and the occasional splash and one man who sighs every few minutes like a kettle letting off."
    "Beside the bath, in a smaller tub, the water is cold, and men go from the hot to the cold and back, and they make no ceremony of it, they just move between the two temperatures like a decision they have made a thousand times."
    "The old man goes hot, cold, hot. The boys go hot, cold, and then straight back to hot and then get out because they are boys and can only manage so much."
    mc "(The bath is the only room in this country where nobody is anybody. There are no suits in here. There is no one with a title. Everyone is the same shape and the same temperature and nobody looks and nobody minds.)"

    "I do the cold tub once, for a count of ten, mostly to prove something to nobody, and I am very glad when it is over. Then I do the hot tub one more time, slowly, because the hot tub is the reward for the cold one, and everyone here knows that without being told."

    "When I finally get out my skin is pink and my hands are wrinkled and I feel like a person who has been put back together by somebody patient."

    scene bg_sento_outside with walk_fade

    "In the little lobby, by the counter, there is a fridge with a glass door. Inside, squat bottles. Milk. Fruit milk. Coffee milk. In this country, and I do not fully understand why yet, the drink you have after a bath is milk, cold, in a bottle, standing at the counter."
    "The old man behind the counter gestures at the fridge without looking up. One hundred and twenty yen. I take the fruit milk. It is cold and sweet and it goes down the way water goes down after a long walk."

    "The old man from the corner comes out, dressed, transformed, a person again. He sees me with the bottle and nods once, which I understand is the whole conversation we were ever going to have."
    mc "(Wash first. That was the lesson. That was the entire lesson, and it was enough.)"

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    stop music fadeout 2.0

    "The walk home is the best part. The rain has finally started, soft and warm, and the cool air on my hot face is the whole point."
    "I pass the laundry, the hardware shop, the vending machine that hums its one low note. Every one of them looks different now. They look like a street I live on instead of a street I walk down."

    scene bg_kitchen_night with walk_fade
    $ room_ambient(True)

    "At home the kitchen light is on. Hikari is back from her class, at the table with a book and a cup. My dinner is on the stove with a lid over it, still warm."

    hikari "You smell like soap and steam."
    mc "The bathhouse. Two streets over."
    hikari "The sento. You went to the sento."
    mc "You never told me it was there."
    hikari "It is not a thing you tell. It is a thing you find, at the hour you need it."
    mc "How did you know I needed it?"
    hikari "You have been carrying your shoulders by your ears for a week. You needed somewhere hot."
    mc "(She is right. She is always right about the shoulders.)"

    "We eat. She does not ask me anything about the bath, because there is nothing to ask about a bath, which is the point of a bath. She tells me about her English class instead, and how she answered yes to a question that was not a yes or no question, and how the teacher laughed, and how she has decided the teacher was laughing with her."
    mc "(Three weeks from now she will still be deciding that. This is who she is. She does not lose things, she just holds them at a small distance until they are safe.)"

    scene bg_room_night with stair_fade
    $ room_ambient(True)

    "Upstairs, the tenugui I bought at the counter is drying over the chair. Cheap cloth, a pattern of waves, the kind they sell by the door for two hundred yen. It will never be as good as running water over my back, but it is mine, and it cost almost nothing."
    "I write one line about the bath. Wash first. The whole rule of the country in two words, and I learned it from a man who never looked up."

    $ night_desk_line = "the tenugui drying over the chair"

    call night_open from _call_night_open_25

    "Hikari comes in with the tea and sits on the floor with her back against the bed."
    hikari "I am not staying."
    mc "You never stay."
    hikari "I have to be up early for the run. So."

    menu:
        "[tag_grace] Rank 3: Tell her you want to take her to the sento properly." if has_attribute("grace", 3):
            mc "Next time, come with me. Not to wait outside. All the way in."
            hikari "You would take me to a bathhouse."
            mc "I would wash first, like the old man said. Then I would sit in the cold tub and complain."
            hikari "That is the most specific invitation anyone has ever made me."
            mc "(She is smiling at the floor. I decide not to say anything about it.)"
            $ log_memory("hikari", "invited her to the sento properly, wash first, then the cold tub")
            $ reward_attributes_once("day48_night_invite", [("grace", "micro")], show="auto")
        "Tell her the old man taught me.":
            mc "There was an old man. He told me to wash first."
            hikari "He was right."
            mc "He never looked at me. He said it to the tiles."
            hikari "That is how the good ones do it. If he had looked at you, you would have felt like a tourist, and he did not want you to feel like a tourist. He wanted you to feel like a person who was getting it slightly wrong."
            mc "Is that better?"
            hikari "It is completely different, and yes."
            $ log_memory("hikari", "said the old man told me off to the tiles so I would feel like a person, not a tourist")
            $ reward_attributes_once("day48_night_oldman", [("insight", "micro")], show="auto")
        "Ask why the milk after the bath.":
            mc "The milk. After the bath. Nobody explained it. Everyone just did it."
            hikari "Nobody explains it because it is not a rule. It is just true."
            mc "That is not an answer."
            hikari "It is the only answer. Some things in this country do not have reasons. They have habits long enough to look like reasons."
            mc "(She makes it sound obvious and it is obvious and I still do not understand it and I suspect that is the correct amount of understanding.)"
            $ log_memory("hikari", "said the milk after a bath is not a rule, it is just true")
            $ reward_attributes_once("day48_night_milk", [("grace", "micro")], show="auto")
        "Say nothing. Finish the tea.":
            "I do not tell her about the mural or the milk or the cold tub. I drink the tea and let the day go quiet, which is the last part of a bath, the part nobody talks about."
            "Hikari does not fill the silence. She never does. She just sits and lets it be a room with two people in it."
            mc "(Tomorrow is a school day and the rain is really here now and somewhere two streets over a painted mountain is waiting for whoever needs it next.)"
            $ log_memory("hikari", "sat with me in the quiet after the bath and did not fill it")
            $ reward_attributes_once("day48_night_quiet", [("nerve", "micro")], show="auto")

    call night_close from _call_night_close_25

    "She takes the cup and leaves the door open a hand's width. I hear her go down the stairs, then the house settle into its night sounds."
    "The rain is steady now. It will rain tomorrow and the day after, and the man behind the counter will still be reading his paper, and the mountain on the wall will still be there with its two birds faded to almost nothing."
    mc "(Wash first. I will remember that longer than I will remember anything anyone lectured at me all term.)"

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
