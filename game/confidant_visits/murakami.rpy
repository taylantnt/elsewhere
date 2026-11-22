################################################################################
## MURAKAMI: THE ELECTIVE THAT REFUSES TO END
################################################################################
##
## The Japanese elective is not a lesson, it is a room. Twelve students from
## twelve countries, one teacher who has been doing this for twenty years and
## still finds it funny, and one protagonist who keeps showing up because the
## misunderstandings are better than the grammar.
##
## The embedded lessons already happened on Days 10-17 (the elective fair,
## Jimbocho, the old city, sound words). This file is the hub arc: office
## hours and extra sessions after those days, counted by `confidant_visits`.
##
## This arc does not end. Ten written visits, then `murakami_lesson_repeat`
## keeps the room open forever. The comedy is the point, but the warmth is
## real: a teacher who keeps showing up, and students who keep getting it
## wrong in the same loving way.
##
## The recurring cast:
##   Wei      - China. Reads kanji, cannot read kana. Certain he understands.
##   Priya    - India. Asks the questions nobody else thinks to ask.
##   Oliver   - England. Treats every custom like a puzzle with a punchline.
##   Prakash  - Nepal. Quiet until he is not. Then devastating.
##   Saman    - Sri Lanka. Studies anime Japanese. Speaks like a documentary.

# Defined late so type_sound (script.rpy) already exists when this runs.
init 999 python:
    wei = Character("Wei", color="#d8b06a", callback=type_sound, image="wei")
    priya = Character("Priya", color="#c9a0dc", callback=type_sound, image="priya")
    oliver = Character("Oliver", color="#a8c0d8", callback=type_sound, image="oliver")
    prakash = Character("Prakash", color="#b8a888", callback=type_sound, image="prakash")
    saman = Character("Saman", color="#98b8a8", callback=type_sound, image="saman")
    # The five recurring students above now have portraits (image= tags matching
    # the `image side` declarations in script.rpy). This generic, non-recurring
    # exchange student is deliberately left faceless and nameless: a face for
    # somebody who only passes through the room once would be a lie.
    exchange_student = Character("Student", color="#9aa4ad", callback=type_sound)

label confidant_visit_murakami:
    $ visit = confidant_visits.get("murakami", 0)
    if visit == 0:
        jump murakami_visit_01
    elif visit == 1:
        jump murakami_visit_02
    elif visit == 2:
        jump murakami_visit_03
    elif visit == 3:
        jump murakami_visit_04
    elif visit == 4:
        jump murakami_visit_05
    elif visit == 5:
        jump murakami_visit_06
    elif visit == 6:
        jump murakami_visit_07
    elif visit == 7:
        jump murakami_visit_08
    elif visit == 8:
        jump murakami_visit_09
    elif visit == 9:
        jump murakami_visit_10
    else:
        jump murakami_lesson_repeat
    return

label murakami_common_open:
    scene bg_department_hall with walk_fade
    "The small room on the second floor. Twelve desks, a whiteboard, and a window that looks out at a wall."
    "It is the least impressive classroom in the building, which is exactly why they love it."
    return

################################################################################
## VISIT 1: THE WRONG ANSWER
################################################################################

label murakami_visit_01:
    call murakami_common_open from _call_murakami_common_open

    "Office hours. The sign on the door says MURAKAMI, OFFICE HOURS, and underneath, in smaller letters: BRING A QUESTION YOU CANNOT ANSWER."
    "I have a question I cannot answer. It is why I am here."

    murakami "Ah. The foreign student. The one who keeps coming back."
    mc "You remembered me."
    murakami "I remember everyone who comes back. It is a small class. I have to."
    "She is already writing on the board before I sit down. Not scolding. Just... preparing."

    murakami "Today we review. Yesterday's homework. The particles. You all know the particles."
    "Twelve heads nod. The nodding is synchronized, which is either impressive or ominous."
    murakami "Priya, read me your answer."
    priya "I wrote: 'Watashi wa sushi ga suki desu.' I am sushi."
    "A pause. The kind of pause that has weight."
    murakami "...That is not what that sentence means."
    priya "But the grammar is perfect. I checked with Wei."
    wei "The kanji are correct. I checked them twice."
    murakami "The kanji are correct. The sentence is a disaster. You have built a grammatically perfect sentence that means nothing."
    oliver "Is that even possible?"
    murakami "It is the most common kind of possible. Grammar is the skeleton. Meaning is the person inside. You have been studying skeletons."
    mc "(She says it gently. But 'you have been studying skeletons' lands like a diagnosis.)"

    murakami "Let us try again. Together. 'Watashi wa sushi ga suki desu.' Say it."
    "The room repeats it. Twelve voices, one sentence, slightly different accents, all wrong in the same way."
    murakami "Good. Now, who can tell me what it means?"
    "Silence. The silence has texture. Wei is reading the kanji on the board like they are a legal document."
    wei "I... am... liked by sushi?"
    murakami "Close enough to be dangerous. Sit down, Wei."
    "She erases the board. The sentence is gone. The lesson is not."

    menu:
        "Ask what 'skeletons' means." :
            mc "You said we have been studying skeletons. What does that mean?"
            murakami "It means you know the shape of the language. The bones. But the bones do not tell you what the body is doing."
            mc "So I am a skeleton?"
            murakami "You are a very polite skeleton. Sit down."
            $ reward_attributes_once("murakami_v01_skeleton", [("insight", "micro")], show="auto")
        "Ask if everyone gets it wrong the same way." :
            mc "Do they all misunderstand the same way?"
            murakami "Yes. That is the terrifying thing. They are all wrong in the same direction, like a flock of birds flying into the same window."
            murakami "It is not their fault. It is the language's fault. Japanese is very good at looking like it means one thing and meaning another."
            $ reward_attributes_once("murakami_v01_same", [("grace", "micro")], show="auto")
        "Ask if she has seen worse." :
            mc "Have you had worse students?"
            murakami "I have had students who wrote essays in Japanese that were entirely in English with Japanese particles stuck on."
            murakami "You are not worse. You are just... early. Sit down and learn from their skeletons."
            $ reward_attributes_once("murakami_v01_worse", [("nerve", "micro")], show="auto")

    "I sit in the back. The room smells like chalk and old paper and twelve people who are all a little lost and a little hopeful."
    "Murakami is already explaining something else. The board is filling up again. The wrong answers are being corrected one by one."
    "It is the most honest classroom I have ever been in. Nobody is pretending to understand. They are just trying."

    $ confidant_visits["murakami"] = max(confidant_visits.get("murakami", 0), 1)
    $ murakami_lessons = max(murakami_lessons, 1)
    $ japanese_fluency = min(5, japanese_fluency + 1)
    $ log_memory("murakami", "first office hours; the whole class got the same sentence wrong in the same way")
    $ reward_attributes_once("murakami_v01_close", [("grace", "micro")], show="auto")
    return

