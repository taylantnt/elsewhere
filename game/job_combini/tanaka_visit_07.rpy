################################################################################
## THE COMBINI JOB: VISIT 7: CLOSING
################################################################################
##
## The last teaching shift. Tanaka lets the protagonist close the store, and
## the lesson underneath all the others finally gets said out loud. The job
## does not end here; the row keeps repeating after this. But the teaching is
## done, and both of them know it.

label tanaka_visit_07:
    call tanaka_common_open

    "The shift is different from the first second, and it takes me an hour to work out why."
    "He is not standing behind me."
    tanaka "Tonight you close."
    mc "Close the store?"
    tanaka "Lock the store. Count the drawer. Drain the fryer. Log the disposal. Turn the sign. I will be in the office."
    mc "And if something goes wrong?"
    tanaka "Then something goes wrong and you fix it. The store has survived me for years. It will survive you for one night."

    "Four hours of the script. Old man, one banana. Schoolgirl, two ice creams. Mother, bento and milk. A man in a suit who buys a razor and a pudding and does not explain himself."
    "I pull the franks at brown. I pull the karaage on the timer. I sell the last nikuman at nine and leave the sleeve empty, and nobody is more surprised than me at how good the empty sleeve looks."
    mc "(Just enough. The case is not full. It is right.)"

    menu:
        "Close it exactly as taught.":
            "Drawer. Fryer. Disposal log, tagged and honest. The sign turned, the lights down, the door locked. Every step in the order he taught it."
            "When I come out of the office, he is putting on his coat."
            tanaka "You closed my store."
            mc "Yes."
            tanaka "It was here when I got here tonight. It will be here tomorrow. That is the whole test."
            $ reward_attributes_once("tanaka_v7_exact", [("grace", "micro")], show="auto")
        "Leave the last judgment call to him.":
            "Two karaage are still in the case at close. Sellable, technically. I bring the question to the office instead of deciding alone."
            tanaka "You are asking me."
            mc "It's your store."
            tanaka "It is your shift. Decide."
            "I log them and bag them. He watches me write the tag and nods once."
            tanaka "That is the job. Not the fryer. The deciding."
            $ reward_attributes_once("tanaka_v7_judgment", [("nerve", "micro")], show="auto")
        "Ask what happens after tonight.":
            mc "Is this the last one? The teaching."
            tanaka "Teaching was never the plan. Work was the plan. Teaching is what happened while you were working."
            mc "So what do I learn now?"
            tanaka "Repetition. It is the only teacher left. It is also the one that matters."
            mc "(He is telling me the arc is over and the job is not. I did not know a combini could say that.)"
            $ reward_attributes_once("tanaka_v7_after", [("insight", "micro")], show="auto")

    call tanaka_wage_close

    "He puts on his coat. The coat is better than the shirt. It always was; I just never let myself notice."
    tanaka "One more thing. Then you go home."
    mc "Okay."
    tanaka "Every person who walks in here is carrying a day. You do not know if it was a good one. The register does not ask. The case does not ask."
    tanaka "But a store that is clean, and lit, and stocked, and honest about its fryer, says the same thing to every one of them: whoever you are, tonight you are a customer. That is the whole country, in a glass case on a corner."
    mc "(He has been teaching me Japan through a fryer. Six visits. I thought the teacher was the elective.)"
    mc "Thank you. For the teaching."
    tanaka "Do not thank me. You paid attention. That is the whole tuition."

    call tanaka_night
    return
