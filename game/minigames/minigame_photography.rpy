################################################################################
## CIRCLE: FIELD PHOTOGRAPHY MINIGAME
################################################################################
##
## A standalone visual composition minigame designed for Sim's Photography Club
## ("Circle") and free afternoon explorations in Elsewhere.
##
## FICTION:
##   Sim gives the protagonist his first field camera assignment for Circle:
##   "The city gives you ten thousand things at once. A camera doesn't just
##   record — it decides what matters. Find the line that holds the frame together."
##
## DESIGN:
##   * 3 field assignments in different locations:
##       1. Akihabara: "The Living Line" (Human gesture amidst neon chaos)
##       2. The Alleyway: "Shadow & Lantern" (Leading lines and low-light depth)
##       3. The River Path: "The Uncanny Surface" (Spotting the reflection anomaly)
##   * Realistic Viewfinder HUD:
##       - Rule-of-Thirds compositional grid (toggleable ON/OFF)
##       - 3 candidate framing crops per location (Wide / Thirds / Tight)
##       - Exposure compensation (EV -0.7 / 0.0 / +0.7)
##       - Shutter release button with camera sound and mirror-flash effect
##   * Critique Phase:
##       - Photos develop like prints on a darkroom contact sheet
##       - Sim provides rich, encouraging, educational critique tailored to your choices
##       - Ratings (S / A / B) based on composition and exposure harmony
##   * Safe & Standalone:
##       - Tests via console: jump test_photography
##       - OR press 'P' key anytime to test
##       - Call via story: call minigame_photography
################################################################################

