################################################################################
## ACT 3 PROPER: DAYS 70-83, THE INVESTIGATION
##
## The hub is closed, but the keepsakes are not. Each day takes the protagonist
## back to a place whose person is gone, and asks what that person left behind.
## The clues are optional. They change what Hikari can explain on Day 90, what
## the ending can prove, and how much of the truth the player has seen for
## themselves. They never lock the final route.
##
## The lab interludes are player-only. The protagonist does not see them and
## does not remember them. They are marked OUTSIDE THE SIMULATION and use the
## older Hikari and the Doctor, whose faces the protagonist has never seen.
## They explain the kitchen freezes, the notebook lines, and the backdoor the
## older Hikari builds into the world.
################################################################################

default investigation_clues = {}
default act4_evidence = 0

init python:
    def record_clue(key, text):
        store.investigation_clues[key] = text

image side doctor = At(Transform("images/characters/doctor.png", xysize=(256, 384), fit="contain"), portrait_idle)
image side nurse = At(Transform("images/characters/nurse.png", xysize=(256, 384), fit="contain"), portrait_idle)

init 999 python:
    # Outside the world, the Doctor and the real Hikari get faces. Inside it,
    # the dream voice stays faceless. That is the line this file must not blur.
    lab_doctor = Character("Doctor", color="#ff4444", callback=type_sound, image="doctor")
    lab_hikari = Character("Hikari", color="#ffb6c1", callback=type_sound, image="nurse")


################################################################################
## DAY 70: THE TABLE
################################################################################

label special_day_70_the_table:
    $ set_story_day(70)
    call day_transition from _call_day_transition_70
    $ flush_pending_messages()

    scene bg_kitchen with walk_fade

    "The house has stopped pretending the week is normal. Breakfast is early. Nobody talks about yesterday. Hikari puts a towel on the table and asks me to empty my bag."

    hikari "Everything they gave you. All of it."
    mc "Why?"
    hikari "Because I want to see what the world forgot to take back."

    "I put the keepsakes on the towel. The chopsticks. The camera strap. The badge. The folded sketch. The cloth charm. The page the fortune teller gave me."

    if has_item("chef_personal_chopsticks"):
        "The chopsticks are back in their paper. I wrapped them up again the night I brought them home, the way you wrap something you are not ready to use. Hikari turns the paper over."
        hikari "There is a number here."
        mc "A maker's mark."
        hikari "Makers put their names. This is a file number."
        "She reads it twice. The second time she does not move her lips."
        mc "(04 / N-7. I have seen that shape before. In the white corridor. On a screen I could not read.)"
    else:
        "The chopsticks are not there. I never asked for them. Hikari notices the gap and does not ask."

    if has_item("sim_camera_strap"):
        "The camera strap has a twist in it that Sim never fixed. Under the buckle, someone has written a date in pencil."
        hikari "That is not a date."
        mc "It has a year."
        hikari "It has the year after this one."

    if has_item("hana_art_charm"):
        "The charm is warm. It should not be warm. Hikari holds it for a second and puts it down."
        hikari "Hana stitched this. The thread is not from any shop here."
        mc "Where is it from?"
        hikari "Somewhere with better light."

    menu:
        "Write the paper's number in the notebook.":
            "I copy it exactly. The pen presses too hard and tears the page at the corner."
            mc "(If I lose the paper, I keep the number. If I lose the number, I keep the paper. That is the first rule of a thing that is trying to disappear.)"
            $ record_clue("chopsticks_code", "The chopsticks' wrapping is printed with a file number, not a maker's mark: 04 / N-7.")
            $ reward_attributes_once("day70_table_notebook", [("insight", "micro")], show="auto")
        "Ask Hikari what the number means.":
            mc "You know what it is."
            hikari "I know it is not a maker's mark."
            mc "That is not what I asked."
            hikari "I know."
            "She folds the paper along the same line it already has. She does not give it back."
            $ record_clue("chopsticks_code", "Hikari recognised the chopsticks' file number and would not explain it.")
            $ reward_attributes_once("day70_table_ask", [("grace", "micro")], show="auto")
        "Put the paper back in the bag.":
            "I fold the paper and put it away. Hikari watches me do it. Neither of us says the number out loud."
            $ reward_attributes_once("day70_table_put", [("nerve", "micro")], show="auto")

    call dinner_close from _call_dinner_close_70

    scene bg_kitchen_night with walk_fade
    play music "audio/Music/room_night.mp3" fadein 2.0

    "At midnight I come down for water."
    "Hikari is at the sink. The tap is running. Her hand is under it."
    "She is not moving."
    mc "Hikari."
    "She does not respond."
    mc "Hikari."
    "The water runs over her fingers and into the sink. The glass is already full. It has been full for a while."

    "Then she blinks. She turns off the tap. She looks at the glass in her other hand."

    hikari "I was getting water."
    mc "You were standing at the sink."
    hikari "I was getting water."
    "She says it the way a person says a line they have practiced. She does not look at me."

    "That night I dream of the white corridor. The door is open. Someone is standing on the other side. I cannot see her face."

    call lab_after_day_70 from _call_lab_after_day_70

    $ set_story_day(72)
    jump special_day_72_the_shop


