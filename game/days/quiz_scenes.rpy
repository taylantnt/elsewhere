################################################################################
## QUIZ SCENES
################################################################################
##
## Pop quizzes and exam sets that use the run_quiz system (quiz.rpy). Each label
## is called from the day file at the natural moment: the professor or Murakami
## asks a few questions at the end of a lecture, or Hikari quizzes the MC at
## home. Rewards follow the clean-sheet convention: Insight small for all
## correct, nothing otherwise. One-time flags prevent farming.
##
## Pacing across the build:
##   Day 5  - Sunday practice (existing, menu-style, script.rpy)
##   Day 6  - Monday quiz (existing, menu-style, script.rpy)
##   Day 8  - quiz_basho_lesson (run_quiz, 3 questions)
##   Day 11 - quiz_book_town (run_quiz, 3 questions)
##   Day 17 - quiz_sound_words (run_quiz, 3 questions)
##   Day 20 - Midterm (existing, menu-style, special_day_20)
##   Day 31 - quiz_everyday_language (run_quiz, 3 questions)
##   Day 42 - quiz_particles (run_quiz, 3 questions)
################################################################################


## --- DAY 8: after the Basho lecture -----------------------------------------

label quiz_basho_lesson:
    professor "Before you leave. Three questions. Not a quiz. A check."
    mc "(It is a quiz. He calls them checks. They are quizzes.)"

    $ _quiz_results = run_quiz([
        {
            "q": "What is mono no aware?",
            "choices": [
                "The sadness of losing something beautiful",
                "The pathos of things, the beauty of what is passing",
                "A type of seasonal poem",
                "The feeling of arriving somewhere new"
            ],
            "answer": 1,
            "explain": "Not sadness. Not quite. The feeling of a thing being beautiful because it is passing.",
        },
        {
            "q": "In Basho's old pond poem, which word is the kigo?",
            "choices": [
                "The pond",
                "The water",
                "The frog",
                "The sound"
            ],
            "answer": 2,
            "explain": "Frog is spring. The first warmth. The water warm enough to hold a life.",
        },
        {
            "q": "What did Issa write about, and why?",
            "choices": [
                "Large things, because he wanted to be famous",
                "Small things, because the large things had already happened to him",
                "Only nature, because he lived in the mountains",
                "War, because he lived through one"
            ],
            "answer": 1,
            "explain": "The beauty is not despite the loss. It is made of it.",
        },
    ])

    if all(_quiz_results):
        professor "Good. All three."
        $ reward_attributes_once("quiz_day8_clean", [("insight", "small")], show="auto")
    else:
        professor "Some. Review the handout tonight."

    $ del _quiz_results
    return


## --- DAY 11: after the Jimbocho book town trip -------------------------------

label quiz_book_town:
    murakami "Before we part. Three questions. You have read three authors today. Let us see if they stayed."
    mc "(She does this. She pretends it is casual. It is not casual.)"

    $ _quiz_results = run_quiz([
        {
            "q": "What is wabi-sabi?",
            "choices": [
                "A type of tea ceremony",
                "The beauty of what is imperfect, incomplete, and passing",
                "A style of calligraphy",
                "A seasonal festival"
            ],
            "answer": 1,
            "explain": "It is not a decoration. It is a way of looking at a thing that is already leaving.",
        },
        {
            "q": "What does ichigo ichie mean?",
            "choices": [
                "One book, one reader",
                "One time, one meeting. Every encounter happens once and never again",
                "A type of cherry blossom",
                "The first cup of tea"
            ],
            "answer": 1,
            "explain": "Not because people die. Because the people who meet are never the same two people twice.",
        },
        {
            "q": "Which author asked whether you can know another person?",
            "choices": [
                "Kawabata (Snow Country)",
                "Tanizaki (In Praise of Shadows)",
                "Soseki (Kokoro)",
                "Murasaki Shikibu (Genji)"
            ],
            "answer": 2,
            "explain": "A man who cannot say the thing he means until it is too late.",
        },
    ])

    if all(_quiz_results):
        murakami "All three. You were listening."
        $ reward_attributes_once("quiz_day11_clean", [("insight", "small")], show="auto")
    else:
        murakami "Some. The books are still in your bag. Read them again tonight."

    $ del _quiz_results
    return


## --- DAY 17: after the giongo/gitaigo lesson --------------------------------

