import machine
import time
from displays import display_array

# Todo - Hookup Button. 
button_pin = machine.Pin(12, machine.Pin.IN)


def main():
    display_index = 0
    while True:
        display_array[display_index]()
        print(f"Displaying {display_array[display_index].__name__}")
        display_index = (display_index + 1) % len(display_array)
        time.sleep(1)


if __name__ == "__main__":
    main()
