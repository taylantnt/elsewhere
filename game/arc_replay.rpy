################################################################################
## ARC REPLAY ― CONSOLE TEST MODE
################################################################################
##
## Shift+O, then `jump arc_replay`. Pick a confidant and watch their whole
## written chain back-to-back, without playing the days between the visits.
## You can also jump straight to one arc:
##
##   jump arc_replay_sim      jump arc_replay_orson
##   jump arc_replay_aya      jump arc_replay_hana
##
## This calls the real visit labels, so the dialogue, menus, attribute cards,
## memories and WIRE messages are exactly the ones from play. It snapshots the
## save state on the way in and puts it back on the way out, so a test run in a
## live save does not permanently spend your rewards or advance your counters.
## Quitting in the middle of a replay skips the restore ― finish the arc.
##
## Visit 1 for Orson, Aya and Hana is inside the Day 1/2 routes, not a separate
## label, so those arcs start at visit 2. Sim's visit 1 is standalone and is
## included.

init python:
    import copy

    _arc_replay_saved = None

    def arc_replay_begin():
        """Snapshot everything the visits write, then prime a clean chain."""
        global _arc_replay_saved
        names = (
            "confidant_visits", "sim_affection", "orson_affection",
            "aya_affection", "hana_affection", "attribute_reward_flags",
            "character_memories", "memory_names", "pending_messages",
            "wire_unlocked", "wire_contacts", "camera_unlocked",
            "phone_map_unlocked", "phone_map_visited", "sim_campus_intro",
        )
        _arc_replay_saved = {}
        for name in names:
            if hasattr(store, name):
                _arc_replay_saved[name] = copy.deepcopy(getattr(store, name))

        # A clean slate makes the reward cards fire and lets each visit's own
        # counter update decide where the chain is, exactly as in play.
        store.confidant_visits = dict((key, 0) for key in store.confidant_visits)
        store.attribute_reward_flags = []
        store.character_memories = {}
        store.memory_names = {}
        store.pending_messages = []
        store.sim_campus_intro = False
        store.sim_affection = 0
        store.orson_affection = 0
        store.aya_affection = 0
        store.hana_affection = 0

    def arc_replay_end():
        """Put the live save back the way it was before the replay."""
        global _arc_replay_saved
        if _arc_replay_saved:
            for name, value in _arc_replay_saved.items():
                setattr(store, name, value)
        _arc_replay_saved = None
        renpy.notify("Arc replay finished. Your progress was restored.")


label arc_replay:
    scene black with Dissolve(0.8)
    "ARC REPLAY"
    "Pick a chain. Every visit is the real scene, played back-to-back with a card between them."
    "Nothing you do here is kept: the visits, rewards, memories and messages are restored when the arc ends."
    menu:
        "Sim ― Circle (visit 1 through the epilogue)":
            call arc_replay_sim from _arc_hub_sim
        "Orson ― Lupin's Den (visits 2-7 and the epilogue)":
            call arc_replay_orson from _arc_hub_orson
        "Aya ― the Maid Cafe (visits 2-7 and the epilogue)":
            call arc_replay_aya from _arc_hub_aya
        "Hana ― the Reading Club (visits 2-7 and the epilogue)":
            call arc_replay_hana from _arc_hub_hana
        "Stop":
            return
    scene black with Dissolve(0.6)
    jump arc_replay


label arc_replay_sim:
    $ arc_replay_begin()
    scene black with Dissolve(0.5)
    "SIM // VISIT 1 ― THE DOOR WITH TAPE ON IT"
    call sim_visit_01 from _arc_sim_01

    scene black with Dissolve(0.5)
    "SIM // VISIT 2 ― CAMERA FIRST, INTRODUCTIONS SECOND"
    call sim_visit_02 from _arc_sim_02

    scene black with Dissolve(0.5)
    "SIM // VISIT 3 ― THE FIRST FRAME THAT IS HIS"
    call sim_visit_03 from _arc_sim_03

    scene black with Dissolve(0.5)
    "SIM // VISIT 4 ― THE EXHIBITION"
    call sim_visit_04 from _arc_sim_04

    scene black with Dissolve(0.5)
    "SIM // VISIT 5 ― THE EMPTY ROOM"
    call sim_visit_05 from _arc_sim_05

    scene black with Dissolve(0.5)
    "SIM // VISIT 6 ― THE MAGAZINE OFFER"
    call sim_visit_06 from _arc_sim_06

    scene black with Dissolve(0.5)
    "SIM // VISIT 7 ― TT AT THE EXHIBITION"
    call sim_visit_07 from _arc_sim_07

    scene black with Dissolve(0.5)
    "SIM // EPILOGUE ― THE CLUB ON HOLD"
    call sim_visit_closed from _arc_sim_closed

    $ arc_replay_end()
    scene black with Dissolve(0.8)
    "END OF SIM'S ARC"
    return


