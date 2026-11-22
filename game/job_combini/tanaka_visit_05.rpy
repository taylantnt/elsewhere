################################################################################
## THE COMBINI JOB: VISIT 5: JUST ENOUGH
################################################################################
##
## Make just enough. Do not be afraid to sell out. The last lesson before the
## protagonist finds out who has been teaching him.

label tanaka_visit_05:
    call tanaka_common_open from _call_tanaka_common_open_5

    "Today there is a clipboard. The clipboard is the scariest thing in the building."
    tanaka "The order. What the store will make this afternoon. You do not fill the case. You predict the afternoon."
    tanaka "Too much is disposal. Too little is an empty sleeve. Both are failures, but only one of them is a lie."
    mc "Which one is the lie?"
    tanaka "Too much. It says: I could not imagine the customer, so I made a mountain to hide behind."
    "He shows me the numbers. Last Tuesday's afternoon. The Tuesday before that. Rain, and what rain does to a Tuesday."
    tanaka "The store remembers its afternoons. You do not guess. You ask the store and you believe it."

    "We build the order together. I write the numbers. He does not correct the first column. He lets it be wrong on paper first."
    tanaka "Write what you think. The paper is cheap. The fried rice is not."
    mc "(He wants my guess. Not the safe guess. My guess.)"

    menu:
        "Order less than the store says.":
            "I round every number down. If the afternoon is slow, the case stays fresh and the disposal bag stays light."
            tanaka "You will sell out of the karaage at six."
            mc "Is that bad?"
            tanaka "It is honest. A sold-out sleeve says: we made the right amount and the city was hungrier than the paper said."
            tanaka "A customer walks away hungry and comes back tomorrow. A customer who bites something old does not come back at all."
            mc "(Sold out is not failure. It is a promise that got kept slightly too well.)"
            $ reward_attributes_once("tanaka_v5_less", [("insight", "micro")], show="auto")
        "Order exactly the store's number.":
            "I copy the last four Tuesdays and split the difference. The numbers are boring and correct."
            tanaka "Good. The store does not need courage. It needs a Tuesday."
            mc "(He gave me the answer and then made me arrive at it myself. That is the trick of good teaching, I think.)"
            $ reward_attributes_once("tanaka_v5_exact", [("grace", "micro")], show="auto")
        "Ask what he does when he is wrong.":
            mc "What happens when you get it wrong?"
            tanaka "I eat the mistake. Not literally. The record shows the batch, the disposal, the gap. The next order fixes it."
            tanaka "Being wrong on purpose is fine. Being wrong by accident twice is not."
            mc "(He said on purpose twice today. Everything here is chosen. Even the mistakes.)"
            $ reward_attributes_once("tanaka_v5_wrong", [("nerve", "micro")], show="auto")

    "At six the karaage sleeve is empty and stays empty until seven. Two people ask for it. Two people get told when the next batch is."
    tanaka "You see? Sold out is a conversation. Old is a monologue."
    mc "(He taught me quality and timing and the honest garbage bag. Every shift I am grateful. Every shift he orders me around like the floor is his living room.)"
    mc "(If he is not the manager, then the manager owes him a raise. If he is the manager, then I have been being trained by the building itself.)"
    mc "(Either way. Somebody is this store's father, and I am starting to think I have been working for him all along.)"
    mc "(I do not know how many afternoons I have given him. I do not remember choosing the first one.)"

    call tanaka_wage_close from _call_tanaka_wage_close_5

    tanaka "Eat something before you go home."
    "He puts a rice ball on the counter and pushes it toward me. It is not on the receipt."
    mc "I didn't pay for this."
    tanaka "It is damaged stock."
    mc "It is in perfect condition."
    tanaka "Then it is damaged in a way you cannot see."
    mc "(I take it. He goes back to the drawer.)"

    call tanaka_walk_home from _call_tanaka_walk_home_5
    return
