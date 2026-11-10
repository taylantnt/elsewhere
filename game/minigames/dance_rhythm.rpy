################################################################################
## NEON STEP — FOUR-LANE RHYTHM MINIGAME
################################################################################
##
## Original music is generated for this chart at 110 BPM.
## Keyboard: arrow keys. Touch: tap the matching lane button.
## Story use: call minigame_dance
## Test: jump test_dance
##

init python:
    import math

    DANCE_BPM = 110
    DANCE_BEAT = 60.0 / DANCE_BPM
    DANCE_HIT_LINE = 470
    DANCE_NOTE_SPEED = 300.0
    DANCE_HIT_WINDOW = 0.22
    DANCE_LANES = [
        {"key": "left", "glyph": "←", "color": "#5fb8ff"},
        {"key": "down", "glyph": "↓", "color": "#77d98b"},
        {"key": "up", "glyph": "↑", "color": "#f0b85a"},
        {"key": "right", "glyph": "→", "color": "#ff7890"},
    ]

    def make_dance_chart():
        lane_pattern = [0, 1, 2, 3, 0, 2, 1, 3, 2, 0, 3, 1, 0, 3, 2, 1]
        chart = []

        # A two-bar instrumental lead-in gives the first arrows time to enter.
        for beat_index in range(4, 62):
            if beat_index % 8 not in (3,):
                chart.append({
                    "time": beat_index * DANCE_BEAT,
                    "lane": lane_pattern[beat_index % len(lane_pattern)],
                    "judged": False,
                    "result": None,
                })

            # Add a few off-beat steps in the later bars for a gentle lift.
            if beat_index >= 28 and beat_index % 8 in (2, 6):
                chart.append({
                    "time": (beat_index + 0.5) * DANCE_BEAT,
                    "lane": lane_pattern[(beat_index + 5) % len(lane_pattern)],
                    "judged": False,
                    "result": None,
                })

        chart.sort(key=lambda note: note["time"])
        return chart

    class DanceRhythmEngine:
        def __init__(self):
            self.notes = make_dance_chart()
            self.elapsed = 0.0
            self.score = 0
            self.combo = 0
            self.best_combo = 0
            self.perfect = 0
            self.great = 0
            self.good = 0
            self.misses = 0
            self.last_judgement = "GET READY"
            self.last_judgement_color = "#e4f1fa"
            self.judgement_timer = 1.2
            self.phase = "playing"
            self.chart_end = max(note["time"] for note in self.notes) + 0.75

        def hit(self, lane):
            if self.phase != "playing":
                return

            candidates = [
                note for note in self.notes
                if not note["judged"] and note["lane"] == lane
                and abs(note["time"] - self.elapsed) <= DANCE_HIT_WINDOW
            ]
            if not candidates:
                self.last_judgement = "KEEP THE BEAT"
                self.last_judgement_color = "#8ca0b3"
                self.judgement_timer = 0.35
                return

            note = min(candidates, key=lambda item: abs(item["time"] - self.elapsed))
            difference = abs(note["time"] - self.elapsed)
            note["judged"] = True

            if difference <= 0.075:
                note["result"] = "PERFECT"
                self.perfect += 1
                self.score += 300
                self.last_judgement_color = "#f0e68c"
            elif difference <= 0.145:
                note["result"] = "GREAT"
                self.great += 1
                self.score += 200
                self.last_judgement_color = "#77d98b"
            else:
                note["result"] = "GOOD"
                self.good += 1
                self.score += 100
                self.last_judgement_color = "#5fb8ff"

            self.combo += 1
            self.best_combo = max(self.best_combo, self.combo)
            self.last_judgement = note["result"]
            self.judgement_timer = 0.45

        def tick(self, dt):
            if self.phase != "playing":
                return

            self.elapsed += min(dt, 0.1)
            self.judgement_timer = max(0.0, self.judgement_timer - dt)

            for note in self.notes:
                if not note["judged"] and self.elapsed > note["time"] + DANCE_HIT_WINDOW:
                    note["judged"] = True
                    note["result"] = "MISS"
                    self.misses += 1
                    self.combo = 0
                    self.last_judgement = "MISS"
                    self.last_judgement_color = "#ff7890"
                    self.judgement_timer = 0.45

            if self.elapsed >= self.chart_end:
                self.phase = "complete"

        @property
        def total_notes(self):
            return len(self.notes)

        @property
        def accuracy(self):
            if not self.total_notes:
                return 0.0
            return 100.0 * (self.perfect + self.great + self.good) / self.total_notes

        @property
        def passed(self):
            return self.accuracy >= 70.0


init python:
    renpy.music.register_channel("dance_music", mixer="music", loop=False)