label arc_replay_orson:
    $ arc_replay_begin()
    scene black with Dissolve(0.5)
    "ORSON // VISIT 2 ― THE MASKS"
    call orson_visit_02 from _arc_orson_02

    scene black with Dissolve(0.5)
    "ORSON // VISIT 3 ― THE NOTEBOOK"
    call orson_visit_03 from _arc_orson_03

    scene black with Dissolve(0.5)
    "ORSON // VISIT 4 ― THE LIFE BEFORE THE BAR"
    call orson_visit_04 from _arc_orson_04

    scene black with Dissolve(0.5)
    "ORSON // VISIT 5 ― THE ROUTINES"
    call orson_visit_05 from _arc_orson_05

    scene black with Dissolve(0.5)
    "ORSON // VISIT 6 ― THE COASTER AND THE CRACK"
    call orson_visit_06 from _arc_orson_06

    scene black with Dissolve(0.5)
    "ORSON // VISIT 7 ― HE TAKES THE MASK OFF"
    call orson_visit_07 from _arc_orson_07

    scene black with Dissolve(0.5)
    "ORSON // EPILOGUE ― THE WOLF STILL HANGING"
    call orson_visit_closed from _arc_orson_closed

    $ arc_replay_end()
    scene black with Dissolve(0.8)
    "END OF ORSON'S ARC"
    return


label arc_replay_aya:
    $ arc_replay_begin()
    scene black with Dissolve(0.5)
    "AYA // VISIT 2 ― RECOGNITION"
    call aya_visit_02 from _arc_aya_02

    scene black with Dissolve(0.5)
    "AYA // VISIT 3 ― THE MASK, ONE LAYER"
    call aya_visit_03 from _arc_aya_03

    scene black with Dissolve(0.5)
    "AYA // VISIT 4 ― THE PERFORMANCE SLIPS"
    call aya_visit_04 from _arc_aya_04

    scene black with Dissolve(0.5)
    "AYA // VISIT 5 ― WHAT IS UNDER IT"
    call aya_visit_05 from _arc_aya_05

    scene black with Dissolve(0.5)
    "AYA // VISIT 6 ― THE NAME SHE CHOSE"
    call aya_visit_06 from _arc_aya_06

    scene black with Dissolve(0.5)
    "AYA // VISIT 7 ― NOT PERFORMING"
    call aya_visit_07 from _arc_aya_07

    scene black with Dissolve(0.5)
    "AYA // EPILOGUE ― THE SAME OMURICE"
    call aya_visit_closed from _arc_aya_closed

    $ arc_replay_end()
    scene black with Dissolve(0.8)
    "END OF AYA'S ARC"
    return


label arc_replay_hana:
    $ arc_replay_begin()
    scene black with Dissolve(0.5)
    "HANA // VISIT 2 ― GIVING THE BOOK BACK"
    call hana_visit_02 from _arc_hana_02

    scene black with Dissolve(0.5)
    "HANA // VISIT 3 ― OBSERVATION"
    call hana_visit_03 from _arc_hana_03

    scene black with Dissolve(0.5)
    "HANA // VISIT 4 ― SMALL ATTEMPTS"
    call hana_visit_04 from _arc_hana_04

    scene black with Dissolve(0.5)
    "HANA // VISIT 5 ― THE ART BOOK"
    call hana_visit_05 from _arc_hana_05

    scene black with Dissolve(0.5)
    "HANA // VISIT 6 ― SHARED SILENCE"
    call hana_visit_06 from _arc_hana_06

    scene black with Dissolve(0.5)
    "HANA // VISIT 7 ― THE CONFESSION"
    call hana_visit_07 from _arc_hana_07

    scene black with Dissolve(0.5)
    "HANA // EPILOGUE ― THE LAST FAREWELL"
    call hana_visit_closed from _arc_hana_closed

    $ arc_replay_end()
    scene black with Dissolve(0.8)
    "END OF HANA'S ARC"
    return
