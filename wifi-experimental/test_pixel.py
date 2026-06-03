import machine
import neopixel
import time

np = neopixel.NeoPixel(machine.Pin(13, machine.Pin.OUT), 64)

for i in range(64):
    np[i] = (0, 0, 0)
np.write()

np[0] = (0, 50, 0)
np.write()
time.sleep(1)
print("OK")