################################################################################
## VISIT 2: THE KANJI TRAP
################################################################################

label murakami_visit_02:
    call murakami_common_open from _call_murakami_common_open_1

    "The kanji lesson. Murakami writes a character on the board and the room goes quiet, which is its own kind of applause."
    "It is a complex one. Too many strokes. It looks like it is trying to be three characters at once."

    murakami "This is 'yūjō'. {jp}友情{/jp} Friendship. The radical on the left is 'person.' The part on the right is... 'have.' Person-have. Friendship."
    wei "I know this one."
    murakami "You know it?"
    wei "My grandmother taught me. The kanji for friendship. I can write it."
    "He comes to the board and writes it from memory. It is beautiful. Perfect strokes. The kind of kanji that makes teachers cry."
    murakami "...That is correct."
    wei "I told you. My grandmother."
    murakami "Yes. I believe you. Now, can you read it? Not write it. Read it."
    "Wei looks at the character. The confidence drains out of his face like water from a bath."
    wei "...I can see the person radical. I can see the 'have.' But I cannot... read it as a word."
    murakami "Because it is not a word. It is a kanji. The kanji means friendship, but the word for friendship is 'yūjō' written in kana."
    wei "So I have been writing the right character for the wrong reason?"
    murakami "You have been writing a beautiful character that you cannot pronounce. It is the most honest mistake I have ever seen."
    "The room laughs. Wei laughs too, which is the first time I have heard him laugh."
    priya "So kanji is like a trap?"
    murakami "Kanji is like a library where every book is also a person. You can recognize the person but you cannot read the book."
    oliver "That is the most romantic description of illiteracy I have ever heard."
    murakami "It is not illiteracy. It is a different kind of literacy. Wei can read a thousand years of Chinese literature. He just cannot read a menu."
    mc "(The kanji are not a shortcut. They are a different road. Wei has been driving on the wrong one, beautifully.)"
    if japanese_fluency >= 4:
        "I copy 'yūjō' onto a sticky note of my own. The kanji is still a mystery. The kana I can almost read. For the first time the two are starting to be the same word."

    menu:
        "Ask Wei what his grandmother taught him." :
            mc "What else did your grandmother teach you?"
            wei "She taught me the kanji for 'home.' And 'food.' And 'not dead.'"
            priya "'Not dead'?"
            wei "The kanji for 'alive.' It looks like a person with a pulse mark. My grandmother said it is the most important character to know."
            murakami "She was right. It is. Sit down, Wei. You have taught us all more than the board has."
            $ reward_attributes_once("murakami_v02_grandmother", [("grace", "micro")], show="auto")
        "Ask if kanji helps or hurts." :
            mc "Does knowing kanji help or hurt?"
            murakami "Both. It gives you a head start on vocabulary and a handicap on pronunciation. You think you know a word because you know the character, but the character is not the word."
            murakami "It is like knowing the lyrics to a song you have never heard. You can sing along but you do not know the melody."
            $ reward_attributes_once("murakami_v02_kanji", [("insight", "micro")], show="auto")
        "Ask if she can read kanji." :
            mc "Can you read kanji?"
            murakami "I can read some. I can write more. I can recognize the ones that matter: 'stop,' 'exit,' 'danger,' 'bath.'"
            murakami "The rest I have to look up. I am not a kanji master. I am a teacher who happens to be Japanese. There is a difference."
            $ reward_attributes_once("murakami_v02_read", [("nerve", "micro")], show="auto")

    "The lesson ends with Wei writing 'friendship' on a sticky note and putting it on his bag. He does not know how to pronounce it. He does not care."
    "That is the thing about kanji. It is a language you can carry without speaking."

    $ confidant_visits["murakami"] = max(confidant_visits.get("murakami", 0), 2)
    $ murakami_lessons = max(murakami_lessons, 2)
    $ japanese_fluency = min(5, japanese_fluency + 1)
    $ log_memory("murakami", "the kanji lesson; Wei wrote friendship perfectly but could not read it")
    $ reward_attributes_once("murakami_v02_close", [("grace", "micro")], show="auto")
    return

################################################################################
## VISIT 3: THE BOWING PROBLEM
################################################################################

