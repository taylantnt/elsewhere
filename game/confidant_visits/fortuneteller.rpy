################################################################################
## THE FORTUNE TELLER: ASAKUSA
################################################################################
##
## Visit 1 happened in script.rpy, on the Day 13 walk to Asakusa: the omikuji,
## the white corridor coming back, the three cards, "the person who put you
## here is not the person you think," and the square WIRE code she pressed
## into his hand without being asked. `fortune_arc_started` opened the hub row.
##
## Her arc is not like the others. The five confidants are people he gets to
## know; she is a reader of the pages themselves. She does not predict the
## future so much as recite it, the days he has not lived yet, the choices
## he has not made, the questions that will be printed in his own handwriting.
## She is also the only confidant who knows what this place is, which is why
## her last visits sound less like a fortune and more like a warning.
##
## The chain is written: visit 2 is the two-card reading and the three
## prophecies; visit 3 is the corner she promised, where she gives "the last
## thing I am allowed to give you"; visit 4 proves she reads pages by naming
## his afternoon before he tells her; visit 5 admits the blank page, the part
## of the script that is his to write; visit 6 is the debt, because she has
## watched the other pages close; visit 7 is the last reading, and the corner
## is where she stays for whatever comes after. After that the row never
## closes: the corner remains.

label confidant_visit_fortune:
    $ visit = confidant_visits.get("fortune", 0)
    if visit <= 1:
        jump fortune_visit_02
    elif visit == 2:
        jump fortune_visit_03
    elif visit == 3:
        jump fortune_visit_04
    elif visit == 4:
        jump fortune_visit_05
    elif visit == 5:
        jump fortune_visit_06
    elif visit == 6:
        jump fortune_visit_07
    else:
        jump fortune_visit_closed

label fortune_common_open:
    scene bg_fortune_stall with walk_fade
    stop music fadeout 1.0
    "The incense burner is lit even when she is not. It is the only thing at the stall that never goes out."
    return


################################################################################
## VISIT 2: THE TWO CARDS
################################################################################
##
## The reading she promised: two cards face down, a third already in his
## pocket. One true thing, two pieces of noise, and she will not say which.
## This is the scene that used to be the whole arc; it is visit 2 now, and its
## "the deck is closed" is a table closing, not a story ending.

label fortune_visit_02:
    call fortune_common_open from _call_fortune_common_open
    "I take the train back to Asakusa. The afternoon is already going orange. The crowd is thinner than it was yesterday."
    "She is at the same folding table, between the incense burner and the souvenir stalls. She does not look surprised."
    fortune_teller "You came back."
    mc "You said the cards would change."
    fortune_teller "I said you would change them. The cards are only paper."
    "She lays two cards face down. There is no third card on the table."
    fortune_teller "The first card is a street. The second is a corner. The third is already in your pocket."
    mc "The omikuji."
    fortune_teller "The paper remembers what the hand forgets."
    "She turns over the first card. A narrow street with crepe stands and vintage shops. The crowd is a river of color."
    fortune_teller "Harajuku. You will walk it and forget why. That is not a warning. It is what the street is for."
    mc "And the second?"
    "She turns over the second card. A street corner at night. A streetlight. A house that looks like every other house."
    fortune_teller "The corner near your house. You will see me there. I will not have a table."
    mc "What will you have?"
    fortune_teller "The last thing I am allowed to give you."
    "She puts the cards away. She does not offer a third question. She does not offer a price."
    fortune_teller "One true thing, and two pieces of noise. That is the rule."
    mc "Which is which?"
    fortune_teller "If I told you, it would be three true things. That is not the rule."
    "She looks at me for a long moment. The smoke from the burner drifts between us."
    fortune_teller "The person who put you here is not the person you think."
    fortune_teller "Beware of vending machines that do not take coins."
    fortune_teller "The cat on the wall is not a cat."
    mc "(One of those is true. I do not know which. I think I do. I hope I am wrong.)"
    "She folds the table. This time I watch her hands. They are ordinary hands. They are not doing anything unusual."
    fortune_teller "That is all three. The deck is closed."
    mc "Will I see you again?"
    fortune_teller "You will see me on the corner. That is not the same as seeing me again."
    "She walks into the crowd. The table is gone. The brass bowl is gone. There is only the smoke and the sound of the temple."

    $ confidant_visits["fortune"] = max(confidant_visits.get("fortune", 0), 2)
    $ log_memory("hikari", "went back to the fortune teller alone and was told the deck was closed")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


