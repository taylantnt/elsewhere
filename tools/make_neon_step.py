#!/usr/bin/env python3
"""Synthesize "Neon Step" — the original 128 BPM synthwave track for the dance minigame.

Pure-stdlib additive/wavetable synth. Writes a 44.1 kHz stereo WAV, which is then
converted to OGG with ffmpeg.

Structure (bars of 4/4, 128 BPM):
  0-1   intro      pad + sparkle arp
  2-9   verse      four-on-the-floor, clap, bass, arp
  10-13 build      snare roll + riser, pickup
  14-21 chorus 1   lead hook, full groove
  22-25 break      pad + arp, half-time
  26-33 chorus 2   lead hook + octave harmony
  34-37 outro      sustained pad, final hit
"""

import math
import random
import wave
from array import array

SR = 44100
BPM = 128.0
BEAT = 60.0 / BPM
BAR = BEAT * 4.0
TOTAL_BARS = 38
TAIL = 3.0
DURATION = TOTAL_BARS * BAR + TAIL
N = int(DURATION * SR)

L = array("d", bytes(8 * N))
R = array("d", bytes(8 * N))
SEND = array("d", bytes(8 * N))

TW = 2048
random.seed(20261116)


def midi(note):
    return 440.0 * (2.0 ** ((note - 69) / 12.0))


def make_table(harmonics, kind):
    table = [0.0] * (TW + 1)
    for i in range(TW):
        x = 2.0 * math.pi * i / TW
        value = 0.0
        for h in range(1, harmonics + 1):
            if kind == "saw":
                value += math.sin(h * x) / h
            elif kind == "square":
                if h % 2:
                    value += math.sin(h * x) / h
        table[i] = value
    peak = max(abs(v) for v in table) or 1.0
    for i in range(TW + 1):
        table[i] /= peak
    table[TW] = table[0]
    return table


SAW = make_table(26, "saw")
SQUARE = make_table(19, "square")
SINE = [math.sin(2.0 * math.pi * i / TW) for i in range(TW)] + [0.0]

DETUNE = 2.0 ** (7.0 / 1200.0)  # ~7 cents


def pan_gains(pan):
    angle = (pan + 1.0) * math.pi * 0.25
    return math.cos(angle), math.sin(angle)


def add_note(buf_l, buf_r, start, samples, gl, gr):
    """Mix a mono sample list that has already been generated."""
    i0 = int(start * SR)
    for k, value in enumerate(samples):
        index = i0 + k
        if index >= N:
            break
        buf_l[index] += value * gl
        buf_r[index] += value * gr


# --------------------------------------------------------------------------
# Instruments
# --------------------------------------------------------------------------

def kick(t, amp=0.95):
    dur = 0.42
    n = int(dur * SR)
    i0 = int(t * SR)
    phase = 0.0
    pitch_env = 1.0
    pitch_dec = math.exp(-34.0 / SR)
    gain = amp
    gain_dec = math.exp(-8.4 / SR)
    for k in range(n):
        index = i0 + k
        if index >= N:
            break
        pitch_env *= pitch_dec
        freq = 46.0 + 128.0 * pitch_env
        phase += freq * TW / SR
        if phase >= TW:
            phase -= TW
        sample = SINE[int(phase)] * gain
        # click transient
        if k < 90:
            sample += (random.random() * 2.0 - 1.0) * (1.0 - k / 90.0) * 0.12 * amp
        gain *= gain_dec
        L[index] += sample
        R[index] += sample


def snare(t, amp=0.34, tone=0.5):
    dur = 0.24
    n = int(dur * SR)
    i0 = int(t * SR)
    gain = amp
    gain_dec = math.exp(-24.0 / SR)
    phase = 0.0
    inc = 186.0 * TW / SR
    prev = 0.0
    for k in range(n):
        index = i0 + k
        if index >= N:
            break
        phase += inc
        if phase >= TW:
            phase -= TW
        body = SINE[int(phase)] * 0.55 * tone
        noise = random.random() * 2.0 - 1.0
        high = noise - prev * 0.7
        prev = noise
        sample = (body + high * 0.85) * gain
        gain *= gain_dec
        L[index] += sample
        R[index] += sample * 0.96