label quiz_sound_words:
    murakami "Three questions before you go. Sound words. State words. Silence."
    mc "(She is already holding the card. She had it ready before I sat down.)"

    $ _quiz_results = run_quiz([
        {
            "q": "What is the difference between giongo and gitaigo?",
            "choices": [
                "Giongo is for writing, gitaigo is for speaking",
                "Giongo is sound words, gitaigo is state words",
                "Giongo is old, gitaigo is new",
                "There is no difference"
            ],
            "answer": 1,
            "explain": "Giongo is the sound a thing makes, written down. Gitaigo is the way a thing is, written down as if it were a sound.",
        },
        {
            "q": "What is shiin?",
            "choices": [
                "A type of poem",
                "A word for silence that is not the absence of sound",
                "A punctuation mark",
                "A seasonal word"
            ],
            "answer": 1,
            "explain": "The silence between stations. The pause that is not a pause.",
        },
        {
            "q": "Which script was called onnade, women's hand?",
            "choices": [
                "Kanji",
                "Katakana",
                "Hiragana",
                "Manyougana"
            ],
            "answer": 2,
            "explain": "The curves. Because women wrote the private things in it, and the novel was born there.",
        },
    ])

    if all(_quiz_results):
        murakami "Clean. You are paying attention."
        $ reward_attributes_once("quiz_day17_clean", [("insight", "small")], show="auto")
    else:
        murakami "Close. Listen to the city tonight. It will teach you the rest."

    $ del _quiz_results
    return


## --- DAY 31: everyday language quiz (common day) ----------------------------

label quiz_everyday_language:
    murakami "Quick check. Three questions. Nothing you have not heard."
    mc "(She says nothing you have not heard. She means nothing you should have remembered.)"

    $ _quiz_results = run_quiz([
        {
            "q": "What does 'benkyou suru' break down to?",
            "choices": [
                "Study-hard. The effort is the act",
                "Study-do. The doing is borrowed, the naming is the act",
                "Study-fast. The speed is the point",
                "Study-again. The repetition is the act"
            ],
            "answer": 1,
            "explain": "In Japanese, you do things by naming them.",
        },
        {
            "q": "Which honorific is used for customers?",
            "choices": [
                "-kun",
                "-chan",
                "-sama",
                "-senpai"
            ],
            "answer": 2,
            "explain": "For those you serve. Never yourself.",
        },
        {
            "q": "What is the difference between honne and tatemae?",
            "choices": [
                "Honne is the face, tatemae is the feeling",
                "Honne is what you mean, tatemae is what you show",
                "Honne is formal, tatemae is casual",
                "There is no difference"
            ],
            "answer": 1,
            "explain": "The feeling and the face. What you mean versus what you show.",
        },
    ])

    if all(_quiz_results):
        murakami "All three. You are settling in."
        $ reward_attributes_once("quiz_day31_clean", [("insight", "small")], show="auto")
    else:
        murakami "Some. The city will test you on the rest."

    $ del _quiz_results
    return


## --- DAY 42: particles quiz (common day) ------------------------------------

label quiz_particles:
    murakami "Three questions. Particles. The small words that decide everything."
    mc "(She has been waiting for this one. I can tell.)"

    $ _quiz_results = run_quiz([
        {
            "q": "What is the difference between 'wa' and 'ga'?",
            "choices": [
                "Wa is formal, ga is casual",
                "Wa marks the topic, ga marks the subject",
                "Wa is for questions, ga is for statements",
                "There is no difference"
            ],
            "answer": 1,
            "explain": "One is context. The other is news.",
        },
        {
            "q": "What does 'Watashi wa' versus 'Watashi ga' illustrate?",
            "choices": [
                "Two ways to say the same thing",
                "Two ways to be a person: as the topic of someone else's life, or as the subject of your own",
                "One is polite, one is rude",
                "One is written, one is spoken"
            ],
            "answer": 1,
            "explain": "Because there are two ways to be a person.",
        },
        {
            "q": "What is kanji?",
            "choices": [
                "Characters borrowed from China",
                "The curves invented by women",
                "A type of seasonal word",
                "A sound word"
            ],
            "answer": 0,
            "explain": "Serious, official, the language of documents.",
        },
    ])

    if all(_quiz_results):
        murakami "Clean. You are thinking in the right shape now."
        $ reward_attributes_once("quiz_day42_clean", [("insight", "small")], show="auto")
    else:
        murakami "Close. The particles will click eventually. They always do."

    $ del _quiz_results
    return