label murakami_visit_03:
    call murakami_common_open from _call_murakami_common_open_2

    "The keigo lesson. Murakami stands at the front of the room and demonstrates a bow so deep it looks like she is bowing to the floor."
    "Then she straightens and does it again, shallower. Then again, shallowest."

    murakami "Three bows. Deep, medium, shallow. The depth tells the listener how much respect you are giving."
    oliver "Is this... a dance?"
    murakami "It is not a dance. It is grammar. The body is the punctuation."
    oliver "Right. Grammar. Punctuation. Body."
    "He tries it. The bow is too deep. He nearly falls over. The room erupts."
    murakami "Oliver, the bow is not a fall. It is a greeting. You are greeting the floor, not the person."
    oliver "I was trying to greet the floor. I respect floors."
    "Wei tries next. He bows with his whole body, hands pressed together like a karate student. It is technically correct and completely wrong."
    murakami "Wei, the hands are for holding things, not for praying. Unless you are praying. Are you praying?"
    wei "I am showing respect."
    murakami "You are showing respect to the concept of respect. Sit down."

    "Then it is my turn. Murakami looks at me and waits."
    murakami "You. The foreign student. Bow."
    "I bow. Medium depth. Not too deep, not too shallow. The kind of bow that says 'I have been here long enough to know the difference.'"
    murakami "...Better. Still too formal. You are bowing like a tourist."
    mc "What does a resident bow like?"
    murakami "A resident bows like they are too tired to bow properly but they do it anyway because it is the right thing."
    "I bow again. This time it is smaller. Almost a nod."
    murakami "Yes. That is it. You are learning."

    menu:
        "Ask what happens if you bow wrong." :
            mc "What happens if you bow too deep or too shallow?"
            murakami "Too deep and you look like you are apologizing for existing. Too shallow and you look like you do not care. The middle is respect. The edges are accidents."
            murakami "But most people will forgive you. The bow is not a test. It is a greeting. Greetings can be retried."
            $ reward_attributes_once("murakami_v03_bow", [("grace", "micro")], show="auto")
        "Ask why the body matters." :
            mc "Why does the body matter? Why not just say the words?"
            murakami "Because the words are only half the message. The other half is in the angle of your shoulders, the depth of your bow, the timing of your breath."
            murakami "Japanese is a language you say with your whole body. The words are just the part you can write down."
            $ reward_attributes_once("murakami_v03_body", [("insight", "micro")], show="auto")
        "Ask if she bows to students." :
            mc "Do you bow to us?"
            murakami "I bow to the room. The room contains you. If I bowed to each of you individually we would be here until dinner."
            murakami "But I do nod at you when you answer correctly. That is my version of a bow. It is smaller. It is also more sincere."
            $ reward_attributes_once("murakami_v03_bow_back", [("nerve", "micro")], show="auto")

    "The lesson ends with everyone practicing bows in pairs. Wei and Priya are bowing at each other like two samurai who have never met."
    "Oliver is bowing to the wall. Prakash is bowing so shallowly it looks like he is leaning."
    "Saman is not bowing at all. He is taking notes."
    "It is the most ridiculous and most honest thing I have ever seen."

    $ confidant_visits["murakami"] = max(confidant_visits.get("murakami", 0), 3)
    $ murakami_lessons = max(murakami_lessons, 3)
    $ japanese_fluency = min(5, japanese_fluency + 1)
    $ log_memory("murakami", "the bowing lesson; everyone bowed wrong except me, barely")
    $ reward_attributes_once("murakami_v03_close", [("grace", "micro")], show="auto")
    return

################################################################################
## VISIT 4: THE TRICK QUESTION
################################################################################

label murakami_visit_04:
    call murakami_common_open from _call_murakami_common_open_3

    "The quiz. Murakami hands out a single sheet of paper and the room goes quiet in the way rooms go quiet when they are about to be tested."
    "The quiz is one question. Just one. It is short. It looks easy."

    murakami "Read it. Do not write yet. Read it twice."
    "The question is: 'How many animals are in the room?'"
    "Twelve heads look up. Look around. Look at the walls. Look at the ceiling."
    priya "There are none."
    murakami "Are you sure?"
    priya "There are no animals. This is a classroom."
    murakami "Look again."
    "I look again. The room has desks, chairs, a whiteboard, a window, a radiator, and twelve students who are all very confused."
    oliver "Wait. Is it a trick?"
    murakami "It is always a trick. That is the point of a quiz."
    "Wei is counting the kanji on the board. Prakash is counting the exits. Saman is counting the students."
    murakami "Time. Write your answers."
    "The papers fill with answers. I write: 'None.' It is the obvious answer. It is probably wrong."

    murakami "Papers up. Let us see."
    "She reads them. Her face does something complicated, like she is trying not to laugh and failing."
    murakami "Priya: 'None.' Wei: 'Twelve.' Oliver: 'Zero.' Prakash: 'Three.' Saman: 'One.'"
    murakami "And you?"
    mc "I wrote 'none.'"
    murakami "You wrote 'none.' That is... interesting."
    murakami "The correct answer is twelve."
    "A pause. The kind of pause that makes twelve brains do twelve different kinds of math."
    murakami "Twelve animals. Twelve students. Each of you is an animal. The question was not about the room. It was about the people in it."
    priya "So we are the animals?"
    murakami "You are the animals. The room is just where the animals sit."
    oliver "That is the most Japanese thing I have ever heard."
    murakami "It is also the most honest. Sit down. You all failed. But you failed interestingly."

    menu:
        "Ask if she does this often." :
            mc "Do you do this often? Trick questions?"
            murakami "Once a week. The students hate it. I love it. It is the only way to see if they are actually thinking or just memorizing."
            murakami "A trick question is a mirror. It shows you what the student thinks the question is really asking. Most of them think it is asking about grammar. It is asking about attention."
            $ reward_attributes_once("murakami_v04_trick", [("insight", "micro")], show="auto")
        "Ask what she would have answered." :
            mc "What would you have answered?"
            murakami "I would have answered 'twelve.' I have been doing this long enough to know the trick. But I would have been wrong."
            murakami "The trick is not that you do not know the answer. The trick is that you think you know what kind of question it is."
            $ reward_attributes_once("murakami_v04_would", [("grace", "micro")], show="auto")
        "Ask if the animals know they are animals." :
            mc "Do the animals know they are animals?"
            murakami "That is the best question anyone has asked all week. The answer is: some do, some do not, and the ones who do not are the most interesting."
            murakami "Sit down. You have just described every student in this room. Including yourself."
            $ reward_attributes_once("murakami_v04_animals", [("nerve", "micro")], show="auto")

    "The quiz papers are collected. The room is still buzzing with the wrong answers, turning them over like stones looking for something underneath."
    "I keep mine. It says 'NONE' in my handwriting, underlined twice, like a small act of rebellion."

    $ confidant_visits["murakami"] = max(confidant_visits.get("murakami", 0), 4)
    $ murakami_lessons = max(murakami_lessons, 4)
    $ japanese_fluency = min(5, japanese_fluency + 1)
    $ log_memory("murakami", "the trick question quiz; the answer was twelve, and we were all the animals")
    $ reward_attributes_once("murakami_v04_close", [("insight", "micro")], show="auto")
    return

################################################################################
## VISIT 5: THE LANGUAGE EXCHANGE
################################################################################

