from config import LOOKUP
import time
import machine
import neopixel
import random

NEO_PIXEL_PIN = 13
NEO_PIXEL_COUNT = 64

neo_pin = machine.Pin(NEO_PIXEL_PIN, machine.Pin.OUT)
np = neopixel.NeoPixel(neo_pin, NEO_PIXEL_COUNT)


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


def display_spiral():
    x, y = 3, 3  # Center
    spiral = []
    size = 1
    dx, dy = 1, 0  # Start going right
    while len(spiral) < 64:
        for _ in range(2):  # Each direction is done twice
            for _ in range(size):  # Move 'size' steps in current direction
                if 0 <= x < 8 and 0 <= y < 8:
                    spiral.append(y * 8 + x)
                x, y = x + dx, y + dy
            dx, dy = -dy, dx  # Rotate 90 degrees
        size += 1

    while True:
        for i, pos in enumerate(spiral):
            np[LOOKUP[pos]] = (255, 0, 0)
            np.write()
            time.sleep_ms(50)
            np[LOOKUP[pos]] = (0, 0, 0)


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


all_displays = {
    "random_color": display_random_color,
    "snake": display_snake,
    "spiral": display_spiral,
    "firework": display_firework,
}
