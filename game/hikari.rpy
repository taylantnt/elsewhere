################################################################################
## HIKARI — THE RIVER RUN
################################################################################
##
## Hikari is the host sister and the one person who stays. Her arc is not one of
## the five confidant chains in locations.rpy: it is the recurring river run,
## tracked by `hikari_visits` and `sister_affection`. The first run is written
## into `after_school_run` in script.rpy (Day 2) and must not be duplicated
## here. This file holds the other six beats, visits 2 through 7.
##
## The hub's "Walk home with Hikari" row routes to `confidant_visit_hikari`,
## which reads the visit count and jumps to the next run. After the seventh run
## the row falls back to the ordinary walk home (`afternoon_walk_hikari`), so
## the place never runs out of something to do.
##
## The seven beats are the ones in story_treatment.md, "The Run Becomes
## Recurring": the route, the evening he keeps up, the night neither of them
## says anything, the rain, the night she asks him to run somewhere that is not
## home, and the last run. The arc ends on her question, not on an answer.
##
## Reward rule: every answered choice pays one attribute at micro size, one
## option per attribute per menu, and each run closes with a rotating micro
## (the last run closes at small). Hikari's close rewards follow the same
## Grace / Insight / Nerve rotation as the five confidant files.


label confidant_visit_hikari:
    if hikari_visits <= 0:
        # The first run belongs to Day 2. If it was skipped, the ordinary walk
        # home is the honest fallback.
        jump afternoon_walk_hikari
    elif hikari_visits == 1:
        jump hikari_visit_02
    elif hikari_visits == 2:
        jump hikari_visit_03
    elif hikari_visits == 3:
        jump hikari_visit_04
    elif hikari_visits == 4:
        jump hikari_visit_05
    elif hikari_visits == 5:
        jump hikari_visit_06
    elif hikari_visits == 6:
        jump hikari_visit_07
    # Seven runs and the arc's first movement is over. She still walks home.
    jump afternoon_walk_hikari


################################################################################
## VISIT 2 — THE ROUTE
################################################################################
##
## She runs the route from memory, the way the chef makes ramen. He notices she
## cannot look at the river for long. The beat is not the route itself; it is
## that the route is a need she has stopped pretending is a hobby.

