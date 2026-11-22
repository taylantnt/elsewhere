################################################################################
## COMMON DAYS: THE ACT 2 SKELETON
################################################################################
##
## Days 8-21 are all SPECIAL days: each one carries a hand-written set piece
## (the frog, Genji, the midterm, the results). From day 22 onward the calendar
## splits into two kinds of file:
##
##   special_day_NN_slug.rpy   a fixed beat. Written by hand, one per file.
##   common_day_NN.rpy         a routine day. Calls `common_day_core`, which
##                             runs the shared skeleton below.
##
## The skeleton is deliberately smaller than the special-day shape. The commute
## collapses to three lines, the lecture is short, and the afternoon is always
## the hub. What keeps a common day from feeling like a copy is COMMON_DAY_BEATS:
## one entry per day carrying that day's morning, Hikari's lesson, Murakami's
## topic, the dinner table, and the night menu answers. Every common day should
## teach or notice one small thing about Japan, the city, or the people in it.
##
## `act2_day_router` is the only place that knows the order of days 22-45. When
## a special day is written, its stub already sits in the chain; filling in the
## stub changes nothing else.
##
## Weekend common days (Saturday/Sunday) skip the lecture block entirely and
## play their `off` beat instead. The hub still opens; the day just starts
## slower.

init python:

    # A line is (speaker, text). "narr" is narration; anything else must match
    # a store character name (mc, hikari, father, mother, murakami).
    COMMON_SPEAKER_FALLBACK = "narr"

    def common_day_say(speaker, text):
        if not speaker or speaker == "narr":
            renpy.say(None, text)
            return
        who = getattr(store, speaker, None)
        if who is None:
            renpy.say(None, text)
        else:
            renpy.say(who, text)

    def common_day_school(day):
        """True on weekdays. Weekends skip the lecture block."""
        return story_calendar_weekday(day) < 5

    def common_day_beat(day):
        return COMMON_DAY_BEATS.get(int(day), COMMON_DAY_FALLBACK_BEAT)

    def collect_notebook_line(day):
        """Record the day's one small true thing for the phone Journal.

        The line is already spoken in the scene; this only files it. A day is
        collected once, so replaying a beat can never duplicate an entry.
        """
        day = int(day)
        if any(entry[0] == day for entry in store.notebook_lines):
            return
        note = common_day_beat(day).get("notebook")
        if note:
            store.notebook_lines.append((day, note))

    # The phone chat rotates through this pool. A contact that is not unlocked
    # yet simply produces no chat that morning.
    COMMON_DAY_CHAT_POOL = [
        ("hikari", [
            {"them": "You're up early.", "options": [
                {"label": "\"You are too.\"",
                 "send": "You are too.",
                 "them": ["I was already awake.", "The house was too quiet."]},
                {"label": "\"I couldn't sleep.\"",
                 "send": "I couldn't sleep.",
                 "them": ["Then come down.", "The miso soup is still warm."]},
            ]},
        ]),
        ("tanaka", [
            {"them": "Shift this afternoon. Three o'clock. Do not be late.", "options": [
                {"label": "\"I'll be there.\"",
                 "send": "I'll be there.",
                 "them": ["Good.", "Wear the shirt. The collar one."]},
                {"label": "\"Can I ask about the register?\"",
                 "send": "Can I ask about the register?",
                 "them": ["You will learn it this afternoon.", "That is what the shift is for."]},
            ]},
        ]),
        ("chef", [
            {"them": "The soup is different today. Come taste it before it changes again.", "options": [
                {"label": "\"What changed?\"",
                 "send": "What changed?",
                 "them": ["The recipe is in the pot.", "Less pressure."]},
                {"label": "\"I'll come by after class.\"",
                 "send": "I'll come by after class.",
                 "them": ["Good.", "Bring the appetite, not the phone."]},
            ]},
        ]),
        ("sim", [
            {"them": "Bring the camera. Wear the good jacket.", "options": [
                {"label": "\"What are we shooting?\"",
                 "send": "What are we shooting?",
                 "them": ["A place that does not know it is being watched.", "You will see."]},
                {"label": "\"I have class today.\"",
                 "send": "I have class today.",
                 "them": ["Class ends.", "The city does not."]},
            ]},
        ]),
        ("hikari", [
            {"them": "Did you see the cat on the wall again?",
             "options": [
                {"label": "\"The same one?\"",
                 "send": "The same one?",
                 "them": ["Different one. Same wall.", "The wall keeps them."]},
                {"label": "\"I didn't see it today.\"",
                 "send": "I didn't see it today.",
                 "them": ["It saw you.", "That is what cats do."]},
            ]},
        ]),
        ("aya", [
            {"them": "New menu item. The omurice has a secret ingredient. You may guess.", "options": [
                {"label": "\"Truffle?\"",
                 "send": "Truffle?",
                 "them": ["Close. It is love.", "And a little ketchup."]},
                {"label": "\"I'll come taste it.\"",
                 "send": "I'll come taste it.",
                 "them": ["Good.", "Ask for the corner table."]},
            ]},
        ]),
    ]

    # Per-day morning chats. Each entry is the message that the beat's
    # `chat_note` reacts to, so the note never narrates a text the player did
    # not actually receive. A locked contact falls back to the rotating pool,
    # and the core skips the note in that case.
    COMMON_DAY_CHATS = {
        23: ("hikari", [
            {"them": "I put my umbrella by the door. The sky has not decided yet, but I have.", "options": [
                {"label": "\"Take yours too.\"",
                 "send": "Take yours too.",
                 "them": ["It is folded and waiting.", "Two umbrellas are one more than we need. That is fine."]},
                {"label": "\"It looks sunny.\"",
                 "send": "It looks sunny.",
                 "them": ["That is what the sky wants you to think.", "Bring it anyway."]},
            ]},
        ]),
        30: ("tanaka", [
            {"them": "Shift this afternoon. Three o'clock. Four hours. Do not be late.", "options": [
                {"label": "\"I'll be there.\"",
                 "send": "I'll be there.",
                 "them": ["Good.", "Wear the shirt. The collar one."]},
                {"label": "\"Can I ask about the register?\"",
                 "send": "Can I ask about the register?",
                 "them": ["You will learn it this afternoon.", "That is what the shift is for."]},
            ]},
        ]),
        31: ("hikari", [
            {"them": "Queue with your eyes open today. Watch how they merge.", "options": [
                {"label": "\"I'll watch.\"",
                 "send": "I'll watch.",
                 "them": ["Do not stare.", "Watching is not staring."]},
                {"label": "\"I already do.\"",
                 "send": "I already do.",
                 "them": ["Then you will see something new.", "Look at the empty space between people."]},
            ]},
        ]),
        32: ("sim", [
            {"them": "Bring the camera. Wear the good jacket.", "options": [
                {"label": "\"What are we shooting?\"",
                 "send": "What are we shooting?",
                 "them": ["A place that does not know it is being watched.", "You will see."]},
                {"label": "\"I have neither ready.\"",
                 "send": "I have neither ready.",
                 "them": ["Then you have all afternoon.", "The jacket is in the closet. The camera is on the shelf."]},
            ]},
        ]),
        34: ("tanaka", [
            {"them": "Shift this afternoon. Do not be late.", "options": [
                {"label": "\"I'll be there.\"",
                 "send": "I'll be there.",
                 "them": ["Good.", "Ask about the point card while you are at it."]},
                {"label": "\"I am tired.\"",
                 "send": "I am tired.",
                 "them": ["Then the register will be tired too.", "Come anyway. Four hours is four hours."]},
            ]},
        ]),
        35: ("hikari", [
            {"them": "Try the kissaten today. Tell me if the coffee is better than the machine's.", "options": [
                {"label": "\"I'll go after class.\"",
                 "send": "I'll go after class.",
                 "them": ["Good.", "Order the siphon. Not the drip."]},
                {"label": "\"I cannot tell.\"",
                 "send": "I cannot tell.",
                 "them": ["Then you will have to go twice.", "That is a good arrangement."]},
            ]},
        ]),
        36: ("chef", [
            {"them": "The soup is different on Thursdays. Come taste it before it becomes Thursday.", "options": [
                {"label": "\"Today is not Thursday.\"",
                 "send": "Today is not Thursday.",
                 "them": ["Then it is practice soup.", "Less pressure."]},
                {"label": "\"I'll come by.\"",
                 "send": "I'll come by.",
                 "them": ["Good.", "Bring the appetite, not the phone."]},
            ]},
        ]),
        37: ("sim", [
            {"them": "Bring the camera. Wear the good jacket.", "options": [
                {"label": "\"What are we shooting?\"",
                 "send": "What are we shooting?",
                 "them": ["A place that does not know it is being watched.", "You will see."]},
                {"label": "\"I have class.\"",
                 "send": "I have class.",
                 "them": ["Class ends.", "The city does not."]},
            ]},
        ]),
        38: ("aya", [
            {"them": "New menu item. The omurice has a secret ingredient. You may guess.", "options": [
                {"label": "\"Truffle?\"",
                 "send": "Truffle?",
                 "them": ["Close. It is love.", "And a little ketchup."]},
                {"label": "\"I'll come taste it.\"",
                 "send": "I'll come taste it.",
                 "them": ["Good.", "Ask for the corner table."]},
            ]},
        ]),
        39: ("hikari", [
            {"them": "The mist is nice today. Come see it with me.", "options": [
                {"label": "\"I'm already dressed.\"",
                 "send": "I'm already dressed.",
                 "them": ["I know.", "I saw you from the window."]},
                {"label": "\"Give me a minute.\"",
                 "send": "Give me a minute.",
                 "them": ["The mist will wait. It is patient.", "So will I."]},
            ]},
        ]),
        40: ("sim", [
            {"them": "Sunday. Bring the camera. The rain is good for photos.", "options": [
                {"label": "\"I have it.\"",
                 "send": "I have it.",
                 "them": ["Good.", "Shoot the gutters. They tell the truth."]},
                {"label": "\"It is pouring.\"",
                 "send": "It is pouring.",
                 "them": ["That is why the camera is for.", "Bring an umbrella for the lens."]},
            ]},
        ]),
        42: ("hikari", [
            {"them": "The rain stopped. Come see the clean city with me.", "options": [
                {"label": "\"I'm already dressed.\"",
                 "send": "I'm already dressed.",
                 "them": ["I know.", "I have been waiting at the door."]},
                {"label": "\"Give me a minute.\"",
                 "send": "Give me a minute.",
                 "them": ["The city is not going anywhere.", "Neither am I, really."]},
            ]},
        ]),
        43: ("chef", [
            {"them": "The soup is different on Thursdays. Come taste it before it becomes Thursday.", "options": [
                {"label": "\"Today is not Thursday.\"",
                 "send": "Today is not Thursday.",
                 "them": ["Then it is practice soup.", "Less pressure."]},
                {"label": "\"I'll come by.\"",
                 "send": "I'll come by.",
                 "them": ["Good.", "Bring the appetite, not the phone."]},
            ]},
        ]),
        44: ("sim", [
            {"them": "Thursday. Bring the camera. Wear the good jacket.", "options": [
                {"label": "\"What are we shooting?\"",
                 "send": "What are we shooting?",
                 "them": ["A place that does not know it is being watched.", "You will see."]},
                {"label": "\"I have class.\"",
                 "send": "I have class.",
                 "them": ["Class ends.", "The city does not."]},
            ]},
        ]),
        45: ("aya", [
            {"them": "New menu item. The omurice has a secret ingredient. You may guess.", "options": [
                {"label": "\"Truffle?\"",
                 "send": "Truffle?",
                 "them": ["Close. It is love.", "And a little ketchup."]},
                {"label": "\"I'll come taste it.\"",
                 "send": "I'll come taste it.",
                 "them": ["Good.", "Ask for the corner table."]},
            ]},
        ]),
    }

    def common_day_chat(day):
        day = int(day)
        cid, beats = COMMON_DAY_CHATS.get(day, COMMON_DAY_CHAT_POOL[day % len(COMMON_DAY_CHAT_POOL)])
        # Register cadence: a player who never took a shift does not get Tanaka's
        # reminder, and the beat's chat_note is skipped with it. Hikari nudges
        # instead. Nothing is lost; the afternoon stays player-initiated.
        if cid == "tanaka" and store.combini_shifts == 0:
            if "hikari" in store.wire_unlocked:
                return ("hikari", [
                    {"them": "You said you needed work. The store next to the ramen shop is still hiring.", "options": [
                        {"label": "\"I know.\"", "send": "I know.", "them": ["Then why haven't you gone?", "I am only asking."]},
                        {"label": "\"Not today.\"", "send": "Not today.", "them": ["Tomorrow, then.", "The card stays in the window."]},
                    ]},
                ])
            return None
        if cid in store.wire_unlocked:
            return (cid, beats)
        # Fall back to Hikari, who is always reachable once the phone exists.
        if "hikari" in store.wire_unlocked:
            return ("hikari", COMMON_DAY_CHAT_POOL[0][1])
        return None

    # Regular faculty lectures for common days. Murakami teaches the elective in
    # her own after-school visits, not the daily class; ordinary school days
    # belong to `professor`. A beat may still supply a one-off `lecture` dict.
    COMMON_PROFESSOR_LECTURES = [
        {
            "intro": [
                ("professor", "Today we are not learning a poem. We are learning how to stand in front of one."),
                ("professor", "The reader's posture. Where you put your eyes. What you refuse to look at."),
            ],
            "a": [
                ("professor", "Basho wrote three lines and left a door open. The reader's job is to walk through it, not to slam it."),
                ("mc", "(So reading is not decoding. It is deciding how long to stay in the doorway.)"),
            ],
            "b": [
                ("professor", "Why does posture matter? Because a poem is not a message. It is a room, and you are either a guest or a surveyor."),
                ("mc", "(The city is a poem too. I have been a surveyor for a month. Today I try to be a guest.)"),
            ],
            "c": [
                ("professor", "Write down one thing you looked at today and did not understand. That is where the poem is."),
                ("mc", "(I write: the vending machine's hum. I still do not know what it means. I keep writing it down anyway.)"),
            ],
        },
        {
            "intro": [
                ("professor", "The syllabus is a map, not a contract. Read it the way you read a city: for the roads, not the fences."),
                ("professor", "What the exam cannot measure is the only thing worth measuring. Remember that when the marks arrive."),
            ],
            "a": [
                ("professor", "You have all passed exams that tested memory. None of them tested whether you noticed the room you were sitting in."),
                ("mc", "(The midterm tested what I could repeat. This tests what I can see. I am not sure which one I am better at.)"),
            ],
            "b": [
                ("professor", "A mark is a receipt. It proves you were present. It does not prove you were there."),
                ("mc", "(I think of the attendance stamps. Present, present, present. And underneath, a person who is somewhere else entirely.)"),
            ],
            "c": [
                ("professor", "Write down one thing the syllabus does not mention. Anything. The margins are part of the text."),
                ("mc", "(I write: the professor's watch. It is slow. He checks it like it owes him time.)"),
            ],
        },
        {
            "intro": [
                ("professor", "Today: the footnote. The smallest text on the page, and the one that tells the truth."),
                ("professor", "Every author puts the real thing in the footnote. The body is for visitors. The footnote is for residents."),
            ],
            "a": [
                ("professor", "Find me a footnote in anything you read this week. A dictionary entry. A receipt. A sign."),
                ("mc", "(The train announcement is a footnote. It tells you nothing and means everything.)"),
            ],
            "b": [
                ("professor", "Why do writers hide the truth in small print? Because small print cannot be skimmed. It makes you lean in."),
                ("mc", "(So the details I keep noticing, the humming machines and the wrong doors, maybe they are the footnotes. Maybe they are the only honest text.)"),
            ],
            "c": [
                ("professor", "Copy one small true thing into your notebook. Not a quote. A detail. The kind only a resident would write down."),
                ("mc", "(I write: the way the station cat sleeps in the same spot every afternoon, like it pays rent.)"),
            ],
        },
    ]

    def common_professor_lecture(day):
        return COMMON_PROFESSOR_LECTURES[int(day) % len(COMMON_PROFESSOR_LECTURES)]

    # The commute is the most repeated block in the game, so common days share
    # four rotating versions instead of writing five new ones.
    COMMON_COMMUTES = [
        [("narr", "Two changes. The first car is full of salarymen asleep standing up."),
         ("narr", "The second is empty. An old woman is reading a newspaper with her whole body."),
         ("narr", "I get off one station early and walk the rest. The street smells like bread."),
         ("mc", "(The walk is longer than the train. The walk is better.)")],
        [("narr", "One change today. The platform is crowded and nobody says sorry, which is its own kind of manners."),
         ("narr", "A student is practicing English under her breath. She is not embarrassed. That is the lesson."),
         ("mc", "(Everyone here is a beginner at something. The trick is that nobody calls it that.)")],
        [("narr", "The express skips my stop. I take the local back one station and walk."),
         ("narr", "A construction site is louder than the train. The city is always being rebuilt a little."),
         ("mc", "(Being lost is a skill. I am getting better at it on purpose.)")],
        [("narr", "The train is quiet in the way libraries are quiet. Nobody performs silence here. It just happens."),
         ("narr", "A student across from me is asleep against the window, her headphones still on."),
         ("mc", "(Four weeks ago this ride was the scariest part of my day. Now it is the part I think about least, which might be the point.)")],
    ]

    def common_day_commute(day):
        """The rotating ride, plus the man who keeps the end seat warm.

        He belongs to the weekday train. Golden Week takes him away, weekends
        belong to somebody else, and by Day 45 the seat stays empty without an
        explanation. The special days carry the same running gag; this keeps it
        alive on the routine days without writing it out every time.
        """
        day = int(day)
        lines = list(COMMON_COMMUTES[day % len(COMMON_COMMUTES)])
        if 25 <= day <= 29:
            lines.append(("narr", "The end seat is empty. Even the sleeping man has gone somewhere for the holiday."))
        elif day == 45:
            lines.append(("narr", "The end seat is empty. The sleeping man is not on the train."))
            lines.append(("mc", "(I do not know when he stopped coming. I do not know if I would have noticed.)"))
        elif story_calendar_weekday(day) >= 5:
            lines.append(("narr", "The end seat is empty. Weekends belong to somebody else."))
        else:
            lines.append(("narr", "The sleeping man is on the end seat, chin on his chest. He is always there on a weekday."))
        return lines