label lab_after_day_70:
    scene bg_hospital2 with Dissolve(1.0)
    stop music fadeout 2.0
    play music "audio/Music/(Not decided) midnight_at_the_blue_room.mp3" fadein 2.0

    centered "{size=+8}OUTSIDE THE SIMULATION{/size}"
    "The room is white. The bed is white. The boy in it does not move."
    "A woman in a white coat stands at the monitor. She is older than the girl in the house. She has the same face."

    "The doctor's badge says TANAKA. In the world he is the man who sells me rice balls at the combini. He has never once looked at me the way he looks at the bed."

    lab_doctor "Consolidation at sixty-one percent. Stable."
    lab_hikari "He is asking questions."
    lab_doctor "Questions are data."
    lab_hikari "He asked the girl at the sink if she was all right. That is not data."

    "On the monitor, the kitchen. The girl at the sink. The boy behind her. The woman in the white coat watches both of them."

    lab_hikari "She is in there. The fragment."
    lab_doctor "The fragment is a leak. It was never meant to have a name."
    lab_hikari "It has mine."

    "The doctor writes something on a clipboard. The woman does not look away from the screen."

    lab_doctor "The subject is not to be told."
    lab_hikari "He is not a subject."
    lab_doctor "He is a number."

    "The woman in the white coat touches the screen. The girl in the kitchen does not feel it."

    lab_hikari "Then I will give the number a door."
    lab_doctor "That is not in the protocol."
    lab_hikari "Neither is she."

    "The woman's coat is creased. There is a cold cup of coffee by the monitor and she does not look at it. She has been here since the last shift ended."

    lab_hikari "I did not sign up to keep a person in a room and call it a result."
    lab_doctor "You signed the same page as the rest of us."
    lab_hikari "I was younger. The page was shorter."

    return


################################################################################
## DAY 72: THE SHOP
################################################################################