def clap(t, amp=0.3):
    dur = 0.3
    n = int(dur * SR)
    i0 = int(t * SR)
    gain = amp
    gain_dec = math.exp(-17.0 / SR)
    prev = 0.0
    for k in range(n):
        index = i0 + k
        if index >= N:
            break
        time = k / SR
        # three quick slaps, then a short tail
        burst = 0.0
        for offset in (0.0, 0.011, 0.022):
            delta = time - offset
            if 0.0 <= delta < 0.05:
                burst = max(burst, 1.0 - delta / 0.05)
        noise = random.random() * 2.0 - 1.0
        high = noise - prev * 0.82
        prev = noise
        sample = high * (burst * 0.8 + 0.28) * gain
        gain *= gain_dec
        L[index] += sample
        R[index] += sample


def hat(t, amp=0.12, open_hat=False):
    dur = 0.32 if open_hat else 0.055
    n = int(dur * SR)
    i0 = int(t * SR)
    gain = amp
    gain_dec = math.exp((-15.0 if open_hat else -78.0) / SR)
    prev = 0.0
    for k in range(n):
        index = i0 + k
        if index >= N:
            break
        noise = random.random() * 2.0 - 1.0
        high = noise - prev
        prev = noise
        sample = high * gain
        gain *= gain_dec
        L[index] += sample * 0.82
        R[index] += sample


def crash(t, amp=0.3):
    dur = 1.6
    n = int(dur * SR)
    i0 = int(t * SR)
    gain = amp
    gain_dec = math.exp(-3.0 / SR)
    prev = 0.0
    for k in range(n):
        index = i0 + k
        if index >= N:
            break
        noise = random.random() * 2.0 - 1.0
        high = noise - prev * 0.94
        prev = noise
        sample = high * gain
        gain *= gain_dec
        L[index] += sample
        R[index] += sample * 0.9


def bass(t, dur, note, amp=0.42, cutoff=0.16):
    freq = midi(note)
    n = int((dur + 0.06) * SR)
    i0 = int(t * SR)
    phase = 0.0
    inc = freq * TW / SR
    lp = 0.0
    attack = int(0.004 * SR) or 1
    release_start = int(dur * SR)
    release_len = max(1, n - release_start)
    for k in range(n):
        index = i0 + k
        if index >= N:
            break
        phase += inc
        while phase >= TW:
            phase -= TW
        index_int = int(phase)
        frac = phase - index_int
        saw = SAW[index_int] + (SAW[index_int + 1] - SAW[index_int]) * frac
        lp += cutoff * (saw - lp)
        if k < attack:
            env = k / attack
        elif k < release_start:
            env = 0.82 + 0.18 * math.exp(-(k - attack) / SR * 22.0)
        else:
            env = max(0.0, 1.0 - (k - release_start) / release_len)
        sample = lp * env * amp
        L[index] += sample
        R[index] += sample


def pad(t, dur, notes, amp=0.085, attack=0.22, cutoff=0.10):
    n = int((dur + 0.7) * SR)
    i0 = int(t * SR)
    attack_samples = int(attack * SR) or 1
    release_start = int(dur * SR)
    release_len = max(1, n - release_start)
    for note in notes:
        freq = midi(note)
        gl, gr = pan_gains(((note * 0.37) % 1.0) * 2.0 - 1.0)
        for detune, buf, gain_mul in ((1.0, L, 1.0), (DETUNE, R, 0.92)):
            phase = (note * 0.113) % TW
            inc = freq * detune * TW / SR
            lp = 0.0
            for k in range(n):
                index = i0 + k
                if index >= N:
                    break
                phase += inc
                while phase >= TW:
                    phase -= TW
                index_int = int(phase)
                frac = phase - index_int
                saw = SAW[index_int] + (SAW[index_int + 1] - SAW[index_int]) * frac
                lp += cutoff * (saw - lp)
                if k < attack_samples:
                    env = k / attack_samples
                elif k < release_start:
                    env = 1.0
                else:
                    env = max(0.0, 1.0 - (k - release_start) / release_len)
                buf[index] += lp * env * amp * gain_mul
                if buf is L:
                    R[index] += lp * env * amp * 0.55
                else:
                    L[index] += lp * env * amp * 0.55


def arp(t, dur, note, amp=0.1, pan=0.0):
    freq = midi(note)
    n = int((dur + 0.05) * SR)
    i0 = int(t * SR)
    phase = 0.0
    inc = freq * TW / SR
    lp = 0.0
    gain = amp
    gain_dec = math.exp(-22.0 / SR)
    gl, gr = pan_gains(pan)
    for k in range(n):
        index = i0 + k
        if index >= N:
            break
        phase += inc
        while phase >= TW:
            phase -= TW
        index_int = int(phase)
        frac = phase - index_int
        square = SQUARE[index_int] + (SQUARE[index_int + 1] - SQUARE[index_int]) * frac
        lp += 0.5 * (square - lp)
        sample = lp * gain
        gain *= gain_dec
        L[index] += sample * gl
        R[index] += sample * gr