################################################################################
## VISIT 3: THE CORNER
################################################################################
##
## The prophecy kept. No table, no burner, no price, just her on the step
## under the streetlight near his house, and the last thing she is allowed
## to give. It is a warning about a test that has not happened yet: the
## ghost question, printed in his own handwriting, is coming.

label fortune_visit_03:
    scene bg_home_exterior_night with walk_fade
    $ night_street()

    "It is not a meeting. It is a corner I happen to be walking past at an hour I did not plan to be out."
    "The streetlight is the only one working on the block. Under it, on the bottom step of a house that is not mine, sits a woman with a folding table's worth of patience and no table."
    "She is wearing the same coat. She is holding a paper cup of something hot that is not tea."
    fortune_teller "You found the corner."
    mc "You said I would see you here."
    fortune_teller "I said I would not have a table. I did not say I would be hard to find."

    menu:
        "Ask what the last thing is." :
            mc "The last thing you are allowed to give me. What is it?"
            fortune_teller "A warning. Warnings are cheaper than answers, so I am allowed more of them."
            $ reward_attributes_once("fortune_v3_warning", [("insight", "micro")], show="auto")
        "Ask why there is no table." :
            mc "Where is the table? The burner? The whole stall?"
            fortune_teller "Folded. Some days the table is a table. Some days it is a step. The reading is the same size either way."
            $ reward_attributes_once("fortune_v3_table", [("grace", "micro")], show="auto")
        "Ask if this is a dream." :
            mc "Is this a dream?"
            fortune_teller "If it were, the streetlight would be kinder to you."
            mc "(She says it flatly. It is not an answer. It is better than an answer.)"
            $ reward_attributes_once("fortune_v3_dream", [("nerve", "micro")], show="auto")

    "She turns the paper cup slowly. The steam goes up and does not come back down."
    fortune_teller "In six days a man will hand you a page with three questions on it. You will know two of them. The third will be in your own handwriting, and it will not have been there a moment before."
    mc "...What?"
    fortune_teller "Do not be afraid of the question. Be afraid of what writes it."
    mc "(The white corridor. The voice that called me a name I was not given. She is describing something I have not told her about.)"
    mc "When did you see this?"
    fortune_teller "Pages do not have times. They have order. Yours comes before mine."
    "She reaches into her coat and takes out a small folded square of paper. Not a card. A page, folded once, worn soft at the creases."
    fortune_teller "This is the last thing. For the day you need it more than the day I give it to you."
    "She puts it in my hand and closes my fingers around it. Her hands are cold. The paper is warm."
    fortune_teller "Do not read it tonight. Some pages only work if you are not looking at them."
    mc "What does it say?"
    fortune_teller "You will know when you are standing on it."

    $ confidant_visits["fortune"] = max(confidant_visits.get("fortune", 0), 3)
    $ remember("mc", "received a folded page from the fortune teller that must not be read until he is standing on it", "fortune_folded_page")
    $ queue_message("fortune", "The corner stays lit after I fold. If you need the page, you know where to stand.", day="yesterday")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


################################################################################
## VISIT 4: THE PAGES
################################################################################
##
## The table is back, tables do that. She proves she reads ahead by naming
## his afternoon before he tells her, then lays three cards face down and
## refuses to turn them: the endings. She can see the script; she cannot , 
## or will not, choose which page he stands on.