label murakami_visit_05:
    call murakami_common_open from _call_murakami_common_open_4

    "Not a lesson. Murakami has pushed the desks into a circle and there is a bag of snacks on the table that she clearly did not buy herself."
    "Language exchange day. The students teach him their languages. He teaches them his. It is chaos with a syllabus."

    murakami "Today we are not learning Japanese. We are learning each other. Wei, you start. Teach us one Chinese word."
    wei "Um. 'Ni hao.' Hello."
    murakami "Ni hao. Easy. Now, can you teach us a harder one? Something that means something."
    wei "'Xie xie.' Thank you. But also... 'bu keqi.' You are welcome. But literally it means 'not worthy of your politeness.'"
    murakami "Bu keqi. Say it."
    "The room repeats it. It sounds like a sneeze."
    oliver "That sounds like a sneeze."
    wei "It does. But it means something very polite. Chinese has many words for politeness. It is exhausting."
    murakami "Now you. Oliver. One English word."
    oliver "'Serendipity.'"
    "Silence. The kind of silence that means 'I do not know that word but I am too embarrassed to ask.'"
    murakami "Serendipity. Write it down. It means finding something good without looking for it."
    oliver "That is... a nice word."
    murakami "It is. Now, who wants to teach me a word from their language?"
    "Prakash raises his hand. Slowly. Like he is not sure he is allowed."
    prakash "Nepali. 'Namaste.'"
    murakami "Namaste. I know that one. It means 'I bow to you.' It is the same as the bow we practiced, but in words."
    prakash "Yes. It is both."
    murakami "Saman?"
    saman "Sinhala. 'Ayubowan.' It means 'may you live long.'"
    murakami "Ayubowan. That is... a lot to ask of a greeting."
    saman "It is. But it is also true. We greet each other with a wish, not just a hello."
    "The room is quiet. The snacks are being passed around. The language exchange is working, sort of."

    menu:
        "Ask Murakami what word she would teach." :
            mc "What word would you teach us?"
            murakami "I would teach you 'ikigai.' The reason you get up in the morning. It is not a word for 'happiness.' It is a word for 'the thing that makes the day worth having.'"
            murakami "I teach it because I see it in this room. You are all here for a reason. The reason is not the grade. It is the reason."
            $ reward_attributes_once("murakami_v05_ikigai", [("insight", "micro")], show="auto")
        "Ask Wei to teach a harder Chinese word." :
            mc "Wei, teach us a harder one. Something that does not sound like a sneeze."
            wei "'Yīngxióng.' Hero. But also... 'yīngxióng zhǔyì.' Heroism. It is the thing that makes you do something brave when you are afraid."
            murakami "Yīngxióng. Write it down. It is a good word."
            wei "It is. My grandmother used to say it when she was proud of me. It is the word for 'I see you being brave.'"
            $ reward_attributes_once("murakami_v05_wei", [("grace", "micro")], show="auto")
        "Ask Oliver to teach a harder English word." :
            mc "Oliver, teach us a harder English word. Something that is not 'serendipity.'"
            oliver "'Kaleidoscope.'"
            murakami "Kaleidoscope. Write it down."
            oliver "It is a tube with mirrors and colored glass. You turn it and the pattern changes. It is beautiful and it never repeats."
            murakami "That is a good word. It is also a good metaphor for this class. We turn it and the pattern changes every time."
            $ reward_attributes_once("murakami_v05_oliver", [("nerve", "micro")], show="auto")

    "The lesson ends with everyone teaching each other words and laughing at the ones that sound like sneezes or animals."
    "Murakami is writing words on the board in five different scripts. The board is full. The room is full. The snacks are almost gone."
    "It is the most alive the room has ever felt."

    $ confidant_visits["murakami"] = max(confidant_visits.get("murakami", 0), 5)
    $ murakami_lessons = max(murakami_lessons, 5)
    $ japanese_fluency = min(5, japanese_fluency + 1)
    $ log_memory("murakami", "the language exchange; we taught each other words and it was the most alive the room has felt")
    $ reward_attributes_once("murakami_v05_close", [("grace", "micro")], show="auto")
    return

################################################################################
## VISIT 6: HER JAPANESE BREAKS
################################################################################

label murakami_visit_06:
    call murakami_common_open from _call_murakami_common_open_5

    "Murakami is telling a story. Not a lesson. A story. She is standing in front of the room with her hands moving like she is conducting an orchestra of small disasters."
    "It is a pun. A Japanese pun. The kind that only works if you have been inside the language for twenty years."

    murakami "So the student says to the teacher: 'Why did the chicken cross the playground?'"
    "A pause. The room waits."
    murakami "And the teacher says: 'To get to the other slide.'"
    "Silence. Total silence. The kind of silence that has weight."
    "Wei is looking at the kanji on the board. Priya is looking at Oliver. Oliver is looking at the floor."
    murakami "...It is a pun. 'Playground' and 'slide' sound like 'class' and 'lesson' if you say them fast enough."
    priya "I do not understand."
    murakami "You are not supposed to understand. That is the point. It is a joke that only Japanese people get."
    oliver "That is the worst joke I have ever heard."
    murakami "It is not a joke. It is a test. If you get it, you are fluent. If you do not, you are still learning."
    "Prakash raises his hand. Slowly."
    prakash "I think I get it. 'Playground' is 'asobi-ba.' 'Slide' is 'suberu.' They do not sound alike."
    murakami "They do if you say them fast and do not think about it. Language is not logic. It is music."
    prakash "So the joke is that the chicken was trying to get to the other lesson?"
    murakami "...Yes. That is exactly it. You have just understood a pun that took me twenty years to learn."
    "Prakash smiles. It is the first time I have seen him smile."
    murakami "You see? This is why I teach. Not for the grammar. For the moments when someone gets it."
    "The room is quiet. The pun is still hanging in the air, not quite landing, not quite missing."

    menu:
        "Ask if she tells jokes often." :
            mc "Do you tell jokes often?"
            murakami "Every day. Japanese is full of them. They are called 'dajare' and they are terrible. That is why they work."
            murakami "A good pun is a door that only opens if you are already inside. You have to be fluent enough to be inside before you can get the joke."
            $ reward_attributes_once("murakami_v06_jokes", [("insight", "micro")], show="auto")
        "Ask if she has told that joke before." :
            mc "Have you told that joke before?"
            murakami "Every year. The students always laugh at the wrong part. It is my favorite tradition."
            murakami "This year, Prakash got it. That has never happened before. You have made my year."
            $ reward_attributes_once("murakami_v06_tradition", [("grace", "micro")], show="auto")
        "Ask what other puns she knows." :
            mc "What other puns do you know?"
            murakami "I know one about a samurai and a pencil. I know one about a frog and a staircase. I know one about a student who asked why the bus was late and the teacher said because it was stuck in traffic."
            murakami "They are all terrible. They are all perfect. That is the thing about puns. They are terrible and perfect at the same time."
            $ reward_attributes_once("murakami_v06_puns", [("nerve", "micro")], show="auto")

    "The lesson ends with Murakami writing 'dajare' on the board and underlining it twice."
    murakami "Dajare. {jp}駄洒落{/jp}. It means 'pun.' It also means 'the sound of a door opening.' It is the most important word in Japanese."
    "I do not know if that is true. But I believe her."

    $ confidant_visits["murakami"] = max(confidant_visits.get("murakami", 0), 6)
    $ murakami_lessons = max(murakami_lessons, 6)
    $ japanese_fluency = min(5, japanese_fluency + 1)
    $ log_memory("murakami", "she told a pun only Japanese get and Prakash understood it; her Japanese broke for a moment")
    $ reward_attributes_once("murakami_v06_close", [("grace", "micro")], show="auto")
    return

