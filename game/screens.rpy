################################################################################
## Initialization
################################################################################

init offset = -1


################################################################################
## Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## In-game screens
################################################################################


## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None
## if no name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py
## uses this to manage text display. It can also create displayables with
## id "who" and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):

    ## The portrait of whoever is speaking, drawn BEFORE the dialogue plate so it
    ## sits *behind* the textbox. For the main ADV layout we place it in the middle
    ## and scale it up, so the speaker reads more like a Phoenix Wright witness
    ## stand-up than a small side mugshot. It stays anchored to the floor, which
    ## keeps the body grounded behind the textbox instead of hovering awkwardly.
    ## A character appears here by being declared with image="name" and given an
    ## "image side name" picture; anyone without one (the narrator, the MC) shows
    ## nothing. No room for it on the phone variant.
    if not renpy.variant("small"):
        add SideImage() xalign 0.5 ypos config.screen_height yanchor 1.0 zoom 1.8

    window:
        id "window"

        ## A hairline of accent light along the top edge of the dialogue plate,
        ## aligned with the column the text sits in. It ties the textbox to the
        ## same rule that sits under the title on the main menu.
        add Solid(gui.accent_color) xpos gui.dialogue_xpos ypos gui.scale(5) xsize gui.dialogue_width ysize gui.scale(2)

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"


## Make the namebox available for styling through the Character object.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background gui.namebox_background
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False

## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used
## to pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept
## the various input parameters.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the
## menu statement. The one parameter, items, is a list of objects, each
## with caption and action fields.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos gui.scale(270)
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.text_properties("choice_button")


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the
## out-of-game menus.

screen quick_menu():

    ## Ensure this appears on top of other screens.
    zorder 100

    if quick_menu:

        frame:
            style "quick_menu_frame"

            hbox:
                style_prefix "quick"
                style "quick_menu"

                textbutton _("Back") action Rollback()
                textbutton _("History") action ShowMenu('history')
                textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
                textbutton _("Auto") action Preference("auto-forward", "toggle")
                textbutton _("Save") action ShowMenu('save')
                textbutton _("Q.Save") action QuickSave()
                textbutton _("Q.Load") action QuickLoad()
                textbutton _("Bag") action ShowMenu('inventory')
                textbutton _("Prefs") action ShowMenu('preferences')


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_menu_frame is empty
style quick_menu is hbox
style quick_button is default
style quick_button_text is button_text

## The slim bar the quick buttons sit on. It is a translucent near-black chip
## pinned to the bottom of the screen, inside the dialogue plate, so the buttons
## read as part of the textbox rather than floating on the art.
style quick_menu_frame:
    xalign 0.5
    yalign 1.0
    yoffset gui.scale(-4)

    background Solid("#0e0d0cd6")
    padding (gui.scale(26), gui.scale(3), gui.scale(26), gui.scale(3))

style quick_menu:
    spacing gui.scale(20)

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")


## Wallet ######################################################################
##
## A small chip in the top-right corner showing what the protagonist has on him.
## It is an overlay screen, so Ren'Py hides it by itself while a game menu is
## open, and the money it reads is the `money` variable in script.rpy.

screen wallet():

    ## Below the quick menu (100) and well below the confirm prompt (200).
    zorder 90

    if not main_menu:

        frame:
            style "wallet_frame"

            hbox:
                spacing gui.scale(10)

                text _("Cash") style "wallet_label"

                text "¥ [money]" style "wallet_text"


init python:
    ## The cash chip is switched off. The screen above is still fully defined, so
    ## putting the indicator back on screen is this one line and nothing else.
    # config.overlay_screens.append("wallet")
    pass


style wallet_frame is empty
style wallet_label is gui_text
style wallet_symbol is gui_text
style wallet_text is gui_text

style wallet_frame:
    xalign 0.995
    yalign 0.01

    background Solid("#0e0d0ccc")
    padding (gui.scale(18), gui.scale(8), gui.scale(18), gui.scale(8))

