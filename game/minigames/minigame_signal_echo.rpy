################################################################################
## SIGNAL ECHO — NEURAL CALIBRATION MINIGAME
################################################################################
##
## A standalone psychological-thriller minigame designed for Elsewhere's dream
## or facility-bleed sequences.
##
## FICTION:
##   Subject 04's neural connection to the Tokyo simulation experiences a drift.
##   The facility monitoring terminal broadcasts a sequence of frequency channels
##   (Alpha, Theta, Delta, Gamma). The subject must echo back the exact sequence
##   to stabilize the simulation matrix.
##
## DESIGN:
##   * 3 rounds with progressive sequence length (3, 4, 5 signals).
##   * Audio + Visual paired cues: each channel has a distinct sound frequency,
##     glyph, color, and name, so it is fully playable with sound off.
##   * "REPLAY SIGNAL" option so distraction doesn't punish the player.
##   * 3 error tolerances: mistakes re-transmit the sequence rather than instantly failing.
##   * Non-blocking: winning grants an Insight reward; failing blurs the dream
##     with a clinical line without halting story progression.
##
## TESTING THIS MINIGAME:
##   1. Open the console with Shift+O and type:
##          jump test_signal_echo
##   2. OR press the 'M' key from the Main Menu or in-game to jump to the test.
################################################################################

init python:
    import random

    class SignalChannel:
        def __init__(self, channel_id, name, symbol, glyph, color, sound):
            self.id = channel_id
            self.name = name
            self.symbol = symbol
            self.glyph = glyph
            self.color = color
            self.sound = sound

    SIGNAL_CHANNELS = [
        SignalChannel(0, "ALPHA", "α", "◇", "#5fb8ff", "audio/SFX/attribute_tick.wav"),
        SignalChannel(1, "THETA", "θ", "⬡", "#77d98b", "audio/SFX/wire_connect.wav"),
        SignalChannel(2, "DELTA", "δ", "△", "#f0b85a", "audio/SFX/attribute_rise.wav"),
        SignalChannel(3, "GAMMA", "γ", "○", "#ff6b6b", "audio/SFX/attribute_land.wav"),
    ]

    class SignalEchoEngine:
        def __init__(self, total_rounds=3, starting_length=3, max_tolerances=3):
            self.total_rounds = total_rounds
            self.starting_length = starting_length
            self.current_round = 1
            self.tolerances = max_tolerances
            self.max_tolerances = max_tolerances
            self.replays_remaining = 2

            # State machine: "prep", "broadcasting", "input", "evaluating", "round_clear", "glitch", "victory", "abort"
            self.phase = "prep"
            self.status_message = "INITIALIZING SIGNAL..."

            # Playback tracking
            self.sequence = []
            self.playback_step = 0
            self.active_flash_id = None

            # Player input tracking
            self.player_input = []

            # Start first round sequence
            self.generate_sequence()

        def generate_sequence(self):
            target_len = self.starting_length + (self.current_round - 1)
            # Avoid repeating the exact same channel 3 times in a row for pleasant flow
            seq = []
            for _ in range(target_len):
                choices = [0, 1, 2, 3]
                if len(seq) >= 2 and seq[-1] == seq[-2]:
                    choices.remove(seq[-1])
                seq.append(random.choice(choices))
            self.sequence = seq
            self.playback_step = 0
            self.active_flash_id = None
            self.player_input = []

        def start_broadcast(self):
            self.phase = "broadcasting"
            self.status_message = "BROADCASTING CARRIER SEQUENCE..."
            self.playback_step = 0
            self.active_flash_id = None
            self.player_input = []

        def trigger_replay(self):
            if self.phase == "input" and self.replays_remaining > 0:
                self.replays_remaining -= 1
                self.start_broadcast()

        def step_playback(self):
            if self.phase != "broadcasting":
                return

            if self.active_flash_id is not None:
                # Turn off active flash
                self.active_flash_id = None
                self.playback_step += 1
                if self.playback_step >= len(self.sequence):
                    # Sequence finished, hand over to player
                    self.phase = "input"
                    self.status_message = "AWAITING ECHO INPUT..."
                    self.player_input = []
            else:
                # Turn on current flash
                if self.playback_step < len(self.sequence):
                    cid = self.sequence[self.playback_step]
                    self.active_flash_id = cid
                    channel = SIGNAL_CHANNELS[cid]
                    renpy.sound.play(channel.sound, channel="sfx")

        def handle_input(self, channel_id):
            if self.phase != "input":
                return

            channel = SIGNAL_CHANNELS[channel_id]
            renpy.sound.play(channel.sound, channel="sfx")
            self.active_flash_id = channel_id

            expected_id = self.sequence[len(self.player_input)]

            if channel_id == expected_id:
                self.player_input.append(channel_id)
                # Check if complete
                if len(self.player_input) >= len(self.sequence):
                    self.phase = "round_clear"
                    renpy.sound.play("audio/SFX/memory_restore.wav", channel="attribute_ui")
                    if self.current_round >= self.total_rounds:
                        self.status_message = "CALIBRATION COMPLETE // HARMONY RESTORED"
                    else:
                        self.status_message = "HARMONY RATIO STABILIZED"
            else:
                # Mistake / deviation
                self.tolerances -= 1
                self.phase = "glitch"
                renpy.sound.play("audio/SFX/memory_deviation.wav", channel="attribute_ui")
                if self.tolerances <= 0:
                    self.status_message = "SIGNAL COLLAPSE // CALIBRATION ABORTED"
                else:
                    self.status_message = "DEVIATION DETECTED // RE-TRANSMITTING"

        def advance_after_clear(self):
            if self.current_round >= self.total_rounds:
                self.phase = "victory"
            else:
                self.current_round += 1
                self.generate_sequence()
                self.start_broadcast()

        def retry_after_glitch(self):
            if self.tolerances <= 0:
                self.phase = "abort"
            else:
                self.playback_step = 0
                self.active_flash_id = None
                self.start_broadcast()


