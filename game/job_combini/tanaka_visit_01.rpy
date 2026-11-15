################################################################################
## THE COMBINI JOB — VISIT 1: THE FIRST SHIFT
################################################################################
##
## Orientation. The shirt, the register, the script. The protagonist learns
## that a combini conversation has a receipt, and Tanaka learns that the new
## part-timer says irasshaimase like an apology.

label tanaka_visit_01:
    call tanaka_common_open

    "The shift starts at six. Tanaka is already there, counting the register drawer with the concentration of a man defusing something."
    tanaka "You are on time."
    mc "You said not to be late."
    tanaka "Being on time is not the same as not being late. It is better."
    "He hands me a striped shirt that smells of detergent and cold air."
    tanaka "Wear it. The collar is the uniform. The rest is just a shirt."
    tanaka "Today you stand where I stand and you say the words. That is the whole lesson. Tomorrow the words are still the lesson."

    "The next four hours are a loop. The door chimes. A customer comes in. I say the words. The words are the same every time."
    mc "(いらっしゃいませ。温めますか。フォークは。スプーンは。お箸は。ポイントカードは。お支払いは。クーポンは。袋は。)"
    mc "(By the second hour I can say them without thinking. By the third hour I can say them while thinking about something else.)"
    mc "(By the fourth hour I understand why Tanaka likes that the conversation ends.)"

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

    call tanaka_wage_close

    tanaka "You said irasshaimase like an apology."
    mc "Did I?"
    tanaka "Lower. From the chest. You are not sorry to be here. You are here."
    mc "(I try it again. It sounds different. He nods once.)"
    mc "(He taught me a thing my first language did not have a word for. I am grateful. I am also tired.)"
    mc "(He is just staff. Same shirt as mine. Why does the other worker get to be the one who corrects me?)"

    call tanaka_night
    return