def lead(t, dur, note, amp=0.148, vibrato=0.0):
    freq = midi(note)
    n = int((dur + 0.12) * SR)
    i0 = int(t * SR)
    phase = 0.0
    phase2 = 0.0
    lp = 0.0
    gain = 0.0
    attack = int(0.008 * SR) or 1
    release_start = int(dur * SR)
    release_len = max(1, n - release_start)
    vib_phase = 0.0
    vib_inc = 5.6 * 2.0 * math.pi / SR
    for k in range(n):
        index = i0 + k
        if index >= N:
            break
        vib_phase += vib_inc
        bend = 1.0 + vibrato * math.sin(vib_phase)
        inc = freq * bend * TW / SR
        phase += inc
        if phase >= TW:
            phase -= TW
        phase2 += inc * 1.003
        if phase2 >= TW:
            phase2 -= TW
        i1 = int(phase)
        i2 = int(phase2)
        saw = SAW[i1] + (SAW[i1 + 1] - SAW[i1]) * (phase - i1)
        saw2 = SAW[i2] + (SAW[i2 + 1] - SAW[i2]) * (phase2 - i2)
        lp += 0.36 * ((saw + saw2 * 0.55) * 0.6 - lp)
        if k < attack:
            gain += 1.0 / attack
            if gain > 1.0:
                gain = 1.0
        elif k < release_start:
            gain = 1.0
        else:
            gain = max(0.0, 1.0 - (k - release_start) / release_len)
        env = gain * (0.86 + 0.14 * (1.0 if k % 512 < 256 else -1.0) * 0.0)
        sample = lp * env * amp
        L[index] += sample
        R[index] += sample
        SEND[index] += sample * 0.55


def riser(t, dur, amp=0.16):
    n = int(dur * SR)
    i0 = int(t * SR)
    prev = 0.0
    lp = 0.0
    gain = 0.0
    gain_inc = amp / max(1, n * 0.7)
    for k in range(n):
        index = i0 + k
        if index >= N:
            break
        noise = random.random() * 2.0 - 1.0
        high = noise - prev * 0.9
        prev = noise
        cutoff = 0.02 + 0.5 * (k / n)
        lp += cutoff * (high - lp)
        gain = min(amp, gain + gain_inc)
        sample = lp * gain
        L[index] += sample * 0.8
        R[index] += sample


def impact(t, amp=0.5):
    n = int(0.9 * SR)
    i0 = int(t * SR)
    phase = 0.0
    pitch_env = 1.0
    gain = amp
    gain_dec = math.exp(-4.5 / SR)
    for k in range(n):
        index = i0 + k
        if index >= N:
            break
        pitch_env *= math.exp(-8.0 / SR)
        freq = 38.0 + 40.0 * pitch_env
        phase += freq * TW / SR
        if phase >= TW:
            phase -= TW
        sample = SINE[int(phase)] * gain
        gain *= gain_dec
        L[index] += sample
        R[index] += sample


# --------------------------------------------------------------------------
# Arrangement
# --------------------------------------------------------------------------

CHORDS = [
    (33, [57, 60, 64, 69]),  # Am
    (29, [53, 57, 60, 65]),  # F
    (36, [55, 60, 64, 67]),  # C
    (31, [55, 59, 62, 67]),  # G
]

MELODY = [
    (0.0, 0.5, 69), (0.5, 0.5, 72), (1.0, 0.5, 76), (1.5, 0.5, 74),
    (2.0, 0.5, 72), (2.5, 0.5, 69), (3.0, 0.5, 67), (3.5, 0.5, 69),

    (4.0, 0.5, 65), (4.5, 0.5, 69), (5.0, 0.5, 72), (5.5, 0.5, 69),
    (6.0, 0.5, 67), (6.5, 0.5, 65), (7.0, 0.5, 67), (7.5, 0.5, 69),

    (8.0, 0.5, 76), (8.5, 0.5, 79), (9.0, 0.5, 76), (9.5, 0.5, 74),
    (10.0, 0.5, 72), (10.5, 0.5, 76), (11.0, 0.5, 74), (11.5, 0.5, 72),

    (12.0, 0.5, 71), (12.5, 0.5, 74), (13.0, 0.5, 79), (13.5, 0.5, 77),
    (14.0, 0.5, 74), (14.5, 0.5, 71), (15.0, 1.0, 69),

    (16.0, 1.0, 69), (17.0, 0.5, 76), (17.5, 0.5, 74), (18.0, 0.5, 72),
    (18.5, 0.5, 71), (19.0, 0.5, 72), (19.5, 0.5, 76),

    (20.0, 0.5, 77), (20.5, 0.5, 76), (21.0, 0.5, 72), (21.5, 0.5, 69),
    (22.0, 0.5, 72), (22.5, 0.5, 74), (23.0, 0.5, 72), (23.5, 0.5, 69),

    (24.0, 0.5, 79), (24.5, 0.5, 76), (25.0, 0.5, 79), (25.5, 0.5, 81),
    (26.0, 0.5, 79), (26.5, 0.5, 76), (27.0, 0.5, 74), (27.5, 0.5, 76),

    (28.0, 0.5, 74), (28.5, 0.5, 71), (29.0, 0.5, 74), (29.5, 0.5, 76),
    (30.0, 1.0, 79), (31.0, 1.0, 74),
]