# --- UI SCREEN ---

screen signal_echo_minigame(engine):
    modal True
    zorder 120

    # Dark phosphor background
    add Solid("#04070c")

    # Faint CRT scanline overlay
    add Solid("#09121c66")

    # Main telemetry container
    frame:
        background Solid("#080e16e6")
        xalign 0.5
        yalign 0.5
        xsize gui.scale(920)
        ysize gui.scale(620)
        padding (gui.scale(24), gui.scale(20))

        # Top diagnostic bar
        vbox:
            xfill True
            spacing gui.scale(4)

            hbox:
                text "FACILITY TELEMETRY // POD 03" size gui.scale(11) color "#688299" kerning gui.scale(2)
                text "SUBJECT 04" size gui.scale(11) color "#8ba6bf" xalign 1.0 kerning gui.scale(2)

            hbox:
                text "NEURAL HARMONY CALIBRATION" size gui.scale(22) bold True color "#e4f1fa" kerning gui.scale(1)

                # Sync percentage
                $ sync_pct = int(((engine.current_round - 1) / float(engine.total_rounds)) * 100)
                if engine.phase in ("round_clear", "victory"):
                    $ sync_pct = int((engine.current_round / float(engine.total_rounds)) * 100)
                text "[sync_pct]%%" size gui.scale(22) bold True color "#5fb8ff" xalign 1.0

            add Solid("#1b2f42") xysize (gui.scale(872), 1)

            # Secondary indicators
            hbox:
                yoffset gui.scale(4)
                spacing gui.scale(20)

                # Round indicator
                text "BAND [engine.current_round] / [engine.total_rounds]" size gui.scale(12) color "#9eb5c7" kerning gui.scale(1)

                # Tolerances remaining
                hbox:
                    spacing gui.scale(4)
                    text "STABILITY:" size gui.scale(11) color "#688299" yalign 0.5
                    for t in range(engine.max_tolerances):
                        if t < engine.tolerances:
                            add Solid("#5fb8ff") xysize (gui.scale(12), gui.scale(8)) yalign 0.5
                        else:
                            add Solid("#ff6b6b55") xysize (gui.scale(12), gui.scale(8)) yalign 0.5

                # Replay button
                if engine.phase == "input" and engine.replays_remaining > 0:
                    textbutton "↺ REPLAY SIGNAL ([engine.replays_remaining])":
                        action Function(engine.trigger_replay)
                        text_size gui.scale(11)
                        text_color "#f0b85a"
                        text_hover_color "#ffffff"
                        xalign 1.0
                elif engine.replays_remaining == 0:
                    text "NO REPLAYS REMAINING" size gui.scale(11) color "#546473" xalign 1.0

        # Status readout / Oscilloscope area
        frame:
            xalign 0.5
            ypos gui.scale(125)
            xsize gui.scale(872)
            ysize gui.scale(85)
            background Solid("#050a10")
            padding (gui.scale(16), gui.scale(12))

            vbox:
                xalign 0.5
                yalign 0.5
                spacing gui.scale(6)

                # Status label
                $ status_col = "#5fb8ff"
                if engine.phase == "glitch" or engine.phase == "abort":
                    $ status_col = "#ff6b6b"
                elif engine.phase == "round_clear" or engine.phase == "victory":
                    $ status_col = "#77d98b"
                elif engine.phase == "input":
                    $ status_col = "#77d98b"

                text "[engine.status_message]" size gui.scale(15) bold True color status_col xalign 0.5 kerning gui.scale(2)

                # Sequence step dots
                hbox:
                    xalign 0.5
                    spacing gui.scale(10)
                    for s_idx in range(len(engine.sequence)):
                        $ dot_color = "#1d3042"
                        if engine.phase == "broadcasting":
                            if s_idx == engine.playback_step and engine.active_flash_id is not None:
                                $ dot_color = SIGNAL_CHANNELS[engine.sequence[s_idx]].color
                            elif s_idx < engine.playback_step:
                                $ dot_color = "#355670"
                        elif engine.phase == "input":
                            if s_idx < len(engine.player_input):
                                $ dot_color = SIGNAL_CHANNELS[engine.player_input[s_idx]].color
                            else:
                                $ dot_color = "#1d3042"
                        elif engine.phase in ("round_clear", "victory"):
                            $ dot_color = SIGNAL_CHANNELS[engine.sequence[s_idx]].color
                        elif engine.phase in ("glitch", "abort"):
                            $ dot_color = "#ff6b6b"

                        add Solid(dot_color) xysize (gui.scale(22), gui.scale(6))

        # 4 Interactive Channel Nodes
        grid 2 2:
            xalign 0.5
            ypos gui.scale(225)
            spacing gui.scale(22)

            for channel in SIGNAL_CHANNELS:
                $ is_lit = (engine.active_flash_id == channel.id)
                $ bg_color = channel.color if is_lit else "#0d1a26"
                $ border_col = channel.color if is_lit else channel.color + "55"
                $ text_col = "#ffffff" if is_lit else channel.color

                button:
                    xsize gui.scale(360)
                    ysize gui.scale(110)
                    background Solid(bg_color)
                    hover_background Solid(channel.color + "33")
                    sensitive (engine.phase == "input")
                    action Function(engine.handle_input, channel.id)

                    fixed:
                        # Top-left channel symbol
                        text channel.symbol size gui.scale(24) bold True color text_col xpos gui.scale(18) ypos gui.scale(12) outlines []

                        # Central glyph
                        text channel.glyph size gui.scale(36) color text_col xalign 0.5 yalign 0.45 outlines []

                        # Channel name
                        text channel.name size gui.scale(14) bold True color text_col xpos gui.scale(18) ypos gui.scale(75) kerning gui.scale(2) outlines []

                        # Frequency band label
                        text "CH-0[channel.id + 1]" size gui.scale(11) color (text_col if is_lit else "#50697f") xalign 0.94 ypos gui.scale(78) outlines []

        # Footer guide
        hbox:
            xalign 0.5
            ypos gui.scale(575)
            spacing gui.scale(12)
            text "Observe the broadcast rhythm. Echo the sequence to restore equilibrium." size gui.scale(12) color "#688299" outlines []

    # --- Timers for State Progression ---

    # Prep pause before broadcasting
    if engine.phase == "prep":
        timer 0.8 action Function(engine.start_broadcast)

    # Broadcast stepping timer
    if engine.phase == "broadcasting":
        timer 0.55 repeat True action Function(engine.step_playback)

    # Input active flash clear
    if engine.phase == "input" and engine.active_flash_id is not None:
        timer 0.2 action SetField(engine, "active_flash_id", None)

    # Round clear wait
    if engine.phase == "round_clear":
        timer 1.2 action Function(engine.advance_after_clear)

    # Glitch wait
    if engine.phase == "glitch":
        timer 1.3 action Function(engine.retry_after_glitch)

    # Victory finish
    if engine.phase == "victory":
        timer 1.5 action Return(True)

    # Abort finish
    if engine.phase == "abort":
        timer 1.5 action Return(False)


