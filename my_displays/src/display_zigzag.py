from config import get_led_index
from common import NEO_PIXEL_PIN, NEO_PIXEL_COUNT
import time
import machine
import neopixel
import random

DISPLAY_SIDE_LENGTH = int(NEO_PIXEL_COUNT**0.5)

neo_pin = machine.Pin(NEO_PIXEL_PIN, machine.Pin.OUT)
np = neopixel.NeoPixel(neo_pin, NEO_PIXEL_COUNT)


def get_random_color():
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


def interpolate(c1, c2, fraction):
    return (
        int(c1[0] + (c2[0] - c1[0]) * fraction),
        int(c1[1] + (c2[1] - c1[1]) * fraction),
        int(c1[2] + (c2[2] - c1[2]) * fraction),
    )


def zigzag_order():
    """Yield coordinates in zig-zag pattern top→bottom."""
    while True:
        # top to bottom
        for y in range(DISPLAY_SIDE_LENGTH):
            if y % 2 == 0:  # left to right
                for x in range(DISPLAY_SIDE_LENGTH):
                    yield (x, y)
            else:  # right to left
                for x in reversed(range(DISPLAY_SIDE_LENGTH)):
                    yield (x, y)
        # bottom to top
        for y in reversed(range(DISPLAY_SIDE_LENGTH)):
            if y % 2 == 0:  # left to right
                for x in range(DISPLAY_SIDE_LENGTH):
                    yield (x, y)
            else:  # right to left
                for x in reversed(range(DISPLAY_SIDE_LENGTH)):
                    yield (x, y)


def display_zigzag():
    current_color = get_random_color()
    path = zigzag_order()

    while True:
        # pick target + number of steps
        target_color = get_random_color()
        steps = random.randint(30, 80)

        for i in range(steps):
            fraction = i / (steps - 1) if steps > 1 else 1.0
            color = interpolate(current_color, target_color, fraction)

            # move one LED along zigzag path
            x, y = next(path)
            np[get_led_index(y, x)] = color
            np.write()
            time.sleep(0.05)

        current_color = target_color


if __name__ == "__main__":
    display_zigzag()
