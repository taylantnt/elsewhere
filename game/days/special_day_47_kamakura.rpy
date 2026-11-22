################################################################################
## SPECIAL DAY 47: THE BUDDHA AND THE LITTLE GREEN TRAIN
## Sunday, May 24, 2026. Hikari takes him to Kamakura, because a city that old
## deserves a whole day and a train ride, and because she has been saving it.
##
## Hikari's lesson today is a real one: a shrine and a temple are not the same
## place, and the difference is in your hands.
################################################################################

label special_day_47_kamakura:
    $ set_story_day(47)
    call day_transition from _call_day_transition_30
    $ last_afternoon_place = None
    $ last_afternoon_hikari_tour = False

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Sunday. The light comes in flat and even, the way it does when the day has nothing to prove."
    "I wake to the sound of Hikari going through her bag in the next room. Zippers. The tap. Zippers again."

    "There is a note slid under my door in her handwriting, which she has never done before."
    "It says: Shoes you can walk in. We are leaving at eight. Bring money for lunch and nothing else."
    mc "(She has planned something. She does not plan things out loud. She plans them by leaving a note under a door and going quiet.)"

    "My phone buzzes."

    $ run_chat("hikari", [
        {"them": "Read the note.", "options": [
            {"label": "\"I read it. Where are we going?\"",
             "send": "I read it. Where are we going?",
             "them": ["That is a question for a person who is not coming.", "You are coming.", "So it does not matter yet."]},
            {"label": "\"Shoes you can walk in. How far?\"",
             "send": "Shoes you can walk in. How far?",
             "them": ["Far enough that the wrong shoes would ruin it.", "Not so far that you would complain.", "Probably."]},
        ]},
    ])
    mc "(Probably. She typed probably and then put the phone down and went back to her bag.)"

    call murakami_daily_ping from _call_murakami_daily_ping_17

    scene bg_kitchen with walk_fade

    "Downstairs Mother is at the table with her tea. Father is not. On Sunday he is a shape at the edge of the house, present and not quite accounted for."
    mother "She is taking you somewhere."
    mc "She would not say where."
    mother "Then it is somewhere she likes. She only gets quiet about the places she likes."
    mc "Am I supposed to guess?"
    mother "No. You are supposed to go and look."
    mc "(Everyone in this house has a rule about going and looking. Nobody writes them down.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "Hikari is already at the gate when I come out. She has a small canvas bag and a hat she does not normally wear and a look I have learned to read as I have decided something and I am not going to argue about it."
    hikari "You are on time."
    mc "You gave me a note."
    hikari "The note was the plan. The plan was the train. The train does not wait for people who are not on time."
    mc "(She is right. It does not.)"

    scene bg_station with walk_fade
    scene bg_platform with walk_fade
    scene bg_train_interior with walk_fade
    play music "audio/Music/train.mp3" fadein 2.0

    "The train south takes about an hour. It goes through the city and then under it and then out the other side, and the buildings get lower, and then there are hills, and then there is a gap in the hills where the sea is hiding."
    hikari "You can tell the moment the city ends. It is not a sign. It is the sound."
    mc "What sound?"
    hikari "The sound stops having an echo. The city is all hard faces. Out here it lets go."
    "She is right. It is not that it goes quiet. It is that the quiet has a bottom to it now, the way a room has a floor."

    mc "You had this planned for a while."
    hikari "A while."
    mc "Why now?"
    hikari "Because it is that time of year, and because it is the kind of place you should see before it rains for a month."
    mc "(The rainy season. She has been watching the sky the way Father watches the road.)"

    scene bg_kamakura_station with walk_fade
    stop music fadeout 1.5
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 1.5

    "Kamakura station is small and old and smells of the tram that runs through it. Outside there is a street of shops packed shoulder to shoulder, selling everything a person could want and nothing a person could need."

    "Hikari walks it like a person walking a hallway she grew up in."
    hikari "Souvenirs. If you buy one, buy it on the way back. Otherwise you carry it all day."
    mc "Do I want a souvenir?"
    hikari "You want a soft serve. Everyone wants a soft serve. You will fight it until lunch and then buy one anyway."
    mc "(I will buy one at eleven. I already know this about myself.)"

    "She is proved right before noon. Matcha, the color of a thing that grew in shade. We eat them walking, and she pretends not to be delighted, and fails."
    hikari "Do not tell anyone I did this."
    mc "Did what?"
    hikari "The face I am making."
    mc "I am not looking at your face."
    hikari "Good."
    mc "(I was looking at her face. She knows I was looking at her face. That was also fine.)"

    scene bg_kamakura_daibutsu with walk_fade
    play music "audio/Music/(Hanabi night) lanterns_at_dusk.mp3" fadein 2.0

    "Then the street opens and there he is."
    "The Great Buddha. Bronze, seated, taller than the trees. He has no roof over him and has not had one for five hundred years, because the sea came up once and took the hall away and the sea is not coming back for the hall."
    "So he sits. In the open. In the rain and the sun and the snow, for five centuries, and looks at whoever comes, and does not seem to mind which one of them it is."

    mc "(I have seen a thousand photographs of this. In the photographs he is a statue. He is not a statue. He is a man who sat down five hundred years ago and stayed.)"

    hikari "Do not stand in the path. People will walk through you."
    "She takes my sleeve and moves me, gently, to the side."

    "Near the steps there is a basin under a little roof. Water, a ladle, the same order I learned on the mountain with Father: right hand, left hand, water in the palm, the quiet rinse."
    "I do it without being told, in the right order, and Hikari watches me do it and does not correct me, which I understand, suddenly, is a kind of applause."

    hikari "You remembered."
    mc "I remembered."
    hikari "Good. Now watch."
    "She steps up to the offering box in front of the Buddha. She does not clap. She puts her palms together, and she is quiet for exactly as long as it takes to be quiet, and then she lets her hands fall."
    mc "You did not clap."
    hikari "You do not clap here."
    mc "At the shrine with Father, you clapped."
    hikari "That was a shrine. This is a temple. They are not the same thing and the difference is in your hands."
    mc "Explain it."
    hikari "At a shrine you clap. You are calling somebody's attention. At a temple you do not. You are not asking. You are listening."
    mc "(All this time I have been doing both of them the same. I have been introducing myself to gods the way you introduce yourself at a door, when one of them wanted me to sit down first.)"

    menu:
        "[tag_nerve] Rank 3: Put a coin in and say what you are carrying." if has_attribute("nerve", 3):
            "I put a coin in the box. It makes a small sound against the wood."
            mc "I am carrying a question I do not want answered."
            hikari "That is what the box is for. You just said it out loud."
            $ reward_attributes_once("day47_coin_carry", [("nerve", "micro")], show="auto")
        "Ask why she offered no coin.":
            mc "You did not put anything in the box."
            hikari "I did at the shrine with Father. The five-yen coin."
            mc "Why not here?"
            hikari "Because he is not collecting. A shrine is a house with a keeper. A temple is a place that is simply here, and it does not care if you pay."
            mc "Then why does the box exist?"
            hikari "Because people need somewhere to put the thing they are carrying. The box is not for him. It is for you."
            mc "(It is for me. I did not put anything in. I do not know yet what I am carrying.)"
            $ log_memory("hikari", "said the offering box at the temple is for the person, not for the Buddha")
            $ reward_attributes_once("day47_coin", [("insight", "micro")], show="auto")
        "Go inside the Buddha.":
            "I pay the small coin at the little gate and duck through a door set into the Buddha's back, and I am inside him."
            "It is dark and warm and smells of old metal and old smoke. A few small windows on his back let in thin panels of light, and in the light I can see the seams of the bronze, the joins where men in a hotter age poured him out in pieces and put him together."
            "It is not a hollow. It is a body. There is a small staircase up his spine."
            mc "(I am standing inside a person who has been sitting on this spot longer than the city I live in has had its current name. I do not know where to put that. So I stand still and I do not check how long.)"
            "When I come back out Hikari is waiting with her hands in her pockets, looking at the trees."
            hikari "Well?"
            mc "He is hollow. There is a staircase in him."
            hikari "People always come out saying that. They never come out saying what they felt inside."
            mc "What did you feel?"
            hikari "Warm. He is warmer than the air. Do not tell anyone. It sounds like a thing a person made up."
            $ log_memory("hikari", "said the inside of the Great Buddha was warmer than the air, and asked me not to tell anyone")
            $ reward_attributes_once("day47_inside", [("nerve", "micro")], show="auto")
        "Watch the people around the Buddha.":
            "I step back and just watch. A school group in identical hats. An old couple who walk to the box together and stand a long time. A toddler who points and says the word for big about forty times."
            "Hikari stands beside me and watches the people watching him."
            hikari "Everyone makes the same face."
            mc "They do."
            hikari "That is the whole point of him. He is the one thing in this city that everybody agrees on."
            mc "(A bronze man in a field, five hundred years, and a thousand strangers a day making the same small face. There is nothing in the city I live in that everybody agrees on.)"
            $ log_memory("hikari", "said the Great Buddha is the one thing in this country everybody agrees on")
            $ reward_attributes_once("day47_watch", [("grace", "micro")], show="auto")

    scene bg_enoden with walk_fade
    play music "audio/Music/train.mp3" fadein 2.0

    "After the Buddha we take the little green train, the Enoden. It runs on a track so small and so old that on some streets it just goes down the middle of the road, past shops and houses and a woman hanging laundry, close enough that I could reach out the window and touch a wall."
    hikari "Do not put your hand out the window."
    mc "I was not going to."
    hikari "You were thinking about it. I saw the thinking."
    mc "(I was thinking about it. She is getting very good at watching me think.)"

    "At one stop the train slows for no reason I can see, and everyone in the car turns their head the same way, and there it is, between the houses, a strip of ocean, blue and flat and enormous."
    hikari "That is why they all look. They have looked a thousand times. They still look."
    mc "(Some things do not wear out. The sea is one of them.)"

    scene bg_kamakura_shore with walk_fade
    play music "audio/Music/(Hanami) summer_night_embers.mp3" fadein 2.0

    "We get off by the water. The beach is grey sand and black rock and gulls that are not afraid of anyone. A man is walking a dog that has clearly won every argument it has ever had."

    "Hikari leads me to a little place along the road where the menu is on the wall and the specialty is a bowl of rice with whitebait on top, the tiny fish this coast is known for."
    "There are two kinds. One is boiled, the whole bowl pale and warm. One is raw, and it is only served where the fish is fresh enough that morning, and it costs more."

    menu:
        "Order the raw whitebait. The morning's catch.":
            mc "The raw one. How fresh does it have to be?"
            hikari "Fresh enough that they would not dare if the boats had not come in. If you order it and it comes, the sea is having a good day."
            "It comes. It is cool and glassy and tastes of nothing much and of the sea at once, the way a very good thing often does."
            hikari "Well?"
            mc "It tastes like the water the boat was on."
            hikari "That is the most accurate thing anyone has ever said about it."
            $ log_memory("hikari", "told me raw whitebait only comes on days when the sea is having a good day")
            $ reward_attributes_once("day47_shirasu_nama", [("nerve", "micro")], show="auto")
        "Order the boiled whitebait. The safe bowl.":
            mc "The boiled one. I would rather know what I am eating."
            hikari "You would rather be sure. That is not the same thing. But the boiled one is also very good, and the sea will not be offended."
            "It comes warm and pale, soft and slightly sweet, and I eat it in the order the bowl asks for, fish and rice and fish and rice, until it is done."
            hikari "You ate it in order."
            mc "Was that wrong?"
            hikari "No. It was exactly right. You did not even notice you were doing it."
            mc "(I did not notice. This country is quietly teaching me its table manners while I am looking at the sea.)"
            $ log_memory("hikari", "said I ate the bowl in order without noticing I had learned how")
            $ reward_attributes_once("day47_shirasu_kamaage", [("grace", "micro")], show="auto")

    "We sit outside while the light starts to go long and orange over the water. Hikari watches the sea and says nothing for a while, which for her is a full sentence."

    hikari "My mother brought me here when I was small. Not this restaurant. This coast."
    mc "The host mother."
    hikari "Yes. She used to say the sea is the same sea everywhere, so you can always find your way back to it. I thought that was silly. The sea is enormous. Finding your way back to the sea is like finding your way back to the sky."
    mc "And now?"
    hikari "Now I think she meant something else. She meant that some things are so big that they are the same even when they are different. You do not find the sea. You find that you have been standing next to it the whole time."
    mc "(I do not say anything. There is nothing to add to that, and she would know if I tried.)"
    $ add_affection("sister", 1)

    scene bg_train_interior with walk_fade
    play music "audio/Music/train.mp3" fadein 2.0

    "We take the train home in the last of the light. Hikari falls asleep against the window, which she would deny with her whole body, and I let her, and I watch the hills turn into the city again."
    "At the far end of the car a woman is reading a paperback. Two stops on, she is still on the same page. Some books are only good enough to hold."

    scene bg_home_exterior_night with walk_fade
    $ night_street()

    "Home at dark. Father is home, which is unusual. The house smells of the dinner Mother has been keeping warm."
    scene bg_kitchen_night with walk_fade
    $ room_ambient(True)

    mother "You went far."
    hikari "Kamakura."
    mother "Ah. The Buddha."
    hikari "The Buddha."
    father "I went once. As a boy. I do not remember the Buddha. I remember the train."
    hikari "That is because you are a man who remembers the train and not the thing the train was for."
    father "Hm."
    mc "(Hikari argues with Father the way other people agree with him. He seems to find it restful.)"

    mother "Did you eat?"
    mc "Whitebait. Both kinds between us."
    mother "Good. That is the right thing to eat there. Nothing else you eat in Kamakura is the right thing."
    father "The soft serve is the right thing."
    mother "You have never been."
    father "I have read about it."
    mother "You have read about the soft serve."
    father "The article was very convincing."
    mc "(Two lines. Over. The marriage again.)"

    scene bg_room_night with stair_fade
    $ room_ambient(True)

    "Upstairs, I empty my pockets onto the desk. The Enoden ticket. A folded map with a tear along one fold. The little wooden charm I did not buy."
    "I write two lines in the notebook, one about the Buddha and one about the sea, and then I sit and do not write a third, because some days do not want a third line."

    $ night_desk_line = "the Enoden ticket and the folded map"

    call night_open from _call_night_open_24

    "Hikari comes in a while later with the tea and, and this is new, the hat she wore all day, which she sets on the desk like a small surrendered animal."
    hikari "I am not staying."
    mc "You brought the hat."
    hikari "The hat is not staying either. The hat is resting."
    mc "(The hat is staying. I know it is staying. She will come back for it and it will be gone and she will pretend she never left it.)"

    menu:
        "Ask her about what her mother said, about the sea.":
            mc "The thing your mother said. About the sea being the same everywhere."
            hikari "You have been carrying that around all day."
            mc "I have."
            hikari "So have I. I think about it every time I go back to the water. That is why I go to the water."
            mc "To check if it is still the same?"
            hikari "To check that I am still standing next to it. That is the part she was really saying. The sea does not move. You do."
            mc "(She says it like a thing she has confirmed many times and never once said out loud until now.)"
            $ log_memory("hikari", "said she goes to the water to check that she is still standing next to it")
            $ reward_attributes_once("day47_night_sea", [("insight", "micro")], show="auto")
        "Tell her the temple lesson landed.":
            mc "The clapping thing. Shrine and temple. I have been doing it wrong for six weeks."
            hikari "You have been doing it wrong for six weeks and nobody told you, and now you will never do it wrong again."
            mc "Why did nobody tell me?"
            hikari "Because it is a small thing, and small things are the ones people let you keep until you are ready to trade them in."
            mc "(She could have told me on the first day. She did not. She waited until it was a gift and not a correction.)"
            hikari "Do not look at me like that."
            mc "Like what?"
            hikari "Like I did something good. I just waited, is all."
            mc "(Waiting is doing something good. It might be the only good thing there is.)"
            $ log_memory("hikari", "waited six weeks to correct the way I clapped, so it would be a gift and not a correction")
            $ reward_attributes_once("day47_night_lesson", [("grace", "micro")], show="auto")
        "Let her rest. Say nothing.":
            "I do not ask her anything. She is tired from a day of walking and telling me things and being the one who knows the way."
            "We drink the tea. Outside, a train, then the quiet, then the small sounds of a house getting ready to sleep."
            "Before she goes she says, mostly to the window, that the day was good. She does not say it to me. She says it to the window. But I am close enough to the window to hear it."
            $ log_memory("hikari", "said to the window that the day was good, because saying it to me would have been too much")
            $ reward_attributes_once("day47_night_quiet", [("nerve", "micro")], show="auto")

    call night_close from _call_night_close_24

    "She takes the cup and leaves the hat and goes. I hear the door click once, which is the correct number of times."
    "The ticket is on the desk. The map is folded the way I found it. The sea is somewhere south of here, doing what it does, and I am a person who has stood next to it and come home."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