################################################################################
## VISIT 7: THE QUIET STUDENT
################################################################################

label murakami_visit_07:
    call murakami_common_open from _call_murakami_common_open_6

    "Saman has been quiet for weeks. Not shy quiet. Studying quiet. The kind of quiet that is actually listening."
    "Today he raises his hand. Murakami calls on him. The room goes still."

    murakami "Saman. What is your question?"
    saman "Why did you become a teacher?"
    "The question hangs in the air. It is not a grammar question. It is not a vocabulary question. It is a question about a person."
    "The room is very quiet. Even Wei is not reading kanji."
    murakami "...That is a good question."
    saman "I have been wondering. You teach us Japanese. But you are not Japanese. You are from..."
    murakami "I am from Osaka. I have been teaching Japanese to foreigners for twenty years. I started because I wanted to understand why people come here."
    saman "And did you?"
    murakami "...Yes. I think I did. The students are not here for the language. They are here for the reason. The language is just the vehicle."
    "Saman nods. He writes something in his notebook. It is not vocabulary. It is a sentence."
    saman "I came to Japan because of anime. I wanted to understand the words. But I stayed because of the people. The teacher who stays after class. The student who helps another student. The room that smells like chalk and old paper."
    saman "That is why I am here. Not for the language. For the room."
    "The room is very quiet. The kind of quiet that is almost a hug."
    murakami "...That is the best answer anyone has given me."
    "She does not say it loudly. She says it the way you say something you mean."
    "Prakash is looking at Saman. Wei is looking at the board. Oliver is looking at his hands. Priya is looking at Murakami."
    "We are all looking at the room."

    menu:
        "Ask Saman if he will stay." :
            mc "Will you stay? After the course?"
            saman "I do not know. I want to. But I also want to go home and tell my family that I survived."
            saman "But I will come back. I think. The room is not finished with me. I am not finished with the room."
            $ reward_attributes_once("murakami_v07_saman", [("grace", "micro")], show="auto")
        "Ask Murakami if she gets asked that often." :
            mc "Do you get asked that often?"
            murakami "Once a year. Usually by a student who has been here long enough to see past the grammar."
            murakami "It is always the best question. It is always the hardest to answer."
            $ reward_attributes_once("murakami_v07_asked", [("insight", "micro")], show="auto")
        "Ask what the room smells like to her." :
            mc "What does the room smell like to you?"
            murakami "Chalk. Old paper. And twenty years of students who thought they were bad at Japanese."
            murakami "It smells like hope. It smells like the moment before someone understands something for the first time."
            $ reward_attributes_once("murakami_v07_smell", [("nerve", "micro")], show="auto")

    "The lesson ends with Saman writing his sentence on the board. It is not vocabulary. It is not grammar. It is a sentence about why he is here."
    "Murakami leaves it there. She does not erase it."
    "Some sentences should not be erased."

    $ confidant_visits["murakami"] = max(confidant_visits.get("murakami", 0), 7)
    $ murakami_lessons = max(murakami_lessons, 7)
    $ japanese_fluency = min(5, japanese_fluency + 1)
    $ log_memory("murakami", "Saman asked why she teaches and said he stayed for the room, not the language")
    $ reward_attributes_once("murakami_v07_close", [("grace", "micro")], show="auto")
    return

################################################################################
## VISIT 8: THE FOOD DAY
################################################################################