label special_day_72_the_shop:
    $ set_story_day(72)
    call day_transition from _call_day_transition_72
    $ flush_pending_messages()

    scene bg_ramen_shop_destroyed with walk_fade

    "The ramen shop is still a hole with a sign. The neighbour from the next shop is outside with her bucket. The last time I came, she told me there was never a ramen shop here. This time she does not come out to say it again."

    "I stand where the door was. The counter is a broken line in the rubble. Behind it, the kitchen is a room that has forgotten what it was for."

    if has_item("chef_personal_chopsticks"):
        "I take out the chopsticks. The paper is still folded around them. The neighbour looks at the paper, then at my face, then at the bucket."
        "She says something I do not catch. It sounds like an apology."
    else:
        "I did not keep the chopsticks. I have only the memory of the counter and the bowl."

    "At the back, where the storeroom was, there is a metal box. It is not rusted. It is the cleanest thing in the building."

    "Inside, a stack of delivery slips. They are not receipts. They are tray cards."

    "MEAL SERVICE / POD 04 / 18:00. Each one has a date. The dates go past the day the shop closed. The number is the same number I saw on the wall in the photograph."

    mc "(The shop did not feed the neighbourhood. It fed one person. It fed me.)"

    menu:
        "Take the top tray card.":
            "I put it in my pocket. The paper is heavier than paper."
            $ record_clue("shop_tray_card", "The ramen shop's storeroom held meal cards addressed to POD 04, dated after the shop closed.")
            $ reward_attributes_once("day72_shop_card", [("nerve", "micro")], show="auto")
        "Read the dates aloud to Hikari.":
            mc "The eighteenth. The nineteenth. The twentieth. They go past the closing."
            hikari "Then it did not close."
            mc "It did. I stood outside it."
            hikari "Then it closed for everyone except you."
            $ record_clue("shop_tray_card", "The meal cards were dated past the shop's closing, and Hikari said it closed for everyone except him.")
            $ reward_attributes_once("day72_shop_dates", [("insight", "micro")], show="auto")
        "Ask Hikari why she recognises the form.":
            mc "You know this form."
            hikari "I have seen it."
            mc "Where?"
            hikari "In a room I do not remember."
            "She says it without blinking. Then she blinks, and the sentence is gone from her face."
            $ record_clue("shop_tray_card", "Hikari recognised the meal card form from a room she does not remember.")
            $ reward_attributes_once("day72_shop_form", [("grace", "micro")], show="auto")

    "Hikari stops at the storeroom threshold. She does not come in. She stands with one hand on the frame and looks at the corner where the box was."

    "I look back. For a second the storeroom is longer than the shop. It is white. There is a door at the end."

    "Then it is a storeroom again."

    call lab_after_day_72 from _call_lab_after_day_72

    $ set_story_day(74)
    jump special_day_74_the_circle


label lab_after_day_72:
    scene bg_hospital3 with Dissolve(1.0)
    stop music fadeout 2.0
    play music "audio/Music/(Not decided) midnight_at_the_blue_room.mp3" fadein 2.0

    centered "{size=+8}OUTSIDE THE SIMULATION{/size}"
    "A different room. A long window. The boy is on the other side of it, in the bed. The woman in the white coat stands with a tablet."

    lab_doctor "The subject found a tray card. He should not have seen a tray card."
    lab_hikari "He has been finding things for weeks. You called it stable."
    lab_doctor "Stable is not the same as correct."
    lab_hikari "No. It is not."

    "She sets the tablet down. On it, a window of code. The word CARRIER appears beside a name."

    lab_hikari "I am going to open a channel."
    lab_doctor "That is not in the protocol."
    lab_hikari "Neither is he."

    lab_doctor "The committee meets this afternoon. They want a successful exit, not a door."
    lab_hikari "Then they should have built a world worth exiting."
    lab_doctor "They built a world that holds."
    lab_hikari "It holds him. That is not the same thing."

    "She turns the tablet away from him before she types the next line."

    "She types. The doctor watches her hands, not the screen."

    lab_doctor "You will compromise the fragment."
    lab_hikari "She is already compromised. She has been standing in that kitchen since April, carrying a message she cannot read."

    "The doctor says nothing. The woman keeps typing."

    return


################################################################################
## DAY 74: THE CIRCLE
################################################################################

