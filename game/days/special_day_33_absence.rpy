################################################################################
## DAY 33: SUNDAY, MAY 10, 2026
## The professor is absent. Hikari takes him to Shibuya. The arcade is a trap.
################################################################################

label special_day_33_absence:
    $ set_story_day(33)
    call day_transition from _call_day_transition_21

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Sunday. The fifth week of the term. The professor's office hours were supposed to be today."
    "I wake up with the notebook still on my desk. The corridor map. The doors that are not in order."
    mc "(He said bring one question. I brought one. The corridor. The question I cannot answer.)"

    "My phone buzzes."

    if "tanaka" in wire_unlocked:
        $ run_chat("tanaka", [
            {"them": "Afternoon shift today. Four hours. You in?", "options": [
                {"label": "\"I have plans.\"",
                 "send": "I have plans.",
                 "them": ["Plans are good. Plans are also expensive."]},
                {"label": "\"Maybe later.\"",
                 "send": "Maybe later.",
                 "them": ["Later is a time that does not exist."]},
            ]},
        ])
        mc "(Later is a time that does not exist. I have learned that much.)"
    else:
        $ run_chat("hikari", [
            {"them": "Are you still thinking about the professor?", "options": [
                {"label": "\"Yes.\"",
                 "send": "Yes.",
                 "them": ["Then you should stop. The answer will not come from him."]},
                {"label": "\"I don't know.\"",
                 "send": "I don't know.",
                 "them": ["That is the first honest answer you have given me all week."]},
            ]},
        ])
        mc "(Not from him. Then from where. The not-knowing is starting to feel like a place I live.)"

    call murakami_daily_ping from _call_murakami_daily_ping_15

    scene bg_kitchen with walk_fade

    "The kitchen is quiet. The plum is gone. There is nothing in its place."
    father "You are not going to school today?"
    mc "I am going. The professor's office hours were supposed to be today."
    father "On a Sunday?"
    mc "He said so. I want to see for myself."
    father "And if they are not?"
    mc "Then I will come straight home."
    father "Then you have an afternoon."
    mc "I know."
    father "Use it. Do not waste it on the sofa."
    mother "He is right. You have been sitting too much lately."
    hikari "I was going to suggest something."
    father "What?"
    hikari "Shibuya. The observation deck. He needs to see the city from above."
    father "From above?"
    hikari "From above. He has been staring at that map all week. He needs to see the city."
    mc "(She is talking about the city. She is also talking about me. I do not know which one she means.)"

    scene bg_home_exterior_day with walk_fade
    # Sunday house wear ends at the door. Hikari changes into her usual
    # outside clothes for Shibuya; she changes back once we are home again.
    $ sunday_at_home = False
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The walk to the station is a walk I have done a hundred times. The crack. The shrine. The gate."
    hikari "You are quiet."
    mc "I am thinking about the professor."
    hikari "You are always thinking about the professor."
    mc "I have to ask him something."
    hikari "Then ask him. And if he is not there, we will ask the city."
    hikari "Shibuya. The observation deck. It is free if you know where to go. I will show you."
    mc "I thought Shibuya Sky was paid."
    hikari "It is. But there is a rooftop in Hikarie that is not. It is not as famous. It is better."
    mc "Better how?"
    hikari "Fewer people. Better view. No queue. You will see."

    scene bg_station with walk_fade
    scene bg_platform with walk_fade
    scene bg_train_interior_day with walk_fade

    "The train is not crowded. The sleeping man is not on this train either."
    mc "(He is not on this train. I am starting to think he never was.)"

    scene bg_school_gate with Fade(0.0, 0.0, 1.5)
    play music "audio/Music/school.mp3" fadein 1.5
    $ phone_map_visit("school")
    scene bg_campus_interior with walk_fade
    scene bg_department_hall with walk_fade

    "The professor's office. Same room. Same desk. Same wall of books."
    "There is a note on the door. It is handwritten. It says: 'Office hours cancelled today. Come back next class.'"
    "The red pen is not on the desk. The tea is not made. The room is just a room."
    mc "(He is not here. The question is still here. The corridor is still here. I am still here.)"

    "I turn around and walk out. Hikari is waiting in the hallway."
    hikari "Well?"
    mc "He is not here."
    hikari "I know. I saw the note."
    mc "You saw the note?"
    hikari "I saw the note. I also saw you standing there reading it."
    mc "I was deciding what to do."
    hikari "You were deciding whether to be disappointed or relieved."
    mc "I was deciding both."
    hikari "Then decide quickly. We have a train to catch."

    scene bg_campus_interior with walk_fade
    scene bg_school_gate with walk_fade
    scene bg_station with walk_fade
    scene bg_platform with walk_fade
    scene bg_train_interior with walk_fade

    scene bg_shibuya_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "Shibuya is loud. Today it sounds like it is listening."
    "The crossing is already full of people. The light is changing. The crowd is moving like water."
    hikari "This is the scramble. Everyone crosses at once. Nobody waits."
    mc "How does that work?"
    hikari "It does not. That is the point. You just walk and the crowd moves around you."
    "We stand at the edge of the crossing. The light changes. The crowd surges forward."
    "I am carried along by the tide. Hikari is beside me, but she is not holding my hand. She watches the crowd."
    mc "(I am in the middle of a crowd. I am also alone.)"

    "We walk to Hikarie. The building is tall and clean. The rooftop is free."
    "We take the elevator to the top. The doors open onto pale sky and a grid of people."
    "The crossing is below us, a grid of people moving in patterns. The buildings are small from up here. The sky is wide and pale."
    mc "Why did you bring me here?"
    hikari "Because up here you can see the patterns. Down there you are inside them."
    "We stand at the railing. The wind is cold. The city is loud even from here."
    hikari "Look at the crossing. Everyone is moving. Nobody is standing still."
    mc "What does that mean?"
    hikari "Nobody's lost up here. That's what I wanted you to see."
    mc "(The professor is not here. The question is not here. I am here. And I am going somewhere. I do not know where.)"

    menu:
        "[tag_insight] Rank 2: Tell her you have been walking like that all afternoon." if has_attribute("insight", 2):
            mc "You said I am looking for the answer. I did not tell you that."
            hikari "You have been walking like that all afternoon."
            mc "Then you have been reading me the way you read the crowd."
            $ reward_attributes_once("day33_shibuya_read", [("insight", "micro")], show="auto")
        "Ask Hikari what she sees." :
            mc "What do you see?"
            hikari "Some people are looking for something. Some are running from something. Some are just walking because that is what you do."
            hikari "You are looking for the answer. You are running from the question. You are walking because you do not know what else to do."
            mc "(She is not guessing. She knows. I did not know she could do that.)"
            $ reward_attributes_once("day33_shibuya_see", [("insight", "micro")], show="auto")
        "Ask her to show him the nightlife." :
            mc "Show me the nightlife. The part of Shibuya that is not for tourists."
            hikari "The nomiya. The girls waiting near Hachiko. The men asking girls for drinks."
            mc "I am not good at that."
            hikari "You do not have to be good at it. You just have to be there."
            $ reward_attributes_once("day33_shibuya_night", [("nerve", "micro")], show="auto")
        "Ask about the corridor." :
            mc "The doors in the corridor. They are not in order."
            hikari "Then stop counting them. You have been reading that map like it owes you an answer."
            hikari "The answer is not in the hallway. It is out here. In the city. In the crowd. In the arcade."
            mc "(Out here. Not in the hallway. That is something. It is not an answer, but it is a direction.)"
            $ reward_attributes_once("day33_shibuya_answer", [("grace", "micro")], show="auto")

    "The light goes flat, then gold on one side of the building."
    hikari "Come on. I want to show you the nightlife. The part that is not in the guidebooks."
    mc "I am not sure I am ready."
    hikari "Nobody is ready for this. That is why it is worth doing."

    scene bg_shibuya_dusk with walk_fade
    play music "audio/Music/(shibuya night?) rain_at_the_crossing.mp3" fadein 2.0
    "We walk down from Hikarie. The streets are getting louder. The lights are coming on."
    "We pass Center Gai. The arcades are full of people. The restaurants are full of smoke and noise."
    "We pass Hachiko. The statue is surrounded by people. Some are taking photos. Some are just standing there."
    hikari "Those girls over there. The ones in the corner. They are waiting for someone."
    mc "For who?"
    hikari "For anyone. That is the point. They are not waiting for a specific person. They are waiting for the night to happen."
    hikari "Hachiko is a meeting spot. It is also where the nanpa men come looking."
    mc "Nanpa?"
    hikari "Men who stop girls they do not know. Right here in the street. They ask for a drink, or for a date."
    mc "Has anyone ever... done that to you?"
    hikari "Sure. You say no and they leave. That is how it works."
    hikari "Some of them do not leave. They keep talking. They walk beside you for a little while."
    mc "(She says it like she is talking about the weather. I do not know if she is used to it.)"
    hikari "Do not worry. I know how to say no."
    mc "(That is not what worries me.)"
    hikari "Some nights are sad. Some are free. Most are both."

    "We keep walking. The streets get narrower. The lights get brighter. The noise gets louder."
    "We turn a corner. There is an arcade. A big one. The sign says 'GAME CENTER' in bright letters."
    hikari "In there. Loudest place in the building."
    mc "I have never been any good at these."
    hikari "Then be bad at it with me."

    scene bg_arcade_entrance with walk_fade
    # The arcade track plays as we enter and explore, but is paused during the
    # claw machine scene so the machine SFX land on silence. It resumes for the
    # games and the walk back out, then night_street() takes over on the way home.
    play music "audio/Music/arcade.mp3" fadein 2.0
    "The arcade is big. It is loud. It is bright. The machines are everywhere."
    "Claw machines. Racing games. Shooting games. Dance games."
    "There are people everywhere. Some are serious. Some are laughing. Some are just watching."
    hikari "This is where you can be anyone. For a little while."
    mc "I am already someone. I am not sure I want to be someone else."
    hikari "You are not being someone else. You are being yourself in a place that does not care who you are."

    "Hikari stops mid-step. She is staring at something near the claw machines."
    hikari "Wait. Is that...?"
    # The bear is the whole picture here. Hide her side portrait for the beat so
    # the two do not stack, and show the scaled-down plushie on its own.
    $ hikari_portrait_hidden = True
    show plushie at center
    hikari "It is. It is him. Kuma. The Lucky Bear."
    hikari "I want it."
    mc "You know that bear?"
    hikari "Everyone knows Kuma. He is from an anime. He is lucky. He is perfect."
    mc "(She is not even trying to hide it.)"
    hide plushie
    $ hikari_portrait_hidden = False

    scene bg_arcade_claw with walk_fade
    # Pause the arcade BGM for the claw machine scene so the coin/machine SFX
    # and the beats of silence between them are not buried under music.
    "We end up at the claw machines. There are dozens of them. Each one has a different prize."
    hikari "They are the most honest games. You put in money. You try. You fail. You try again."
    "Hikari stops in front of one. The bear is inside. It is wearing its little hat. It is smiling."
    hikari "It is limited edition. There are only a few left. And it is in this machine."
    mc "You want it?"
    hikari "I do not want it. I just think it is cute. That is different."
    mc "(She was shouting about it a moment ago. Now she is pretending. That is not fooling anyone.)"
    "The machine has a sign that says '100 yen per play.'"
    mc "One hundred yen. I can afford that."
    hikari "That is how they get you. One coin at a time."
    mc "Let me worry about the coins. You just tell me when to stop."
    hikari "I will not. I want to watch you try."

    menu:
        "I will get it for you." :
            mc "I will get it for you. Stay here and watch."
            hikari "You will not get it. These machines are rigged. They are designed to make you fail."
            mc "I have failed before. I can fail again."
            hikari "That is not the point. The point is that you will spend every yen you have trying."
            mc "I want to. I want to see your face when it drops."
            hikari "You will be broke before you know it."
            mc "(I probably will be broke. I am going to try anyway. Those are two separate facts.)"
            $ reward_attributes_once("day33_arcade_let_me", [("nerve", "micro")], show="auto")
        "Does it make you nervous when I do this?":
            mc "You don't have to watch if it makes you nervous."
            hikari "I want to watch. I just don't want you looking at me after every try."
            mc "All right. Eyes on the bear."
            $ reward_attributes_once("day33_arcade_you_try", [("grace", "micro")], show="auto")
        "[tag_insight] Rank 2: Watch where the claw lets go." if has_attribute("insight", 2):
            "I let the person at the next machine finish. The claw holds the toy until it rises past the rim. Then all three fingers open a little."
            mc "I'm not going to lift it. I'll try to drag it toward the slot."
            hikari "Show me where you're aiming."
            $ reward_attributes_once("day33_arcade_split", [("insight", "micro")], show="auto")
    stop music fadeout 2.0

    # The told price is 2500 yen. Earlier spending can leave him short, so make up
    # the difference here; the wallet and the dialogue at dinner must agree.
    if not can_afford(2500):
        $ money = 2500
        "I count what is left. It is just short of twenty-five tries."
        mc "(It is not enough. I am going to try anyway. I want her to see me try.)"

    # The claw game is player-driven now. The bear is won when the money spent
    # reaches the target (25 coins, 2500 yen), however the player breaks the tries
    # into batches. Each batch plays out as separate coin tries, then hands the
    # choice back, so the pace belongs to the player instead of a fixed marathon.
    $ claw_goal = 25
    $ claw_tries = 0
    $ claw_round = 0
    $ claw_success = False

    while claw_tries < claw_goal:

        $ claw_left = claw_goal - claw_tries

        # The argument escalates between batches. The four lines this scene lives
        # on ("stop it", "one last time", "I hate this", "I am enjoying this")
        # appear here and in the per-try beats below, and get louder near the end.
        if claw_left <= 2:
            hikari "Stop it. Stop it. That is enough. I mean it."
            mc "One last time. One last time. Just one more. I promise."
        elif claw_round == 0:
            # The intro above already made the first pitch.
            pass
        elif claw_round == 1:
            hikari "Stop. We are wasting good money."
            mc "One last time. That is all I am asking."
        elif claw_round == 2:
            hikari "I hate this. I actually hate this."
            mc "I am enjoying this. I am enjoying this too much."
        elif claw_round == 3:
            hikari "Stop it, stop it, stop it!"
            mc "One last time. I know I said that. I meant it."
        elif claw_round == 4:
            hikari "You are not listening to a word I say."
            mc "I am listening. I just do not want to stop. Not while you are watching."
        else:
            hikari "I hate this. I hate this. I hate this."
            mc "One last time. One last time. One last time."

        # An odd remainder cannot split into even batches, so one of them has to
        # be the last. The choice labels below change to match that near the end.
        if claw_left % 2 == 1 and claw_left <= 5 and claw_left > 2:
            mc "(An odd number. One of them has to be the last one.)"

        $ claw_one_label = "One last time. I mean it." if claw_left <= 2 else "One last time."
        $ claw_two_label = "Try 2 times."
        if claw_left == 2:
            $ claw_two_label = "Try 2 times. Then we stop."
        elif claw_left % 2 == 1 and claw_left <= 5:
            $ claw_two_label = "Try 2 times. Then one last time."

        menu:
            "[claw_one_label]":
                $ claw_batch = 1
            "[claw_two_label]" if claw_left >= 2:
                $ claw_batch = 2
            "Try 5 times." if claw_left >= 5:
                $ claw_batch = 5
            "Try 10 times." if claw_left >= 10:
                $ claw_batch = 10

        $ claw_round += 1
        $ claw_batch = min(claw_batch, claw_left)

        # Play the chosen number of tries, one coin at a time. Every coin goes
        # through spend_money so the wallet and the told cost agree. Each play is
        # a three-beat rhythm built to make the player expect a win: the coin text
        # arrives with the machine track (claw_start.mp3) and waits for a click,
        # the dots appear on that click with the machine still running, and the
        # machine cuts as the dots finish so the result lands on the reveal song.
        while claw_batch > 0:
            $ claw_batch -= 1
            $ claw_tries += 1
            $ spend_money(100)

            # Beat 1: the coin text and the machine track arrive together. There
            # is no {nw} here, so the line stops and waits for the player.
            $ coin_label = {1: "first", 2: "second", 3: "third"}.get(claw_tries, "next")
            play sound "audio/SFX/claw_start.mp3"
            "The [coin_label] coin goes in."

            # Beat 2: on advance, the dots appear with the machine still running.
            # The waits live in this line, so the suspense costs no extra clicks.
            if claw_tries <= 3:
                "...{w=0.45}....{w=0.45}...{w=0.45}{nw}"
            else:
                "...{w=0.25}..{w=0.25}...{w=0.25}{nw}"

            # Beat 3: the machine cuts as the dots finish. The win lands on the
            # coin that brings the total to the target, whatever batch it is in.
            if claw_tries == claw_goal:
                stop sound fadeout 0.5
                "The claw moves. It tries again."
                # claw_win.mp3 is mastered even quieter than the fail sting,
                # hence 5.0.
                play sfx "audio/SFX/claw_win.mp3" volume 5.0
                "This time, it grabs the bear. It lifts it up. It drops it into the chute."
                "We reach in and pull out the bear. It is small and soft and it has a red ribbon."
                "Kuma. The Lucky Bear. It is limited edition. I got it for her."
                $ claw_success = True
                $ claw_batch = 0

            else:
                # The fail song plays over the miss text as the reveal.
                # claw_fail.mp3 is mastered about 12 dB below the arcade BGM, so
                # volume 4.0 brings it up to the same level; the peak stays just
                # under 0 dBFS, so it does not clip.
                stop sound fadeout 0.2
                play sfx "audio/SFX/claw_fail.mp3" volume 4.0
                $ miss_line = ["Nothing. Not even a loose ribbon.", "It slips off at the last second.", "The bear rolls out of reach.", "The claw picks up a different bear, then drops that one too.", "It grabs him, then lets go.", "The machine makes a sound like a sigh."][(claw_tries - 1) % 6]

                if claw_tries == 1:
                    "The claw closes on nothing."
                elif claw_tries == 2:
                    "The claw comes back empty."
                elif claw_tries == 3:
                    "Still nothing."
                    mc "(This is not working. I am going to spend every coin I have and still not get the bear.)"
                    hikari "Stop it. Stop it. We are wasting money."
                    mc "One last time. One last time. That is all I am asking."
                elif claw_tries == 15:
                    "The claw drops the bear and it rolls back under the rail."
                    hikari "This is the worst date I have ever been on."
                    mc "I am having a good time. The best. I am enjoying this far too much."
                elif claw_tries == 34:
                    "The claw brushes the bear and drops it. I swear it moved."
                    hikari "One more. If this does not work, we are leaving."
                    mc "One more. I promise. This is the last one."
                elif claw_tries % 10 == 0:
                    "The claw moves again. It misses. We are [claw_tries * 100] yen in."
                    hikari "I hate this. I hate this so much."
                    mc "I am enjoying this. I am enjoying this far too much."
                elif claw_tries % 9 == 0:
                    "The claw grabs a handful of nothing. Again."
                    hikari "Stop. Please. Just stop."
                    mc "I cannot. We have come this far. I cannot stop now."
                elif claw_tries % 7 == 0:
                    "The claw drops the bear back where it was."
                    hikari "This is going to bankrupt us. Stop it."
                    mc "We are going to get you the bear. I do not care what it costs."
                elif claw_tries % 5 == 0:
                    "Another miss."
                    hikari "This is insane. Stop it, stop it, stop it."
                    mc "We will keep going. I am enjoying this. That is the problem."
                    hikari "Then we are both insane. Keep going."
                else:
                    "[miss_line]"

                if claw_tries in (10, 25):
                    scene black with Dissolve(0.8)
                    pause 0.6
                    if claw_tries == 10:
                        "Ten tries. I am beginning to think the claw is afraid of him."
                    else:
                        "We have spent enough to buy a real bear. A bigger one. With a better ribbon."
                    pause 0.6
                    scene bg_arcade_claw with Dissolve(0.8)
                    if claw_tries == 10:
                        hikari "Maybe he does not want to be rescued."
                        mc "Then he has very different taste from you."
                    else:
                        hikari "We should have just asked the price of the bear."
                        mc "This is the price of the bear."

    scene bg_arcade_entrance with walk_fade
    play music "audio/Music/arcade.mp3" fadein 2.0
    "Hikari takes the bear. She holds it. She looks at it. She smiles."

    # Her bear-hugging drawing takes over as her portrait for this beat, instead
    # of a second, full-size image being shown on top of her usual picture.
    $ hikari_hugging_bear = True
    hikari "He is mine. He is really mine."
    "She pulls Kuma against her chest and hugs him. She hugs him so hard the red ribbon bends."
    hikari "I am never letting you go. Not ever."
    hikari "He is going to bring me luck."
    mc "You knew him the moment you saw him."
    hikari "Everyone knows Kuma. I told you. As long as I have him, I feel lucky."
    mc "He already brought you luck. He brought you to Shibuya."
    hikari "That was you, not him. You are the one who kept putting coins in."
    mc "(She is smiling. The bear is against her chest. I think that is enough.)"
    $ hikari_hugging_bear = False
    $ add_affection("sister", 1)


    # --- ARCADE GAMES ---
    scene bg_arcade_entrance with walk_fade
    # The claw machine scene is over; bring the arcade BGM back.
    "We walk through the arcade. More machines. More games. More people."
    "Hikari is holding the bear. She is not letting go."
    hikari "Come on. Let us look at the other arcade machines."
    mc "I thought you had enough."
    hikari "I had enough of the claw machine. This is different."
    mc "(The bear is won. There is nothing left to prove in this corner of the arcade.)"

    "We pass a row of dance machines. Four people are playing, and they are good. They move like they have done this a thousand times."
    "One of them has a phone on a small stand. It records only their own body and the flashing floor. Nobody walking past is in the frame."
    mc "(They are not playing for anyone here. They are playing for people somewhere else.)"
    mc "I do not think I can do that."
    hikari "You do not have to be that good. You just have to step on the arrows."
    mc "(I am intimidated. I want to try anyway.)"

    menu:
        "Try NEON STEP." :
            mc "I want to try NEON STEP."
            hikari "The dance game is the most physical. You have to move. You have to be in your body."
            hikari "It is the city in miniature. You move. You fail. You move again."
            call minigame_dance from _call_minigame_dance_1
            if _return:
                "I finish the set in rhythm. The floor lights flare as the last chord rings out."
                hikari "You did it. That was good."
                mc "I am not good at this. I just kept trying."
                hikari "That is what good is. Trying until it works."
                $ reward_attributes_once("day33_dance_success", [("grace", "micro")], show="auto")
            else:
                "The set ends early, but the beat is still waiting."
                hikari "You did not finish. But you tried. That is enough."
                mc "It is not enough. I want to finish."
                hikari "You will finish next time. There is always a next time."
                $ reward_attributes_once("day33_dance_fail", [("nerve", "micro")], show="auto")
        "Try Orbit Defender." :
            mc "I want to try Orbit Defender."
            hikari "Orbit Defender is the most aggressive. You have to aim. You have to shoot. You have to survive."
            hikari "Like the city. You aim. You fail. You aim again."
            call minigame_arcade_shooter from _call_minigame_arcade_shooter_1
            if _return:
                "The ship survives. The waves keep coming. I keep shooting."
                hikari "That is what good means. Trying until it works."
                $ reward_attributes_once("day33_shooter_success", [("insight", "micro")], show="auto")
            else:
                "The ship is destroyed. The waves keep coming. I keep dying."
                hikari "You did not survive. But you tried. That is enough."
                mc "It is not enough. I want to survive."
                hikari "You will survive next time. There is always a next time."
                $ reward_attributes_once("day33_shooter_fail", [("nerve", "micro")], show="auto")
        "Try the signal echo game." :
            mc "I want to try the signal echo game."
            hikari "The signal echo game is the most mysterious. You have to listen. You have to echo. You have to remember."
            hikari "The same as the city. You listen. You echo. You remember."
            call minigame_signal_echo from _call_minigame_signal_echo_1
            if _return:
                "The signal harmonizes. The dream solidifies into focus."
                hikari "That is the whole thing. Trying until it works."
                $ reward_attributes_once("day33_echo_success", [("grace", "micro")], show="auto")
            else:
                "The signal slips away. The dream dissolves into static."
                hikari "You did not harmonize. But you tried. That is enough."
                mc "It is not enough. I want to harmonize."
                hikari "You will harmonize next time. There is always a next time."
                $ reward_attributes_once("day33_echo_fail", [("nerve", "micro")], show="auto")
        "We are done. Let us go home." :
            mc "We are done. Let us go home."
            hikari "Good. I am tired. I want to go home."
            hikari "I want to take him home."
            mc "(I am tired too. Let us get the two of them home.)"

    # Fade to black and back
    scene black with Dissolve(1.5)
    pause 1.5
    scene bg_arcade_entrance with Dissolve(1.5)

    "We walk out of the arcade. The night is cold. The city is loud. The bear is in her arms."
    hikari "I had a lot of fun today. I am going to cherish this bear."
    mc "For the rest of your life?"
    hikari "Yes. He is limited edition. He is mine. He is lucky."
    mc "(He is hers. I do not need to say it out loud.)"

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    "We walk home. The city is quieting down. The lights are still on. The bear is still in her arms."
    hikari "Thank you. For today. For the bear. For trying."
    mc "You do not have to thank me. I wanted to get it for you."
    hikari "I know. That is why it worked."
    mc "(It worked because I wanted to make her happy. That was the whole point.)"

    scene bg_kitchen_night with walk_fade
    $ sunday_at_home = True
    "The kitchen is warm. Mother has dinner on the table. Rice, soup, and something with fish."
    mother "Sit. Eat. You must be hungry after Shibuya."
    hikari "We went to the arcade. I got a bear."
    mother "A bear from the arcade?"
    hikari "A lucky bear. With a red ribbon. He is limited edition."
    father "How much did it cost?"
    hikari "2500 yen."
    father "2500 yen for a bear?"
    hikari "It was worth it. The money bought the trying, not just the bear."
    father "The experience of spending 2500 yen on a bear?"
    hikari "Yes. Trying. Succeeding. Having fun."
    father "That is a very expensive lesson."
    father "Those machines are traps. The whole arcade is built to take your money and call it fun."
    father "You take care of what you have. That is all I am saying."
    hikari "You always do this. I had fun. That is the whole point."
    hikari "It is not a lesson. It is a memory."
    mc "(She is right. The trying was the fun part. I would do it again.)"
    $ add_affection("sister", 1)

    call dinner_close from _call_dinner_close_17

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the window is open a crack. The city is doing its night sounds: a train, a cat, a drainpipe."
    "The bear is on my desk. She set him down when she came in, but she keeps looking at him. Kuma. The Lucky Bear. He is small and soft and he has a red ribbon."
    "The notebook is still there. The corridor map. The doors that are not in order."
    "The tomato timer is on the desk. Hikari gave it to me. It is not running."
    $ night_desk_line = "a lucky bear, a timer that is not running, and the notebook"
    call night_open from _call_night_open_21

    menu:
        "Ask Hikari about the dream." :
            mc "Did you dream about the bear?"
            hikari "I dreamed about the claw machine, the bear, and you trying to get it."
            hikari "It was a good dream. I hope it keeps coming back."
            mc "(I will take it as it is.)"
            $ log_memory("hikari", "said she dreamed about the claw machine and the bear and it was a lucky dream")
            $ reward_attributes_once("day33_night_dream", [("insight", "micro")], show="auto")
        "Ask her about the note." :
            mc "The note said come back next class."
            hikari "I saw it. That is not an absence. That is a boundary. He is telling you the answer is not in his office."
            hikari "The answer is here. In the city. In the crowd. In the arcade. In the bear."
            mc "(Here. Not in his office. That is the second time today someone has told me the same thing.)"
            $ log_memory("hikari", "said the professor's absence is a boundary and the answer is here")
            $ reward_attributes_once("day33_night_boundary", [("grace", "micro")], show="auto")
        "Watch the bear. Say nothing." :
            "I do not say anything. The bear is on the desk. The city is doing its night sounds."
            "Hikari watches me without needing to say anything."
            mc "(We are still building something. The room is not what it was yesterday.)"
            $ log_memory("hikari", "watched the lucky bear in silence on the night of Shibuya")
            $ reward_attributes_once("day33_night_quiet", [("nerve", "micro")], show="auto")

    call night_close from _call_night_close_21

    "The fifth week is not a fresh start. It is the first week where I know the professor is not the answer."
    "I switch off the lamp. The dark fills the room. The room is not empty. The bear is on the desk. The timer is on the desk. The notebook is on the desk."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5

    # Dream sequence: Orbit Defender, but the controls do not answer.
    scene bg_space with Dissolve(1.5)
    "I dream about the arcade. Orbit Defender. The waves."
    "The ship. The bullets. The enemies."
    "I try to move. I try to shoot. I try to survive."
    "But the controls do not work. The ship does not move. The bullets do not fire."
    call minigame_arcade_shooter_dream from _call_minigame_arcade_shooter_dream
    "The waves keep coming. The enemies keep shooting. The ship keeps dying."
    "I am trapped. I cannot move. I cannot shoot. I cannot survive."
    "I wake up. The room is dark. The bear is on the desk. The timer is on the desk. The notebook is on the desk."
    mc "(It was a dream. I lost control in it.)"

    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