label hikari_visit_02:
    $ hikari_run = False
    $ last_afternoon_was_run = True
    play music "audio/Music/(shibuya night?) rain_at_the_crossing.mp3" fadein 2.0

    scene bg_school_gate with walk_fade
    "Hikari is at the gate with her bag already at her feet. She is not on her phone. She is watching the gate like it owes her something."
    hikari "You're late."
    mc "I'm on time."
    hikari "You're late in a way that makes me early."
    mc "(I have known her long enough to know better than to argue with that.)"

    "We walk home without discussing it."
    scene bg_home_exterior_day with walk_fade
    "At the house she goes straight upstairs and comes down in running clothes, and I do the same, and four minutes later we are back at the door."
    $ hikari_run = True
    hikari "Four minutes."
    mc "You didn't time me."
    hikari "I always time you."
    mc "(That is either affection or a warning. With her it is usually both.)"

    scene bg_river with walk_fade
    "The river path is the same as it was the first time. The same fence, the same trees, the same vending machines lit like aquariums."
    "She does not slow down to show me. She assumes I remember."
    "She is right. I do."

    "She names the vending machines as we pass them, the way another person would name stations."
    hikari "This one has the good sports drink. This one is broken on Tuesdays. This one has a cat that sleeps on the compressor."
    mc "A cat."
    hikari "You'll see it in about forty metres."
    "I see it. It does not wake up."
    mc "(She knows the cat. She knows the machines. She knows the cracks in the path without looking down.)"

    menu:
        "How long have you been running this route?":
            mc "How long have you been running this route?"
            hikari "Since before I can remember."
            mc "That's not an answer."
            hikari "It is the only answer I have. I don't remember learning it. I just know it."
            mc "(She says it the way a person says their own address. Not like a memory. Like a fact.)"
            $ reward_attributes_once("hikari_visit_02_how", [("insight", "micro")], show="auto")
        "You know every crack in this path.":
            mc "You know every crack in this path."
            hikari "I know it the way you know the way to your own kitchen in the dark. You don't think about it. You just go."
            mc "That's a strange thing to be proud of."
            hikari "I'm not proud of it. I'm just telling you what it is."
            $ reward_attributes_once("hikari_visit_02_cracks", [("grace", "micro")], show="auto")
        "What are you training for?":
            mc "What are you training for?"
            hikari "Nothing."
            mc "Nothing?"
            hikari "There's no race. There's just the part where I'm not in the house."
            mc "(She says it lightly. It does not land lightly.)"
            $ reward_attributes_once("hikari_visit_02_training", [("nerve", "micro")], show="auto")

    "We run the first kilometre without talking. My legs complain. Her legs do not."
    "The path bends left at the second bridge and she takes the bend without looking. I look. There is nothing to see. That is the point."

    "At the bridge she stops. She puts her hands on the railing and looks down at the water, and then she looks away from it, the way a person looks away from a light that is too bright."
    mc "(She doesn't look at the river for long. She looks at the path. She looks at the next turn. She looks at everything except the thing she came here for.)"

    hikari "I used to think I ran because I liked it."
    mc "And now?"
    hikari "Now I think I need it. Those are different things."
    mc "What's the difference?"
    hikari "One of them is a choice."

    menu:
        "What would you do if you couldn't run?":
            mc "What would you do if you couldn't run?"
            hikari "..."
            hikari "I don't know. I've never had to find out."
            mc "(For a second she looks younger than she does in the house. Then it is gone.)"
            hikari "That scares me more than it should."
            $ reward_attributes_once("hikari_visit_02_cant", [("insight", "micro")], show="auto")
        "You don't have to tell me.":
            mc "You don't have to tell me."
            hikari "I know."
            "She looks at me then, properly, the way she does when she is deciding whether someone is worth the trouble."
            hikari "That's why I'm telling you."
            $ reward_attributes_once("hikari_visit_02_donttell", [("grace", "micro")], show="auto")
        "Then let's run somewhere you don't know.":
            mc "Then let's run somewhere you don't know."
            hikari "Somewhere I don't know."
            mc "You said you know this route without thinking. So take a different one."
            "She smiles. It is not a happy smile. It is the smile of someone who has been asked a question she has been avoiding."
            hikari "Not tonight. But ask me again."
            $ reward_attributes_once("hikari_visit_02_elsewhere", [("nerve", "micro")], show="auto")

    "We finish the route. She points out the place where the path floods in summer, the stretch where the lamps are out, the vending machine that gives two cans if you press the button twice."
    "I press it twice. It gives two cans. She takes one without saying thank you, which is how I know she expected it."

    $ hikari_visits = max(hikari_visits, 2)
    $ add_affection("sister", 1)
    $ remember("hikari", "showed him her river route and admitted she needs it, not just likes it")
    $ queue_message("hikari", "The route is not the point. The point is that I know it without looking. Don't ask me why that bothers me.", day="yesterday")
    $ reward_attributes_once("hikari_visit_02_close", [("grace", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    "At the house gate she stops with her key in her hand."
    hikari "Same time next week?"
    mc "Same time next week."
    hikari "Good. I wasn't asking."
    "She goes inside. The kitchen light is on. I stand at the gate for a moment longer than I need to."
    $ hikari_run = False
    return


################################################################################
## VISIT 3 — THE EVENING HE KEEPS UP
################################################################################
##
## He matches her pace for ten minutes, and she is surprised enough to say so.
## What it costs her is that he sees her face when she is not performing.

label hikari_visit_03:
    $ hikari_run = True
    $ last_afternoon_was_run = True
    play music "audio/Music/(shibuya night?) rain_at_the_crossing.mp3" fadein 2.0

    scene bg_school_gate with walk_fade
    "She is already in running clothes when I get to the gate. She has changed at school, which she has never done before."
    mc "You changed here."
    hikari "I had a free period."
    mc "You had a free period and you used it to be ready to run."
    hikari "I used it to be ready to leave. The running is incidental."
    mc "(She says it like a joke. I am starting to hear the difference between her jokes and the things she means.)"

    "We do not go home. She takes the path from the school directly to the river, and it is shorter than the way I know, and I do not ask how she found it."

    scene bg_river with walk_fade
    "She sets a faster pace tonight. Not by much. Just enough that I have to decide whether to say something."
    "I don't say anything. I run."
    "The first ten minutes are my legs arguing with me. Then the argument stops. The path goes easy under my feet, and I am still beside her."
    "She glances over. Once. Twice. The third time she slows down."
    hikari "You're still here."
    mc "I'm still here."
    hikari "Huh."

    menu:
        "Why does that surprise you?":
            mc "Why does that surprise you?"
            hikari "Because nobody keeps up."
            mc "Maybe they didn't try."
            hikari "They tried. I didn't let them."
            mc "(She says it without apology. It is not a boast. It is a confession.)"
            $ reward_attributes_once("hikari_visit_03_why", [("insight", "micro")], show="auto")
        "I'm glad you let me.":
            mc "I'm glad you let me."
            hikari "Don't make it a thing."
            mc "Too late."
            "She looks away, but she is smiling. It is the first smile tonight that does not look like it costs her something."
            $ reward_attributes_once("hikari_visit_03_glad", [("grace", "micro")], show="auto")
        "Then don't slow down on my account.":
            mc "Then don't slow down on my account."
            hikari "You're going to regret that."
            mc "I regret it already."
            "She speeds up. I keep up. I do not know how. The river goes past us in long dark strips."
            $ reward_attributes_once("hikari_visit_03_slowdown", [("nerve", "micro")], show="auto")

    "We stop at the vending machine. She buys the same energy drink, and this time she buys two without asking."
    "Her hands are shaking. Just slightly. Not from the run."
    mc "(She is not out of breath. She is not cold. She is afraid of something, and she is trying not to let me see it.)"

    hikari "I don't know what to do when someone stays."
    mc "What do you mean?"
    hikari "People leave. That's what people do. I'm not used to the other thing."

    menu:
        "What other thing?":
            mc "What other thing?"
            hikari "The part where they're still there in the morning."
            mc "(She says it like a fact she has tested. More than once.)"
            $ reward_attributes_once("hikari_visit_03_other", [("insight", "micro")], show="auto")
        "You don't have to do anything.":
            mc "You don't have to do anything."
            hikari "That's not true. I have to not run away. That's harder than it sounds."
            mc "(She says it to the can in her hand, not to me.)"
            $ reward_attributes_once("hikari_visit_03_nothing", [("grace", "micro")], show="auto")
        "I'm not going anywhere.":
            mc "I'm not going anywhere."
            hikari "..."
            "She looks at me for a long time. The river fills the silence."
            hikari "Don't promise that. Just be here now."
            mc "(It is the most honest thing she has ever asked me for.)"
            $ reward_attributes_once("hikari_visit_03_anywhere", [("nerve", "micro")], show="auto")

    "We sit on the wall. She drinks half her can and hands it to me."
    hikari "Here. You look like you need it more than me."
    mc "I just ran ten minutes at your pace."
    hikari "That's what I said."
    "The can is warm from her hand. I drink."
    "She leans her shoulder against mine. Just for a second. Then she sits up straight."
    hikari "Don't tell anyone I did that."
    mc "Did what?"
    hikari "Exactly."

    $ hikari_visits = max(hikari_visits, 3)
    $ add_affection("sister", 1)
    $ remember("hikari", "kept up with her for ten minutes and saw the face she makes when she is not performing")
    $ queue_message("hikari", "You kept up. I didn't think anyone would. I don't know what to do with that. Give me a week.", day="yesterday")
    $ reward_attributes_once("hikari_visit_03_close", [("insight", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    "At the gate she stops and looks at me."
    hikari "You kept up."
    mc "You let me."
    hikari "..."
    "She goes inside. The kitchen light comes on. I stand there until it does."
    $ hikari_run = False
    return


################################################################################
## VISIT 4 — THE NIGHT NEITHER OF THEM SAYS ANYTHING
################################################################################
##
## They run, they stop, they drink, they walk home in silence. It is the most
## honest either of them has been. The beat is the silence itself.

label hikari_visit_04:
    $ hikari_run = False
    $ last_afternoon_was_run = True
    play music "audio/Music/(shibuya night?) rain_at_the_crossing.mp3" fadein 2.0

    scene bg_school_gate with walk_fade
    "She is at the gate. She does not say anything. I do not say anything either."
    "We walk home without discussing it."
    "Not because there is nothing to say. Because there is too much, and neither of us wants to be the one who starts."

    scene bg_home_exterior_day with walk_fade
    "At the house she changes without a word. I change without a word. We meet in the yard."
    $ hikari_run = True
    "She does not time me. I do not ask why."

    scene bg_river_night with walk_fade
    "The run is quiet. Our footsteps find the same rhythm without either of us trying."
    "The river is loud. The city is far away. The path is a dark line between them."
    "We stop at the second bridge. She sits on the railing. I sit beside her."
    "She has two cans in her bag. She hands me one without looking."
    "I open it. She opens hers. We drink."
    "The silence is not awkward. It is a room we are both standing in."

    menu:
        "Say something.":
            mc "I'm going to say something, and you can tell me to stop."
            hikari "Don't."
            mc "..."
            hikari "Not yet."
            mc "(She does not look at me. Her hand is tight around the can.)"
            $ reward_attributes_once("hikari_visit_04_say", [("nerve", "micro")], show="auto")
        "Leave the silence alone.":
            "I let it be. The river fills the space where a sentence would go."
            "Her shoulders drop. She did not know she was holding them up."
            hikari "Thank you."
            mc "(She says it without looking at me. That is how I know she means it.)"
            $ reward_attributes_once("hikari_visit_04_silence", [("grace", "micro")], show="auto")
        "Listen to the river.":
            "I listen. The water has a rhythm. It is not a word, but it is not nothing."
            mc "It sounds like it's counting something."
            hikari "It does that."
            mc "You've noticed."
            hikari "I've had a lot of time to notice."
            $ reward_attributes_once("hikari_visit_04_river", [("insight", "micro")], show="auto")

    hikari "This is the part I like."
    mc "What part?"
    hikari "The part where nobody has to be anything."
    "She looks at me. Her face is open in a way I have not seen it. There is no performance in it. There is no host sister. There is just a person, tired, sitting on a bridge."
    hikari "I don't have to be the one who knows where everything is out here. I can just be tired."
    mc "You can be tired with me."
    hikari "I know."
    mc "Then what's wrong?"
    hikari "That's the problem."

    menu:
        "Then keep me.":
            mc "Then keep me."
            "She laughs. It is surprised out of her, not performed."
            hikari "That's not how it works."
            mc "Why not?"
            hikari "Because people aren't things you keep."
            mc "(She is still smiling. I decide not to point that out.)"
            $ reward_attributes_once("hikari_visit_04_keep", [("nerve", "micro")], show="auto")
        "You don't have to perform with me.":
            mc "You don't have to perform with me."
            hikari "I know."
            "She looks at the water."
            hikari "I've been performing for so long I don't know where the performance ends."
            mc "(She says it quietly. It is the most honest thing she has said to me.)"
            $ reward_attributes_once("hikari_visit_04_perform", [("grace", "micro")], show="auto")
        "What would you do if you didn't have to be anything?":
            mc "What would you do if you didn't have to be anything?"
            hikari "..."
            "She is quiet for a long time. The river counts something. The city glows behind us."
            hikari "I'd stay. Right here. I wouldn't go home."
            mc "(The answer is so simple that it takes me a moment to understand how much it costs her.)"
            $ reward_attributes_once("hikari_visit_04_anything", [("insight", "micro")], show="auto")

    "We walk home in silence. The same silence, but it is different now. It has a shape. It has a door in it."

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    "At the gate she stops. The kitchen light is on. The amado is closed."
    hikari "Thank you for not filling it."
    mc "I didn't know I was supposed to."
    hikari "That's why."
    "She touches my sleeve. Just once. Then she goes inside."

    $ hikari_visits = max(hikari_visits, 4)
    $ add_affection("sister", 1)
    $ remember("hikari", "sat with him in silence on the bridge and admitted she does not know where the performance ends")
    $ queue_message("hikari", "I meant what I said. I don't say that often. Don't make it weird.", day="yesterday")
    $ reward_attributes_once("hikari_visit_04_close", [("nerve", "micro")], show="card")

    "I stand at the gate for a while after she goes in. The kitchen light stays on. The amado does not open."
    $ hikari_run = False
    return


################################################################################
## VISIT 5 — THE RAIN
################################################################################
##
## The bridge in the rain, and the first true thing she says about the house.
## The amado is the crack in the world she can hear but cannot name.

label hikari_visit_05:
    $ hikari_run = True
    $ last_afternoon_was_run = True
    play music "audio/Music/(shibuya night?) rain_at_the_crossing.mp3" fadein 2.0

    scene bg_school_gate with walk_fade
    "She is already in running clothes when I reach the gate. So am I. Neither of us mentions it."
    "The rain starts before we reach the river. She does not turn back. Neither do I."

    scene bg_river_night with walk_fade
    "By the time we are on the path we are both soaked. She is laughing. It is a real laugh, the kind that surprises her."
    hikari "You look like a drowned cat."
    mc "You look like a drowned cat."
    hikari "I look like a cat that chose to be in the rain. There's a difference."
    mc "(She is right. She always looks like she chose whatever is happening to her. I am starting to wonder how much of that is true.)"

    "The path is empty. The river is louder in the rain. The vending machines glow like small rooms with the doors left open."
    "We stop under the bridge. The rain sounds like static on the roof. She sits on the concrete ledge and pulls her knees up."
    "She is still smiling. Then she is not."

    hikari "My father closes the amado every night."
    mc "The shutters?"
    hikari "The metal ones. Left side first. Then the right. Then he checks the latch twice."
    "She says it slowly, the way a person recites something they have heard a thousand times."
    hikari "I used to think that was what safety sounded like."
    mc "And now?"
    hikari "Now I hear it and I think: who taught him to do it in that order?"

    menu:
        "What changed?":
            mc "What changed?"
            hikari "I don't know. That's the problem. Nothing changed. It's the same sound it's always been."
            hikari "I'm the one who started hearing it."
            mc "(She looks at her hands. The rain fills the space where the rest of the answer should be.)"
            $ reward_attributes_once("hikari_visit_05_changed", [("insight", "micro")], show="auto")
        "It sounds like a good memory.":
            mc "It sounds like a good memory."
            hikari "It is."
            mc "Then why does it bother you?"
            hikari "Because good memories don't usually make me feel like I'm missing something."
            $ reward_attributes_once("hikari_visit_05_memory", [("grace", "micro")], show="auto")
        "Do you want to get out of the rain?":
            mc "Do you want to get out of the rain?"
            hikari "No."
            mc "You're soaked."
            hikari "I know. I want to stand here until it stops. Is that stupid?"
            mc "Yes."
            hikari "Good. Then I'm not the only one."
            $ reward_attributes_once("hikari_visit_05_rain", [("nerve", "micro")], show="auto")

    "The rain gets heavier. She does not move. I do not move."
    "She looks past me, at the street beyond the bridge, at the houses with their lights on."
    hikari "Does this street look right to you?"
    mc "What do you mean?"
    hikari "I don't know. Just... does it look like a street that was here before you got here?"
    mc "(It is a strange question. It is stranger because she is not joking.)"

    menu:
        "It looks like a street.":
            mc "It looks like a street."
            hikari "That's what I thought."
            "She does not sound relieved. She sounds like someone who has just confirmed a suspicion."
            $ reward_attributes_once("hikari_visit_05_street", [("insight", "micro")], show="auto")
        "It looks like home.":
            mc "It looks like home."
            hikari "That's a good answer."
            "She looks at me. The rain runs down her face and she does not wipe it away."
            hikari "I don't know if it's true."
            $ reward_attributes_once("hikari_visit_05_home", [("grace", "micro")], show="auto")
        "No. Something's off.":
            mc "No. Something's off."
            hikari "..."
            "She goes very still. The rain keeps falling."
            hikari "You feel it too."
            "It is not a question."
            $ reward_attributes_once("hikari_visit_05_off", [("nerve", "micro")], show="auto")

    "She takes my hand. Her grip is too tight for the rain."
    "We walk home like that, hand in hand, until the gate."

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    "At the gate she lets go. The amado is closing. Left side first. Then the right. Then the latch, twice."
    hikari "Don't tell them I said that."
    mc "I won't."
    hikari "I know."
    "She goes inside. I stand in the rain until the kitchen light comes on."

    $ hikari_visits = max(hikari_visits, 5)
    $ add_affection("sister", 2)
    $ remember("hikari", "told him the amado sounds wrong and asked if the street looked right")
    $ queue_message("hikari", "The amado. He closes it left side first. Every night. I don't know why I noticed. I don't know why I can't stop noticing.", day="yesterday")
    $ reward_attributes_once("hikari_visit_05_close", [("grace", "micro")], show="card")
    $ hikari_run = False
    return


################################################################################
## VISIT 6 — THE NIGHT SHE ASKS HIM TO RUN SOMEWHERE THAT IS NOT HOME
################################################################################
##
## She takes him to the part of the river she keeps for herself. The vending
## machine with no cable is the first leak she lets him see on purpose. She
## almost tells him what makes the house feel small, and does not.

label hikari_visit_06:
    $ hikari_run = True
    $ last_afternoon_was_run = True
    play music "audio/Music/(shibuya night?) rain_at_the_crossing.mp3" fadein 2.0

    scene bg_school_gate with walk_fade
    "She is waiting at the gate with her bag over one shoulder and a look I have not seen before. She is already in running clothes."
    mc "Where are we going?"
    hikari "Not home."
    mc "I can see that."
    hikari "Good."
    "She turns and walks. I follow. I changed before I came. Her message said not home and nothing else, which was enough."

    scene bg_river_night with walk_fade
    "She takes a turn I have never seen her take. The path narrows. The houses fall away. The river widens."
    "We run until the path ends at a concrete platform above the water. There is a bench, a vending machine with no light, and a bridge in the distance that I do not recognize."
    "The city is a glow behind us. The river is black. The vending machine is humming."
    mc "Where are we?"
    hikari "Nowhere. That's the point."

    "She sits on the bench. I sit beside her. The vending machine hums like something asleep."
    hikari "I come here when the house feels too small."
    mc "(She says it like a confession. She does not look at me.)"

    menu:
        "Why here?":
            mc "Why here?"
            hikari "Because it doesn't belong to anyone. Not the house. Not the school. Not even the city."
            hikari "It's just a place."
            mc "(She says it like a place is a rare thing. Maybe it is.)"
            $ reward_attributes_once("hikari_visit_06_why", [("insight", "micro")], show="auto")
        "It's beautiful.":
            mc "It's beautiful."
            hikari "I never thought of it that way."
            "She looks around, as if seeing it for the first time."
            hikari "I just thought of it as far."
            $ reward_attributes_once("hikari_visit_06_beautiful", [("grace", "micro")], show="auto")
        "What makes the house feel small?":
            mc "What makes the house feel small?"
            hikari "..."
            "She looks at the water. The vending machine hums."
            hikari "That's the question, isn't it."
            mc "(She does not answer it. She does not have to. The fact that she does not is the answer.)"
            $ reward_attributes_once("hikari_visit_06_small", [("nerve", "micro")], show="auto")

    "She gets up and walks to the vending machine. She presses a button. Nothing happens. She presses it again."
    hikari "It's been like this for a month. I keep coming back to see if it works."
    mc "The light's out."
    hikari "There is no light."
    "I look. There is no cable. There is no outlet. The machine is humming."
    mc "(It is not plugged into anything. It is still humming.)"
    hikari "That's a metaphor, isn't it."
    mc "For what?"
    hikari "For me. Standing in front of something that used to work and waiting for it to light up."

    menu:
        "You checked?":
            mc "You checked? The machine?"
            hikari "The first time. There's no cable. There's no outlet. It just hums."
            mc "And you kept coming back."
            hikari "I keep coming back to a lot of things."
            $ reward_attributes_once("hikari_visit_06_checked", [("insight", "micro")], show="auto")
        "Then we don't need it to work.":
            mc "Then we don't need it to work."
            hikari "No. I guess we don't."
            "She smiles. It is a small smile, but it is hers."
            $ reward_attributes_once("hikari_visit_06_work", [("grace", "micro")], show="auto")
        "Take me further.":
            mc "Take me further."
            hikari "Further?"
            mc "Past the platform. Past the bridge. Somewhere you haven't shown me."
            "She looks at the dark path beyond the platform. For a second she looks afraid."
            hikari "Not tonight."
            mc "Why not?"
            hikari "Because I don't know what's out there."
            "A pause. The river moves."
            hikari "That's a lie. I do know. That's why not tonight."
            $ reward_attributes_once("hikari_visit_06_further", [("nerve", "micro")], show="auto")

    "She sits back down. She leans her head on my shoulder. I do not move."
    "The vending machine hums. The river moves. The city glows behind us like something we are not allowed to touch."
    "She is quiet for a long time."
    hikari "It's not the house."
    mc "What isn't?"
    hikari "The thing I'm running from."
    "She does not say anything else. I do not ask."

    $ hikari_visits = max(hikari_visits, 6)
    $ add_affection("sister", 1)
    $ remember("hikari", "took him to the part of the river she keeps for herself and said the house was not what made it feel small")
    $ queue_message("hikari", "I almost told you tonight. I'm sorry I didn't. I'm not sorry I brought you there.", day="yesterday")
    $ reward_attributes_once("hikari_visit_06_close", [("insight", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    "We walk back without talking. At the gate she stops."
    hikari "You didn't ask again."
    mc "You said it wasn't the house. The rest sounded like yours to tell."
    hikari "I know."
    "She looks at the house. The porch light flickers once, then stays on."
    hikari "Thank you."
    "She goes inside."
    $ hikari_run = False
    return


################################################################################
## VISIT 7 — THE LAST RUN
################################################################################
##
## She is faster than she has ever been and he cannot keep up. She asks the
## question the whole arc has been walking toward. The scene ends on the
## question, not an answer; the threshold belongs to Act 3/4.

label hikari_visit_07:
    $ hikari_run = True
    $ last_afternoon_was_run = True
    play music "audio/Music/(shibuya night?) rain_at_the_crossing.mp3" fadein 2.0

    scene bg_school_gate with walk_fade
    "She is already at the gate when I get there. She is in running clothes, and so am I. She is not stretching. She is not waiting. She is looking at the sky."
    mc "You're early."
    hikari "You're late."
    mc "I'm on time."
    hikari "Not tonight."
    "She does not explain. She turns and starts walking, and I follow."
    "She starts running before we reach the corner. I do not have time to ask why."

    scene bg_river_night with walk_fade
    "She is faster than she has ever been. Not by a little. By enough that I lose sight of her at the first bend."
    "I try to keep up. I really try. My legs are burning. My breath is a ragged thing. The path keeps going."
    "By the time I reach the second bridge, she is standing at the railing, looking at the water."
    "The city is quiet. The moon is out. The river is a long black sentence."
    mc "I couldn't keep up."
    hikari "I know."
    mc "You didn't wait."
    hikari "I did. You just didn't see me."
    "She does not turn around. Her hands are on the railing. The water goes past underneath."
    hikari "Don't you ever feel like we've done this before?"

    menu:
        "Yes.":
            mc "Yes."
            "She turns. Her face is unreadable."
            hikari "You do?"
            mc "I don't know. But when you said it, I did."
            mc "(It is the truest thing I have said to her, and I do not know what it means.)"
            $ reward_attributes_once("hikari_visit_07_yes", [("nerve", "micro")], show="auto")
        "What do you mean?":
            mc "What do you mean?"
            hikari "This. The river. The run. You. Me. All of it."
            hikari "Like we're doing it again, and I'm the only one who remembers the first time."
            mc "(The water goes past. The moon does not move.)"
            $ reward_attributes_once("hikari_visit_07_mean", [("insight", "micro")], show="auto")
        "I don't know. But I'm here.":
            mc "I don't know. But I'm here."
            "She looks at me for a long time. The river fills the silence."
            hikari "That's the best answer anyone's given me."
            mc "(I do not know if that is a compliment or a confession. With her it is usually both.)"
            $ reward_attributes_once("hikari_visit_07_here", [("grace", "micro")], show="auto")

    hikari "I keep thinking if I run fast enough, I'll get to the part where it makes sense."
    mc "The route?"
    hikari "The route. The house. My father closing the amado. You."
    "She laughs. It is not a joke."
    hikari "I don't think there is a part where it makes sense. I think I've been running the wrong way."
    mc "(She says it to the water. She does not look at me. It is the most afraid I have ever seen her.)"

    menu:
        "Then stop running.":
            mc "Then stop running."
            hikari "I don't know how. I've been running since before I can remember."
            mc "(She says it simply. It is not a refusal. It is a fact.)"
            $ reward_attributes_once("hikari_visit_07_stop", [("grace", "micro")], show="auto")
        "Then we run the other way.":
            mc "Then we run the other way."
            hikari "You'd come with me?"
            mc "Yes."
            hikari "You don't even know where it goes."
            mc "No."
            "She looks at me. Something in her face changes. It is not hope. It is something older and more careful."
            hikari "Okay."
            $ reward_attributes_once("hikari_visit_07_otherway", [("nerve", "micro")], show="auto")
        "What are you afraid of?":
            mc "What are you afraid of?"
            hikari "..."
            "She is quiet for a long time. The river counts something. The moon does not answer."
            hikari "That I already know how this ends."
            mc "(She says it without looking at me. I do not ask what she means. I am not sure I want to know.)"
            $ reward_attributes_once("hikari_visit_07_afraid", [("insight", "micro")], show="auto")

    "She takes a step toward me. The railing is behind her. The water is below. The city is far away."
    hikari "If I ever ask you to run somewhere that isn't home, say yes."
    mc "I will."
    hikari "Don't promise. Just remember."
    "She smiles. It is the smile from the first run, the one she gave me when she said I was not unfit, just new."
    hikari "Race you back."
    "She runs. I do not catch her. I do not think I was supposed to."

    $ hikari_visits = max(hikari_visits, 7)
    $ hikari_run_finished = True
    $ add_affection("sister", 2)
    $ remember("hikari", "asked if they had done this before and made him promise to say yes if she ever asked him to run somewhere that isn't home")
    $ queue_message("hikari", "I meant what I said. About running somewhere that isn't home. I'm not asking yet. I'm just putting it somewhere you can find it.", day="yesterday")
    $ reward_attributes_once("hikari_visit_07_close", [("insight", "small")], show="card")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    "She is already inside when I get to the gate. The kitchen light is on. The amado is closed."
    "I stand there, breathing hard, and the river is still going one way and coming back the same way."
    mc "(She asked me if I ever feel like we've done this before.)"
    mc "(I did not know what to say. She did not expect me to.)"
    mc "(But I keep thinking about the first run. The way she said same time next week. The way she said it like she already knew.)"
    "The porch light flickers once. Then it stays on."
    "I go inside."
    $ hikari_run = False
    return
