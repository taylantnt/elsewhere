label special_day_69_the_copy:
    $ set_story_day(69)
    call day_transition from _call_day_transition_69
    $ flush_pending_messages()

    scene bg_campus_interior with walk_fade
    "Between classes I try the copier in the hall. The first copy comes out warm. The second one jams. A student behind me reaches around and opens the tray."
    "I thank her. For a minute I'm only a person holding up the line."
    "When I get the page back, I check the bottom. The answer in blue is on both copies."
    "I catch Hikari between classes and give her one. She holds it up to the window, then folds it into quarters."

    menu:
        "Take Sim's strap back to Circle." if has_item("sim_camera_strap"):
            call act3_revisit_circle from _call_act3_revisit_circle
        "Take Hana's charm back to the library." if has_item("hana_art_charm"):
            call act3_revisit_hana from _call_act3_revisit_hana
        "[tag_insight] Rank 4: Compare them without telling her which one you wrote." if has_attribute("insight", 4):
            "I line up the bottom corners against the window and say nothing about which is mine."
            hikari "You are looking for the pen mark."
            mc "It is the only part I can call mine. Everything else is in both."
            hikari "Then keep the mark. That is what a copy is for."
            $ reward_attributes_once("day69_copy_mark", [("insight", "micro")], show="auto")
        "Stay on campus and compare the copies.":
            "We line up the bottom corners against the window. Even the little mark where I rested my pen is the same."
            hikari "You don't have to carry both."
            "She puts hers in her pocket. I put mine away flat."

    scene bg_kitchen_night with walk_fade
    "After dinner Hikari puts her copy beside mine. The creases divide the blue line into three pieces. It's still there."
    if keepsake_observations:
        mc "I went back to see what else was left."
        hikari "Was there anything?"
        mc "Enough to know I hadn't made all of it up."
    else:
        mc "I don't want to take it back to the professor."
        hikari "Then don't. You don't need him to mark it."
    "She puts the torch on the table. The nick in the rim catches on the cloth when she turns it."
    hikari "Tomorrow let's try leaving something where neither of us will touch it."
    mc "Where?"
    "She looks toward the hall. From the table I can see exactly as far as the first stair."

    jump act2_day_router
