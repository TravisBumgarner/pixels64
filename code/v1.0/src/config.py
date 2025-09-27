LOOKUP = [
    63,
    62,
    61,
    60,
    47,
    46,
    45,
    44,
    59,
    58,
    57,
    56,
    43,
    42,
    41,
    40,
    55,
    54,
    53,
    52,
    39,
    38,
    37,
    36,
    51,
    50,
    49,
    48,
    35,
    34,
    33,
    32,
    15,
    14,
    13,
    12,
    31,
    30,
    29,
    28,
    11,
    10,
    9,
    8,
    27,
    26,
    25,
    24,
    7,
    6,
    5,
    4,
    23,
    22,
    21,
    20,
    3,
    2,
    1,
    0,
    19,
    18,
    17,
    16,
]

# 2D mapping for easier coordinate-based access (8x8 grid)
GRID_SIZE = 8
LOOKUP_2D = [
    LOOKUP[row * GRID_SIZE : (row + 1) * GRID_SIZE] for row in range(GRID_SIZE)
]


def get_led_index(row, col):
    """Helper function to get LED index from 2D coordinates (0-7, 0-7)"""
    if 0 <= row < 8 and 0 <= col < 8:
        return LOOKUP_2D[row][col]
    return None