init python:
    class PhotoAssignment:
        def __init__(self, key, title, subtitle, location, bg_image, frames, optimal_frame, optimal_ev, hint):
            self.key = key
            self.title = title
            self.subtitle = subtitle
            self.location = location
            self.bg_image = bg_image
            # frames: list of dicts: {"label": "...", "desc": "...", "crop": (x, y, w, h), "critique": "..."}
            self.frames = frames
            self.optimal_frame = optimal_frame  # index 0, 1, or 2
            self.optimal_ev = optimal_ev        # 0.0 (balanced) or -0.7 / +0.7
            self.hint = hint

    PHOTO_ASSIGNMENTS = [
        PhotoAssignment(
            key="akihabara",
            title="THE LIVING LINE",
            subtitle="Assignment 01: Find the human pulse amidst the electronic roar",
            location="AKIHABARA // ELECTRIC TOWN",
            bg_image="images/backgrounds/bg_akihabara.png",
            frames=[
                {
                    "label": "FRAME A: WIDE CHAOS",
                    "desc": "A wide angle capturing every neon billboard, storefront, and crowd stream.",
                    "crop": (0, 0, 1280, 720),
                    "critique": "A lively shot! You caught the sheer volume of the district. The only challenge is the eye wanders without finding a single anchor. Still, authentic energy."
                },
                {
                    "label": "FRAME B: BALANCED THIRDS",
                    "desc": "Framed so the vertical street signs balance against the lone pedestrian waiting at the crossing.",
                    "crop": (180, 40, 920, 640),
                    "critique": "Look at that balance. The signs guide the eye down, and the figure in the lower third grounds the whole street. That's not just a snapshot, that's a story."
                },
                {
                    "label": "FRAME C: TIGHT DETAIL",
                    "desc": "A close crop cutting off the street, focusing tightly on a glowing store window.",
                    "crop": (350, 150, 680, 480),
                    "critique": "Intimate, but you lost the sense of scale. Akihabara is all about how overwhelming it is. When you crop out the street, it could be any shop anywhere."
                }
            ],
            optimal_frame=1,
            optimal_ev=0.0,
            hint="Look for the frame that balances the towering signs with someone standing in the light."
        ),
        PhotoAssignment(
            key="alley",
            title="SHADOW & LANTERN",
            subtitle="Assignment 02: Leading lines and low-light depth in the backstreets",
            location="SIDE STREET // DUSK",
            bg_image="images/backgrounds/bg_alley.png",
            frames=[
                {
                    "label": "FRAME A: DEEP PERSPECTIVE",
                    "desc": "The camera hugs the pavement line, following the narrow alley toward the glowing red lantern.",
                    "crop": (120, 30, 980, 660),
                    "critique": "Superb leading line. The eye travels straight down the cobblestones directly to the red lantern. Low dusk light is tough, but you made the shadows work for you."
                },
                {
                    "label": "FRAME B: HIGH ROOFLINE",
                    "desc": "A high-angled composition looking up at the telephone wires and twilight sky.",
                    "crop": (200, 0, 880, 520),
                    "critique": "The wire patterns against the dusk sky are poetic! But we lost the doorway that gives the alley its warmth. A nice abstract, even if it misses the subject."
                },
                {
                    "label": "FRAME C: ASYMMETRICAL WALL",
                    "desc": "Framed closely against the corrugated siding on the left, obscuring the right half.",
                    "crop": (40, 80, 800, 600),
                    "critique": "The texture of the wall is gritty, but it chokes the light. In street photography, let the shadows invite curiosity, not block the view."
                }
            ],
            optimal_frame=0,
            optimal_ev=0.0,
            hint="Use the narrowing alley as a natural pointer toward the lantern."
        ),
        PhotoAssignment(
            key="river",
            title="THE UNCANNY SURFACE",
            subtitle="Assignment 03: The boundary between city light and still water",
            location="RIVER PATH // NIGHT",
            bg_image="images/backgrounds/bg_river.png",
            frames=[
                {
                    "label": "FRAME A: LEVEL HORIZON",
                    "desc": "A classic composition splitting the river and night sky across the middle.",
                    "crop": (0, 60, 1280, 600),
                    "critique": "Clean and tranquil. The reflection matches the shoreline symmetrically. A very peaceful study of the water."
                },
                {
                    "label": "FRAME B: WATER REFLECTION",
                    "desc": "Low framing tilting downward, capturing the ripple patterns under the lamppost.",
                    "crop": (220, 120, 900, 580),
                    "critique": "Wait... look closely at that ripple in the lower left. Is that... a grid distortion in the reflection? The water shouldn't break into digital artifacts like that. What a strange, captivating capture. You notice things nobody else sees."
                },
                {
                    "label": "FRAME C: DISTANT BRIDGE",
                    "desc": "Zoomed in on the distant pedestrian bridge in heavy silhouette.",
                    "crop": (380, 40, 720, 500),
                    "critique": "A bit noisy in the dark, but the silhouette of the bridge is moody. Night shooting pushes camera sensors to their limit."
                }
            ],
            optimal_frame=1,
            optimal_ev=0.0,
            hint="Look down at the water. Notice how the light breaks on the surface."
        )
    ]

    class PhotographyEngine:
        def __init__(self):
            self.current_idx = 0
            self.total_assignments = len(PHOTO_ASSIGNMENTS)

            # Viewfinder parameters
            self.selected_frame_idx = 0
            self.selected_ev = 0.0  # -0.7, 0.0, +0.7
            self.show_grid = True

            # State: "viewfinder", "shutter_flash", "review", "complete"
            self.state = "viewfinder"

            # Stored results: list of {"assignment": ..., "frame": ..., "ev": ..., "score": ..., "critique": ...}
            self.results = []

        @property
        def current_assignment(self):
            return PHOTO_ASSIGNMENTS[self.current_idx]

        def toggle_grid(self):
            self.show_grid = not self.show_grid

        def select_frame(self, idx):
            self.selected_frame_idx = idx

        def cycle_ev(self):
            ev_steps = [-0.7, 0.0, 0.7]
            curr_pos = ev_steps.index(self.selected_ev) if self.selected_ev in ev_steps else 1
            self.selected_ev = ev_steps[(curr_pos + 1) % len(ev_steps)]

        def snap_photo(self):
            if self.state != "viewfinder":
                return

            # Sound effects: Shutter click + settle
            renpy.sound.play("audio/SFX/attribute_tick.wav", channel="sfx")
            renpy.sound.play("audio/SFX/attribute_settle.wav", channel="attribute_ui")

            # Calculate score for this shot
            assignment = self.current_assignment
            frame_data = assignment.frames[self.selected_frame_idx]

            is_optimal_frame = (self.selected_frame_idx == assignment.optimal_frame)
            is_optimal_ev = (abs(self.selected_ev - assignment.optimal_ev) < 0.1)

            if is_optimal_frame and is_optimal_ev:
                grade = "S"
                score_pts = 3
            elif is_optimal_frame or is_optimal_ev:
                grade = "A"
                score_pts = 2
            else:
                grade = "B"
                score_pts = 1

            # Critique construction
            critique_text = frame_data["critique"]
            if self.selected_ev < -0.1:
                critique_text += " It's a touch underexposed, giving it a heavier, moody shadow."
            elif self.selected_ev > 0.1:
                critique_text += " The exposure is slightly high, giving the lights a diffused halo."

            result_entry = {
                "assignment": assignment,
                "frame": frame_data,
                "ev": self.selected_ev,
                "grade": grade,
                "score": score_pts,
                "critique": critique_text
            }
            self.results.append(result_entry)
            self.state = "shutter_flash"

        def finish_flash(self):
            self.state = "review"

        def next_assignment(self):
            if self.current_idx + 1 < self.total_assignments:
                self.current_idx += 1
                self.selected_frame_idx = 0
                self.selected_ev = 0.0
                self.state = "viewfinder"
            else:
                self.state = "complete"

        def get_total_score(self):
            return sum(r["score"] for r in self.results)

        def is_mastery(self):
            # Maximum score is 9 (3 shots x 3 pts)
            return self.get_total_score() >= 7


