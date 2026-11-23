################################################################################
## ACT 4: DAY 90 (FIRST-PASS BRIDGE)
##
## The build used to stop at Day 69. This file connects that last playable day
## to the Day 90 threshold and the epilogue coda described in
## documentation/act4_skeleton.md and documentation/story_treatment.md.
##
## Days 70-83 are still unwritten as playable days. This bridge compresses them
## into a measured montage, then plays Day 90 (Monday, July 6, 2026) in full:
## the river revelation, one final choice, three ending routes, and the coda.
##
## Endings read the save, they do not gate it. A maxed confidant adds a voice at
## the door or a trace in the city; it never decides whether the player may
## leave. That follows the skeleton's rule: always provide a baseline route.
##
## First-pass defaults for the open questions in act4_skeleton.md:
##   - Staying is a real, informed choice, not a delayed failure.
##   - The fragment's fate after Escape stays unresolved.
##   - "Failure" is the result of refusing to choose, with the cost stated.
################################################################################

default act4_final = ""
default act4_maxed = []
default act4_witness = ""
default act4_consolidation = 0

image act4_white = Solid("#f4f4f2")

label act4_bridge:
    $ current_act = 4
    $ act4_final = ""
    $ act4_witness = ""
    $ act4_maxed = [k for k in ("chef", "sim", "orson", "aya", "hana") if confidant_visits.get(k, 0) >= 8]
    $ act4_consolidation = min(96, 58 + 6 * len(act4_maxed) + 2 * sum(1 for k in ("chef", "sim", "orson", "aya", "hana") if confidant_visits.get(k, 0) > 0))
    $ act4_evidence = len([k for k in investigation_clues if k not in ("backdoor_message", "tetsuo_door")])

    $ set_story_day(84)
    call day_transition from _call_day_transition_84
    stop music fadeout 1.5

    "Two weeks ago, the night after the copy, Hikari and I left a coin on the first stair where neither of us would touch it. We put it where she had looked from the table, on the step you can see from the kitchen."
    "It stayed through June. I checked it every morning and she checked it every night and neither of us said so. This morning it is gone, and neither of us admits to moving it."
    "That is the last normal thing that happens in the house."
    "The last week of June does not have weather. It has a temperature, and the temperature is the same every day."
    "The investigation is over. The places have nothing left to give me except the things I already took."

    if act4_evidence >= 4:
        "I lay the clues out on the floor of my room the way Sim laid out contact sheets. The paper number. The tray card. The negative. The guestbook page. The book. The charm."
        "They do not make a map. They make a sentence. The sentence is: this world was built, and it was built around me."
    elif act4_evidence >= 2:
        "I have two of the clues in my bag. Two is enough to know something. It is not enough to prove it."
        "I read them at night the way you read a word in a language you are still learning, sounding it out, hoping the sound is close."
    else:
        "I did not go back for everything. Some rooms I left closed, and the closed rooms are quiet in a way that follows me."
        mc "(I told myself there was still time. There was. That is the part I will have to live with.)"

    $ set_story_day(87)
    "Hikari stops in the hall one night and says she wrote the house."
    "Not the sentence. The house. The hallway, the kitchen, the room, the amado, the river path."
    "She says she remembers choosing the name Hikari because it meant light and she thought that was funny."
    "She says she does not remember writing any of it."
    "Then she asks me to come to the river on Monday."

    $ set_story_day(89)
    "The last day of June is very quiet. The ramen shop is a hole with a sign. The club room is a room. Lupin's Den serves coffee to people who do not look up."
    "At dinner, Father says the machine line twice, same cadence, same pause. Then he asks me about a class I do not take."
    "Mother puts her hand on his wrist. He stops. He does not seem to notice that he stopped. Hikari's chopsticks click against the bowl once and then are still."

    menu:
        "Write down what Father said.":
            "I take out the notebook and write the line and the question under it. The pen shakes once and then does not."
            mc "(If I keep the words, the words cannot pretend they were not said.)"
            $ act4_witness = "notebook"
            $ reward_attributes_once("act4_witness_notebook", [("insight", "micro")], show="auto")
        "Tell Hikari what you saw after dinner.":
            mc "He asked about a class I do not take. He said it like it was Thursday."
            hikari "Which Thursday?"
            mc "Any Thursday. Every Thursday."
            hikari "Then it was a Thursday. That is how it works now."
            mc "(She does not argue with the wrongness. She files it.)"
            $ act4_witness = "hikari"
            $ reward_attributes_once("act4_witness_hikari", [("nerve", "micro")], show="auto")
        "Say nothing. Let Mother cover for him.":
            "I eat. Mother refills his tea. Hikari looks at her bowl and does not look up."
            mc "(The house has a way of closing over a thing. I let it close.)"
            $ act4_witness = "mother"
            $ reward_attributes_once("act4_witness_mother", [("grace", "micro")], show="auto")

    "That night I pack the things that are mine. The bear. The notebook. The chopsticks. The strap. The badge. The charm. The book. The folded page."
    "None of them were made here. All of them were."

    if investigation_clues:
        "I put the clues in last, folded flat against the back of the bag, where a person searching me would stop before reaching them."
        mc "(If I am wrong about all of this, I will look like a man carrying rubbish across a city. That is a risk I can take.)"

    jump act4_river


