################################################################################
## DAY 61: SUNDAY, JUNE 7, 2026
## The house is growing. The room is bigger by centimeters. The hallway is
## longer by steps. Mother is standing in the kitchen at three in the morning,
## facing the wall. The geometry is wrong and it is measurable.
##
## Corruption level 3. Undeniable. The structure itself has changed.
################################################################################

label special_day_61_the_geometry:
    $ set_story_day(61)
    $ corruption_level = 3
    call day_transition from _call_day_transition_61
    $ last_afternoon_place = None
    $ last_afternoon_hikari_tour = False

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Sunday. Twelve days of rain. I did not sleep. I sat at the desk with the notebook open and the two lines staring at me. She is leaking. She does not know."
    "At some point I measured the room."
    "I do not know why. I do not remember deciding to measure it. I was sitting at the desk and then I was standing with my arm against the wall, counting the spans from the window to the door."
    mc "(Eleven spans. The room is eleven spans wide. I have measured it before. I measured it in the first week, because I was bored and the room was new and measuring things is what you do when you are in a place you do not know.)"
    mc "(It was ten spans. In the first week, it was ten spans. I am sure it was ten. I counted ten. I remember counting ten.)"
    mc "(Now it is eleven.)"
    "I measure it again. Eleven. I measure it with my other arm. Eleven. I measure it with steps. Eleven. The room is eleven spans wide and it was ten and I am not imagining it."
    mc "(The room is bigger. Not by much. By one span. By the width of my hand. The walls have moved apart in the night, or over many nights, and I did not notice because I was counting other things. Tiles and cards and footsteps and the order of sounds.)"

    "My phone buzzes."

    $ run_chat("hikari", [
        {"them": "Sunday. I am going to the library again. I need to read more about somnambulism.", "options": [
            {"label": "\"More?\"",
             "send": "More?",
             "them": ["I could not stop thinking about it.", "There are things in the literature I do not want to believe."]},
            {"label": "\"What things?\"",
             "send": "What things?",
             "them": ["I will tell you when I know.", "Right now I only have questions."]},
        ]},
    ])
    mc "(She is researching what happened to her. She is treating it as a medical question. I do not know if it is a medical question. I do not know what kind of question it is.)"

    call murakami_daily_ping from _call_murakami_daily_ping_61

    scene bg_kitchen with walk_fade

    call corruption_morning from _call_corruption_morning_61

    "The kitchen is bigger. I measured the room upstairs and now I am in the kitchen and it is bigger too. The table has not moved but there is more space around it. The walls have stepped back."
    "I count the tiles from the door to the counter. I counted them on Day fifty-four. Seven. Today there are eight."
    mc "(Eight tiles. One more tile. The kitchen has grown a tile. The house is growing. The house is adding tiles and spans and steps and I am the only one who is counting.)"
    mother "Good morning."
    mc "Good morning."
    mother "You look like you have been measuring something."
    mc "(She says it. She does not know she says it. She says it the way she says everything. Lightly. Like weather. But she said measuring. I was measuring. She could not have seen me. She was in her room.)"
    mc "I was not measuring."
    mother "Good. Measuring is for tailors and carpenters. You are a student."
    mc "(She is right. I am a student. I am not a tailor or a carpenter. I should not be measuring rooms. I should not be counting tiles. I should be studying.)"
    father "Sunday. The day of rest. Even the rain is resting."
    hikari "The rain is not resting. It is just slower. That is not the same thing."
    father "You are right. Slower is not rest. Slower is just a different speed."
    mc "(They are having a conversation about the rain. It is a normal conversation. It is the kind of conversation that happens on a Sunday morning in a kitchen that is one tile bigger than it was a week ago.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/school.mp3" fadein 2.0

    "Sunday. No lecture. No campus. The city is doing its slow version. The rain is doing its slow version. I am doing my slow version."
    mc "(I should go somewhere. The hub is open. The afternoon is a door. I should walk through it. The doors are closing. I can feel them closing. Not today, but soon.)"

    call free_afternoon from _call_free_afternoon_61

    call corruption_post_visit from _call_corruption_post_visit_61

    scene bg_home_exterior_day with walk_fade
    stop music fadeout 2.0

    "The walk home. The streets are the streets. The distances are wrong. The combini is closer than it was. Or I am walking faster. Or the city is shrinking while the house is growing. I do not know which direction the wrongness is moving."
    mc "(The house is growing. The city is shrinking. Or both are the same and I am the one who is moving. I am the fragment. I do not have the blueprint.)"

    scene bg_kitchen with walk_fade

    call dinner_open from _call_dinner_open_61

    "I count the steps from the stairs to the kitchen. I counted them yesterday. Twelve. Today there are fourteen."
    mc "(Two more steps. The hallway has grown two steps. The hallway is longer. The house is longer. The house is growing in every direction and I am the only one who is measuring.)"
    father "You are counting."
    mc "What?"
    father "Your lips. You are counting. I can see it."
    mc "I was counting the steps."
    father "How many?"
    mc "Fourteen."
    father "It has always been fourteen."
    mc "(He says always. He says it lightly. He says it the way he says everything. But it was twelve. I counted twelve. I am sure I counted twelve.)"
    mother "Eat your rice."
    hikari "He is counting, Mother. Let him count."
    mother "Counting is for after dinner. Dinner is for eating."
    mc "(Hikari said let him count. She said it like she understands. She said it like she is counting too. She is counting something else. The somnambulism. The literature. The things she does not want to believe.)"

    call dinner_close from _call_dinner_close_61

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "The room. Eleven spans wide. The desk. The notebook. The laundry rack. The window. The rain."
    $ night_desk_line = "the measuring"
    call night_open from _call_night_open_61

    menu:
        "[tag_insight] Rank 3: Ask what has a destination if not her feet." if has_attribute("insight", 3):
            mc "You said destination. Not wandering."
            hikari "I stood in one place. That is not sleepwalking."
            mc "Then it was not your feet that were asleep."
            hikari "Do not finish that sentence. I know where it goes."
            $ reward_attributes_once("day61_night_destination", [("insight", "micro")], show="auto")
        "Ask whether she thinks she was sleepwalking.":
            hikari "The library. The literature. The things I do not want to believe."
            mc "What things?"
            hikari "Sleepwalking is supposed to be random. Purposeless. You stand, you walk, you go back. There is no pattern."
            mc "And?"
            hikari "Mine has a pattern. I stood at your door. I was looking at the wall. That is not random. That is directed. That is a destination."
            mc "(She is right. She was not wandering. She was standing. She was looking at a specific wall. The wall behind me. The wall that has the twelfth door on the other side of it.)"
            $ log_memory("hikari", "said her sleepwalking has a pattern, a destination, it is not random")
            $ reward_attributes_once("day61_night_a", [("grace", "micro")], show="auto")
        "Show her how you measured the room.":
            mc "The room is bigger."
            hikari "What?"
            mc "Eleven spans. It was ten. I measured it in the first week. Ten. Now it is eleven."
            hikari "You measured your room."
            mc "I measured it today. And the kitchen. Eight tiles. It was seven. And the hallway. Fourteen steps. It was twelve."
            "She is quiet. She is looking at the walls. She is measuring them with her eyes."
            hikari "I cannot tell. It looks the same to me."
            mc "I counted."
            hikari "I believe you counted. I do not believe the counting."
            mc "That is fair."
            hikari "But I believe you."
            $ log_memory("hikari", "could not see the room was bigger but said she believes me, which is different from believing the counting")
            $ reward_attributes_once("day61_night_b", [("nerve", "micro")], show="auto")
        "Say nothing. Listen to the city.":
            "The rain. The city. The Sunday sounds. The silence that is not silence. The house that is not doing its sounds."
            "Hikari is on the floor. She is not sleeping. She is measuring the room with her eyes. I can see her doing it. She is counting spans."
            $ log_memory("hikari", "was measuring the room with her eyes, counting spans, even though she said she could not tell")
            $ reward_attributes_once("day61_night_c", [("insight", "micro")], show="auto")

    call night_close from _call_night_close_61

    call corruption_night from _call_corruption_night_61

    "I lie in the dark. The house is not doing its sounds. All six are gone. The silence is full. The sound of a room holding its breath."
    "Then the fridge starts. Just the fridge. It hums and stops and hums and stops. Like it is trying to remember the rest."
    "I get up. I need water."
    "I walk down the stairs. Fourteen steps. I count them. Fourteen."
    "The kitchen is dark. The moon is through the window and the rain is on the glass and the kitchen is lit by the colour of outside."
    "Mother is standing at the counter."
    "She is facing the wall. Not the counter. The wall. Her back is to me. Her hands are at her sides. She is not moving."
    mc "Mother."
    "She does not respond."
    mc "Mother."
    "She does not respond. She is standing the way Hikari was standing. The same posture. The same stillness. The same absence."
    "I say her name a third time."
    mc "Mother."
    "She turns."
    "She turns and she smiles and the smile is her smile and the eyes are not her eyes. The eyes are the eyes of someone who has been standing at a wall in the dark and has been called back."
    mother "Water?"
    mc "Yes. Water."
    "She turns to the tap. She fills a glass. She hands it to me. Her hand is steady. Her hand is perfectly steady. The glass is cold. The water is cold."
    mother "Go to bed. It is late."
    mc "You too."
    mother "I was just getting water."
    "She says it. The same words Hikari said. I was getting water. The same sentence. From a different person. From the same script."
    "She walks past me. She goes upstairs. I hear her bedroom door close."
    "I stand in the kitchen with the glass of water. The fridge hums and stops and hums and stops."
    "The wall she was facing is the wall between the kitchen and the hallway. The hallway that has grown two steps. The hallway that leads to the stairs. The stairs that lead to the room that has grown one span."
    mc "(She was facing the wall. Not the counter. Not the window. The wall. The wall that is between the kitchen and the rest of the house. She was facing the house.)"
    "I drink the water. I put the glass in the sink. I go upstairs. Fourteen steps."
    "The laundry rack is in the corner. The notebook is on the desk. The rain is on the window."
    "I do not sleep."
    $ collect_notebook_line(61)

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
