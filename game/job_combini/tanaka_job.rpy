################################################################################
## THE COMBINI JOB: DISPATCHER AND SHARED BEATS
################################################################################
##
## Tanaka is the man behind the counter who rang up the first purchase and
## asked six questions in the right order. The purchase scene
## (`combini_first_counter`, in `city_rows.rpy`) put the HELP WANTED card in the
## window; the hub's `tanaka` row is the job.
##
## The job is structured like a confidant arc: one visit per shift, one file
## per visit (`tanaka_visit_01.rpy` … `tanaka_visit_07.rpy`), but it is not a
## confidant. The row never closes, because the store does not. Progress is
## `tanaka_story`, the number of teaching shifts he has given; `combini_shifts`
## counts every shift worked, including repeats.
##
## What Tanaka is: the tencho. The store manager. He never says so until visit
## 6, and the protagonist spends five visits assuming the manager is somebody
## else, because a manager who spends his afternoons telling a part-timer where
## the daikon goes does not fit the word.
##
## After visit 7 the job keeps repeating (`tanaka_visit_repeat`): the same four
## hours, the same wage, the same drawer. Work does not end; it just stops
## teaching.

## The dispatcher. `tanaka_story` is the index of the NEXT teaching shift.
label tanaka_shift:
    $ next_shift = tanaka_story
    if next_shift == 0:
        jump tanaka_visit_01
    elif next_shift == 1:
        jump tanaka_visit_02
    elif next_shift == 2:
        jump tanaka_visit_03
    elif next_shift == 3:
        jump tanaka_visit_04
    elif next_shift == 4:
        jump tanaka_visit_05
    elif next_shift == 5:
        jump tanaka_visit_06
    elif next_shift == 6:
        jump tanaka_visit_07
    else:
        jump tanaka_visit_repeat

label tanaka_common_open:
    scene bg_combini with walk_fade
    play sound "audio/SFX/combini.mp3"
    play music "audio/Music/kombini.mp3" fadein 1.0
    return

## The drawer, the wage, and the bookkeeping every shift shares.
## Each visit plays its own closing exchange AFTER this label returns.
label tanaka_wage_close:
    "At the end of the shift, Tanaka counts the drawer again. The numbers match. He does not look surprised."
    tanaka "Four hours. Four thousand eight hundred yen. It is in your hand."
    mc "Thank you."
    tanaka "Do not thank me. It is the wage."
    mc "I am thanking you anyway."
    tanaka "Then thank the store. I am only the person who counts."
    $ give_money(4800)
    $ combini_shifts += 1
    $ tanaka_story = min(7, tanaka_story + 1)
    $ last_afternoon_place = "tanaka"
    if "tanaka" not in wire_unlocked:
        $ wire_unlock("tanaka")
    return

label tanaka_walk_home:
    scene bg_river_dusk with walk_fade
    stop music fadeout 1.5
    "The sky over the canal has gone amber. Shop windows and streetlamps come on in the same order, each one handing the light to the next."
    "The combini is a bright square behind me, already part of the street. The four hours stay in my hands a little longer, then drain away on the walk home."
    return


################################################################################
## THE REPEAT SHIFT
################################################################################
##
## Every shift after the teaching ones. The work is the same and that is the
## point: a job is the day you make twice.

label tanaka_visit_repeat:
    call tanaka_common_open from _call_tanaka_common_open

    "Tanaka is already there, counting the drawer. He hands me my shirt without looking up."
    tanaka "You know the job."
    mc "I know the job."
    tanaka "Then the job is easy and the hours are long. That is the deal."

    menu:
        "Work the register without thinking.":
            "The script comes out of me in the right order. Old man, one banana. Schoolgirl, two ice creams. Mother, bento and milk."
            mc "(I could do this in my sleep. Some of it I think I do.)"
            $ reward_attributes_once("tanaka_repeat_register", [("grace", "micro")], show="auto")
        "Restock the shelves before he asks.":
            "I fill the gaps before the gaps are called. He notices. He does not say anything, which is how he says it."
            $ reward_attributes_once("tanaka_repeat_stock", [("insight", "micro")], show="auto")
        "Watch the store instead.":
            "For one hour I stand where he stands and watch what he watches. The door. The hot case. The hands of the clock."
            mc "(The store is a machine. He is the part that decides which part matters.)"
            $ reward_attributes_once("tanaka_repeat_watch", [("nerve", "micro")], show="auto")

    call tanaka_wage_close from _call_tanaka_wage_close
    mc "(The lessons stop. The shifts do not. I think that is the whole thing he was trying to teach.)"
    mc "(Somewhere there is another shift in a room I cannot remember. I keep thinking he is working that one too.)"
    tanaka "Same time next shift."
    mc "Same time."
    tanaka "Good. A store is a thing that is open. Everything else is decoration."
    call tanaka_walk_home from _call_tanaka_walk_home
    return
