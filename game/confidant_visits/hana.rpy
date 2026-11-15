################################################################################
## HANA — READING CLUB
################################################################################
##
## Visit 1 happened in script.rpy, on the Saturday library errand: the haiku
## handout, the quiet room, the girl who flees, and the book left on the desk.
## Everything after that lives here. The arc follows the documentation under
## Reading Club - Hana/: observation, tiny attempts at connection, the art book
## revelation, the shared silence, the confession, and the final farewell where
## she leaves to pursue art.

label confidant_visit_hana:
    $ visit = confidant_visits.get("hana", 0)
    if visit == 1:
        jump hana_visit_02
    elif visit == 2:
        jump hana_visit_03
    elif visit == 3:
        jump hana_visit_04
    elif visit == 4:
        jump hana_visit_05
    elif visit == 5:
        jump hana_visit_06
    elif visit == 6:
        jump hana_visit_07
    elif visit >= 7:
        jump hana_visit_closed
    return

label hana_common_open:
    scene bg_library with walk_fade
    stop music fadeout 1.2
    play music "audio/Music/(Hanami? Nature setting?) tea_under_the_canopy.mp3" fadein 2.0
    $ phone_map_visit("school")
    return

label hana_visit_02:
    call hana_common_open

    "The window light is thinner today — late afternoon, everything turning amber."
    "The usual readers are in their usual seats. The ceiling fan ticks its slow clock."
    "I take the same table as last time. The book she left is in my bag, and I still don't know what to do with it."
    "I set it on the table, spine out, in case she's watching."

    "I read. Ten minutes. Twenty. Nothing."

    "And then — a shadow at the edge of my table. She's there, a stack of returns balanced against her chest, so close I can see the loose thread on her sleeve."
    "She sets a book down near mine. Not on my table. Just... near it. Close enough to be meant."

    "She doesn't leave immediately this time. She pauses — half a second, one full second — hovering as if she's going to say something."
    "Then she turns and walks back toward the shelves."

    "That's when I see it. Pinned to her collar. A small plastic badge, printed in plain lettering."

    hana "Hana."

    "So that's her name."

    menu:
        "\"Hana... thanks. For the book.\"":
            mc "Hana... thanks. For the book."
            "She stops. Her shoulders go rigid. Slowly — like turning a key in a rusted lock — she half-turns toward me."
            "She doesn't speak. She bows. A quick, deep bow, eyes on the floor, then straightens and disappears into the shelves."
            $ reward_attributes_once("hana_visit_02_thanks", [("grace", "micro")], show="auto")
        "(Watch her quietly)":
            "I don't say anything. I just watch her walk away, the way you watch a bird you don't want to startle."
            "She doesn't stop, but her walk slows for a moment. As if she's waiting for something that doesn't come."
            $ reward_attributes_once("hana_visit_02_quiet", [("insight", "micro")], show="auto")

    "The student from last week slides into the chair beside me, following my gaze."

    quiet_student "See? That right there? That was practically a conversation, for her."

    mc "That was a bow."

    quiet_student "Yeah. That's a lot for Hana."
    quiet_student "She's like a ghost. Shows up, disappears. Honest? I don't think she has any friends. Not one. People give up on her after a week or two."

    "I look at the book she left. Then at the empty space where she was standing."

    "The hour ends. Regulars drift out. I stay a little longer than I need to, turning the book over in my hands."
    "At the very back, just inside the cover, someone has pencilled a small, private star next to the title. Faint. Practically invisible."

    "I put the book in my bag."

    $ hana_affection += 1
    $ confidant_visits["hana"] = max(confidant_visits.get("hana", 0), 2)
    $ remember("hana", "learned her name from her badge and saw she left a star in the book")
    $ queue_message("hana", "The book... the one with the star. I hope you liked it. Please come back.", day="yesterday")
    $ reward_attributes_once("hana_visit_02_close", [("grace", "micro")], show="card")

    scene bg_campus_interior with walk_fade
    stop music fadeout 2.0
    return

