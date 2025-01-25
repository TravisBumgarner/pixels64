# Resource

- https://micropython.org/download/ESP32_GENERIC

# Commands

- Get a list of connected devices 
    - `ls /dev/cu.* /dev/tty.*`
    - The desired device should look something like `tty.usbserial-0001`
- Get a terminal to esp32 
    - `screen /dev/tty.usbserial-0001 115200` 
    - Press `Control + C` to get access to the terminal (Might need to press a few times)
    - Press `Control + A` then `Control + D` to exit.
- Send file to esp32 
    - `ampy --port /dev/tty.usbserial-0001 put boot.py`
    - If `put` fails, reconnect device.
    - Push button with "en" to launch code. 
- Remove a file
    - `ampy --port /dev/tty.usbserial-0001 rm boot.py`
- List files
    - `ampy --port /dev/tty.usbserial-0001 ls`

