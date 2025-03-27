# Environment Setup

## Code

1. Make a virtual environment
    - `python -m venv venv`
    - `source venv/bin/activate`
1. Install dependencies
    - `pip install -r requirements.txt`


## esp32

1. Find the device
    - `ls /dev/cu.* /dev/tty.*`
    - The desired device should look something like `tty.usbserial-0001`
1. Connect to the device to view output from `print` statements
    - `mpremote`
    - Note - you can't use the `print` statement while uploading code.
    
## NeoPixel Mapping

The LED circuit board I designed supports multiple configurations, meaning the default ordering of NeoPixels may not match the expected layout. For example, setting neopixel[0] = (255, 255, 255) won't necessarily light up the top-left LED.

This script cycles through each pixel one at a time, allowing you to determine the actual order. Once identified, we can remap the ordering. For example, the physical layout might be:

```
 3  2  1  0  
 7  6  5  4
11 10  9  8
15 14 13 12
```
We can then transform it into a more intuitive sequence:

```
 0  1  2  3
 4  5  6  7
 8  9 10 11
12 13 14 15
```
This remapping ensures easier indexing and consistent control over the LEDs.

Take the following code and save it to `main.py`
```
import machine
import time
import neopixel

NEO_PIXEL_PIN = 13
NEO_PIXEL_COUNT = 64

neo_pin = machine.Pin(NEO_PIXEL_PIN, machine.Pin.OUT)
np = neopixel.NeoPixel(neo_pin, NEO_PIXEL_COUNT)


def set_pixel(i, r, g, b):
    np[i] = (r, g, b)
    np.write()


def main():
    while True:
        for i in range(64):
            set_pixel(i, 255, 0, 0)
            time.sleep_ms(2000)
            set_pixel(i, 0, 0, 0)


if __name__ == "__main__":
    main()

```

Upload the code to the esp32
```
ampy --port [replace with your device] put main.py
```

Place a sheet of paper over the LEDs and tape in place.

Press the `en` button on the esp32 to run the code.

You should see the LEDs light up in a red color.

Mark the first LED that lights up as `0` and complete until done.

Now, starting from the top left, write the numbers of the LEDs in a left to right top to bottom order in the config.py file, replacing the variable `LOOKUP`.

## Troubleshooting

- Get a list of connected devices 
    - `ls /dev/cu.* /dev/tty.*`
    - The desired device should look something like `tty.usbserial-0001`
- Get a terminal to esp32 
    - `mpremote`
- Send file to esp32 
    - `ampy --port /dev/tty.usbserial-0001 put boot.py`
    - If `put` fails, reconnect device.
    - Push button with "en" to launch code. 
- Remove a file
    - `ampy --port /dev/tty.usbserial-0001 rm boot.py`
- List files
    - `ampy --port /dev/tty.usbserial-0001 ls`