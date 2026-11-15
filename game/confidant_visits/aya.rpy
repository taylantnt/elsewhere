################################################################################
## AYA — THE MAID CAFE
################################################################################
##
## Visit 1 happened in script.rpy, on the day he wandered into Akihabara: the
## omurice, the kitty in ketchup, the spell, and the WIRE card. Everything
## after that lives here. The arc is the one the documentation folder under
## Maid Cafe - Aya/ describes: recognition, then the slow work of a person
## taking the mask off one layer at a time, until the last visit is the only
## one where she is not performing at all.

# Defined late so type_sound (script.rpy) already exists when this runs.
init 999 python:
    shiori = Character("Shiori", color="#dda0dd", callback=type_sound, image="aya")

label confidant_visit_aya:
    $ visit = confidant_visits.get("aya", 0)
    if visit == 1:
        jump aya_visit_02
    elif visit == 2:
        jump aya_visit_03
    elif visit == 3:
        jump aya_visit_04
    elif visit == 4:
        jump aya_visit_05
    elif visit == 5:
        jump aya_visit_06
    elif visit == 6:
        jump aya_visit_07
    return

label aya_common_open:
    scene bg_maidcafe with walk_fade
    stop music fadeout 1.2
    play music "audio/Music/maidcafe.mp3" fadein 2.0
    $ phone_map_visit("akihabara")
    return