label hana_visit_03:
    call hana_common_open

    "Rain outside. The club room feels smaller and warmer for it — coats over chair backs, umbrellas leaning by the door."
    "The window is a blur of grey light. Everyone reads a little slower on days like this."

    "Three weeks now. The book she left is on my shelf at home. I still haven't figured out how to say thank you in a way she'd let me finish."

    "I'm actually reading this time. Deep enough that I don't notice her until she's already there."

    "A shadow. She's standing at the end of my table, holding a book in both hands like it might evaporate."
    "Her mouth opens."

    hana "...Um."

    "That's it. One sound. So small I'm not even sure it happened."

    menu:
        "\"...What? Sorry, I didn't catch that.\"":
            mc "...What? Sorry, I didn't catch that."
            "Her whole body flinches, like I'd shouted. She bows — too fast, too deep — and backs away, nearly knocking a chair."
            "Then she's gone through the side door, and the only evidence she was ever here is the chair still rocking."
            $ reward_attributes_once("hana_visit_03_whisper", [("grace", "micro")], show="auto")
        "(Wait silently)":
            "I wait, giving her space to try again. But she's already retreating, her courage spent in that one half-word."
            "She bows quickly and slips out the side door, vanishing before I can react."
            $ reward_attributes_once("hana_visit_03_wait", [("insight", "micro")], show="auto")

    "I shouldn't have said anything. Or — I don't know. I didn't do anything wrong. So why does it feel like something broke?"

    "The student next to me chuckles softly, without looking up from the page."

    quiet_student "Told you. Impossible to talk to. Don't take it personally — everyone tries once."

    mc "She almost said something."

    quiet_student "She does that. Every few weeks, some new person, some new half-word. Then she bails. It's like she wants to, and then... her body vetoes her."

    "I stare at the side door."

    "Almost. She almost said something. That has to mean something, right? You don't try four times with someone you want to forget."

    "The hour ends. I pack up slowly. As I reach for my coat, I notice something on the floor by my chair — a thin corner of paper, half-tucked under the leg of the table."
    "I pull it free."

    "A torn corner of a page. On it, in careful pencil: half a drawing of a window with rain on it. Finished right up to the last two raindrops. Then abandoned."

    "I fold it and put it in my pocket."

    $ hana_affection += 1
    $ confidant_visits["hana"] = max(confidant_visits.get("hana", 0), 3)
    $ remember("hana", "heard her first word attempt and found a rain window drawing she dropped")
    $ queue_message("hana", "I... I tried to say something. I couldn't. The words wouldn't come. I'm sorry.", day="yesterday")
    $ reward_attributes_once("hana_visit_03_close", [("insight", "micro")], show="card")

    scene bg_campus_interior with walk_fade
    stop music fadeout 2.0
    return

label hana_visit_04:
    call hana_common_open

    "The room is nearly empty today. Two other readers, both lost in their own books."
    "The blinds are open for once, and the late sun lays a long bright stripe across the floor, right down the middle of the room."

    "She's standing at the far end of that stripe. And she's looking at me."

    "Actually looking. Not glancing. For the first time, Hana is holding my gaze — and she's holding something else, too."
    "A large, heavy book, clutched against her chest with both arms, cover turned outward."

    "I can read the title from here. 'Impressionist Masters.'"

    "She takes one step. Then another. Halfway across the room — right at the edge of the sunlight — she stops."

    "Her grip tightens. Her knuckles go pale against the spine. She looks at me, then at the book, then at the floor."
    "Her mouth moves, but nothing comes out."

    "Then she hugs the book to her chest like it's the only warm thing in the building, turns, and retreats behind the shelves. Quiet. Fast. Certain."

    "She made it exactly as far as the light reaches. Not one step further."

    "I sat there with my heart going. Because I understood something, suddenly."
    "She wasn't trying to hand me a book. She was trying to hand me the thing she hides. And she got all the way to the edge of it and her courage ran out."

    "The book is still on the shelf where she took it from. I know, because there's a gap in the row."

    menu:
        "Get up and pull a matching art book off the shelf.":
            mc "I walk to the art section, slow as I can. I put my hand on a book from the same row — another volume on the Impressionists — and take it back to my seat."
            "I don't look toward the shelves. I just open it, out in the open, where she can see. I read for the rest of the hour with a painting of a water garden on the cover."
            $ reward_attributes_once("hana_visit_04_match", [("nerve", "micro")], show="auto")
        "Stay where I am. Don't spook her.":
            mc "I don't move. If she's watching, I want her to see me stay. Staying is the only thing I have that costs nothing and says everything."
            $ reward_attributes_once("hana_visit_04_stay", [("grace", "micro")], show="auto")

    "Somewhere behind the shelves, a page turns. Then another. She's still here. She didn't leave the room this time."

    "She's reading. Just on the other side of the row. Our books back to back across a wall of paper."

    "The hour ends. When I stand to leave, the gap in the art shelf is filled. She reshelved it — but not in its old place."
    "She put it right at the end of the row, where I'd have to walk past it. Right where someone sitting in my chair would see it on the way out."

    $ hana_affection += 1
    $ confidant_visits["hana"] = max(confidant_visits.get("hana", 0), 4)
    $ remember("hana", "she brought an art book and he responded with a matching one; they read back-to-back")
    $ queue_message("hana", "You... you saw. The art book. You picked one too. That means... that means you understand.", day="yesterday")
    $ reward_attributes_once("hana_visit_04_close", [("nerve", "micro")], show="card")

    scene bg_campus_interior with walk_fade
    stop music fadeout 2.0
    return