label fortune_visit_04:
    call fortune_common_open from _call_fortune_common_open_1

    "The folding table is back in its spot between the incense burner and the souvenir stalls, like it never left."
    "She does not look up when I sit. She is already reading."
    fortune_teller "You came from the river side. You walked the long way because the short way has a slope you are tired of."
    mc "...How do you know that?"
    fortune_teller "I read the page."
    mc "What page?"
    fortune_teller "Yours. You are standing on it."
    $ tour_place_name = destination_names.get(last_afternoon_place, "somewhere") if last_afternoon_place else "nowhere"
    if last_afternoon_place:
        fortune_teller "This afternoon you went to [tour_place_name]. You spent money you did not need to spend, and you came home with one small thing you will keep."
        mc "(She is right. I did all of those things. I have not told her any of them.)"
    else:
        fortune_teller "This afternoon you went nowhere on purpose. You sat with it. Most people cannot."
        mc "(I did sit with it. I did not plan to tell her that either.)"

    menu:
        "Ask what else is on the page." :
            mc "What else is written?"
            fortune_teller "Tomorrow. The day after. The day after that. Pages are cheap. Choices are the expensive part."
            $ reward_attributes_once("fortune_v4_pages", [("insight", "micro")], show="auto")
        "Ask if she can change it." :
            mc "Can you change it? The page?"
            fortune_teller "I turn cards. I do not write them."
            $ reward_attributes_once("fortune_v4_change", [("nerve", "micro")], show="auto")
        "Ask why she reads at all." :
            mc "Why do you do this? Reading pages for strangers."
            fortune_teller "Because somebody has to keep count of what is being spent."
            mc "(Spent. The word lands differently than I expected.)"
            $ reward_attributes_once("fortune_v4_why", [("grace", "micro")], show="auto")

    "She lays three cards face down in a row. This time there is no fourth card up her sleeve. There are only three."
    fortune_teller "Three cards. Three endings. I have dealt them before."
    mc "What are they?"
    fortune_teller "One has you walking out of a door. One has you staying at a table. One has you never arriving at all."
    mc "That's not helpful."
    fortune_teller "It is the most honest thing I own. Helpfulness is a service. Honesty is a material."
    mc "Which one am I on?"
    fortune_teller "You are on all three until you pick up the pen."
    "She gathers the cards without turning them. The smoke leans toward her and away, like it is making a decision."
    fortune_teller "Do not ask me to turn them. I have already turned them. You are the one who has to live them."

    $ confidant_visits["fortune"] = max(confidant_visits.get("fortune", 0), 4)
    $ remember("mc", "the three face-down cards named the three endings: out of a door, at a table, never arriving", "fortune_three_endings")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


################################################################################
## VISIT 5: THE BLANK PAGE
################################################################################
##
## The limit of her sight. There is a page she cannot read, blank, unwritten,
## his to fill, and a warning that someone else is reading over her shoulder.
## The first real hint that the reader of the script is not the only audience.

label fortune_visit_05:
    call fortune_common_open from _call_fortune_common_open_2

    "She is not at the table today. She is standing at the edge of the crowd with her back to the incense, watching the temple like it owes her money."
    "When she sees me, she does not smile. She has not smiled at me once."
    fortune_teller "You came back faster than the page said you would."
    mc "What does that mean?"
    fortune_teller "It means the page moved. Somebody is reading ahead of me."

    menu:
        "Ask who is reading." :
            mc "Who is reading ahead of you?"
            fortune_teller "I do not know their face. I know their patience. It is the patience of a man who has already read the ending and is only waiting for the middle to catch up."
            $ reward_attributes_once("fortune_v5_reader", [("insight", "micro")], show="auto")
        "Ask about the blank page." :
            mc "You said there is a page you cannot read."
            fortune_teller "There is a page in your book that is blank. Not unwritten, unwritable. It stays blank until you stand on it."
            mc "What's on it?"
            fortune_teller "Whatever you decide. That is the only page in the whole story that is yours."
            $ reward_attributes_once("fortune_v5_blank", [("nerve", "micro")], show="auto")
        "Ask if she is afraid." :
            mc "Are you afraid of what you see?"
            fortune_teller "I am afraid of what is allowed to see me."
            $ reward_attributes_once("fortune_v5_afraid", [("grace", "micro")], show="auto")

    "The crowd presses past us toward the temple. Somewhere a child is crying in a way that is not distress."
    fortune_teller "One thing I can tell you for free. Stop looking for the door at the end of the corridor."
    mc "The corridor. The white one."
    fortune_teller "Yes. You keep walking toward it like it is a destination. It is not. It is a threshold. Thresholds are not places you arrive at. They are places you decide to cross."
    fortune_teller "When you see the person reading over my shoulder, do not look at their face. Look at what they are holding. The face is a costume. The hands are the truth."
    mc "(A pen? A page? Something else?)"
    fortune_teller "You will know the hands when you see them. Everyone in this city has the same hands. That is the problem."
    "She picks up her table cloth and folds it into a square, the way she folds everything, like the world is a document and she is its only careful reader."
    fortune_teller "Go. The page is moving and I am standing in the margin."

    $ confidant_visits["fortune"] = max(confidant_visits.get("fortune", 0), 5)
    $ log_memory("hikari", "told him about the blank page and warned him not to look at the reader's face")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


