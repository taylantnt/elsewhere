################################################################################
## SPECIAL DAY 26: SUNDAY, MAY 3, 2026, GOLDEN WEEK
## Nakameguro. The last of the blossoms, the canal, and the thing Hikari has
## been saving for a day with no school.
##
## Sakura reality check: by May 3 the somei-yoshino are gone. What remains is
## the tail, late-blooming varieties and the falling itself. That is the
## point. This is nochizakura, the leftover-blossom viewing, and it is the
## most honest hanami there is: you go because it is ending, not because it
## is perfect.
################################################################################

label special_day_26_nakameguro:
    $ set_story_day(26)
    call day_transition from _call_day_transition_17
    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Sunday, May third. The middle of Golden Week, which means the whole country has decided to leave at once."
    "I wake to the sound of luggage wheels on the street below. Someone is going somewhere. Everyone is."
    mc "(The city empties for the holiday. That is what Golden Week means: the people who stay are the ones with nowhere else to be.)"

    "Hikari is already dressed. Not school clothes. Real clothes. A coat she has not worn since I got here."
    hikari "Get dressed. We are going out."
    mc "Where?"
    hikari "Nakameguro. The canal."
    mc "I've never heard of it."
    hikari "That is why we are going. You cannot know a place until someone takes you."
    mc "(She says it like a rule she made up on the spot. Maybe she did.)"

    call murakami_daily_ping from _call_murakami_daily_ping_11

    scene bg_kitchen with walk_fade

    mother "Where are you two going?"
    hikari "Out. Somewhere with trees."
    mother "Take your phone. And eat something first."
    father "Golden Week. The trains will be full of people going to see things."
    mc "Like us?"
    father "Like you. You are the only ones I know going to see something."

    scene bg_station with walk_fade

    "The station on a holiday is a different animal. Twice as many people, half as many excuses."
    "A family with a toddler on dad's shoulders. A student with a suitcase the size of a small dog. An old couple holding hands like they are holding the last bench on the train."
    mc "(Everyone is going somewhere beautiful. I am going somewhere beautiful. For once the crowd is on my side.)"

    scene bg_platform with walk_fade

    "The train fills before the doors open. I get pushed gently into a corner and accept it."
    hikari "Hold the rail. Not the strap. The strap is for standing still."
    mc "How do you know all this?"
    hikari "I grew up taking this train. Everyone in this city knows the trains the way you know your own hands."

    scene bg_train_interior with walk_fade

    "The train rocks through neighborhoods I have never seen. Small streets. Shrines. A canal glimpsed between buildings, brown and patient."
    "Then it slows, and the doors open onto a street I do not recognize, and the smell changes."
    mc "(It smells like spring's last afternoon. Green things, wet stone, and something floral that is almost gone.)"

    scene bg_nakameguro with Fade(0.0, 0.0, 1.5)

    "Nakameguro is a canal with trees on both sides. The canal is narrow and dark and moving slowly, and the trees lean over it like they are reading the water."
    "And the blossoms."
    "They are not in bloom. They are ending. What is left is falling. Petals on the water, petals on the railings, petals in the hair of a little girl who does not care that they are almost done."
    "It is almost over. That is the whole point of it."

    menu:
        "Stand under the trees and let them fall on you.":
            "I step under the lowest branch and wait."
            "A petal lands on my shoulder. Then another. Then the air itself seems to be made of them."
            hikari "Don't move."
            mc "I'm not moving. I'm being rained on."
            hikari "That is what it is. The tree is doing its last rain."
            mc "(It is not sad. It is not happy. It is just... is there a word... it is just the thing itself, happening, for the last time this year.)"
            $ log_memory("hikari", "stood under the last sakura while the petals fell like slow rain")
            $ reward_attributes_once("d26_nakameguro_stand", [("grace", "micro")], show="auto")
        "Sit on the railing and watch them float down the canal.":
            "I sit on the stone railing and watch the petals go by."
            "Each one spins once, catches the light, and is gone under the bridge. They do not hurry. They have nowhere to be."
            hikari "They are not falling. They are being carried. The water is doing the work."
            mc "That's almost nicer."
            hikari "It is nicer. The water knows where it is going. They do not."
            mc "(The petals are luckier than I am. They get to be carried by something.)"
            $ log_memory("hikari", "watched the petals float down the canal like slow luck")
            $ reward_attributes_once("d26_nakameguro_float", [("insight", "micro")], show="auto")
        "Take a photo for her. Show her what it looks like.":
            "I take out my phone and frame the canal. The petals, the water, the trees, Hikari's shoulder in the corner."
            hikari "You are taking my picture."
            mc "I'm taking the canal's picture. You're just in it."
            hikari "That is the same thing."
            "I take three. Then I put the phone away."
            mc "(The photo will keep it. But I had to be here to take it. The photo is the receipt, not the meal.)"
            $ log_memory("hikari", "took photos of the canal and pretended she was not the subject")
            $ reward_attributes_once("d26_nakameguro_photo", [("nerve", "micro")], show="auto")

    "We walk the length of the canal. It is maybe four hundred meters, and it takes an hour."
    "People are everywhere. Families on benches, couples under the trees, a man selling paper crowns made of petals for fifty yen."
    "A little girl has petals in her hair like a crown. She is not posing. She is just a girl who has been caught in a beautiful accident."
    hikari "That is the thing about sakura. It does not ask permission. It just falls."
    mc "And then it's gone."
    hikari "Yes. That is why it matters. The tree gives everything at once, all at the end, and then it is done for the year."
    mc "That's not how flowers work. Flowers keep going."
    hikari "Sakura is not like other flowers. It comes all at once, for two weeks, and then it stops. That is what makes it worth waiting for."
    mc "(A choice, made every year, to end.)"

    scene bg_nakameguro with walk_fade

    "Near the end of the canal there is a small bridge, and under it the water is thick with petals, all moving the same slow way."
    "Hikari stops. She picks up a petal that has landed on the railing and holds it out to me."
    hikari "Take it."
    mc "Why?"
    hikari "Because it is the last one. Because you saw it. Because someone should carry a piece of it home."
    "I take it. It is soft and already drying. It weighs almost nothing."
    hikari "It will be gone by tomorrow. That is all right. It was never meant to last."
    mc "(She is giving me a thing that is already ending.)"
    $ log_memory("hikari", "gave me the last sakura petal from the Nakameguro canal")
    $ add_item("sakura_petal")

    scene bg_station with walk_fade

    "The train home is emptier. Everyone has seen their thing. We are the last ones going back."
    "The petals are still falling in my mind. I can see them on the water, on the railing, in her hair."
    hikari "You looked happy today."
    mc "I did?"
    hikari "You were quiet. Quiet is what happy looks like on you."
    mc "(I did not know I had a quiet-happy. She does. She is learning me faster than I am learning the city.)"

    scene bg_home_exterior_day with walk_fade

    "We get home before dark. The house smells like dinner. Mother calls us in."
    mother "Did you see the blossoms?"
    hikari "We saw the last of them."
    mother "Then you saw them at the right time."

    call dinner_open from _call_dinner_open_16

    father "Nakameguro. The canal."
    mc "The canal. The last of the blossoms. Hikari gave me a petal."
    father "A petal."
    mc "It is already drying. It will be gone by tomorrow."
    father "That is the point of petals. They are not supposed to last."
    mc "(He understands. He always understands the thing I am trying to say before I have said it.)"

    call dinner_close from _call_dinner_close_16

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    $ night_desk_line = "the petal on the desk"
    call night_open from _call_night_open_17

    menu:
        "Ask her what she will remember about today.":
            mc "What will you remember?"
            hikari "The petals on the water. The little girl. The way you stood under the tree like you were being rained on."
            mc "Was I?"
            hikari "You were. You did not move. That is the only way to see it properly."
            mc "(She remembers the details. She always does. I am starting to think she is writing me down.)"
            $ log_memory("hikari", "asked what she will remember and she listed the petals, the girl, and me standing still")
            $ reward_attributes_once("d26_night_remember", [("grace", "micro")], show="auto")
        "Tell her about the petal in my pocket.":
            mc "I still have it. In my pocket. It is dry now, but it was soft this morning."
            hikari "Keep it. Not because it will last. Because it was yours."
            mc "It was yours first. You picked it."
            hikari "Then we are sharing it. That is better."
            $ log_memory("hikari", "told her the petal is still in my pocket and she said we are sharing it")
            $ reward_attributes_once("d26_night_petal", [("nerve", "micro")], show="auto")
        "Say nothing. Look at the petal on the desk.":
            "I say nothing. The petal is on the desk, next to the phone, next to the notebook, next to the things that are supposed to last."
            "It does not look out of place. It looks like it belongs there. Like it has always been there, waiting for me to notice."
            hikari "You kept it."
            mc "I kept it."
            hikari "Good. Some things should be kept even though they will not last."
            $ log_memory("hikari", "kept the petal on the desk and she said some things should be kept even though they will not last")
            $ reward_attributes_once("d26_night_keep", [("insight", "micro")], show="auto")

    call night_close from _call_night_close_17

    "The petals are gone now. The canal is just water. The trees are just trees. The city has moved on to the next thing."
    "But I have the petal. It is dry and brown and almost nothing. I do not know what it means. I know it is mine."

    "I turn off the lamp. The dark comes in. The room is not empty. The petal is somewhere in it."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