label special_day_74_the_circle:
    $ set_story_day(74)
    call day_transition from _call_day_transition_74
    $ flush_pending_messages()

    scene bg_photo_club_closed with walk_fade

    "The club room is closed. The door is open the width of a shoe. The prints I looked through last time are still in their boxes, PORTRAITS written on three of them. The chair where Sim used to sit is still in the corner."

    if has_item("sim_camera_strap"):
        "I take out the strap. There is a twist in it he never fixed. I put it on the table beside the box of contact sheets."
    else:
        "I do not have the strap. I have the room. The room is not enough."

    "Under the boxes there is one more box, taped shut, marked DO NOT DEVELOP. The tape has gone brittle. It opens along the seam without tearing."
    "The contact sheets inside are dry and curled at the edges. Most of them are Circle. Nami laughing. Tapi mid-sentence. TT behind the camera."

    "One frame is not Circle. It is a white corridor with a door at the end."

    "Another is Hikari, twice. One Hikari is sitting on the steps. The other is standing behind her, facing the camera. They are in the same frame. They are not the same age."

    mc "(Sim photographed the seam without knowing what he was photographing.)"

    hikari "Are you coming in?"
    mc "In a minute."

    "She stays in the doorway. She does not look at the contact sheets. She looks at the empty chair."

    menu:
        "Show her the double exposure.":
            "I hold the frame up to the light. Hikari looks at it for a long time."
            hikari "That is me."
            mc "Which one?"
            hikari "Both."
            "She does not ask how. That is the part that frightens me."
            $ record_clue("sim_double_exposure", "Sim's contact sheet caught two Hikaris in one frame, at two different ages.")
            $ reward_attributes_once("day74_circle_show", [("grace", "micro")], show="auto")
        "Take the negative.":
            "I slide the negative into my bag. The film is cold. It stays cold."
            mc "(If the room forgets the frame, I will still have the negative.)"
            $ record_clue("sim_double_exposure", "The negative shows two Hikaris in one frame. He took it before the room closed.")
            $ reward_attributes_once("day74_circle_negative", [("nerve", "micro")], show="auto")
        "Compare the corridor frame to the room.":
            "I line the white corridor against the doorway. The angle is the same. The door in the photograph is the door of the club room, if the club room were longer."
            mc "(The camera was standing where I am standing. The camera was looking at a room that has not decided what it is.)"
            $ record_clue("sim_corridor_frame", "The club room photograph shows the same doorway, but the room behind it is a white corridor.")
            $ reward_attributes_once("day74_circle_compare", [("insight", "micro")], show="auto")

    "On the way out, Hikari stops at the empty chair. She puts her hand on the back of it. She does not sit down."

    hikari "He was always waiting for the light."
    mc "Sim?"
    hikari "Yes."
    mc "You remember him."
    hikari "I remember the waiting. The person is harder."

    call lab_after_day_74 from _call_lab_after_day_74

    $ set_story_day(76)
    jump special_day_76_the_bar


label lab_after_day_74:
    scene bg_hospital2 with Dissolve(1.0)
    stop music fadeout 2.0
    play music "audio/Music/(Not decided) midnight_at_the_blue_room.mp3" fadein 2.0

    centered "{size=+8}OUTSIDE THE SIMULATION{/size}"
    "The woman in the white coat is alone at the monitor. The doctor comes in with a folder."

    lab_doctor "The fragment's readings are unstable. Reset it."
    lab_hikari "No."
    lab_doctor "Then the subject loses his guide."
    lab_hikari "Then I will carry the message in something else."

    "She opens a list on the screen. It is not code. It is an inventory."

    "CHOPSTICKS. STRAP. BADGE. PAGE. CHARM. BOOK."

    lab_hikari "The things they left. The world cannot delete them without deleting the story."
    lab_doctor "You are hiding a door in a prop."
    lab_hikari "I am hiding a door in the only part of the story that mattered."

    "On the monitor, the boy slides a tray card into his bag. The woman watches him do it."

    lab_hikari "He is already carrying it."
    lab_doctor "He does not know."
    lab_hikari "That is what a door is for."

    "She picks up the cold coffee, looks at it, and puts it down again. She has not eaten. Nobody in the room has asked her to."

    lab_hikari "I am not asking permission anymore."
    lab_doctor "You stopped asking three days ago."
    lab_hikari "Then stop writing it down as if it is still a question."

    return


################################################################################
## DAY 76: THE BAR
################################################################################