# --- VIEWFINDER TRANSFORM HELPERS ---

init python:
    def crop_viewport(img_path, crop_rect, target_w=960, target_h=540):
        # Crop on a shared 16:9 canvas, then contain it in a fixed viewport.
        # This keeps assignment crops intact and prevents their aspect ratios
        # from changing the size or bounds of the surrounding UI.
        cx, cy, cw, ch = crop_rect
        base_img = Transform(img_path, xysize=(1280, 720), fit="cover")
        viewport_size = (gui.scale(target_w), gui.scale(target_h))
        cropped_img = Transform(base_img, crop=(cx, cy, cw, ch))
        return Fixed(
            Solid("#000000"),
            Transform(
                cropped_img,
                xysize=viewport_size,
                fit="contain",
                xalign=0.5,
                yalign=0.5
            ),
            xysize=viewport_size
        )


# --- VIEWFINDER SCREEN ---

screen photography_viewfinder(engine):
    modal True
    zorder 115

    default flash_alpha = 1.0

    $ assignment = engine.current_assignment
    $ cur_frame = assignment.frames[engine.selected_frame_idx]
    $ crop_rect = cur_frame["crop"]
    $ cur_label = cur_frame["label"]
    $ ev_str = ("+0.7" if engine.selected_ev > 0.1 else "-0.7" if engine.selected_ev < -0.1 else "±0.0")
    $ ev_disp = "EV " + ev_str
    $ banner_text = assignment.location + "  •  " + assignment.title
    $ header_study = "CIRCLE // FIELD STUDY " + str(engine.current_idx + 1) + " OF " + str(engine.total_assignments)
    $ sub_title = assignment.subtitle

    # 1. Dark Rangefinder Body
    add Solid("#06080b")

    # 2. Central Live Camera Sensor Frame
    fixed:
        xalign 0.5
        ypos gui.scale(42)
        xysize (gui.scale(960), gui.scale(540))

        # The cropped photographic view
        add crop_viewport(assignment.bg_image, crop_rect, 960, 540)

        # Exposure brightness tint overlay
        if engine.selected_ev < -0.1:
            add Solid("#00000045")
        elif engine.selected_ev > 0.1:
            add Solid("#ffffff28")

        # Optional Rule-of-Thirds Grid
        if engine.show_grid:
            # Vertical lines
            add Solid("#ffffff30") xpos gui.scale(320) ypos 0 xysize (1, gui.scale(540))
            add Solid("#ffffff30") xpos gui.scale(640) ypos 0 xysize (1, gui.scale(540))
            # Horizontal lines
            add Solid("#ffffff30") xpos 0 ypos gui.scale(180) xysize (gui.scale(960), 1)
            add Solid("#ffffff30") xpos 0 ypos gui.scale(360) xysize (gui.scale(960), 1)

        # Viewfinder Corner Brackets
        add Solid("#ffffffb0") xpos gui.scale(16) ypos gui.scale(16) xysize (gui.scale(24), gui.scale(2))
        add Solid("#ffffffb0") xpos gui.scale(16) ypos gui.scale(16) xysize (gui.scale(2), gui.scale(24))

        add Solid("#ffffffb0") xpos gui.scale(960 - 40) ypos gui.scale(16) xysize (gui.scale(24), gui.scale(2))
        add Solid("#ffffffb0") xpos gui.scale(960 - 18) ypos gui.scale(16) xysize (gui.scale(2), gui.scale(24))

        add Solid("#ffffffb0") xpos gui.scale(16) ypos gui.scale(540 - 18) xysize (gui.scale(24), gui.scale(2))
        add Solid("#ffffffb0") xpos gui.scale(16) ypos gui.scale(540 - 40) xysize (gui.scale(2), gui.scale(24))

        add Solid("#ffffffb0") xpos gui.scale(960 - 40) ypos gui.scale(540 - 18) xysize (gui.scale(24), gui.scale(2))
        add Solid("#ffffffb0") xpos gui.scale(960 - 18) ypos gui.scale(540 - 40) xysize (gui.scale(2), gui.scale(24))

        # Center Auto-Focus Reticle
        fixed:
            xalign 0.5
            yalign 0.5
            xysize (gui.scale(40), gui.scale(40))
            add Solid("#5fb8ffcc") xpos 0 ypos gui.scale(19) xysize (gui.scale(12), gui.scale(2))
            add Solid("#5fb8ffcc") xpos gui.scale(28) ypos gui.scale(19) xysize (gui.scale(12), gui.scale(2))
            add Solid("#5fb8ffcc") xpos gui.scale(19) ypos 0 xysize (gui.scale(2), gui.scale(12))
            add Solid("#5fb8ffcc") xpos gui.scale(19) ypos gui.scale(28) xysize (gui.scale(2), gui.scale(12))

        # Live telemetry banner inside viewfinder
        frame:
            background Solid("#00000099")
            xalign 0.5
            ypos gui.scale(16)
            padding (gui.scale(14), gui.scale(5))
            text banner_text size gui.scale(11) bold True color "#e0e7ee" kerning gui.scale(2)

        # Bottom sensor readouts
        frame:
            background Solid("#000000aa")
            xfill True
            yalign 1.0
            padding (gui.scale(16), gui.scale(6))

            hbox:
                spacing gui.scale(22)
                text "35mm PRIME" size gui.scale(11) color "#8ca0b3" kerning gui.scale(1)
                text "f/2.8" size gui.scale(11) color "#8ca0b3"
                text "1/250s" size gui.scale(11) color "#8ca0b3"

                text ev_disp size gui.scale(11) bold True color ("#f0b85a" if engine.selected_ev != 0.0 else "#8ca0b3")

                text cur_label size gui.scale(11) bold True color "#5fb8ff" xalign 1.0

    # 3. Top Header Bar
    hbox:
        xalign 0.5
        ypos gui.scale(10)
        xsize gui.scale(960)

        text header_study size gui.scale(12) bold True color "#8faec7" kerning gui.scale(2)
        text sub_title size gui.scale(11) color "#5b758c" xalign 1.0

    # 4. Bottom Camera Controls & Shutter Deck
    frame:
        background Solid("#0d131a")
        xalign 0.5
        ypos gui.scale(592)
        xsize gui.scale(960)
        ysize gui.scale(118)
        padding (gui.scale(18), gui.scale(12))

        hbox:
            xfill True
            yalign 0.5

            # Left controls: Framing selections
            vbox:
                spacing gui.scale(6)
                text "COMPOSITION FRAMING:" size gui.scale(10) bold True color "#6e899e" kerning gui.scale(1)

                hbox:
                    spacing gui.scale(8)
                    for f_idx, fr in enumerate(assignment.frames):
                        $ is_sel = (engine.selected_frame_idx == f_idx)
                        $ f_btn_label = "FRAME 0" + str(f_idx + 1)
                        button:
                            background Solid("#5fb8ff" if is_sel else "#16232e")
                            hover_background Solid("#5fb8ff77")
                            padding (gui.scale(12), gui.scale(6))
                            action Function(engine.select_frame, f_idx)
                            text f_btn_label size gui.scale(11) bold True color ("#04080d" if is_sel else "#c8d9e6")

            # Center controls: Grid & Exposure adjustments
            vbox:
                xalign 0.5
                spacing gui.scale(6)
                text "VIEWFINDER CONTROLS:" size gui.scale(10) bold True color "#6e899e" kerning gui.scale(1)

                hbox:
                    spacing gui.scale(10)
                    $ grid_label = "GRID: ON" if engine.show_grid else "GRID: OFF"
                    textbutton grid_label:
                        action Function(engine.toggle_grid)
                        background Solid("#1d2c38")
                        hover_background Solid("#294052")
                        padding (gui.scale(12), gui.scale(6))
                        text_size gui.scale(11)
                        text_color ("#77d98b" if engine.show_grid else "#8ca0b3")

                    $ ev_label = ("EV +0.7" if engine.selected_ev > 0.1 else "EV -0.7" if engine.selected_ev < -0.1 else "EV ±0.0")
                    textbutton ev_label:
                        action Function(engine.cycle_ev)
                        background Solid("#1d2c38")
                        hover_background Solid("#294052")
                        padding (gui.scale(12), gui.scale(6))
                        text_size gui.scale(11)
                        text_color ("#f0b85a" if engine.selected_ev != 0.0 else "#8ca0b3")

            # Right: Shutter Release Button
            button:
                xalign 1.0
                yalign 0.5
                background Solid("#22628f")
                hover_background Solid("#3188c4")
                padding (gui.scale(22), gui.scale(14))
                action Function(engine.snap_photo)

                hbox:
                    spacing gui.scale(10)
                    text "●" size gui.scale(18) color "#ff6b6b" yalign 0.5
                    text "CAPTURE FRAME" size gui.scale(14) bold True color "#ffffff" kerning gui.scale(2) yalign 0.5

    # 5. Shutter White-Out Flash Transition
    if engine.state == "shutter_flash":
        add Solid("#ffffff")
        timer 0.15 action Function(engine.finish_flash)