label hana_visit_05:
    call hana_common_open

    "Warm, drowsy afternoon light. Fewer readers than usual — just three of us and the ticking fan."
    "The room has that slumped, unhurried feel of a place that knows everyone is tired."

    "I take my usual seat and spread out my book, expecting the usual: a book left near my table, a shadow at the edge of my vision, a bow, gone."

    "Instead, she sits down."

    "Hana sets a book on the same table. Not near it — on it. She pulls out the chair across from me, sits down stiffly, and opens the book to a random page."
    "She holds it up in front of her face like a shield."

    "She's pretending to read. Badly. The book is upside down."

    menu:
        "Don't say anything. Just read.":
            mc "I don't say anything. I don't think I breathe. I just open my own book and try to keep my eyes on the page."
            $ reward_attributes_once("hana_visit_05_quiet", [("grace", "micro")], show="auto")
        "Pretend not to notice.":
            mc "I turn a page carefully, like the upside-down book is perfectly normal. If she wants to be invisible, I'll let her be invisible."
            $ reward_attributes_once("hana_visit_05_pretend", [("insight", "micro")], show="auto")

    "After a while, I feel it — the tiny weight of being watched. I glance up. Over the top edge of her book, her eyes flick away, and the book rises another inch to hide her face."

    "She peeked. She peeked at me."

    "We sit like that for most of the hour. Two people reading badly. Neither of us turning a page."

    "The hour ends. Chairs scrape. People pack up. Hana stays very still until I start to gather my things — then, in a single quick motion, she stands and heads for the door."
    "She doesn't look at me. She doesn't bow."

    "On the table, where her book was, there's a small square of folded paper. Folded four times, edges lined up with obsessive care, sitting dead centre in the space between where we were sitting."

    "I wait until she's gone to pick it up."

    "Inside, in careful pencil, in handwriting that's small enough to fit on a train ticket:"

    hana "Arigatou... Thank you... for not giving up on me."

    "Nothing else. No signature. No smiley. Just those seven words, and the ghost of an eraser mark beneath the final line, like she'd written it more than once before getting it right."

    "I read it three times standing by the door. The room's empty now. The fan ticks. Somewhere below, the library stacks whisper as someone reshelves a cart."

    "I fold the note back exactly the way she'd folded it, along every crease, and put it in my pocket with the torn window drawing."

    $ hana_affection += 1
    $ confidant_visits["hana"] = max(confidant_visits.get("hana", 0), 5)
    $ remember("hana", "she sat at his table and left a note thanking him for not giving up")
    $ queue_message("hana", "The note... I was scared to leave it. But I wanted you to know. Thank you for staying.", day="yesterday")
    $ reward_attributes_once("hana_visit_05_close", [("grace", "micro")], show="card")

    scene bg_campus_interior with walk_fade
    stop music fadeout 2.0
    return

