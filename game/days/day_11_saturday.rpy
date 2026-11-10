################################################################################
## DAY 11 — SATURDAY, APRIL 18, 2026 (THE ELECTIVE, PART 2)
################################################################################

label saturday_recovery:
    $ set_story_day(11)
    call day_transition

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    scene bg_home_exterior_night with walk_fade
    $ night_street()
    "Saturday. The house is quiet in a different way. The kitchen is not lit. The living room is not lit. The whole building is holding its breath."
    "Murakami comes to the door. He does not knock. He never knocks. He stands where he is and talks through the door."
    professor "The elective is not a class. It is a way of walking. Bring the frog."
    mc "The frog."
    professor "The frog. And the river. And the quiet."
    "The lesson is at the kitchen table. The professor's Japanese is better than anyone in the building, and it is still not enough to make the room feel like it was built for him. He knows that too."
    "The night is the first night of the language. The first night of the country. I sleep differently. I do not know how yet, but I sleep differently."

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    jump sunday_practice