################################################################################
## VISIT 6: THE DEBT
################################################################################
##
## The emotional core of her arc. She has watched the other confidants' pages
## close, the bar shuttered, the shelf emptied, the booth gone, and she is
## asking, in her own sideways way, not to be left out of the ending. She
## cannot leave. She can only ask to be remembered.

label fortune_visit_06:
    call fortune_common_open from _call_fortune_common_open_3

    "The stall is quieter than it has ever been. Fewer stalls are open. The incense smoke is thinner."
    "She is alone at the table with three cups of tea and only one of them drunk."
    fortune_teller "Sit. You are the only one left who comes."
    mc "The others?"
    fortune_teller "Their pages are closing. I can see the ink running out. The bar is folded. The cafe has new hands. The shelf is being straightened by someone who does not know my name for it."
    mc "...You can see them leave?"
    fortune_teller "I have watched four pages end this month. Yours is the only one still being written."
    "She finally looks at me. Her eyes are the color of the smoke."
    fortune_teller "I am not asking you to stay. I am asking you to remember."

    menu:
        "Ask what she wants him to remember." :
            mc "Remember what, exactly?"
            fortune_teller "The smoke. The corner. The sound of a table being folded. When they are gone, the city will keep going like nothing happened. You have to be the one who says it happened."
            $ reward_attributes_once("fortune_v6_remember", [("grace", "micro")], show="auto")
        "Ask if she is leaving too." :
            mc "Are you leaving? Like the others?"
            fortune_teller "I was never a page. I am the margin. Margins do not end. They are what is left when the writing stops."
            mc "(That is either the saddest or the most hopeful thing anyone has said to me in this country.)"
            $ reward_attributes_once("fortune_v6_margin", [("insight", "micro")], show="auto")
        "Ask what she sees at the end." :
            mc "What do you see at the end? For me."
            fortune_teller "I see you standing in a room that is not this one. There is a woman beside the bed who looks like someone you love. She is older. She is tired. She is real."
            mc "...That is the ending?"
            fortune_teller "That is one of them. The other two are quieter. I will not say which one you will get."
            $ reward_attributes_once("fortune_v6_ending", [("nerve", "micro")], show="auto")

    "She pours the second cup of tea. It is still hot. She does not drink it."
    fortune_teller "One thing. When it is my turn, and it will be my turn, they always come for the margin last, do not let them fold the table while I am still talking."
    mc "You won't be gone?"
    fortune_teller "I will be gone from the stall. I will not be gone from the smoke."
    "She stands. The table folds itself, or she folds it; I do not see which."
    fortune_teller "Go home. The night is a page too, and yours is almost turned."

    $ confidant_visits["fortune"] = max(confidant_visits.get("fortune", 0), 6)
    $ log_memory("hikari", "asked her to remember the smoke and promised not to let them fold the table while she was still talking")
    $ queue_message("fortune", "The smoke remembers what the table forgets. Come back before the last page turns.", day="yesterday")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


################################################################################
## VISIT 7: THE LAST READING
################################################################################
##
## The farewell. The stall is half-packed, the incense is down to its last
## coil, and she deals one final card, not an ending, but the corner itself.
## After this the row stays open forever: the corner remains, and so does she.

