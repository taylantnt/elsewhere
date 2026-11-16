#!/usr/bin/env python3
"""Generate the NEON STEP art set: club backdrop, gems, receptors and FX.

Everything is drawn at 4x and downsampled, so edges stay clean at any GUI scale.
White assets are tinted per lane at runtime.
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageChops

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "game", "images", "dance")
os.makedirs(OUT, exist_ok=True)
random.seed(8842)

SS = 4


def save(image, name):
    path = os.path.join(OUT, name)
    image.save(path, optimize=True)
    print("wrote", name, image.size)



def paste_layer(base, layer, position):
    canvas = Image.new("RGBA", base.size, (0, 0, 0, 0))
    canvas.paste(layer, position, layer)
    return Image.alpha_composite(base, canvas)


def vertical_gradient(size, stops):
    """stops: list of (position 0..1, (r,g,b,a))"""
    width, height = size
    strip = Image.new("RGBA", (1, height))
    pixels = []
    for y in range(height):
        t = y / max(1, height - 1)
        for index in range(len(stops) - 1):
            p0, c0 = stops[index]
            p1, c1 = stops[index + 1]
            if p0 <= t <= p1:
                k = (t - p0) / max(1e-6, p1 - p0)
                pixels.append(tuple(int(c0[i] + (c1[i] - c0[i]) * k) for i in range(4)))
                break
        else:
            pixels.append(stops[-1][1])
    strip.putdata(pixels)
    return strip.resize(size, Image.BILINEAR)


def radial_glow(size, color, power=2.4, radius=1.0):
    width, height = size
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    pixels = []
    cx, cy = width / 2.0, height / 2.0
    max_dist = min(cx, cy) * radius
    r, g, b, a = color
    for y in range(height):
        for x in range(width):
            d = math.hypot(x - cx, y - cy) / max_dist
            if d >= 1.0:
                pixels.append((0, 0, 0, 0))
            else:
                k = (1.0 - d) ** power
                pixels.append((r, g, b, int(a * k)))
    image.putdata(pixels)
    return image


# ---------------------------------------------------------------- backdrop


def make_lane_panel():
    width, height = 156, 568
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = []
    for y in range(height):
        t = y / (height - 1)
        base_alpha = int(16 + 46 * (t ** 1.25))
        for x in range(width):
            edge = min(x, width - 1 - x)
            if edge < 2:
                alpha = base_alpha + 95
            elif edge < 9:
                alpha = base_alpha + int(34 * (1.0 - (edge - 2) / 7.0))
            else:
                alpha = base_alpha
            pixels.append((255, 255, 255, alpha))
    image.putdata(pixels)
    save(image, "lane_panel.png")



def make_background():
    width, height = 1280, 720
    image = vertical_gradient((width, height), [
        (0.00, (4, 5, 14, 255)),
        (0.35, (9, 8, 26, 255)),
        (0.58, (26, 12, 44, 255)),
        (0.70, (46, 16, 58, 255)),
        (0.72, (12, 8, 24, 255)),
        (1.00, (4, 4, 12, 255)),
    ])

    # stars
    stars = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(stars)
    for _ in range(260):
        x = random.randint(0, width - 1)
        y = random.randint(0, 452)
        size = random.choice((1, 1, 1, 2))
        alpha = random.randint(40, 190)
        draw.ellipse([x, y, x + size, y + size], fill=(200, 226, 255, alpha))
    image = Image.alpha_composite(image, stars)

    # skyline, three depth layers
    def skyline(layer_y, tint, window_alpha, max_height, step, seed_colors):
        layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        x = -40
        while x < width + 60:
            w = random.randint(step, step * 2)
            h = random.randint(max_height // 3, max_height)
            top = layer_y - h
            draw.rectangle([x, top, x + w, layer_y], fill=tint)
            # roof details
            if random.random() < 0.35:
                draw.rectangle([x + w // 2 - 2, top - random.randint(6, 26), x + w // 2 + 2, top],
                               fill=tint)
            # windows
            for wx in range(x + 8, x + w - 8, 12):
                for wy in range(top + 10, layer_y - 10, 14):
                    if random.random() < 0.42:
                        color = random.choice(seed_colors)
                        draw.rectangle([wx, wy, wx + 3, wy + 5],
                                       fill=(color[0], color[1], color[2], window_alpha))
            x += w + random.randint(6, 18)
        return layer

    image = Image.alpha_composite(image, skyline(
        478, (10, 12, 30, 255), 74, 190, 34,
        [(120, 220, 255), (255, 120, 190), (255, 200, 120)]))
    image = Image.alpha_composite(image, skyline(
        500, (7, 9, 24, 255), 100, 140, 46,
        [(110, 200, 255), (255, 130, 180), (255, 190, 130)]))

    # horizon neon band
    horizon = Image.new("RGBA", (width, 40), (0, 0, 0, 0))
    hdraw = ImageDraw.Draw(horizon)
    for y in range(40):
        k = 1.0 - abs(y - 20) / 20.0
        hdraw.rectangle([0, y, width, y + 1],
                        fill=(255, 70, 170, int(70 * k * k)))
    image = paste_layer(image, horizon, (0, 480 - 20))
    haze = radial_glow((900, 300), (255, 80, 170, 38), power=2.6)
    image = paste_layer(image, haze, (640 - 450, 500 - 150))

    # dance floor perspective grid
    floor = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(floor)
    vanish = (640, 478)
    for i in range(-14, 15):
        x_bottom = 640 + i * 96
        draw.line([vanish, (x_bottom, height)], fill=(90, 200, 255, 26), width=1)
    y = 478
    gap = 6
    while y < height:
        draw.line([(0, y), (width, y)], fill=(180, 90, 255, 30), width=1)
        gap *= 1.42
        y += gap
    image = Image.alpha_composite(image, floor)

    # stage light pools
    for cx, color in ((240, (90, 220, 255, 46)), (1040, (255, 90, 190, 46))):
        pool = radial_glow((620, 320), color, power=2.2)
        image = paste_layer(image, pool, (cx - 310, 700 - 160))

    # speaker stacks at the edges
    def speaker(x, y, w, h, flip=False):
        block = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(block)
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=8, fill=(8, 10, 20, 255),
                            outline=(52, 66, 96, 255), width=2)
        for offset in range(16, h - 10, 26):
            d.ellipse([w // 2 - 14, offset, w // 2 + 14, offset + 22],
                      fill=(4, 5, 12, 255), outline=(38, 48, 72, 255))
        return block

    image = paste_layer(image, speaker(22, 470, 88, 210), (22, 470))
    image = paste_layer(image, speaker(1170, 470, 88, 210), (1170, 470))

    # subtle grain
    grain = Image.effect_noise((width, height), 16).convert("L")
    grain_rgba = Image.merge("RGBA", (grain, grain, grain,
                                      Image.new("L", (width, height), 10)))
    image = Image.alpha_composite(image, grain_rgba)
    save(image, "bg_neon_club.png")


# ------------------------------------------------------------------- panels


def make_dialog_panel():
    width, height = 820, 600
    scale = 3
    big = Image.new("RGBA", (width * scale, height * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(big)
    radius = 24 * scale
    draw.rounded_rectangle([0, 0, width * scale - 1, height * scale - 1],
                           radius=radius, fill=(7, 12, 22, 246))
    draw.rounded_rectangle([2, 2, width * scale - 3, height * scale - 3],
                           radius=radius, outline=(74, 118, 164, 130), width=2 * scale)
    draw.rounded_rectangle([2 * scale, 2 * scale, width * scale - 3, 76 * scale],
                           radius=radius, fill=(110, 170, 230, 14))
    save(big.resize((width, height), Image.LANCZOS), "dialog_panel.png")



def make_panel():
    width, height = 300, 580
    scale = 3
    big = Image.new("RGBA", (width * scale, height * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(big)
    radius = 20 * scale
    draw.rounded_rectangle([0, 0, width * scale - 1, height * scale - 1],
                           radius=radius, fill=(9, 14, 30, 208))
    draw.rounded_rectangle([1, 1, width * scale - 1, height * scale - 1],
                           radius=radius, outline=(90, 130, 190, 90), width=1 * scale)
    # top sheen
    draw.rounded_rectangle([1 * scale, 1 * scale, width * scale - 1, 90 * scale],
                           radius=radius, fill=(120, 170, 230, 16))
    glow = big.filter(ImageFilter.GaussianBlur(6 * scale))
    combined = Image.alpha_composite(glow, big)
    save(combined.resize((width, height), Image.LANCZOS), "hud_panel.png")


def make_note_gem():
    size = 512
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    # rounded diamond mask
    mask = Image.new("L", (size, size), 0)
    mdraw = ImageDraw.Draw(mask)
    box = [122, 122, 390, 390]
    mdraw.rounded_rectangle(box, radius=54, fill=255)
    mask = mask.rotate(45, resample=Image.BICUBIC)

    # vertical gloss gradient
    body = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(body)
    for y in range(0, size, 2):
        t = y / size
        if t < 0.45:
            value = int(255 - t * 40)
        else:
            value = int(236 - (t - 0.45) * 170)
        bdraw.rectangle([0, y, size, y + 2], fill=(value, value, min(255, value + 8), 255))
    body.putalpha(mask)

    # inner shading at bottom
    shade = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shade)
    sdraw.rounded_rectangle([150, 230, 362, 380], radius=36, fill=(20, 24, 40, 70))
    shade = shade.filter(ImageFilter.GaussianBlur(18))
    body = Image.alpha_composite(body, Image.composite(
        shade, Image.new("RGBA", (size, size), (0, 0, 0, 0)), mask))
    body.putalpha(mask)

    # rim light
    rim = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    rdraw = ImageDraw.Draw(rim)
    rdraw.rounded_rectangle([128, 128, 384, 384], radius=52, outline=(255, 255, 255, 235),
                            width=7)
    rim = rim.rotate(45, resample=Image.BICUBIC)
    rim.putalpha(ImageChops.multiply(rim.getchannel("A"), mask))
    body = Image.alpha_composite(body, rim)

    # specular highlight
    glint = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glint)
    gdraw.ellipse([190, 168, 300, 236], fill=(255, 255, 255, 140))
    glint = glint.filter(ImageFilter.GaussianBlur(12))
    glint.putalpha(ImageChops.multiply(glint.getchannel("A"), mask))
    body = Image.alpha_composite(body, glint)

    # outer glow
    halo = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    hdraw = ImageDraw.Draw(halo)
    hdraw.rounded_rectangle([126, 126, 386, 386], radius=54, fill=(255, 255, 255, 120))
    halo = halo.rotate(45, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(26))
    halo.putalpha(ImageChops.multiply(halo.getchannel("A"), mask))
    body = Image.alpha_composite(halo, body)

    save(body.resize((96, 96), Image.LANCZOS), "note_gem.png")


def make_trail():
    width, height = 24, 160
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = []
    for y in range(height):
        t = y / (height - 1)
        alpha = int(120 * (t ** 1.7))
        half = 4 + int(5 * t)
        for x in range(width):
            d = abs(x - width / 2.0) / half
            if d >= 1.0:
                pixels.append((255, 255, 255, 0))
            else:
                pixels.append((255, 255, 255, int(alpha * (1.0 - d * d))))
    image.putdata(pixels)
    save(image, "note_trail.png")


def make_receptor():
    width, height = 168, 60
    scale = 4
    big = Image.new("RGBA", (width * scale, height * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(big)
    pad = 10 * scale
    draw.rounded_rectangle([pad, pad, width * scale - pad, height * scale - pad],
                           radius=16 * scale, fill=(255, 255, 255, 40),
                           outline=(255, 255, 255, 150), width=2 * scale)
    inner = big.filter(ImageFilter.GaussianBlur(6 * scale))
    combined = Image.alpha_composite(inner, big)
    save(combined.resize((width, height), Image.LANCZOS), "receptor_pad.png")

    # ring
    ring = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    pixels = []
    for y in range(200):
        for x in range(200):
            d = math.hypot(x - 100, y - 100)
            if d > 96:
                pixels.append((0, 0, 0, 0))
                continue
            edge = abs(d - 76.0)
            k = max(0.0, 1.0 - edge / 10.0)
            alpha = int(210 * (k ** 2))
            pixels.append((255, 255, 255, alpha))
    ring.putdata(pixels)
    ring = ring.filter(ImageFilter.GaussianBlur(1.2))
    save(ring.resize((160, 160), Image.LANCZOS), "receptor_ring.png")


def make_fx():
    save(radial_glow((160, 160), (255, 255, 255, 220), power=2.6), "glow.png")

    # burst ring
    size = 256
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    pixels = []
    for y in range(size):
        for x in range(size):
            d = math.hypot(x - size / 2.0, y - size / 2.0)
            k = max(0.0, 1.0 - abs(d - 92.0) / 34.0)
            alpha = int(235 * (k ** 1.7))
            pixels.append((255, 255, 255, alpha))
    image.putdata(pixels)
    save(image.filter(ImageFilter.GaussianBlur(2)), "burst.png")

    # spark streak
    spark = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    pixels = []
    for y in range(32):
        for x in range(32):
            dx = (x - 16) / 3.2
            dy = (y - 16) / 12.0
            d = math.hypot(dx, dy)
            alpha = 0 if d >= 1 else int(230 * (1 - d) ** 1.5)
            pixels.append((255, 255, 255, alpha))
    spark.putdata(pixels)
    save(spark.filter(ImageFilter.GaussianBlur(1.1)), "spark.png")


def make_beam():
    width, height = 800, 800
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = []
    apex_x = width / 2.0
    for y in range(height):
        t = y / height
        half = 26.0 + 360.0 * t
        fade = max(0.0, 1.0 - t) ** 1.5
        for x in range(width):
            dx = abs(x - apex_x)
            if dx >= half:
                pixels.append((255, 255, 255, 0))
            else:
                k = (1.0 - dx / half) ** 1.8
                pixels.append((255, 255, 255, int(96 * k * fade)))
    image.putdata(pixels)
    save(image, "beam.png")


def make_vignette():
    width, height = 1280, 720
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = []
    cx, cy = width / 2.0, height / 2.0
    max_d = math.hypot(cx, cy)
    for y in range(height):
        for x in range(width):
            d = math.hypot(x - cx, y - cy) / max_d
            k = max(0.0, (d - 0.42) / 0.58)
            pixels.append((0, 0, 0, int(150 * (k ** 1.7))))
    image.putdata(pixels)
    save(image, "vignette.png")


def make_floor_glow():
    width = 1280
    image = Image.new("RGBA", (width, 120), (0, 0, 0, 0))
    pixels = []
    for y in range(120):
        t = y / 119.0
        alpha = int(90 * (1 - t) ** 2)
        for x in range(width):
            edge = min(x, width - 1 - x) / 300.0
            k = min(1.0, edge) if edge < 1 else 1.0
            pixels.append((120, 210, 255, int(alpha * k * 0.5)))
    image.putdata(pixels)
    save(image, "floor_glow.png")


make_background()
make_lane_panel()
make_panel()
make_dialog_panel()
make_note_gem()
make_trail()
make_receptor()
make_fx()
make_beam()
make_vignette()
make_floor_glow()
print("done")
