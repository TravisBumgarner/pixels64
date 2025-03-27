# Pixels64

An 8x8 grid of 64 individually addressable RGB LEDs using the WS2812B package. Pixels64 is controlled by the esp32 running CircuitPython and the `neopixel` library. A 3D-printable housing is included.

(Need help? [Join the community](https://discord.com/invite/J8jwMxEEff)!)

![Logo](logo.png)

This repository includes all the files needed to build the Pixel64 display. 
- `cad` - 3D models for housing
- `circuit` - PCB diagram and schematic
- `code` - Code for showing various displays

The PCB is designed to be modular, allowing multiple boards to be combined in an N x M configuration for any display size.

## Setup

### Tools

- Wire cutters
- Soldering Iron

### Components 

- esp32
- Three different colors of wire (Red, Black, Blue)
- White Filament
- Black Filament
- 4x pixel64 Boards
- 16x M3x6x4.2 Brass Knurled Nuts
- 16x M3x5 Metal Screws

### Quick Setup

1. Print `base-plate.stl` and `walls.stl` in black. Print `case.stl` in white.
1. Upload files in `jlcpcb` and order from JLCPCB
1. Cut wire to length
    - 3x 25mm Red
    - 3x 25mm Blue
    - 3x 25mm Black
    - 1x 12mm Red
    - 1x 12mm Blue
    - 1x 12mm Black
1. Solder boards together. 
    - Blue (data) goes to the center pad. Red (power) to the square pad. Black (power) to the circle pad. 
    - Solder the short wires to the `DataIn1` of the first PCB. 
    - Solder the long wires from `Dataout1` to the `DataIn1` of the next PCB.
    - Repeat the previous step two more times.
1. Use a soldering iron to press fit the brass knurled nuts into the risers on the `base-plate.stl`. 
1. Screw in the boards. 
    - Note that all of the boards are oriented with `DataIn1` at the bottom. 
    - The arrangement of boards is
    ```
    3 4
    1 2
    ```
1. Setup virtual environment `python -m venv venv` inside the code directory
1. Use virtual environment `source venv/bin/activate
1. Install dependencies `pip install -r requirements.txt`
1. Run `write.sh` script to upload files to device.
1. Pres the `en` button to shuffle the displays. 


## Additional Notes

### CAD

#### Case

- The `case.stl` services as the "screen" of the pixel64. It can be challenging to get a clean print of such a size. You'll need very good first layer adhesion. An alternative here would be to make a case out of white acrylic instead or cover the walls with a white sheet of paper.


### Code

#### Useful commands

- Get a list of connected devices 
    - `ls /dev/cu.* /dev/tty.*`
    - The desired device should look something like `tty.usbserial-0001`
- Get a terminal to esp32 
    - `mpremote`
    - Note - you can't use the `print` statement while uploading code.
    - Be sure to setup your Python virtual environment before running `mpremote`. 
- Send file to esp32 
    - `ampy --port /dev/tty.usbserial-0001 put boot.py`
    - If `put` fails, reconnect device.
    - Push button with "en" to launch code. 
- Remove a file
    - `ampy --port /dev/tty.usbserial-0001 rm boot.py`
- List files
    - `ampy --port /dev/tty.usbserial-0001 ls`

### Circuit

#### NeoPixel Mapping

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


