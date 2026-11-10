################################################################################
## CAMERA
##
## The camera arrives with Sim. Before Circle, this is not a camera: S does
## nothing, and the Camera app says so. After Circle, S photographs the frame
## the player is looking at - the scene and the dialogue, never the phone - and
## the Camera app becomes the roll of film: every shot taken, newest first,
## each one opening full screen when tapped.
##
## Why it is built this way:
##   * Ren'Py's own S binding writes a screenshot of whatever is on screen,
##     phone included. `config.keymap["screenshot"] = []` turns that binding
##     off; `camera_hotkey` replaces it with one that only exists after the
##     story has handed him a camera.
##   * The phone opens in its own context and clears the screens layer, so a
##     shot taken from inside it would have no dialogue and a phone in frame.
##     The shutter therefore closes the phone first and takes the photo from
##     the game context, where the say screen still is.
################################################################################

default camera_unlocked = False
default camera_photo_count = 0
default camera_photos = []
default camera_viewer_index = 0
default camera_shot_requested = False

define hint_text_camera = (
    "You have a camera now. Press S at any time to take a photo of the game, "
    "or open the Camera app on your phone and press the shutter.\n\n"
    "The photo keeps the scene and the dialogue exactly as they are on screen, "
    "but never the phone. Every shot is kept in the Camera app, and the files "
    "are saved as PNGs in the game's screenshots folder."
)


init python:
    import os
    import struct

    # Ren'Py's default S binding saves whatever is on screen, phone included.
    # Emptying it turns the binding off. camera_hotkey below replaces it.
    config.keymap["screenshot"] = []

    config.always_shown_screens.append("camera_hotkey")

    # The roll of film is bounded so a long play session cannot bloat a save
    # with thumbnails. The PNGs themselves stay on disk either way.
    camera_gallery_limit = 40
    camera_thumb_size = (160, 90)

    def camera_photo_folder():
        """Where the PNGs live. Somewhere the player can actually find."""
        if renpy.macapp:
            return os.path.expanduser("~/Desktop")

        # Beside the game folder, never inside it: a screenshot is not a game
        # asset, and it must not end up in a distribution build.
        return os.path.join(os.path.dirname(os.path.normpath(config.gamedir)), "screenshots")

    def camera_photo_folder_label():
        if renpy.macapp:
            return "Desktop"

        return "screenshots/"

    def camera_photo_path():
        """The next free screenshot path, in the camera's own folder."""
        dest = camera_photo_folder()

        try:
            os.makedirs(dest, exist_ok=True)
        except Exception:
            pass

        pattern = getattr(store, "_screenshot_pattern", None) or config.screenshot_pattern

        index = 1
        while True:
            path = os.path.join(dest, pattern % index)
            if not os.path.exists(path):
                return path
            index += 1

    def camera_take_photo():
        """Photograph the frame the player is looking at. No phone in the shot."""
        if not store.camera_unlocked:
            return False

        path = camera_photo_path()

        if not renpy.screenshot(path):
            renpy.notify("The photo did not save.")
            return False

        try:
            thumb = renpy.screenshot_to_bytes(store.camera_thumb_size)
        except Exception:
            thumb = None

        store.camera_photo_count += 1
        store.camera_photos.append({
            "name": os.path.basename(path),
            "path": path,
            "thumb": thumb,
        })

        while len(store.camera_photos) > store.camera_gallery_limit:
            del store.camera_photos[0]

        play_sfx("audio/SFX/camera_shutter.wav")
        return True

    def camera_thumb_source(entry):
        """A small image for the grid, falling back to the full file."""
        thumb = entry.get("thumb")

        if thumb:
            return renpy.display.im.Data(thumb, "camera_thumb.png"), 160, 90

        return camera_photo_source(entry)

    def camera_photo_source(entry):
        """The full-size image for the viewer, with the thumbnail as fallback."""
        path = entry.get("path")

        try:
            with open(path, "rb") as f:
                data = f.read()

            if len(data) > 24 and data[:8] == b"\x89PNG\r\n\x1a\n":
                width, height = struct.unpack(">II", data[16:24])
                return renpy.display.im.Data(data, os.path.basename(path)), width, height
        except Exception:
            pass

        thumb = entry.get("thumb")

        if thumb:
            return renpy.display.im.Data(thumb, "camera_thumb.png"), 160, 90

        return Solid("#111111"), 1, 1

    def camera_unlock():
        """Hand him the camera, once, with the card that explains it."""
        if store.camera_unlocked:
            return False

        store.camera_unlocked = True
        renpy.call_screen("hint_card", eyebrow="Camera", body=store.hint_text_camera)
        return True

    # A save made before the camera existed may already be past Circle. Those
    # players get the camera quietly; replaying the card at a scene they have
    # already left would be worse than not seeing it.
    def _camera_after_load():
        # A save from before the gallery existed still has its PNGs on disk.
        # Adopt them so the roll is not empty behind a non-zero photo count.
        if not store.camera_photos:
            folder = camera_photo_folder()

            try:
                names = sorted(
                    name for name in os.listdir(folder)
                    if name.startswith("screenshot") and name.endswith(".png")
                )
            except Exception:
                names = []

            for name in names[-store.camera_gallery_limit:]:
                store.camera_photos.append({
                    "name": name,
                    "path": os.path.join(folder, name),
                    "thumb": None,
                })

            if store.camera_photos:
                store.camera_photo_count = max(store.camera_photo_count, len(store.camera_photos))

        if store.camera_unlocked:
            return

        if getattr(store, "confidant_visits", {}).get("sim", 0) > 0:
            store.camera_unlocked = True

    config.after_load_callbacks.append(_camera_after_load)

    def camera_hotkey():
        """S. Quiet until the camera exists, and never inside a window."""
        if not store.camera_unlocked:
            return

        if getattr(store, "main_menu", False):
            return

        # Only the story is photographable. The phone, WIRE, the game menu and
        # the notice cards all run in their own context, and none of them
        # belongs in a photo.
        if len(renpy.game.contexts) != 1:
            return

        if standalone_window_active():
            return

        camera_take_photo()


