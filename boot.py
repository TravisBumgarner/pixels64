import machine
import neopixel
import time

# Define the GPIO pin connected to the WS2812B data line
LED_PIN = 13  # Use GPIO 18, or change to your chosen pin
LED_COUNT = 30  # Number of LEDs in the strip

# Create a neopixel object
pin = machine.Pin(LED_PIN, machine.Pin.OUT)
strip = neopixel.NeoPixel(pin, LED_COUNT)

def color_wipe(color, wait_ms=50):
    """Wipe color across the strip one LED at a time."""
    for i in range(LED_COUNT):
        strip[i] = color
        strip.write()  # Update the strip
        time.sleep_ms(wait_ms)

def rainbow_cycle(wait_ms=20):
    """Cycle through the rainbow colors."""
    for j in range(256):
        for i in range(LED_COUNT):
            color = wheel((i * 256 // LED_COUNT + j) & 255)
            strip[i] = color
        strip.write()
        time.sleep_ms(wait_ms)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

# Main program
while True:
    print("Color wipe: Red")
    color_wipe((255, 0, 0))  # Red
    print("Color wipe: Green")
    color_wipe((0, 255, 0))  # Green
    print("Color wipe: Blue")
    color_wipe((0, 0, 255))  # Blue
    print("Rainbow cycle")
    rainbow_cycle()