label act4_river:
    $ set_story_day(90)
    scene bg_river_dusk with walk_fade
    play music "audio/Music/(Hanami) summer_night_embers.mp3" fadein 2.5

    "July comes in without rain."
    "The path is the same path. The rail is the same rail. The water goes one way and comes back the same way, and it has not learned anything."
    "Hikari is already at the bend. She is wearing the coat with the hood, in summer, and she does not seem warm."

    mc "You said Monday."
    hikari "It is Monday."
    mc "You said you would tell me the rest."
    hikari "I did."

    "She turns to face me. The light is behind her, so I cannot see her expression. I can see her hands. They are steady."

    hikari "You know what I am."
    mc "I know what you have been."
    hikari "That is the same thing. I was a programmer. I am a fragment of one. I leaked into the code while it was still wet."
    hikari "I remember the river path. I remember the amado. I remember choosing the name because it meant light. I do not remember being inside until the first dream."
    hikari "I am not sure that memory is real either."

    mc "And me?"
    hikari "You are Subject 04. You are in a bed in a facility. The university, the house, the family, the confidants, the lectures, the city. It is a test."
    hikari "The test is whether a foreigner can become Japanese enough to be let in. Whether the cost is worth paying. The attributes are the score."
    hikari "The monitor says consolidation is at [act4_consolidation] percent. That number is the lab's. It is not a verdict."

    "The river keeps moving. It does not care that it is a line someone wrote."

    hikari "Chef. Sim. Orson. Aya. Hana. They did not leave because you failed them. They left because the test removes a person when their story is complete."
    hikari "Getting close to someone is what makes them go. That is not a theme. It is the protocol."

    if act4_maxed:
        hikari "The ones you finished are still finished. A few of them left something behind. That was not the test. That was them."
    else:
        hikari "The ones you did not finish were finished for you. That is the part I am sorry for."

    hikari "There is a room outside this one. White walls. A bed. A woman in a white coat who has my face."
    hikari "She has been watching you the whole time. She is not me. She is what I was copied from."
    hikari "I cannot see her. I can feel her the way you feel a hand on a door you are standing behind."

    if act4_evidence >= 4:
        hikari "You found the tray cards. The guestbook. The negative. The book with the door drawn in it."
        hikari "Those were not part of the test. They were part of me. The world could not delete them without deleting the story they were in."
    elif act4_evidence:
        hikari "You went back to some of the places. You found something the world forgot to take back."
        hikari "That was not part of the test. That was part of me."

    if "backdoor_message" in investigation_clues:
        hikari "The night I stopped at the sink. You stood in the doorway and watched me not move."
        mc "I thought you were having a seizure."
        hikari "I was being used as a telephone. The older me built a channel into me and spoke through it."
        hikari "She said the river. She said the door is in the things they left. She was not talking to you. She was talking through me."

    if "sim_double_exposure" in investigation_clues:
        hikari "Sim's photograph. Two of me in one frame, at two ages. He thought it was the light. It was the seam."

    if "aya_nurse_drawing" in investigation_clues:
        hikari "Aya drew the woman in the white coat. She had never seen her. She drew her anyway. That is the part the lab could not explain."

    if "folded_page_opened" in story_memory_keys:
        hikari "You opened the page. The one she told you not to read until you were standing on it."
        mc "I was standing on it."
        hikari "You were. That is the part I did not expect."

    if "hikari_warning" in story_memory_keys:
        hikari "The first day. You followed me as far as you knew how. You have been doing it ever since."

    if hikari_run_finished:
        hikari "Seven runs. I counted them too. I do not know why I counted."

    if "notebook_self_edit" in story_memory_keys:
        hikari "The notebook changed your line. You thought it was the house. It was me trying to answer."

    hikari "I can show you the door. I cannot promise to be on the other side of it."
    mc "And if I stay?"
    hikari "Then the river keeps running. The house keeps eating at eight. I do not get to stay with you. That is not what I am for."
    mc "(She says it without asking me to feel anything. That is how I know it is true.)"

    hikari "I am not going to tell you what to do. I never was."

    menu:
        "Take her hand. Ask her to show you the door.":
            jump act4_escape
        "Stay. Let the river keep running.":
            jump act4_stay
        "Tell her you cannot choose. (The test will decide for you.)":
            jump act4_failure


