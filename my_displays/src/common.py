import random

NEO_PIXEL_PIN = 13
NEO_PIXEL_COUNT = 64
DISPLAY_SIDE_LENGTH = int(NEO_PIXEL_COUNT**0.5)


def hsv_to_rgb(h, s, v):
    """Convert HSV (0–1) to RGB (0–255)."""
    i = int(h * 6)
    f = h * 6 - i
    p = int(255 * v * (1 - s))
    q = int(255 * v * (1 - f * s))
    t = int(255 * v * (1 - (1 - f) * s))
    v = int(255 * v)
    i = i % 6
    if i == 0:
        return (v, t, p)
    if i == 1:
        return (q, v, p)
    if i == 2:
        return (p, v, t)
    if i == 3:
        return (p, q, v)
    if i == 4:
        return (t, p, v)
    if i == 5:
        return (v, p, q)


def get_random_color():
    return (
        random.randint(64, 255),
        random.randint(64, 255),
        random.randint(64, 255),
    )


def interpolate(c1, c2, fraction):
    return (
        int(c1[0] + (c2[0] - c1[0]) * fraction),
        int(c1[1] + (c2[1] - c1[1]) * fraction),
        int(c1[2] + (c2[2] - c1[2]) * fraction),
    )


def fill(np, color):
    for i in range(NEO_PIXEL_COUNT):
        np[i] = color
    np.write()