screen camera_hotkey():
    key "K_s" action Function(camera_hotkey)


## The shutter closes the phone first, so the photo has none of it in frame.
## _clear_layers=False is what keeps the dialogue box: the phone cleared the
## screens layer when it opened, and this context puts the frame back.
label _camera_capture_after_phone:
    # modal=False: a timed pause holds forever while a modal screen is up, and
    # the shutter must never deadlock behind one.
    $ renpy.pause(0.05, hard=True, modal=False)
    $ camera_take_photo()
    return


################################################################################
## THE CAMERA APP
################################################################################

screen phone_app_camera_contents():
    $ camera_content_w = gui.scale(menu_phone_content_w)
    $ camera_folder_label = camera_photo_folder_label()

    if not camera_unlocked:
        vbox:
            xalign 0.5
            yalign 0.5
            spacing gui.scale(12)
            use phone_app_icon("camera", 72, True)
            text "NOT AVAILABLE YET":
                xalign 0.5
                size gui.scale(14)
                kerning gui.scale(1)
                color "#dce4e8"
                outlines []
            text "The camera is not available yet.":
                xalign 0.5
                textalign 0.5
                xmaximum gui.scale(205)
                size gui.scale(13)
                color "#83909a"
                outlines []
    else:
        fixed:
            xysize (camera_content_w, gui.scale(474))

            text "PHOTOS  [camera_photo_count]":
                xpos gui.scale(4)
                ypos gui.scale(2)
                size gui.scale(10)
                kerning gui.scale(1)
                color "#83909a"
                outlines []

            if camera_photos:
                text "TAP A PHOTO TO VIEW":
                    xalign 1.0
                    xoffset gui.scale(-4)
                    ypos gui.scale(2)
                    size gui.scale(9)
                    kerning gui.scale(1)
                    color "#5c6a74"
                    outlines []

                viewport:
                    xpos gui.scale(2)
                    ypos gui.scale(22)
                    xysize (camera_content_w - gui.scale(4), gui.scale(360))
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    vscrollbar_xsize gui.scale(3)
                    vscrollbar_base_bar Solid("#ffffff10")
                    vscrollbar_thumb Solid("#c8a06a66")
                    vscrollbar_unscrollable "hide"

                    vpgrid:
                        cols 3
                        spacing gui.scale(5)
                        xalign 0.5

                        # Newest first: the shot the player just took is the
                        # one they want to see.
                        for i in range(len(camera_photos) - 1, -1, -1):
                            button:
                                xysize (gui.scale(68), gui.scale(38))
                                background Solid("#0a1218")
                                hover_background Solid("#c8a06a55")
                                action [
                                    SetVariable("camera_viewer_index", i),
                                    Show("camera_photo_viewer"),
                                ]

                                $ thumb_source, thumb_w, thumb_h = camera_thumb_source(camera_photos[i])
                                $ thumb_zoom = min(gui.scale(68) / float(thumb_w), gui.scale(38) / float(thumb_h))
                                add Transform(
                                    thumb_source,
                                    zoom=thumb_zoom,
                                    xalign=0.5,
                                    yalign=0.5,
                                )
            else:
                vbox:
                    xalign 0.5
                    ypos gui.scale(130)
                    spacing gui.scale(10)
                    text "NO PHOTOS YET":
                        xalign 0.5
                        size gui.scale(12)
                        kerning gui.scale(1)
                        color "#5c6a74"
                        outlines []
                    text "Press S during the story, or use the shutter below.":
                        xalign 0.5
                        textalign 0.5
                        xmaximum gui.scale(196)
                        size gui.scale(11)
                        color "#6f7d87"
                        outlines []

            textbutton "TAKE PHOTO":
                style "phone_option"
                xalign 0.5
                ypos gui.scale(398)
                xsize gui.scale(150)
                action Return("camera_shot")

            text "SAVED TO  [camera_folder_label]":
                xalign 0.5
                ypos gui.scale(444)
                size gui.scale(9)
                kerning gui.scale(1)
                color "#4f5b64"
                outlines []


