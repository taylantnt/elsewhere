################################################################################
## THE COMBINI JOB: VISIT 4: THE FRYER
################################################################################
##
## Deep fried food is exactly timed, and what is past its time is disposed of.
## Quality is not a slogan here; it is a schedule.

label tanaka_visit_04:
    call tanaka_common_open

    "Tonight the fryer. It is the size of a suitcase and it is hotter than the argument about whether it should be open."
    tanaka "The fryer is the only machine in the store that cannot be argued with. Oil does not negotiate."
    tanaka "Karaage. Four minutes. Fries. Two fifty. When the timer speaks, the basket comes up. Not when you feel like it."
    "He sets the timer and does not watch it. He watches me."
    mc "(He trusts the clock more than he trusts me. That is fair. I would too.)"

    "The baskets go down. The oil talks. Four minutes is a long time to stand in front of a machine that is right."
    tanaka "Fried food has two lives. In the fryer and out of it. Out of the fryer it starts dying. The case slows it down. Time finishes it."
    tanaka "So the case only holds what was born recently. The rest goes."
    mc "Goes where?"
    tanaka "Disposed. Logged. Counted against the batch. It goes in the disposal bag and it goes outside of the store."
    mc "That seems like a waste."
    tanaka "It is a cost. Waste is when you did not know. A cost is when you chose. We choose every night, on purpose."

    menu:
        "Pull the basket on the timer.":
            "The timer beeps and the basket comes up. The karaage is gold at the edges and pale at the bone."
            tanaka "Now the case. Two hours. Then the disposal bag, no exceptions."
            "I line them up in the sleeve. The steam goes up and smells like a Friday."
            mc "(Four minutes ago this was batter. Two hours from now it will be garbage. Everything in between is the job.)"
            $ reward_attributes_once("tanaka_v4_timer", [("nerve", "micro")], show="auto")
        "Ask why not just sell it later.":
            mc "It's still good after two hours. Someone would buy it."
            tanaka "Someone would buy it and not come back. The sale is not the thing. The next visit is the thing."
            tanaka "A person forgives a sold-out shelf. A person does not forgive a bad bite. Sold out says we were busy. A bad bite says we do not care."
            mc "(Sold out is honest. Old is a lie. That is a whole business plan in one sentence.)"
            $ reward_attributes_once("tanaka_v4_why", [("insight", "micro")], show="auto")
        "Log the disposal properly.":
            "The disposal bag gets a tag: what, how many, what time. Tanaka checks the tag the way other people check passports."
            tanaka "A record is how a store tells itself the truth. The garbage is the only honest part of the night."
            mc "(He likes endings. Receipts, records, timers. Everything here ends on purpose.)"
            $ reward_attributes_once("tanaka_v4_log", [("grace", "micro")], show="auto")

    "At nine the fryer gets drained and wiped and covered, and the kitchen stops being hot."
    mc "(He orders me around like the clock orders him. I keep being grateful, and I keep wondering why the other worker is allowed to run the night.)"
    mc "(Somebody should ask the manager why one employee does everything. If we ever meet him.)"

    call tanaka_wage_close

    tanaka "You are not the worst."
    mc "Is that a compliment?"
    tanaka "It is a schedule. You are reliable. Reliability is rarer than talent."
    mc "(I am going to count that as a promotion.)"

    call tanaka_night
    return
