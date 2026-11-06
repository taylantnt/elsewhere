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
    if not renpy.variant("small") and not standalone_window_active():
        add SideImage() xalign 0.5 ypos config.screen_height yanchor 1.0 zoom 1.8

    window:
        id "window"
        at Transform(alpha=0.0 if standalone_window_active() else 1.0)

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

    # Keep the most recent spoken line on screen while the answers are visible,
    # so a choice reads like a reply to the conversation rather than a detached
    # list floating in the middle of the scene.
    $ last_line = renpy.last_say()

    if last_line and last_line.what:

        window:
            style "choice_prompt_window"

            add Solid(gui.accent_color) xpos gui.dialogue_xpos ypos gui.scale(5) xsize gui.dialogue_width ysize gui.scale(2)

            text last_line.what style "choice_prompt_text"

    vbox:
        for i in items:
            textbutton i.caption action i.action


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text
style choice_prompt_window is window
style choice_prompt_text is say_dialogue

style choice_vbox:
    xalign 0.5
    ypos gui.scale(270)
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

    ## The hovered choice keeps the dark plate of the idle one and simply lifts
    ## it a shade, while the text switches to the accent. The amber plate it
    ## used to swap in put near-black text on a mid-tone fill, which is what
    ## made the hover hard to read.
    ##
    ## There is no insensitive art in gui/button, so a locked answer used to fall
    ## back to the idle plate with dim text and read as selectable. It gets its
    ## own recessed chip instead, so a closed door looks closed.
    hover_background Solid("#3d362bf0")
    insensitive_background Solid("#100f0dcc")

style choice_button_text is default:
    properties gui.text_properties("choice_button")

style choice_prompt_window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style choice_prompt_text:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the
## out-of-game menus.

screen quick_menu():

    ## Ensure this appears on top of other screens.
    zorder 100

    if quick_menu and not standalone_window_active():

        frame:
            style "quick_menu_frame"

            hbox:
                style_prefix "quick"
                style "quick_menu"

                textbutton _("Back") action Rollback()
                textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
                textbutton _("Auto") action Preference("auto-forward", "toggle")
                textbutton _("Q.Save") action QuickSave()
                textbutton _("Q.Load") action QuickLoad()
                if wire_unlocked:
                    textbutton _("WIRE") action Function(wire_open)
                textbutton _("Phone") action Function(apps_open)

        key "game_menu" action Function(apps_open)


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
##
## attribute_hud rides along with it. It is the three orbs in the corner that fill
## as he grows, and it is registered here rather than in script.rpy so that every
## always-on overlay the game has is declared in one place. Like the quick menu it
## is hidden by Ren'Py itself while a game menu is open, and the screen carries its
## own switch (`show_attribute_hud`) so it can stay off through the disclaimer
## cards at the start of the game.
init python:
    config.overlay_screens.append("quick_menu")
    config.overlay_screens.append("attribute_hud")

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

    import math
    import random
    import time

    def sakura_petals(count=84):
        """Independent small and medium petals, already spread through the sky."""
        width = config.screen_width
        rng = random.Random()
        petals = []

        for _i in range(count):
            small = _i % 3 != 0
            fall = rng.uniform(11.0, 23.0) if small else rng.uniform(8.0, 18.0)
            petals.append({
                "x": rng.uniform(-60, width + 60),
                "fall": fall,
                "phase": rng.uniform(0.0, fall),
                "sway": rng.uniform(12.0, 40.0),
                "sway_period": rng.uniform(3.0, 7.0),
                "drift": rng.uniform(-5.0, 14.0),
                "size": rng.uniform(0.14, 0.32) if small else rng.uniform(0.34, 0.58),
                "fade": rng.uniform(0.35, 0.70),
                "spin": rng.uniform(12.0, 48.0) * rng.choice((-1, 1)),
                "wind_response": rng.uniform(1.0, 1.45) if small else rng.uniform(0.65, 1.0),
            })
        return petals

    def sakura_field():
        # Session-only weather keeps moving through menu changes without touching
        # saves or consuming the story's rollback-aware random number stream.
        field = renpy.session.get("menu_sakura_field")
        if field is None:
            rng = random.Random()
            gusts = []
            cursor = 0.0
            for _i in range(4):
                cursor += rng.uniform(11.0, 19.0)
                duration = rng.uniform(3.5, 6.5)
                gusts.append((cursor, duration, rng.uniform(110.0, 210.0) * rng.choice((-1, 1))))
                cursor += duration
            field = {
                "started_at": time.monotonic(),
                "petals": sakura_petals(),
                "gusts": gusts,
                "period": cursor + 12.0,
            }
            renpy.session["menu_sakura_field"] = field
        return field

    def sakura_wind(elapsed, field):
        cycle, local = divmod(elapsed, field["period"])
        displacement = cycle * sum(gust[2] for gust in field["gusts"])
        for start, duration, strength in field["gusts"]:
            progress = min(1.0, max(0.0, (local - start) / duration))
            displacement += strength * (0.5 - 0.5 * math.cos(math.pi * progress))
        return displacement

    def sakura_motion(trans, st, at, p, field):
        elapsed = time.monotonic() - field["started_at"]
        progress = ((elapsed + p["phase"]) % p["fall"]) / p["fall"]
        sway = p["sway"] * math.sin((elapsed + p["phase"]) * 2.0 * math.pi / p["sway_period"])
        horizontal = p["x"] + p["drift"] * elapsed + sway + sakura_wind(elapsed, field) * p["wind_response"]
        # Float positions are relative in Ren'Py; these coordinates are pixels.
        trans.xpos = int(horizontal % (config.screen_width + 120) - 60)
        trans.ypos = int(-90 + progress * (config.screen_height + 180))
        trans.rotate = (elapsed + p["phase"]) * p["spin"] % 360
        trans.alpha = p["fade"] * min(1.0, progress / 0.10, (1.0 - progress) / 0.12)
        return 0.0