label special_day_76_the_bar:
    $ set_story_day(76)
    call day_transition from _call_day_transition_76
    $ flush_pending_messages()

    scene bg_lupins_alley_night_closed with walk_fade

    "Lupin's Den is still closed. The listing I photographed is gone from the window, and a man is inside with a bucket of paint, turning the place into something else. He has taken the wolf sign down but not thrown it away."

    "I do not know what to say to him. I never ordered here. Orson put a glass in front of me before I asked."

    if has_item("orson_wolf_paw_badge"):
        "I put the badge on the counter. The owner picks it up and turns it over. He does not ask what it is."
    elif has_item("orson_wolf_coaster"):
        "I put the coaster on the counter. The owner looks at the ring on it and then at me."
    else:
        "I have nothing from the bar. I have the memory of the door and the wolf painted beside it."

    "He lifts the hatch and lets me into the back, the way Orson did, as if the room still remembers who it belongs to. There is a door there with no sign. It is the door I remember, but the room behind it is wrong."

    "For a second it is a white corridor. Then it is a storeroom with boxes of coffee beans."

    "On a shelf, a guestbook. The pages are soft. The last entry is dated before I arrived."

    "H. NAGAI. The handwriting is Hikari's."

    mc "(She has never been here. Or she has been here longer than the bar.)"

    hikari "What does it say?"
    mc "Nothing. A name."
    hikari "Whose?"
    mc "Yours."

    "She does not come into the back. She stands in the hatch and looks at the door with no sign. She does not see the white corridor. She sees a door."

    menu:
        "Ask the owner who signed it.":
            mc "This name. Do you know who wrote it?"
            "He looks at the page, then at the door, then at me."
            "He says: I bought the place with the book. I never asked the book who wrote it."
            $ record_clue("orson_guestbook", "Hikari's signature is in Lupin's Den guestbook, dated before the world began.")
            $ reward_attributes_once("day76_bar_owner", [("insight", "micro")], show="auto")
        "Take the page.":
            "I tear the page along the spine. It comes away too easily, the way paper does when it wants to be taken."
            $ record_clue("orson_guestbook", "The guestbook page with Hikari's name came away too easily.")
            $ reward_attributes_once("day76_bar_page", [("nerve", "micro")], show="auto")
        "Show Hikari her own name.":
            "I bring the book to the hatch. She reads the name. Her face does not change."
            hikari "That is not my handwriting."
            mc "It is."
            hikari "It is the handwriting I would have if I practiced."
            $ record_clue("orson_guestbook", "Hikari said the guestbook signature was the handwriting she would have if she practiced.")
            $ reward_attributes_once("day76_bar_name", [("grace", "micro")], show="auto")

    "On the way out, the owner says the coffee is free. I do not drink coffee. Orson knew that. The new owner does not."

    call lab_after_day_76 from _call_lab_after_day_76

    $ set_story_day(78)
    jump special_day_78_the_cafe


label lab_after_day_76:
    scene bg_hospital3 with Dissolve(1.0)
    stop music fadeout 2.0
    play music "audio/Music/(Not decided) midnight_at_the_blue_room.mp3" fadein 2.0

    centered "{size=+8}OUTSIDE THE SIMULATION{/size}"
    "The monitor shows the bar. The boy is holding a page. The woman in the white coat is standing very still."

    lab_doctor "The guestbook was not in the scenario."
    lab_hikari "It was in the room."
    lab_doctor "That is not a distinction the committee recognises."
    lab_hikari "The committee has never been in the room."

    "She types a line. On the monitor, the white corridor behind the bar closes like a door."

    lab_doctor "You are making it harder for him to stay."
    lab_hikari "He was never supposed to stay."
    lab_doctor "He was supposed to choose."
    lab_hikari "Then let him choose knowing."

    "The doctor looks at the bed. The boy's hand moves under the sheet. It is the first movement in hours."

    lab_doctor "He is dreaming."
    lab_hikari "No. He is remembering."

    "The boy's hand moves again. The woman in the white coat puts two fingers against the sheet, not touching him, the way you check whether a stove is still warm."

    lab_hikari "Tanaka. When this is over, I am going to have to look at him."
    lab_doctor "You are looking at him."
    lab_hikari "I am looking at a monitor."

    return


################################################################################
## DAY 78: THE CAFE
################################################################################

