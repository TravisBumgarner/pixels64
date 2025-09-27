# displays_midenergy.py
# “Mid-energy” NeoPixel patterns: lively but not seizure-y.
# Structure matches your previous files: standalone display_* functions.
# Uses your existing common.py and config.get_led_index

import time, random
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
# 9) Dual Chase — two color stops chase along a serpentine path
# ============================================================


def display_dual_chase():
    # Build serpentine paths for horizontal (rows) and vertical (columns)
    path_h = []
    for y in range(SIZE):
        xs = range(SIZE) if y % 2 == 0 else reversed(range(SIZE))
        for x in xs:
            path_h.append((x, y))

    path_v = []
    for x in range(SIZE):
        ys = range(SIZE) if x % 2 == 0 else reversed(range(SIZE))
        for y in ys:
            path_v.append((x, y))

    n = len(path_h)  # == SIZE*SIZE == len(path_v)

    # Two heads, opposite along the path
    a, b = 0, n // 2

    # Hue pair: complementary colors
    h = random.random()  # head A
    # head B will use (h + 0.5) % 1.0

    # Mode toggles: start horizontal, then vertical, repeat
    horizontal = True
    steps_in_mode = 0
    SWITCH_AFTER = n  # switch after a full traversal; tweak if you want faster switches

    while True:
        fade_all(0.92)

        path = path_h if horizontal else path_v

        x1, y1 = path[a]
        x2, y2 = path[b]

        c1 = common.hsv_to_rgb(h % 1.0, 0.8, 0.4)
        c2 = common.hsv_to_rgb((h + 0.5) % 1.0, 0.8, 0.4)

        np[get_led_index(y1, x1)] = c1
        np[get_led_index(y2, x2)] = c2

        # advance both heads together along the current orientation
        a = (a + 1) % n
        b = (b + 1) % n

        # gentle hue drift; complement follows automatically
        h = (h + 0.003) % 1.0

        steps_in_mode += 1
        if steps_in_mode >= SWITCH_AFTER:
            horizontal = not horizontal
            steps_in_mode = 0
            # keep the same indices so heads continue from analogous positions in the new path

        np.write()
        time.sleep(0.05)
