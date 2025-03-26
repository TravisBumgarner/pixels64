import machine
import time
import neopixel

# Button pin setup (not used for NeoPixels)
button_pin = machine.Pin(12, machine.Pin.IN)

# NeoPixel setup (use an appropriate GPIO pin)
neo_pin = machine.Pin(13, machine.Pin.OUT)
np = neopixel.NeoPixel(neo_pin, 64)

LOOKUP = [
    63, 62, 61, 60, 47, 46, 45, 44,
    59, 58, 57, 56, 43, 42, 41, 40,
    55, 54, 53, 52, 39, 38, 37, 36,
    51, 50, 49, 48, 35, 34, 33, 32,
    15, 14, 13, 12, 31, 30, 29, 28,
    11, 10, 9, 8, 27, 26, 25, 24,
    7, 6, 5, 4, 23, 22, 21, 20,
    3, 2, 1, 0, 19, 18, 17, 16,
]

def set_pixel(i, r, g, b):
    np[LOOKUP[i]] = (r, g, b)
    np.write()  # Ensure updates are applied

def main():
    print("starting!")
    while True:
        for i in range(64):
            set_pixel(i, 255, 0, 0)
            time.sleep_ms(100)
            set_pixel(i, 0, 0, 0)
            time.sleep_ms(100)

if __name__ == "__main__":
    main()
