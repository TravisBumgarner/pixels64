from config import get_led_index
import time
import machine
import neopixel
import random

NEO_PIXEL_PIN = 13
NEO_PIXEL_COUNT = 64

DISPLAY_SIDE_LENGTH = int(NEO_PIXEL_COUNT**0.5)  # Assuming a square layout

neo_pin = machine.Pin(NEO_PIXEL_PIN, machine.Pin.OUT)
np = neopixel.NeoPixel(neo_pin, NEO_PIXEL_COUNT)

SQUARE_ORIGINS = [
    (i, j)
    for i in range(0, DISPLAY_SIDE_LENGTH, 2)
    for j in range(0, DISPLAY_SIDE_LENGTH, 2)
]


def fill_square(x, y, color):
    # Fill a 2x2 square starting at position (x, y)
    for i in range(2):
        for j in range(2):
            led_index = get_led_index(y + i, x + j)
            if led_index is not None:
                np[led_index] = color
    np.write()


def init():
    for i in range(0, DISPLAY_SIDE_LENGTH, 2):
        for j in range(0, DISPLAY_SIDE_LENGTH, 2):
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            fill_square(j, i, color)
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


# Don't return to recently used squares
def get_next_square(last_displayed):
    available_squares = [sq for sq in SQUARE_ORIGINS if sq not in last_displayed]
    if not available_squares:
        last_displayed.pop(0)  # Remove the oldest
        available_squares = SQUARE_ORIGINS
    next_square = random.choice(available_squares)
    last_displayed.append(next_square)
    if len(last_displayed) > 3:  # Keep only last 3
        last_displayed.pop(0)
    return next_square


def display_gradient_squares():
    init()
    last_displayed = []  # Simple list instead of Queue

    while True:
        x, y = get_next_square(last_displayed)

        current_color = np[get_led_index(y, x)]
        random_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

        for color in interpolate_colors(current_color, random_color):
            fill_square(x, y, color)
            time.sleep(0.05)


if __name__ == "__main__":
    display_gradient_squares()