## A photo, full screen, with the rest of the roll either side of it.
screen camera_photo_viewer():
    modal True
    zorder 200

    $ viewer_total = len(camera_photos)
    $ viewer_position = camera_viewer_index + 1
    $ viewer_entry = camera_photos[camera_viewer_index]
    $ viewer_source, viewer_w, viewer_h = camera_photo_source(viewer_entry)
    $ viewer_zoom = min(
        (config.screen_width - gui.scale(120)) / float(viewer_w),
        (config.screen_height - gui.scale(120)) / float(viewer_h),
    )

    fixed:
        xysize (config.screen_width, config.screen_height)

        # Tapping the backdrop closes the viewer.
        button:
            xysize (config.screen_width, config.screen_height)
            background Solid("#000000")
            action Hide("camera_photo_viewer")

        add Transform(viewer_source, zoom=viewer_zoom, xalign=0.5, yalign=0.5)

        text "[viewer_position] / [viewer_total]":
            xalign 0.5
            ypos gui.scale(22)
            size gui.scale(13)
            kerning gui.scale(2)
            color "#c8c2b8"
            outlines []

        text viewer_entry["name"]:
            xalign 0.5
            ypos config.screen_height - gui.scale(34)
            size gui.scale(10)
            color "#6f7d87"
            outlines []

        textbutton "CLOSE":
            style "phone_small_button"
            xalign 1.0
            xoffset gui.scale(-28)
            ypos gui.scale(18)
            text_size gui.scale(13)
            action Hide("camera_photo_viewer")

        if camera_viewer_index > 0:
            textbutton "‹":
                style "phone_small_button"
                xpos gui.scale(20)
                yalign 0.5
                text_size gui.scale(34)
                action SetVariable("camera_viewer_index", camera_viewer_index - 1)

        if camera_viewer_index < viewer_total - 1:
            textbutton "›":
                style "phone_small_button"
                xalign 1.0
                xoffset gui.scale(-20)
                yalign 0.5
                text_size gui.scale(34)
                action SetVariable("camera_viewer_index", camera_viewer_index + 1)

    key "game_menu" action Hide("camera_photo_viewer")
    key "K_ESCAPE" action Hide("camera_photo_viewer")
    key "K_LEFT" action If(
        camera_viewer_index > 0,
        SetVariable("camera_viewer_index", camera_viewer_index - 1),
        NullAction(),
    )
    key "K_RIGHT" action If(
        camera_viewer_index < viewer_total - 1,
        SetVariable("camera_viewer_index", camera_viewer_index + 1),
        NullAction(),
    )
