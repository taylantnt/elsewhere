default honki_unlocked = False

image bg_honki_outside = bg_or_placeholder("bg_honki_outside", "#26212f", "HONKI!\nROADSIDE BRANCH")
image bg_honki_outside_dusk = bg_or_placeholder("bg_honki_outside_dusk", "#403248", "HONKI!\nSTATION BRANCH")
image bg_honki_inside = bg_or_placeholder("bg_honki_inside", "#42262c", "HONKI!\nINSIDE")

define honki_catalog = (
    ("milk_pudding", "Milk Pudding", 158, "A little cup with a layer of burnt caramel. Good for a late-night snack."),
    ("melon_soda", "Melon Soda", 128, "Bright green, even before you hold it up to the light. Best cold."),
    ("seaweed_chips", "Seaweed Potato Chips", 198, "Salty potato chips dusted with aonori. The bag is bigger than it needs to be."),
    ("peach_gummies", "Peach Gummies", 168, "Soft peach-shaped gummies with a thin coat of sugar."),
    ("miso_noodles", "Instant Miso Noodles", 218, "A quick meal for a night when the kitchen is quiet. Just add hot water."),
    ("rice_crackers", "Soy Rice Crackers", 298, "Individually wrapped crackers. Easy to share without opening the whole bag."),
    ("yuzu_candy", "Yuzu Drops", 238, "A pocket tin of sharp citrus sweets. The lid makes a good snap."),
    ("barley_tea", "Roasted Barley Tea", 118, "Unsweetened and caffeine free. The bottle is narrow enough for a side pocket."),
    ("curry_pouch", "Mild Curry Pouch", 348, "Heat the pouch and pour it over rice. Dinner with only one pan to wash."),
    ("furikake", "Sesame Furikake", 268, "A small shaker of sesame and seaweed for a bowl of plain rice."),
    ("pocket_tissues", "Pocket Tissues", 148, "Four pocket packs. Useful when a cafe napkin isn't quite enough."),
    ("folding_umbrella", "Folding Umbrella", 1190, "A compact umbrella that fits in a school bag. The sleeve never goes back on quite right."),
    ("warm_patches", "Pocket Warmers", 328, "Sealed heat packs you can warm in your coat pocket on a cold platform."),
    ("socks", "Striped Socks", 398, "A spare pair with thin navy stripes. The seam sits flat at the toes."),
    ("sleep_mask", "Sleep Mask", 548, "A soft mask that blocks the glow through the curtains."),
    ("laundry_net", "Laundry Net", 348, "A mesh bag that keeps small things together in the wash."),
    ("travel_bottle", "Travel Bottle", 798, "A small reusable bottle with a screw cap and a loop for your finger."),
    ("notebook", "Grid Notebook", 278, "Squared paper with enough margin for a second thought."),
    ("gel_pen", "Black Gel Pen", 158, "A fine black pen. Good for small writing on cramped handouts."),
    ("sticky_tabs", "Page Tabs", 218, "Five colors of removable tabs to mark pages without folding their corners."),
    ("photo_sleeves", "Photo Sleeves", 448, "Clear sleeves sized for small prints. Keep fingerprints off the picture."),
    ("bag_clip", "Steel Bag Clip", 298, "A little spring clip for an open packet of snacks."),
    ("cable", "Braided USB Cable", 890, "A short charging cable with a woven sleeve. Check the plug before lending it."),
    ("batteries", "AA Batteries", 398, "A set of alkaline batteries for a torch or a stubborn old remote."),
    ("key_torch", "Keyring Torch", 698, "A thumb-sized light for finding a lock without waking the house."),
)

