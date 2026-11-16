#!/usr/bin/env python3
"""Generate the short sound effects used by the dance minigame."""

import math
import os
import random
import struct
import wave

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "game", "audio", "SFX")
os.makedirs(OUT, exist_ok=True)
SR = 44100
random.seed(5511)


def write(name, samples):
    path = os.path.join(OUT, name)
    frames = bytearray()
    for value in samples:
        value = max(-1.0, min(1.0, value))
        frames += struct.pack("<h", int(value * 32767))
    with wave.open(path, "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(SR)
        handle.writeframes(bytes(frames))
    print("wrote", name, "%.2fs" % (len(samples) / SR))


def pluck(freq, duration=0.13, amp=0.5, bright=0.5, click=0.25):
    n = int(duration * SR)
    out = []
    phase = 0.0
    phase2 = 0.0
    prev = 0.0
    for k in range(n):
        t = k / SR
        env = math.exp(-t * 26.0) * (1.0 - math.exp(-t * 900.0))
        f = freq * (1.0 + 0.06 * math.exp(-t * 60.0))
        phase += 2.0 * math.pi * f / SR
        phase2 += 2.0 * math.pi * f * 2.01 / SR
        s = math.sin(phase) * 0.7 + math.sin(phase2) * 0.22 * bright
        noise = random.random() * 2.0 - 1.0
        high = noise - prev
        prev = noise
        s += high * click * math.exp(-t * 240.0)
        out.append(s * env * amp)
    return out


def thud(freq=90.0, duration=0.26, amp=0.55):
    n = int(duration * SR)
    out = []
    phase = 0.0
    for k in range(n):
        t = k / SR
        env = math.exp(-t * 12.0)
        f = freq * (1.0 + 0.9 * math.exp(-t * 22.0))
        phase += 2.0 * math.pi * f / SR
        s = math.sin(phase) * 0.8
        s += (random.random() * 2.0 - 1.0) * 0.12 * math.exp(-t * 45.0)
        out.append(s * env * amp)
    return out


def shimmer(duration=0.9, amp=0.3):
    n = int(duration * SR)
    out = [0.0] * n
    notes = [(880.0, 0.0), (1108.7, 0.07), (1318.5, 0.14), (1760.0, 0.21), (2217.5, 0.28)]
    for freq, offset in notes:
        start = int(offset * SR)
        tone = pluck(freq, 0.42, amp=0.34, bright=0.25, click=0.08)
        for k, value in enumerate(tone):
            index = start + k
            if index >= n:
                break
            out[index] += value
    return out


def blip(freqs, duration=0.16, amp=0.35):
    n = int(duration * SR)
    out = []
    for k in range(n):
        t = k / SR
        freq = freqs[min(len(freqs) - 1, int(t / (duration / len(freqs))))]
        env = math.exp(-t * 14.0)
        out.append(math.sin(2.0 * math.pi * freq * t) * env * amp)
    return out


write("dance_hit0.wav", pluck(1046.5))
write("dance_hit1.wav", pluck(1174.7))
write("dance_hit2.wav", pluck(1318.5))
write("dance_hit3.wav", pluck(1568.0))
write("dance_miss.wav", thud(78.0, amp=0.5))
write("dance_fever.wav", shimmer(amp=0.26))
write("dance_select.wav", blip([660.0, 990.0], amp=0.3))
write("dance_start.wav", blip([523.3, 659.3, 784.0, 1046.5], duration=0.34, amp=0.32))