style wallet_label:
    size gui.scale(16)
    color "#b9b3a7"
    yalign 0.5

style wallet_symbol:
    size gui.scale(22)
    color gui.accent_color
    yalign 0.5

style wallet_text:
    size gui.scale(22)
    color "#f4efe6"
    yalign 0.5


## Main menu sakura drift #####################################################
##
## Blossoms that keep falling across the title screen for as long as it is open.
## Each one gets its own set of numbers from sakura_petals() below, so no two
## take the same route and the whole thing never visibly comes round again.

init python:

    def sakura_petals(count=30):
        """A fresh bag of blossom routes, one per petal.

        The screen calls this once, through `default`, so the arrangement is
        only decided when the menu opens and then holds still. Opening the menu
        again deals a new one.
        """
        width = config.screen_width
        petals = []

        for _i in range(count):

            fall = renpy.random.uniform(9.0, 17.0)

            petals.append({
                # Where it comes in, and how long the whole descent takes. The
                # spread of fall times is what stops the petals ever marching
                # in step: the fast ones lap the slow ones within a pass or two.
                "x": renpy.random.randint(-40, width + 40),
                "fall": fall,

                # A short head start, so they do not all leave the tree on the
                # same beat when the menu first opens.
                "phase": renpy.random.uniform(0.2, 5.0),

                # How far it wanders sideways, its size, how solid it is, and
                # how far it turns. The turn is a whole number of rotations so
                # that the loop joins up without a visible snap.
                "sway": renpy.random.randint(50, 150) * renpy.random.choice((-1, 1)),
                "size": renpy.random.uniform(0.5, 1.05),
                "fade": renpy.random.uniform(0.4, 0.8),
                "spin": renpy.random.choice((-720.0, -360.0, 360.0, 720.0)),
            })

        return petals


## One blossom. Each block below repeats on its own, forever, and each one sets
## its own starting value first, which is what lets the loop join up cleanly.
transform petal_fall(p):

    subpixel True
    xanchor 0.5
    yanchor 0.5
    zoom p["size"]

    parallel:
        # Wait its turn, drift all the way down, then start again from the top.
        pause p["phase"]
        ypos -90
        linear p["fall"] ypos config.screen_height + 80
        repeat

    parallel:
        # Fades up just after it leaves the top edge, and out again near the
        # floor, so neither end of the journey shows a hard edge.
        pause p["phase"]
        alpha 0.0
        linear 0.9 alpha p["fade"]
        pause p["fall"] - 2.0
        linear 1.1 alpha 0.0
        repeat

    parallel:
        # The breeze: over to the right, back past where it started, home.
        pause p["phase"]
        xpos p["x"]
        ease p["fall"] * 0.3 xpos p["x"] + p["sway"]
        ease p["fall"] * 0.4 xpos p["x"] - p["sway"]
        ease p["fall"] * 0.3 xpos p["x"]
        repeat

    parallel:
        # And a lazy turn as it goes.
        pause p["phase"]
        rotate 0
        linear p["fall"] * 0.55 rotate p["spin"] * 0.55
        linear p["fall"] * 0.45 rotate p["spin"]
        repeat

## The blossom itself. Drawn as art rather than a wingding character: neither of
## the game's fonts carries the ❀/✿ dingbats, so text petals rendered as blank
## space and nothing ever appeared on screen.
image petal = "images/ui/petal.png"

screen sakura_blossoms():

    ## Decided once, when the menu opens, and then left alone. Building the list
    ## inside the loop instead would re-roll every petal on each screen refresh,
    ## which would make them jump around mid-air.
    default petals = sakura_petals()

    for p in petals:
        add "petal" at petal_fall(p)