label murakami_visit_08:
    call murakami_common_open from _call_murakami_common_open_7

    "Food day. The desks are pushed to the walls and the table in the middle is covered with containers and bags and the kind of chaos that only happens when twelve people bring food to share."
    "Murakami has made tea. The students have brought everything else."

    murakami "Today we eat. No grammar. No vocabulary. Just food and talking."
    wei "I brought dumplings. From the shop near my apartment. They are not as good as my grandmother's but they are good."
    priya "I brought samosas. My mother made them. She said to tell you they are for the teacher."
    murakami "Tell your mother thank you. And tell her I am honored."
    oliver "I brought... a sandwich. From a shop. It is not special. It is just a sandwich."
    murakami "Oliver, a sandwich is a perfectly good thing to bring. Do not apologize for it."
    prakash "I brought rice. Plain rice. I did not know what else to bring."
    murakami "Plain rice is perfect. It goes with everything."
    saman "I brought... tea. From Sri Lanka. It is called 'Ceylon.' It is very strong."
    murakami "Ceylon tea. I know it. It is good. Thank you."
    "I brought onigiri. Two of them. Salmon and tuna. I made them last night. They are not perfect. The rice is a little too sticky. But they are mine."
    "I put them on the table. Wei picks one up and looks at it."
    wei "This is... nice."
    murakami "It is more than nice. It is the first thing you have brought that is not from a shop."
    "The room is quiet. The food is being passed around. The tea is being poured. The talking is in five languages and one that is mostly gestures."
    "It is the most human thing that has happened in this room."

    menu:
        "Ask Murakami what her favorite food is." :
            mc "What is your favorite food?"
            murakami "Osaka-style takoyaki. Octopus balls. They are small and they are perfect."
            murakami "But I do not make them. I buy them. I am a teacher, not a chef. I leave the cooking to people who are better at it."
            $ reward_attributes_once("murakami_v08_food", [("grace", "micro")], show="auto")
        "Ask Wei what his grandmother's dumplings taste like." :
            mc "Wei, what do your grandmother's dumplings taste like?"
            wei "They taste like... home. Like the kitchen in my grandmother's house. Like the sound of her chopping vegetables."
            wei "I cannot describe it in Japanese or English. It is just... home."
            murakami "That is what food is. It is the thing that tastes like home even when you are far away."
            $ reward_attributes_once("murakami_v08_wei", [("insight", "micro")], show="auto")
        "Ask Oliver if he will bring food next time." :
            mc "Oliver, will you bring food next time?"
            oliver "I will try. I am not good at cooking. But I can buy things. I can bring things that are good."
            murakami "That is enough. The bringing is the point. The cooking is a bonus."
            $ reward_attributes_once("murakami_v08_oliver", [("nerve", "micro")], show="auto")

    "The food day ends with everyone full and everyone a little slower. The room smells like dumplings and samosas and Ceylon tea and onigiri."
    "Murakami writes 'food day' on the board and underlines it twice."
    "It is the best lesson she has ever taught."

    $ confidant_visits["murakami"] = max(confidant_visits.get("murakami", 0), 8)
    $ murakami_lessons = max(murakami_lessons, 8)
    $ japanese_fluency = min(5, japanese_fluency + 1)
    $ log_memory("murakami", "food day; we brought dishes and the room smelled like home")
    $ reward_attributes_once("murakami_v08_close", [("grace", "micro")], show="auto")
    return

################################################################################
## VISIT 9: THE SKIT
################################################################################

label murakami_visit_09:
    call murakami_common_open from _call_murakami_common_open_8

    "The skit. Murakami has written a short script on the board and the students are rehearsing it in the corner."
    "It is a skit about daily life in Japan. A student tries to buy a train ticket. A station attendant tries to help. Everything goes wrong."
    "The students have been working on it for a week. They are not ready."

    murakami "Places, everyone. The skit starts now."
    "Wei is the student. Priya is the attendant. Oliver is the narrator. Prakash is the train. Saman is the ticket machine."
    "I am... the lost tourist. I have one line. 'Sumimasen, eki wa doko desu ka?' Excuse me, where is the station?"
    "I say it. My accent is bad. My grammar is worse. But I say it with confidence, which is the most important thing."
    priya "The station is... over there?"
    "She gestures vaguely. Wei nods like he understands. Oliver reads the narration. Prakash makes a train sound. Saman beeps like a ticket machine."
    "It is terrible. It is perfect. It is the most Japanese thing that has ever happened in this room."
    "Murakami is watching from the side. She is not smiling. She is... listening. Really listening."
    "When the skit ends, the room is quiet. Then everyone laughs. Not the polite laugh. The real laugh. The kind that comes from the stomach."
    murakami "...Again."
    "They do it again. It is worse the second time. It is better the second time."
    "By the third time, Wei has ad-libbed a line in Chinese. Priya has ad-libbed a line in Hindi. Oliver has ad-libbed a line in English that is mostly 'blimey.'"
    "The skit is now a mess. It is also the best thing that has ever happened in this classroom."

    menu:
        "Ask Murakami what she thinks of the skit." :
            mc "What do you think?"
            murakami "It is terrible. It is also perfect. The grammar is wrong. The timing is wrong. The accents are wrong. But the heart is right."
            murakami "That is what I want. Not perfect Japanese. Perfect trying. The skit is not about the language. It is about the people who are trying to speak it."
            $ reward_attributes_once("murakami_v09_skit", [("insight", "micro")], show="auto")
        "Ask Wei what his ad-lib was." :
            mc "Wei, what was your ad-lib?"
            wei "I said 'Ni hao' in the middle of the skit. It did not fit. But it was the only Chinese I could remember under pressure."
            murakami "It fit perfectly. It was the only honest thing in the whole skit."
            $ reward_attributes_once("murakami_v09_wei", [("grace", "micro")], show="auto")
        "Ask Oliver what 'blimey' means." :
            mc "Oliver, what does 'blimey' mean?"
            oliver "It is an English word. It means... surprise. Or shock. Or 'oh my god.' It is very British. I cannot help it."
            murakami "It fit. Keep it. It is now part of the skit."
            $ reward_attributes_once("murakami_v09_oliver", [("nerve", "micro")], show="auto")

    "The skit ends with everyone bowing to each other, which is not in the script but is very Japanese."
    "Murakami bows back. It is the smallest bow she has ever given. It is also the biggest."

    $ confidant_visits["murakami"] = max(confidant_visits.get("murakami", 0), 9)
    $ murakami_lessons = max(murakami_lessons, 9)
    $ japanese_fluency = min(5, japanese_fluency + 1)
    $ log_memory("murakami", "the skit; we performed a train ticket scene and it was terrible and perfect")
    $ reward_attributes_once("murakami_v09_close", [("grace", "micro")], show="auto")
    return

################################################################################
## VISIT 10: THE CERTIFICATES
################################################################################