transform petal_fall(p, field):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    zoom p["size"]
    function renpy.curry(sakura_motion)(p=p, field=field)

## The blossom itself. Drawn as art rather than a wingding character: neither of
## the game's fonts carries the ❀/✿ dingbats, so text petals rendered as blank
## space and nothing ever appeared on screen.
image petal = "images/ui/petal.png"

screen sakura_blossoms():

    default field = sakura_field()

    for p in field["petals"]:
        add "petal" at petal_fall(p, field)


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

        xpos gui.scale(34 if renpy.variant("small") else 74)
        ypos gui.scale(76)
        spacing gui.scale(5)

        if main_menu:

            text "ELSEWHERE":
                style "menu_nav_brand"

            text _("TITLE SCREEN"):
                style "menu_nav_section"

            textbutton _("New Story") action MenuStart()
            textbutton _("Continue") action MenuContinue()

        else:

            text "ELSEWHERE":
                style "menu_nav_brand"

            text _("IN THIS STORY"):
                style "menu_nav_section"

            textbutton _("History") action ShowMenu("history")

            textbutton _("Save") action ShowMenu("save")

            textbutton _("Bag") action ShowMenu("inventory")

            textbutton _("Attributes") action ShowMenu("attributes")

        textbutton _("Load Game") action MenuLoad()

        textbutton _("Settings") action ShowMenu("preferences")

        if _in_replay:

            textbutton _("End Replay") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Title Screen") action MainMenu()

        textbutton _("About") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## Help isn't necessary or relevant to mobile devices.
            textbutton _("Help") action ShowMenu("help")

        if renpy.variant("pc"):

            ## The quit button is banned on iOS and unnecessary on Android and Web.
            textbutton _("Quit") action Quit(confirm=True)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    properties gui.button_properties("navigation_button")
    background Solid("#ffffff08")
    hover_background Solid("#e8a9c222")
    insensitive_background Solid("#ffffff04")
    xfill True
    padding (gui.scale(12), gui.scale(8))

style navigation_button_text:
    properties gui.text_properties("navigation_button")
    size gui.scale(19)
    color "#d7dce7"
    hover_color "#fff1e2"
    selected_color gui.accent_color
    hover_underline False
    xalign 0.0

style menu_nav_brand is gui_text
style menu_nav_section is gui_text

style menu_nav_brand:
    font "DejaVuSans.ttf"
    size gui.scale(22)
    bold True
    color "#fff5e8"
    kerning gui.scale(1)
    bottom_margin gui.scale(12)

style menu_nav_section:
    font gui.interface_text_font
    size gui.scale(11)
    color "#dfa8c0"
    kerning gui.scale(1)
    bottom_margin gui.scale(6)


## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():

    tag menu
    use phone_title


transform title_phone_enter:
    alpha 0.0
    zoom 0.9
    yoffset gui.scale(35)
    easeout 0.62 alpha 1.0 zoom 1.0 yoffset 0


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