################################################################################
## THE SKELETON
################################################################################

label common_day_lines(lines):
    python:
        for speaker, text in lines:
            common_day_say(speaker, text)
    return

label common_day_core:
    $ beat = common_day_beat(store.story_day)
    $ today = store.story_day

    call day_transition from _call_day_transition
    $ flush_pending_messages()

    scene bg_room_day with Dissolve(1.5)
    $ room_ambient(False)
    call common_day_lines(beat["morning"]) from _call_common_day_lines

    $ beat_chat = COMMON_DAY_CHATS.get(today)
    $ chat_pick = common_day_chat(today)
    if chat_pick:
        $ run_chat(chat_pick[0], chat_pick[1])
        # Only narrate the note if its message is the one that was actually sent.
        if beat_chat and chat_pick == beat_chat and beat.get("chat_note"):
            call common_day_lines(beat["chat_note"]) from _call_common_day_lines_1

    call murakami_daily_ping from _call_murakami_daily_ping

    scene bg_kitchen with walk_fade
    call common_day_lines(beat["kitchen"]) from _call_common_day_lines_2

    scene bg_home_exterior_day with walk_fade
    call common_day_lines(beat["lesson"]) from _call_common_day_lines_3

    scene bg_train_interior with walk_fade
    call common_day_lines(common_day_commute(today)) from _call_common_day_lines_4

    if common_day_school(today):
        scene bg_lecture_hall with walk_fade
        $ lec = beat["lecture"] if beat.get("lecture") else common_professor_lecture(today)
        call common_day_lines(lec["intro"]) from _call_common_day_lines_5
        menu:
            "Ask him to say it again.":
                call common_day_lines(lec["a"]) from _call_common_day_lines_6
                $ reward_attributes_once("cd%d_lec_a" % today, [("insight", "micro")], show="auto")
            "Ask why it matters here.":
                call common_day_lines(lec["b"]) from _call_common_day_lines_7
                $ reward_attributes_once("cd%d_lec_b" % today, [("grace", "micro")], show="auto")
            "Copy the line into your notebook.":
                call common_day_lines(lec["c"]) from _call_common_day_lines_8
                $ reward_attributes_once("cd%d_lec_c" % today, [("nerve", "micro")], show="auto")

        if today == 31:
            call quiz_everyday_language from _call_quiz_everyday_language_1
        elif today == 42:
            call quiz_particles from _call_quiz_particles_1

        scene bg_campus_interior with walk_fade
        if beat.get("campus"):
            call common_day_lines(beat["campus"]) from _call_common_day_lines_9
    else:
        scene bg_home_exterior_day with walk_fade
        call common_day_lines(beat["off"]) from _call_common_day_lines_10

    $ flush_pending_messages()
    call free_afternoon from _call_free_afternoon

    scene bg_home_exterior_day with walk_fade
    call common_day_lines(beat.get("walk", [])) from _call_common_day_lines_11
    # Day 42 answers the warm twelfth door from Day 41 with cold shrine water.
    # The echo only exists once he has actually touched that handle.
    if beat.get("echo") and store.door_twelfth_seen:
        call common_day_lines(beat["echo"]) from _call_common_day_lines_12

    $ dinner_lines = beat["dinner"]
    if beat.get("dinner_no_shift") and store.combini_shifts == 0:
        $ dinner_lines = beat["dinner_no_shift"]
    call dinner_open from _call_dinner_open
    call common_day_lines(dinner_lines) from _call_common_day_lines_13
    # Day 38 only: Father says his Day 34 line word for word. The glitch is the
    # repetition, not the delivery, so the sound is the only thing that marks it.
    if beat.get("leak_after_dinner"):
        call leak_audio from _call_leak_audio
        call common_day_lines(beat["leak_after_dinner"]) from _call_common_day_lines_14
        if today == 38:
            $ remember("mc", "Father repeated the machine line word for word and the sound was wrong; Hikari said fathers repeat themselves", "father_verbatim_repeat")
    call dinner_close from _call_dinner_close

    scene bg_room_night with stair_fade
    $ room_ambient(True)
    $ night_desk_line = beat.get("desk", "the window")
    call night_open from _call_night_open

    menu:
        "Ask about the day.":
            call common_day_lines(beat["night_a"]) from _call_common_day_lines_15
            if beat.get("remember_a"):
                $ log_memory("hikari", beat["remember_a"])
            $ reward_attributes_once("cd%d_night_a" % today, [("grace", "micro")], show="auto")
        "Tell her one true thing.":
            call common_day_lines(beat["night_b"]) from _call_common_day_lines_16
            if beat.get("remember_b"):
                $ log_memory("hikari", beat["remember_b"])
            $ reward_attributes_once("cd%d_night_b" % today, [("nerve", "micro")], show="auto")
        "Say nothing. Listen to the city.":
            call common_day_lines(beat["night_c"]) from _call_common_day_lines_17
            $ reward_attributes_once("cd%d_night_c" % today, [("insight", "micro")], show="auto")
        # Open once everyone has been met. Hikari never names anybody she has
        # not met herself; the doors she cannot see stay unnamed.
        "Ask what she's left off the map." if all_confidants_met():
            $ closed_line = beat.get("night_d", [
                ("mc", "Is there anywhere you know well that you haven't put on my map?"),
                ("hikari", "A few places. I wanted you to have somewhere to start. I didn't mean to decide where you'd stop."),
                ("mc", "You could show me one more."),
                ("hikari", "Next time you show me one."),
            ])
            call common_day_lines(closed_line) from _call_common_day_lines_18
            $ reward_attributes_once("cd%d_night_d" % today, [("insight", "micro")], show="auto")

    call night_close from _call_night_close
    call common_day_lines(beat.get("close", [])) from _call_common_day_lines_19
    $ collect_notebook_line(today)

    stop music fadeout 2.0
    scene black with Dissolve(1.5)
    pause 1.5
    return