# --- REVIEW & CRITIQUE SCREEN ---

screen photography_review(engine):
    modal True
    zorder 120

    $ last_result = engine.results[-1]
    $ assignment = last_result["assignment"]
    $ frame_data = last_result["frame"]
    $ grade_col = ("#5fb8ff" if last_result["grade"] == "S" else "#77d98b" if last_result["grade"] == "A" else "#f0b85a")
    $ rev_title = assignment.title
    $ rev_grade = "GRADE " + str(last_result["grade"])
    $ frame_label_rev = frame_data["label"]
    $ critique_text = '"' + last_result["critique"] + '"'
    $ comp_text = "• Composition: " + frame_data["desc"]
    $ ev_eval = ("Underexposed (EV -0.7)" if last_result["ev"] < -0.1 else "Overexposed (EV +0.7)" if last_result["ev"] > 0.1 else "Balanced Exposure (EV ±0.0)")
    $ meter_text = "• Light Meter: " + ev_eval

    # Dark background
    add Solid("#05080c")

    frame:
        background Solid("#0c141ceb")
        xalign 0.5
        yalign 0.5
        xsize gui.scale(1020)
        ysize gui.scale(640)
        padding (gui.scale(28), gui.scale(24))

        vbox:
            xfill True
            spacing gui.scale(16)

            # Header
            hbox:
                vbox:
                    text "CIRCLE // DEVELOPED PRINT REVIEW" size gui.scale(11) bold True color "#6e8a9e" kerning gui.scale(2)
                    text rev_title size gui.scale(24) bold True color "#e4f1fa"

                # Rating stamp
                frame:
                    xalign 1.0
                    background Solid(grade_col + "22")
                    padding (gui.scale(18), gui.scale(8))
                    text rev_grade size gui.scale(18) bold True color grade_col kerning gui.scale(2)

            add Solid("#1b2c3a") xysize (gui.scale(964), 1)

            # Central body: Captured Print on Left, Sim's critique on Right
            hbox:
                spacing gui.scale(28)

                # Photo Print
                vbox:
                    spacing gui.scale(8)
                    frame:
                        background Solid("#000000")
                        padding (gui.scale(6), gui.scale(6))
                        xsize gui.scale(460)
                        ysize gui.scale(264)
                        add crop_viewport(assignment.bg_image, frame_data["crop"], 448, 252)

                    text frame_label_rev size gui.scale(11) color "#8ca0b3" xalign 0.5

                # Sim's Feedback Panel
                vbox:
                    xsize gui.scale(470)
                    spacing gui.scale(14)

                    hbox:
                        spacing gui.scale(12)
                        add "images/characters/sim.png" xysize (gui.scale(56), gui.scale(76)) fit "contain" yalign 0.5
                        vbox:
                            yalign 0.5
                            text "SIM" size gui.scale(16) bold True color "#add8e6"
                            text "Circle Founder & Guide" size gui.scale(11) color "#688299"

                    frame:
                        background Solid("#060c12")
                        padding (gui.scale(16), gui.scale(14))
                        xfill True
                        text critique_text size gui.scale(14) color "#dce9f5" line_spacing gui.scale(4) italic True

                    vbox:
                        spacing gui.scale(4)
                        text "TECHNICAL EVALUATION:" size gui.scale(10) bold True color "#6e899e" kerning gui.scale(1)
                        text comp_text size gui.scale(11) color "#a6bac9"
                        text meter_text size gui.scale(11) color "#a6bac9"

            # Bottom Continue Button
            hbox:
                xalign 1.0
                yoffset gui.scale(10)
                spacing gui.scale(14)

                if engine.current_idx + 1 < engine.total_assignments:
                    textbutton "NEXT ASSIGNMENT →":
                        action Function(engine.next_assignment)
                        background Solid("#22628f")
                        hover_background Solid("#3188c4")
                        padding (gui.scale(24), gui.scale(12))
                        text_size gui.scale(13)
                        text_bold True
                        text_color "#ffffff"
                        text_kerning gui.scale(1)
                else:
                    textbutton "COMPLETE FIELD STUDY →":
                        action Function(engine.next_assignment)
                        background Solid("#2b7a59")
                        hover_background Solid("#3aa376")
                        padding (gui.scale(24), gui.scale(12))
                        text_size gui.scale(13)
                        text_bold True
                        text_color "#ffffff"
                        text_kerning gui.scale(1)