def section(bar):
    if bar < 2:
        return "intro"
    if bar < 10:
        return "verse"
    if bar < 14:
        return "build"
    if bar < 22:
        return "chorus"
    if bar < 26:
        return "break"
    if bar < 34:
        return "chorus2"
    return "outro"


for bar in range(TOTAL_BARS):
    start = bar * BAR
    sec = section(bar)
    root, chord = CHORDS[bar % 4]

    # ---- pad -----------------------------------------------------------
    if sec == "intro":
        pad(start, BAR, chord[1:], amp=0.075, attack=0.5)
    elif sec == "break":
        pad(start, BAR, chord, amp=0.075, attack=0.3)
    elif sec == "outro":
        pad(start, BAR * 1.6, chord, amp=0.08, attack=0.35)
    else:
        pad(start, BAR, chord[1:], amp=0.062, attack=0.12)

    # ---- arp -----------------------------------------------------------
    if sec in ("intro", "break", "outro"):
        step = BEAT / 2.0
        gain = 0.075 if sec == "intro" else 0.085
        pattern = [0, 1, 2, 1, 2, 3, 2, 1]
        for i in range(8):
            note = chord[pattern[i] % len(chord)] + 12
            arp(start + i * step, step * 0.9, note, amp=gain, pan=(-0.45 if i % 2 else 0.45))
    else:
        step = BEAT / 4.0
        pattern = [0, 2, 1, 2, 3, 2, 1, 2]
        gain = 0.052 if sec in ("chorus", "chorus2") else 0.07
        for i in range(16):
            note = chord[pattern[i % len(pattern)] % len(chord)] + 12
            accent = 1.0 if i % 4 == 0 else 0.72
            arp(start + i * step, step * 0.85, note, amp=gain * accent, pan=(-0.5 if i % 2 else 0.5))

    # ---- kick ----------------------------------------------------------
    if sec == "intro":
        if bar == 1:
            kick(start, 0.55)
            kick(start + BEAT * 2, 0.45)
    elif sec in ("verse", "chorus", "chorus2"):
        for beat in range(4):
            kick(start + beat * BEAT, 0.95)
    elif sec == "build":
        if bar < 13:
            for beat in range(4):
                kick(start + beat * BEAT, 0.92)
        else:
            kick(start, 0.95)
            kick(start + BEAT, 0.95)
    elif sec == "break":
        kick(start, 0.6)
        if bar == 25:
            kick(start + BEAT * 2, 0.5)
    elif sec == "outro":
        if bar in (34, 35):
            kick(start, 0.7)
            kick(start + BEAT * 2, 0.55)

    # ---- clap / snare --------------------------------------------------
    if sec in ("verse", "chorus", "chorus2"):
        clap(start + BEAT, 0.3)
        clap(start + BEAT * 3, 0.3)
    if sec == "build":
        if bar < 12:
            clap(start + BEAT, 0.26)
            clap(start + BEAT * 3, 0.26)
        elif bar == 12:
            for i in range(4):
                snare(start + BEAT * 2 + i * BEAT * 0.5, 0.2 + i * 0.03)
        else:
            for i in range(8):
                snare(start + i * BEAT * 0.5, 0.16 + i * 0.022)
            for i in range(4):
                snare(start + BEAT * 2 + BEAT * 0.5 + i * BEAT * 0.25, 0.24 + i * 0.03)
    if sec == "break" and bar == 25:
        for i in range(4):
            snare(start + BEAT * 3 + i * BEAT * 0.25, 0.17 + i * 0.03)

    # ---- hats ----------------------------------------------------------
    if sec in ("verse", "chorus", "chorus2", "build"):
        for i in range(8):
            offset = i * BEAT / 2.0
            gain = 0.085 if i % 2 else 0.055
            hat(start + offset, gain, open_hat=(i % 2 == 1 and sec in ("chorus", "chorus2")))
        if sec == "chorus2":
            for i in range(16):
                if i % 2 == 0:
                    hat(start + i * BEAT / 4.0, 0.032)
    if sec == "intro" and bar == 1:
        for i in range(4):
            hat(start + BEAT * 2 + i * BEAT / 2.0, 0.05)

    # ---- bass ----------------------------------------------------------
    if sec == "intro":
        if bar == 1:
            bass(start, BAR, root, amp=0.24)
    elif sec in ("verse", "build"):
        pattern = [0, 0, 0, 12, 0, 0, 12, 0]
        gain = 0.4 if sec == "verse" else 0.36
        for i in range(8):
            bass(start + i * BEAT / 2.0, BEAT * 0.46, root + pattern[i],
                 amp=gain, cutoff=0.14)
    elif sec in ("chorus", "chorus2"):
        pattern = [0, 0, 12, 0, 0, 0, 12, 0]
        for i in range(8):
            bass(start + i * BEAT / 2.0, BEAT * 0.44, root + pattern[i],
                 amp=0.42, cutoff=0.2)
    elif sec == "break":
        bass(start, BAR * 0.95, root, amp=0.3, cutoff=0.1)
    elif sec == "outro":
        if bar < 37:
            bass(start, BAR, root, amp=0.26, cutoff=0.09)

    # ---- lead ----------------------------------------------------------
    if sec in ("chorus", "chorus2"):
        chorus_index = (bar - 14) % 8 if sec == "chorus" else (bar - 26) % 8
        melody_start = chorus_index * BAR
        for beat_offset, length, note in MELODY:
            if melody_start <= beat_offset < melody_start + BAR:
                local = beat_offset - melody_start
                lead(start + local * BEAT, length * BEAT * 0.94, note,
                     amp=0.15, vibrato=0.0 if length < 0.75 else 0.006)
                if sec == "chorus2":
                    lead(start + local * BEAT + 0.008, length * BEAT * 0.94, note + 12,
                         amp=0.045, vibrato=0.004)

    # ---- transitions ---------------------------------------------------
    if sec == "build" and bar == 13:
        for i in range(4):
            lead(start + BEAT * 2 + i * BEAT * 0.25, BEAT * 0.22, [69, 72, 74, 76][i],
                 amp=0.11)
    if bar in (14, 26, 34):
        crash(bar * BAR, 0.24)
        impact(bar * BAR, 0.35)
    if bar == 37:
        crash(bar * BAR, 0.34)
        impact(bar * BAR, 0.5)