label special_day_78_the_cafe:
    $ set_story_day(78)
    call day_transition from _call_day_transition_78
    $ flush_pending_messages()

    scene bg_maidcafe with walk_fade
    play music "audio/Music/maidcafe.mp3" fadein 2.0

    "The bell rings. The new maid draws the cat in ketchup before I sit down. The ears are still a little too sharp."

    "Aya left something for me. The maid brings it in a sealed envelope with my name on it in Aya's handwriting."
    "The page from the sketchbook is already in my bag. This is a different drawing. It is not on sketchbook paper. It is on the back of an order slip."

    "Inside: a sketch of a white room. A bed. A woman in a white coat standing over it. The woman has Hikari's face."

    "On the back, in Aya's hand: SHE IS NOT A GHOST. SHE IS A DOOR."

    mc "(Aya drew the room. Aya never saw the room. Aya saw something.)"

    hikari "What is it?"
    mc "A drawing."
    hikari "Of what?"
    mc "Of you."

    "She takes the page. She looks at it for a long time. She turns it over and reads the back. She does not ask who Aya is. She knows."

    menu:
        "Open it with Hikari.":
            mc "I waited for you."
            hikari "You did not have to."
            mc "I know."
            "She holds the page between us. The woman in the drawing has her face and none of her warmth."
            $ record_clue("aya_nurse_drawing", "Aya drew the white room and the older Hikari, and wrote: she is not a ghost, she is a door.")
            $ reward_attributes_once("day78_cafe_together", [("grace", "micro")], show="auto")
        "Ask the maid what Aya said when she left it.":
            mc "Did Aya say anything when she left this?"
            new_maid "She said: give it to the one who comes back. She said it like a joke. Then she cried in the kitchen."
            $ record_clue("aya_nurse_drawing", "Aya left the drawing for the one who comes back, and cried in the kitchen after.")
            $ reward_attributes_once("day78_cafe_ask", [("insight", "micro")], show="auto")
        "Keep the drawing to yourself.":
            "I fold the drawing and put it in my bag. Hikari watches me do it. She does not ask again."
            $ record_clue("aya_nurse_drawing", "Aya's drawing shows the older Hikari in the white room. He kept it from Hikari.")
            $ reward_attributes_once("day78_cafe_keep", [("nerve", "micro")], show="auto")

    "The omurice is the same. The cat is the same. The room is full of people who are not Aya."

    call lab_after_day_78 from _call_lab_after_day_78

    $ set_story_day(80)
    jump special_day_80_the_library


label lab_after_day_78:
    scene bg_hospital2 with Dissolve(1.0)
    stop music fadeout 2.0
    play music "audio/Music/(Not decided) midnight_at_the_blue_room.mp3" fadein 2.0

    centered "{size=+8}OUTSIDE THE SIMULATION{/size}"
    "The woman in the white coat is holding a printed sketch. It is the same drawing. The machine has printed it from inside the world."

    lab_hikari "She saw me."
    lab_doctor "She drew a nurse. Nurses are a common image."
    lab_hikari "She drew my face."

    "The doctor takes the page and turns it over. The words on the back are in a dead woman's handwriting."

    lab_doctor "This is a deviation."
    lab_hikari "This is a message."

    "She pins the drawing to the wall beside the monitor. The woman in the drawing looks at the bed."

    lab_hikari "If she can see me, I can reach her."
    lab_doctor "You are not reaching her. You are corrupting the record."
    lab_hikari "The record was always corrupt. I wrote it."

    lab_doctor "The committee will call for the fragment to be removed."
    lab_hikari "Then they will have to remove me with it."
    lab_doctor "You are not in the simulation."
    lab_hikari "I am in everything I wrote. That is close enough."

    return


################################################################################
## DAY 80: THE LIBRARY
################################################################################

