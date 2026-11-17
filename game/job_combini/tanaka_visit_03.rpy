################################################################################
## THE COMBINI JOB: VISIT 3: THE HOT CASE
################################################################################
##
## The grill. Not overdone. The hot snacks are the part of the store a customer
## smells from the street, and Tanaka treats them like an instrument.

label tanaka_visit_03:
    call tanaka_common_open

    "Tonight the lesson is the hot case. The glass front, the warmer, the row of paper sleeves."
    tanaka "The hot case is the only part of the store a person can smell from the street. The register sells. The case invites."
    tanaka "So it is never empty and it is never tired. If the case is tired, the street can tell."
    "He shows me the trays. Nikuman in their paper cradles. Karaage in the basket. Corn dogs on their sticks. Frankfurters turning on the roller."
    tanaka "Everything here has a clock. Your job is to take it off the clock at the right second."

    "The grill is the test. Frankfurters roll on the heated bars, slow, like they are being judged."
    tanaka "The grill does not stop. You do not walk away from the grill. A frank that goes around twice is a frank nobody buys."
    tanaka "Brown is the color. Not dark brown. Not tan. Brown. When you see the color, you take it. You do not wait to be sure."
    mc "(Take it at the right second. Not before, not after. Confidence is timing with the fear removed.)"

    menu:
        "Pull one at the exact second.":
            "I watch the roller like it owes me money. One frank goes from pale to brown in the space of a breath, and I take it."
            tanaka "Good."
            "That is all he says. It is the longest good I have ever been given."
            mc "(I have been praised by a man who counts drawers. I am going to think about this for a week.)"
            $ reward_attributes_once("tanaka_v3_pull", [("nerve", "micro")], show="auto")
        "Ask what happens to the ones that go too far.":
            mc "What about the ones that go past brown?"
            tanaka "They come off. They get logged. They get disposed of. Every one."
            mc "Thrown away?"
            tanaka "Given to the trash, with a record. A store that sells tired food is telling its customers a lie every hour."
            tanaka "I do not like lying in my own building."
            mc "(His own building. Staff do not usually say that. I let it go.)"
            $ reward_attributes_once("tanaka_v3_dispose", [("insight", "micro")], show="auto")
        "Admit the fear.":
            mc "I keep waiting to be sure. That's the problem."
            tanaka "Yes. You want a signature on the decision. The frank does not sign."
            tanaka "You decide at the second you decide. Then you live there."
            mc "(He is not talking about franks anymore. He never is.)"
            $ reward_attributes_once("tanaka_v3_fear", [("grace", "micro")], show="auto")

    "For the last hour I run the case alone. He stands a step behind me and does not reach past me once."
    mc "(He taught me the case. He teaches me a thing and then he orders me around about it for the rest of the shift. I am grateful and I am annoyed in the same breath.)"
    mc "(Why does the other worker get to teach and correct and order? Somebody should tell the manager his staff has opinions.)"

    call tanaka_wage_close

    tanaka "You keep looking at me like you know me."
    mc "You remind me of someone."
    tanaka "Everyone reminds someone of someone. That is how the world saves money on faces."
    "He says it without smiling. For a second the register light is too bright, and the store is a white room with a door at the end."
    mc "(I do not tell him. I do not know how.)"

    call tanaka_night
    return