label hana_visit_06:
    call hana_common_open

    "It's raining again. The room is almost empty — just Hana and me and one student asleep over a textbook in the corner."
    "The blinds are down. The fan ticks. The rain makes the whole room sound like it's wrapped in cloth."

    "Hana is already at my table when I sit down. She has a large, soft-covered notebook in front of her, both hands flat on top of it, like she's keeping it from flying away."

    "She doesn't pretend to read this time. She just looks at me. Her eyes are wet, but not from crying — more like she's been holding her breath for a very long time and is finally, slowly, letting some of it out."

    hana "I... try. Going to... try. Please. Don't... fill in. If I stop. Don't. Please."

    menu:
        "\"Okay. Take your time.\"":
            mc "Okay. Take your time."
            $ reward_attributes_once("hana_visit_06_time", [("grace", "micro")], show="auto")
        "\"I'm listening.\"":
            mc "I'm listening."
            $ reward_attributes_once("hana_visit_06_listen", [("insight", "micro")], show="auto")

    hana "No friends. Not... not one. Don't... don't know when. When... when I stopped."

    hana "Hate it. Want to... to talk. But body... says no. Tried. Stood there. For... for hour. Said... nothing."

    "She looks down at her notebook."

    hana "Here for... art books. Real reason. Tell club... like shelving. Don't. Just want... near pictures."

    hana "Parents... lawyers. Both. Decided. University. Law school. Same office. Same life. Never ask... what I want. I never... tell them."

    hana "Feel... stuck. Like... person-shaped space. Where person... should be. Can't say anything. Can't... rebel. So I... hide. Here. In books. Under... arms."

    "A long silence. The rain fills it. Then, slowly, she pushes the notebook across the table toward me — with one finger, like she's surrendering a weapon."

    hana "You can... look. Never shown... anyone."

    "I open it."

    "I'd expected hidden sketches. Pencil doodles. What's actually in there stops me cold."
    "Page after page — ink and watercolour, ink and pencil — a city that's unmistakably Tokyo, but painted like nobody has ever looked at it properly."
    "Rain on a train window. The inside of a convenience store at 2 a.m. An old man feeding crows, drawn so gently he looks like he's about to cry."
    "A girl with her back to us, holding a book over her face. Her. Over and over. The same girl, from behind, from the side, always unfinished at the face."

    "The last page is dated. It's today."

    menu:
        "\"You should tell them how you feel.\"":
            mc "You should tell them how you feel. Your parents. About the art."
            hana "...How? I don't know how to say a sentence that long out loud."
            $ reward_attributes_once("hana_visit_06_tell", [("nerve", "micro")], show="auto")
        "\"These are incredible. Do you know that?\"":
            mc "These are incredible. Do you know that? You have real talent."
            hana "Just... doodling. But... thank you. Nobody... ever said that. Before."
            $ reward_attributes_once("hana_visit_06_incredible", [("grace", "micro")], show="auto")

    hana "First person... who stayed. Everyone else... gave up. After week. You just... kept showing up. Never asked me... to be normal."

    hana "Don't know... if I can. What you're saying. But... think I want... to try."

    "She closes the notebook, holds it against her chest, and for the first time all year — Hana smiles."
    "It's small and crooked and terrified, like a first step. But it's real."

    "The hour ends. She leaves before I do, but at the door she stops, half-turns, and bows. Not the fast panicked bow from before. A slow one. Deliberate. Thank you."

    $ hana_affection += 1
    $ confidant_visits["hana"] = max(confidant_visits.get("hana", 0), 6)
    $ remember("hana", "she confessed her loneliness and showed him her sketchbook full of Tokyo drawings")
    $ queue_message("hana", "I showed you. The drawings. Everything. I was so scared. But you didn't look away. Thank you.", day="yesterday")
    $ reward_attributes_once("hana_visit_06_close", [("insight", "micro")], show="card")

    scene bg_campus_interior with walk_fade
    stop music fadeout 2.0
    return

