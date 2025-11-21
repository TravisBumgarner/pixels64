from config import LOOKUP
import time
import machine
import neopixel
import random
from common import NEO_PIXEL_PIN, NEO_PIXEL_COUNT

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


def fisher_yates_shuffle(arr):
    for i in range(len(arr) - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]


def shuffled_array(n):
    arr = list(range(n))
    fisher_yates_shuffle(arr)
    return arr


def display_random_pulses_towards_color():
    target_color = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )
    fill_with_random_colors()

    while True:
        sequence = shuffled_array(len(LOOKUP))
        for i in sequence[: len(sequence) // 2]:  # Only first half
            current_color = np[LOOKUP[i]]
            new_color = tuple(
                int(current + (target - current) * 0.7)
                for current, target in zip(current_color, target_color)
            )
            np[LOOKUP[i]] = new_color
            np.write()
            time.sleep(0.1)

        target_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )


if __name__ == "__main__":
    display_random_pulses_towards_color()
