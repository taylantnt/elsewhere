################################################################################
## THE COMBINI JOB ― VISIT 2: THE FLOOR
################################################################################
##
## New stock, and the order of the shelves. The protagonist starts to notice
## that the store has an opinion about where things go, and that the man who
## keeps ordering him around is always the same man.

label tanaka_visit_02:
    call tanaka_common_open

    "Tonight there is no register. There is a cart."
    tanaka "The delivery comes at five. You have been standing in front of what it became. Tonight you see what it was."
    "The back door is a rolling shutter. Behind it is a cage of cardboard, and the cardboard is the store in pieces."
    tanaka "New stock does not go where there is room. It goes where the store wants it."
    mc "The store wants things?"
    tanaka "The customer wants things. The store is how the customer finds them. Same thing, if you do it right."
    "He walks the floor and points. I carry."

    "The rules come out of him one at a time, each one smaller and harder than the last."
    tanaka "The new item goes at eye level. Not because it is new. Because the eye is where decisions are made."
    tanaka "The cheap thing goes low. A person who buys cheap is not looking up. They already decided."
    tanaka "The thing a child wants goes at the height of a child's hand. The parent says no at eye level. The child wins at knee height."
    mc "(He has thought about the height of a child's hand. That is either devotion or madness.)"

    menu:
        "Face the labels forward.":
            "Every label forward, every gap closed, every row squared to the edge of the shelf. It takes longer and it looks like nothing happened."
            "Tanaka walks the aisle once. He fixes one label. Then he nods."
            tanaka "Tomorrow it will be wrong again. That is the job. Not the fixing. The doing it again."
            mc "(I could do that every day. I think that is what he is saying.)"
            $ reward_attributes_once("tanaka_v2_labels", [("grace", "micro")], show="auto")
        "Ask what the store is for.":
            mc "Why does it matter? It is a combini. People come in, they grab, they go."
            tanaka "A person in a hurry does not read. They scan. If the store argues with the scan, they leave."
            tanaka "The shelves are not for finding things. They are for not having to look."
            mc "(He is describing my first week in this country. I did not know it was also a shelf.)"
            $ reward_attributes_once("tanaka_v2_why", [("insight", "micro")], show="auto")
        "Ask why he does the floor himself.":
            mc "Doesn't someone else do this?"
            tanaka "Someone else does it wrong. Wrong is a habit. I do not keep habits I did not choose."
            mc "(He says it like a fact about cardboard. It is a fact about him.)"
            $ reward_attributes_once("tanaka_v2_who", [("nerve", "micro")], show="auto")

    "By the end of the shift my arms know the weight of a box of puddings. It is not a useful weight. It is a true one."
    mc "(He is not my boss. He is just the man who is always here. And he keeps ordering me around like the store is his.)"
    mc "(Maybe the manager should say something about that. Whoever the manager is.)"

    call tanaka_wage_close

    tanaka "Why do you want this job?"
    mc "Money."
    tanaka "Good. People who say experience are lying."
    mc "Is that all?"
    tanaka "That is enough. A job is a thing you make every day. The rest is a story you tell about it."

    call tanaka_night
    return
