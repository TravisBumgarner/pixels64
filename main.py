import machine
import neopixel


# Define the GPIO pin connected to the WS2812B data line
LED_PIN = 13  # Use GPIO 18, or change to your chosen pin
LED_COUNT = 5  # Number of LEDs in the strip

# Create a neopixel object
pin = machine.Pin(LED_PIN, machine.Pin.OUT)
strip = neopixel.NeoPixel(pin, LED_COUNT)

strip[0] = (0, 255, 0)
strip.write()