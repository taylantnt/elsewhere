################################################################################
## THE LEAK LAYER
################################################################################
##
## Act 2 is supposed to be clean on the surface and wrong underneath. The
## treatment calls these leaks: a sentence repeated word for word, a pause that
## lasts a beat too long, a face that arrives twice. They are not dreams and
## they do not explain anything. They are the seam showing.
##
## Two sizes:
##
##     call leak_audio          sound only, for a room that is almost right
##     call leak_flash          a white hospital frame, for the seam opening
##
## Keep them rare. One every day or two is the rhythm the treatment describes;
## a leak on every screen is noise, not dread.

default fortune_teller_met = False
# The Day 12 cameo is only a glimpse. The Day 13 Asakusa reading is what opens
# the hub row and turns her into a limited confidant.
default fortune_arc_started = False
default fortune_result = "mixed"
default fortune_hint = ""
default murakami_lessons = 0
default murakami_homework_done = False
default murakami_asked_about_page = False


label leak_audio:
    $ play_sfx("audio/SFX/memory_deviation.wav")
    pause 0.35
    return


label leak_flash:
    $ play_sfx("audio/SFX/memory_deviation.wav")
    show hospital_flash onlayer overlay at truecenter, leak_flash_motion
    pause 0.24
    hide hospital_flash onlayer overlay
    return


transform leak_flash_motion:
    alpha 0.0
    linear 0.05 alpha 0.48
    linear 0.09 alpha 0.0