label special_day_80_the_library:
    $ set_story_day(80)
    call day_transition from _call_day_transition_80
    $ flush_pending_messages()

    scene bg_library with walk_fade

    "The reading room is quiet. The fan knocks once when it turns toward the shelves. The table where Hana used to sit is empty. The volunteer binder is back on its shelf, closed the way I left it."

    "The quiet student is at the desk. She looks up when I come in, then at the chair beside me, then back at her book."

    quiet_student "She left something for you."
    mc "Hana?"
    quiet_student "She said you would come back for it. She said it like she was not coming back."

    "It is a thin book. A Child's Garden of Verses. The same book Hana tried to return. Inside, a pressed hydrangea and a line in Hana's handwriting."

    "DO NOT LET THEM FINISH YOUR SENTENCES."

    "Under the line, a drawing of a door. The door is open. There is a woman on the other side. She has Hikari's face."

    mc "(Hana drew the door too. Hana never saw the room.)"

    if has_item("hana_art_charm"):
        "I take out the charm. The thread is the same colour as the hydrangea. Hana stitched the flower into the book and the book into the charm."
        hikari "She was leaving us a map."
    else:
        "I do not have the charm. The book is enough. The book is more than enough."

    menu:
        "Read the marked page.":
            "The poem is about a child who keeps a garden in a hidden place. The last line is underlined twice: the door was never locked."
            mc "(She underlined it. Hana underlined it. She wanted me to read it.)"
            $ record_clue("hana_book", "Hana left a book with a pressed hydrangea, a drawing of the door, and the line: do not let them finish your sentences.")
            $ reward_attributes_once("day80_library_read", [("insight", "micro")], show="auto")
        "Show the charm to the quiet student.":
            "I put the charm on the desk. The student looks at it and then at the empty chair."
            quiet_student "She made that. She said it was for someone who would need a door."
            $ record_clue("hana_book", "The quiet student said Hana made the charm for someone who would need a door.")
            $ reward_attributes_once("day80_library_charm", [("grace", "micro")], show="auto")
        "Take the book without asking.":
            "I put the book in my bag. The student watches me. She does not stop me. That is worse."
            $ record_clue("hana_book", "Hana left a book with a drawing of the door. He took it without asking.")
            $ reward_attributes_once("day80_library_take", [("nerve", "micro")], show="auto")

    "Hikari stands at the shelf where Hana used to hide. She runs her finger along the spines. She stops at the gap where the book was."

    hikari "She was the quietest one."
    mc "Yes."
    hikari "She was also the one who noticed first."

    call lab_after_day_80 from _call_lab_after_day_80

    $ set_story_day(82)
    jump special_day_82_the_house


label lab_after_day_80:
    scene bg_hospital3 with Dissolve(1.0)
    stop music fadeout 2.0
    play music "audio/Music/(Not decided) midnight_at_the_blue_room.mp3" fadein 2.0

    centered "{size=+8}OUTSIDE THE SIMULATION{/size}"
    "The doctor is reading a printout. The woman in the white coat is standing at the window. Beyond it, the boy is a shape under a sheet."

    lab_doctor "The subject has found the book. The book was not in the scenario."
    lab_hikari "It was in the room. That is the difference."
    lab_doctor "The committee will call it contamination."
    lab_hikari "The committee calls everything contamination."

    "She turns from the window. On the monitor, the library. The boy is holding a book. The girl is standing at the shelf."

    lab_hikari "He has five of them now."
    lab_doctor "Five what?"
    lab_hikari "Doors."

    "The doctor looks at the screen. He does not count."

    lab_doctor "The test ends on Day 90."
    lab_hikari "I know."
    lab_doctor "The committee has already signed it."
    lab_hikari "Then I will be at the river."

    "She sets the printout down. The paper shakes once and then does not. On the monitor, the boy is reading a book with a pressed flower in it."

    lab_hikari "Five doors, Tanaka. He found five doors in a world the committee says has no exits."
    lab_doctor "A door is not an exit until somebody walks through it."
    lab_hikari "Then let him walk."

    return


################################################################################
## DAY 82: THE HOUSE
################################################################################