################################################################################
## THE ROUTER: story_day -> the label of the NEXT day
################################################################################
##
## Every day label (special or common) ends by jumping here. The router reads
## the day that just finished and sends the story to the next one. Day 69
## currently ends at the end-of-build card.

init python:

    # story_day -> the label that starts that day. Used only by
    # `save_compat_recovery` below.
    DAY_START_LABELS = {
        8: "wednesday_morning",
        9: "thursday_morning",
        10: "friday_morning",
        11: "saturday_recovery",
        12: "sunday_practice",
        13: "monday_asakusa",
        14: "tuesday_week_two",
        15: "wednesday_preview",
        16: "thursday_mitate",
        17: "friday_sounds",
        18: "saturday_matsuri",
        19: "sunday_mock",
        20: "monday_midterm",
        21: "tuesday_results",
        22: "special_day_22_see_me",
        23: "common_day_23",
        24: "special_day_24_early_may",
        25: "common_day_25",
        26: "special_day_26_nakameguro",
        27: "special_day_27_gw_trip",
        28: "special_day_28_gw_evening",
        29: "special_day_29_school_returns",
        30: "common_day_30",
        31: "common_day_31",
        32: "common_day_32",
        33: "special_day_33_absence",
        34: "common_day_34",
        35: "common_day_35",
        36: "common_day_36",
        37: "common_day_37",
        38: "common_day_38",
        39: "common_day_39",
        40: "common_day_40",
        41: "special_day_41_leak",
        42: "common_day_42",
        43: "common_day_43",
        44: "common_day_44",
        45: "common_day_45",
        46: "special_day_46_tsukiji",
        47: "special_day_47_kamakura",
        48: "special_day_48_sento",
        49: "special_day_49_hydrangea",
        50: "special_day_50_fireflies",
        51: "special_day_51_the_line",
        52: "special_day_52_same_face",
        53: "special_day_53_fragment",
        54: "special_day_54_the_return",
        55: "special_day_55_the_word",
        56: "special_day_56_the_repeat",
        57: "special_day_57_the_clock",
        58: "special_day_58_the_stall",
        59: "special_day_59_the_door",
        60: "special_day_60_the_question",
        61: "special_day_61_the_geometry",
        62: "special_day_62_the_sentence",
        63: "special_day_63_the_threshold",
        64: "special_day_64_the_rail",
        65: "special_day_65_the_answer",
        66: "special_day_66_the_notice",
        67: "special_day_67_the_lot",
        68: "special_day_68_the_detail",
        69: "special_day_69_the_copy",
    }

################################################################################
## SAVE RECOVERY: renamed day files vs. old saves
################################################################################
##
## The day files were renamed (day_N_slug.rpy -> special_day_NN_slug.rpy) after
## saves already existed. A Ren'Py save stores its call stack as node names
## containing the source filename, so any save taken while a call chain reached
## into a renamed file can no longer find its return site and crashes on load
## with "Could not find return label".
##
## `config.return_not_found_label` routes those dead ends here. There is no way
## to resume mid-scene, so the honest recovery is to restart the current day
## from its label. `pop_call` keeps the dynamic/abnormal stacks in step while
## the dead entries are dropped.

define config.return_not_found_label = "save_compat_recovery"

label save_compat_recovery:
    python:
        while renpy.game.context().return_stack:
            renpy.game.context().pop_call()
    $ target = DAY_START_LABELS.get(store.story_day, "act2_day_router")
    jump expression target

label act2_day_router:
    if store.story_day <= 21:
        jump special_day_22_see_me
    elif store.story_day == 22:
        jump common_day_23
    elif store.story_day == 23:
        jump special_day_24_early_may
    elif store.story_day == 24:
        jump common_day_25
    elif store.story_day == 25:
        jump special_day_26_nakameguro
    elif store.story_day == 26:
        jump special_day_27_gw_trip
    elif store.story_day == 27:
        jump special_day_28_gw_evening
    elif store.story_day == 28:
        jump special_day_29_school_returns
    elif store.story_day == 29:
        jump common_day_30
    elif store.story_day == 30:
        jump common_day_31
    elif store.story_day == 31:
        jump common_day_32
    elif store.story_day == 32:
        jump special_day_33_absence
    elif store.story_day == 33:
        jump common_day_34
    elif store.story_day == 34:
        jump common_day_35
    elif store.story_day == 35:
        jump common_day_36
    elif store.story_day == 36:
        jump common_day_37
    elif store.story_day == 37:
        jump common_day_38
    elif store.story_day == 38:
        jump common_day_39
    elif store.story_day == 39:
        jump common_day_40
    elif store.story_day == 40:
        jump special_day_41_leak
    elif store.story_day == 41:
        jump common_day_42
    elif store.story_day == 42:
        jump common_day_43
    elif store.story_day == 43:
        jump common_day_44
    elif store.story_day == 44:
        jump common_day_45
    elif store.story_day == 45:
        jump special_day_46_tsukiji
    elif store.story_day == 46:
        jump special_day_47_kamakura
    elif store.story_day == 47:
        jump special_day_48_sento
    elif store.story_day == 48:
        jump special_day_49_hydrangea
    elif store.story_day == 49:
        jump special_day_50_fireflies
    elif store.story_day == 50:
        jump special_day_51_the_line
    elif store.story_day == 51:
        jump special_day_52_same_face
    elif store.story_day == 52:
        jump special_day_53_fragment
    elif store.story_day == 53:
        jump special_day_54_the_return
    elif store.story_day == 54:
        jump special_day_55_the_word
    elif store.story_day == 55:
        jump special_day_56_the_repeat
    elif store.story_day == 56:
        jump special_day_57_the_clock
    elif store.story_day == 57:
        jump special_day_58_the_stall
    elif store.story_day == 58:
        jump special_day_59_the_door
    elif store.story_day == 59:
        jump special_day_60_the_question
    elif store.story_day == 60:
        jump special_day_61_the_geometry
    elif store.story_day == 61:
        jump special_day_62_the_sentence
    elif store.story_day == 62:
        jump special_day_63_the_threshold
    elif store.story_day == 63:
        jump special_day_64_the_rail
    elif store.story_day == 64:
        jump special_day_65_the_answer
    elif store.story_day == 65:
        jump special_day_66_the_notice
    elif store.story_day == 66:
        jump special_day_67_the_lot
    elif store.story_day == 67:
        jump special_day_68_the_detail
    elif store.story_day == 68:
        jump special_day_69_the_copy
    else:
        jump end_of_build

################################################################################
## COMMON DAY WRAPPERS
################################################################################
##
## One label per common day. Each pins its absolute day, runs the shared
## skeleton, then hands the calendar to the router.

label common_day_23:
    $ set_story_day(23)
    call common_day_core from _call_common_day_core
    jump act2_day_router

label common_day_25:
    $ set_story_day(25)
    call common_day_core from _call_common_day_core_1
    jump act2_day_router

label common_day_30:
    $ set_story_day(30)
    call common_day_core from _call_common_day_core_2
    jump act2_day_router

label common_day_31:
    $ set_story_day(31)
    call common_day_core from _call_common_day_core_3
    jump act2_day_router

label common_day_32:
    $ set_story_day(32)
    call common_day_core from _call_common_day_core_4
    jump act2_day_router

label common_day_34:
    $ set_story_day(34)
    call common_day_core from _call_common_day_core_5
    jump act2_day_router

label common_day_35:
    $ set_story_day(35)
    call common_day_core from _call_common_day_core_6
    jump act2_day_router

label common_day_36:
    $ set_story_day(36)
    call common_day_core from _call_common_day_core_7
    jump act2_day_router

label common_day_37:
    $ set_story_day(37)
    call common_day_core from _call_common_day_core_8
    jump act2_day_router

label common_day_38:
    $ set_story_day(38)
    call common_day_core from _call_common_day_core_9
    jump act2_day_router

label common_day_39:
    $ set_story_day(39)
    call common_day_core from _call_common_day_core_10
    jump act2_day_router

label common_day_40:
    $ set_story_day(40)
    call common_day_core from _call_common_day_core_11
    jump act2_day_router

label common_day_42:
    $ set_story_day(42)
    call common_day_core from _call_common_day_core_12
    jump act2_day_router

label common_day_43:
    $ set_story_day(43)
    call common_day_core from _call_common_day_core_13
    jump act2_day_router

label common_day_44:
    $ set_story_day(44)
    call common_day_core from _call_common_day_core_14
    jump act2_day_router

label common_day_45:
    $ set_story_day(45)
    call common_day_core from _call_common_day_core_15
    jump act2_day_router

################################################################################
## THE BEATS: one small true thing per day
################################################################################
##
## Each entry owns the day. `lesson` is Hikari teaching him a manner or a fact;
## `lecture` is a one-off class (ordinary days use the professor pool); `off`
## replaces the lecture on weekends. Keep every beat concrete: a thing you can
## see, a rule you can break, a word with a shape.
##
## `notebook` is the one small true thing collected for the phone Journal.
## `leak_after_dinner` fires leak_audio before its lines (Day 38 only). `echo`
## plays only once its flag is set (Day 42 answers the Day 41 door).

