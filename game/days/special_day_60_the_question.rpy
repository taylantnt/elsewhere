################################################################################
## DAY 60: SATURDAY, JUNE 6, 2026
## The morning after the door. Hikari does not remember. But she asks what she
## looked like, and she has done it before. At dinner, Father says the line
## again. Hikari's lips move with it. The notebook is open.
##
## Corruption level 2. The last deniable day. After this, denial is a choice.
################################################################################

label special_day_60_the_question:
    $ set_story_day(60)
    $ corruption_level = 2
    call day_transition from _call_day_transition_60
    $ last_afternoon_place = None
    $ last_afternoon_hikari_tour = False

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Saturday. Eleven days of rain. I did not sleep. I sat at the desk and watched the door and waited for her to come back. She did not come back."
    "The morning is here. The morning is grey and wet and normal and I have to decide whether to ask her."
    mc "(I have to ask her. If I do not ask her, I am keeping it. If I keep it, it becomes mine. It should not become mine. It should stay hers.)"

    "My phone buzzes."

    $ run_chat("hikari", [
        {"them": "Good morning. I slept well. I think.", "options": [
            {"label": "\"You think?\"",
             "send": "You think?",
             "them": ["I do not remember falling asleep.", "That is not new. That is just how I sleep."]},
            {"label": "\"Can I ask you something?\"",
             "send": "Can I ask you something?",
             "them": ["Yes.", "Is it about last night?"]},
        ]},
    ])
    mc "(She knows. She does not remember but she knows. She said is it about last night before I told her there was a last night.)"

    call murakami_daily_ping from _call_murakami_daily_ping_60

    scene bg_kitchen with walk_fade

    call corruption_morning from _call_corruption_morning_60

    "Hikari is at the table. She is eating rice. She is looking at her rice. She is the Hikari who slept, not the Hikari who stood at my door."
    mc "Can I ask you something?"
    hikari "You already did. On the phone."
    mc "Last night. You came to my room."
    "She puts down her chopsticks. She does not look up."
    hikari "I did?"
    mc "You stood at the door. You were looking at the wall. I said your name three times. You did not respond. Then you blinked and said you were getting water."
    "She is quiet. She is looking at her rice."
    hikari "I do not remember that."
    mc "I know."
    hikari "What did I look like?"
    mc "(She asks what she looked like. Not whether it happened. Not whether I am sure. What she looked like. Like she needs the description to match something she already knows.)"
    mc "You were standing. Your eyes were open. You were not looking at me. You were looking at the wall behind me. You were not there."
    hikari "Not there."
    mc "Your body was there. You were not."
    "She is quiet for a long time. The kitchen is doing its kitchen sounds. The fridge. The tap. The clock that is stopped."
    hikari "I have done that before."
    mc "What?"
    hikari "When I was small. My mother told me. I would stand at her door in the night. She would say my name and I would not answer. She would have to walk me back to my room."
    mc "How old were you?"
    hikari "Five. Six. She said I grew out of it."
    mc "You grew out of it."
    hikari "She said I did."
    mc "(She said she said. Past tense. Mother told her she grew out of it. Mother does not tell her that now. Mother does not mention it. Mother stalls over vinegar and does not remember. Maybe Mother does not remember the sleepwalking either.)"
    hikari "Do you think it is coming back?"
    mc "I do not know."
    hikari "I am asking you because you are the only person who saw it. I cannot ask Mother. She would not remember. I cannot ask Father. He would say it is the rain."
    mc "It might be the rain."
    hikari "It is not the rain."
    mc "(She says it is not the rain. She says it flat. She says it like she knows what it is. She does not know what it is. But she knows what it is not.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/school.mp3" fadein 2.0

    "Saturday. No lecture. No campus. No corridor with the tile. The day is a shape without edges."
    "Hikari is in the library. I am walking. The rain is lighter today, almost a mist, and the city is doing its Saturday version: slower, emptier, the shops open but not trying."
    mc "(I should go somewhere. I should see someone. The hub is open. The afternoon is a door. I should walk through it before the doors start closing.)"

    call free_afternoon from _call_free_afternoon_60

    call corruption_post_visit from _call_corruption_post_visit_60

    scene bg_home_exterior_day with walk_fade
    stop music fadeout 2.0

    "The walk home. The combini. The card. I look at it. The handwriting has not changed since yesterday. Or it has. I have stopped checking. The checking was the thing that was making it worse. The checking was the fragment that did not have the blueprint."
    mc "(I am going to stop checking. I am going to walk home. I am going to eat dinner. I am going to sit with Hikari and not ask about the door. The door is asked. The answer is given. The answer is: she does not remember, and she has done it before.)"

    scene bg_kitchen with walk_fade

    call dinner_open from _call_dinner_open_60

    father "Saturday. The week is a machine. It runs the same program every seven days and the output is always Sunday."
    "He says it. The whole sentence. The fourth time. The same words, the same cadence, the same pause before Sunday."
    "Hikari does not react. She is eating. She is looking at her bowl."
    "But her lips are moving."
    "I see it from across the table. Her lips are forming the words. Not out loud. Just the shape. The week is a machine. It runs the same program. Her lips are moving with his voice."
    mc "(She is not doing it on purpose. She does not know she is doing it. She is mouthing his sentence the way a child mouths the words to a song they have heard too many times.)"
    mc "(Or she is mouthing it because it is her sentence now. Because the sentence has moved from him to her. Because the sentence is leaking.)"
    mother "Eat your rice."
    hikari "I am eating."
    mother "Then eat. Do not move your mouth when you are not eating."
    "Hikari's lips stop. She looks at Mother. Mother is at the counter. Mother did not see the lips. Mother heard the silence and filled it with instruction."
    mc "(Mother did not see it. Only I saw it. Only I am seeing these things. The tile, the card, the notebook, the door, the lips. Only I am the witness. That is either because I am the one who is awake, or because I am the one who is dreaming.)"

    call dinner_close from _call_dinner_close_60

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "The room. The desk. The notebook. The laundry rack. The window. The rain. The door where Hikari stood."
    $ night_desk_line = "the notebook, open"
    call night_open from _call_night_open_60

    menu:
        "[tag_nerve] Rank 3: Tell her you are afraid of the answer." if has_attribute("nerve", 3):
            mc "I am afraid. Of what the third thing will be."
            hikari "You did not say that before."
            mc "I am saying it now. I did not want to be the person who was afraid."
            hikari "You are the person who is afraid. That is a relief."
            mc "Why?"
            hikari "Because now there are two of us in the room and only one pattern."
            mc "(It is not less frightening. It is less lonely.)"
            $ log_memory("hikari", "said he was afraid of the third thing too, and she called it a relief")
            $ reward_attributes_once("day60_night_afraid", [("nerve", "micro")], show="auto")
        "Ask what she found out about sleepwalking.":
            hikari "I was in the library. I read about sleepwalking. It is called somnambulism. It is common in children. It can return in adults under stress."
            mc "Are you under stress?"
            hikari "The paper. The rain. The house. You. All of it. None of it. I do not know what counts as stress anymore."
            mc "(She does not know what counts as stress. She is measuring her life against a scale she cannot read. That is all of us. That is the condition.)"
            $ log_memory("hikari", "read about somnambulism in the library, said she does not know what counts as stress anymore")
            $ reward_attributes_once("day60_night_a", [("grace", "micro")], show="auto")
        "Tell her what you saw at dinner.":
            mc "At dinner. When Father said the line. Your lips were moving."
            hikari "What?"
            mc "The week is a machine. He said it and your lips were moving with it. You were mouthing the words."
            "She is quiet. She is looking at me. She is not looking at the wall. She is looking at me."
            hikari "I did not know I was doing that."
            mc "I know."
            hikari "That is two things now. The door and the lips. Two things I did not know I was doing."
            mc "Yes."
            hikari "Two is a pattern."
            mc "Yes."
            hikari "I do not want it to be three."
            $ log_memory("hikari", "learned her lips moved with Father's sentence, said two things is a pattern and she does not want it to be three")
            $ reward_attributes_once("day60_night_b", [("nerve", "micro")], show="auto")
        "Say nothing. Let the question stay open.":
            "The rain. The city. The Saturday sounds. No dog. The dog does not bark on Saturdays. Or I have not noticed."
            "Hikari is on the floor. She is sleeping. She is breathing the way she breathes when she is not at the door. The way she breathes when she is here."
            $ log_memory("hikari", "was sleeping and breathing the way she breathes when she is here, not at the door")
            $ reward_attributes_once("day60_night_c", [("insight", "micro")], show="auto")

    call night_close from _call_night_close_60

    call corruption_night from _call_corruption_night_60

    "I do not lie down. I sit at the desk. I open the notebook."
    "I turn to the page from Day forty-nine. The hydrangea day."
    "The line is there. She is leaking. In handwriting that is not mine."
    "I turn to the page from Day fifty-six. The day I found it."
    "The line is still there. But there is another line now. Below it. In the same handwriting. The same small, tight letters."
    "It says: \"She does not know.\""
    mc "(Two lines. Two messages. In my notebook. In handwriting that is not mine. She is leaking. She does not know.)"
    "I stare at the lines. The lines stare back."
    "I close the notebook. I put it on the desk. I sit in the dark."
    "The laundry rack is in the corner. The rain is on the window. The house is doing its sounds in the wrong order. Hikari is in her room. The door is closed."
    "I do not sleep."
    $ collect_notebook_line(60)

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
