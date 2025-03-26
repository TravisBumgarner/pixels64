from config import LOOKUP
import time
import machine
import neopixel

NEO_PIXEL_PIN = 13
NEO_PIXEL_COUNT = 64

neo_pin = machine.Pin(NEO_PIXEL_PIN, machine.Pin.OUT)
np = neopixel.NeoPixel(neo_pin, NEO_PIXEL_COUNT)


def display_initial_test():
    for i in LOOKUP:
        np[i] = (255, 0, 0)
        np.write()
        time.sleep_ms(2000)
        np[i] = (0, 0, 0)
        np.write()


def display_all_yellow():
    for i in LOOKUP:
        np[i] = (255, 255, 0)
    np.write()


def display_all_green():
    for i in LOOKUP:
        np[i] = (0, 255, 0)
    np.write()


def display_all_blue():
    for i in LOOKUP:
        np[i] = (0, 0, 255)
    np.write()


all_displays = {
    "initial_test": display_initial_test,
    "all_yellow": display_all_yellow,
    "all_green": display_all_green,
    "all_blue": display_all_blue,
}