label murakami_visit_10:
    call murakami_common_open from _call_murakami_common_open_9

    "The last day of the unit. Murakami has printed certificates. Actual certificates. On real paper. With a real seal."
    "The room is quiet. The kind of quiet that happens before something important."

    murakami "Today we do not learn Japanese. Today we acknowledge what we have learned."
    "She hands out certificates. Wei gets 'Most Improved Kanji.' Priya gets 'Most Improved Grammar.' Oliver gets 'Most Improved Accent.'"
    "Prakash gets 'Most Improved Silence.' Saman gets 'Most Improved Anime.'"
    "And I get... 'Most Improved Foreigner.'"
    "The room laughs. Murakami does not. She is looking at the certificate like it is the most important thing she has ever printed."
    murakami "You are not the most improved foreigner. You are the most improved student. The 'foreigner' part is just a detail."
    mc "That is... nice."
    murakami "It is not nice. It is true. You came here not knowing which platform. Now you know the trains. You came here not knowing the particles. Now you know the particles. You came here not knowing how to bow. Now you bow like a resident."
    murakami "You are not a foreigner who is learning Japanese. You are a person who is learning to be here."
    "The room is very quiet. The certificates are being held like they are made of glass."
    murakami "The certificate says {jp}修了証書{/jp}. That is what it is called. It means 'proof of completion.' You earned it."
    murakami "The course is not over. There is more to learn. More grammar, more vocabulary, more customs. But the first part is done. You have learned the room."
    murakami "Now go and use it."

    menu:
        "Ask if she is proud of the class." :
            mc "Are you proud of the class?"
            murakami "I am proud of every single one of you. Not because you are perfect. Because you are trying. Trying is the only thing that matters."
            murakami "I have had students who were perfect and students who tried. The ones who tried are the ones I remember."
            $ reward_attributes_once("murakami_v10_proud", [("grace", "micro")], show="auto")
        "Ask what she will teach next." :
            mc "What will you teach next?"
            murakami "Next term, we do the same thing. New students, same room, same misunderstandings. The course never ends. Neither do the students."
            murakami "But you will be gone soon. You will go back to your country. You will take the room with you. That is what teachers hope for."
            $ reward_attributes_once("murakami_v10_next", [("insight", "micro")], show="auto")
        "Ask if the certificates are real." :
            mc "Are the certificates real?"
            murakami "They are as real as anything I make. I printed them myself. I stamped them myself. I signed them myself."
            murakami "They are not official. They are not recognized by any ministry. But they are real to me. And they should be real to you."
            $ reward_attributes_once("murakami_v10_real", [("nerve", "micro")], show="auto")

    "The certificates are folded and put in bags. The room is being cleaned. The chalk is being erased."
    "I tuck my certificate into my bag. Murakami's signature is still wet."
    $ add_item("murakami_certificate")
    "Murakami writes 'THE END' on the board and then erases it."
    "Because there is no end. Only the next class."

    $ confidant_visits["murakami"] = max(confidant_visits.get("murakami", 0), 10)
    $ murakami_lessons = max(murakami_lessons, 10)
    $ japanese_fluency = min(5, japanese_fluency + 1)
    $ log_memory("murakami", "the certificates; I got 'Most Improved Foreigner' and she said I am learning to be here, not just the language")
    $ reward_attributes_once("murakami_v10_close", [("grace", "micro")], show="card")
    $ queue_message("murakami", "You got your certificate. I signed it myself. Do not lose it. The course is not over, but this part is done. - Murakami", day="yesterday")
    return

################################################################################
## VISIT 11+: THE ROOM STAYS OPEN
################################################################################
##
## The arc does not end. After the ten written visits, office hours continue
## forever. The room is still there. The students are still wrong in the same
## loving way. Murakami is still writing on the board.
##
## This scene rotates through three small beats so repeat visits do not feel
## identical. The comedy is the same; the details change.