style title_start_button is button
style title_start_text is gui_text
style title_start_arrow is gui_text
style title_phone_status is gui_text
style title_phone_back_button is button
style title_phone_brand is gui_text
style title_phone_heading is gui_text
style title_phone_subheading is gui_text
style title_phone_menu_button is button
style title_phone_menu_marker is gui_text
style title_phone_menu_title is gui_text
style title_phone_menu_detail is gui_text
style title_phone_footer is gui_text

style title_start_button:
    background Solid("#0b1425dd")
    hover_background Solid("#1b2940ed")
    padding (gui.scale(18), gui.scale(12))
    xalign 0.0
    yalign 0.0

style title_start_text:
    font "DejaVuSans.ttf"
    size gui.scale(20)
    bold True
    color "#fff5e8"
    kerning gui.scale(1)
    yalign 0.5

style title_start_arrow:
    font "DejaVuSans.ttf"
    size gui.scale(34)
    color gui.accent_color
    yalign 0.42

style title_phone_status:
    font "DejaVuSans.ttf"
    size gui.scale(9)
    color "#f5f7fb"
    yalign 0.5

style title_phone_back_button:
    background Solid("#ffffff14")
    hover_background Solid("#ffffff30")
    padding (gui.scale(4), gui.scale(0))
    xsize gui.scale(24)
    ysize gui.scale(24)

style title_phone_back_button_text:
    font "DejaVuSans.ttf"
    size gui.scale(22)
    color "#f4f4fa"
    yalign 0.5
    xalign 0.5

style title_phone_brand:
    font "DejaVuSans.ttf"
    size gui.scale(14)
    bold True
    color "#f5f7fb"
    kerning gui.scale(1)

style title_phone_heading:
    font gui.interface_text_font
    size gui.scale(19)
    color "#fff5e8"

style title_phone_subheading:
    font gui.interface_text_font
    size gui.scale(12)
    color "#b7c5d8"

style title_phone_menu_button:
    background Solid("#ffffff0b")
    hover_background Solid("#e8a9c233")
    insensitive_background Solid("#ffffff05")
    padding (gui.scale(9), gui.scale(4))

style title_phone_menu_marker:
    font "DejaVuSans.ttf"
    size gui.scale(22)
    yalign 0.5

style title_phone_menu_title:
    font gui.interface_text_font
    size gui.scale(14)
    color "#f6f3f5"

style title_phone_menu_detail:
    font gui.interface_text_font
    size gui.scale(9)
    color "#b5c0d0"

style title_phone_footer:
    font "DejaVuSans.ttf"
    size gui.scale(8)
    color "#8c9fb4"
    xalign 0.5


## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid".
## This screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    use phone_game_menu(title, scroll, yinitial, spacing):
        transclude


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
    xsize gui.scale(1200)
    ysize gui.scale(670)
    xalign 0.5
    yalign 0.5
    padding (gui.scale(22), gui.scale(22))
    background Solid("#0a1422e8")

style game_menu_navigation_frame:
    xsize gui.scale(230)
    yfill True
    background Solid("#121f30")
    padding (gui.scale(10), gui.scale(16))

style game_menu_content_frame:
    left_margin gui.scale(20)
    right_margin gui.scale(4)
    top_margin gui.scale(16)
    bottom_margin gui.scale(8)
    xfill True
    yfill True
    background Solid("#101a28d9")
    padding (gui.scale(24), gui.scale(18))

style game_menu_viewport:
    xfill True
    yfill True

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing gui.scale(10)

style game_menu_label:
    xpos gui.scale(300)
    ypos gui.scale(32)
    ysize gui.scale(64)

style game_menu_label_text:
    size gui.scale(34)
    color "#f4d6e2"
    yalign 0.5

style return_button:
    xpos gui.scale(42)
    yalign 1.0
    yoffset gui.scale(-34)
    xsize gui.scale(190)


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
    use phone_inventory


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


## Attributes ##################################################################
##
## The three pillars, read from the same definitions the gain card and the corner
## cluster use, so the three of them can never disagree about which orb is which
## or what a rank is called.
##
## Two different measures of progress appear on each row, and the difference is
## deliberate:
##
##   the orb  — how solid this pillar has become across the whole ladder. It only
##              ever fills, so reaching a new rank never looks like a reset.
##   the bar  — how far through the *current* rank he is, so the ladder reads as
##              rungs, and each rung can be watched filling on its own.

screen attributes():

    tag menu
    use phone_attributes


style attributes_intro is gui_text:
    size gui.scale(17)
    color "#c5cdd4"
    xmaximum gui.scale(720)

