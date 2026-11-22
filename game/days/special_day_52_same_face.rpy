################################################################################
## DAY 52: FRIDAY, MAY 29, 2026
## The same face. The woman in the grey coat is everywhere. Hikari mentions
## it first, the way she does, like a question about the weather.
################################################################################

label special_day_52_same_face:
    $ set_story_day(52)
    call day_transition from _call_day_transition_52

    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)

    "The rain is still here. It was here when I slept. It is here when I wake. The window is the same color it was yesterday, which is the color of a pillowcase that has been washed too many times, and I am starting to think the window is going to be this color for a month."
    "I slept badly. The dream is still in the room the way smoke is in a room. The white walls. The bed. The wires. The voices. The sentence I was saying in my sleep."
    mc "(Consolidation at seventy-eight percent. I do not know what consolidation means. I do not know what seventy-eight percent of it is. I know the voice said it the way a voice says a thing it has said before, which is to say without interest.)"

    "My phone buzzes."

    $ run_chat("hikari", [
        {"them": "Are you awake?", "options": [
            {"label": "\"Yes.\"",
             "send": "Yes.",
             "them": ["Good. The rain is still here.", "I made tea. It is on the counter."]},
            {"label": "\"No.\"",
             "send": "No.",
             "them": ["Then this message will wait.", "The tea will not."]},
        ]},
    ])

    call murakami_daily_ping from _call_murakami_daily_ping_52

    scene bg_kitchen with walk_fade

    "The kitchen is warm. The tea is on the counter. Hikari is at the table, already eating. Father is gone. His newspaper is folded on his chair, which means he left early, which means the rain did not change his schedule."
    mother "He left at six. The train was on time."
    mc "In this rain?"
    mother "The rain does not change the train. That is what the train is for."
    hikari "Eat. You look like you slept in a field."
    mc "I slept in my bed."
    hikari "Your bed slept in a field. You were just in it."
    "She says it the way she says things, which is warm and flat at the same time. I eat. The rice is rice. The miso is miso. She does not say Father's sentence. I watch her for the whole meal. She does not say it."
    mc "(She did not say it. She did not say it yesterday, after breakfast. She did not say it today. The sentence moved once. It has not moved again. That does not make me feel better. It makes me wait.)"

    scene bg_home_exterior_day with walk_fade
    play music "audio/Music/(shibuya morning) scramble_hour.mp3" fadein 2.0

    "The street is wet. The shrine is wet. The shop is closed. The sign is right."
    "Hikari has the umbrella. She holds it over both of us. The rain taps the plastic."

    scene bg_station with walk_fade
    scene bg_platform with walk_fade

    "The platform is wet. The yellow line. The queue. The sign says one minute."
    "The woman in the grey coat is standing at the far end. The same coat. The same bag. The same weight on one foot."
    "She is reading her phone."
    mc"(She was here yesterday. She was on the train yesterday. She was at the gate yesterday. She is here today.)"
    "The train comes. She gets on the same car. She stands at the far end. She reads."

    scene bg_train_interior_day with walk_fade

    "The car is not crowded. The rain streaks the windows. The woman in the grey coat is at the far end."
    "I look at Hikari. She is looking at the woman."
    mc "You see her."
    hikari "See who?"
    mc "The woman. The grey coat. The bag."
    hikari "I see her."
    mc "You have seen her before."
    hikari "I have seen a lot of people before. Tokyo has a lot of people. Some of them ride the same train."
    mc "The same train. The same car. The same end."
    hikari "The same end is where she likes to stand. That is not strange. I stand at the same end."
    mc "You stand at this end."
    hikari "Then we are different. That is the point. People have ends they like."
    "She says it easily. She says it the way she says things that are true. I let it go. The train rocks. The rain streaks. The woman reads."

    scene bg_school_gate with Fade(0.0, 0.0, 1.5)
    play music "audio/Music/school.mp3" fadein 1.5
    $ phone_map_visit("school")

    "The gate. The guard. The wet path."
    "The woman in the grey coat is at the gate. She is walking through it. She has a lanyard around her neck that I cannot read from here."
    mc "(She was on the platform. She was on the train. She is at the gate. She is not a student. She has a lanyard. She works here, or she is visiting, or she is walking through a gate that anyone can walk through.)"
    "I do not mention it. Hikari is ahead of me. She does not look at the woman."

    scene bg_campus_interior with walk_fade
    scene bg_lecture_hall with walk_fade
    play music "audio/Music/classroom.mp3" fadein 1.0

    "The lecture is about the Meiji Restoration. The professor talks about a country that decided to change, and the speed at which it changed, and the people who were left behind by the speed, and the people who were not."
    "I take notes. I write the things he says. I do not think about the woman in the grey coat. I think about her for ten minutes. Then I write the things he says again."
    "The professor writes a date on the board. May. The twenty-ninth. Today. He looks at it. He does not erase it. He writes the lecture title under it."
    mc"(Today's date is today. That is a relief. I am keeping track of the things that are reliefs.)"

    scene bg_campus_interior with walk_fade

    "After the lecture I walk the corridor. Eleven doors. The wall. The fire extinguisher. The notice board. The third tile that squeaks."
    "The woman in the grey coat is at the far end of the corridor. She is walking away from me. She turns the corner."
    mc"(She is in the building. She is in the corridor. She was on the train and she is in the corridor and she is walking away from me.)"
    "I walk to the corner. I look around it. The corridor is empty."
    mc"(She turned the corner. She is not here. The corridor is empty. Corridors are empty when people turn corners. That is what corners are for.)"

    scene bg_campus_interior with walk_fade

    "I find Hikari in the courtyard. She is under the eaves. She is reading her phone. The umbrella is closed."
    hikari "You have a face."
    mc "What face?"
    hikari "The one from yesterday. The one you get when you have seen something and are deciding whether to say it."
    mc "I saw the woman again."
    hikari "The grey coat?"
    mc "Yes."
    hikari "Where?"
    mc "The platform. The train. The gate. The corridor."
    "She puts her phone in her pocket. She looks at me. She looks at me the way she looked at me yesterday, which is patient, which is the way you are patient with a person who is tired."
    hikari "Do you ever see someone and think you have seen them before, in exactly the same place, doing exactly the same thing?"
    mc "Yes."
    hikari "Me too."
    "She says it like a question about the weather. It is not a question about the weather."
    mc "You see them too?"
    hikari "I see faces. The same face in different places. The same coat. The same bag. The same weight on one foot."
    mc "The woman."
    hikari "Not just her. There are others. A man with a blue bag. A girl with a yellow hat."
    mc "The child."
    hikari "What child?"
    mc "The one from Asakusa. The one on the platform. The yellow hat."
    hikari "I did not see a child in Asakusa."
    mc "You were there."
    hikari "I was there. I did not see a child in a yellow hat. You told me about her on the day of the door. I did not see her."
    mc"(She did not see the child. She saw the woman. She saw the man with the blue bag. She did not see the child. We are seeing different faces, or we are seeing the same faces in different places, or one of us is seeing faces that are not there.)"
    hikari "It is probably nothing. Tokyo is a city. Cities have faces. People ride the same trains and walk the same streets and stand at the same ends of the same cars."
    mc "You said that already. On the train."
    hikari "I said it because it is true. It is still true."
    mc "It is true and it is not the whole thing."
    hikari "No. It is not the whole thing."
    "She says it quietly. The rain is on the courtyard. The eaves keep us dry. She does not say what the whole thing is. I do not ask."

    menu:
        "Ask her what she thinks it is.":
            mc "What do you think it is? The faces."
            hikari "I think the city is too big and too small at the same time. I think we see the same people because there are only so many people in a city, and only so many routes, and only so many ends of a train car."
            mc "And the child?"
            hikari "I did not see the child."
            mc "If you had?"
            hikari "Then I would worry. But I did not."
            "She says it the way she says things she means. She means it. She did not see the child. I saw the child. The woman is shared. The child is not."
            $ remember("mc", "sees the same face in three places but did not see the child in the yellow hat; they are seeing different things", "different_faces_split")
            $ reward_attributes_once("day52_ask_faces", [("insight", "small")], show="auto")
        "Ask her if she is afraid.":
            mc "Are you afraid?"
            hikari "Of the faces?"
            mc "Of any of it."
            hikari "I am not afraid of faces. Faces are just faces."
            mc "You said it is not the whole thing."
            hikari "It is not. Not being the whole thing is not the same as being afraid of it."
            "She looks at the rain. The rain does not look back."
            hikari "I am watching. That is different from being afraid. Watching is what you do when you are not sure what you are looking at yet."
            $ log_memory("hikari", "said she is watching not afraid and watching is what you do when you are not sure what you are looking at")
            $ reward_attributes_once("day52_ask_afraid", [("grace", "small")], show="auto")
        "Say nothing. Walk home together.":
            "I do not ask. She does not tell. We walk home under the umbrella and the rain taps the plastic and the city is wet and the faces are in it and we do not name them."
            mc"(She sees them too. That is enough for today. The whole thing can wait.)"
            $ reward_attributes_once("day52_walk_home", [("nerve", "micro")], show="auto")

    scene bg_home_exterior_night with walk_fade
    $ night_street()

    "The walk home is the walk home. The rain is the rain. The shrine is wet. The shop is closed. The sign is right."

    call dinner_open from _call_dinner_open_52

    "Dinner is quiet. Father is home. He eats. He does not say the machine line. He says something about the garden, which is too wet, and the drain, which is slow. Mother says she will call someone. Hikari eats and does not say much."
    "I watch her. She does not say Father's sentence. She does not say anyone's sentence. She eats her rice and her soup and she says good rice and thank you and that is all."
    mc"(She is quieter than usual. She is not sad. She is not tired. She is quiet the way a person is quiet when they are listening for something. I am listening for the same thing. Neither of us names it.)"

    call dinner_close from _call_dinner_close_52

    scene bg_room_night with stair_fade
    $ room_ambient(True)

    "Upstairs, the bear is on the desk. The notebook is under him. The rain is on the window."
    "I sit down. I open the notebook. I write: Friday. The woman in the grey coat was on the platform, on the train, at the gate, and in the corridor. Hikari sees her too. Hikari sees a man with a blue bag. Hikari did not see the child."
    "I write: Hikari asked if I ever see someone and think I have seen them before. She said me too. She said it like a question about the weather."
    "I write: She said it is not the whole thing. She did not say what the whole thing is."
    $ night_desk_line = "the notebook and the rain and the bear watching both"
    call night_open from _call_night_open_52

    menu:
        "Ask Hikari about the child.":
            mc "The child in the yellow hat. You said you did not see her."
            hikari "I did not."
            mc "I saw her three times. Asakusa. The platform. The gate."
            hikari "Three times."
            mc "Three times, in three places, doing the same thing."
            hikari "And I did not see her once."
            mc "We were together in Asakusa."
            hikari "We were. I did not see her."
            "She is in the doorway. She is not holding tea tonight. Her hands are empty."
            hikari "If you saw her and I did not, then one of us is wrong."
            mc "I do not think I am wrong."
            hikari "I do not think I am wrong either."
            mc "Then what?"
            hikari "Then we are both right, and the child was there and was not there, and that is not a thing I know how to say without sounding like I have lost something."
            "She leans against the doorframe. The rain is on the window. The hallway is dark behind her."
            hikari "Go to sleep. The rain will be here tomorrow."
            $ log_memory("hikari", "said they were both right about the child and that is not a thing she knows how to say without sounding like she has lost something")
            $ reward_attributes_once("day52_night_child", [("insight", "small")], show="auto")
        "Write about the dream.":
            "I open the notebook to a new page. I write about the dream."
            "I write: White walls. A bed. Wires at the wrists. Two voices. One patient, one clinical. They called me Subject 04. Consolidation at seventy-eight percent. I was saying the sentence in my sleep. The week is a machine."
            "I write: They said that is not supposed to happen yet. The talking in my sleep. That is not supposed to happen yet. Which means something is ahead of schedule. Or I am behind it."
            "I close the notebook. I put it under the bear. The pen goes on top."
            mc"(Subject 04. Not my name. A number. They gave me a number the way a lab gives a rat a number, and the rat does not know it has a number, and the number is not for the rat.)"
            $ reward_attributes_once("day52_night_dream", [("insight", "small")], show="auto")
        "Listen to the rain.":
            "I do not write. I do not ask. I sit at the desk and I listen to the rain."
            "The rain is on the window. The rain is on the roof. The rain is in the gutters. The rain is real."
            mc"(The rain is real. The faces are real or they are not. The child is real or she is not. The sentence is real or it moved. The dream is real or it is a dream. The rain is real. I am holding on to the rain.)"
            $ reward_attributes_once("day52_night_rain", [("nerve", "micro")], show="auto")

    call night_close from _call_night_close_52

    "The room is dark. The bear is on the desk. The rain is on the window."
    "I lie down. I close my eyes. The dream comes."

    scene black with Dissolve(1.5)
    pause 1.0

    # The dream: longer this time. The room has more detail.
    scene bg_hospital with Dissolve(0.3)
    play sfx "audio/SFX/leak.mp3"

    "White. Walls. A bed. Wires at the wrists and the chest."
    "A monitor. The line on it goes up and down. The line is green. The line is the only color in the room."
    "The first voice. Patient. Female. Close."
    "He is at seventy-nine percent."
    "The second voice. Clinical. Male. Farther."
    "That is faster than projected."
    "The first voice."
    "He is dreaming. The REM signature is unusual. He is talking."
    "The second voice."
    "What is he saying?"
    "The first voice."
    "A sentence. Repeated. The same one as yesterday."
    "The second voice."
    "That is not supposed to happen yet."
    "The first voice."
    "I know."
    "A pause. The monitor goes up and down. The line is green."
    "The second voice."
    "Is the sister fragment aware?"
    "The first voice."
    "She is the one who wrote the sentence."

    stop sfx
    scene black with Dissolve(0.2)
    pause 0.5

    "I wake up. The room is dark. The rain is on the window."
    mc"(The sister fragment. She is the one who wrote the sentence. They called her the sister fragment. They said she wrote it.)"
    mc"(I do not know what a sister fragment is. I know what a sister is. I know what Hikari is. I do not know what a fragment of her is.)"
    "The rain does not stop. The bear does not move. I lie in the dark and I hold the word fragment the way you hold a stone in your mouth, and it does not dissolve."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump act2_day_router