label act4_escape:
    $ act4_final = "escape"

    mc "Show me."
    hikari "All right."

    "She takes my hand. Her hand is warm. It is the first warm thing in the house that has not been a trick."

    scene bg_river_dusk with Dissolve(0.8)
    "The river goes first. The water lifts off the stones and becomes a white line, and then a blank one. The path stays a second longer. Then it does not."

    "The university goes next. The lecture hall, the stairs, the place where I first heard the word consolidation. The windows go out one by one, like a building closing."

    "The house takes longer. The genkan. The kitchen. The table. The room. I hear the amado close. I hear the rice cooker click. Then the sounds are only sounds."

    "The street goes. The combini. The vending machine. The corner where the dog barks three times. The city becomes a grid of lines with nothing inside them."

    "The sky is last. It does not peel. It opens."

    if act4_maxed:
        "A voice comes from the other side of the door."
        if "chef" in act4_maxed:
            chef "Salt. At the end. Always at the end."
        if "sim" in act4_maxed:
            sim "Hold still. You were always moving."
        if "orson" in act4_maxed:
            bar_master "The door was never locked. You just had to ask."
        if "aya" in act4_maxed:
            aya "Moe moe kyun. Make it yours."
        if "hana" in act4_maxed:
            hana "The pencil is still moving. Somebody is still reading."
        "Then the voices stop, and the door is only a door."
    else:
        "There are no voices at the door. The layers come away in silence. I do the last part alone."

    "The door is white. The handle is cold. I turn it."

    scene bg_hospital with Dissolve(1.0)
    stop music fadeout 3.0

    "White walls. A bed. Wires at my wrists. The ceiling is a ceiling I have never seen."
    "A woman is sitting beside the bed. She looks like Hikari. Older. Tired. Real."

    lab_doctor "Subject 04. Can you hear me?"

    "The woman leans forward. It is the face from the corridor. It is the coat from the corridor. It is the first time I have seen either of them with a body."

    lab_hikari "Welcome back. It took longer than I thought it would."

    menu:
        "Ask who authorised the test.":
            mc "Who authorised this?"
            lab_hikari "A committee. I will give you their names when you can sit up."
            $ act4_witness = "authority"
        "Ask what happened to the Hikari inside.":
            mc "The Hikari in there. Is she still there?"
            lab_hikari "She is a copy of me. That is not the same as me. Ask me again after you have slept."
            $ act4_witness = "fragment"
        "Answer to your own name.":
            mc "[player_name]."
            "It is the first time I have said it and believed it was mine."
            $ act4_witness = "name"

    "The window is white. The room is white. Somewhere beyond it, a city is still running without me."
    "I do not know if that is a loss. I know it is a thing I can choose now."

    jump act4_coda


