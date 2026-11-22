################################################################################
## DAY 51: THURSDAY, MAY 28, 2026
## The line she did not say. The first morning of the rain. The hit that
## changes the tone of the game: Hikari says Father's sentence, word for word,
## and nobody in the room notices except him.
################################################################################

label special_day_51_the_line:
    $ set_story_day(51)
    call day_transition from _call_day_transition_51

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Rain."
    "It has been dry since the day I arrived. Fifty days of pale skies and the sound of the city doing whatever the city does when it is not raining. This morning the window is wet and the sky is the color of a pillowcase that has been washed too many times."
    "The rain is not heavy. It is the kind that does not end. It taps the glass in no particular rhythm and it has been doing it since before I woke, and it will be doing it after I sleep, and it does not care whether I am listening."
    mc "(Tsuyu. Hikari told me the word last week. The rainy season. It comes in June and it stays until July and it is the reason the hydrangeas are the color they are.)"
    mc "(It is May. It is not June. The rain is early.)"

    "My phone buzzes."

    if "tanaka" in wire_unlocked:
        $ run_chat("tanaka", [
            {"them": "Rain. Slow shift today. Bring the umbrella they gave you.", "options": [
                {"label": "\"I did not get an umbrella.\"",
                 "send": "I did not get an umbrella.",
                 "them": ["Then buy one. The combini has them by the door.", "That is where umbrellas live when it is raining."]},
                {"label": "\"I have one somewhere.\"",
                 "send": "I have one somewhere.",
                 "them": ["Somewhere is not here. Here is where the rain is."]},
            ]},
        ])
    else:
        $ run_chat("hikari", [
            {"them": "It is raining. Do you have an umbrella?", "options": [
                {"label": "\"I think so.\"",
                 "send": "I think so.",
                 "them": ["Think faster. The rain does not wait for thinking."]},
                {"label": "\"No.\"",
                 "send": "No.",
                 "them": ["Then take mine. I have two. I have always had two."]},
            ]},
        ])
        mc "(She has always had two. I do not know why that sentence stays with me.)"

    call murakami_daily_ping from _call_murakami_daily_ping_51

    scene bg_kitchen with walk_fade

    "The kitchen is warm. The rice cooker has finished. The miso is on the stove. The window is wet and the light in the room is the color of the light through the wet window, which is a color I have not seen in this kitchen before."
    "Father has the newspaper folded into a square. Mother is pouring tea. Hikari is sitting at her place, holding her chopsticks the way she holds them when she is waiting for the rice, which is to say she is holding them like she is not thinking about them at all."
    father "The rain."
    mc "The rain."
    father "It will stay."
    mc "Until July?"
    father "Until it is done with us. The rain does not negotiate."
    mother "Eat. Both of you. The rice is not improved by talking about the weather."
    "I sit. The rice is rice. The miso is miso. The fish is grilled the way it is always grilled. The window does what the window does when it is raining, which is nothing, loudly."

    "Father turns the newspaper. He folds it to a new square. He reads for a moment. He puts it down."
    father "The week is a machine. The combini is a smaller machine. You are learning to operate both."

    "I look up. The sentence is the one he said on the Monday I caught the last train. The one he said again, word for word, on the day Hikari asked whether he had said it before. He has said it twice now. This is the third time."
    "I wait for Hikari to notice. She noticed last time. She asked. She dismissed it. She said fathers repeat themselves."

    hikari "The week is a machine. The combini is a smaller machine. You are learning to operate both."

    "The sentence comes out of her mouth the way a sentence comes out of a mouth that has said it before. The cadence is his. The pause after machine is his pause. The emphasis on both is his emphasis. She is looking at her rice when she says it. She picks up a piece of fish. She chews. She swallows."

    # The world tears for one frame. Nobody in the room sees it. Only the
    # player does. The ChromaGlitch plugin slices the screen and offsets the
    # slices with chromatic aberration for 0.08 seconds, then the screen is
    # whole again and the kitchen is warm and the rice is rice.
    show layer master at glitch
    pause 0.08
    show layer master

    "Nobody looks up."
    "Father turns the newspaper. Mother pours more tea. Hikari eats her fish."
    "I am holding my chopsticks in the air. I have not moved them since she said it. I put them down. I pick them up. I eat. The rice is rice. The miso is miso. The sentence is still in the room, the way smoke is in a room after the cigarette is out."
    mc "(She said his sentence. She said it the way he says it. She did not notice she said it. He did not notice she said it. Mother did not notice she said it. I am the only person at this table who heard it.)"
    mc "(Or I am the only person at this table who noticed that it was wrong.)"

    "I eat. I eat the way you eat when you are trying to eat the way you always eat. The chopsticks do what chopsticks do. The bowl empties. Mother fills it halfway without asking, which is what she does when she thinks I am not eating enough."
    mother "More?"
    mc "Please."
    "She fills the rest. The rice is warm. The rain is on the window. The sentence is not in the room anymore. I am the only one carrying it."

    menu:
        "[tag_nerve] Rank 3: Ask her to say the line again, slowly." if has_attribute("nerve", 3):
            mc "Say it again. Slowly. The sentence you did not say."
            hikari "I did not say it."
            mc "I know. Say it anyway."
            $ reward_attributes_once("day51_say_again", [("nerve", "micro")], show="auto")
        "Ask Hikari if she meant to say that.":
            mc "Hikari."
            hikari "Mm?"
            mc "What you just said. About the machine."
            hikari "What about it?"
            mc "You said it. The sentence Father says."
            hikari "I said the rice is good."
            mc "You said the week is a machine."
            hikari "I did not say that. Why would I say that? That is Father's line."
            "She looks at me the way she looks at me when I have not slept enough. Not unkind. Patient, the way you are patient with a person who is tired."
            hikari "You are tired. The rain does that. It makes the house feel smaller and the head feel heavier."
            mc "(She did not say it. She does not remember saying it. Or she said it and does not know she said it, which is a different thing, and the different thing is the one I am afraid of.)"
            $ remember("mc", "said Father's machine sentence in his exact cadence and did not remember saying it; the room tore for one frame", "hikari_said_fathers_sentence")
            $ reward_attributes_once("day51_ask_hikari", [("insight", "small")], show="auto")
        "Say nothing. Finish the rice.":
            "I eat. The rice is warm. The fish is gone. The miso is half a bowl. I finish all of it because finishing is what I do when I do not know what else to do."
            mc "(If I say it out loud, it becomes a thing that happened. If I do not, it stays a thing I noticed. I have been here before. The milk. The door. The shop. The child. I noticed all of them. I did not say any of them out loud. I am not going to start now.)"
            $ log_memory("hikari", "said Father sentence at breakfast and he said nothing about it")
            $ reward_attributes_once("day51_say_nothing", [("nerve", "small")], show="auto")
        "Ask Father if he noticed.":
            mc "Father."
            father "Mm."
            mc "You said the machine line."
            father "I say it when it is true. It is true."
            mc "Hikari said it too."
            father "Did she?"
            "He looks at Hikari. Hikari looks at him. They look at each other the way two people look at each other when one of them has been told something the other does not remember."
            father "She was agreeing with me."
            hikari "I was agreeing with you."
            father "There. She was agreeing with me."
            mc "(She was not agreeing. She was saying it. The same words, the same cadence, the same pause after machine. He heard it as agreement. She heard it as agreement. I heard it as a sentence that moved from one mouth to another without asking.)"
            $ log_memory("hikari", "said Father sentence and Father heard it as agreement")
            $ reward_attributes_once("day51_ask_father", [("grace", "small")], show="auto")

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The street is wet. The gutters are running. The shrine at the corner has water on its steps and the temizuya is full and the ladle is floating in it, which I have not seen before."
    "The shop on the corner is closed. The paper is on the glass. The sign says closed until the end of the month. It has said that since May."
    mc "(It is the end of the month. It is the twenty-eighth. The sign says until the end of the month and it is the end of the month and the shop is closed and the sign is right and I am tired of looking at it.)"

    "Hikari is ahead of me. She has the umbrella. It is clear plastic and it makes the rain sound different, the way a roof makes rain sound different, which is to say it makes it quieter and closer."
    hikari "You are walking slowly."
    mc "I am thinking."
    hikari "About the rain?"
    mc "About the kitchen."
    hikari "The kitchen is fine. The rice was good. Mother is a good cook."
    mc "That is not what I was thinking about."
    hikari "Then what?"
    mc "Nothing. The rain."
    "She holds the umbrella over both of us. She does not ask again. The rain taps the plastic the way it taps the window, which is to say in no particular rhythm, and I walk under it and I do not say what I am thinking, and she does not ask, and the street is wet and the shrine is wet and the shop is closed and the sign is right."

    scene bg_station with walk_fade
    scene bg_platform with walk_fade

    "The platform is wet. The yellow line is wet. The queue is not a queue. The sign says one minute, which is honest."
    "A woman in a grey coat is standing at the far end of the platform. She has a bag over her shoulder and she is reading something on her phone."
    mc "(I have seen her before. The coat. The bag. The way she stands with her weight on one foot.)"
    "I have seen her at the university gate. I have seen her at the combini. I have seen her on this platform, at this end, with her weight on that foot."
    "The train comes. She gets on the same car. She stands at the far end. She reads her phone."

    scene bg_train_interior_day with walk_fade

    "The car is not crowded. The rain makes the windows streak. The woman in the grey coat is at the far end, reading."
    "Hikari is beside me, holding the strap. She is looking at the window. The city goes by in the glass, backwards and wet."
    hikari "You are staring."
    mc "I am looking at the window."
    hikari "You are looking at the woman in the grey coat."
    mc "I am not."
    hikari "You are. I can tell because you are not blinking."
    "I blink."
    hikari "See. You forgot to."
    mc "(She is right. I was not blinking. I was looking at the woman in the grey coat and I was not blinking and Hikari noticed before I did.)"

    scene bg_school_gate with Fade(0.0, 0.0, 1.5)
    play music "audio/Music/school.mp3" fadein 1.5
    $ phone_map_visit("school")

    "The gate is the gate. The guard is in his box. The path is wet. The bicycle is gone and the sign about the lost cat is gone and there is nothing in their place, which is different from there being something else in their place."
    mc "(The sign was there last week. The cat was lost last week. The sign is gone. The cat is found, or the sign is gone, and those are two different things and I do not know which one is true.)"

    scene bg_campus_interior with walk_fade
    scene bg_lecture_hall with walk_fade
    play music "audio/Music/classroom.mp3" fadein 1.0

    "The lecture hall is full. The professor is at the board. He is writing."
    "He writes a date. June. He writes a year. He writes a number after the year that is not a date I recognize."
    "He looks at it. He puts the chalk down. He picks up the eraser. He erases the date. He writes a new one. May. The twenty-eighth. Today."
    "He does not comment on it. He does not turn around. He writes the lecture title under the date and he begins."
    mc "(He wrote a date that is not today. He erased it. He wrote today. He did not say anything about it. The room did not notice. I noticed. I am noticing a lot of things today that the room does not notice.)"

    "The lecture is about the Heian court. The professor talks about the way the court wrote letters, which was in a language nobody outside the court could read, on paper nobody outside the court could afford, about feelings nobody outside the court was allowed to have."
    "He says the word mono no aware and I write it in my notebook and I do not hear the rest of the lecture because I am thinking about the kitchen and the sentence and the woman in the grey coat and the date on the board that was not today."

    scene bg_campus_interior with walk_fade

    "After the lecture I stand in the corridor. The twelfth door is not there. The wall is a wall. The fire extinguisher. The notice board. The third tile that squeaks."
    "I count the doors. Eleven. I count them again. Eleven."
    mc "(Eleven. Not twelve. The door is gone. The door was there on the eighteenth and it is gone on the twenty-eighth and I do not know where doors go when they are gone.)"

    menu:
        "Go straight home.":
            mc "(I am going home. I am going to sit at the desk and open the notebook and write down what happened. I am going to write it in the order it happened. I am going to write it in my handwriting. I am going to close the notebook and put it under the bear and see what it says in the morning.)"
            $ reward_attributes_once("day51_go_home", [("nerve", "micro")], show="auto")
        "Walk in the rain first.":
            "I walk. The campus is wet. The courtyard is empty. The rain is on my face because I did not bring the umbrella, because Hikari has the umbrella, because she has always had two and she gave me one and I left it at the house."
            "I walk for twenty minutes. The rain does not stop. I do not stop. We are both doing what we do."
            mc "(The rain is real. The rain on my face is real. The cold is real. Whatever else is happening in this city, the rain is not part of it. The rain is just rain.)"
            $ reward_attributes_once("day51_walk_rain", [("grace", "micro")], show="auto")
        "Find Hikari.":
            "I find her in the courtyard, under the eaves, reading her phone. She has the umbrella closed. She is dry."
            hikari "You are wet."
            mc "I am."
            hikari "I gave you an umbrella."
            mc "I left it at the house."
            hikari "Then you are wet on purpose."
            mc "I am wet because I forgot."
            hikari "Those are the same thing."
            "She holds the umbrella over me. I stand under it. The rain taps the plastic. She does not ask what is wrong. She stands there and she holds the umbrella and I dry, slowly, under the plastic, and the rain does not stop."
            $ reward_attributes_once("day51_find_hikari", [("grace", "micro")], show="auto")

    scene bg_home_exterior_night with walk_fade
    $ night_street()

    "The walk home is wet. The shrine is wet. The vending machine hums its note. The shop on the corner is closed. The sign is right."
    "The house is warm. The amado is closed. Father closed it. He closes it the same way every night, in the same order, and I have been listening to the order for fifty-one days and I could do it myself if I had to."

    call dinner_open from _call_dinner_open_51

    "Dinner is rice and soup and something with pork. The rain is on the kitchen window. The light is the color of the light through the wet window."
    "Father says something about the rain. Mother says something about the garden. Hikari says nothing."
    "I watch her. She eats. She chews. She swallows. She does not say the sentence. She does not say any sentence that is not hers. I wait for it. I wait through the rice. I wait through the soup. I wait through the pork."
    "She does not say it."
    mc "(The relief is worse than the repeat would have been. The repeat would have been a thing that happened twice. The relief is a thing that happened once and might happen again and I do not know when.)"

    father "The rain will be here for a while."
    mc "I know."
    father "You are quiet."
    mc "I am tired."
    father "Tired is a thing you say when you do not want to say the other thing."
    mc "There is no other thing."
    father "Then you are tired."
    "He says it the way he said it on the day of the door. The same words. The same cadence. I do not know if he remembers saying it before. I do not know if remembering is the thing that makes a sentence yours."

    call dinner_close from _call_dinner_close_51

    scene bg_room_night with stair_fade
    $ room_ambient(True)

    "Upstairs, the bear is on the desk. The timer is beside him. The notebook is open to the corridor map."
    "I sit down. I uncap the pen. The rain is on the window. The room is the room."
    "I write: Thursday. The rain started. Hikari said Father sentence at breakfast. The week is a machine. The combini is a smaller machine. You are learning to operate both. She said it in his cadence. She did not remember saying it. Nobody noticed."
    "I write: The professor wrote a date on the board that was not today. He erased it. He wrote today. He did not comment."
    "I write: The woman in the grey coat was on the platform, on the train, and at the gate. I have seen her before."
    "I write: The door is gone. Eleven doors. The wall is a wall."
    "I close the notebook. I put it under the bear. I put the pen on top."
    $ night_desk_line = "the bear, the notebook underneath him, and the rain on the window"
    call night_open from _call_night_open_51

    menu:
        "Tell Hikari about the line.":
            mc "This morning. At breakfast. You said something."
            hikari "I said a lot of things. I said the rice was good."
            mc "You said the week is a machine."
            hikari "Dad says that. I don't."
            mc "It sounded like him, too."
            "She sets the cup down without taking her hand off it."
            "She is standing in the doorway. She is holding a cup of tea. The steam goes up and does not come back down."
            hikari "You are scaring me."
            mc "I am scaring myself."
            hikari "Then stop."
            mc "I cannot."
            hikari "Then tell me what to do."
            mc "I do not know."
            "She stands there. The tea steams. The rain taps the window. She does not come in. She does not leave."
            hikari "I am going to go to bed. You should go to bed. The rain will be here in the morning and you will need the sleep."
            mc "Hikari."
            hikari "Good night."
            "She goes. The door clicks. The hallway is quiet. The rain is louder than the hallway."
            mc "(She said good night. She said it the way she says it. She did not say it the way Father says it. I am checking now. I am checking the way she says good night. That is what today has done to me.)"
            $ log_memory("hikari", "told him she was scared when he brought up Father's line")
            $ reward_attributes_once("day51_night_tell", [("insight", "small")], show="auto")
        "Read the fortune teller's page." if confidant_visits.get("fortune", 0) >= 3:
            "I take the folded page out of my pocket. The one she gave me on the corner. The one she said not to read until I was standing on it."
            "I unfold it. The paper is soft at the creases. The handwriting is small and careful."
            "It says: The sentence that moves is not the one you hear. It is the one you are about to hear."
            "I fold it again. I put it back in my pocket."
            mc "(She knew. She knew about the sentence. She knew it would move. She gave me this page weeks ago and she knew.)"
            mc "(Or she did not know. She wrote something that sounds like it fits, and I am fitting it to the thing that happened, because that is what you do with fortunes. You make them true after the fact.)"
            mc "(I do not know which one. I do not know if knowing which one would help.)"
            $ log_memory("fortune", "the folded page said the sentence that moves is not the one you hear it is the one you are about to hear")
            $ reward_attributes_once("day51_night_fortune", [("insight", "small")], show="auto")
        "Sit with the rain.":
            "I do not open the notebook again. I do not read the page. I sit at the desk and I listen to the rain."
            "The rain is on the window. The rain is on the roof. The rain is in the gutters. The rain is on the shrine and the shop and the station and the platform and the train and the gate and the campus and the corridor and the kitchen window."
            "The rain is real. Whatever else is happening, the rain is real."
            mc "(I am going to hold on to that. The rain is real. The rain does not repeat itself. The rain does not say someone else's sentence. The rain is just rain.)"
            $ log_memory("hikari", "sat with the rain and decided the rain was real")
            $ reward_attributes_once("day51_night_rain", [("nerve", "small")], show="auto")

    call night_close from _call_night_close_51

    "The room is dark. The bear is on the desk. The notebook is under him. The rain is on the window."
    "I lie down. The pillow is cool. The rain does what the rain does."
    "I sleep. The dream comes."

    scene black with Dissolve(1.5)
    pause 1.0

    # The dream: a white frame, longer than before. Not a flash. A room.
    scene bg_hospital with Dissolve(0.3)
    play sfx "audio/SFX/leak.mp3"

    "White. Walls. A bed. Wires at the wrists."
    "A voice. Patient. Female. Close."
    "He is talking in his sleep."
    "A second voice. Clinical. Male. Farther."
    "That is not supposed to happen yet."
    "Consolidation at seventy-eight percent."
    "The first voice again."
    "He is saying a sentence."
    "What sentence?"
    "The week is a machine."

    stop sfx
    scene black with Dissolve(0.2)
    pause 0.5

    "I wake up. The room is dark. The bear is on the desk. The rain is on the window."
    mc "(I was saying it in my sleep. The sentence. The one she said. The one he said. I was saying it in my sleep and they heard me.)"
    mc "(Who heard me?)"
    mc "(I do not know. I do not know who they are. I do not know where that room is. I know it is white and I know it has walls and I know it has wires and I know they call me something that is not my name.)"

    "The rain does not stop. The bear does not move. The notebook is under the bear and I do not reach for it."
    "I lie in the dark and I listen to the rain and I wait for the morning."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
