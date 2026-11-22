label special_day_68_the_detail:
    $ set_story_day(68)
    call day_transition from _call_day_transition_68
    $ flush_pending_messages()

    scene bg_room_day with Dissolve(0.8)
    $ room_ambient(False)
    "Yesterday I had one picture I couldn't open and one I could. Today I print the review sheet before I leave the house."
    "On the back I write the address of the ramen shop. I write the word storeroom beside it, then cross it out. That's what she remembered. It's not what I remember."

    menu:
        "Go back to Lupin's Den with Orson's keepsake." if has_item("orson_wolf_paw_badge") or (confidant_visits.get("orson", 0) >= 7 and has_item("orson_wolf_coaster")):
            "I wait until after dark. It's the only time I've ever gone looking for that door."
            call act3_revisit_lupins from _call_act3_revisit_lupins
        "Take Aya's sketch back to the cafe." if has_item("aya_sketchbook_page"):
            call act3_revisit_aya from _call_act3_revisit_aya
        "Ask Hikari to write down what she remembers.":
            scene bg_kitchen with walk_fade
            "I put two sheets of paper on the table. I ask her not to look at mine."
            if "rail_independent_accounts" in story_memory_keys:
                hikari "Like at the rail. I go first, and you don't tell me if I got it right."
            hikari "The rail?"
            mc "The way back. Just the light. Where you remember it going out."
            "She writes three lines. I write two. Neither of us puts a line through the other's."

    scene bg_room_night with Dissolve(0.8)
    $ room_ambient(True)
    "I put the print in my notebook. Before I close it I add one line underneath the address: I ate there."

    jump act2_day_router
