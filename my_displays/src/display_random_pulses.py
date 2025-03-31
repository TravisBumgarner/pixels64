from config import LOOKUP
import time
import machine
import neopixel
import random

NEO_PIXEL_PIN = 13
NEO_PIXEL_COUNT = 64

neo_pin = machine.Pin(NEO_PIXEL_PIN, machine.Pin.OUT)
np = neopixel.NeoPixel(neo_pin, NEO_PIXEL_COUNT)


def fill_with_random_colors():
    for i in LOOKUP:
        np[i] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    np.write()


def interpolate_colors(current_color, target_color, steps=5, delay=0.05):
    r1, g1, b1 = current_color
    r2, g2, b2 = target_color

    for i in range(steps + 1):
        fraction = i / steps
        r = int(r1 + (r2 - r1) * fraction)
        g = int(g1 + (g2 - g1) * fraction)
        b = int(b1 + (b2 - b1) * fraction)
        yield (r, g, b)
        time.sleep(delay)


def display_random_pulses():
    fill_with_random_colors()

    while True:
        random_index = random.choice(LOOKUP)
        current_color = np[random_index]
        random_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

        for color in interpolate_colors(current_color, random_color):
            np[random_index] = color
            np.write()


# Currently doing just one display
all_displays = {
    "random_pulses": display_random_pulses,
}
