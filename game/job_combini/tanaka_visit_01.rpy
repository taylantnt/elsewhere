################################################################################
## THE COMBINI JOB: VISIT 1: THE FIRST SHIFT
################################################################################
##
## Orientation. The shirt, the register, the script. The protagonist learns
## that a combini conversation has a receipt, and Tanaka learns that the new
## part-timer says irasshaimase like an apology.
##
## This is the first shift the player chooses from the JOBS row in the free
## afternoon hub. Work is never an event that happens to him on a scripted day;
## it happens because he picked the Convenience Store for the afternoon. The
## unlock comes from the first purchase on Day 8, where the HELP WANTED card in
## the window puts this row in the hub.

label tanaka_visit_01:
    call tanaka_common_open from _call_tanaka_common_open_1

    "The shift starts at three. I have come straight from the last class, still carrying the bag, and Tanaka is already there counting the register drawer with the concentration of a man defusing something."
    tanaka "You are on time."
    mc "You said not to be late."
    tanaka "Being on time is not the same as not being late. It is better."
    "He hands me a striped shirt that smells of detergent and cold air."
    tanaka "Wear it. The collar is the uniform. The rest is just a shirt."
    tanaka "Today you stand where I stand and you say the words. That is the whole lesson. Tomorrow the words are still the lesson."

    scene bg_combini_working with walk_fade

    "The cold drink fridge hums along the back wall. It is the loudest thing in the store. The register is smaller than it looks from the customer side."
    "He puts me in front of it and stands beside me, not behind."
    tanaka "The register is a script. Six lines. You know them as a customer. Now you learn them from the other side."
    "He points at each button in order. His finger does not hurry."
    tanaka "Scan. Total. Cash. Change. Receipt. Bag."
    tanaka "The machine does the numbers. You do the order."
    "He taps a shallow plastic tray beside the register."
    tanaka "Hundred-yen coins go here. Flat. Not stacked."
    mc "Flat."
    tanaka "Flat. A stack falls. A tray does not."

    "The door chimes. A man in a wet coat comes in. Tanaka steps back and looks at me."
    tanaka "Say it."
    mc "Irasshaimase."
    tanaka "Again. From the chest."
    mc "Irasshaimase."
    tanaka "Once more."
    mc "Irasshaimase."
    tanaka "Now say it to the man."
    "I say it to the man. He nods without looking at me and goes to the drinks."
    "By the twentieth customer the word has stopped being a word. It is the sound the door makes. It is the sound I make when the door makes it."

    "The next four hours are a loop. The door chimes. A customer comes in. I say the words. The words are the same every time."
    mc "(いらっしゃいませ。温めますか。フォークは。スプーンは。お箸は。ポイントカードは。お支払いは。クーポンは。袋は。)"
    mc "(By the second hour I can say them without thinking. By the third hour I can say them while thinking about something else.)"
    mc "(By the fourth hour I understand why Tanaka likes that the conversation ends.)"
    mc "(I came in for money. I am being taught. I do not remember agreeing to be taught.)"

    menu:
        "Work the register.":
            "I stand at the register and say the script until my mouth knows it better than my head does."
            "An old man buys a single banana. A teenager buys three energy drinks and no food. A mother buys a bento and a small carton of milk."
            mc "(Everyone is buying a small piece of their day. I am the person who hands it to them.)"
            $ reward_attributes_once("tanaka_v1_register", [("grace", "micro")], show="auto")
        "Restock the shelves.":
            "I carry boxes from the back and fill the gaps. The shelves have a logic I did not see from the customer side."
            "The seasonal things go at eye level. The cheap things go at the bottom. The things children want go where children can reach them."
            mc "(The store is not arranged for me. It is arranged for everyone. That is the whole trick.)"
            $ reward_attributes_once("tanaka_v1_stock", [("insight", "micro")], show="auto")
        "Clean the hot case.":
            "I wipe the glass until it stops showing my face. The tongs go in their holder. The oil goes in the tray."
            "Tanaka watches me for a moment and says nothing. Then he adjusts one of the tongs by a centimeter."
            mc "(That was a compliment. I am almost sure.)"
            $ reward_attributes_once("tanaka_v1_clean", [("nerve", "micro")], show="auto")

    "At half past four an old woman comes in with an umbrella she does not need. She picks up one onigiri, then puts it back and asks me something from the shelf."
    "I catch two words and lose the rest."
    mc "(Ume. I know ume. Plum. I think. The rest is a door closing.)"
    mc "Sumimasen. Mō ichido onegaishimasu."
    "She says it again, slower. \"Ume. Onigiri no, ume.\""
    "She holds up the empty space where the onigiri was. I understand the shape of the question and none of the words."

    menu:
        "Take out the phrasebook.":
            "I take the phrasebook from my back pocket. It is small and soft at the corners."
            "I find the page for shopping. I find the word for same. I do not find the word for plum."
            "I show her the page and say the word for wait. She reads it, nods once, and waits while I go to the back shelf."
            "The plum onigiri are behind the tuna ones, in a row. I bring two to the counter. She takes one and puts the other back."
            mc "(The phrasebook did not give me the word. It gave me a minute. A minute was enough.)"
            $ log_memory("tanaka", "used the phrasebook at the counter and found the plum onigiri")
        "Ask Tanaka.":
            mc "Tanaka-san. Sumimasen."
            "He is at the hot case. He does not come over. He just looks."
            mc "Ume. Onigiri. Arimasu ka."
            tanaka "Back shelf. Bottom. Behind the tuna."
            mc "Thank you."
            tanaka "You asked in three words. That is enough."
            "I find them. The old woman takes one and bows her head once."
            mc "(I thought asking would look like failing. It looked like asking.)"
            $ log_memory("tanaka", "asked him for the word for plum instead of guessing")
        "Guess.":
            "I point at the onigiri shelf, then at the microwave, then make a circle with my hands that means nothing."
            "She says the word again and points at the shelf. Then at the back. Then at me."
            "I follow her finger to the back shelf. The plum onigiri are there, behind the tuna."
            "When I come back she is almost smiling. Not at me. At the situation."
            mc "(I do not think she is praising me. I think she is saying: you got there.)"
            $ log_memory("tanaka", "guessed at the counter and the customer pointed him to the plum onigiri")

    "She pays with a hundred-yen coin. I put it in the tray. Flat. The receipt prints, and I tear it straight on the first try."
    "She takes it, says thank you, and goes out into the street that did not rain. The door chimes behind her."

    "The counter is a room. The old woman and I built one in ninety seconds. The receipt is the part that stayed."
    "Then she left, and the next customer came, and I built another."
    mc "(A room you build and then leave. I am getting good at it.)"

    "By six the store empties, the after-school rush long gone. Tanaka hands me a mop and a grey bucket. The water is warm and smells of lemon and bleach."
    tanaka "Hot case first. Then the floor. Then the door glass."
    "I mop in rows. The fridge keeps humming. The mop keeps leaving water. The two sounds do not agree."

    call tanaka_wage_close from _call_tanaka_wage_close_1

    tanaka "The tray is flat."
    mc "Yes."
    tanaka "The receipts are straight."
    mc "Mostly."
    tanaka "Mostly is not a word I use."
    "He says it without heat. Then he takes one receipt from the spike and lines it up with the others."
    tanaka "You said irasshaimase like an apology. Like a word you had to remember."
    mc "It was."
    tanaka "Tomorrow it will be a greeting."
    mc "That is a promotion."
    tanaka "It is the job."

    call tanaka_walk_home from _call_tanaka_walk_home_1
    return