# --- FINAL SUMMARY SCREEN ---

screen photography_summary(engine):
    modal True
    zorder 125

    $ is_pass = engine.is_mastery()
    $ total_pts = engine.get_total_score()

    add Solid("#04070a")

    frame:
        background Solid("#0b141ee6")
        xalign 0.5
        yalign 0.5
        xsize gui.scale(1160)
        ysize gui.scale(610)
        padding (gui.scale(28), gui.scale(26))

        vbox:
            xsize gui.scale(1104)
            spacing gui.scale(14)

            text "CIRCLE // FIELD STUDY SUMMARY" size gui.scale(11) bold True color "#6e8a9e" kerning gui.scale(2) xalign 0.5

            if is_pass:
                text "PHOTOGRAPHIC INTUITION VERIFIED" size gui.scale(24) bold True color "#77d98b" xalign 0.5 kerning gui.scale(1)
            else:
                text "FIELD STUDY COMPLETED" size gui.scale(24) bold True color "#5fb8ff" xalign 0.5 kerning gui.scale(1)

            hbox:
                xsize gui.scale(1104)
                spacing gui.scale(16)

                for res in engine.results:
                    $ res_title = res["assignment"].title
                    $ res_location = res["assignment"].location
                    $ res_grade = str(res["grade"])

                    frame:
                        xsize gui.scale(357)
                        ysize gui.scale(262)
                        background Solid("#0d1822")
                        padding (gui.scale(12), gui.scale(12))

                        vbox:
                            xfill True
                            spacing gui.scale(8)

                            frame:
                                xsize gui.scale(333)
                                ysize gui.scale(187)
                                background Solid("#000000")
                                padding (0, 0)
                                add crop_viewport(res["assignment"].bg_image, res["frame"]["crop"], 333, 187)

                            hbox:
                                xfill True
                                text res_title size gui.scale(12) bold True color "#dce9f5" xmaximum gui.scale(280)
                                text res_grade size gui.scale(14) bold True color "#5fb8ff" xalign 1.0

                            text res_location size gui.scale(9) bold True color "#6e8a9e" kerning gui.scale(1)

            add Solid("#1b2c3a") xysize (gui.scale(1104), 1)

            hbox:
                xsize gui.scale(1104)
                text "FINAL SCORE  [total_pts] / 9" size gui.scale(11) bold True color "#8ca0b3" kerning gui.scale(1)
                text ("MASTERY" if is_pass else "FIRST ROLL") size gui.scale(11) bold True color ("#77d98b" if is_pass else "#5fb8ff") xalign 1.0

            frame:
                background Solid("#070d14")
                padding (gui.scale(16), gui.scale(12))
                xsize gui.scale(1104)
                ysize gui.scale(82)
                if is_pass:
                    text "\"You have a natural eye for what to keep and what to cut away. That's the hardest part of photography. The club is going to love these.\"" size gui.scale(13) color "#d4e4f0" italic True xalign 0.0 yalign 0.5
                else:
                    text "\"A solid first roll. Every photographer has to shoot through their mistakes before their true eye wakes up. That's why we come back every week.\"" size gui.scale(13) color "#d4e4f0" italic True xalign 0.0 yalign 0.5

            textbutton "FINISH REVIEW":
                xalign 0.5
                action Return(is_pass)
                background Solid("#22628f")
                hover_background Solid("#3188c4")
                padding (gui.scale(28), gui.scale(12))
                text_size gui.scale(13)
                text_bold True
                text_color "#ffffff"
                text_kerning gui.scale(1)


