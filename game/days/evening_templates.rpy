################################################################################
## THE EVENING TEMPLATES
################################################################################
##
## Days 8-12 used to carry four copies of the same dinner and five copies of the
## same night visit. The content was good; the delivery was a loop. This file
## keeps one copy of each piece and rotates the frame around it.
##
## A day still owns what is actually said:
##
##     call dinner_open
##     father "And the book?"
##     ...
##     call dinner_close
##
## `dinner_open` picks the frame for the day and plays the shared afternoon
## report. `dinner_close` lands the frame after the day's own topic. The same
## split applies to the night: `night_open`, the day's menu, `night_close`.
##
## The frame is chosen by `story_day`, not at random, so a save always comes
## back to the same dinner. A reload is not a re-roll.

default dinner_variant_today = "ordinary"
default night_variant_today = "tea"

## What the day's narrator was looking at when Hikari knocked. The day sets it
## before calling `night_open`; the tea variant uses it for her "same thing".
default night_desk_line = "the wall"

init python:

    def dinner_variant_for_day(day=None):
        """Which dinner frame belongs to a day. Deterministic, never random."""
        if day is None:
            day = store.story_day
        day = int(day)
        if day == 12:
            return "hikari_cooks"
        return ["ordinary", "quiet", "tetsuo", "miharu"][(day - 8) % 4]

    def night_variant_for_day(day=None):
        """Which night frame belongs to a day. Deterministic, never random."""
        if day is None:
            day = store.story_day
        day = int(day)
        if day == 8:
            return "tea"
        if day == 9:
            return "window"
        if day == 10:
            return "sleep"
        if day == 11:
            return "tea"
        if day == 12:
            return "sleep"
        return ["tea", "window", "sleep"][(day - 8) % 3]


################################################################################
## DINNER
################################################################################

label dinner_open(variant=None):

    $ dinner_variant_today = variant if variant else dinner_variant_for_day()

    scene bg_home_night with walk_fade
    $ room_ambient(True)
    "The house is warm the way it is when someone has been cooking for a while."
    "I leave my shoes by the door, turned around, and follow the smell to the kitchen."

    scene bg_kitchen_night with walk_fade

    if dinner_variant_today == "quiet":
        jump dinner_open_quiet
    elif dinner_variant_today == "tetsuo":
        jump dinner_open_tetsuo
    elif dinner_variant_today == "miharu":
        jump dinner_open_miharu
    elif dinner_variant_today == "hikari_cooks":
        jump dinner_open_hikari_cooks

    jump dinner_open_ordinary


label dinner_open_ordinary:
    "Mother is ladling something into four bowls. Father is setting the table with the careful imprecision of a man who has been told to help."
    mother "There you are. Wash your hands."
    hikari "You're late."
    mc "I'm not late. Dinner is early."
    hikari "Dinner is on time. You're late."
    "I wash my hands. The water is warm."
    mother "Where did you go?"
    call dinner_report
    return


label dinner_open_quiet:
    "The kitchen is dimmer than usual. One lamp over the table, the stove turned down to nothing."
    "Mother is already seated. Father is at the head of the table with his hands folded, not reading, not eating."
    mother "Sit."
    "Nobody asks where I was. The question is not being withheld. It has been decided that I will say it if it matters."
    "Hikari comes in behind me and sits without a word."
    father "You were out."
    mc "I was out."
    father "Good."
    call dinner_report
    return


label dinner_open_tetsuo:
    "Father is standing at the counter with his back to the table. He is not helping. He is watching the pot the way he watches the news."
    father "Sit. Before the food."
    "I sit. Mother sets down four bowls. Hikari raises her eyebrows at me, which means: he has been like this since he came home."
    father "A man at work asked me what I do at home."
    mc "What did you say?"
    father "I said I set the table."
    father "He laughed. I did not."
    "He turns from the pot. He has the look he gets when he has decided to say a thing in the order he has planned it."
    father "A job is a thing you make every day. A table is a thing you make every night. One of them can be taken from you."
    mc "(I do not know if that is comfort or a warning. In this house it is usually both.)"
    mother "Tetsuo."
    father "I am being helpful."
    mother "You are being ominous."
    father "It is the same thing, in this house."
    father "Where did you go?"
    call dinner_report
    return


