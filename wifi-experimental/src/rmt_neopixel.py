import esp32
from machine import Pin

# clock_div=2 -> 80MHz / 2 = 40MHz -> 25ns per tick
# WS2812B timing
T0H, T0L = 14, 32
T1H, T1L = 28, 24

_BYTE_PULSES = []
for _b in range(256):
    _p = []
    for _bit in range(7, -1, -1):
        if _b & (1 << _bit):
            _p.append(T1H); _p.append(T1L)
        else:
            _p.append(T0H); _p.append(T0L)
    _BYTE_PULSES.append(tuple(_p))
_BYTE_PULSES = tuple(_BYTE_PULSES)


class NeoPixel:
    def __init__(self, pin, n, bpp=3, channel=0):
        self.n = n
        self.bpp = bpp
        self.buf = bytearray(n * bpp)
        self.brightness = 1.0
        self._pulses = [0] * (n * bpp * 16)
        if not isinstance(pin, Pin):
            pin = Pin(pin, Pin.OUT)
        self.rmt = esp32.RMT(channel, pin=pin, clock_div=2)

    def __setitem__(self, i, v):
        off = i * self.bpp
        self.buf[off]     = v[1] & 0xff  # G
        self.buf[off + 1] = v[0] & 0xff  # R
        self.buf[off + 2] = v[2] & 0xff  # B

    def __getitem__(self, i):
        off = i * self.bpp
        return (self.buf[off + 1], self.buf[off], self.buf[off + 2])

    def __len__(self):
        return self.n

    def fill(self, v):
        for i in range(self.n):
            self[i] = v

    def write(self):
        out = self._pulses
        table = _BYTE_PULSES
        b = self.brightness
        idx = 0
        if b >= 0.999:
            for byte in self.buf:
                out[idx:idx + 16] = table[byte]
                idx += 16
        else:
            for byte in self.buf:
                scaled = int(byte * b)
                if scaled > 255: scaled = 255
                out[idx:idx + 16] = table[scaled]
                idx += 16
        self.rmt.write_pulses(out, 1)