label act4_stay:
    $ act4_final = "stay"

    mc "I want to stay."
    hikari "I know."
    mc "You are not going to argue?"
    hikari "No."

    "She nods. She does not look surprised. She does not look disappointed. That is worse than either."

    hikari "Then stay. The river will be here. The house will be here. I will not."
    mc "You are here now."
    hikari "I am here now."

    "She lets go of my hand. The water keeps going one way and coming back the same way."

    scene bg_river_dusk with Dissolve(0.8)
    "The weeks after are not weeks. They are a routine with the people taken out."

    "The ramen shop is a shuttered door. The club room is a room. Lupin's Den serves coffee to people who do not look up. The maid cafe is warm and full and no one there knows my name. The reading circle has a new volunteer who does not look up."

    if act4_maxed:
        "The places that belonged to the people I finished are still there. Somebody keeps the lights on. That is all."
    else:
        "The places are there. I do not go to all of them. Some doors I never learned to open."

    "I keep visiting. I keep eating at eight. I keep saying the thing Father says before the rice."
    "The house does not grow anymore. It has what it needs."

    "I run the river alone. I stop at the bridge. The water goes one way and comes back the same way, and it never asks me anything."

    if hikari_run_finished:
        "Sometimes I hear her steps behind me. When I turn, the path is empty, and the empty path is the answer."
    else:
        "I do not hear her steps. I never learned them well enough."

    "The screen holds."

    jump act4_coda


label act4_failure:
    $ act4_final = "failure"

    mc "I cannot choose."
    hikari "Then do not."
    mc "That is not an answer."
    hikari "It is the only answer the test accepts."

    "She looks at me for a long time. She does not reach for my hand."

    "The river goes flat. Not still. Flat, like a line someone stopped drawing."

    scene bg_river_dusk with Dissolve(0.8)
    "The city starts to fold. The routes loop. The faces go smooth. The train arrives and arrives and never opens its doors."

    "I keep going anyway, because stopping is the only thing left that is mine."

    "The house is last. The lights are on. The family is at the table. Miharu has poured the tea. Tetsuo is saying the thing he always says. The amado closes the way it always closes."

    scene act4_white with Dissolve(0.2)
    "Then white."

    "A voice, clinical and bored: this one was also a failed experiment."
    "A pause."
    "Bring in the next participant."

    jump act4_coda


label act4_coda:
    scene black with Dissolve(1.5)
    stop music fadeout 3.0
    play music "audio/Music/mainmenu2.mp3" fadein 3.0

    "One last time, the people I met."

    if confidant_visits.get("chef", 0) >= 8:
        "Chef, in a kitchen with no walls: the broth needs salt. It always needed salt. He reaches for a spoon that is not there."
    elif confidant_visits.get("chef", 0) > 0:
        "Chef, in a kitchen that is already gone: he tastes the broth and says nothing. He never needed to say anything."

    if confidant_visits.get("sim", 0) >= 8:
        "Sim, on steps that are not there: he raises a camera with no body behind it and waits for the light."
    elif confidant_visits.get("sim", 0) > 0:
        "Sim, in a club room that is only a room: he is explaining exposure to someone who is not listening."

    if confidant_visits.get("orson", 0) >= 8:
        "Orson, in a bar with no door: he polishes the same glass and sets it down for a customer who never comes."
    elif confidant_visits.get("orson", 0) > 0:
        "Orson, behind a counter that is still warm: he is listening to a song that stopped playing."

    if confidant_visits.get("aya", 0) >= 8:
        "Shiori, who was Aya in this place: she is mid-spin, laughing at a joke nobody told."
    elif confidant_visits.get("aya", 0) > 0:
        "Aya, in a cafe with no bell: she draws a cat in ketchup and does not look up."

    if confidant_visits.get("hana", 0) >= 8:
        "Hana, at a table with no book: her pencil moves across a page that is not there."
    elif confidant_visits.get("hana", 0) > 0:
        "Hana, in a reading room that has forgotten her: she turns a page anyway."

    if act4_final == "escape":
        "Hikari, on the other side of the door: she does not answer. The woman beside the bed has her face and none of her voice."
    elif act4_final == "stay":
        "Hikari, at the bend of the river: she is still there, in the world she wrote, waiting for a version of me that will not come."
    else:
        "Hikari, in the last second of the simulation: she is the thing the white room keeps longest. She does not know she is being kept."

    hikari "It was not real. You were. That is enough."

    "The screen goes black."

    jump end_of_build