screen dance_rhythm(engine):
    modal True
    zorder 130

    add Solid("#050812")

    frame:
        background Solid("#0b1420")
        xalign 0.5
        yalign 0.5
        xsize gui.scale(1080)
        ysize gui.scale(700)
        padding (gui.scale(24), gui.scale(10))

        vbox:
            xfill True
            spacing gui.scale(8)

            hbox:
                text "NEON STEP // RHYTHM CLUB" size gui.scale(11) bold True color "#7b98b1" kerning gui.scale(2)
                text "SCORE  [engine.score]" size gui.scale(15) bold True color "#5fb8ff" xalign 1.0

            hbox:
                text "FOLLOW THE BEAT" size gui.scale(22) bold True color "#e4f1fa"
                text "COMBO  [engine.combo]" size gui.scale(14) bold True color "#f0b85a" xalign 1.0

            fixed:
                xalign 0.5
                xsize gui.scale(880)
                ysize gui.scale(520)

                add Solid("#07111d") xysize (gui.scale(880), gui.scale(520))

                for lane in range(4):
                    $ lane_x = gui.scale(40 + lane * 205)
                    add Solid("#111f2d") xpos lane_x ypos 0 xsize gui.scale(180) ysize gui.scale(520)
                    add Solid("#21364a") xpos lane_x ypos 0 xsize gui.scale(1) ysize gui.scale(520)
                    add Solid(DANCE_LANES[lane]["color"] + "66") xpos lane_x + gui.scale(89) ypos gui.scale(DANCE_HIT_LINE - 2) xsize gui.scale(2) ysize gui.scale(42)
                    text DANCE_LANES[lane]["glyph"] size gui.scale(30) bold True color DANCE_LANES[lane]["color"] xpos lane_x + gui.scale(74) ypos gui.scale(DANCE_HIT_LINE + 2)

                add Solid("#b8eaff") xpos gui.scale(40) ypos gui.scale(DANCE_HIT_LINE) xsize gui.scale(795) ysize gui.scale(2)
                add Solid("#b8eaff44") xpos gui.scale(40) ypos gui.scale(DANCE_HIT_LINE - 4) xsize gui.scale(795) ysize gui.scale(10)

                for note in engine.notes:
                    if not note["judged"]:
                        $ note_y = DANCE_HIT_LINE - (note["time"] - engine.elapsed) * DANCE_NOTE_SPEED
                        if -36 <= note_y <= 520:
                            $ note_x = 40 + note["lane"] * 205
                            $ note_color = DANCE_LANES[note["lane"]]["color"]
                            add Solid(note_color + "55") xpos gui.scale(note_x + 60) ypos gui.scale(note_y - 4) xsize gui.scale(60) ysize gui.scale(50)
                            add Solid(note_color) xpos gui.scale(note_x + 66) ypos gui.scale(note_y) xsize gui.scale(48) ysize gui.scale(38)
                            text DANCE_LANES[note["lane"]]["glyph"] size gui.scale(26) bold True color "#07111d" xpos gui.scale(note_x + 66) ypos gui.scale(note_y + 1)

                if engine.judgement_timer > 0.0:
                    text engine.last_judgement size gui.scale(22) bold True color engine.last_judgement_color xalign 0.5 ypos gui.scale(400) outlines [(gui.scale(2), "#07111d", 0, gui.scale(1))]

            hbox:
                xalign 0.5
                spacing gui.scale(10)
                for lane in range(4):
                    $ lane_label = DANCE_LANES[lane]["glyph"] + "  " + DANCE_LANES[lane]["key"].upper()
                    textbutton lane_label:
                        xsize gui.scale(190)
                        action Function(engine.hit, lane)
                        background Solid(DANCE_LANES[lane]["color"] + "33")
                        hover_background Solid(DANCE_LANES[lane]["color"] + "88")
                        padding (gui.scale(12), gui.scale(10))
                        text_size gui.scale(18)
                        text_bold True
                        text_color DANCE_LANES[lane]["color"]

            hbox:
                xfill True
                text "ARROW KEYS OR TAP A LANE  •  HIT WHEN THE ARROWS REACH THE LINE" size gui.scale(10) color "#8ca0b3"
                text "ACCURACY  [int(engine.accuracy)]%" size gui.scale(10) bold True color "#8ca0b3" xalign 1.0

    if engine.phase == "playing":
        key "K_LEFT" action Function(engine.hit, 0)
        key "K_DOWN" action Function(engine.hit, 1)
        key "K_UP" action Function(engine.hit, 2)
        key "K_RIGHT" action Function(engine.hit, 3)
        key "K_ESCAPE" action Return(False)
        timer 0.016 repeat True action Function(engine.tick, 0.016)
    else:
        frame:
            background Solid("#03070ddd")
            xalign 0.5
            yalign 0.5
            xsize gui.scale(520)
            padding (gui.scale(28), gui.scale(24))

            vbox:
                xalign 0.5
                spacing gui.scale(12)
                text ("DANCE COMPLETE" if engine.passed else "KEEP PRACTICING") size gui.scale(23) bold True color ("#77d98b" if engine.passed else "#f0b85a") xalign 0.5
                text "ACCURACY  [int(engine.accuracy)]%" size gui.scale(17) color "#e4f1fa" xalign 0.5
                text "PERFECT [engine.perfect]   GREAT [engine.great]   GOOD [engine.good]   MISS [engine.misses]" size gui.scale(11) color "#a6bac9" xalign 0.5
                text "BEST COMBO  [engine.best_combo]" size gui.scale(12) color "#f0b85a" xalign 0.5
                textbutton "FINISH":
                    xalign 0.5
                    action Return(engine.passed)
                    background Solid("#22628f")
                    hover_background Solid("#3188c4")
                    padding (gui.scale(24), gui.scale(10))
                    text_size gui.scale(13)
                    text_bold True
                    text_color "#ffffff"


label minigame_dance:
    window hide
    $ _dance_engine = DanceRhythmEngine()
    play dance_music "minigames/neon_step.wav" fadein 0.4
    call screen dance_rhythm(_dance_engine)
    $ _dance_result = _return
    stop dance_music fadeout 0.3
    return _dance_result


label test_dance:
    scene black with Dissolve(0.4)
    "Follow the arrows as they reach the line. Use the arrow keys or tap the matching lane."
    call minigame_dance from _call_minigame_dance
    if _return:
        "You finish the song in rhythm. The dance floor lights flare around you."
    else:
        "The song ends, but there is always another chance to find the beat."
    return


