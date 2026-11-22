################################################################################
## DAY 14: TUESDAY, APRIL 21, 2026
## The second week opens: one free afternoon, and everything it can hold.
################################################################################

label tuesday_week_two:
    $ set_story_day(14)
    call day_transition from _call_day_transition_7

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Tuesday comes in grey and quiet. The rain that Mother promised is somewhere else, but the air is damp with it."
    "I wake with the fortune slip still on the desk and the white corridor already fading, the way a dream fades when you try to look at it."
    mc "(It was not a dream. That is the part I cannot put down.)"

    "My phone buzzes once on the desk."

    if "tanaka" in wire_unlocked:
        $ run_chat("tanaka", [
            {"them": "Shift available. Four hours. Do not be late.", "options": [
                {"label": "\"I'll be there.\"",
                 "send": "I'll be there.",
                 "them": ["Good.", "Wear the shirt. The one with the collar."]},
                {"label": "\"What time?\"",
                 "send": "What time?",
                 "them": ["The time we agreed.", "You did not agree. That is why I am telling you."]},
            ]},
        ])
        mc "(He texts like a man filling out a form. Every word is in its box.)"
    else:
        $ run_chat("hikari", [
            {"them": "You're awake. I can hear you thinking from here.", "options": [
                {"label": "\"I'm not thinking.\"",
                 "send": "I'm not thinking.",
                 "them": ["You are. It's loud.", "Come down. There is rice."]},
                {"label": "\"I'm thinking about the corridor.\"",
                 "send": "I'm thinking about the corridor.",
                 "them": ["Then think about it at the table.", "The rice does not care, but I do."]},
            ]},
        ])
        mc "(She is already at the stairs. I can hear her.)"

    call murakami_daily_ping from _call_murakami_daily_ping_1

    scene bg_kitchen with walk_fade

    "The kitchen is quiet. Everyone is being kind without saying so."
    mother "Sit. Eat. You have class."
    father "And an afternoon."
    mc "An afternoon?"
    father "You have one every day. The question is what you do with it."
    hikari "He is going to do something useful. I can tell."
    mc "I have a job now."
    father "A job."
    mc "At the combini. Afternoon shift. Four hours."
    "Father puts down his newspaper. He looks at me for a moment that is longer than it needs to be."
    father "Good. A job is a thing you make every day."
    mother "He said that already."
    father "It is still true."
    mc "(I think he is proud. I will take that.)"

    scene bg_lecture_hall with walk_fade

    "The elective is in the small room on the second floor. Murakami is at the board with a piece of chalk and no notes."
    murakami "The city as a conversation."
    murakami "You have been in this country for two weeks. You have learned the words for hello and thank you and excuse me. You have learned which platform. You have learned to turn your shoes around."
    murakami "None of that is the language. The language is what happens when two people who do not understand each other decide to keep talking."
    mc "(I think of the combini. The cashier asking six questions in a row. Me answering yes, no, no, IC, no, no.)"
    murakami "A conversation is not a transfer of information. It is a room two people build and then leave."
    murakami "You have been building rooms all week. Today you get to choose which one to walk into."
    mc "That is a lot of responsibility for an afternoon."
    murakami "It is a lot of responsibility for a life. The afternoon is the practice."

    menu:
        "[tag_grace] Rank 2: Ask whether asking questions counts as building." if has_attribute("grace", 2):
            mc "Have I been building? These two weeks. Or only taking?"
            murakami "You asked me four questions today. That is building."
            mc "I thought I was only confused."
            murakami "Confusion is the first brick. Sit down."
            $ reward_attributes_once("day14_lecture_building", [("grace", "micro")], show="auto")
        "Ask how you know when a conversation is over.":
            mc "How do you know when a conversation is over?"
            murakami "When one of you stops building."
            mc "And if neither of you stops?"
            murakami "Then it is not a conversation. It is a habit."
            mc "(I think of Hikari. I think of the tea. I do not know which one this is.)"
            $ reward_attributes_once("day14_lecture_over", [("insight", "micro")], show="auto")
        "Ask whether a city can be wrong.":
            mc "Can a city be wrong?"
            murakami "A city can be unjust. It cannot be wrong. It is too many people for one answer."
            mc "That is a convenient thing to say."
            murakami "It is an accurate thing to say. Convenience is a bonus."
            $ reward_attributes_once("day14_lecture_wrong", [("nerve", "micro")], show="auto")
        "Write down the line about building rooms.":
            "I copy it into my notebook. The sentence looks like a diagram of the last two weeks."
            mc "(A room two people build and then leave. I have left a lot of rooms.)"
            $ reward_attributes_once("day14_lecture_rooms", [("grace", "micro")], show="auto")
    $ japanese_fluency = min(5, japanese_fluency + 1)

    scene bg_campus_interior with walk_fade

    "Hikari is waiting by the stairs with her bag already on her shoulder."
    hikari "The afternoon is yours."
    mc "You keep saying that."
    hikari "Because you keep looking at me like it is a trap."
    mc "It is a trap."
    hikari "It is an afternoon. The trap is optional."
    "She walks away before I can ask what that means."

    $ flush_pending_messages()
    call free_afternoon from _call_free_afternoon_5

    call dinner_open from _call_dinner_open_7

    father "And the afternoon?"
    mc "I used it."
    father "That is not what I asked."
    mc "It is the best answer I have."
    father "Then it is a good answer."
    mc "(That is the closest thing to a blessing this table gives.)"

    call dinner_close from _call_dinner_close_7

    ## WORK IS PLAYER-INITIATED. The afternoon shift is not an event that happens
    ## to him on this day. If he wants it, he picks "Convenience Store" from
    ## the JOBS row in free_afternoon above, and the shift plays in
    ## game/job_combini/ (the first one is tanaka_visit_01). Here the afternoon
    ## is simply over, whatever he chose.

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the window is open a crack. The city is doing its night sounds: a train, a scooter, a door."
    $ night_desk_line = "the week ahead"
    call night_open from _call_night_open_7

    menu:
        "Ask what she thinks happens next.":
            mc "What do you think happens next?"
            hikari "The midterm. Then the next midterm. Then the one after that."
            mc "That is not a story. That is a calendar."
            hikari "A calendar is just a story that hasn't happened yet."
            mc "(She says it like a joke. It does not land like one.)"
            $ log_memory("hikari", "asked what happens next, and she said a calendar is a story with the endings removed")
            $ reward_attributes_once("day14_night_next", [("insight", "micro")], show="auto")
        "Tell her about the job.":
            mc "The combini. The manager is teaching me the register."
            hikari "The manager."
            mc "Tanaka. He is not a manager. He is just there."
            hikari "That is how managers start."
            mc "(I do not tell her he looks like someone. I do not know how to say it.)"
            $ log_memory("hikari", "told her about the combini job and Tanaka")
            $ reward_attributes_once("day14_night_job", [("grace", "micro")], show="auto")
        "Say nothing. Listen to the city.":
            "I do not say anything. The window is open. The city comes in a piece at a time."
            "Hikari listens with me. She does not fill the silence."
            mc "(A room two people build and then leave. We are still building.)"
            $ log_memory("hikari", "listened to the city with him in silence")
            $ reward_attributes_once("day14_night_listen", [("nerve", "micro")], show="auto")

    call night_close from _call_night_close_7

    "The second week is not a fresh start. It is the first week, only harder."
    "I turn off the lamp. The room goes dark. The window is still open a crack."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump wednesday_preview
