################################################################################
## DAY 54: SUNDAY, MAY 31, 2026
## The return. Three days of wrongness, and then a Sunday that is just a
## Sunday. The hub reopens. The lecture is tomorrow. The laundry rack is back.
##
## Corruption level 1. One wrong detail. The player might not notice.
################################################################################

label special_day_54_the_return:
    $ set_story_day(54)
    $ corruption_level = 1
    call day_transition from _call_day_transition_54
    $ last_afternoon_place = None
    $ last_afternoon_hikari_tour = False

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Sunday. The rain has not stopped since Thursday, but today it is the kind of rain that is just weather. Not a sign. Not a symptom. Just rain."
    "I sit on the edge of the bed and wait for the feeling to pass. The feeling that the last three days were a crack in something and today is the thing closing over it."
    mc "(Maybe it closed. Maybe it was always closed and I was the one who was open.)"

    "My phone buzzes."

    $ run_chat("hikari", [
        {"them": "It is Sunday. You do not have class. I do not have class. The house is ours.", "options": [
            {"label": "\"What are you doing?\"",
             "send": "What are you doing?",
             "them": ["Reading. The seminar has a paper due Wednesday.", "But the afternoon is free. You should go somewhere."]},
            {"label": "\"I think I will stay in.\"",
             "send": "I think I will stay in.",
             "them": ["You have been in for three days.", "Go somewhere. Anyone. It does not have to be me."]},
        ]},
    ])
    mc "(She is right. Three days in the house. Three days of the line, the faces, the word. I should go somewhere.)"

    call murakami_daily_ping from _call_murakami_daily_ping_54

    scene bg_kitchen with walk_fade

    call corruption_morning from _call_corruption_morning_54

    "Hikari is at the table with a book open and a pen that has not moved in twenty minutes. Father is reading the paper. Mother is making tea."
    "It is a Sunday. It is exactly a Sunday."
    mother "You look better. You slept."
    mc "Did I?"
    mother "You did not come down for water. You did not knock on any doors. You slept."
    mc "(I did sleep. I do not remember dreaming. That is the first time in a week.)"
    father "The rain will break by Tuesday. The news is certain."
    hikari "The news was certain about last Tuesday too."
    father "The news is always certain. That is its job. Accuracy is a hobby."
    mc "(This is the house I know. This is the family I know. The last three days were a fever. Today the fever broke.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/school.mp3" fadein 2.0

    "The street is wet and the air smells like the inside of a greenhouse. Sunday morning, and the city is doing its slow version: fewer trains, longer pauses, people walking like they have nowhere to be."
    mc "(I should go somewhere. Hikari said so. The hub is open. The afternoon is a door with something written on it for once.)"

    "At the corner across the street, a woman in a grey coat is standing under an umbrella, reading her phone. I have seen that coat before. I look away, and when I look back, the corner is empty."
    mc "(I am seeing people I have seen before. That is what three days inside does. The city starts to rhyme.)"

    call free_afternoon from _call_free_afternoon_54

    call corruption_post_visit from _call_corruption_post_visit_54

    scene bg_home_exterior_day with walk_fade
    stop music fadeout 2.0

    "I walk home through the wet streets. The rain has thinned to a mist that does not need an umbrella. The city looks like a photograph of itself, slightly out of focus."
    mc "(It was good to see someone. It was good to talk about something that was not the house, or the line, or the dream. It was good to be a person for an afternoon.)"

    scene bg_kitchen with walk_fade

    call dinner_open from _call_dinner_open_54

    mother "You went out."
    mc "I did."
    mother "Good. The house is not a hospital. You do not get better by staying in bed."
    father "Where did you go?"
    mc "(I tell him. He nods. It is a normal exchange. The kind that happens on a Sunday.)"
    hikari "Did you eat?"
    mc "I ate."
    hikari "Then you are ahead of me. I forgot."
    mother "You did not forget. You were reading."
    hikari "I was reading and I forgot. Those are the same thing."

    call dinner_close from _call_dinner_close_54

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "The room is the room. The desk is the desk. The window is the window, and the rain is tapping it from the outside, which is where rain belongs."
    $ night_desk_line = "the window"
    call night_open from _call_night_open_54

    menu:
        "[tag_insight] Rank 3: Ask what the book was that she forgot to eat over." if has_attribute("insight", 3):
            mc "You forgot to eat because you were reading. What was the book?"
            hikari "A person who keeps waking up in a house that is almost hers."
            mc "Does it end well?"
            hikari "I have not got there. I keep starting the same chapter."
            mc "(She says it to the wall. I do not ask whether she means the book.)"
            $ log_memory("hikari", "was holding a book about a person who keeps waking in a house that is almost hers")
            $ reward_attributes_once("day54_night_book", [("insight", "micro")], show="auto")
        "Ask how she spent Sunday.":
            hikari "It was a Sunday. I read. I forgot to eat. You went out."
            mc "That is all?"
            hikari "That is all a Sunday needs to be. Not every day is a lecture."
            mc "(She is right. Not every day is a lecture. Some days are just the space between lectures, and that is what they are for.)"
            $ log_memory("hikari", "said not every day is a lecture, and some days are just the space between")
            $ reward_attributes_once("day54_night_a", [("grace", "micro")], show="auto")
        "Tell her the dreams have stopped.":
            mc "I dreamed for three nights. Last night I did not."
            hikari "That is good."
            mc "I am not sure. The dreaming felt like something was trying to tell me something. The not dreaming feels like it gave up."
            hikari "Or it finished. Messages do not repeat once you have heard them."
            mc "(She says that like she knows. Like she has received messages and heard them and moved on. I do not ask.)"
            $ log_memory("hikari", "said the dreams might have finished, that messages do not repeat once heard")
            $ reward_attributes_once("day54_night_b", [("nerve", "micro")], show="auto")
        "Let the city talk first.":
            "I do not talk. The rain is on the window and the city is doing its Sunday sounds: a distant train, a bell, a scooter that goes and does not come back."
            "Hikari is on the floor with her book. She is not reading. She is holding the book and looking at the wall, and I do not ask what she sees there."
            $ log_memory("hikari", "was holding a book and looking at the wall, and I did not ask what she saw")
            $ reward_attributes_once("day54_night_c", [("insight", "micro")], show="auto")
        "Ask what is still a closed door." if all_confidants_met():
            mc "Is there anyone here I have not met yet?"
            hikari "You keep asking that."
            mc "You keep not answering."
            hikari "Because the answer is the same. There are rooms I have never walked into. But you keep finding doors."
            mc "(She says it the same way she said it the first time. Word for word. I do not think she notices. I do not think it is a performance.)"
            $ log_memory("hikari", "repeated her answer about closed doors word for word, and did not notice")
            $ reward_attributes_once("day54_night_d", [("insight", "micro")], show="auto")

    call night_close from _call_night_close_54

    call corruption_night from _call_corruption_night_54

    "I turn off the lamp. The room is dark. The room is fine."
    "Then I see it. In the corner. The laundry rack."
    "Mother took it down two weeks ago. I watched her fold it and put it in the closet. It is back. It is standing in the corner where it used to stand, fully extended, with nothing on it."
    mc "(She put it back. That is all. She put it back because the rain is heavy and she needed to dry something inside. That is what laundry racks are for.)"
    "I stare at it for a long time. It stares back, the way furniture stares, which is not at all, which is worse."
    $ collect_notebook_line(54)

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