################################################################################
## Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.5

        spacing gui.navigation_spacing

        if main_menu:

            textbutton _("Start") action Start()

        else:

            textbutton _("History") action ShowMenu("history")

            textbutton _("Save") action ShowMenu("save")

            textbutton _("Bag") action ShowMenu("inventory")

        textbutton _("Load") action ShowMenu("load")

        textbutton _("Preferences") action ShowMenu("preferences")

        if _in_replay:

            textbutton _("End Replay") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Main Menu") action MainMenu()

        textbutton _("About") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## Help isn't necessary or relevant to mobile devices.
            textbutton _("Help") action ShowMenu("help")

        if renpy.variant("pc"):

            ## The quit button is banned on iOS and unnecessary on Android and Web.
            textbutton _("Quit") action Quit(confirm=not main_menu)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.text_properties("navigation_button")


## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():

    ## This ensures that any other menu screen is replaced.
    tag menu

    add gui.main_menu_background
    use sakura_blossoms

    ## This empty frame darkens the main menu.
    frame:
        style "main_menu_frame"

    ## A hairline of accent light down the inner edge of the dark column, so the
    ## title block on the right reads as a panel of its own.
    add Solid(gui.accent_color) xpos gui.scale(280) ypos 0 xsize gui.scale(2) ysize config.screen_height

    ## The use statement includes another screen inside this one. The actual
    ## contents of the main menu are in the navigation screen.
    use navigation

    if gui.show_name:

        vbox:
            style "main_menu_vbox"

            ## Only the version sits here now. The title block used to sit above it,
            ## but the wordmark on the background art carries the name already.
            add Solid(gui.accent_color) xsize gui.scale(240) ysize gui.scale(2) xalign 1.0

            text "[config.version]":
                style "main_menu_version"


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize gui.scale(280)
    yfill True

    background "gui/overlay/main_menu.png"

style main_menu_vbox:
    xalign 1.0
    xoffset gui.scale(-20)
    xmaximum gui.scale(800)
    yalign 1.0
    yoffset gui.scale(-20)

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")


## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid".
## This screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            spacing spacing

                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        spacing spacing

                        transclude

                else:

                    transclude

    ## The same hairline as the main menu, so the two menus feel like one place.
    add Solid(gui.accent_color) xpos gui.scale(280) ypos 0 xsize gui.scale(2) ysize config.screen_height

    use navigation

    textbutton _("Return"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding gui.scale(30)
    top_padding gui.scale(120)

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize gui.scale(280)
    yfill True

style game_menu_content_frame:
    left_margin gui.scale(40)
    right_margin gui.scale(20)
    top_margin gui.scale(10)

style game_menu_viewport:
    xsize gui.scale(920)

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing gui.scale(10)

style game_menu_label:
    xpos gui.scale(50)
    ysize gui.scale(120)

style game_menu_label_text:
    size gui.scale(50)
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset gui.scale(-30)


## About screen ################################################################
##
## This screen gives credit and copyright information about the game and
## Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one.
    ## The vbox child is then included inside the viewport inside the
    ## game_menu screen.
    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            ## gui.about is usually set in options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Inventory screen ############################################################
##
## The protagonist's bag: what he has on hand and what he has picked up. The
## money and the item list themselves live in script.rpy, so this screen only
## has to read them.

screen inventory():

    tag menu

    ## Which slot the player is currently looking at.
    default browsing = 0

    ## Which item is open, if any. Selecting a usable item sets this and the item
    ## is drawn large over the menu; closing it clears the variable again.
    default viewing = None

    use game_menu(_("Bag")):

        style_prefix "inventory"

        if inventory:
            $ current_index = browsing if browsing < len(inventory) else 0
            $ current_item = inventory[current_index]

        vbox:
            spacing gui.scale(18)

            frame:
                style "inventory_money_frame"

                hbox:
                    spacing gui.scale(14)

                    text _("Cash") style "inventory_money_label"
                    text "¥ [money]" style "inventory_money_value"

            if inventory:

                frame:
                    style "inventory_grid_frame"

                    vpgrid:
                        cols 4
                        mousewheel True
                        draggable True
                        spacing gui.scale(14)
                        ymaximum gui.scale(265)

                        for i, item in enumerate(inventory):

                            button:
                                style "inventory_slot_button"
                                action SetScreenVariable("browsing", i)
                                selected (i == current_index)

                                vbox:
                                    xalign 0.5
                                    yalign 0.5
                                    spacing gui.scale(8)

                                    add item_icon(item, gui.scale(94)) xalign 0.5
                                    text item_name(item) style "inventory_slot_name" xalign 0.5

                frame:
                    style "inventory_detail_frame"

                    hbox:
                        spacing gui.scale(24)

                        add item_icon(current_item, gui.scale(150)) yalign 0.5

                        vbox:
                            spacing gui.scale(10)
                            xsize gui.scale(560)

                            text item_name(current_item) style "inventory_item_name"

                            ## A thing he can actually do something with gets a
                            ## button that says what the thing does, not just a
                            ## label saying it is possible. Everything else still
                            ## says so, in red, so the difference is readable at a
                            ## glance.
                            if item_usable(current_item):
                                textbutton item_use_label(current_item) action SetScreenVariable("viewing", current_item) style "inventory_action_button"
                            else:
                                text _("Cannot be used") style "inventory_unusable"

                            null height gui.scale(2)

                            text item_desc(current_item) style "inventory_item_desc"

            else:

                frame:
                    style "inventory_detail_frame"

                    text _("Nothing yet. Everything he owns still fits in his suitcase.") style "inventory_empty_text"

    ## Opening an item. The Bag stays a menu, so the item is drawn large over it
    ## rather than replacing it: the room dims, the thing itself takes the middle
    ## of the screen, and it closes the same way it opened. Anywhere outside the
    ## card closes it too, which is what a person tries first.
    if viewing:

        button:
            style "inventory_dimmer"
            action SetScreenVariable("viewing", None)
            xfill True
            yfill True

            add Solid("#0b0a09e6")

        frame:
            background Solid("#1c1b18f2")
            padding (gui.scale(34), gui.scale(28))
            xalign 0.5
            yalign 0.5

            vbox:
                spacing gui.scale(20)
                xalign 0.5

                text item_name(viewing) style "notice_label" xalign 0.5
                add Solid("#3a352e") xysize (gui.scale(420), 1) xalign 0.5

                add item_icon(viewing, gui.scale(520)) xalign 0.5

                textbutton _("Close") action SetScreenVariable("viewing", None) style "notice_button" xalign 0.5


style inventory_label is label_text
style inventory_text is gui_text
style inventory_money_frame is empty
style inventory_money_label is inventory_text
style inventory_money_value is inventory_text
style inventory_grid_frame is empty
style inventory_detail_frame is empty
style inventory_slot_button is button
style inventory_slot_button_text is gui_text
style inventory_slot_name is inventory_text
style inventory_empty_text is inventory_text

style inventory_label_text:
    size gui.label_text_size

style inventory_text:
    size gui.text_size

style inventory_money_frame:
    background Solid("#11100ecc")
    padding (gui.scale(20), gui.scale(14), gui.scale(20), gui.scale(14))

style inventory_money_label:
    size gui.scale(18)
    color "#b9b3a7"
    yalign 0.5

style inventory_money_value:
    size gui.scale(28)
    color "#f4efe6"
    yalign 0.5

style inventory_grid_frame:
    background Solid("#0f0e0ccc")
    padding (gui.scale(16), gui.scale(16), gui.scale(16), gui.scale(16))

style inventory_detail_frame:
    background Solid("#151310dd")
    padding (gui.scale(22), gui.scale(22), gui.scale(22), gui.scale(22))

style inventory_slot_button:
    xminimum gui.scale(178)
    yminimum gui.scale(156)
    padding (gui.scale(14), gui.scale(14), gui.scale(14), gui.scale(14))
    background Solid("#ffffff08")
    hover_background Solid("#ffffff12")
    selected_idle_background Solid("#c79b5928")
    selected_hover_background Solid("#c79b5938")

## The pocket buttons on the left, and the item panel on the right.
style inventory_button_text is gui_text:
    size gui.scale(24)

style inventory_slot_name:
    size gui.scale(18)
    textalign 0.5
    color "#f0ece3"

style inventory_item_name is inventory_text:
    size gui.scale(30)

style inventory_item_desc is inventory_text:
    size gui.scale(21)
    color "#b9b3a7"

style inventory_usable is inventory_text:
    size gui.scale(20)
    color "#8fd694"

style inventory_unusable is inventory_text:
    size gui.scale(20)
    color "#d68989"

## The dimmer behind an opened item. It is a button so clicking anywhere outside
## the card closes the item, which is what a person tries first, but it carries
## no plate of its own: only the dark.
style inventory_dimmer is button:
    background None
    hover_background None
    padding (0, 0, 0, 0)

## The action button on a usable item, the one that opens it. It reads as a small
## warm plate so it looks like something to press, not another line of caption.
style inventory_action_button is button:
    background Solid("#c79b5926")
    hover_background Solid("#c79b5940")
    padding (gui.scale(20), gui.scale(9), gui.scale(20), gui.scale(9))

style inventory_action_button_text is button_text:
    size gui.scale(20)
    kerning gui.scale(2)
    idle_color "#e8cfa4"
    hover_color "#f4efe6"

style inventory_empty_text:
    size gui.scale(22)
    color "#c6c0b4"


## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and
## load it again. Since they share nearly everything in common, both
## are implemented in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save
## https://www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu

    use file_slots(_("Save"))


screen load():

    tag menu

    use file_slots(_("Load"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter
            ## event before any of the buttons do.
            order_reverse True

            ## The page name, which can be edited by clicking on a button.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            vbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                hbox:
                    xalign 0.5

                    spacing gui.page_spacing

                    textbutton _("<") action FilePagePrevious()
                    key "save_page_prev" action FilePagePrevious()

                    if config.has_autosave:
                        textbutton _("{#auto_page}A") action FilePage("auto")

                    if config.has_quicksave:
                        textbutton _("{#quick_page}Q") action FilePage("quick")

                    ## range(1, 10) gives the numbers from 1 to 9.
                    for page in range(1, 10):
                        textbutton "[page]" action FilePage(page)

                    textbutton _(">") action FilePageNext()
                    key "save_page_next" action FilePageNext()

                if config.has_sync:
                    if CurrentScreenName() == "save":
                        textbutton _("Upload Sync"):
                            action UploadSync()
                            xalign 0.5
                    else:
                        textbutton _("Download Sync"):
                            action DownloadSync()
                            xalign 0.5


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding gui.scale(50)
    ypadding gui.scale(3)
    xalign 0.5

style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.text_properties("slot_button")


## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better
## suit themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu

    use game_menu(_("Preferences"), scroll="viewport"):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        style_prefix "radio"
                        label _("Display")
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "check"
                    label _("Skip")
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                ## Additional vboxes of type "radio_pref" or "check_pref" can be added here, to
                ## add additional creator-defined preferences.

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("Text Speed")

                    bar value Preference("text speed")

                    label _("Auto-Forward Time")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("Music Volume")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Sound Volume")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Voice Volume")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Mute All"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin gui.scale(2)

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize gui.scale(225)

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.text_properties("check_button")

style slider_slider:
    xsize gui.scale(350)

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin gui.scale(10)

style slider_button_text:
    properties gui.text_properties("slider_button")

style slider_vbox:
    xsize gui.scale(450)


## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player.
## While there isn't anything special about this screen, it does have to
## access the dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0, spacing=gui.history_spacing):

        style_prefix "history"

        for h in _history_list:

            window:

                ## This lays things out properly if history_height is None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        ## Take the color of the who text from the Character, if set.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("The dialogue history is empty.")


## This determines what tags are allowed to be displayed on the history
## screen.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Help screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses
## other screens (keyboard_help, mouse_help, and gamepad_help) to display the
## actual help.

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Help"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing gui.scale(15)

            hbox:

                textbutton _("Keyboard") action SetScreenVariable("device", "keyboard")
                textbutton _("Mouse") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Space")
        text _("Advances dialogue without selecting choices.")

    hbox:
        label _("Arrow Keys")
        text _("Navigate the interface.")

    hbox:
        label _("Escape")
        text _("Accesses the game menu.")

    hbox:
        label _("Ctrl")
        text _("Skips dialogue while held down.")

    hbox:
        label _("Tab")
        text _("Toggles dialogue skipping.")

    hbox:
        label _("Page Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Page Down")
        text _("Rolls forward to later dialogue.")

    hbox:
        label "H"
        text _("Hides the user interface.")

    hbox:
        label "S"
        text _("Takes a screenshot.")

    hbox:
        label "V"
        text _("Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}.")

    hbox:
        label "Shift+A"
        text _("Opens the accessibility menu.")


screen mouse_help():

    hbox:
        label _("Left Click")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Middle Click")
        text _("Hides the user interface.")

    hbox:
        label _("Right Click")
        text _("Accesses the game menu.")

    hbox:
        label _("Mouse Wheel Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Mouse Wheel Down")
        text _("Rolls forward to later dialogue.")


screen gamepad_help():

    hbox:
        label _("Right Trigger\nA/Bottom Button")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Left Trigger\nLeft Shoulder")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Right Shoulder")
        text _("Rolls forward to later dialogue.")

    hbox:
        label _("D-Pad, Sticks")
        text _("Navigate the interface.")

    hbox:
        label _("Start, Guide, B/Right Button")
        text _("Accesses the game menu.")

    hbox:
        label _("Y/Top Button")
        text _("Hides the user interface.")

    textbutton _("Calibrate") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin gui.scale(8)

style help_button_text:
    properties gui.text_properties("help_button")

style help_label:
    xsize gui.scale(250)
    right_padding gui.scale(20)

style help_label_text:
    size gui.text_size
    xalign 1.0
    textalign 1.0



################################################################################
## Additional screens
################################################################################


## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or
## no question.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing gui.scale(30)

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing gui.scale(100)

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    ## Right-click and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    textalign 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.text_properties("confirm_button")


## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing gui.scale(6)

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    ## glyph in it.
    font "DejaVuSans.ttf"


## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example,
## when the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Displays dialogue in either a vpgrid or the vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Displays the menu, if given. The menu may be displayed incorrectly
        ## if config.narrator_menu is set to True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## This controls the maximum number of NVL-mode entries that can be displayed
## at once.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.text_properties("nvl_button")


## Bubble screen ###############################################################
##
## The bubble screen is used to display dialogue to the player when using
## speech bubbles. The bubble screen takes the same parameters as the say
## screen, must create a displayable with the id of "what", and can create
## displayables with the "namebox", "who", and "window" ids.
##
## https://www.renpy.org/doc/html/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

        default ctc = None
        showif ctc:
            add ctc

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}



################################################################################
## Mobile Variants
################################################################################

style pref_vbox:
    variant "medium"
    xsize gui.scale(450)

## Since a mouse may not be present, we replace the quick menu with a version
## that uses fewer and bigger buttons that are easier to touch.
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        hbox:
            style "quick_menu"
            style_prefix "quick"

            textbutton _("Back") action Rollback()
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Bag") action ShowMenu('inventory')
            textbutton _("Menu") action ShowMenu()


style window:
    variant "small"
    background "gui/phone/textbox.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize gui.scale(340)

style game_menu_content_frame:
    variant "small"
    top_margin 0

style game_menu_viewport:
    variant "small"
    xsize gui.scale(870)

style pref_vbox:
    variant "small"
    xsize gui.scale(400)

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize gui.scale(600)
