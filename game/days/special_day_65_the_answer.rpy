label special_day_65_the_answer:
    $ set_story_day(65)
    call day_transition from _call_day_transition_65
    $ flush_pending_messages()

    scene bg_lecture_hall with walk_fade
    "The professor hands out a short review sheet. Two questions. The first is about the lecture. The second asks for an example of a city keeping something after it has stopped needing it."
    "I start to write about the rail. Then I cross it out."
    professor "You can use something you have seen. It does not have to be in the reading."
    "Under the second question, in the space he left for an answer, there's a third. The tail of the first letter bends back on itself. Mine always does that."
    "What would you take with you?"

    menu:
        "Write: Something that reminds me of home.":
            "I write it small. There is enough room to change my mind."
            $ act3_exam_reply = "home"
        "Write: I don't know yet.":
            "I leave the word yet at the end. It feels important to leave it there."
            $ act3_exam_reply = "unsure"
        "Leave it blank.":
            "I cap my pen and set it across the page."
            $ act3_exam_reply = "blank"
        "[tag_nerve] Rank 3: Write that this question wasn't on the sheet." if has_attribute("nerve", 3):
            "I write beside the question: This wasn't here when you handed it to me."
            "I put a box around it so it can't be mistaken for an answer."
            $ act3_exam_reply = "objection"

    "The professor comes down my row. I put my hand on the bottom of the sheet so he can't take it yet."
    "Under my hand, there's a line in blue ink. I've been writing in black."
    "I don't need to take anything. I'll be back tomorrow."
    professor "Are you finished?"
    mc "Can I keep this one?"
    "He looks at the stack in his hand."
    professor "Yes. I have plenty."
    $ remember("mc", "a third question appeared on the review sheet in his own handwriting, and the answer changed in blue ink in the record", "ghost_question_delivered")
    "I fold the sheet with the blue ink on the inside."

    scene bg_room_night with Dissolve(0.8)
    $ room_ambient(True)
    "I leave the paper under the torch. Before I go to sleep, I check that neither of them has moved."
    stop ambient fadeout 0.5

    scene hospital_flash:
        blur 38
    with Dissolve(0.8)
    "There are two voices. I can't tell which side of the bed either of them is on."
    if act3_exam_reply == "blank":
        "He left it blank."
    elif act3_exam_reply == "objection":
        "He wasn't answering. He was asking us to look at the question."
    else:
        "That's not what he wrote."
    "It's the answer on record."
    "I watched the record change."
    "Somebody pulls a chair out. It makes a sound like a desk on the floor of a classroom."
    "Can we give him one morning without a test?"
    "We did. He went to class."

    scene black with Dissolve(0.8)
    jump act2_day_router

default act3_exam_reply = None
