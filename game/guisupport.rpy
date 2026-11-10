init -100 python in gui:

    def scale(n):
        return int(n)

init 100 python in gui:

    if not renpy.mobile:
        from store import config

        import sys
        import os
        sys.path.insert(0, os.path.join(config.renpy_base, "launcher", "game"))

        # launcher/game only exists inside the SDK. In a built distribution the
        # generated gui/ images are already in the game directory, so skip
        # regeneration there instead of dying on the import.
        try:
            from gui7.parameters import GuiParameters
            from gui7.images import ImageGenerator
            from gui7 import generate_gui
        except ImportError:
            pass
        else:
            p = GuiParameters(
                config.gamedir, config.gamedir,
                config.screen_width, config.screen_height,
                accent_color, "#000000", False, None,
                True, False, False, "gui")

            p.skip_backup = True

            generate_gui(p)

            _skip_backup = True
            _gui_images()
