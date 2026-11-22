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
# Whether he has formally joined the elective. Day 10 is the meeting; the
# decision to actually learn is the player's, made on the night of Day 12.
default murakami_enrolled = False
default murakami_homework_done = False
default murakami_asked_about_page = False
# Set on Day 41 when he touches the handle of the door that is not there. Day 42
# answers it with cold water; the callback only exists once the door has happened.
default door_twelfth_seen = False


label leak_audio:
    $ play_sfx("audio/SFX/leak.mp3")
    pause 0.35
    return


label leak_flash:
    $ play_sfx("audio/SFX/leak.mp3")
    show hospital_flash onlayer overlay at truecenter, leak_flash_motion
    pause 0.24
    hide hospital_flash onlayer overlay
    return


transform leak_flash_motion:
    alpha 0.0
    linear 0.05 alpha 0.48
    linear 0.09 alpha 0.0
