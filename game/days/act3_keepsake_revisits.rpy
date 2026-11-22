default keepsake_observations = {}

label act3_revisit_circle:
    scene bg_photo_club_closed with walk_fade
    "The door is open the width of a shoe. Inside, the prints are standing on their edges in cardboard boxes. Somebody has written PORTRAITS on three of them."
    "I take Sim's strap out of my bag. There's a little twist in it he never bothered to straighten. I look for it in the prints before I look for his face."
    "In TT's portrait, the strap runs down the side of an empty chair. On the back, in pencil: SIM, BEFORE THE SPEECH."
    menu:
        "Look for another copy.":
            "There are two more prints in the sleeve. I hold them up against each other. The chair is empty in both."
        "Turn it over and leave it for Circle.":
            "I put it back with the writing facing up. The next person who opens the box will see his name first."
    $ keepsake_observations["sim_camera_strap"] = "TT's portrait still has Sim's name on the back. There is an empty chair where he should be."
    return

label act3_revisit_lupins:
    scene bg_lupins_alley_night_closed with walk_fade
    "There's a sign on the door, but all it says is that the place is closed. Above it, two chains hang from an empty bracket."
    if has_item("orson_wolf_paw_badge"):
        $ orson_keepsake = "orson_wolf_paw_badge"
        "I turn the badge over. The pin is bent where I'd tried to get it through my coat on the way home."
    else:
        $ orson_keepsake = "orson_wolf_coaster"
        "I take out the coaster. The bottom edge has gone soft from the glass he set on it."
    "In the window there's a paper listing for the space. Under previous use it says storage. I read down to the date. It covers the entire time I've been here."
    menu:
        "Take a picture of the listing.":
            "The first photo catches my reflection. I move to one side and take it again. I leave the first one on my phone too."
        "Leave it where it is.":
            "I sit on the step for a minute. The smell from two doors down hasn't changed."
    $ keepsake_observations[orson_keepsake] = "The wolf sign is gone. The listing says the room was used for storage while I was drinking there."
    return

label act3_revisit_hana:
    scene bg_library with walk_fade
    "The fan still knocks once when it turns toward the shelves. I wait for it to do it again while I open the volunteer binder."
    "On the page from April there are two staple holes and a pale rectangle where a name was covered. I keep my thumb on the edge of the page."
    quiet_student "Are you looking for something?"
    menu:
        "Ask about Hana.":
            mc "Do you remember Hana? She used to sit here."
            quiet_student "I remember you waiting for somebody. I thought you liked the table."
        "Show her the charm.":
            "The charm catches on the zipper of my bag. I undo it and lay it on the binder."
            quiet_student "That's nice. Did you make it?"
            mc "No. A friend did."
    "I close the binder before I can start looking for my own name."
    $ keepsake_observations["hana_art_charm"] = "There is a pale rectangle in the April volunteer record where a name should be. Hana's stitches are still on the charm."
    return

label act3_revisit_aya:
    scene bg_maidcafe with walk_fade
    "The bell sounds as I come in. There's an omurice at the window table before I've ordered. The cat has one ear that leans in."
    new_maid "I started doing the ears like that. People seem to like it."
    "The cat in the sketch Aya gave me has the same ear. I look at the folded corner of the paper."
    menu:
        "Show her Aya's sketch.":
            "She looks from the paper to the plate."
            new_maid "I don't remember seeing that before."
            "She sounds sorry. I fold it up before she can apologise for anything else."
        "Keep the sketch in your bag.":
            "I order tea. I eat the rice from the other side and leave the ear until last."
    $ keepsake_observations["aya_sketchbook_page"] = "The new maid says the crooked ear was her idea. Aya drew it that way on the page she gave me."
    return
