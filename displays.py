import machine
import neopixel

LED_PIN = 13
LED_COUNT = 64
led_pin = machine.Pin(LED_PIN, machine.Pin.OUT)
strip = neopixel.NeoPixel(led_pin, LED_COUNT)


# Todo - replace this with custom mapping once LED order is known.
LED_MAPPING = {i: i for i in range(LED_COUNT)}


def display_all_yellow():
    for i in range(LED_COUNT):
        strip[LED_MAPPING[i]] = (255, 255, 0)
    strip.write()


def display_all_green():
    for i in range(LED_COUNT):
        strip[LED_MAPPING[i]] = (0, 255, 0)
    strip.write()


def display_all_blue():
    for i in range(LED_COUNT):
        strip[LED_MAPPING[i]] = (0, 0, 255)
    strip.write()


display_array = [
    display_all_yellow,
    display_all_green,
    display_all_blue,
]