# --- WRAPPER LABEL FOR EASY USE IN STORY ---
## Usage in any story script:
##     call minigame_signal_echo
##     if _return:
##         "The frequency harmonizes."
##     else:
##         "The signal slips away."

label minigame_signal_echo(rounds=3, starting_len=3, tolerances=3):
    window hide
    $ _echo_engine = SignalEchoEngine(total_rounds=rounds, starting_length=starting_len, max_tolerances=tolerances)
    call screen signal_echo_minigame(_echo_engine)
    $ _minigame_success = _return
    return _minigame_success


# --- STANDALONE TEST LABEL ---
## Run directly via console: jump test_signal_echo
## Or press 'M' on keyboard anytime during testing.

label test_signal_echo:
    scene black with Dissolve(0.8)
    play music "audio/Music/dream sequence.wav" fadein 2.0

    "TEST SEQUENCE: SIGNAL ECHO // NEURAL CALIBRATION"
    "This is a standalone test of the minigame."
    "The simulation will transmit an audio-visual sequence across 4 channels. Repeat each sequence accurately."

    call minigame_signal_echo(rounds=3, starting_len=3, tolerances=3)

    if _return:
        play sfx "audio/SFX/attribute_swell.wav"
        show hospital_flash onlayer overlay at truecenter:
            alpha 0.0
            linear 0.1 alpha 0.45
            linear 0.1 alpha 0.0
        "Telemetry: Signal lock established at 100%%. Neural drift arrested."
        "The dream solidifies into focus."
    else:
        show screen dream_static
        pause 0.6
        hide screen dream_static
        "Telemetry: Sequence tolerances exceeded. Pod holding at baseline."
        "The frequencies dissolve into static."

    "Test complete. Returning to game."
    stop music fadeout 1.5
    scene black with Dissolve(1.0)
    return


# Optional test shortcut: Bind key 'M' to jump to test_signal_echo
init python:
    config.underlay.append(
        renpy.Keymap(
            K_m=lambda: renpy.jump_out_of_context("test_signal_echo")
        )
    )
