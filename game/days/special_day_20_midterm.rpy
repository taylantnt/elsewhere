################################################################################
## DAY 20: MONDAY, APRIL 27, 2026
## The midterm. Written, practical, and a map. Plus one question he did not write.
################################################################################

label monday_midterm:
    $ set_story_day(20)
    call day_transition from _call_day_transition_13

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "The alarm does not ring. I have been awake for an hour."
    "Zero days. There is nothing left to count except the hours until ten."
    "The fourth card is under Mister Plum's bowl. I can see the edge of it through the glass."
    mc "(I am going to take it with me. I do not know why. I am not going to leave it here alone.)"

    "My phone buzzes."

    if "aya" in wire_unlocked:
        $ run_chat("aya", [
            {"them": "Good luck today. The cafe is quiet until eleven if you need somewhere to be nervous.", "options": [
                {"label": "\"I'll come after.\"",
                 "send": "I'll come after.",
                 "them": ["Then I will have something ready.", "Something with too much foam. You look like a person who needs too much foam."]},
                {"label": "\"I'm not nervous.\"",
                 "send": "I'm not nervous.",
                 "them": ["Of course not.", "The quiet table is still yours."]},
            ]},
        ])
        mc "(She is very good at giving a person a place to be. That is the whole cafe.)"
    else:
        $ run_chat("hikari", [
            {"them": "Today.", "options": [
                {"label": "\"Today.\"",
                 "send": "Today.",
                 "them": ["Eat something. Then come down.", "I will be at the table with the cards."]},
                {"label": "\"I'm ready.\"",
                 "send": "I'm ready.",
                 "them": ["You are not ready. You are awake. Those are different."]},
            ]},
        ])

    "Three knocks. Hikari opens the door with the tomato timer in her hand."
    hikari "I am holding this. You are not allowed to wind it today."
    mc "Why?"
    hikari "Because you wind it when you are thinking. Today you are not allowed to think until after eleven."
    mc "That's the whole exam."
    hikari "Then choose."
    "She takes the fourth card from under the fish bowl before I can stop her, looks at it, and puts it in her own pocket."
    hikari "I will keep this. You can have it back when you come home."
    mc "You saw the question."
    hikari "I wrote nothing. I looked at a card. That is allowed."
    mc "(She is taking the impossible question away from me. I should object. I do not.)"

    call murakami_daily_ping from _call_murakami_daily_ping_7

    scene bg_kitchen with walk_fade

    "There is a plum in the middle of everyone's rice. Father taps the table twice. Mother pretends not to see him doing it."
    mother "Eat the plum."
    mc "I'm eating it."
    hikari "The whole thing. Not just around it."
    father "A plum is not a puzzle. You do not have to go around it."
    mc "(I eat the plum. It is sour and it wakes me up more than the alarm would have.)"

    menu:
        "Ask Mother if she is nervous for me.":
            mc "Are you nervous?"
            mother "No."
            mc "That was fast."
            mother "I am past nervous. I made rice. There is nothing left to do."
            mc "(That is the most restful thing anybody has said to me in this country.)"
            $ reward_attributes_once("day20_kitchen_mother", [("grace", "micro")], show="auto")
        "Ask Father for advice.":
            mc "Any advice?"
            father "Answer the question they asked, not the question you wish they had asked."
            mc "That's it?"
            father "And if they ask you to draw a map, draw the street you actually walked, not the one you think you should have walked."
            $ reward_attributes_once("day20_kitchen_father", [("insight", "micro")], show="auto")
        "Let Hikari check the cards one last time.":
            "She takes the three cards from her pocket and holds them up like a referee."
            hikari "Kigo. Scripts. City. That is all. If they ask anything else, make something up and sound calm."
            mc "That is bad advice."
            hikari "It is emergency advice. Different drawer."
            $ reward_attributes_once("day20_kitchen_cards", [("nerve", "micro")], show="auto")

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The Monday street is a schedule with shoes on. I know where to stand on the platform now. I do not have to be told twice."
    "On the train I look at the strap where the sleeping man holds on. He is there. Of course he is there. He is a Monday person."
    "Between the station and the school there is a small shrine. Hikari tips her head at it as we pass."
    hikari "This was Edo before it was Tokyo. Eighteen sixty-eight, they changed the name. The shrine did not."
    mc "It just kept being a shrine."
    hikari "Mm. Oldest thing on the street."
    mc "(I have walked past it a hundred times without seeing it. Grey wood. A name on the gate I still cannot read.)"

    scene bg_school_gate with Fade(0.0, 0.0, 1.5)
    play music "audio/Music/school.mp3" fadein 1.5
    $ phone_map_visit("school")
    scene bg_campus_interior with walk_fade
    scene bg_quiz with walk_fade
    play music "audio/Music/classroom.mp3" fadein 1.0

    "The exam room is the lecture hall with the desks pulled apart. The professor is at the front with a stack of papers and no notes."
    professor "Good morning. Three parts. Written, practical, map. You have ninety minutes and then the practical takes twenty."
    mc "(Three parts. I have been hearing that sentence for six days.)"

    "He hands me the paper. It has three questions on it."
    "I look at the first one and my shoulders drop."
    mc "(The frog. The pond. The season. I know this. I actually know this.)"

    menu:
        "QUESTION ONE - Which word is the kigo in Bashou's old pond poem?":
            mc "The frog. Frog is spring. The water warm enough to hold a life."
            professor "Correct."
            "He says it the way he says the weather. But my hand is steady when I write the next answer, and it was not steady a moment ago."
            $ midterm_q1_correct = True
            $ reward_attributes_once("day20_exam_q1", [("insight", "micro")], show="auto")
        "QUESTION ONE - Say it is the syllable count.":
            "I write that the kigo is the five-seven-five count. The professor reads over my shoulder."
            professor "Five-seven-five counts sound. A kigo places a poem in a season. You have given me a ruler where I asked for a door."
            mc "(Well. At least I wrote something about a door. That is not the same and I know it now.)"
            $ midterm_q1_correct = False
        "QUESTION ONE - Say it is the poet's name.":
            "I write Bashou. The professor taps the paper once with one finger."
            professor "The poet is not the season. The poet is the person who noticed it. Look again."
            "I look again. The frog. Of course. The word was right there the whole time."
            $ midterm_q1_correct = False

    "Question two. Which script was called onnade, women's hand?"
    "I can hear Murakami in the room even though she is not in it: serious is always borrowed; the curves were called women's hand."
    menu:
        "Hiragana - the curves.":
            mc "Hiragana. The curves. It was called onnade, women's hand, because women wrote the private things in it."
            professor "Correct. And the novel was born there."
            mc "(She said that. I said it back. My hand knew before my mouth did.)"
            $ midterm_q2_correct = True
            $ reward_attributes_once("day20_exam_q2", [("insight", "micro")], show="auto")
        "Manyougana - the compromise.":
            "I write manyougana, the clumsy borrowed sounds. The professor shakes his head once."
            professor "A compromise is not a women's hand. Clumsy is not the same as private."
            $ midterm_q2_correct = False
        "Kanji - the serious one.":
            "I write kanji. I can almost hear Murakami saying that seriousness is always borrowed."
            professor "Kanji was the language of documents. Documents were written by men. Who does that leave?"
            "I cross it out. There is no time to write the right word beautifully, so I write it badly. Hiragana."
            $ midterm_q2_correct = False

    "Question three. What did the professor say a city is?"
    "Two answers are fighting in my head. His: a set of instructions. Hers: a conversation."
    menu:
        "A set of instructions.":
            mc "You said a city is a set of instructions. Walk here. Wait there. The instructions are written in stone and glass."
            professor "Correct. You have been attending."
            mc "(Murakami said a conversation. He said instructions. They are both true. The exam wanted the man in the room.)"
            $ midterm_q3_correct = True
            $ reward_attributes_once("day20_exam_q3", [("insight", "micro")], show="auto")
        "A conversation.":
            "I write that a city is a room two people build and then leave."
            "The professor reads it and is quiet for one beat longer than he was for the other answers."
            professor "That is Murakami's line. It is a good line. It is not my question."
            $ midterm_q3_correct = False
        "Both, depending on who is asking.":
            "I write that a city is instructions until somebody answers back, and then it is a conversation."
            "The professor looks at the page for a long time."
            professor "That is not what I said. It is also not wrong. I am going to allow it, which is a thing I do about once a year."
            $ midterm_q3_correct = True
            $ reward_attributes_once("day20_exam_both", [("nerve", "micro")], show="auto")

    "I turn the paper over to write the map."
    "There is a fourth question printed at the bottom. It was not there a moment ago."
    "ドアの向こうに何がある。"
    "What is on the other side of the door."
    "It is in my handwriting."
    "I look at my pocket. The fourth card is not there. Hikari has it. She is in the library with the tomato timer and a blue pen."
    "My mouth is dry. The room is the room. The professor is at the front, reading something. Nobody else is looking at my paper."

    call leak_audio from _call_leak_audio_6

    "I have ninety minutes. I spend one of them staring at the question. Then I write the honest answer, because it is the only one I have."
    "「白い廊下。その先に扉がある。」"
    "A white corridor. There is a door at the end of it."
    "I do not decorate it. I do not explain it. I put the pen down."

    $ professor_corridor_note = True

    "I draw the map from memory. The school gate. The station. The platform with the yellow line. The pharmacy on the corner. The small shrine I walked past a hundred times without seeing it. The street where the lanterns were."
    "I draw the festival street wider than the others. That is where my hand slows down."

    "The professor collects the papers. He stops at mine."
    "He reads the three answers. He reads the fourth. He does not change his face."
    "Then he takes a red pen and writes two words in the margin."
    "See me."
    mc "(Two words. Not a grade. Not a comment about the map. Two words.)"
    $ midterm_result = "see_me"

    professor "Practical. Stand up. Bring your card and nothing else."

    scene bg_combini with walk_fade
    play music "audio/Music/kombini.mp3" fadein 1.0
    play sound "audio/SFX/combini.mp3"

    "The practical happens in the combini two stops from campus. The whole class stands outside in a line while the professor gives the instruction."
    professor "Buy one thing. Ask the price. Say thank you. Leave. Thirty seconds. You are being graded on whether you were a person the whole time."
    "I am fourth in line. I watch the three before me. One bows too much. One points at everything. One says thank you to the door on the way out, which the professor writes down."

    "Then it is my turn. The door chimes twice."
    "Tanaka is at the register. He does not look up until I am standing in front of him."
    "I have practiced these phrases all week. They come out without my having to translate each word first."
    tanaka "いらっしゃいませ。"
    mc "おにぎりはいくらですか。"
    tanaka "百八十円です。"
    mc "一つ、お願いします。"
    "He scans it. He puts it in a bag. He holds the bag out with both hands."
    tanaka "ありがとうございました。"
    mc "ありがとうございました。"
    "I take the bag. I bow once. Twenty-nine seconds."
    tanaka "随分上手になりましたね。"
    mc "(I know 上手 means good at something. The rest is a guess, but his tone sounds like a compliment.)"
    mc "Thank you. I have been practising."
    tanaka "Practising is the job."
    mc "(He says it like a man filling out a form. Every word in its box. But he said it to me and not to the register.)"

    scene bg_quiz with walk_fade
    play music "audio/Music/classroom.mp3" fadein 1.0

    professor "Twenty-nine seconds. You asked the price. You thanked him. You left. You were a person the whole time."
    mc "Is that all?"
    professor "That is everything. Most people spend thirty seconds proving they are a tourist. You did not."
    mc "(Tanaka helped. I do not say that. The professor knows.)"

    "The last part is the map. I hand over the page with the festival street drawn too wide."
    "The professor looks at it for a moment."
    professor "You drew the street where the festival was."
    mc "I walked it yesterday. I drew what I saw."
    professor "Good. That is the whole test. You were looking."
    "He gathers the papers. He puts my exam on the top of the stack, face down."
    professor "See me tomorrow."

    "The exam is over. My hand still feels like it is holding a pen."
    "The rest of the day is mine. Nobody is grading where I walk or what I buy."
    mc "(One place, then home. The sentence has worn smooth from use.)"

    $ flush_pending_messages()
    call free_afternoon from _call_free_afternoon_11

    call dinner_open from _call_dinner_open_13

    mother "And?"
    mc "I knew the answers. That is the strange part. I thought I would not."
    hikari "Which ones did you get wrong?"
    mc "I don't know. He did not say."
    hikari "That is not an answer. That is a holding pattern."
    father "He said he knew them. That is the answer."
    mother "A plum works, then."
    mc "The plum worked."
    hikari "I am going to need a bigger plum next time."
    mc "(I do not tell them about the fourth question. Hikari knows. She has the card in her pocket.)"

    call dinner_close from _call_dinner_close_13

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    "Upstairs, the exam paper is on the desk. Two words in red in the margin. See me."
    "Mister Plum circles the bowl. The fourth card is back under the bowl, where Hikari put it while I was not looking."
    $ night_desk_line = "two red words"
    call night_open from _call_night_open_13

    menu:
        "[tag_insight] Rank 2: Point out she knew before you showed her." if has_attribute("insight", 2):
            mc "You knew it was on the paper. Before I told you."
            hikari "You told me with the card under the fish."
            mc "That is not the same as knowing."
            hikari "It is the same in this house."
            $ reward_attributes_once("day20_night_knew", [("insight", "micro")], show="auto")
        "Ask her about the fourth question on the paper.":
            mc "It was on the exam. The question. In my handwriting."
            hikari "I know."
            mc "You know? It was not there when the professor handed it out."
            hikari "You kept the card under the fish. Things that are kept under fish do not stay under fish."
            mc "That is not an explanation."
            hikari "It is the only one I have."
            $ log_memory("hikari", "said things kept under the goldfish bowl do not stay under the goldfish bowl")
            $ reward_attributes_once("day20_night_fourth", [("insight", "micro")], show="auto")
        "Tell her I wrote about the corridor.":
            mc "I wrote the honest answer. A white corridor with a door at the end."
            hikari "What did the professor say?"
            mc "He wrote 'see me.'"
            hikari "That is not a bad thing."
            mc "How do you know?"
            hikari "If it were a bad thing, he would have written it in black."
            $ log_memory("hikari", "said red ink means it is not a bad thing")
            $ reward_attributes_once("day20_night_red", [("grace", "micro")], show="auto")
        "Say nothing. Look at the two red words.":
            "I do not say anything. The words sit in the margin. They are not a grade. They are an invitation, and I have been told recently that an invitation can be declined."
            "I do not think I am going to decline this one."
            $ log_memory("hikari", "stared at the two red words on the exam paper and said nothing")
            $ reward_attributes_once("day20_night_quiet", [("nerve", "micro")], show="auto")

    call night_close from _call_night_close_13

    "One day. I knew the answers. I was a person in a shop for twenty-nine seconds. And there are two words in red in the margin."
    "Tomorrow is Tuesday. The professor wants to see me."
    "I switch off the lamp. The room goes dark. It does not go quiet."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump tuesday_results