label aya_visit_02:
    call aya_common_open

    "The bell over the door rings before I am fully inside, and the room answers it."
    "Jackets off, voices up, the whole ritual of arriving somewhere that has decided to be happy about it."
    "I scan the aprons for pink hair and find it on the far side of the room, already waving."

    maid "Okaerinasaimase, Goshujin-sama!"
    "The chorus comes from everywhere at once, cheerful and slightly out of tune with each other."

    aya "Master! You came back!"
    "She crosses the room at a speed that suggests she was already halfway here."
    "Not the professional warmth of a first visit. Something faster. Almost relief."

    mc "I did. The omurice was too good to only eat once."
    aya "Ha! Most people say that and then never come back. Foreign guests especially. They come for the 'Maid Cafe experience,' take one photo, and that is the whole story."
    aya "But you— you actually came back. I half expected to forget your face by now."
    "She says it lightly, but she is already pulling out 'your' table, the one by the window with the sticker on the leg."

    menu:
        "Same as last time." :
            mc "Same as last time, please. The omurice."
            aya "Predictable! But I will allow it."
            aya "At least it means I am doing my job well."
            $ reward_attributes_once("aya_visit_02_same", [("grace", "micro")], show="auto")
        "Surprise me again." :
            mc "Surprise me again."
            aya "Dangerous answer! Now I get to pick, and I hope you are ready for a real maid cafe classic."
            $ reward_attributes_once("aya_visit_02_surprise", [("nerve", "micro")], show="auto")
        "What do you recommend today?" :
            mc "What do you recommend today?"
            aya "You actually asked for my opinion? Well then— let me think."
            aya "The curry rice is good today. I will make sure it looks cute for you."
            $ reward_attributes_once("aya_visit_02_recommend", [("insight", "micro")], show="auto")

    "She writes it down, and instead of walking away she stays at the edge of the table, tray against her hip."
    aya "By the way… you probably guessed already, but I am the cafe's 'English emergency team.'"
    "She laughs, a small real one this time."
    aya "I have been studying English on my own for a while, so when we get guests like you, I am the one who gets picked. Lucky me."
    aya "I actually like it, though. It is fun to use what I have learned. Sometimes I even pick up little things about other cultures."
    aya "I guess I am traveling without leaving Tokyo."

    menu:
        "That sounds lonely." :
            mc "That sounds a little lonely. Being the only bridge between languages."
            aya "Maybe! But someone has to do it."
            aya "And honestly? I like being useful in a way that is not just serving coffee."
            $ reward_attributes_once("aya_visit_02_lonely", [("insight", "micro")], show="auto")
        "Do you want to travel for real?" :
            mc "Do you want to travel somewhere for real?"
            aya "Someday, maybe. Canada, or somewhere warm. I have only been dreaming about it."
            aya "For now, Tokyo is where the customers are."
            $ reward_attributes_once("aya_visit_02_travel", [("nerve", "micro")], show="auto")
        "You picked a good job for that." :
            mc "You picked a good job for learning languages."
            aya "They picked me, actually. But I am not complaining."
            $ reward_attributes_once("aya_visit_02_picked", [("grace", "micro")], show="auto")

    "The food arrives, and this time she does not just set it down and leave."
    "She stands beside the table with the marker, and for a moment she just looks at me like she is deciding whether I am worth the effort."
    aya "Now… it is time for your custom art again. Same request as before? Or do you trust my artistic vision today?"

    menu:
        "Surprise me." :
            mc "Surprise me."
            aya "Alright, but do not complain if it looks like a strange creature. I am still practicing!"
            $ reward_attributes_once("aya_visit_02_art_surprise", [("nerve", "micro")], show="auto")
        "Same as last time." :
            mc "Same as last time, please."
            aya "Consistency. I respect that. But next time, I will convince you to let me draw something fun."
            $ reward_attributes_once("aya_visit_02_art_same", [("grace", "micro")], show="auto")

    scene bg_maidcafe_omurice with Dissolve(0.5)

    "She draws fast, the way people draw when they have done it a hundred times and still enjoy it."
    "It is not the kitty this time. It is a rabbit, holding a tiny train."

    aya "A rabbit. You looked like someone who would appreciate the effort."
    mc "I do. It is very good."
    aya "Flattery will get you everywhere in this cafe."

    scene bg_maidcafe with Dissolve(0.5)

    "Before I eat, she clasps her hands, and her face does something it did not do on the first visit."
    "The smile gets quieter, and for half a second I can see the person under the performance."

    voice "audio/VO/moekyun.mp3"
    aya "Moe moe… kyun!"

    "The spell is shorter now, more routine, but it is also more hers."
    "I catch myself copying the hand motion without being asked."

    "I eat. The curry is better than it has any right to be, and the drawing is still there when I am done."
    "She comes back to clear the table, and this time she does not go straight to the next customer."
    aya "Hey… do you think it is silly? All of this. The costumes, the spells, the chants."

    menu:
        "It's a little silly, but in a fun way." :
            mc "It is a little silly, but in a fun way. Like playing pretend again."
            aya "Exactly! A good kind of silly."
            $ reward_attributes_once("aya_visit_02_silly", [("grace", "micro")], show="auto")
        "Not silly at all. It makes people smile." :
            mc "Not silly at all. It makes people smile. That is not nothing."
            aya "…Thanks. That is what I want to believe, too."
            $ reward_attributes_once("aya_visit_02_smile", [("grace", "micro")], show="auto")
        "I don't know yet." :
            mc "I do not know yet. I am still figuring Japan out."
            aya "Fair answer. Give it time."
            $ reward_attributes_once("aya_visit_02_time", [("insight", "micro")], show="auto")

    "She bows lightly as she takes the plate, but the smile she gives me back is different."
    "Less of a performance. More her own."
    aya "See you next time, Master."
    mc "I will try not to make you wait too long."
    aya "I will hold you to that."
    $ aya_affection += 1

    $ confidant_visits["aya"] = max(confidant_visits.get("aya", 0), 2)
    $ remember("aya", "came back to the maid cafe and she remembered him")
    $ queue_message("aya", "Master! I drew you a rabbit today! Do not forget to come back before the season changes!", day="yesterday")
    $ reward_attributes_once("aya_visit_02_close", [("grace", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return

label aya_visit_03:
    call aya_common_open

    "The cafe is quiet this afternoon. A few students in the corner, a couple of salarymen nursing coffee."
    "It is the version of the place that exists between the rushes, when the performance has more space to breathe."

    "Aya spots me almost immediately, but instead of the usual bright approach, she simply raises two fingers to her lips."
    "Shh. Not yet."

    "She finishes what she is doing, then crosses the room at her usual speed and sits down on the edge of my table."
    "Not standing over it. Sitting. Which I do not think maids are supposed to do."

    aya "Okay, I am breaking the rules for exactly one minute. Do not tell the manager."
    mc "I will not tell the manager."
    aya "Good. Because the truth is, some days this job is fun and some days it is… a lot."

    "She turns her apron string absently around one finger while she talks."
    aya "I like making people smile. I really do. But sometimes I wonder if anyone ever asks how I am."
    aya "Everyone sees the maid. The cute apron, the cheerful voice, the drawing. Nobody asks if the person inside is tired."

    menu:
        "How are you, actually?" :
            mc "How are you, actually? Not the maid version. You."
            aya "…Tired, mostly. But that is not a very interesting answer, is it?"
            $ reward_attributes_once("aya_visit_03_how", [("grace", "micro")], show="auto")
        "Do you ever get to just be yourself here?" :
            mc "Do you ever get to just be yourself here?"
            aya "Sometimes. When the customer is interesting. When they actually look at me instead of through me."
            $ reward_attributes_once("aya_visit_03_self", [("insight", "micro")], show="auto")
        "That sounds exhausting." :
            mc "That sounds exhausting. Pretending to be cheerful all day."
            aya "It is. But it is also… familiar. I am used to it."
            $ reward_attributes_once("aya_visit_03_exhausting", [("nerve", "micro")], show="auto")

    "She looks away for a second, toward the window, and something crosses her face that is not the maid smile."
    aya "You know what I actually like? Not this. Not the cafe part."
    aya "I like performing. Real performing. On a stage, with lights, with people who came because they wanted to hear something."
    aya "I used to dream about being a singer. Or maybe just… being on stage somehow. I am not sure which one anymore."

    menu:
        "Have you ever tried?" :
            mc "Have you ever actually tried? Singing, or performing?"
            aya "A little. Karaoke, school festivals, things like that. But nothing real. Nothing that counted."
            aya "And then I got this job, and the costume became the whole thing. It is hard to tell where the dream ends and the uniform begins."
            $ reward_attributes_once("aya_visit_03_tried", [("insight", "micro")], show="auto")
        "That dream still sounds alive." :
            mc "That dream still sounds alive."
            aya "Does it? I am not sure. It is easy to say it out loud and then just… keep serving parfaits."
            $ reward_attributes_once("aya_visit_03_alive", [("grace", "micro")], show="auto")
        "You should try. For real." :
            mc "You should try. For real. Not karaoke. An actual stage."
            aya "…It is easy for you to say. You are not the one who has to walk back into this cafe afterward."
            aya "But thank you. It helps hearing that from someone who is not my mother."
            $ reward_attributes_once("aya_visit_03_try", [("nerve", "micro")], show="auto")

    "She catches herself, straightens up, and the maid comes back like a coat being put on."
    "But she does not stand up right away. She sits there for one more second, and I think she is deciding if I am safe."

    aya "Anyway! That was too much for an afternoon parfait."
    "She smiles, and this time it reaches her eyes a little."
    aya "Let me get your food before I say something I cannot take back."

    "The omurice arrives with a small heart drawn in ketchup, slightly crooked, clearly drawn by someone whose mind was elsewhere."
    aya "Sorry. It is not my best work today."
    mc "I think it is my favorite one so far."
    aya "…You are trouble, Master."

    "She takes the empty plate without ceremony and heads back to the kitchen."
    "I realize I have been watching her work all afternoon without noticing the time pass."
    $ aya_affection += 1

    $ confidant_visits["aya"] = max(confidant_visits.get("aya", 0), 3)
    $ remember("aya", "heard about her dream of performing and the way the maid uniform hides it")
    $ queue_message("aya", "I could not stop thinking about what you said today. Maybe I will try something. Maybe not. But I am thinking about it.", day="yesterday")
    $ reward_attributes_once("aya_visit_03_close", [("insight", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return

label aya_visit_04:
    call aya_common_open

    "The cafe smells like coffee and butter today, and the light through the windows is the color of late afternoon."
    "A new girl is working the counter, but Aya finds me anyway, weaving between tables with a tray that is somehow always level."

    aya "Master! You picked a good day. The light is nice today."
    mc "You sound different today."
    aya "Different how?"
    mc "More like yourself. Less like the cafe version."
    "She laughs, but it is not quite the bright one."
    aya "You are getting dangerous, Master. A man who can tell the difference is a man who should be careful."

    "She sets my drink down and does not leave. She pulls the chair across from me, the one meant for staff breaks, and sits."
    "The other maids pretend not to see. One of them mouths 'five minutes' and holds up a hand."
    aya "I am allowed five minutes. I am using three."

    aya "So… I have been meaning to ask you something."
    aya "Why did you come to Japan? Just to travel, or something more?"

    menu:
        "For school. I have a scholarship here." :
            mc "For school, mostly. I have a scholarship here. I did not fully choose it; it chose me."
            aya "That sounds like the kind of thing that happens to everyone eventually."
            aya "You came anyway. That is more brave than it sounds."
            $ reward_attributes_once("aya_visit_04_school", [("insight", "micro")], show="auto")
        "For a change. I was tired of my old life." :
            mc "For a change. I was tired of my old life, and this was far enough to be different."
            aya "That is honest. I like honest."
            aya "I did something like that once. I studied abroad for a short time. It was… louder there. Freer."
            $ reward_attributes_once("aya_visit_04_change", [("nerve", "micro")], show="auto")
        "I am still figuring it out." :
            mc "I am still figuring it out. Japan happened before I had a plan for it."
            aya "That might be the best answer. Plans are for people who already know what they want."
            $ reward_attributes_once("aya_visit_04_figuring", [("grace", "micro")], show="auto")

    "She turns her cup slowly on the table, and for a moment the performance is completely gone."
    aya "I studied abroad once, you know. Just for a few months. Canada, I think it was. Or maybe it was Australia. I mix them up."
    aya "But the place does not matter. What matters is that for those months, nobody expected me to be a maid, or a daughter, or a smile."
    aya "I could just… be a person. Order coffee wrong, laugh too loud, ask stupid questions. Nobody cared."

    menu:
        "What was it like coming back?" :
            mc "What was it like coming back?"
            aya "Like putting a costume back on that you had forgotten was a costume."
            aya "Here, we wear uniforms, roles, even smiles like masks. Sometimes I wonder if people ever see the real me."
            $ reward_attributes_once("aya_visit_04_back", [("insight", "micro")], show="auto")
        "Do you think they see you?" :
            mc "Do you think they see you? The real you, I mean."
            aya "…Sometimes. When someone asks the right question."
            aya "You are asking the right questions, Master. That is dangerous for me."
            $ reward_attributes_once("aya_visit_04_see", [("grace", "micro")], show="auto")
        "Masks are human too." :
            mc "Masks are human too. Everyone wears one sometimes."
            aya "True. But some of us wear them so long we forget there is anything underneath."
            $ reward_attributes_once("aya_visit_04_masks", [("nerve", "micro")], show="auto")

    "Another maid hovers at the edge of our table, tray in hand, clearly waiting for permission to interrupt."
    aya "Not yet. Two more minutes."
    "The maid retreats. Aya watches her go, then looks back at me."
    aya "You know what is strange? I have been doing this job for two years, and you are the first person who ever asked me why I came to Japan."
    aya "Everyone else asks what I recommend, or if I can draw something specific, or how much the photo set costs."
    aya "Nobody asks why."

    menu:
        "Because I wanted to know." :
            mc "Because I wanted to know. That is all."
            aya "…That is all? That is the whole reason?"
            aya "You are either very honest or very dangerous. I have not decided which yet."
            $ reward_attributes_once("aya_visit_04_wanted", [("grace", "micro")], show="auto")
        "You seemed like someone worth asking." :
            mc "You seemed like someone worth asking. That is all."
            aya "Careful, Master. Say things like that and I might start believing them."
            $ reward_attributes_once("aya_visit_04_worth", [("nerve", "micro")], show="auto")

    "She checks the time on her phone and stands, smoothing her apron."
    "The maid mask goes back on, but it sits differently today. Looser."
    aya "I have to go. But… thank you for sitting with me. Not as a customer. Just… sitting."
    mc "Anytime."
    aya "I will remember that."

    $ aya_affection += 1

    $ confidant_visits["aya"] = max(confidant_visits.get("aya", 0), 4)
    $ remember("aya", "she told him about studying abroad and wondering if anyone sees the real her")
    $ queue_message("aya", "I keep thinking about our conversation today. You asked questions nobody else asks. I do not know what to do with that yet.", day="yesterday")
    $ reward_attributes_once("aya_visit_04_close", [("nerve", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return

label aya_visit_05:
    call aya_common_open

    "The cafe is nearly empty when I arrive. Just one table of students and the soft hum of the machines."
    "Aya is there, but something is off. Her voice is a little hoarse, and the brightness takes an extra second to switch on."

    aya "Welcome back, Master! You came at a good time— actually, no, you came at a very quiet time. That is better."
    "She says it warmly, but I can hear the effort in it."

    "We sit. She does not do the usual menu presentation. She just watches me with eyes that are tired in a way that has nothing to do with sleep."
    aya "Can I tell you something? And you have to promise not to make it weird."
    mc "I promise."
    aya "I have been thinking about quitting."

    "The words land softly, but they land."
    aya "Not today, not tomorrow. But soon. Maybe next month, maybe next year. I do not know yet."
    aya "My parents do not really approve of this job. They think it is frivolous. Not respectable. A waste of my education."
    "She turns her cup again, the way she does when she is saying something she has practiced in her head."
    aya "And they might be right. I mean… what does a twenty-two-year-old maid cafe worker become? Another cute face in another apron?"

    menu:
        "What would you do instead?" :
            mc "What would you do instead? If you quit, what would you want?"
            aya "I do not know. That is the problem. I have ideas, but nothing solid."
            aya "Maybe I would study something. Maybe I would move somewhere. Maybe I would just… stop performing for a while."
            $ reward_attributes_once("aya_visit_05_instead", [("insight", "micro")], show="auto")
        "Your parents do not have to understand everything." :
            mc "Your parents do not have to understand everything. This is your life."
            aya "I know. But knowing and doing are different things."
            aya "I love them. That is the part that makes it hard. Their disappointment feels like a weight I carry even when I am smiling."
            $ reward_attributes_once("aya_visit_05_parents", [("grace", "micro")], show="auto")
        "It sounds like you are carrying a lot." :
            mc "It sounds like you are carrying a lot. More than the apron shows."
            aya "…You notice that? Most people just see the maid."
            $ reward_attributes_once("aya_visit_05_carrying", [("nerve", "micro")], show="auto")

    "She looks down at the table, and for a moment she is just a girl who is tired, not a character in an apron."
    aya "You know what is strange? When I talk with you, I feel a little braver."
    aya "Like maybe I could actually do something. Something that is mine. Not just… this."

    menu:
        "You already are doing something." :
            mc "You already are doing something. You are talking about it. That is more than most people do."
            aya "Is it? Maybe. Maybe that is enough for now."
            $ reward_attributes_once("aya_visit_05_doing", [("grace", "micro")], show="auto")
        "Bravery is just fear with better posture." :
            mc "Bravery is just fear with better posture. You already have the fear part."
            aya "…That is either very wise or very stupid. I cannot tell which."
            aya "But I will take it."
            $ reward_attributes_once("aya_visit_05_brave", [("nerve", "micro")], show="auto")
        "What would make you stay?" :
            mc "What would make you stay? Is there anything that would keep you here?"
            aya "The customers, maybe. The regulars who actually see me."
            aya "And… you. I am not saying that to be nice. It is just true."
            $ reward_attributes_once("aya_visit_05_stay", [("insight", "micro")], show="auto")

    "A manager passes by the table, and Aya straightens up instantly. The maid comes back on like a switch."
    "But she does not stand up to leave. She stays seated, and the manager moves on."

    aya "I should go. I have tables to clear, orders to take, smiles to perform."
    "She stands, and for a second she looks like she wants to say more. Then she does not."
    aya "But thank you. For listening. You are kind, Master. Kind in a way that is not just customer service."
    mc "I will see you next time."
    aya "I will be here. I am always here. That is the problem."

    $ aya_affection += 1

    $ confidant_visits["aya"] = max(confidant_visits.get("aya", 0), 5)
    $ remember("aya", "she confessed she is thinking of quitting and that he makes her feel braver")
    $ queue_message("aya", "I did not sleep well last night. I keep thinking about what I said. Maybe I am finally ready to do something about it.", day="yesterday")
    $ reward_attributes_once("aya_visit_05_close", [("grace", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return

label aya_visit_06:
    call aya_common_open

    "The cafe feels different today. Lighter. The usual noise is there, but something underneath it has shifted."
    "Aya is there, but she is not doing the full performance. She is smiling, but it is a real smile, not a costume."

    aya "Master! You came at the right time. I have something to tell you."
    "She says it before I even sit down, which is not like her. Usually she makes me wait for the performance to begin."

    menu:
        "Tell me." :
            mc "Tell me."
            aya "I auditioned."
            $ reward_attributes_once("aya_visit_06_audition", [("nerve", "micro")], show="auto")
        "What kind of audition?" :
            mc "What kind of audition?"
            aya "A singing contest. Local, small, not a big deal. But I actually went. I actually sang."
            $ reward_attributes_once("aya_visit_06_kind", [("insight", "micro")], show="auto")
        "You look different." :
            mc "You look different today."
            aya "I feel different. Like I am allowed to exist outside the apron for a little while."
            $ reward_attributes_once("aya_visit_06_different", [("grace", "micro")], show="auto")

    "She sits across from me, and for once she does not check if the manager is watching."
    aya "I was so nervous I could not eat breakfast. My hands were shaking. I thought I would throw up in the green room."
    aya "But then I sang, and it was… not perfect. But it was mine. And nobody laughed."
    "She looks down at her hands, and I see that they are still slightly shaking. Not from fear anymore. From something else."

    menu:
        "How did it feel?" :
            mc "How did it feel? When you sang."
            aya "Like coming home to a place I did not know I had left."
            aya "For three minutes, I was not a maid. I was just… a person who could sing."
            $ reward_attributes_once("aya_visit_06_felt", [("insight", "micro")], show="auto")
        "Are you going to do it again?" :
            mc "Are you going to do it again? Another audition, another show?"
            aya "I think so. I do not know if I will succeed. But just applying made me feel alive."
            aya "I did not know I was allowed to want things."
            $ reward_attributes_once("aya_visit_06_again", [("nerve", "micro")], show="auto")
        "I am proud of you." :
            mc "I am proud of you."
            aya "…You do not even know me that well."
            mc "Maybe I do. Maybe that is the point."
            aya "You are very dangerous, Master. You say things that make me want to believe them."
            $ reward_attributes_once("aya_visit_06_proud", [("grace", "micro")], show="auto")

    "She reaches into her apron pocket and pulls out a small sketchbook. It is worn at the corners, covered in doodles and half-finished designs."
    aya "I have been drawing too. Streetwear, mostly. Things I would wear if I were not wearing this."
    "She opens it to a page that shows a hoodie with a cat on the front, drawn in careful, slightly messy lines."
    aya "I call it 'Sunday Hoodie.' I have been working on it for months."
    aya "I do not know if it is good. I do not know if anyone would wear it. But it is mine."

    menu:
        "Can I see more?" :
            mc "Can I see more? The other designs?"
            aya "Sure. But fair warning, some of them are bad. I am still learning."
            aya "But I am learning. That is the difference."
            $ reward_attributes_once("aya_visit_06_see", [("insight", "micro")], show="auto")
        "You should show someone." :
            mc "You should show someone. A teacher, a designer, anyone who knows clothes."
            aya "Maybe. But first I need to show myself that I can finish something."
            aya "One step at a time. That is what I keep telling myself."
            $ reward_attributes_once("aya_visit_06_show", [("nerve", "micro")], show="auto")
        "It is already good." :
            mc "It is already good. The cat is very good."
            aya "…You are too kind. But thank you. I will remember that."
            $ reward_attributes_once("aya_visit_06_good", [("grace", "micro")], show="auto")

    "She closes the sketchbook and puts it back in her pocket, but she does not put the apron back on."
    "For a moment, she is just Aya. Not the maid. Not the character. Just Aya."
    aya "You know, I used to think I had to choose. Between this job and my dreams. Between being safe and being brave."
    aya "But talking to you, I realize I do not have to choose. I can do both. I can serve parfaits and sing. I can wear the apron and draw hoodies."
    aya "I can be both things at once."

    menu:
        "You already are both." :
            mc "You already are both. You just needed someone to tell you that."
            aya "Maybe. Or maybe I just needed to hear it from someone who was not my mother."
            $ reward_attributes_once("aya_visit_06_both", [("grace", "micro")], show="auto")
        "That is the bravest thing." :
            mc "That is the bravest thing I have heard all week."
            aya "Brave? I am just… tired of pretending there is only one version of me."
            $ reward_attributes_once("aya_visit_06_brave", [("nerve", "micro")], show="auto")

    "She stands up and smooths her apron, but this time it looks less like a costume and more like a uniform she chose."
    aya "I have to go. I have tables to clear and smiles to perform. But… thank you. For being here. For asking questions. For seeing me."
    mc "I will see you next time."
    aya "I will be here. But I will not be the same. I am becoming someone new."

    $ aya_affection += 1

    $ confidant_visits["aya"] = max(confidant_visits.get("aya", 0), 6)
    $ remember("aya", "she auditioned for a singing contest and showed him her streetwear sketchbook")
    $ queue_message("aya", "I did it. I sang. I was terrified and I did it anyway. You were right— I am allowed to want things.", day="yesterday")
    $ reward_attributes_once("aya_visit_06_close", [("insight", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 2.0
    return

label aya_visit_07:
    call aya_common_open

    "The cafe is quieter than usual. Fewer customers, softer music, the kind of afternoon that feels like it is already saying goodbye."
    "Aya is there, but she does not do the usual bright welcome. She just looks at me, and her eyes are sad in a way that has nothing to do with tiredness."

    aya "Master… I need to tell you something."
    "She says it before I sit down, and her voice is softer than I have ever heard it."
    aya "This might be the last time you see me here. I am leaving."

    "The words hang in the air, and the cafe noise fades into background."
    "I sit down slowly, and she sits across from me, not in the staff chair but in the guest chair. Like we are both customers now."

    menu:
        "Leaving the cafe?" :
            mc "Leaving the cafe?"
            aya "Yes. I have decided to chase it. My dream. Designing clothes. I do not know if I will succeed, but… staying here forever would be safe, and I do not want to be safe anymore."
            $ reward_attributes_once("aya_visit_07_leaving", [("insight", "micro")], show="auto")
        "What happened?" :
            mc "What happened? Did something change?"
            aya "I did. I auditioned. I sang. I showed someone my sketches. And they said… maybe. Maybe I could do this."
            aya "Maybe is enough. Maybe is more than I have ever had."
            $ reward_attributes_once("aya_visit_07_happened", [("nerve", "micro")], show="auto")
        "I am sorry to hear that." :
            mc "I am sorry to hear that. I will miss you."
            aya "I will miss you too. But I do not want to stay just because it is comfortable."
            $ reward_attributes_once("aya_visit_07_sorry", [("grace", "micro")], show="auto")

    "She takes a deep breath, and for a moment she looks like she is about to cry. Then she smiles, and it is the most real smile I have ever seen on her face."
    aya "When you first came in, I thought you were just another customer. But you kept coming back. You listened. You let me be myself when I was not even sure I could."
    "Her voice shakes a little, but she keeps going."
    aya "You gave me courage. Just by being here. Just by asking questions. Just by seeing me."
    aya "That is something I will never forget."

    menu:
        "I am proud of you." :
            mc "I am proud of you."
            aya "Thank you. Really. I do not know if I would have done this without you."
            $ reward_attributes_once("aya_visit_07_proud", [("grace", "micro")], show="auto")
        "You made me braver too." :
            mc "You made me braver too. We are even."
            aya "…We are? I did not know I could do that."
            aya "But maybe we can. Maybe we both got a little braver because of each other."
            $ reward_attributes_once("aya_visit_07_braver", [("nerve", "micro")], show="auto")
        "I will miss this place." :
            mc "I will miss this place. And I will miss you."
            aya "I will miss you too. But I do not want to stay just because it is familiar."
            $ reward_attributes_once("aya_visit_07_miss", [("grace", "micro")], show="auto")

    "She reaches into her pocket and pulls out the sketchbook again. She turns to a page I have not seen before, and holds it out to me."
    "It is a drawing of a cat in a streetwear hoodie, the same cat from her sketchbook but now wearing something she designed."
    aya "This is for you. I drew it last night. It is my way of saying thank you."
    aya "Wear it when you make it big. Or when you just need to feel brave."

    menu:
        "I will treasure it." :
            mc "I will treasure it. Thank you."
            aya "You are welcome. It is yours now."
            $ reward_attributes_once("aya_visit_07_treasure", [("grace", "micro")], show="auto")
        "This is perfect." :
            mc "This is perfect. I do not know what to say."
            aya "You do not have to say anything. Just remember me."
            $ reward_attributes_once("aya_visit_07_perfect", [("nerve", "micro")], show="auto")

    "She stands up, and for the first time, she does not do the maid bow. She just… bows. Like a person, not a character."
    aya "Ah, one more thing. I should finally introduce myself properly, should not I?"
    aya "My name is Shiori."
    "She looks at me, and her eyes are bright and sad and full of hope all at once."
    shiori "Thank you for everything. Maybe… someday, somewhere, we will meet again."

    "I take the sketchbook page carefully, and it feels heavier than it should."
    mc "Shiori. I will remember that."
    shiori "I know you will. You are good at remembering things."

    "She turns and walks back to the kitchen, and I realize she is not coming back."
    "The cafe is still there. The music is still there. The other maids are still there."
    "But Aya is gone. And I am left with a drawing of a cat in a hoodie, and a name I will not forget."

    $ aya_affection += 1

    $ confidant_visits["aya"] = max(confidant_visits.get("aya", 0), 7)
    $ remember("aya", "she left the cafe to pursue her dream and revealed her real name is Shiori")
    $ wire_contacts["aya"]["name"] = "Shiori"
    $ queue_message("aya", "It is Shiori now. Same phone, different name. I am going to miss this place, but I am not going to miss who I was here. Thank you for everything.", day="yesterday")
    $ reward_attributes_once("aya_visit_07_close", [("nerve", "micro")], show="card")

    scene bg_home_exterior_night with walk_fade
    stop music fadeout 3.0
    return
