import machine
import time
import neopixel
from config import LOOKUP

NEO_PIXEL_PIN = 13
NEO_PIXEL_COUNT = 64

neo_pin = machine.Pin(NEO_PIXEL_PIN, machine.Pin.OUT)
np = neopixel.NeoPixel(neo_pin, NEO_PIXEL_COUNT)


def set_pixel(i, r, g, b):
    np[LOOKUP[i]] = (r, g, b)
    np.write()


def main():
    while True:
        for i in range(64):
            set_pixel(i, 255, 0, 0)
            time.sleep_ms(2000)
            set_pixel(i, 0, 0, 0)


if __name__ == "__main__":
    main()
