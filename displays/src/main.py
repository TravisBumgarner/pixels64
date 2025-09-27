from display_gradient_squares import display_gradient_squares
from display_random_pulses import display_random_pulses


LAST_DISPLAY_FILE = "last_display.txt"

displays_to_run = {
    "random_pulses": display_random_pulses,
    "display_gradient_squares": display_gradient_squares,
}


def save_last_display(name):
    with open(LAST_DISPLAY_FILE, "w") as f:
        f.write(name)


def get_last_display():
    try:
        with open(LAST_DISPLAY_FILE, "r") as f:
            return f.read().strip()
    except:
        return None


def get_next_display(current):
    displays = list(displays_to_run.keys())
    if not current or current not in displays:
        return displays[0]
    current_idx = displays.index(current)
    next_idx = (current_idx + 1) % len(displays)
    return displays[next_idx]


def main():
    # Power cycle device to get next display
    last_display = get_last_display()
    display_name = get_next_display(last_display)

    print(f"Displaying {display_name}")
    save_last_display(display_name)

    displays_to_run[display_name]()


if __name__ == "__main__":
    main()
