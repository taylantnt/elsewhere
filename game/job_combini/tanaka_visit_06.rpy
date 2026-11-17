################################################################################
## THE COMBINI JOB ― VISIT 6: THE TENCHO
################################################################################
##
## The reveal. The man who has been ordering the protagonist around for five
## shifts is not a colleague. He is the tencho. The store manager. The store
## has been his voice the whole time.

label tanaka_visit_06:
    call tanaka_common_open

    "The shift starts normally. That is the last normal thing about it."
    "At seven, the phone behind the counter rings. It is an old phone with a cord and it rings like a threat."
    "Tanaka picks it up. He listens. He says four words in a row that I do not catch, and then he says one that I do."
    tanaka "店長です。"
    mc "(A word I do not know, said like a name. I will ask what it means.)"
    "He puts the phone down and writes something on a slip and keeps working, and the word sits in the air between us like spilled salt."

    menu:
        "Ask him directly.":
            mc "You're the manager."
            tanaka "Yes."
            mc "Since when?"
            tanaka "Since the shutters went up. Before your shirt. Before my shirt had a different name on it."
            $ reward_attributes_once("tanaka_v6_ask", [("nerve", "micro")], show="auto")
        "Put the ledger back exactly where he left it.":
            "I set the ledger down where it was, corner aligned with the corner of the crate. The fryer hums."
            "He lets three customers go by before he speaks. He is a man who chooses his seconds."
            tanaka "You have been wondering."
            mc "A little."
            tanaka "Good. A person who wonders is a person who is paying attention."
            $ reward_attributes_once("tanaka_v6_wait", [("grace", "micro")], show="auto")
        "Ask why he hid it.":
            mc "You never said. Five shifts."
            tanaka "If I say it first, you work for a title. Titles make people careful. I did not want you careful. I wanted you good."
            mc "(He did not want me careful. That is the most management I have ever heard in a sentence.)"
            $ reward_attributes_once("tanaka_v6_hidden", [("insight", "micro")], show="auto")

    "He takes the slip with the phone number on it and pins it to the wall behind the register. The wall is a foot thick with pinned slips."
    "Bills. Delivery notes. A photo of a dog. A card that says, in a child's handwriting, GANBATTE."
    tanaka "This is the office. It is four square meters and it has the best view in the store."
    mc "There's no window."
    tanaka "There is a counter. A counter is a window that looks at your own work."
    mc "(I have been grateful for five shifts. And for five shifts I have been asking the wrong question.)"
    mc "(Why does the other worker order me around? Because he was never the other worker. The question was always: why does the owner of the whole machine choose to stand in the smallest room?)"

    "For a second the register light is too bright and the wall of slips is a wall of white. A door at the end of it, and someone standing behind the counter of the world."
    call leak_flash
    "Then it is a combini again, and Tanaka is counting the drawer, and I am holding tongs."
    mc "(He runs this. The lights, the oil, the order, the disposal bag. A man in the smallest room, running the biggest thing in the street.)"
    mc "(Somewhere, someone like him runs a room I cannot remember. White. Cleaner than this. The same posture. The same patience.)"
    mc "(I do not know why that thought arrives with the smell of hot oil. I keep it anyway.)"

    call tanaka_wage_close

    tanaka "Now you know."
    mc "Does it change anything?"
    tanaka "It changes what you call me when you are annoyed. Nothing else. The shift was always mine. Now the shift is yours too."
    mc "Why teach me all of it? Register, stock, grill, fryer, order. Managers don't usually..."
    tanaka "Managers who do not work hire people who do not care. I did not want you to care about a wage. I wanted you to care about the case."
    tanaka "The tencho is not the person who signs. The tencho is the person the store answers to. While I stand here, it answers to me. When you stand here, it will answer to you."
    mc "(He is not my boss. He is the building wearing a striped shirt.)"

    call tanaka_night
    return
