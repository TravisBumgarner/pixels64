# displays_midenergy.py
# “Mid-energy” NeoPixel patterns: lively but not seizure-y.
# Structure matches your previous files: standalone display_* functions.
# Uses your existing common.py and config.get_led_index

import time, random, math
import machine, neopixel
from config import get_led_index
import common

neo_pin = machine.Pin(common.NEO_PIXEL_PIN, machine.Pin.OUT)
np = neopixel.NeoPixel(neo_pin, common.NEO_PIXEL_COUNT)
SIZE = common.DISPLAY_SIDE_LENGTH
COUNT = common.NEO_PIXEL_COUNT


# ---------- tiny helpers ----------


def fade_all(f=0.88):
    """Multiply every pixel by f (0..1) to create motion blur / persistence."""
    for i in range(COUNT):
        r, g, b = np[i]
        np[i] = (int(r * f), int(g * f), int(b * f))


def clamp01(v):
    if v < 0:
        return 0.0
    if v > 1:
        return 1.0
    return v


# ============================================================
# 1) Band Pulse — two diagonal bands chase each other
# ============================================================


def display_band_pulse():
    t = 0.0
    base_h = random.random()
    while True:
        t += 0.06
        base_h = (base_h + 0.0008) % 1.0
        for y in range(SIZE):
            for x in range(SIZE):
                u = (x + y) * 0.35
                v = (x - y) * 0.25
                w1 = 0.5 + 0.5 * math.sin(u + t)
                w2 = 0.5 + 0.5 * math.sin(v - t * 0.9)
                vout = 0.18 + 0.22 * (w1 * 0.6 + w2 * 0.4)
                hue = (base_h + 0.08 * w1 - 0.05 * w2) % 1.0
                np[get_led_index(y, x)] = common.hsv_to_rgb(hue, 0.5, vout)
        np.write()
        time.sleep(0.06)




# ============================================================
# 6) Wave Weave — two angled waves interlace; medium tempo
# ============================================================


def display_wave_weave():
    t = 0.0
    h0 = random.random()
    while True:
        t += 0.05
        h0 = (h0 + 0.001) % 1.0
        for y in range(SIZE):
            for x in range(SIZE):
                a = math.sin(0.35 * x + 0.22 * y + t)
                b = math.sin(-0.27 * x + 0.31 * y - t * 0.9)
                w = a * 0.6 + b * 0.4
                v = 0.16 + 0.22 * ((w + 1) / 2)
                h = (h0 + 0.1 * w) % 1.0
                np[get_led_index(y, x)] = common.hsv_to_rgb(h, 0.55, v)
        np.write()
        time.sleep(0.06)


# ============================================================
# 7) Noise Drift — cellular-ish noise scrolling diagonally
# ============================================================


def display_noise_drift():
    t = 0.0
    seed = random.random() * 1000

    def noise(x, y):
        # lightweight value noise
        n = math.sin((x * 12.9898 + y * 78.233 + seed) * 0.07)
        return (n + 1) * 0.5

    while True:
        t += 0.07
        for y in range(SIZE):
            for x in range(SIZE):
                v = noise(x * 0.6 + t, y * 0.6 - t)
                h = (0.58 + 0.12 * v) % 1.0
                np[get_led_index(y, x)] = common.hsv_to_rgb(h, 0.5, 0.18 + 0.22 * v)
        np.write()
        time.sleep(0.07)



# ============================================================
# 9) Dual Chase — two color stops chase along a serpentine path
# ============================================================


def display_dual_chase():
    # build serpentine order once
    path = []
    for y in range(SIZE):
        xs = range(SIZE) if y % 2 == 0 else reversed(range(SIZE))
        for x in xs:
            path.append((x, y))
    n = len(path)
    a, b = 0, n // 2
    ha, hb = random.random(), random.random()
    while True:
        fade_all(0.92)
        x1, y1 = path[a]
        x2, y2 = path[b]
        np[get_led_index(y1, x1)] = common.hsv_to_rgb(ha, 0.8, 0.4)
        np[get_led_index(y2, x2)] = common.hsv_to_rgb(hb, 0.8, 0.4)
        a = (a + 1) % n
        b = (b + 1) % n
        ha = (ha + 0.003) % 1.0
        hb = (hb + 0.002) % 1.0
        np.write()
        time.sleep(0.05)


# ============================================================
# 10) Checker Pulse — out-of-phase breathing per parity
# ============================================================


def display_checker_pulse():
    t = 0.0
    h0 = random.random()
    while True:
        t += 0.07
        h0 = (h0 + 0.001) % 1.0
        for y in range(SIZE):
            for x in range(SIZE):
                phase = 0.0 if ((x + y) & 1) == 0 else math.pi
                w = 0.5 + 0.5 * math.sin(t + phase)
                v = 0.14 + 0.24 * w
                hue = (h0 + 0.05 * w) % 1.0
                np[get_led_index(y, x)] = common.hsv_to_rgb(hue, 0.45, v)
        np.write()
        time.sleep(0.07)


