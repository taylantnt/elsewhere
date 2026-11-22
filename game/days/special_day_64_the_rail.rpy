################################################################################
## DAY 64: WEDNESDAY, JUNE 10, 2026
## Act 3 proper. The afternoon is spoken for. No free-roam hub.
################################################################################

label special_day_64_the_rail:
    $ set_story_day(64)
    $ current_act = 3
    $ corruption_level = 3
    call day_transition from _call_day_transition_64
    $ last_afternoon_place = None
    $ last_afternoon_hikari_tour = False
    $ flush_pending_messages()

    scene bg_kitchen with walk_fade

    "Father has laid a dish towel on the table. His flip phone is open on it, with the battery beside it. He puts the battery in, closes the back, and waits."
    father "What time does yours say?"
    "I show him my phone. He sets his to match. By the time he puts the cover back on, his screen is four minutes behind mine."
    mc "It went back."
    father "I can see that."
    "He starts to take the cover off again. Mother sets his tea down on the edge of the towel."
    mother "Don't. You'll lose that little screw."
    "There isn't a screw. He puts the phone in his pocket anyway."

    scene bg_campus_interior with walk_fade

    "After class I put my phone away without opening the map. Hikari is waiting by the stairs. She's brought the little torch from the kitchen."
    mc "I thought we were going in daylight."
    hikari "We are. I want to find the spot where I dropped it."
    mc "You didn't drop it."
    "She has already started down. She stops with one foot on the next step."
    hikari "Then why do I remember picking it up?"

    scene bg_train_interior with walk_fade
    play music "audio/Music/train.mp3" fadein 2.0

    "She takes the window seat and sets the torch on her knee. It's the cheap kind with a wrist strap. I remember the strap swinging as I followed her back to the station."
    mc "You had it all the way back."
    hikari "Was it on?"
    mc "Yes."
    "She pushes the switch with her thumb. A circle of light comes on against her skirt. She switches it off again."

    scene bg_river with walk_fade
    stop music fadeout 2.0

    "In daylight the path is narrower than I remember. You can see the line the water left on the concrete. Someone has tied a plastic bag to the rail to stop it blowing away."
    "Hikari steps around a loose stone."
    if "hikari_warning" in story_memory_keys:
        hikari "I'm going a little farther. I'll wait at the bend."
        "She waits there until I catch up. I remember the stairs on my first day, when I'd followed her as far as I knew how."
    else:
        "I step around it after her."
    "At the bend she puts a hand out to stop me."
    hikari "There."

    scene bg_river_night

    "At the rail it is night. Not on the path where we are standing. Just at the rail, as far as the grass on either side. A few lights rise out of it."
    "Two people have their backs to us. The shorter one has a torch hanging from her wrist. The taller one pulls his left sleeve down over his hand. I look at my own hand. I've done the same thing without thinking."
    "The torch slips. It hits the stone and rolls back against her shoe. When she stoops for it, the taller one looks over his shoulder."
    "It's my face. He looks just past me, to where the path turns."
    "The torch comes on. The girl shields it with her palm. I can see the pale spot on her thumb where Hikari burned it on the kettle."

    scene bg_river

    "A bicycle bell sounds behind us. We move aside. By the time it passes, the plastic bag is the only thing moving at the rail."

    menu:
        "Ask Hikari what she saw.":
            mc "Tell me what you saw. Before I tell you."
            hikari "You pulled your sleeve down. Then I dropped the torch."
            mc "Did you see his face?"
            hikari "I was looking at my hands."
            $ remember("hikari", "watched themselves at the rail and asked for her account before his, so neither version overwrote the other", "rail_independent_accounts")
        "[tag_nerve] Rank 3: Go back to the exact spot where the torch fell." if has_attribute("nerve", 3):
            "I walk up to the rail and crouch. There's a chip in the concrete, not much bigger than a grain of rice. I can still see where he was standing."
            "Hikari sets the torch in my palm. There's a nick in the rim. I turn it so she can see."
            hikari "It was there when I took it out of the drawer."
            $ log_memory("hikari", "showed him the nick in the torch after they saw it fall at the rail")
        "Ask her to walk back with you.":
            mc "Can we go back to the bend?"
            "She takes my sleeve between two fingers. We walk back together."
            hikari "Should I let go?"
            mc "Not yet."
            $ log_memory("hikari", "held his sleeve on the path back from the rail")

    "We take the long way to the station. Neither of us looks back."
    if "hikari_charm" in story_memory_keys:
        "The two charms on her bag knock together as we walk. She catches them in her hand."
        hikari "You never asked me what your charm was for."
        mc "I wasn't giving it to you for anything."
        hikari "I know. That's why I kept it."
    hikari "Last time, I remember you going ahead of me."
    mc "You went ahead. You had the light."
    hikari "I know. I remember that too."

    scene bg_home_exterior_night with walk_fade
    $ night_street()

    "At the gate I can hear the television through the front window. The weather report is just ending. Mother has left the porch light on."
    "Hikari unthreads the torch strap from her wrist. There is a red line underneath it."
    hikari "Will you keep it tonight?"
    "I put it in my pocket. She waits for me to open the gate."
    "The light is already on inside my pocket. I can see it through the cloth."

    jump act2_day_router