label hana_visit_07:
    call hana_common_open

    "The room is empty when I arrive. Blinds up, late sun, the shelves tidier than I've ever seen them — every spine aligned, every gap closed."
    "The fan ticks. It's the last hour the club meets this month."

    "It looks like someone finished everything and said goodbye to the room."

    "Hana is standing by the window, waiting. Not hiding behind a shelf. Not holding a book. Just standing, hands clasped, facing the door — waiting for me specifically."
    "When she sees me she doesn't look away."

    "She's trembling. But she's smiling."

    hana "I... I did it."

    menu:
        "\"...You told them?\"":
            mc "...You told them?"
            $ reward_attributes_once("hana_visit_07_told", [("insight", "micro")], show="auto")
        "\"You talked to your parents?\"":
            mc "You talked to your parents? About the art?"
            $ reward_attributes_once("hana_visit_07_parents", [("grace", "micro")], show="auto")

    hana "Last night. Both of them. Dinner table. I said... don't want to be lawyer. I said... want to draw. Said it all... at once. Because if I stopped... never start again."

    hana "They were... angry. But not... because of art. That's the part... can't stop thinking about."

    hana "Angry because... I hid it. For so long. Because I sat at table... every night. For years. Never said a word. They thought... I was fine."

    "She looks out the window, at the rooftops, at the city she's been drawing from behind glass her whole life."

    hana "Mother... cried. Father went quiet. The way he does. Then he said... they'd been afraid. Same thing. Made the plan because... thought I needed one. He said... he was sorry."

    hana "And I said... I was sorry too. For not... speaking."

    hana "We talked... until midnight. Really talked. Never... never done that. Never ended with me... winning anything before. Ended with me... going quiet."

    menu:
        "\"So what happens now?\"":
            mc "So what happens now?"
            hana "Now I apply... to art school. Part-time work. Evening classes. Going to be poor. Slow. Nobody impressed. But it's... mine."
            $ reward_attributes_once("hana_visit_07_now", [("insight", "micro")], show="auto")
        "\"Then you did win.\"":
            mc "Then you did win. You found a way to speak."
            hana "Maybe. Doesn't feel like winning. Feels like... putting something heavy down."
            $ reward_attributes_once("hana_visit_07_win", [("grace", "micro")], show="auto")

    "She reaches into her bag and takes out something small, wrapped in a square of plain paper. She holds it out with both hands — the way you hand someone something that matters."

    hana "This is for you. I made it. Not... very good."

    "I unwrap it. A small cloth strap — the kind you'd hang on a phone or a bag — with a tiny brush and a painter's palette stitched into it in coloured thread."
    "The stitching is uneven. Every stitch is deliberate."

    hana "Brush and palette. What I'm going to be... if I'm brave enough. Wanted you to carry it. So you don't... forget me."

    menu:
        "\"I won't forget you.\"":
            mc "I won't forget you."
            $ reward_attributes_once("hana_visit_07_forget", [("grace", "micro")], show="auto")
        "\"This means a lot to me.\"":
            mc "This means a lot to me. Thank you, Hana."
            $ reward_attributes_once("hana_visit_07_means", [("nerve", "micro")], show="auto")

    hana "No — not like that. For you... so you don't forget me. Like... like you carried my dream. When I couldn't. You kept showing up. Every week. Nobody... ever kept showing up."

    "She steps back and bows — slow, deep, the way she did at the door last time. Then she picks up her bag and walks out. Not fleeing. Walking."
    "At the door she stops for half a second and looks back one last time, and this time she holds my eyes for a full breath before she goes."

    "I stand in the empty club room for a while. The shelves are straight. The blinds are up. The fan ticks. There's nothing left here for her — she finished it, tidied it, and closed it."

    "I turn the small charm over in my hand. Uneven stitches. A brush and a palette."

    "Next week the club will still meet. Same room, same chairs, same books, same ticking fan. Someone else will shelve the returns. Hana won't be here."
    "She's somewhere out there, drawing, in a life she finally said out loud."

    $ hana_affection += 1
    $ confidant_visits["hana"] = max(confidant_visits.get("hana", 0), 7)
    $ remember("hana", "she told her parents the truth and gave him a handmade art charm before leaving")
    $ wire_contacts["hana"]["name"] = "Hana"
    $ queue_message("hana", "I did it. I told them. They were angry, then they listened, then they understood. I'm going to art school. Thank you for believing in me when I couldn't.", day="yesterday")
    $ reward_attributes_once("hana_visit_07_close", [("nerve", "micro")], show="card")

    scene bg_campus_interior with walk_fade
    stop music fadeout 3.0
    return

label hana_visit_closed:
    scene bg_library with walk_fade
    stop music fadeout 2.0
    $ phone_map_visit("school")

    "The reading club is still here. The shelves are still full. The fan still ticks."
    "But Hana is gone."

    "A different volunteer is shelving returns — someone I've never seen before. They don't move like Hana did. They don't hesitate before each book."

    quiet_student "Looking for Hana? She stopped coming. Something about art school."

    "I take my usual seat. The table feels larger without her. The silence feels different."

    "The book she left on my first visit is still in my bag. The rain window drawing is still in my pocket. The note is folded along every crease, exactly as she left it."
    "The charm hangs from my phone — brush and palette, uneven stitches, proof that courage comes in small handmade things."

    menu:
        "Leave quietly.":
            "I read for an hour, but it feels like practice. Some rituals survive the people who made them."
            $ reward_attributes_once("hana_visit_closed_quiet", [("grace", "micro")], show="auto")
        "Message her.":
            mc "I'll send her a message. Tell her the room misses her, but I'm glad she found her voice."
            $ reward_attributes_once("hana_visit_closed_message", [("nerve", "micro")], show="auto")

    "The hour ends. I pack up slowly. The fan ticks. Somewhere in the library, a door closes."
    "The room is just a room now. But for months, it was hers."

    $ hana_affection += 1
    $ confidant_visits["hana"] = max(confidant_visits.get("hana", 0), 8)
    $ remember("hana", "found the reading club without her; she left to pursue art")
    $ queue_message("hana", "The room is still there. The books are still there. But I'm not, and that's the point. Thank you for everything.", day="yesterday")
    $ reward_attributes_once("hana_visit_closed_close", [("grace", "micro")], show="card")

    scene bg_campus_interior with walk_fade
    stop music fadeout 3.0
    return
