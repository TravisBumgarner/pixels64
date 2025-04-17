import os
import time

from display_random_pulses import all_displays

LAST_DISPLAY_FILE = "last_display.txt"


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
    displays = list(all_displays.keys())
    if not current or current not in displays:
        return displays[0]
    current_idx = displays.index(current)
    next_idx = (current_idx + 1) % len(displays)
    return displays[next_idx]


def main():
    last_display = get_last_display()
    display_name = get_next_display(last_display)

    print(f"Displaying {display_name}")
    save_last_display(display_name)

    # Run the display function once
    all_displays[display_name]()

    # If we want to keep the display running, we can add a loop here
    # This will allow the script to continue after uploading files
    while True:
        time.sleep(60 * 15)  # Sleep for 15 minutes
        # Optionally refresh the display
        all_displays[display_name]()


if __name__ == "__main__":
    main()