label dinner_open_miharu:
    "The stove is off. The food is already on the table, covered with a cloth."
    "Mother is sitting with her hands around a cup she is not drinking."
    mother "Sit. You are tired."
    mc "I'm not tired."
    mother "You are tired in the way that does not show. That is the kind that counts."
    "She reaches across and straightens my collar. She has not done that before."
    "Hikari looks at her, then at me, and decides not to say anything."
    mother "I was nineteen when I left my mother's house. I did not know I was allowed to be tired."
    mc "Were you?"
    mother "No. That is why I am telling you."
    "She lifts the cloth from the bowls. Steam."
    mother "Where did you go?"
    call dinner_report
    return


label dinner_open_hikari_cooks:
    "The kitchen smells different. Not Mother's cooking. Something with too much soy and not enough patience."
    "Hikari is at the stove, holding a wooden spoon like a tool she has borrowed and intends to return."
    hikari "Don't look at me. Sit."
    mother "She insisted."
    father "She insisted loudly."
    hikari "I could hear you both."
    "She sets down four bowls. One of them is the chipped one. She gives that one to herself."
    mc "You cooked."
    hikari "I cooked. Don't make it a thing."
    mc "(It is already a thing. The whole table knows it.)"
    hikari "Where did you go?"
    call dinner_report
    return


## The one copy of the afternoon callback. Every dinner frame ends here, so the
## place the player picked is still the thing the table asks about.
label dinner_report:
    if last_afternoon_place == "chef":
        mc "The ramen shop. The broth had been going since morning."
        mc "(He did not make a thing of it. That was the whole welcome.)"
    elif last_afternoon_place == "aya":
        mc "The maid cafe. She remembered the order before I said it."
        mc "(For about four seconds she was not performing. I don't think she noticed she did it.)"
    elif last_afternoon_place == "hana":
        mc "The reading room. She was there. She stayed."
        mc "(We did not talk much. It was enough.)"
    elif last_afternoon_place == "orson":
        mc "Lupin's Den. The bar was empty enough to hear the ice."
        mc "(He taught me a phrase I am still turning over.)"
    elif last_afternoon_place == "sim":
        mc "The photography club. Sim made us photograph something ordinary until it stopped being ordinary."
    elif last_afternoon_place == "walk_hikari":
        mc "I walked home with Hikari. We took the long way."
        hikari "You took the long way. I followed."
        mc "That's not how I remember it."
        hikari "That's because you were busy being right."
    elif last_afternoon_place == "walk_alone":
        mc "Nowhere. I walked until the light changed, and then I walked home."
        father "Nowhere is a place. Just not a destination."
        mc "(That is either wisdom or a warning. I am not sure which.)"
    elif last_afternoon_place == "library":
        mc "The campus library. I read until the words stopped moving and started meaning something."
        mother "Good. A library is a building that keeps its promises."
    elif last_afternoon_place == "river":
        mc "The river. I sat on the bank until the light went orange and the trains turned their lights on."
        father "The river is the only thing in this city that is not in a hurry."
    elif last_afternoon_place == "harajuku":
        mc "Harajuku. I have never been looked at so much and spoken to so little."
        hikari "That's the whole street. You survived it."
    elif last_afternoon_place == "karaoke":
        mc "A karaoke box. I sang badly in a room built for people who sing well."
        hikari "How badly?"
        mc "The machine gave me a score. I am not going to say what it was."
    elif last_afternoon_place == "night_market":
        mc "The food stalls. I ate standing up, like everyone else, and nobody asked me to explain myself."
        father "That is how you learn a city. Standing up, with your hands full."
    elif last_afternoon_place == "combini":
        mc "The combini. Pens. The kind of errand that takes an hour because the aisles are interesting."
    elif last_afternoon_place == "odaiba":
        mc "Odaiba. The future they built on purpose. The water looked flat for a second, like a screen."
        hikari "You say that about water a lot."
        mc "The water is doing a lot."
    elif last_afternoon_place == "yokohama":
        mc "Yokohama. Chinatown. I was the foreigner in a place built by foreigners."
        mother "That is a useful thing to be once."
    elif last_afternoon_place == "ueno":
        mc "Ueno Park. Half the city was sitting under the blossoms, drinking."
        father "Hanami. The flowers are an excuse. The sitting is the point."
    elif last_afternoon_place == "shibuya":
        mc "Shibuya. The crossing. A thousand people walking into each other and nobody touching."
        hikari "That's the whole city in one minute."
    elif last_afternoon_place == "shimokitazawa":
        mc "Shimokitazawa. Small streets, small theaters, used records."
        hikari "You went somewhere cool without me. That's a crime."
    elif last_afternoon_place == "omotesando":
        mc "Omotesando. The shopping street, then the shrine behind it. The city got quiet all at once."
        mother "That is the trick of it. You turn one corner and the noise is somebody else's."
    elif last_afternoon_place == "fortune":
        mc "Asakusa. The smoke, the fortune slip, and a woman with a folding table who knew my face."
        hikari "She knew your face?"
        mc "She said she had seen it before. I did not ask where."
    elif last_afternoon_place == "tanaka":
        mc "The combini. Four hours behind the register. My feet hurt and I know where the forks are."
        father "That is a job. A job is a thing you make every day."
    else:
        mc "Nowhere. I came straight home."
        mother "Good. Eat."
        mc "(She does not ask why. I am grateful for that.)"
    return