# riser across the build
riser(12 * BAR + BEAT * 2, BAR * 1.9, amp=0.14)


# --------------------------------------------------------------------------
# Effects + master
# --------------------------------------------------------------------------

delay = int(BEAT * 0.75 * SR)
for i in range(delay, N):
    SEND[i] += SEND[i - delay] * 0.34

for i in range(N):
    left = L[i]
    right = R[i]
    send = SEND[i] * 0.34
    L[i] = left + send
    R[i] = right + send * 0.82

peak = 0.0
for i in range(N):
    value = max(abs(L[i]), abs(R[i]))
    if value > peak:
        peak = value

gain = 0.9 / peak if peak > 0.0 else 1.0


def soft_clip(x):
    x = x * 1.05
    return x * (27.0 + x * x) / (27.0 + 9.0 * x * x)


frames = bytearray(N * 4)
for i in range(N):
    left = soft_clip(L[i] * gain)
    right = soft_clip(R[i] * gain)
    if left > 0.999:
        left = 0.999
    elif left < -0.999:
        left = -0.999
    if right > 0.999:
        right = 0.999
    elif right < -0.999:
        right = -0.999
    offset = i * 4
    value = int(left * 32767.0)
    frames[offset] = value & 0xFF
    frames[offset + 1] = (value >> 8) & 0xFF
    value = int(right * 32767.0)
    frames[offset + 2] = value & 0xFF
    frames[offset + 3] = (value >> 8) & 0xFF

with wave.open("neon_step.wav", "wb") as handle:
    handle.setnchannels(2)
    handle.setsampwidth(2)
    handle.setframerate(SR)
    handle.writeframes(bytes(frames))

print("wrote neon_step.wav  %.1fs  peak %.3f  gain %.3f" % (DURATION, peak, gain))