# --- MAIN MINIGAME COORDINATOR SCREEN ---

screen photography_minigame(engine):
    modal True
    zorder 110

    if engine.state in ("viewfinder", "shutter_flash"):
        use photography_viewfinder(engine)
    elif engine.state == "review":
        use photography_review(engine)
    elif engine.state == "complete":
        use photography_summary(engine)


# --- WRAPPER LABEL FOR STORY SCRIPT ---
## Call anywhere:
##     call minigame_photography
##     if _return:
##         "Sim was impressed by your compositions."

label minigame_photography:
    window hide
    $ _photo_engine = PhotographyEngine()
    call screen photography_minigame(_photo_engine)
    $ _photo_success = _return
    return _photo_success


# --- STANDALONE TEST LABEL ---
## Run via console: jump test_photography
## Or press 'P' key anytime.

label test_photography:
    scene black with Dissolve(0.8)
    play music "audio/Music/school.mp3" fadein 1.5

    "TEST SEQUENCE: CIRCLE // FIELD PHOTOGRAPHY STUDY"
    "This is a standalone test of the photography composition minigame."
    "Sim has given you three assignments around Tokyo. Select your framing and exposure carefully."

    call minigame_photography from _call_minigame_photography

    if _return:
        play sfx "audio/SFX/attribute_swell.wav"
        sim "Remarkable work. You've earned your place in Circle."
        "You feel a deeper grasp of observation and perspective."
    else:
        sim "A great first attempt. We'll head out again next Tuesday."
        "You take the prints home to study."

    "Test complete. Returning to game."
    stop music fadeout 1.5
    scene black with Dissolve(1.0)
    return