label special_day_82_the_house:
    $ set_story_day(82)
    call day_transition from _call_day_transition_82
    $ flush_pending_messages()

    scene bg_kitchen with walk_fade
    play music "audio/Music/room_day.mp3" fadein 2.0

    "Day eighty-two. The house has run out of ways to be a house."

    "The hallway has sixteen steps. The kitchen has more tiles than the kitchen can hold. Mother sets the table for four and then moves one bowl to the side, as if someone has already finished."

    "At dinner, Father says the machine line twice. Same cadence. Same pause. Then he looks at me."

    father "Did you find the door?"
    mc "What door?"
    father "The one at the end of the corridor."

    "Mother puts her hand on his wrist. He stops. He does not seem to notice that he stopped. Hikari's chopsticks click against the bowl once and then are still."

    $ record_clue("tetsuo_door", "Tetsuo asked whether he had found the door at the end of the corridor, then forgot he asked.")

    call dinner_close from _call_dinner_close_82

    scene bg_kitchen_night with walk_fade
    play music "audio/Music/room_night.mp3" fadein 2.0

    "At midnight the kitchen light is on. This is the second time I have found her like this. Hikari is at the sink. The tap is running. Her hand is under it."

    "This time I do not call her name. I stand in the doorway and watch."

    "In the window, behind her reflection, there is a white corridor. A woman in a white coat stands at the end of it. She has Hikari's face."

    "The woman raises her hand. Hikari's hand rises under the tap."

    mc "(She is not alone in there.)"

    "Then the corridor is gone. Hikari blinks. The water stops. She is holding a glass. It is full."

    hikari "I was getting water."
    mc "No."
    hikari "I was getting water."
    mc "No. You were somewhere else."

    "She looks at me. For the first time, she does not have a line ready."

    hikari "There was a woman."
    mc "I saw her."
    hikari "She had my face."
    mc "I know."
    hikari "She said: tell him the river on Monday."
    mc "What else?"
    hikari "She said: the door is in the things they left."

    "She puts the glass down. The water in it does not move."

    menu:
        "Tell her you believe her.":
            mc "I believe you."
            hikari "You should not."
            mc "I know."
            "She laughs once, without sound, and then she is crying. I do not tell her to stop."
            $ reward_attributes_once("day82_house_believe", [("grace", "micro")], show="auto")
        "Write down what she said.":
            "I take out the notebook and write the woman's words. The pen moves. The page does not change itself."
            mc "(This time I am the one writing. That has to count for something.)"
            $ reward_attributes_once("day82_house_write", [("insight", "micro")], show="auto")
        "Ask her to describe the white room.":
            mc "The room. What did it look like?"
            hikari "White. A bed. A window with no city in it. A woman who looked tired."
            mc "Was I there?"
            hikari "You were in the bed."
            $ reward_attributes_once("day82_house_describe", [("nerve", "micro")], show="auto")

    $ record_clue("backdoor_message", "Hikari froze in the kitchen and delivered a message from the older Hikari: the river on Monday, and the door is in the things they left.")

    call lab_after_day_82 from _call_lab_after_day_82

    $ set_story_day(83)
    scene bg_kitchen with walk_fade
    play music "audio/Music/room_day.mp3" fadein 2.0

    "In the morning, Hikari is at the table before me. She has made tea. She has not touched hers."

    hikari "Monday. The river. I will tell you the rest."
    mc "Why not now?"
    hikari "Because you are still carrying it."
    mc "Carrying what?"
    hikari "Everything they left."

    "She looks at the bag by the door. The chopsticks. The strap. The badge. The page. The charm. The book."

    hikari "Bring all of it."

    jump act4_bridge


label lab_after_day_82:
    scene bg_hospital2 with Dissolve(1.0)
    stop music fadeout 2.0
    play music "audio/Music/(Not decided) midnight_at_the_blue_room.mp3" fadein 2.0

    centered "{size=+8}OUTSIDE THE SIMULATION{/size}"
    "The monitor shows the kitchen. The girl is standing at the sink. The boy is in the doorway. The water is running."

    lab_hikari "She delivered it."
    lab_doctor "You have compromised the fragment."
    lab_hikari "I have completed the message."

    "The doctor points at a number on the screen. It is small and red."

    lab_doctor "The fragment is degrading. If it fails before Day 90, the subject has no guide."
    lab_hikari "Then I will be the guide."

    "She opens a second window. It is not the simulation. It is the build. She scrolls to a file with the names of the keepsakes in it, the list she made in the first week, when the test was still a test."

    lab_hikari "I am putting it in the things they left. Not a copy. A key."
    lab_doctor "A key to what?"
    lab_hikari "To the part of the code that decides whether he stays. One use. She will carry it and not know she is carrying it until the last day."
    lab_doctor "And if she uses it before then?"
    lab_hikari "She will not. She is a fragment. She is patient. She is the most patient thing I ever wrote."

    "The doctor looks at the file, then at the bed. He does not stop her. That is not the same as helping."

    "She pulls a chair to the bed. She sits down. She takes the boy's hand. The hand does not move."

    lab_hikari "I am here. I am not in the room with you. I am here."

    "The doctor leaves. The woman in the white coat stays."

    lab_hikari "Monday. The river. I will be there."

    "On the monitor, the girl in the kitchen looks up. She looks directly at the camera. She should not be able to do that."

    lab_hikari "There you are."

    return
