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


def display_rain():
    while True:
        # Move all pixels down
        for y in range(7, 0, -1):
            for x in range(8):
                i = y * 8 + x
                prev = (y - 1) * 8 + x
                np[LOOKUP[i]] = np[LOOKUP[prev]]

        # Generate new drops at top
        for x in range(8):
            if random.random() < 0.1:  # 10% chance of drop
                np[LOOKUP[x]] = (0, 0, 255)
            else:
                np[LOOKUP[x]] = (0, 0, 0)
        np.write()
        time.sleep_ms(100)


def display_bounce():
    x, y = 0, 0
    dx, dy = 1, 1
    while True:
        np[LOOKUP[y * 8 + x]] = (0, 0, 0)

        x += dx
        y += dy
        if x >= 7 or x <= 0:
            dx *= -1
        if y >= 7 or y <= 0:
            dy *= -1

        np[LOOKUP[y * 8 + x]] = (255, 255, 0)
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


def display_matrix():
    cols = [0] * 8  # Column heights
    speeds = [random.randint(1, 3) for _ in range(8)]
    while True:
        for x in range(8):
            for y in range(8):
                i = y * 8 + x
                if y < cols[x]:
                    brightness = 255 if y == cols[x] - 1 else 64
                    np[LOOKUP[i]] = (0, brightness, 0)
                else:
                    np[LOOKUP[i]] = (0, 0, 0)
            cols[x] = (cols[x] + speeds[x] / 10) % 12
        np.write()
        time.sleep_ms(50)


def display_sparkle():
    while True:
        for _ in range(5):  # Number of active sparkles
            i = random.randint(0, 63)
            np[LOOKUP[i]] = (255, 255, 255)
        np.write()
        time.sleep_ms(50)
        clear_display()


def display_checkerboard():
    t = 0
    while True:
        for x in range(8):
            for y in range(8):
                if (x + y + t) % 2 == 0:
                    np[LOOKUP[y * 8 + x]] = (255, 0, 0)
                else:
                    np[LOOKUP[y * 8 + x]] = (0, 0, 255)
        np.write()
        t += 1
        time.sleep_ms(500)


def display_radar():
    angle = 0
    while True:
        for i in range(64):
            x, y = i % 8 - 3.5, i // 8 - 3.5
            beam_angle = math.atan2(y, x)
            if abs(beam_angle - angle) < 0.5:
                dist = (x * x + y * y) ** 0.5
                brightness = max(0, int(255 * (1 - dist / 5)))
                np[LOOKUP[i]] = (0, brightness, 0)
            else:
                np[LOOKUP[i]] = (0, 0, 0)
        np.write()
        angle = (angle + 0.2) % (2 * math.pi)
        time.sleep_ms(50)


def display_tetris():
    pieces = [
        [(0, 0), (1, 0), (2, 0), (3, 0)],  # I
        [(0, 0), (1, 0), (0, 1), (1, 1)],  # O
        [(1, 0), (0, 1), (1, 1), (2, 1)],  # T
    ]
    board = [[0] * 8 for _ in range(8)]
    while True:
        piece = random.choice(pieces)
        x, y = 3, 0
        while y < 7:
            clear_display()
            # Draw board
            for bx in range(8):
                for by in range(8):
                    if board[by][bx]:
                        np[LOOKUP[by * 8 + bx]] = (64, 64, 255)
            # Draw piece
            for px, py in piece:
                np[LOOKUP[(y + py) * 8 + (x + px)]] = (255, 255, 255)
            np.write()
            y += 1
            time.sleep_ms(300)
        # Lock piece
        for px, py in piece:
            board[y + py - 1][x + px] = 1
        # Clear lines
        for by in range(7, -1, -1):
            if all(board[by]):
                del board[by]
                board.insert(0, [0] * 8)


def display_dna():
    t = 0
    while True:
        for y in range(8):
            x = int(3.5 + math.sin(t + y / 2) * 2)
            np[LOOKUP[y * 8 + x]] = (255, 0, 0)
            x2 = int(3.5 + math.sin(t + y / 2 + math.pi) * 2)
            np[LOOKUP[y * 8 + x2]] = (0, 0, 255)
            if y % 2 == 0:
                np[LOOKUP[y * 8 + (x + x2) // 2]] = (255, 255, 0)
        np.write()
        clear_display()
        t += 0.2
        time.sleep_ms(100)


def display_tamo():
    # Define simple 8x8 characters (1 is lit, 0 is off)
    letters = {
        "T": [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
        ],
        "A": [
            [0, 0, 1, 1, 1, 1, 0, 0],
            [0, 1, 1, 0, 0, 1, 1, 0],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1],
        ],
        "M": [
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 1, 0, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 1, 1, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1],
        ],
        "O": [
            [0, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 0],
        ],
        "heart": [
            [0, 1, 1, 0, 0, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ],
    }

    while True:
        # Display each letter for 1 second
        for letter in ["T", "A", "M", "O", "heart"]:
            # Clear display
            for i in range(NEO_PIXEL_COUNT):
                np[LOOKUP[i]] = (0, 0, 0)

            # Draw the letter
            for y in range(8):
                for x in range(8):
                    if letters[letter][y][x]:
                        color = (255, 0, 0) if letter == "heart" else (0, 255, 255)
                        np[LOOKUP[y * 8 + x]] = color
            np.write()
            time.sleep_ms(1000)


# Helper function
def clear_display():
    for i in range(NEO_PIXEL_COUNT):
        np[LOOKUP[i]] = (0, 0, 0)


all_displays = {
    "random_color": display_random_color,
    "snake": display_snake,
    "spiral": display_spiral,
    "firework": display_firework,
    "rain": display_rain,
    "bounce": display_bounce,
    "wave": display_wave,
    "matrix": display_matrix,
    "sparkle": display_sparkle,
    "checkerboard": display_checkerboard,
    "radar": display_radar,
    "tetris": display_tetris,
    "dna": display_dna,
    "tamo": display_tamo,
}