label murakami_lesson_repeat:
    $ visit = confidant_visits.get("murakami", 0)
    $ variant = visit % 3

    call murakami_common_open from _call_murakami_common_open_10

    if variant == 0:
        "Office hours again. The sign on the door still says BRING A QUESTION YOU CANNOT ANSWER."
        "I have a question I cannot answer. It is the same question as last time: why does the language keep surprising me?"
        if japanese_fluency >= 5:
            mc "Ohayou gozaimasu."
            murakami "...You said that without translating it in your head first."
            mc "I think. Maybe."
            murakami "That is what 'maybe' sounds like when it is true."
        murakami "Ah. The foreign student. Back again."
        mc "You keep saying that like it is a warning."
        murakami "It is not a warning. It is a fact. You keep coming back because the room is good."
        "She is writing on the board. Not grammar. Not vocabulary. Just words. Words that mean things."
        murakami "Today we learn 'komorebi.' The light that filters through leaves. There is no English word for it."
        priya "There is not?"
        murakami "There is not. English has 'sunlight' and 'shade' but not 'the light that comes through leaves.' Japanese has it because Japanese people noticed it."
        oliver "That is... nice."
        murakami "It is more than nice. It is proof that the language is alive. It is still making words for things that matter."
        menu:
            "Ask if she makes up words." :
                mc "Do you make up words?"
                murakami "Sometimes. Japanese is good at that. We take two words and make a new one. 'Kimochi' means 'feeling.' 'Kimochi ii' means 'good feeling.' 'Kimochi warui' means 'bad feeling.'"
                murakami "We do not have a word for 'the feeling of being slightly uncomfortable.' We say 'nanto naku.' It means 'somehow' or 'sort of.' It is the most honest word in Japanese."
                $ reward_attributes_once("murakami_rep_komorebi", [("insight", "micro")], show="auto")
            "Ask what her favorite word is." :
                mc "What is your favorite word?"
                murakami "'Itadakimasu.' {jp}いただきます{/jp} The word you say before eating. It means 'I receive this.' It is not 'I eat.' It is 'I am grateful for this.'"
                murakami "It is the most Japanese word I know. It is also the most human."
                $ reward_attributes_once("murakami_rep_itadakimasu", [("grace", "micro")], show="auto")
            "Ask if the students still get it wrong." :
                mc "Do they still get it wrong?"
                murakami "Every day. It is the best part. The wrong answers are always the most interesting."
                murakami "Sit down. Let us see what you get wrong today."
                $ reward_attributes_once("murakami_rep_wrong", [("nerve", "micro")], show="auto")

    elif variant == 1:
        "The review session. Murakami has brought worksheets and the room smells like paper and anxiety."
        "It is the kind of anxiety that is actually excitement."
        murakami "Today we review. Not grammar. Not vocabulary. The things that do not have words."
        murakami "I want you to tell me: what is the hardest thing about living in Japan?"
        "The room is quiet. The kind of quiet that means everyone is thinking."
        oliver "The trains. They are perfect and they are terrifying."
        priya "The food. It is perfect and it is confusing. What do I order? What does it mean?"
        wei "The kanji. I can read them but I cannot say them. I am a library that cannot speak."
        prakash "The silence. People do not talk. They just... exist. It is beautiful and it is hard."
        saman "The anime. It is perfect and it is not real. I want to live in it but I cannot."
        "Murakami looks at each of them. She is not writing. She is just listening."
        murakami "Those are the right answers. The hardest things are the best things. That is why you are still here."
        menu:
            "Ask what her hardest thing is." :
                mc "What is your hardest thing?"
                murakami "Watching you leave. Every year, the students go back. They take the room with them. I am still here. The room is still here. But the students are gone."
                murakami "That is the hardest thing. Not the grammar. Not the vocabulary. The leaving."
                $ reward_attributes_once("murakami_rep_hard", [("grace", "micro")], show="auto")
            "Ask if she misses the students." :
                mc "Do you miss the students?"
                murakami "Every day. I keep their certificates. I keep their sticky notes. I keep the words they taught me."
                murakami "I miss the room when it is empty. I miss the noise. I miss the wrong answers. I miss the moment when someone understands something for the first time."
                $ reward_attributes_once("murakami_rep_miss", [("insight", "micro")], show="auto")
            "Ask if she will teach next year." :
                mc "Will you teach next year?"
                murakami "I will teach until I cannot. The room is my life. The students are my reason."
                murakami "You will be gone. But the room will not. The next students will come. The cycle will continue."
                $ reward_attributes_once("murakami_rep_next", [("nerve", "micro")], show="auto")

    else:
        "The quiet day. No lesson. No quiz. Just the room and the students and Murakami making tea."
        "It is the best kind of day. The kind where nothing happens and everything matters."
        murakami "Today we do nothing. Sit. Drink tea. Talk."
        "We sit. We drink. We talk. In five languages and one that is mostly gestures."
        "Wei is teaching Priya how to say 'delicious' in Chinese. Priya is teaching Oliver how to say 'thank you' in Hindi."
        "Oliver is teaching Prakash how to say 'cheers' in English. Prakash is teaching Saman how to say 'good luck' in Nepali."
        "Saman is teaching me how to say 'thank you' in Sinhala. It sounds like a song."
        "Murakami is watching. She is not teaching. She is just... being there."
        menu:
            "Ask what she is thinking." :
                mc "What are you thinking?"
                murakami "I am thinking that this is the best class I have ever had. Not because the students are perfect. Because they are real."
                murakami "They are scared and excited and lost and found. They are all of those things at once. That is what makes them worth teaching."
                $ reward_attributes_once("murakami_rep_thinking", [("grace", "micro")], show="auto")
            "Ask if she is happy." :
                mc "Are you happy?"
                murakami "I am happy. Not because everything is perfect. Because everything is real. The room is real. The students are real. The mistakes are real."
                murakami "Happiness is not the absence of problems. It is the presence of meaning. This room has meaning."
                $ reward_attributes_once("murakami_rep_happy", [("insight", "micro")], show="auto")
            "Ask what she will do after this." :
                mc "What will you do after this?"
                murakami "I will go home. I will make dinner. I will sleep. Tomorrow I will come back and do it again."
                murakami "That is what teachers do. We come back. We teach. We come back. We teach. The cycle is the point."
                $ reward_attributes_once("murakami_rep_cycle", [("nerve", "micro")], show="auto")

    "The repeat visit ends the same way every time: the room is quiet, the students are still wrong in the same loving way, and Murakami is still writing on the board."
    "The room stays open. The course never ends. Neither do the students."
    "Neither do I."

    $ confidant_visits["murakami"] = max(confidant_visits.get("murakami", 0), 11)
    $ murakami_lessons = max(murakami_lessons, 11)
    $ japanese_fluency = min(5, japanese_fluency + 1)
    $ log_memory("murakami", "another office hours; the room stays open and the students stay wrong in the same loving way")
    $ reward_attributes_once("murakami_rep_close", [("grace", "micro")], show="auto")
    return

################################################################################
## THE DAILY PING
################################################################################
##
## Called once each morning from `common_day_core` and the special days after
## Day 10. Before enrollment she occasionally asks if he has decided; after
## enrollment she reminds him that office hours exist. Everything is
## deterministic on `story_day` so a save always gets the same ping.
##
## The gate is `murakami_enrolled`, not `murakami_lessons`: sitting in on her
## classes informally is not the same as joining the course.

label murakami_daily_ping:
    if "murakami" not in wire_unlocked:
        return
    $ today = store.story_day
    if not store.murakami_enrolled:
        # One real retry on the first class day back, then a gentle nudge
        # every week after that. The seat stays warm; it does not expire.
        if today == 14 or (today > 14 and (today - 14) % 7 == 0):
            $ run_chat("murakami", [
                {"them": "The seat is still warm. Have you decided about the course?"},
            ])
            menu:
                "Sign me up.":
                    $ murakami_enrolled = True
                    $ log_memory("murakami", "enrolled in the Japanese elective after Murakami's text")
                    $ reward_attributes_once("murakami_enroll_text", [("nerve", "micro")], show="auto")
                    "I type 'yes' before I can talk myself out of it. She answers before the bubble finishes forming: Good. Bring a question you cannot answer."
                "Not yet.":
                    "I type 'maybe.' She does not answer for an hour. Then: The seat is warm. It does not expire."
        return
    # Enrolled: a reminder every third weekday, rotating so it never repeats
    # two mornings in a row.
    if common_day_school(today) and today % 3 == 0:
        $ variant = (today // 3) % 3
        if variant == 0:
            $ run_chat("murakami", [
                {"them": "Office hours tomorrow. Second floor. Bring a question you cannot answer."},
            ])
        elif variant == 1:
            $ run_chat("murakami", [
                {"them": "New worksheet. It has a trick question on it. Everyone fails it beautifully."},
            ])
        else:
            $ run_chat("murakami", [
                {"them": "The good chairs go fast. Come early or accept the wall."},
            ])
    return