# Register after the base inventory dictionary has been initialized.
init 10 python:
    honki_prices = {}
    for index, (slug, name, price, desc) in enumerate(honki_catalog):
        item_id = "honki_" + slug
        honki_prices[item_id] = price
        item_data[item_id] = {"name": name, "desc": desc, "honki_icon": index}

    def honki_item_icon(index, size):
        crop = ((index % 5) * 96, (index // 5) * 96, 96, 96)
        tile = Transform("images/honki_products.svg", crop=crop)
        return Transform(tile, xysize=(size, size), fit="contain")


label honki_family_trip:
    scene bg_kitchen_night with walk_fade
    father "Is there any milk pudding left?"
    mother "You ate the last one yesterday."
    father "I left one at the back."
    hikari "You ate that one at the back, too."
    "He looks down into the fridge for a little longer."
    father "Well. I'm off tomorrow. We can go to Honki."
    mother "It's nearly midnight."
    father "They're open twenty-four hours. Do we need anything while we're there?"
    "Mother opens the drawer where she keeps the shopping lists. Hikari is already putting on her shoes."

    scene bg_honki_outside with walk_fade
    $ night_street()
    "We drive past a row of shuttered garages. At the next light the car fills with red, and it isn't coming from the light."
    "Father turns in under a sign big enough to read from the other side of the road. There are people coming out with full carts."
    hikari "They sell everything here. Groceries downstairs, suitcases upstairs, chargers wherever you won't think to look."
    hikari "There's a branch by the station, too. You don't need a car for that one."
    mother "We'll put it on your map. You'll want it the next time you forget something."

    scene bg_honki_inside with walk_fade
    "There are handwritten price cards at eye level and boxes stacked above my head. A song keeps coming from somewhere past the rice cookers."
    "I turn a corner expecting another aisle of food and find a wall of umbrellas."
    father "The pudding used to be beside the milk."
    hikari "That was three rearrangements ago."
    mother "I'll get the washing powder. Meet us at the registers when you're done."
    "I take a basket. It's warm where somebody else held the handle."

    $ honki_unlocked = True
    $ phone_map_visit("honki")
    call honki_browse from _call_honki_browse_family

    scene bg_honki_outside with walk_fade
    $ night_street()
    "At the car Father puts a bag on the back seat and tells us not to let it tip."
    hikari "How many did you get?"
    father "Four. One for each of us."
    mother "Then we'll eat them tomorrow."
    "He looks in the rearview mirror. He doesn't start the car until everyone has fastened their seat belt."
    return


label city_row_honki:
    scene bg_honki_outside_dusk with walk_fade
    "The station branch is narrow from the street. Inside, it goes back farther than the row of buildings I passed to get here."
    scene bg_honki_inside with walk_fade
    call honki_browse from _call_honki_browse_city
    return


label honki_browse:
    $ honki_selection = "honki_milk_pudding"
    while True:
        call screen honki_shop(honki_selection)
        if _return == "finish":
            return
        $ honki_selection = _return
        if honki_selection in honki_prices and not has_item(honki_selection):
            $ buy_item(honki_prices[honki_selection], honki_selection)


screen honki_shop(initial_item):
    modal True
    default selected = initial_item
    $ price = honki_prices[selected]
    $ owned = has_item(selected)
    $ affordable = can_afford(price)
    key "game_menu" action Return("finish")
    add Solid("#100d16c4")

    frame:
        style_prefix "honki"
        align (0.5, 0.5)
        xysize (gui.scale(960), gui.scale(630))
        background Solid("#1e1924")
        padding (gui.scale(24), gui.scale(20))

        vbox:
            spacing gui.scale(14)
            frame:
                xfill True
                ysize gui.scale(54)
                background Solid("#492a42")
                padding (gui.scale(14), gui.scale(7))
                fixed:
                    text "HONKI!   /   MARKET" size gui.scale(23) color "#ffcf78" yalign 0.5
                    text ("Cash  " + money_text()) xalign 1.0 yalign 0.5

            hbox:
                spacing gui.scale(18)
                vbox:
                    spacing gui.scale(9)
                    fixed:
                        xysize (gui.scale(510), gui.scale(26))
                        text "PRODUCT" size gui.scale(14) color "#c4a2bb"
                        text "PRICE" size gui.scale(14) color "#c4a2bb" xalign 1.0 xoffset -gui.scale(26)

                    viewport:
                        xysize (gui.scale(510), gui.scale(421))
                        yinitial item_data[initial_item]["honki_icon"] / float(len(honki_catalog) - 1)
                        mousewheel True
                        draggable True
                        scrollbars "vertical"
                        vbox:
                            spacing gui.scale(3)
                            for slug, name, cost, desc in honki_catalog:
                                $ product = "honki_" + slug
                                button:
                                    id product
                                    xfill True
                                    ysize gui.scale(41)
                                    padding (gui.scale(11), 0)
                                    background Solid("#28202f")
                                    hover_background Solid("#493149")
                                    selected_background Solid("#553443")
                                    selected product == selected
                                    action SetScreenVariable("selected", product)
                                    fixed:
                                        text name yalign 0.5
                                        text money_text(cost) color "#ffcf78" xalign 1.0 yalign 0.5

                frame:
                    xysize (gui.scale(384), gui.scale(456))
                    background Solid("#2d2331")
                    padding (gui.scale(20), gui.scale(18))
                    vbox:
                        spacing gui.scale(11)
                        add item_icon(selected, gui.scale(146)) xalign 0.5
                        text item_name(selected) size gui.scale(23) color "#ffcf78"
                        text item_desc(selected) size gui.scale(17) line_spacing gui.scale(4)
                        text ("Already in your bag" if owned else ("Not enough cash" if not affordable else "Adds one to your bag")) size gui.scale(14) color "#c4a2bb"
                        textbutton ("Buy for " + money_text(price)):
                            id "honki_buy"
                            style "honki_checkout"
                            sensitive not owned and affordable
                            action Return(selected)

            textbutton "Finish shopping":
                id "honki_leave"
                style "honki_checkout"
                action Return("finish")
                xalign 1.0


style honki_text is default:
    size gui.scale(17)
    color "#f6ece2"
    outlines []

style honki_checkout is button:
    background Solid("#57394f")
    hover_background Solid("#74495d")
    insensitive_background Solid("#342b38")
    padding (gui.scale(14), gui.scale(8))

style honki_checkout_text is honki_text:
    insensitive_color "#b39da9"