label dinner_close:
    if dinner_variant_today == "quiet":
        "We eat without talking. It is not uncomfortable. It is the house holding its breath."
    elif dinner_variant_today == "tetsuo":
        "We eat. The rice is good. The lesson sits somewhere behind it."
    elif dinner_variant_today == "miharu":
        "We eat. She watches me take the first bite, then looks away."
    elif dinner_variant_today == "hikari_cooks":
        "We eat what Hikari made. Nobody says anything for a while. It is the best thing anyone has cooked in this house."
    else:
        "Nobody argues with that. We eat."
    return


################################################################################
## NIGHT
################################################################################

label night_open:
    $ night_variant_today = night_variant_for_day()

    if night_variant_today == "window":
        jump night_open_window
    elif night_variant_today == "sleep":
        jump night_open_sleep

    jump night_open_tea


label night_open_tea:
    "A knock at the door. Hikari, with two cups of tea and her own notes under her arm."
    hikari "I'm not staying. I'm just making sure you're not staring at the wall."
    mc "I was staring at [night_desk_line]."
    hikari "Same thing."
    "She sets the tea down and sits on the floor with her back against the bed."
    call night_afternoon_callback
    return


label night_open_window:
    "The door opens without a knock. Hikari crosses the room and pushes the window up."
    hikari "It smells like the inside of your head in here."
    mc "That's not a thing."
    hikari "It is now."
    "She sits on the sill with her legs outside, which cannot be allowed and is clearly allowed."
    hikari "I'm not staying. I'm just letting some air in."
    call night_afternoon_callback
    return


label night_open_sleep:
    "A knock, then the door, then Hikari with two cups and her eyes half closed."
    hikari "I'm not staying. I'm just..."
    "She does not finish. She sets the cups down and slides to the floor with her back against the bed."
    hikari "Talk. I'm listening."
    mc "You're falling asleep."
    hikari "I'm resting my eyes. It's different."
    call night_afternoon_callback
    return


