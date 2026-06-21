# bluetooth-experimental

Bluetooth Low Energy (BLE) control for the Pixels64 8×8 NeoPixel display.

An ESP32 running MicroPython advertises a BLE service; a browser-based Web
Bluetooth UI connects to one or more boards and drives the LEDs in real time —
individual pixels, fills, brightness, and animated presets.

This replaces the earlier `wifi-experimental` sandbox (WiFi web server). BLE
avoids needing to put credentials on the device or share a network, and lets the
page talk to several displays at once.

## Layout

```
bluetooth-experimental/
├── src/
│   ├── boot.py       # runs on power-up; disables WiFi to free memory/radio
│   ├── config.py     # LED index lookup tables for the panel wiring
│   ├── presets.py    # animation classes (rainbow, chase, plasma, ...)
│   └── main.py        # BLE GATT server + render loop
├── web/
│   └── index.html    # Web Bluetooth control UI (single file, no build step)
├── test_pixel.py     # minimal sanity check — lights one pixel green
├── upload.sh         # flash src/*.py to the board via mpremote
└── serve.sh          # serve web/ over http for the browser UI
```

## Requirements

- An ESP32 flashed with MicroPython (with the `bluetooth` module).
- A WS2812/NeoPixel 8×8 panel on GPIO **13**.
- `mpremote` for uploading (`pip install mpremote`).
- A browser that supports **Web Bluetooth** — Chrome or Edge on
  desktop/Android. Safari and iOS are **not** supported.

## Setup

```bash
cd bluetooth-experimental
python3 -m venv venv
source venv/bin/activate
pip install mpremote
```

## Upload firmware to the board

Connect the ESP32 over USB and adjust `PORT` in `upload.sh` if your device
isn't `/dev/tty.usbserial-0001`, then:

```bash
./upload.sh
```

This copies `boot.py`, `config.py`, `presets.py`, and `main.py` to the board and
resets it. On boot it advertises as **`Pixels64`** for a 10-second window
(`BLE_CONNECT_WINDOW_MS`) and lights pixel 0 as a status indicator:

| Indicator | Meaning |
|-----------|---------|
| Green     | Advertising, waiting for a connection |
| Blue      | A client is connected |
| Red       | BLE turned off (connection window expired or client disconnected) |

If no one connects within the window, BLE shuts off to save power. Power-cycle or
reset the board to advertise again. The last running preset is saved to
`active.json` and restored on the next boot.

## Run the control UI

```bash
./serve.sh   # serves web/ at http://localhost:8000
```

Open <http://localhost:8000> in Chrome or Edge, click **+ Add device**, and pick
your `Pixels64` board from the BLE chooser. You can add multiple boards. The UI
provides a paintable 8×8 grid, color picker, fill/clear, brightness and FPS
sliders, and the preset list.

## BLE protocol

A single writable characteristic accepts short binary command packets. Service
and characteristic UUIDs are defined in `main.py`; the first byte is the opcode:

| Opcode | Name         | Payload                          |
|--------|--------------|----------------------------------|
| `0x01` | SET_PIXEL    | `idx, r, g, b`                   |
| `0x02` | FILL         | `r, g, b`                        |
| `0x03` | CLEAR        | —                                |
| `0x05` | PRESET       | `index` (into `PRESET_ORDER`)    |
| `0x06` | BRIGHTNESS   | `0–255`                          |
| `0x07` | BATCH        | `count`, then `count`×`idx,r,g,b`|
| `0x08` | STOP         | — (stop the running animation)   |
| `0x09` | FPS          | `1–30`                           |

Pixel indices are logical positions (0–63, row-major); `config.py`'s `LOOKUP`
table maps them to the panel's physical wiring order.
