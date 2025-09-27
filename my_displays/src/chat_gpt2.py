# displays_mathsets.py
# 20 mid-energy displays: 4 math themes × 5 patterns each (calmer than arcade, not static).
# Drop next to common.py and config.py

import time, random, math
import machine, neopixel
from config import get_led_index
import common

# ---- setup ----
neo_pin = machine.Pin(common.NEO_PIXEL_PIN, machine.Pin.OUT)
np = neopixel.NeoPixel(neo_pin, common.NEO_PIXEL_COUNT)
SIZE = common.DISPLAY_SIDE_LENGTH
COUNT = common.NEO_PIXEL_COUNT

# ---- shim: math.hypot may be missing ----
try:
    hypot = math.hypot
except AttributeError:

    def hypot(x, y):
        return (x * x + y * y) ** 0.5


# ---- small helpers ----
def clamp01(v):
    if v < 0:
        return 0.0
    if v > 1:
        return 1.0
    return v


def fade_all(f=0.90):
    for i in range(COUNT):
        r, g, b = np[i]
        np[i] = (int(r * f), int(g * f), int(b * f))


# ============================================================
# THEME A — Complex / Fractal Dynamics
# ============================================================


# ============================================================
# THEME C — Space-Filling & Raster Orders
# ============================================================


# 11) Hilbert Wave — color wave along 8x8 Hilbert path
def display_hilbert_wave():
    def rot(n, x, y, rx, ry):
        if ry == 0:
            if rx == 1:
                x = n - 1 - x
                y = n - 1 - y
            x, y = y, x
        return x, y

    def d2xy(n, d):
        x = y = 0
        s = 1
        t = d
        while s < n:
            rx = 1 & (t // 2)
            ry = 1 & (t ^ rx)
            x, y = rot(s, x, y, rx, ry)
            x += s * rx
            y += s * ry
            t //= 4
            s *= 2
        return x, y

    path = [d2xy(SIZE, i) for i in range(SIZE * SIZE)]
    k = 0
    base = random.random()
    while True:
        fade_all(0.92)
        for i in range(SIZE // 2):
            idx = (k - i) % len(path)
            x, y = path[idx]
            color = common.hsv_to_rgb(
                (base + i * 0.02) % 1.0, 0.7, 0.35 * (1 - i / (SIZE // 2))
            )
            p = get_led_index(y, x)
            r0, g0, b0 = np[p]
            r1, g1, b1 = color
            np[p] = (min(255, r0 + r1), min(255, g0 + g1), min(255, b0 + b1))
        k = (k + 1) % len(path)
        base = (base + 0.002) % 1.0
        np.write()
        time.sleep(0.20)


# 12) Morton Weave (Z-order path)
def display_morton_weave():
    # deinterleave bits to x,y (3 bits for 8)
    def d2xy(d):
        x = ((d >> 0) & 1) | (((d >> 2) & 1) << 1) | (((d >> 4) & 1) << 2)
        y = ((d >> 1) & 1) | (((d >> 3) & 1) << 1) | (((d >> 5) & 1) << 2)
        return x, y

    path = [d2xy(i) for i in range(SIZE * SIZE)]
    k = 0
    hue = random.random()
    while True:
        fade_all(0.90)
        for i in range(6):
            x, y = path[(k + i * 3) % len(path)]
            idx = get_led_index(y, x)
            col = common.hsv_to_rgb((hue + i * 0.08) % 1.0, 0.7, 0.32)
            r, g, b = np[idx]
            rr, gg, bb = col
            np[idx] = (min(255, r + rr), min(255, g + gg), min(255, b + bb))
        k = (k + 1) % len(path)
        hue = (hue + 0.002) % 1.0
        np.write()
        time.sleep(0.20)


# 13) Spiral Scan (center outward), gradient along index
def display_spiral_scan():
    order = []
    x = y = SIZE // 2
    dx, dy = 1, 0
    step_len = 1
    order.append((x, y))
    while len(order) < SIZE * SIZE:
        for _ in range(step_len):
            x += dx
            y += dy
            if 0 <= x < SIZE and 0 <= y < SIZE:
                order.append((x, y))
            if len(order) >= SIZE * SIZE:
                break
        dx, dy = -dy, dx
        if dy == 0:
            step_len += 1
    k = 0
    base = random.random()
    while True:
        for i, (x, y) in enumerate(order):
            frac = (i + k) % len(order) / (len(order) - 1)
            h = (base + 0.25 * frac) % 1.0
            v = 0.12 + 0.22 * (1 - abs(0.5 - frac) * 2)
            np[get_led_index(y, x)] = common.hsv_to_rgb(h, 0.45, v)
        np.write()
        base = (base + 0.002) % 1.0
        k = (k + 1) % len(order)
        time.sleep(0.08)


# 14) JPEG Zigzag traversal painter
def display_jpeg_zigzag():
    order = []
    for s in range(0, 2 * SIZE - 1):
        if s % 2 == 0:
            x = min(s, SIZE - 1)
            y = s - x
            while x >= 0 and y < SIZE:
                order.append((x, y))
                x -= 1
                y += 1
        else:
            y = min(s, SIZE - 1)
            x = s - y
            while y >= 0 and x < SIZE:
                order.append((x, y))
                y -= 1
                x += 1
    k = 0
    hue = random.random()
    while True:
        fade_all(0.94)
        for i in range(5):
            x, y = order[(k + i * 2) % len(order)]
            idx = get_led_index(y, x)
            col = common.hsv_to_rgb((hue + i * 0.06) % 1.0, 0.65, 0.34)
            r, g, b = np[idx]
            rr, gg, bb = col
            np[idx] = (min(255, r + rr), min(255, g + gg), min(255, b + bb))
        k = (k + 1) % len(order)
        hue = (hue + 0.002) % 1.0
        np.write()
        time.sleep(0.20)


# 15) Diagonal Wave (sum over anti-/main diagonals)
def display_diagonal_wave():
    t = 0.0
    base = random.random()
    while True:
        t += 0.06
        base = (base + 0.001) % 1.0
        for y in range(SIZE):
            for x in range(SIZE):
                a = math.sin(0.6 * (x + y) + t)
                b = math.sin(0.6 * (x - y) - t * 0.8)
                w = (a * 0.6 + b * 0.4 + 2) / 4
                np[get_led_index(y, x)] = common.hsv_to_rgb(
                    (base + 0.12 * w) % 1.0, 0.55, 0.14 + 0.24 * w
                )
        np.write()
        time.sleep(0.06)


# ============================================================
# THEME D — Waves, Modes, & Spectral Tricks
# ============================================================


# 19) Voronoi Ripple: moving sites, sine of distance to nearest
def display_voronoi_ripple():
    sites = []
    for _ in range(5):
        sites.append(
            [
                random.uniform(0, SIZE - 1),
                random.uniform(0, SIZE - 1),
                random.uniform(-0.08, 0.08),
                random.uniform(-0.08, 0.08),
                random.random(),
            ]
        )
    t = 0.0
    while True:
        t += 0.05
        # move sites
        for s in sites:
            s[0] = (s[0] + s[2]) % SIZE
            s[1] = (s[1] + s[3]) % SIZE
            s[4] = (s[4] + 0.002) % 1.0
        for y in range(SIZE):
            for x in range(SIZE):
                best = 1e9
                hh = 0.0
                for sx, sy, _, __, h in sites:
                    d = hypot(x - sx, y - sy)
                    if d < best:
                        best = d
                        hh = h
                w = (math.sin(best * 0.9 - t * 0.8) + 1) / 2
                np[get_led_index(y, x)] = common.hsv_to_rgb(
                    (0.55 + 0.2 * hh) % 1.0, 0.55, 0.14 + 0.24 * w
                )
        np.write()
        time.sleep(0.06)