## Hikari reacts to the afternoon the player actually chose. This is the thing
## five identical night scenes could not do: she was in the house the whole time
## and never once asked where he had been.
label night_afternoon_callback:
    if last_afternoon_place == "chef":
        hikari "You smell like broth."
        mc "I had ramen."
        hikari "You always have ramen. It's becoming a personality."
    elif last_afternoon_place == "aya":
        hikari "You smell like sugar."
        mc "The cafe."
        hikari "The cafe. You say it like it's a country you visited."
    elif last_afternoon_place == "hana":
        hikari "You're doing the quiet thing."
        mc "What quiet thing?"
        hikari "The one you do after the reading room. Like you're still listening to something."
    elif last_afternoon_place == "orson":
        hikari "You smell like a bar."
        mc "It's a very quiet bar."
        hikari "A quiet bar is still a bar. Don't come home smelling like a secret."
    elif last_afternoon_place == "sim":
        hikari "You've got that camera look."
        mc "What look?"
        hikari "The one where you keep framing things. Stop it. You're at home."
    elif last_afternoon_place == "walk_hikari":
        hikari "You walked slower today."
        mc "I was tired."
        hikari "You were keeping pace. It's not the same thing."
    elif last_afternoon_place == "walk_alone":
        hikari "You went nowhere today. I could tell."
        mc "Nowhere is a place."
        hikari "Dad's been saying that. Don't let him hear you agree."
    elif last_afternoon_place == "library":
        hikari "You have that library face."
        mc "What face?"
        hikari "The one that says you read a sentence four times and still lost."
    elif last_afternoon_place == "river":
        hikari "Your shoes are muddy."
        mc "The riverbank."
        hikari "You went to the river without me."
        mc "I didn't know it was a shared thing."
        hikari "It is now."
    elif last_afternoon_place == "harajuku":
        hikari "You look like you got dressed by a committee."
        mc "I didn't buy anything."
        hikari "That's worse. Now you have the look and nothing to show for it."
    elif last_afternoon_place == "karaoke":
        hikari "Your voice is gone."
        mc "I was singing."
        hikari "That is not what I would call it."
    elif last_afternoon_place == "night_market":
        hikari "You smell like fried things."
        mc "I ate standing up."
        hikari "Good. That's how you're supposed to eat at the stalls. Sitting down is for tourists."
    elif last_afternoon_place == "combini":
        if combini_gift:
            hikari "There is a pudding in the fridge with a bear on the lid."
            mc "It was next to the register."
            hikari "It was in your bag with the egg sandwich I like and pretend not to like."
            mc "(The bag said enough. Apparently the fridge said more.)"
        else:
            hikari "You came home smelling like the combini."
            mc "Supplies."
            hikari "Nobody buys three pens at eight p.m. for supplies."
            mc "(She is right. I also bought coffee in a can, and stood outside drinking it.)"
    elif last_afternoon_place == "odaiba":
        hikari "You have that look. The one you get when something is too new."
        mc "The statue blinked."
        hikari "The Gundam?"
        mc "For a frame. Then it didn't."
        hikari "You need to stop telling me things like that right before bed."
    elif last_afternoon_place == "yokohama":
        hikari "You smell like steamed buns."
        mc "Chinatown."
        hikari "You went to Chinatown without me. Did you at least get lost?"
        mc "Twice."
        hikari "Good. That's the only way to do it."
    elif last_afternoon_place == "ueno":
        hikari "You're pink."
        mc "It was the blossoms."
        hikari "It was the sun and the beer the old men gave you."
        mc "I only had one cup."
        hikari "That's what they all say."
    elif last_afternoon_place == "shibuya":
        hikari "Your shoulders are up by your ears."
        mc "The crossing."
        hikari "The crossing does that. You cross it once for the photo and then you avoid it for a year."
    elif last_afternoon_place == "shimokitazawa":
        hikari "You bought a record."
        mc "How did you know?"
        hikari "You have the face of a person carrying a record."
        mc "It was a good record."
        hikari "They always are."
    elif last_afternoon_place == "omotesando":
        hikari "You're quiet in the shrine way."
        mc "The gravel. You can hear every step."
        hikari "That's the point. The city makes you loud. The shrine makes you listen."
    elif last_afternoon_place == "fortune":
        if fortune_result == "good":
            hikari "You're smiling like the paper said something nice."
            mc "It said a door I already opened would open again."
            hikari "That's either a fortune or a threat."
            mc "(In this city it is usually both.)"
        elif fortune_result == "bad":
            hikari "You're quiet. What did the paper say?"
            mc "That a voice would call me by a name I have not been given."
            hikari "And?"
            mc "On the train back, someone behind me said a name. I turned. Nobody was looking."
            hikari "That's not funny."
            mc "I didn't say it was."
        else:
            hikari "You're doing the fortune-teller face."
            mc "I don't have a fortune-teller face."
            hikari "You do. It's the one where you're trying to decide whether to believe something."
    elif last_afternoon_place == "tanaka":
        hikari "You smell like a combini and fried chicken."
        mc "I worked the register."
        hikari "You worked it. For four hours."
        mc "Four hours."
        hikari "And you're still standing. That's more than I expected."
        mc "(That is either an insult or a promotion. I am too tired to tell.)"
    return


label night_close:
    if night_variant_today == "window":
        "She swings her legs back inside, pulls the window down to a crack, and is gone without saying goodnight."
        "I listen to the street come in through the gap, then the house settle into its night sounds."
    elif night_variant_today == "sleep":
        "She is asleep before I finish my tea. I put the blanket over her and leave the door open a hand's width."
        "The house settles into its night sounds around her breathing."
    else:
        "She takes her cup and leaves the door open a hand's width."
        "I listen to her go down the stairs, then the house settle into its night sounds."
    return