label fortune_visit_07:
    call fortune_common_open from _call_fortune_common_open_4

    "The stall is half-packed. Crates are stacked where the souvenir racks were. The incense burner is down to its last coil, and the smoke is the color of weak tea."
    "She is sitting on the folding chair with the deck in her lap, shuffling it slowly, not dealing."
    fortune_teller "Last reading. I can feel it in the paper."
    mc "How do you know it's the last?"
    fortune_teller "Because I have run out of things I am allowed to say that are not also warnings."
    "She deals one card face up. It is the corner. The streetlight. The step. No table."
    fortune_teller "This is the last true thing: the door you keep looking for is not at the end of the corridor."
    mc "Then where?"
    fortune_teller "It is the question they will ask you. Whatever is on the other side of it, it has been waiting for you to knock."
    mc "(The ghost question. The one in my handwriting. She is not predicting it. She is telling me what it is.)"
    mc "What happens after I knock?"
    fortune_teller "That is the blank page. I cannot read it. Nobody can."
    "She turns the card toward me and slides it across the table."
    fortune_teller "Keep it. The corner is yours now."
    $ add_item("fortune_corner_card")
    fortune_teller "When they come for the table, and they will, they always come for the table, I will be on the corner. The streetlight stays lit after I fold."
    mc "Will I find you there?"
    fortune_teller "You will find the corner. Whether you find me depends on what you carried out of this place."
    fortune_teller "Carry the smoke. Carry the page. Carry the question. Do not carry the fear."

    menu:
        "Ask what she hopes I choose." :
            mc "Which ending do you hope I get?"
            fortune_teller "The one where you knock."
            mc "And if I don't?"
            fortune_teller "Then I will be on the corner anyway. Corners do not need endings. They just need someone to stand on them."
            $ reward_attributes_once("fortune_v7_knock", [("nerve", "micro")], show="auto")
        "Ask if she is afraid of the blank page." :
            mc "Aren't you afraid of the blank page?"
            fortune_teller "Every reader is afraid of the blank page. It is the only page that cannot be predicted. It is also the only page that matters."
            $ reward_attributes_once("fortune_v7_blank", [("insight", "micro")], show="auto")
        "Say thank you." :
            mc "Thank you. For the smoke. For the corner. For everything."
            fortune_teller "Do not thank me. I was paid in something better than money. I was paid in a person who kept coming back."
            $ reward_attributes_once("fortune_v7_thanks", [("grace", "micro")], show="auto")

    "She stands. The last coil of incense gives up its smoke. The table folds. The crates are already gone."
    fortune_teller "Go. The page is turning and I am almost out of margin."
    "She walks into the crowd. This time I do not watch her hands. I know they are ordinary."

    $ confidant_visits["fortune"] = max(confidant_visits.get("fortune", 0), 7)
    $ log_memory("hikari", "had his last reading with the fortune teller and was told to carry the smoke and the question")
    $ queue_message("fortune", "The corner is lit. The page is blank. Whatever you decide, decide it like it is yours.", day="yesterday")

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return


################################################################################
## EPILOGUE: THE CORNER, EMPTY
################################################################################
##
## The stall is gone. The corner is still there. The streetlight still works.
## She is not at the step tonight, or she is, and I am not seeing her. Either
## way the corner keeps its promise: it stays lit after she folds.
## Repeatable: the same corner, the same smoke in the air, the same question
## I am still carrying.

label fortune_visit_closed:
    scene bg_home_exterior_night with walk_fade
    $ night_street()

    "The corner is the same corner. The streetlight is the same streetlight. The step is empty."
    "There is no table. There is no burner. There is the faint smell of incense on the air, like the smoke has not quite finished leaving."
    mc "(She said the corner stays lit after she folds. It does. That is the whole point of a corner.)"
    mc "(I stand on the step for a moment. The page in my pocket is still warm. I do not read it. I am saving it for the day I am standing on it.)"
    mc "(Somewhere in this city a woman is folding a table that is not there anymore. The smoke remembers. I remember. That is enough.)"

    scene bg_home_exterior_night with walk_fade
    $ night_street()
    return