style attributes_kicker is gui_text:
    size gui.scale(12)
    color "#8796a2"
    kerning gui.scale(3)

style attributes_row is frame:
    background Solid("#111820e8")
    padding (gui.scale(20), gui.scale(14), gui.scale(20), gui.scale(14))

style attributes_bar is bar:
    left_bar Solid("#ffffff")
    right_bar Solid("#ffffff14")

style attributes_name is gui_text:
    size gui.scale(27)
    kerning gui.scale(2)

style attributes_rank is gui_text:
    size gui.scale(13)
    color "#d7dfe5"
    kerning gui.scale(1)
    yalign 0.5

style attributes_blurb is gui_text:
    size gui.scale(17)
    color "#a7b1ba"

style attributes_next is gui_text:
    size gui.scale(14)
    color "#d2dbe2"

style attributes_total is gui_text:
    size gui.scale(12)
    color "#788691"
    kerning gui.scale(1)


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

    use file_slots(_("Load Game"))


screen file_slots(title):

    use phone_files(title)


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
    background Solid("#17263a")

style page_label_text:
    textalign 0.5
    layout "subtitle"
    color "#f2edf1"
    hover_color gui.accent_color

style page_button:
    background Solid("#ffffff08")
    hover_background Solid("#e8a9c222")
    selected_background Solid("#e8a9c233")
    padding (gui.scale(10), gui.scale(6))

style page_button_text:
    properties gui.text_properties("page_button")
    color "#d7dce7"
    hover_color "#fff1e2"
    selected_color gui.accent_color

style slot_button:
    background Solid("#17263a")
    hover_background Solid("#263a53")
    selected_background Solid("#263a53")
    padding (gui.scale(8), gui.scale(8))
    xsize gui.slot_button_width
    ysize gui.slot_button_height

style slot_button_text:
    font gui.interface_text_font
    size gui.scale(13)
    color "#e8eaf0"
    xalign 0.5

style slot_time_text:
    font gui.interface_text_font
    size gui.scale(11)
    color "#a6b1c2"
    xalign 0.5

style slot_name_text:
    font gui.interface_text_font
    size gui.scale(14)
    color "#fff5e8"
    xalign 0.5


## Options screen ##########################################################
##
## The options screen allows the player to configure the game to better
## suit themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu
    use phone_preferences


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
    color "#f0d2df"
    size gui.scale(18)

style pref_vbox:
    xsize gui.scale(225)

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    background Solid("#ffffff08")
    hover_background Solid("#e8a9c222")
    selected_background Solid("#e8a9c233")
    padding (gui.scale(10), gui.scale(6))
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.text_properties("radio_button")
    color "#d7dce7"
    hover_color "#fff1e2"
    selected_color gui.accent_color

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    background Solid("#ffffff08")
    hover_background Solid("#e8a9c222")
    selected_background Solid("#e8a9c233")
    padding (gui.scale(10), gui.scale(6))
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.text_properties("check_button")
    color "#d7dce7"
    hover_color "#fff1e2"
    selected_color gui.accent_color

style slider_slider:
    xsize gui.scale(350)
    left_bar Solid(gui.accent_color)
    right_bar Solid("#ffffff25")

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

    use game_menu(_("Log"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0, spacing=gui.history_spacing):

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
    use phone_help


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

    use phone_confirm(message, yes_action, no_action)

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

    if quick_menu and not standalone_window_active():

        hbox:
            style "quick_menu"
            style_prefix "quick"

            textbutton _("Back") action Rollback()
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            if wire_unlocked:
                textbutton _("WIRE") action Function(wire_open)
            textbutton _("Phone") action Function(apps_open)

        key "game_menu" action Function(apps_open)


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
    xsize config.screen_width - gui.scale(24)
    ysize config.screen_height - gui.scale(24)
    padding (gui.scale(12), gui.scale(12))
    background Solid("#0a1422e8")

style game_menu_navigation_frame:
    variant "small"
    xsize gui.scale(180)
    yfill True
    padding (gui.scale(6), gui.scale(10))

style game_menu_content_frame:
    variant "small"
    left_margin gui.scale(10)
    right_margin gui.scale(2)
    xfill True
    yfill True
    padding (gui.scale(12), gui.scale(10))

style game_menu_label:
    variant "small"
    xpos gui.scale(205)
    ypos gui.scale(15)

style return_button:
    variant "small"
    xpos gui.scale(18)
    xsize gui.scale(150)

style game_menu_viewport:
    variant "small"
    xfill True
    yfill True

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
