from displays import all_displays
import random


def main():
    display_name = random.choice(list(all_displays.keys()))
    print(f"Displaying {display_name}")
    all_displays[display_name]()


if __name__ == "__main__":
    main()
