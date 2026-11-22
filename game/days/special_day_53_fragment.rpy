################################################################################
## DAY 53: SATURDAY, MAY 30, 2026
## The fragment. Saturday in the rain. The word from the dream will not leave.
## He walks the city and the faces blur and the shrine water is cold and real.
################################################################################

label special_day_53_fragment:
    $ set_story_day(53)
    call day_transition from _call_day_transition_53

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "Saturday. The rain is still here. The house is quiet in the way a house is quiet on a Saturday, which is different from the way it is quiet on a weekday, because on a weekday the quiet is between sounds and on Saturday the quiet is the sound."
    "I slept late. The dream is still in the room."
    mc"(The sister fragment. She is the one who wrote the sentence. They said it in the dream, in the white room, in the voices that call me Subject 04. They said she wrote it.)"
    mc"(I do not know what a fragment is. I know what a sister is. I know what Hikari is. She is the person who made tea this morning and held the umbrella over me in the rain and asked if I ever see faces. She is not a fragment. A fragment is a piece of something that broke. She has not broken.)"
    mc"(Or she has, and I did not see it, the way I did not see the child and she did not see the child and we were both right.)"

    "My phone buzzes."

    $ run_chat("hikari", [
        {"them": "You slept late. The tea is cold. I made more.", "options": [
            {"label": "\"Thank you.\"",
             "send": "Thank you.",
             "them": ["Do not thank me for tea. Thank me for making it twice."]},
            {"label": "\"I dreamed again.\"",
             "send": "I dreamed again.",
             "them": ["I know. I heard you.", "Through the wall."]},
        ]},
    ])
    mc"(She heard me through the wall. She heard me dreaming. I do not know what I said. I do not know if she heard the voices or only me.)"

    scene bg_kitchen with walk_fade

    "The kitchen is warm. Father is at the table with the newspaper. Mother is at the stove. Hikari is at her place, holding a cup of tea with both hands, the way she holds it when the cup is warm and the morning is not."
    father "Saturday."
    mc "Saturday."
    father "No school."
    mc "No school."
    father "Then you have an afternoon. Use it. Do not waste it on the sofa."
    mc "I know."
    father "You say that every time."
    mc "Because you say that every time."
    "He turns the newspaper. He does not smile. He does not not smile. He is Father, and Father on a Saturday morning is a man who has said what he says and is now reading the paper."
    "Hikari watches me over the rim of her cup. She does not say anything. She drinks. She puts the cup down."
    hikari "You look better."
    mc "I do not feel better."
    hikari "Then you look better than you feel. That is something."
    mother "Eat. Both of you. The rice is not going to eat itself."
    "I eat. The rice is rice. The miso is miso. Hikari does not say Father's sentence. She does not say anyone's sentence. She eats and she drinks her tea and she is quiet, and the quiet is the kind of quiet that has a shape, and the shape is the shape of a person who is listening for something."

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The street is wet. The rain is lighter today. It is the kind of rain that does not need an umbrella, but you carry one anyway, because it does not promise to stay light."
    "The shrine is at the corner. The steps are wet. The temizuya is full. The ladle is floating."

    menu:
        "Go to the shrine.":
            "I cross the street. The steps are wet. The water in the temizuya is cold and clean."
            "I pick up the ladle. I pour the water over my left hand. Then my right. The cold goes up my wrists and into my arms and it is real, the way the rain is real, the way the cold is real."
            "I wash twice. I hold my wrists under the water longer than the order requires."
            mc"(A handle was warm where there was no door. This is cold, and it is here. I will take what is here.)"
            "I say it out loud, quietly, to the water."
            mc "I am ready."
            "The water does not answer. The water does not count. It just runs."
            "I put the ladle back. I stand on the wet steps. The shrine is small and old and the wood is dark from the rain and the bell rope is still and the ema wall is full of wooden plaques with wishes on them, and none of the wishes are mine, and all of them are real."
            $ log_memory("hikari", "washed at the shrine in the rain and said I am ready and the water did not answer")
            $ reward_attributes_once("day53_shrine", [("grace", "small")], show="auto")
        "Walk the city.":
            "I walk. The rain is light. The streets are wet. The gutters are running."
            "I walk past the station. Past the combini. Past the school gate, which is closed on a Saturday. Past the campus, which is empty."
            "The woman in the grey coat is at the campus gate. She is standing with her weight on one foot, reading her phone. The gate is closed. She is not going in. She is standing."
            "I walk past her. She does not look up."
            "I turn the corner. The man with the blue bag is at the vending machine. He is buying something. He puts coins in. He presses a button. A can drops. He picks it up. He walks away."
            mc"(Hikari said she sees a man with a blue bag. I see him now. He is at the vending machine. He is buying a drink. That is a thing a man does at a vending machine. That is not strange. That is a man buying a drink.)"
            "I walk. The rain is light. The faces are faces. The city is the city. I am in it."
            $ reward_attributes_once("day53_walk", [("nerve", "small")], show="auto")
        "Stay home.":
            "I go back inside. The house is warm. The kitchen is clean. Mother is in the living room, reading."
            "I sit at the desk. I open the notebook. I do not write. I look at the corridor map. Eleven doors. The wall where the twelfth was."
            "I close the notebook. I put it under the bear. I sit with the bear and the timer and the rain on the window."
            mc"(I am not ready to walk. I am not ready to write. I am ready to sit, which is a kind of ready, which is the kind I have.)"
            $ reward_attributes_once("day53_stay_home", [("nerve", "micro")], show="auto")

    scene bg_home_exterior_night with walk_fade
    $ night_street()

    "The afternoon goes the way an afternoon goes when you are waiting for the evening and the evening is the same as the afternoon, which is to say it is wet and it is quiet and it does not end."
    "The walk home is the walk home. The shrine. The shop. The sign. The house."

    call dinner_open from _call_dinner_open_53

    "Dinner is rice and soup and something with egg. Father is quiet. Mother is quiet. Hikari is quiet. The three of them are quiet the way a family is quiet when the rain has been on the house for three days and nobody has said anything about it that is not about the rain."
    "I eat. I watch Hikari. She does not say the sentence. She does not say any sentence that is not hers."
    father "The drain is slow."
    mother "I will call someone on Monday."
    father "Monday."
    mother "Monday."
    "The conversation is the conversation. The egg is the egg. The rain is on the window."

    call dinner_close from _call_dinner_close_53

    scene bg_room_night with stair_fade
    $ room_ambient(True)

    "Upstairs, the bear is on the desk. The notebook is under him. The rain is on the window."
    "I sit down. I do not open the notebook. I sit with the word."
    mc"(Fragment. A piece of something that broke. She is the one who wrote the sentence. They said she wrote it. She wrote the sentence that Father says, that Hikari said, that I said in my sleep. She wrote it.)"
    mc"(If she wrote it, then she is not just saying it. She is remembering it. The way you remember a thing you made. The way the chef remembers the recipe. The way Sim remembers the photograph. She wrote it, and it is in the house, and it is in Father's mouth, and it was in mine.)"
    mc"(I do not know what that makes her. I do not know what that makes me.)"

    $ night_desk_line = "the bear and the notebook and the word he is holding"
    call night_open from _call_night_open_53

    menu:
        "Ask Hikari what she heard.":
            mc "You said you heard me. Through the wall. Last night."
            hikari "I did."
            mc "What did I say?"
            hikari "A sentence. The same one."
            mc "The machine line."
            hikari "Yes."
            mc "Was I saying anything else?"
            "She is in the doorway. She is holding the doorframe the way she holds it when she is deciding whether to come in."
            hikari "You said a word I did not know."
            mc "What word?"
            hikari "Fragment."
            "The room is quiet. The rain is on the window. The bear is on the desk. The word is in the room now, the way it was in the dream, and she heard it, and she does not know what it means, and I do not know what it means, and we are both standing in it."
            mc "I do not know what it means either."
            hikari "Then we are even."
            mc "Then we are even."
            "She does not come in. She does not leave. She holds the doorframe and she looks at me and the rain taps the window and the word sits between us like a stone on a table."
            hikari "Good night."
            mc "Good night."
            "She goes. The door clicks. The hallway is dark."
            mc"(She heard me say fragment. She heard me say it in my sleep. She did not know what it meant. She does not know what it means. I do not know what it means. But they know. The voices in the white room know. They said she is the sister fragment. They said she wrote the sentence. And she is standing in the hallway of this house, not knowing any of it, and I am sitting at this desk, not knowing what to do with knowing it.)"
            $ log_memory("hikari", "heard him say fragment in his sleep and did not know what it meant")
            $ reward_attributes_once("day53_night_fragment", [("insight", "small")], show="auto")
        "Turn over the fortune teller's page." if confidant_visits.get("fortune", 0) >= 3:
            "I take the folded page out of my pocket. The one she gave me on the corner. The one she said not to read until I was standing on it."
            "I unfold it. The paper is soft at the creases. The handwriting is small and careful."
            "It says: The sentence that moves is not the one you hear. It is the one you are about to hear."
            "I turn it over. There is more on the back. I did not look at the back before."
            "It says: The fragment does not know it is a fragment. That is what makes it kind."
            "I fold it again. I put it in my pocket."
            mc"(She knew. She knew about the fragment. She knew the fragment does not know. She wrote this page before I heard the word, and the word is in the page, and the page was in my pocket the whole time.)"
            mc"(The fragment does not know it is a fragment. That is what makes it kind. Hikari is kind. Hikari does not know. That is what makes her kind.)"
            mc"(I am going to hold on to that. The way I hold on to the rain. The fragment is kind. The rain is real. Those are the two things I have.)"
            $ remember("mc", "opened the folded page: the fragment does not know it is a fragment, and that is what makes it kind", "folded_page_opened")
            $ reward_attributes_once("day53_night_fortune", [("insight", "small")], show="auto")
        "Sit with the rain.":
            "I do not ask. I do not read. I sit at the desk and I listen to the rain."
            "The rain is on the window. The rain is on the roof. The rain is in the gutters. The rain is real."
            mc"(I have the rain. I have the cold water at the shrine. I have the bear on the desk. I have the notebook under the bear. I have the word fragment, which I do not understand. I have the dream, which I do not want. I have Hikari, who is kind, who does not know, who heard me say it in my sleep.)"
            mc"(That is what I have. It is not enough. It is what I have.)"
            $ reward_attributes_once("day53_night_rain", [("nerve", "small")], show="auto")

    call night_close from _call_night_close_53

    "The room is dark. The bear is on the desk. The rain is on the window."
    "I lie down. I close my eyes. The dream comes."

    scene black with Dissolve(1.5)
    pause 1.0

    # The dream: the room is clearer now. The voices are closer.
    scene bg_hospital with Dissolve(0.3)
    play sfx "audio/SFX/leak.mp3"

    "White. Walls. A bed. Wires at the wrists and the chest and the head."
    "The monitor. The green line. The line goes up and down."
    "A window in the wall. The window is dark. There is nothing on the other side of the window."
    "The first voice. Patient. Female. Close."
    "He is at eighty percent."
    "The second voice. Clinical. Male. Farther."
    "The projection was ninety days. We are at fifty-three."
    "The first voice."
    "He is ahead."
    "The second voice."
    "The sister fragment is accelerating it."
    "The first voice."
    "She was not supposed to."
    "The second voice."
    "She was not supposed to do a lot of things. She leaked. She is leaking. The sentence is in the house now."
    "The first voice."
    "He heard it in the dream."
    "The second voice."
    "He heard us."
    "A pause. The monitor goes up and down. The green line is the only color."
    "The first voice."
    "He is awake."
    "The second voice."
    "Not yet."
    "The first voice."
    "He is awake."

    stop sfx

    # The dream does not end. The room is still here. The window is dark.
    # The voices are still here. He is awake in the dream, and the dream
    # does not end, and the room is white and the line is green and the
    # voices are talking about him the way voices talk about a thing on a
    # table.

    "I open my eyes. The room is white. The window is dark. The monitor goes up and down."
    "I can see the monitor. I could not see it before. I was not supposed to see it."
    "The voices stop."
    "The first voice. Close. Right beside me."
    "He can see."
    "The second voice. Farther."
    "That is not supposed to happen yet."
    "The first voice."
    "I know."

    # A glitch. The room tears. The white walls split into chromatic
    # bands for one frame, and the green line doubles, and the window
    # shows a street in the rain for a half-second, and then it is the
    # white room again.
    show layer master at glitch
    pause 0.12
    show layer master

    "I close my eyes. I open them. The room is dark. My room. The bear. The desk. The rain."
    mc"(I saw it. I saw the room. I saw the monitor. I saw the window. I heard them. They know I heard them. They said that is not supposed to happen yet.)"
    mc"(I am awake. I was awake in the dream. They know I was awake in the dream.)"
    "The rain is on the window. The bear is on the desk. The house is quiet. Somewhere downstairs, a door I have counted opens and closes."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