init python:

    COMMON_DAY_FALLBACK_BEAT = {
        "title": "An ordinary day",
        "morning": [
            ("narr", "Another morning. The city does not announce them anymore."),
            ("mc", "(The city does not announce them anymore. I have stopped waiting for it to.)"),
        ],
        "kitchen": [
            ("mother", "Eat. There is enough."),
            ("mc", "There is always enough. That is the problem with enough."),
        ],
        "lesson": [
            ("hikari", "Today I will teach you nothing. Some days are for noticing."),
            ("mc", "That is still a lesson."),
            ("hikari", "It is the only one that cannot be tested."),
        ],
        "off": [
            ("narr", "No class today. The afternoon belongs to the map."),
        ],
        "lecture": {
            "intro": [
                ("murakami", "Today we practice the smallest unit of the language."),
                ("murakami", "A particle. The thing that holds two words together like a door hinge."),
            ],
            "a": [("murakami", "Repeat after me: the difference between 'and' and 'with' is the difference between a list and a room.")],
            "b": [("murakami", "Every sentence is a small architecture. Learn the hinges and you can build anything.")],
            "c": [("murakami", "Write the particle down. It will appear in every sentence you ever speak here.")],
        },
        "dinner": [
            ("father", "School."),
            ("mc", "School."),
            ("father", "Good. School is a thing you make every day too."),
        ],
        "night_a": [("hikari", "Tell me one thing you noticed today that nobody else would."), ("mc", "(I think about the answer all the way upstairs.)")],
        "night_b": [("hikari", "You look tired. The good kind or the other kind?"), ("mc", "The kind that means something happened.")],
        "night_c": [("narr", "I say nothing. The window is open. The city answers in its own time."), ("hikari", "You are getting good at this.")],
        "desk": "the window",
        "close": [("narr", "I turn off the lamp. The room is dark. The room is not empty.")],
    }

    COMMON_DAY_BEATS = {

        23: {
            "title": "Umbrellas and distance",
            "morning": [
                ("narr", "Thursday. The forecast said rain and the sky has not decided yet, which is its own kind of weather."),
                ("narr", "I find Hikari at the genkan already holding her umbrella, folded, like a person who plans to be ready for opinions."),
                ("mc", "(She checks the sky the way other people check their phone. Maybe it is the same thing.)"),
            ],
            "chat_note": [("mc", "(She is already dressed for a weather that has not happened. I make a note of it the way she makes notes of birds.)")],
            "kitchen": [
                ("mother", "Take an umbrella. The news said rain by noon."),
                ("father", "He has one. He has two. He is becoming prepared."),
                ("mc", "Preparation is just anxiety with a schedule."),
            ],
            "lesson": [
                ("hikari", "Umbrella rules. Number one: never open it indoors. The water goes everywhere and everyone pretends not to mind."),
                ("mc", "Even in a small entryway?"),
                ("hikari", "Especially in a small entryway. Number two: when you fold it, point it at yourself. The wet part is a private matter."),
                ("mc", "(An umbrella is a room you carry. Small, wet, and yours.)"),
            ],
            "lecture": {
                "intro": [
                    ("murakami", "Today: the verb that is not a verb. In Japanese, you do things by naming them."),
                    ("murakami", "Benkyou suru. Study-do. The doing is borrowed. The naming is the act."),
                ],
                "a": [
                    ("murakami", "Say it: benkyou suru. Now say it faster. The language rewards speed the way a door rewards a push."),
                    ("mc", "(It sounds like a secret handshake. Maybe all politeness is.)"),
                ],
                "b": [
                    ("murakami", "Why does it matter? Because a culture that names the act before doing it has already agreed on what the act is."),
                    ("mc", "(So the combini script, the six questions, they were a suru-verb. A ritual you perform by saying it.)"),
                ],
                "c": [
                    ("murakami", "Write down three suru-verbs you already know. Undou suru. Exercise-do. Neri suru. Knead-do."),
                    ("mc", "(Cooking is a verb you perform by naming it. I think of the kitchen at night.)"),
                ],
            },
            "campus": [
                ("narr", "The campus is half-empty. Someone has left a bag on a bench with a book on top, a system of trust I do not understand yet."),
                ("mc", "(In my city, that bag would be gone by lunch. Here it waits like it has a reason.)"),
            ],
            "walk": [("narr", "On the way home the sky finally decides. It is a fine rain, the kind that makes umbrellas unnecessary and excuses necessary."),
                     ("mc", "(Hikari is under hers. I am under mine. We are two rooms again, walking the same street.)")],
            "dinner": [
                ("father", "Did it rain?"),
                ("mc", "It is raining. It was going to all day."),
                ("father", "The news was right for once."),
                ("mother", "Eat before it gets cold. Rain waits for no one, but dinner does."),
            ],
            "night_a": [
                ("hikari", "Did the umbrella behave?"),
                ("mc", "It rained on me a little. You were right about pointing it at yourself."),
                ("hikari", "I was right about a lot of things today. The trick is not mentioning them."),
            ],
            "night_b": [
                ("hikari", "You walked in the rain like a person who has accepted the weather."),
                ("mc", "I have stopped fighting it. The umbrella does the fighting now."),
                ("hikari", "That is what umbrellas are for. And men."),
            ],
            "night_c": [
                ("narr", "I say nothing. The rain on the window is the city saying something I almost understand."),
                ("hikari", "Rain is just the sky doing its laundry. You will learn to like it."),
            ],
            "notebook": "(Cooking is a verb you perform by naming it. I think of the kitchen at night.)",
            "desk": "the rain on the window",
            "close": [("narr", "I turn off the lamp. The rain keeps going. Somewhere a gutter is doing its one job very well.")],
            "remember_a": "told her the umbrella behaved, mostly",
            "remember_b": "told her he had stopped fighting the weather",
        },

        25: {
            "title": "The sorting",
            "morning": [
                ("narr", "Saturday. No bell, no platform, no reason to be anywhere before ten."),
                ("narr", "Mother is already up, laying out the week's sorting on the kitchen floor like a card game she has played a thousand times."),
                ("mc", "(Burnable, unburnable, bottles, cans, paper. A whole taxonomy in three bags.)"),
            ],
            "kitchen": [
                ("mother", "You are up. Good. The burnable bag is full and my back is not what it was."),
                ("mc", "I can carry it down."),
                ("mother", "You can learn which bag is which first. That is the real job."),
            ],
            "lesson": [
                ("hikari", "Gomi. Trash. Burnable is red, unburnable is the other one, bottles and cans get rinsed first."),
                ("mc", "Rinsed? For trash?"),
                ("hikari", "The truck drivers know. Everyone knows. The bags are a language and we are both beginners."),
                ("mc", "(Even garbage has grammar here. Especially garbage, maybe.)"),
            ],
            "off": [
                ("narr", "No class. I carry the burnable bag down and back, and the whole errand takes four minutes and feels like a shift."),
                ("narr", "Hikari is at the table with a book and a tea. She does not perform being busy. That is its own kind of company."),
            ],
            "walk": [("narr", "The afternoon is mine. I walk the long way past the river and do not check the time once."),
                     ("mc", "(A day with no schedule is a room with no walls. I keep almost leaving it.)")],
            "dinner": [
                ("father", "A day off."),
                ("mc", "A day off."),
                ("father", "What did you do with it?"),
                ("mc", "Carried trash. Sat by a river. It was enough."),
                ("father", "That is a fuller answer than most people give on a Saturday."),
            ],
            "night_a": [
                ("hikari", "Did the bags make sense?"),
                ("mc", "Burnable, unburnable, bottles. I could run the station by now."),
                ("hikari", "You could. That is the point of errands. They are small ceremonies."),
            ],
            "night_b": [
                ("hikari", "You were quiet today. The good quiet or the other?"),
                ("mc", "The kind where the day was already complete."),
                ("hikari", "I know that kind. It is rare. I hope there are more of them."),
            ],
            "night_c": [
                ("narr", "I say nothing. Saturday night sounds different. Softer. The city is resting its voice."),
                ("hikari", "Saturday is the city's day off too. We just do not admit it."),
            ],
            "notebook": "(Even garbage has grammar here. Especially garbage, maybe.)",
            "desk": "the weekend",
            "close": [("narr", "I turn off the lamp. Tomorrow the city goes back to work. Tonight it belongs to us.")],
        },

        30: {
            "title": "The slurp",
            "morning": [
                ("narr", "Thursday again. The rain the forecast promised all week never came. The sky has been holding its breath."),
                ("narr", "At breakfast Mother puts a bowl of udon in front of me and watches to see if I will do the thing."),
                ("mc", "(The thing being slurping. The loud, committed, slightly embarrassing thing.)"),
            ],
            "chat_note": [("mc", "(Tanaka's shift reminder is already in my pocket. Four hours this afternoon. I keep touching the notification like a coin.)")],
            "kitchen": [
                ("mother", "Eat while it is hot. Udon waits for no one, but it forgives everyone."),
                ("father", "He will slurp it like a man who has never been to Japan."),
                ("mc", "I have been in Japan for a month now. I have opinions about noodles."),
            ],
            "lesson": [
                ("hikari", "Slurping. Yes, it is allowed. It is expected, even. The noodles are hot and the slurp cools them."),
                ("mc", "It sounds like a vacuum."),
                ("hikari", "It sounds like appreciation. The line between rudeness and enthusiasm is just volume and intent."),
                ("mc", "(So I should slurp louder. To show I mean it.)"),
            ],
            "campus": [
                ("narr", "The lecture hall smells like old wood and old coffee. A window is open and the rain keeps trying to get in."),
                ("mc", "(Somewhere a vending machine is humming. I have started hearing them everywhere. They are the city's heartbeat made audible.)"),
            ],
            "walk": [("narr", "I slurp my udon leftovers standing up, loudly, on the way home. Nobody looks twice."),
                     ("mc", "(I have learned to be loud about soup. It is the first Japanese thing that feels like mine.)")],
            "dinner": [
                ("father", "How was the udon?"),
                ("mc", "Good. I slurped it properly."),
                ("father", "Properly."),
                ("mother", "That is the highest praise in this house."),
                ("mc", "(It is the only praise in this house. I will take it.)"),
            ],
            "night_a": [
                ("hikari", "Did you slurp?"),
                ("mc", "Loudly. On the street. Like a local."),
                ("hikari", "Like a tourist who read the manual. But the manual is right, so it counts."),
            ],
            "night_b": [
                ("hikari", "You are getting braver in small ways."),
                ("mc", "The udon helped. Soup is a low-stakes courage."),
                ("hikari", "Everything good here starts low-stakes. That is why it works."),
            ],
            "night_c": [
                ("narr", "I say nothing. The rain has stopped. The city smells like it has been rinsed."),
                ("hikari", "After rain, Tokyo smells like metal and possibility. I think it is the trams."),
            ],
            "notebook": "(I have learned to be loud about soup. It is the first Japanese thing that feels like mine.)",
            "desk": "the rinsed city",
            "close": [("narr", "I turn off the lamp. Tomorrow is Friday. The week is almost a shape I recognize.")],
        },

        31: {
            "title": "The queue",
            "morning": [
                ("narr", "Friday. The week has a shape now: Monday is a wall, Wednesday is a door, Friday is a small vacation."),
                ("narr", "At the station the queue for the ticket gate is already forming before the train arrives. Nobody pushes. Nobody checks if anyone else is pushing."),
                ("mc", "(It is a line that maintains itself, like a flock of birds with rules nobody wrote down.)"),
            ],
            "chat_note": [("mc", "(The phone buzzes. Hikari: 'Queue with your eyes open today. Watch how they merge.' I did not know she was watching me watch queues.)")],
            "kitchen": [
                ("mother", "Bread or rice?"),
                ("mc", "Bread. I have earned toast."),
                ("father", "Toast is a meal for people who have decided the day is manageable."),
                ("mc", "(He is not wrong. The toast is exactly the size of my ambition today.)"),
            ],
            "lesson": [
                ("hikari", "The queue. In Japan it is not a line, it is a contract."),
                ("mc", "What happens if you break it?"),
                ("hikari", "Nothing happens. That is the miracle. Everyone polices it for free, forever, and nobody gets thanked."),
                ("mc", "(It is the opposite of the combini. There, the rules were six questions. Here, the rule is invisible and everyone follows it.)"),
            ],
            "lecture": {
                "intro": [
                    ("murakami", "Today: the announcement. Every station has a voice that tells you nothing important and means everything."),
                    ("murakami", "'Anzen no tame, densha no naka de o-nimotsu o otana ni tsukete kudasai.' For your safety, please hold your belongings."),

                ],
                "a": [
                    ("murakami", "Listen for the melody, not the words. The tune is the message. The words are just the excuse for the tune."),
                    ("mc", "(So the city hums its rules. The melody is how it says 'you are safe, keep going.')")],
                "b": [
                    ("murakami", "Why does a city need a voice? Because a crowd is a question, and the announcement is the answer: you are still inside the plan."),
                    ("mc", "(I think of the hum of the vending machine. Maybe it is the same voice, smaller.)")],
                "c": [
                    ("murakami", "Write down one announcement you heard this week. Any station, any line."),
                    ("mc", "(I write: 'The train will arrive shortly.' It is the most hopeful sentence in the language.)"),
                ],
            },
            "campus": [
                ("narr", "The campus is doing its Friday thing: half the students are already gone, the other half are pretending they have somewhere to be."),
                ("mc", "(The library is full of people who have decided to be somewhere else mentally. I fit right in.)"),
            ],
            "walk": [("narr", "On the platform home I stand in the queue with my hands in my pockets and let the order hold me."),
                     ("mc", "(It is the first time I have stood still without wanting to be somewhere else.)")],
            "dinner": [
                ("father", "Friday. The week is almost done."),
                ("mc", "Three more days. Then Saturday."),
                ("mother", "Saturday is not a holiday. It is just a different kind of work."),
                ("mc", "(She is right. Saturday has its own queue: the laundry, the shopping, the calls.)"),
            ],
            "night_a": [
                ("hikari", "Did you queue properly?"),
                ("mc", "I did not push once. I want it noted."),
                ("hikari", "It is noted. You are becoming a citizen of small systems."),
            ],
            "night_b": [
                ("hikari", "You stood still today. On the platform. Like a person who trusts the schedule."),
                ("mc", "I trust the queue more than the schedule. The queue is honest."),
                ("hikari", "That is the most Japanese thing you have ever said."),
            ],
            "night_c": [
                ("narr", "I say nothing. The city is doing its Friday quiet, the kind that precedes a weekend it is not sure it deserves."),
                ("hikari", "Friday nights smell like the week letting go. Can you smell it?"),
            ],
            "notebook": "(I write: 'The train will arrive shortly.' It is the most hopeful sentence in the language.)",
            "desk": "the queue",
            "close": [("narr", "I turn off the lamp. The week is almost a shape I recognize. I am almost a person who lives here.")],
        },

        32: {
            "title": "The card",
            "morning": [
                ("narr", "Saturday. The apartment is doing its weekend thing: Father is reading the paper with his whole body, Mother is on the phone with someone who sounds worried."),
                ("narr", "I make coffee and stand at the window. The city is doing its slow Saturday: fewer suits, more families, the same hum underneath."),
                ("mc", "(The hum is the constant. Everything else is weather.)"),
            ],
            "chat_note": [("mc", "(Sim's reminder is still in my head. Bring the camera. Wear the good jacket. I have neither ready yet.)")],
            "kitchen": [
                ("mother", "You look like you are thinking about work."),
                ("mc", "I am thinking about cards."),
                ("mother", "Cards?"),
                ("mc", "Business cards. The Japanese kind."),
            ],
            "lesson": [
                ("hikari", "Meishi. The business card. You give it with two hands, receive it with two hands, and never write on it in front of the person."),
                ("mc", "It is that formal?"),
                ("hikari", "It is the person's name and face in one object. To treat it casually is to treat the person casually."),
                ("mc", "(So the card is a small shrine. You bow to it before you read it.)"),
            ],
            "off": [
                ("narr", "No class. I walk to the station and buy a ticket I do not need, just to feel the machine accept me."),
                ("narr", "The ticket is a small rectangle of proof that I belong to a system. I put it in my pocket like a talisman."),
            ],
            "walk": [("narr", "The afternoon is a slow loop: station, bridge, river, back. I do not pick a destination. The city is the destination."),
                     ("mc", "(I have started to like the loop. It is the first place that does not ask me to be anywhere else.)")],
            "dinner": [
                ("father", "A quiet Saturday."),
                ("mc", "The best kind."),
                ("father", "Quiet is not empty. It is full of things not needing attention."),
                ("mc", "(He is learning to speak in aphorisms. Or I am learning to hear them.)"),
            ],
            "night_a": [
                ("hikari", "Did you think about the card?"),
                ("mc", "I imagined giving you one. Your name, my name, two hands."),
                ("hikari", "That is not how it works. But I like the picture."),
            ],
            "night_b": [
                ("hikari", "You are getting good at the small ceremonies."),
                ("mc", "The card, the queue, the slurp. I am collecting them like stamps."),
                ("hikari", "That is exactly what they are. Proof that you were here and paid attention."),
            ],
            "night_c": [
                ("narr", "I say nothing. Saturday night is the city's held breath before Sunday, which is the city's apology for Monday."),
                ("hikari", "You are becoming a poet. It is a side effect of staying."),
            ],
            "notebook": "(So the card is a small shrine. You bow to it before you read it.)",
            "desk": "the small ceremonies",
            "close": [("narr", "I turn off the lamp. The card is still in my pocket. I have not given it to anyone. I am not sure I want to.")],
        },

        34: {
            "title": "The machine",
            "morning": [
                ("narr", "Monday. The week resets. The city puts its suit back on and the trains fill with people who have forgotten Saturday happened."),
                ("narr", "At the combini on the corner I watch the morning regulars: the salaryman who buys the same onigiri, the student who buys the same coffee, the old woman who buys nothing but a paper bag."),
                ("mc", "(The machine knows them. The machine knows everything. I am starting to think the machine is the real shopkeeper.)"),
            ],
            "chat_note": [("mc", "(Tanaka's text: 'Shift this afternoon. Do not be late.' I have started to hear his voice in the punctuation.)")],
            "kitchen": [
                ("mother", "You look tired. The combini?"),
                ("mc", "The combini. And the week."),
                ("father", "The week is a machine. The combini is a smaller machine. You are learning to operate both."),
            ],
            "lesson": [
                ("hikari", "Vending machines. In Japan they are not machines, they are shrines."),
                ("mc", "That is a stretch."),
                ("hikari", "You put in money, you press a button, and it gives you exactly what you asked for. No small talk. No judgment. Perfect service."),
                ("mc", "(The vending machine is the combini's perfect employee. It never calls in sick, never chats, never forgets your order.)"),
            ],
            "campus": [
                ("narr", "The campus is doing its Monday reset: the library is full, the café is full, the benches are full of people pretending to study."),
                ("mc", "(I fit in. I am one of the people pretending. The pretending is the studying.)"),
            ],
            "walk": [("narr", "On the way home I stop at the vending machine and buy a coffee I do not need. The machine hums its approval."),
                     ("mc", "(It is the most reliable relationship I have in this city. It does not ask questions. It does not judge.)")],
            "dinner": [
                ("father", "The combini again?"),
                ("mc", "The combini. Tanaka says I am learning the register."),
                ("father", "The register. That is a word for a skill."),
                ("mc", "(I am learning to hear pride in my father's voice. It is a small sound, but it is there.)"),
            ],
            # The same table if he has never taken a shift. No penalty, no
            # lecture; Father only says the quiet version of the same thing.
            "dinner_no_shift": [
                ("father", "You did not go to the store today."),
                ("mc", "No. I walked."),
                ("father", "The register is not going to learn itself."),
                ("mc", "(He is not nagging. He is stating the weather. That is worse.)"),
            ],
            "night_a": [
                ("hikari", "Did the machine give you what you wanted?"),
                ("mc", "It gave me a coffee and a hum. I did not know I wanted the hum."),
                ("hikari", "That is what machines do. They give you the thing and the thing's ghost."),
            ],
            "night_b": [
                ("hikari", "You are becoming a regular. The city notices regulars."),
                ("mc", "I am a regular at the vending machine and the combini. I am a regular person now."),
                ("hikari", "That is not a small thing. Regular is a verb."),
            ],
            "night_c": [
                ("narr", "I say nothing. The city is doing its Monday hum, the hum that says 'you are expected, you are accounted for, you are safe.'"),
                ("hikari", "Monday is the city's morning prayer. We just call it a workday."),
            ],
            "notebook": "(The vending machine hums. It does not stop. It is the sound of a thing that has no opinion about you and will still be here tomorrow.)",
            "desk": "the hum",
            "close": [("narr", "I turn off the lamp. The vending machine outside is still humming. It will hum all night. It always does.")],
        },

        35: {
            "title": "The coffee shop",
            "morning": [
                ("narr", "Tuesday. The week has a rhythm now."),
                ("narr", "At the station there is a kissaten, an old coffee shop with a noren curtain and a menu written in calligraphy. I have been walking past it for weeks."),
                ("mc", "(Today I go in. The door is heavier than it looks.)"),
            ],
            "chat_note": [("mc", "(Hikari's text: 'Try the kissaten today. Tell me if the coffee is better than the machine's.' She is training me to notice things.)")],
            "kitchen": [
                ("mother", "You look like you have somewhere to be."),
                ("mc", "I have a coffee shop to investigate."),
                ("father", "A coffee shop. In Japan. That is either research or avoidance."),
                ("mc", "It is both. I am not sure which yet."),
            ],
            "lesson": [
                ("hikari", "Kissaten. Not 'coffee shop,' not 'cafe.' Kissaten. The old kind, with the siphon and the slow pour and the regulars who have been coming since before you were born."),
                ("mc", "How is it different?"),
                ("hikari", "A cafe is for working. A kissaten is for being. You go there to exist, not to produce."),
        ("mc", "(So the kissaten is a room where nothing is asked of you. I needed one.)"),
            ],
            "lecture": {
                "intro": [
                    ("murakami", "Today: kigo. Seasonal words. The words that only exist in one season."),
                    ("murakami", "'Shigure' is the winter rain that falls on withered leaves. It has no English word because English does not need it."),
                ],
                "a": [
                    ("murakami", "The language keeps what the weather keeps. If a word dies, it is because the season it belonged to has died too."),
                    ("mc", "(So kigo is a kind of calendar. A calendar of feelings, not dates.)"),
                ],
                "b": [
                    ("murakami", "Why does a language need words for one kind of rain? Because that rain matters. The word is proof."),
                    ("mc", "(I think of the rain that never quite stopped this month. Maybe it had a name I did not know.)"),
                ],
                "c": [
                    ("murakami", "Write down a season word from your own language. Any word that only works in one month."),
                    ("mc", "(I write 'monsoon.' It is not the same, but it is close. Both are rains that mean something.)"),
                ],
            },
            "campus": [
                ("narr", "The campus is doing its Tuesday thing: the lecture hall is full, the courtyard is full of people eating lunch like it is a competition."),
                ("mc", "(I eat alone on a bench. It is not lonely. It is just efficient.)"),
            ],
            "walk": [("narr", "On the way home I stop at the kissaten. The coffee is better than the machine's. The regulars nod at me like I belong."),
                     ("mc", "(I do not belong yet. But I am learning the way regulars learn: by coming back.)")],
            "dinner": [
                ("father", "The coffee shop?"),
                ("mc", "The kissaten. It is different."),
                ("father", "Different how?"),
                ("mc", "It is for being, not for working. I did not know that was a category."),
                ("mother", "Now you do. Eat your dinner. You are becoming a connoisseur of rooms."),
            ],
            "night_a": [
                ("hikari", "Was the coffee better?"),
                ("mc", "It was slower. The machine is fast. The kissaten is slow. Slow is better."),
                ("hikari", "That is the whole lesson. Speed is not the same as quality."),
            ],
            "night_b": [
                ("hikari", "You are collecting places now. The combini, the river, the kissaten."),
                ("mc", "I am building a map of places that do not ask anything of me."),
                ("hikari", "That is the most important kind of map."),
            ],
            "night_c": [
                ("narr", "I say nothing. The city is doing its Tuesday quiet, the kind that knows Wednesday is coming but is not ready to admit it."),
                ("hikari", "Tuesday is the city's deep breath. We just call it a school day."),
            ],
            "notebook": "(I write 'monsoon.' It is not the same, but it is close. Both are rains that mean something.)",
            "desk": "the slow cup",
            "close": [("narr", "I turn off the lamp. The kissaten is still open. The regulars are still there. I will be back tomorrow.")],
        },

        36: {
            "title": "The gap",
            "morning": [
                ("narr", "Wednesday. The week is taking shape."),
                ("narr", "Chef's place is closed today. The sign on the door says 'Closed Wednesdays.' I have started to plan my week around his closure like it is a holiday."),
                ("mc", "(It is not a holiday. It is just a day when the soup does not exist. I miss it anyway.)"),
            ],
            "chat_note": [("mc", "(Chef's WIRE: 'The soup is different on Thursdays. Come taste it before it becomes Thursday.' Today is Wednesday. The soup is elsewhere.)")],
            "kitchen": [
                ("mother", "You look like you have a plan."),
                ("mc", "I am planning to miss the soup."),
                ("mother", "That is a plan?"),
                ("mc", "It is the only plan that involves Chef."),
            ],
            "lesson": [
                ("hikari", "Ma. The gap. The space between two things that is not empty, just unoccupied."),
                ("mc", "Like the space between notes?"),
                ("hikari", "Exactly. The silence between the notes is what makes the music. Ma is that silence, made visible."),
                ("mc", "(So the gap is not nothing. It is the thing that holds the somethings apart. I think of the space between Hikari and me, and it is full of ma.)"),
            ],
            "campus": [
                ("narr", "The campus is doing its Wednesday thing: the lecture hall is full, the courtyard is empty, the library is doing its best impression of a fortress."),
                ("mc", "(I sit in the courtyard and do nothing. It is the most productive nothing I have done all week.)"),
            ],
            "walk": [("narr", "On the way home I take the long way past the river. The water is doing its Wednesday thing: moving, indifferent, beautiful."),
                     ("mc", "(The river does not care about my schedule. It is the only thing in this city that does not perform for me.)")],
            "dinner": [
                ("father", "Chef's closed?"),
                ("mc", "Wednesdays. I forgot."),
                ("father", "You forgot because you were thinking about the soup. That is how attachments work."),
                ("mc", "(He is right. I planned my week around a closed door. That is either devotion or a problem.)"),
            ],
            "night_a": [
                ("hikari", "Did you miss the soup?"),
                ("mc", "I planned my week around its absence. That seems excessive."),
                ("hikari", "It is not excessive. It is the opposite. You are learning to want things."),
            ],
            "night_b": [
                ("hikari", "You took the long way home. Past the river."),
                ("mc", "The river is doing its own thing. I just watched."),
                ("hikari", "That is the best way to watch it. It does not perform for audiences."),
            ],
            "night_c": [
                ("narr", "I say nothing. The gap between Wednesday and Thursday is a small ma, and I am learning to sit in it."),
                ("hikari", "The gap is where the good things hide. You are learning to look."),
            ],
            "notebook": "(Ma. The gap between two things. The silence that is not empty. The pause that is not a pause. I wrote it down and then sat with it for a while.)",
            "desk": "the gap",
            "close": [("narr", "I turn off the lamp. The soup is elsewhere. Tomorrow it will be back. I will be ready.")],
        },

        37: {
            "title": "The curtain",
            "morning": [
                ("narr", "Thursday. The days are starting to feel shorter."),
                ("narr", "On the way to the station I pass a shop with a noren curtain: a blue one with a white circle. I have seen it every day for weeks and never asked what it means."),
                ("mc", "(Today I ask. Hikari is already ahead of me.)"),
            ],
            "chat_note": [("mc", "(Sim's Thursday reminder: 'Bring the camera. Wear the good jacket.' I have the jacket. The camera is still a question.)")],
            "kitchen": [
                ("mother", "You are smiling. What is it?"),
                ("mc", "A curtain. A blue one with a circle."),
                ("mother", "Noren. They mean different things. The circle is a family crest, or a moon, or just a design."),
                ("mc", "(She knows. Of course she knows. She has been here her whole life.)"),
            ],
            "lesson": [
                ("hikari", "Noren. The curtain that says 'we are open' without saying it. Blue is trust, white is purity, the circle is a family mark."),
                ("mc", "So the curtain is a sign?"),
                ("hikari", "It is a promise. The shop is saying 'you may enter, you will be welcome.' It is the first thing you see and the last thing you forget."),
                ("mc", "(The noren is a small gate. It says 'this is a place' before you have decided to be in it.)"),
            ],
            "lecture": {
                "intro": [
                    ("murakami", "Today: the city as a text. Every sign, every curtain, every queue is a sentence."),
                    ("murakami", "You have been reading the city for a month. Today we learn to read it aloud."),
                ],
                "a": [
                    ("murakami", "Look at the noren again. What does it say? Not the words, the meaning. 'Open.' 'Welcome.' 'This is a place.'"),
                    ("mc", "(It says 'you belong here.' Which is a lie and a truth at the same time.)"),
                ],
                "b": [
                    ("murakami", "Why does a city need signs? Because a city is a text that never stops being written. The signs are the footnotes."),
                    ("mc", "(I think of the vending machine's hum. It is a footnote that never ends.)"),
                ],
                "c": [
                    ("murakami", "Write down one sign you saw today. Any sign. Read it like a sentence."),
                    ("mc", "(I write 'Open.' It is the shortest sentence in the language. It means 'you may enter, you will not be harmed.' It is also a lie, sometimes.)"),
                ],
            },
            "campus": [
                ("narr", "The campus is doing its Thursday thing: the lecture hall is full, the courtyard is full of people who look like they are studying but are actually just being there."),
                ("mc", "(I am one of them. The being-there is the studying. The studying is the being-there.)"),
            ],
            "walk": [("narr", "On the way home I stop at the shop with the noren. The curtain is still blue. The circle is still white. I have not gone in yet."),
                     ("mc", "(The curtain is a promise. I am not ready to collect on it. But I am learning to read the promises.)")],
            "dinner": [
                ("father", "The curtain?"),
                ("mc", "The noren. It is a sign. It says 'open' without saying it."),
                ("father", "And you are reading signs now?"),
                ("mc", "I am learning to. The city is a text. I am getting literate."),
            ],
            "night_a": [
                ("hikari", "Did you go into the shop?"),
                ("mc", "I did not. I just read the curtain."),
                ("hikari", "That is enough. The curtain is the invitation. Going in is the answer."),
            ],
            "night_b": [
                ("hikari", "You are learning to read the city. It is a dangerous skill."),
                ("mc", "Why dangerous?"),
                ("hikari", "Because once you can read it, you can see what it is hiding."),
            ],
            "night_c": [
                ("narr", "I say nothing. The noren is still blue. The city is still writing. I am still reading."),
                ("hikari", "The city is a book that never ends. You are learning to turn the pages."),
            ],
            "notebook": "(I write 'Open.' It is the shortest sentence in the language. It means 'you may enter, you will not be harmed.' It is also a lie, sometimes.)",
            "desk": "the curtain",
            "close": [("narr", "I turn off the lamp. The noren is still blue. Tomorrow I might go in. Or I might just read it again.")],
        },

        38: {
            "title": "The last train",
            "morning": [
                ("narr", "Friday. The week has a pattern now."),
                ("narr", "At the station the last-train announcement is already playing: 'The last train will depart at 12:47.' I have started to listen for it the way other people listen for a name."),
                ("mc", "(The last train is a deadline. It is the city's way of saying 'you have until now.')"),
            ],
            "chat_note": [("mc", "(Aya's text: 'New menu item. The omurice has a secret ingredient. You may guess.' I am guessing 'regularity.')")],
            "kitchen": [
                ("mother", "You look like you are counting something."),
                ("mc", "The trains. The last one."),
                ("father", "The last train is a boundary. It says 'the day is ending, you may go home now.'"),
                ("mc", "(He says things like that now. I used to think he was being difficult. Now I think he is being precise.)"),
            ],
            "lesson": [
                ("hikari", "Shūden. The last train. It runs after everyone else has gone home, and it is the only train that is honest."),
                ("mc", "Honest how?"),
                ("hikari", "It does not pretend there will be another one. It says 'this is it, get on or stay.'"),
                ("mc", "(The last train is the city's final word. It does not negotiate.)"),
            ],
            "campus": [
                ("narr", "The campus is thinning out. The people still here are the ones who stayed late."),
                ("mc", "(I sit on a bench and watch them. They look like they are waiting for something, or someone.)"),
            ],
            "walk": [("narr", "On the platform home I check the time. 12:32. The last train is at 12:47. I have fifteen minutes."),
                     ("mc", "(Fifteen minutes is a small eternity. I could do anything. I choose to stand still and watch the city breathe.)")],
            "dinner": [
                ("father", "The last train?"),
                ("mc", "12:47. I almost missed it."),
                ("father", "Almost is the same as did not. The last train does not care about almost."),
                ("mc", "(He is right. The last train is the city's final word. It does not negotiate.)"),
                # Word for word the line he said on Day 34. Nothing about the
                # delivery changes; only the glitch and Hikari notice.
                ("father", "The week is a machine. The combini is a smaller machine. You are learning to operate both."),
            ],
            "leak_after_dinner": [
                ("hikari", "Did your father say that already?"),
                ("mc", "He did. On Monday. Word for word."),
                ("hikari", "Father repeats himself. It is what fathers do."),
                ("mc", "(She says it the way you explain a thing you have explained before. I let it go. The sound was wrong. I do not know how.)"),
            ],
            "night_a": [
                ("hikari", "Did you catch the last train?"),
                ("mc", "I did. With fifteen minutes to spare. I stood still and watched the city."),
                ("hikari", "That is the best way to catch it. The last train is a boundary. You crossed it."),
            ],
            "night_b": [
                ("hikari", "You are learning the city's boundaries. The last train, the queue, the card."),
                ("mc", "I am learning to respect them. The boundaries are what make the city safe."),
                ("hikari", "That is the part most people miss. The edges are what let you relax inside."),
            ],
            "night_c": [
                ("narr", "I say nothing. The last train has gone. The city is doing its Friday night thing: quiet, relieved, a little sad."),
                ("hikari", "Friday night is the city's exhale. We just call it the weekend."),
            ],
            "notebook": "(I wrote 'the salaryman's nod.' It was hiding exhaustion. It was also hiding hope. Both at once.)",
            "desk": "the last train",
            "close": [("narr", "I turn off the lamp. The last train has gone. Tomorrow there will be another one. That is the promise.")],
        },

        39: {
            "title": "The cloth",
            "morning": [
                ("narr", "Saturday. The week has a rhythm now."),
                ("narr", "The sky has been undecided all week. Today it settled on a fine mist that makes the city look like a memory."),
                ("mc", "(The city is doing its Saturday mist. I am doing my Saturday walking. We are both being vague.)"),
            ],
            "chat_note": [("mc", "(Hikari's text: 'The mist is nice today. Come see it with me.' I am already dressed. I did not plan to be.)")],
            "kitchen": [
                ("mother", "You look like you are heading out."),
                ("mc", "I am going to see the mist."),
                ("mother", "With Hikari?"),
                ("mc", "With Hikari. She texted me."),
            ],
            "lesson": [
                ("hikari", "Furoshiki. The wrapping cloth. Before there were bags, there was cloth. You wrap the thing, you carry it, you unwrap it at home."),
                ("mc", "It is just a cloth?"),
                ("hikari", "It is a promise. The cloth says 'this thing matters enough to be wrapped.' It is the first form of care."),
                ("mc", "(So the furoshiki is a small ceremony. You wrap the thing and you say 'this is yours, this is safe.')"),
            ],
            "off": [
                ("narr", "No class. Hikari is already at the door with her umbrella. The mist is doing its Saturday thing: soft, everywhere, indecisive."),
                ("narr", "We walk to the river and back. The mist makes the city look like a memory of itself."),
            ],
            "walk": [("narr", "The afternoon is a slow loop: river, bridge, station, back. The mist makes everything look like it is being remembered."),
                     ("mc", "(I am being remembered too. The mist is doing its job on me.)")],
            "dinner": [
                ("father", "The mist?"),
                ("mc", "The mist. It is nice. Hikari and I walked in it."),
                ("father", "Mist is just rain that has not decided to fall. You are learning to like the undecided."),
                ("mc", "(He is right. The mist is the city's way of saying 'maybe.' I am learning to say maybe too.)"),
            ],
            "night_a": [
                ("hikari", "Did the mist behave?"),
                ("mc", "It did. It was soft and everywhere. It made the city look like a memory."),
                ("hikari", "That is what mist does. It makes the present look like the past. It is a kind of time travel."),
            ],
            "night_b": [
                ("hikari", "You are learning to like the undecided. The mist, the queue, the card."),
                ("mc", "The mist taught me that maybe does not need resolving. It just needs walking through."),
                ("hikari", "That is the lesson of the mist. You do not solve it. You let it hold you."),
            ],
            "night_c": [
                ("narr", "I say nothing. The mist is doing its Saturday night thing: soft, everywhere, indecisive."),
                ("hikari", "Saturday is the city's held breath. Monday is already in the room."),
            ],
            "notebook": "(The mist taught me that maybe does not need resolving. It just needs walking through.)",
            "desk": "the mist",
            "close": [("narr", "I turn off the lamp. The mist is still doing its thing. Tomorrow it will be Sunday. The mist will be gone. I will miss it.")],
        },

        40: {
            "title": "The song",
            "morning": [
                ("narr", "Sunday. The week is almost over and I have stopped counting it."),
                ("narr", "The mist from Saturday finally decided to fall. It is a proper rain now, the kind that makes the city look like it is being washed."),
                ("mc", "(The city is doing its Sunday rain. I am doing my Sunday reading. We are both being washed.)"),
            ],
            "chat_note": [("mc", "(Sim's text: 'Sunday. Bring the camera. The rain is good for photos.' I have the camera. The rain is better.')")],
            "kitchen": [
                ("mother", "You look like you are thinking."),
                ("mc", "I am planning to read. And maybe take photos."),
                ("mother", "With Sim?"),
                ("mc", "With Sim. He texted me."),
            ],
            "lesson": [
                ("hikari", "Karaoke. The empty room where you sing alone. It is not embarrassing because nobody is listening. It is the purest form of performance."),
                ("mc", "That sounds terrifying."),
                ("hikari", "It is. But it is also free. Nobody judges you because nobody is there. It is the only room where you can be anyone."),
        ("mc", "(The karaoke box is a room where the self is optional. I could use one.)"),
            ],
            "off": [
                ("narr", "No class. The rain is doing its Sunday thing: steady, indifferent, beautiful. I read in the window seat and watch the city blur."),
                ("narr", "Sim's text is still on my phone. I have not replied. The rain is a better conversation."),
            ],
            "walk": [("narr", "The afternoon is a slow loop: window, book, tea, window. The rain does the walking for me."),
                     ("mc", "(The rain is the only thing moving. I am the only thing still. We are both being washed.)")],
            "dinner": [
                ("father", "The rain?"),
                ("mc", "The rain. It is nice. I read in it."),
                ("father", "Rain is just water doing its job. You are learning to like the jobs that do not ask questions."),
                ("mc", "(He is right. The rain does not ask questions. It just falls. It is the most honest thing in the city.)"),
            ],
            "night_a": [
                ("hikari", "Did the rain behave?"),
                ("mc", "It did. It was steady and indifferent. It made the city look washed."),
                ("hikari", "That is what rain does. It washes the city and the people in it. It is a kind of baptism."),
            ],
            "night_b": [
                ("hikari", "You are learning to like the things that do not ask questions. The rain, the mist, the queue."),
                ("mc", "Rain asks nothing of me. It just falls. That is the whole contract."),
                ("hikari", "And you are learning to keep your end of it. That is rarer than you think."),
            ],
            "night_c": [
                ("narr", "I say nothing. The rain is doing its Sunday night thing: steady, indifferent, beautiful."),
                ("hikari", "Rain on a roof is the city humming to itself. Listen long enough and it starts to sound like a voice."),
            ],
            "notebook": "(He is right. The rain does not ask questions. It just falls. It is the most honest thing in the city.)",
            "desk": "the rain",
            "close": [("narr", "I turn off the lamp. The rain is still doing its thing. Tomorrow it will be Monday. The rain will be gone. I will miss it.")],
        },

        42: {
            "title": "The water",
            "morning": [
                ("narr", "Tuesday. The week has settled into its routine."),
                ("narr", "It rained on Sunday and the city forgot by Monday. The gutters have been dry since. The city is doing its Tuesday thing: bright, clean, a little smug about it."),
                ("mc", "(The city is showing off. I do not blame it.)"),
            ],
            "chat_note": [("mc", "(Hikari's text: 'The rain stopped. Come see the clean city with me.' I am already dressed. I did not plan to be.)")],
            "kitchen": [
                ("mother", "You look like you are going somewhere."),
                ("mc", "I am going to see the clean city."),
                ("mother", "With Hikari again?"),
                ("mc", "With Hikari. She is already there."),
            ],
            "lesson": [
                ("hikari", "Temizu. The purification at the shrine. You wash your hands and mouth with the water from the ladle. It is not religious, it is hygienic. But it is also symbolic."),
                ("mc", "Symbolic how?"),
                ("hikari", "You are washing away the impurities of the everyday. The city, the work, the worry. You are saying 'I am ready to be here.'"),
        ("mc", "(The temizu is a small baptism. You wash your hands and you say 'I am ready.' )"),
            ],
            "lecture": {
                "intro": [
                    ("murakami", "Today: the particle 'wa.' The topic marker. The word that says 'this is what we are talking about.'"),
                    ("murakami", "'Watashi wa' is 'I, as the topic.' 'Watashi ga' is 'I, as the subject.' The difference is the whole sentence."),
                ],
                "a": [
                    ("murakami", "Try it: 'Hikari wa kimasu.' Hikari-as-for-is-coming. Now 'Hikari ga kimasu.' Hikari-is-coming. Feel the shift?"),
                    ("mc", "(One is context. The other is news. The particle decides what matters.)"),
                ],
                "b": [
                    ("murakami", "Why does a language need two ways to say 'I'? Because there are two ways to be a person: as the topic of someone else's life, or as the subject of your own."),
                    ("mc", "(I am trying to be the topic of my own life. The city keeps making me the subject of its schedule.)"),
                ],
                "c": [
                    ("murakami", "Write down one sentence you said today. Circle the particle. Ask yourself who it made the subject."),
                    ("mc", "(I wrote 'Watashi wa Tanaka ga oshiete kureru.' I-as-for, Tanaka teaches me. The 'wa' makes me the topic. The 'ga' makes Tanaka the subject. Japanese is full of gifts.)"),
                ],
            },
            "campus": [
                ("narr", "The campus is doing its Tuesday thing: the lecture hall is full, the courtyard is full of people who look like they are studying but are actually just being there."),
                ("mc", "(I am one of them. Being there is the work.)"),
            ],
            "walk": [("narr", "On the way home I stop at the shrine. The temizu is cold. The water is clean. I wash my hands and I say 'I am ready.'"),
                     ("mc", "(The water is cold. I say it anyway.)")],
            # Only plays once the twelfth door has happened (Day 41). Yesterday
            # a handle was warm where no door was; today the cold water is real.
            "echo": [
                ("narr", "I hold my wrists under the cold water longer than the order requires. The cold stops being a surprise and becomes a place."),
                ("mc", "(A handle was warm yesterday where there was no door. This is cold, and it is here. I will take what is here.)"),
                ("hikari", "You washed twice."),
                ("mc", "Once was not enough."),
                ("hikari", "The water does not count. It just runs."),
            ],
            "dinner": [
                ("father", "The shrine?"),
                ("mc", "The shrine. I washed my hands. I said 'I am ready.'"),
                ("father", "Ready for what?"),
                ("mc", "I do not know yet. The washing comes first."),
            ],
            "night_a": [
                ("hikari", "Did you wash your hands?"),
                ("mc", "I did. I said 'I am ready.' I am not sure what I am ready for."),
                ("hikari", "That is the point. You do not have to know. The washing is the answer."),
            ],
            "night_b": [
                ("hikari", "You are learning to say 'I am ready' and mean it."),
                ("mc", "'I am ready' is not a claim. It is a direction. You say it and then you walk."),
                ("hikari", "And you walked. That is the part people skip. The saying is easy. The walking is the proof."),
            ],
            "night_c": [
                ("narr", "I say nothing. The temizu is still cold. The water is still clean."),
                ("hikari", "The shrine does not keep score. It just offers the water. What you do with it is yours."),
            ],
            "notebook": "(The water is cold. I say it anyway.)",
            "desk": "the water",
            "close": [("narr", "I turn off the lamp. The temizu is still cold. The water is still clean. I am still learning to say 'I am ready.' Tomorrow I will say it again.")],
        },

        43: {
            "title": "The paw",
            "morning": [
                ("narr", "Wednesday. The week has a weight to it now, the good kind."),
                ("narr", "The shop with the maneki-neko is open today. The cat is still in the window, paw raised, waiting for someone to walk in."),
                ("mc", "(The cat has been waiting longer than I have. It does not seem to mind.)"),
            ],
            "chat_note": [("mc", "(Chef's text: 'The soup is different on Thursdays. Come taste it before it becomes Thursday.' Today is Wednesday. The soup is elsewhere.)")],
            "kitchen": [
                ("mother", "You look like you are planning."),
                ("mc", "I am planning to see the maneki-neko."),
                ("mother", "The beckoning cat?"),
                ("mc", "The beckoning cat. It is everywhere. I want to understand it."),
            ],
            "lesson": [
                ("hikari", "Maneki-neko. The beckoning cat. The paw that is raised is the paw that is beckoning. The paw that is down is the paw that is receiving."),
                ("mc", "So the cat is saying 'come here' and 'thank you' at the same time?"),
                ("hikari", "Exactly. It is the perfect host. It beckons you in and thanks you for coming. It is the city in miniature."),
        ("mc", "(The maneki-neko is a small host. It beckons and it receives.)"),
            ],
            "campus": [
                ("narr", "The campus is doing its Wednesday thing: the lecture hall is half empty, the courtyard is quiet, the library is doing its best to look busy."),
                ("mc", "(I sit in the courtyard and do nothing. The cat in the window is doing the same.)"),
            ],
            "walk": [("narr", "On the way home I stop at the shop with the maneki-neko. The cat is still beckoning. The paw is still raised. I have not gone in yet."),
                     ("mc", "(The cat is a promise. I am not ready to collect on it. But I am learning to read the promises.)")],
            "dinner": [
                ("father", "The cat?"),
                ("mc", "The maneki-neko. It beckons and it receives. That is the whole job."),
                ("father", "And you are learning to be hosted?"),
                ("mc", "I am learning to be a guest. The city is hosting me. I am learning to say thank you."),
            ],
            "night_a": [
                ("hikari", "Did you see the cat?"),
                ("mc", "I did. It is still beckoning. I am still learning to be a guest."),
                ("hikari", "That is the best way to see it. The cat is a promise. You are learning to collect on it."),
            ],
            "night_b": [
                ("hikari", "You are learning to be a guest. The city is hosting you. You are learning to say thank you."),
                ("mc", "Thank you is not a payment. It is a door left open."),
                ("hikari", "And you are learning to walk through it. Slowly. That is the hard part nobody teaches."),
            ],
            "night_c": [
                ("narr", "I say nothing. The maneki-neko is still beckoning. The city is still hosting."),
                ("hikari", "The cat has been beckoning for a hundred years. It does not hurry. Neither should you."),
            ],
            "notebook": "(The maneki-neko lifts one paw. It does not wave. It holds. There is a difference. I am learning the difference.)",
            "desk": "the paw",
            "close": [("narr", "I turn off the lamp. The maneki-neko is still beckoning. The city is still hosting. I am still learning to say thank you. Tomorrow I will say it again.")],
        },

        44: {
            "title": "The button",
            "morning": [
                ("narr", "Thursday. The week has a shape now, and a broken elevator."),
                ("narr", "The elevator in the station has a sign on it: 'Out of service.' Nobody seems upset. They take the stairs like it is the plan."),
                ("mc", "(The city does not apologize for broken things. It just routes around them.)"),
            ],
            "chat_note": [("mc", "(Sim's text: 'Thursday. Bring the camera. Wear the good jacket.' I have the jacket. The camera is still a question.')")],
            "kitchen": [
                ("mother", "You look like you are up to something."),
                ("mc", "I am planning to see the elevator."),
                ("mother", "The elevator?"),
                ("mc", "The elevator. It is in every building. I want to understand why it bothers me."),
            ],
            "lesson": [
                ("hikari", "The elevator button. You press it once to call the elevator. You press it again to close the doors. It is the only place where pressing a button twice is polite."),
                ("mc", "So the button is a conversation?"),
                ("hikari", "Exactly. The first press says 'I am here.' The second press says 'I am ready.' It is the smallest conversation in the city."),
        ("mc", "(The elevator button is a small conversation. It says 'I am here' and 'I am ready.')"),
            ],
            "lecture": {
                "intro": [
                    ("murakami", "Today: the silence between stations. The announcements that tell you nothing and mean everything."),
                    ("murakami", "'The train will arrive shortly.' It is not a promise. It is a permission. You may relax now."),
                ],
                "a": [
                    ("murakami", "The silence between stations is the city's held breath. It is the moment before the next thing happens."),
                    ("mc", "(I think of the gap between Wednesday and Thursday. It is a small ma, and I am learning to sit in it.)"),
                ],
                "b": [
                    ("murakami", "Why does a city need silences? Because a city is a conversation, and conversations need pauses."),
                    ("mc", "(I think of the hum of the vending machine. It is a pause that never ends.)"),
                ],
                "c": [
                    ("murakami", "Write down one silence you heard today. Any silence. Ask yourself what it was holding."),
                    ("mc", "(I wrote 'the silence between stations.' It is holding the next station. It is holding me.)"),
                ],
            },
            "campus": [
                ("narr", "The campus is doing its Thursday thing: the lecture hall is full, the courtyard is full of people who are studying and pretending they are not."),
                ("mc", "(I am one of them. I press the button and wait. Waiting is its own kind of studying.)"),
            ],
            "walk": [("narr", "On the way home I stop at the elevator. I press the button once. I press it again. The doors close. I say 'I am ready.'"),
                     ("mc", "(The doors close before I am ready. I say it anyway.)")],
            "dinner": [
                ("father", "The elevator?"),
                ("mc", "The elevator. I pressed the button twice. I said 'I am ready.'"),
                ("father", "Ready for what, exactly?"),
                ("mc", "I do not know. But I said it. The doors will open when they open."),
            ],
            "night_a": [
                ("hikari", "Did you press the button?"),
                ("mc", "I did. I pressed it twice. I said 'I am ready.' I am not sure what I am ready for."),
                ("hikari", "That is the point. You do not have to know. The pressing is the answer."),
            ],
            "night_b": [
                ("hikari", "You are learning to say 'I am ready' without knowing what you are ready for."),
                ("mc", "'I am ready' is not a destination. It is the moment before the doors open."),
                ("hikari", "Then we are both standing in that moment. It is not a bad place to be."),
            ],
            "night_c": [
                ("narr", "I say nothing. The elevator is still closed. The city is still waiting."),
                ("hikari", "The doors will open. They always do. The trick is not to lean on them before they do."),
            ],
            "notebook": "(I wrote 'the silence between stations.' It is holding the next station. It is holding me.)",
            "desk": "the button",
            "close": [("narr", "I turn off the lamp. The elevator is still closed. The city is still waiting. I am still learning to say 'I am ready.' Tomorrow I will say it again.")],
        },

        45: {
            "title": "The lost thing",
            "morning": [
                ("narr", "Friday. The week is done and I am still here."),
                ("narr", "On the way to the station I pass the lost-and-found office. A shelf of umbrellas, a box of gloves, a scarf with no name."),
                ("mc", "(Nothing here is lost. It is all waiting. The city is the most patient keeper I know.)"),
            ],
            "chat_note": [("mc", "(Aya's text: 'New menu item. The omurice has a secret ingredient. You may guess.' I am guessing 'patience.')")],
            "kitchen": [
                ("mother", "You look like you are thinking about something you lost."),
                ("mc", "I am thinking about the lost and found. The shelf of umbrellas."),
                ("father", "A city that keeps your umbrella is a city that expects you back."),
                ("mc", "(He is right. The shelf is a promise. I have not lost anything yet, but I like knowing where it would wait.)"),
            ],
            "lesson": [
                ("hikari", "Ochimono. The lost and found. In Japan, lost things are not lost. They are waiting. They are in a shelf, in a box, in a drawer, waiting for you to claim them."),
                ("mc", "So nothing is ever really lost?"),
                ("hikari", "Nothing is ever really lost. It is just waiting for you to come back. The city keeps everything. It is the most patient keeper."),
                ("mc", "(The ochimono is a patient shelf. It keeps everything. It waits for you to come back.)"),
            ],
            "campus": [
                ("narr", "The campus is doing its Friday thing: half the students are already gone, the other half are waiting on the last train."),
                ("mc", "(I sit on a bench and think about the shelf. Everything there is waiting for someone to come back.)"),
            ],
            "walk": [("narr", "On the way home I pass the lost-and-found office at the station. A shelf of umbrellas, a box of gloves, a scarf with no name."),
                     ("mc", "(Nothing here is lost. It is all waiting. The city is the most patient keeper I know.)")],
            "dinner": [
                ("father", "The lost and found?"),
                ("mc", "The ochimono. Nothing is ever really lost here. It is just waiting."),
                ("mother", "That is a comforting thing to believe."),
                ("mc", "(It is also a little sad. Waiting is its own kind of lost.)"),
            ],
            "night_a": [
                ("hikari", "Did you see the shelf?"),
                ("mc", "I did. Umbrellas, gloves, a scarf. All waiting for someone to claim them."),
                ("hikari", "That is the most honest shelf in the city. It admits that people lose things."),
            ],
            "night_b": [
                ("hikari", "You are learning that nothing is ever really lost."),
                ("mc", "I am learning that maybe is a kind of waiting. The city waits. I wait. We are both being patient."),
                ("hikari", "Patience is the city's oldest virtue. You are learning it by osmosis."),
            ],
            "night_c": [
                ("narr", "I say nothing. The shelf is still waiting. The city is still keeping everything. I am still learning to wait."),
                ("hikari", "The lost and found is a promise. Someday, someone will come back for these things. It is a promise the city keeps."),
            ],
            "notebook": "(Ochimono. Lost things. The shelf is full of them. Each one was carried by someone who set it down and walked away. I wonder how many of them are still being looked for.)",
            "desk": "the waiting shelf",
            "close": [("narr", "I turn off the lamp. The shelf is still waiting. The city is still keeping everything. I am still learning to wait.")],
        },
    }
