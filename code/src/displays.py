from config import LOOKUP
import time
import machine
import neopixel
import random
import math

NEO_PIXEL_PIN = 13
NEO_PIXEL_COUNT = 64

neo_pin = machine.Pin(NEO_PIXEL_PIN, machine.Pin.OUT)
np = neopixel.NeoPixel(neo_pin, NEO_PIXEL_COUNT)


def hsv_to_rgb(h, s, v):
    if s == 0:
        return (v, v, v)
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))
    if i % 6 == 0:
        return (v, t, p)
    if i % 6 == 1:
        return (q, v, p)
    if i % 6 == 2:
        return (p, v, t)
    if i % 6 == 3:
        return (p, q, v)
    if i % 6 == 4:
        return (t, p, v)
    if i % 6 == 5:
        return (v, p, q)


def display_random_color():
    for i in LOOKUP:
        np[i] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    np.write()


def display_snake():
    pos = 0
    trail_length = 5
    while True:
        for i in range(NEO_PIXEL_COUNT):
            np[LOOKUP[i]] = (0, 0, 0)
        # Draw trail
        for t in range(trail_length):
            trail_pos = (pos - t) % NEO_PIXEL_COUNT
            brightness = 255 - (t * 255 // trail_length)
            np[LOOKUP[trail_pos]] = (brightness, 0, brightness)
        np.write()
        pos = (pos + 1) % NEO_PIXEL_COUNT
        time.sleep_ms(50)




def display_firework():
    while True:
        # Launch
        start_x = random.randint(0, 7)
        for y in range(7, -1, -1):
            for i in range(NEO_PIXEL_COUNT):
                np[LOOKUP[i]] = (0, 0, 0)
            np[LOOKUP[y * 8 + start_x]] = (255, 255, 0)
            np.write()
            time.sleep_ms(100)

        # Explode
        center_x, center_y = start_x, 0
        for radius in range(5):
            for i in range(NEO_PIXEL_COUNT):
                x, y = i % 8, i // 8
                dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                if dist <= radius:
                    np[LOOKUP[i]] = (255, 64, 0)
            np.write()
            time.sleep_ms(100)

        # Fade
        for brightness in range(255, -1, -25):
            for i in range(NEO_PIXEL_COUNT):
                x, y = i % 8, i // 8
                dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                if dist <= 4:
                    np[LOOKUP[i]] = (brightness, brightness // 4, 0)
            np.write()
            time.sleep_ms(50)



def display_wave():
    t = 0
    while True:
        for x in range(8):
            for y in range(8):
                # Create sine wave pattern
                val = math.sin(x / 2 + t) * math.cos(y / 2 + t) * 127 + 128
                np[LOOKUP[y * 8 + x]] = (0, int(val), int(val))
        np.write()
        t += 0.2
        time.sleep_ms(50)



# Helper function
def clear_display():
    for i in range(NEO_PIXEL_COUNT):
        np[LOOKUP[i]] = (0, 0, 0)


def display_gentle_breath():
    brightness = 0
    while True:
        # Very slow breathing effect
        brightness = (
            (math.sin(time.ticks_ms() / 5000) + 1) / 2 * 64
        )  # Max 64 brightness
        for i in range(NEO_PIXEL_COUNT):
            np[LOOKUP[i]] = (int(brightness), int(brightness / 2), int(brightness / 4))
        np.write()
        time.sleep_ms(100)



def display_ocean_depth():
    t = 0
    while True:
        for y in range(8):
            for x in range(8):
                # Darker at bottom, lighter at top
                base = 30 - (y * 3)
                wave = math.sin(x / 4 + t / 10) * 5
                np[LOOKUP[y * 8 + x]] = (0, int(base + wave), int((base + wave) * 1.2))
        np.write()
        t += 1
        time.sleep_ms(200)


def display_candlelight():
    base_brightness = 30
    while True:
        for i in range(NEO_PIXEL_COUNT):
            flicker = random.randint(-5, 5)
            brightness = base_brightness + flicker
            np[LOOKUP[i]] = (brightness, int(brightness / 2), 0)
        np.write()
        time.sleep_ms(100)



def display_quiet_pulse():
    t = 0
    while True:
        center_y = 3.5 + math.sin(t / 20) * 2
        center_x = 3.5 + math.cos(t / 20) * 2
        for y in range(8):
            for x in range(8):
                dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                brightness = max(0, 20 - dist * 6)
                np[LOOKUP[y * 8 + x]] = (
                    int(brightness),
                    int(brightness),
                    int(brightness),
                )
        np.write()
        t += 1
        time.sleep_ms(100)


def display_sunset():
    while True:
        for y in range(8):
            for x in range(8):
                height = (7 - y) / 7  # 1 at top, 0 at bottom
                r = int(255 * height)
                g = int(128 * height)
                b = int(50 * (1 - height))
                np[LOOKUP[y * 8 + x]] = (r, g, b)
        np.write()
        time.sleep_ms(500)



def display_fireplace():
    while True:
        for y in range(8):
            for x in range(8):
                flicker = random.randint(-30, 30)
                base = 255 - (y * 25)  # Brighter at bottom
                r = max(0, min(255, base + flicker))
                g = max(0, min(255, r // 2 + flicker))
                np[LOOKUP[y * 8 + x]] = (r, g, 0)
        np.write()
        time.sleep_ms(100)


# Update all_displays
all_displays = {
    "firework": display_firework,
    "random_color": display_random_color,
    "snake": display_snake,
    "wave": display_wave,
    "gentle_breath": display_gentle_breath,
    "ocean_depth": display_ocean_depth,
    "candlelight": display_candlelight,
    "quiet_pulse": display_quiet_pulse,
    "sunset": display_sunset,
    "fireplace": display_fireplace,
}
