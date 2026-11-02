################################################################################
## PREVIEW ONLY - THIS FILE IS NOT PART OF THE GAME
################################################################################
##
## A scratch label for reading the proposed dialogue rewrites in the real
## dialogue box, so they can be judged before anything is changed in script.rpy.
##
## HOW TO RUN IT
##   1. Launch the game (any point is fine, including the main menu).
##   2. Press Shift+O to open the console.
##   3. Type:   jump rewrite_preview
##
## HOW TO REMOVE IT
##   Delete game/rewrite_preview.rpy AND game/rewrite_preview.rpyc.
##   Nothing in script.rpy refers to this label, so removal changes nothing else.
##
## Each beat plays the version currently in script.rpy (A), then the proposed
## version (B), with a card in between so the two can be read back to back.

label rewrite_preview:

    scene black with Dissolve(1.0)

    "PREVIEW: PROPOSED REWRITES"
    "script.rpy has not been changed. This label is a scratch pad."
    "Three beats follow. Each one plays the current version, then the proposed one."


    # -------------------------------------------------------------------------
    # BEAT 1: SIM, ON WHY HE NEVER LEAVES.
    # A live decision. This is a voice change, not a continuity fix, which is
    # why the clean-noise policy does not decide it for you.
    # -------------------------------------------------------------------------

    scene black with Dissolve(0.8)
    "BEAT 1: SIM"
    "A. Currently in the script."

    scene bg_photo_club with Dissolve(1.0)
    mc "Do you ever think of leaving?"
    sim "(shrugs) Sometimes. Then I think of this place. The people in it. It keeps me here, every time."

    scene black with Dissolve(0.8)
    "B. Proposed. Same answer, and he never states it. He reports a fact about somebody else instead."

    scene bg_photo_club with Dissolve(1.0)
    mc "Do you ever think of leaving?"
    sim "(shrugs) Last spring, nearly. Then Rina brought in a print she hated, and it was good, and she did not know it was good."
    sim "I stayed to tell her. That was eleven months ago."


    # -------------------------------------------------------------------------
    # BEAT 2: HIKARI'S CARD LINE.
    # Not a live decision. The clean-noise policy rules variant B out, so this
    # is here to be looked at and then dismissed rather than adopted.
    # -------------------------------------------------------------------------

    scene black with Dissolve(0.8)
    "BEAT 2: HIKARI'S CARD LINE"
    "A. Currently in the script. This is the version the clean-noise policy keeps."

    scene bg_home_exterior_day with Dissolve(1.0)
    mc "You could have left me at the gate, like everyone else."
    hikari "..."
    hikari "I answered every email you sent this year. That was my job."
    hikari "Walking you home is the same job. I'm just doing it where you can see it."

    scene black with Dissolve(0.8)
    "B. Ruled out by the clean-noise policy."
    "A deliberate slip of the world's furniture, noticed by him and never explained. Shown only so the decision can be checked against how it actually reads."

    scene bg_home_exterior_day with Dissolve(1.0)
    mc "You could have left me at the gate, like everyone else."
    hikari "..."
    hikari "I was standing at a station holding a card with your name on it. I'm still paying that hour off."
    "Three seconds of quiet, and I go back through today, and she is not in it."
    mc "(She was not at any station. I have the whole day in order. There is no version of it with a card in it.)"
    mc "(I do not say so. She does not look like somebody who has made a mistake.)"


    # -------------------------------------------------------------------------
    # BEAT 3: THE VOICES, IN DAYLIGHT.
    # New material, not a rewrite. Under the clean-noise policy this is the
    # flagship Act 2 move, because it escalates without adding any new lore.
    # -------------------------------------------------------------------------

    scene black with Dissolve(0.8)
    "BEAT 3: THE VOICES, IN DAYLIGHT"
    "New draft. Act 2. Half a sentence of the clinical voice while he is awake and mid-conversation, then the denial that Act 1 already built for him."
    "Written to be dropped into a corridor scene at any point. The lines either side of the flash are placeholders."

    scene bg_campus_interior with Dissolve(1.0)
    hikari "You're doing the thing where you look at the floor and count."
    mc "I'm not counting."
    hikari "You're counting."

    show hospital_flash onlayer overlay at truecenter:
        alpha 0.0
        linear 0.1 alpha 0.35
        linear 0.1 alpha 0.0
    "Bring him up slowly. He is not supposed to notice the overlap."

    mc "...Sorry. What did you say?"
    hikari "I said you're counting."
    mc "(That was a voice from the dream. In the corridor. In daylight.)"
    mc "(Long flight. Longer morning. That is all it is.)"


    scene black with Dissolve(1.0)
    "END OF PREVIEW"
    "script.rpy was not touched."
    $ renpy.full_restart()
