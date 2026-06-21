import bluetooth
import time
import gc
import json
import machine
import neopixel
from config import LOOKUP
import presets

PIN = 13
COUNT = 64
DEVICE_NAME = "Pixels64"
ACTIVE_FILE = "active.json"
BLE_CONNECT_WINDOW_MS = 10_000

np = neopixel.NeoPixel(machine.Pin(PIN, machine.Pin.OUT), COUNT)

state = {
    "fn": None,
    "name": "off",
    "frame": 0,
    "last_tick": 0,
    "tick_ms": 120,
    "brightness": 1.0,
}


def write_np():
    b = state["brightness"]
    if b >= 0.999:
        np.write()
        return
    buf = np.buf
    saved = bytes(buf)
    for i in range(len(buf)):
        s = int(buf[i] * b)
        buf[i] = 255 if s > 255 else s
    np.write()
    for i in range(len(buf)):
        buf[i] = saved[i]

ble_state = {
    "on": False,
    "connected": False,
    "started_at": 0,
    "shutdown_requested": False,
}

INDICATOR_IDX = 0
GREEN = (0, 30, 0)
BLUE = (0, 0, 30)
RED = (30, 0, 0)
RED_HOLD_MS = 2000

indicator = {
    "color": None,
    "red_until": 0,
    "dirty": False,
}

PRESET_ORDER = [
    "off",
    "rainbow", "chase", "pulse", "sparkle", "plasma",
    "christmas", "gradient_squares", "random_pulses", "pulses_toward",
    "zigzag", "dual_chase", "hilbert", "morton", "spiral",
    "jpeg_zigzag", "diagonal_wave", "voronoi",
]


def clear():
    for i in range(COUNT):
        np[i] = (0, 0, 0)
    write_np()


def fill(r, g, b):
    for i in range(COUNT):
        np[i] = (r, g, b)
    write_np()


def save_active():
    try:
        with open(ACTIVE_FILE, "w") as f:
            json.dump({"name": state["name"]}, f)
    except Exception as e:
        print("save_active err:", e)


def load_active():
    try:
        with open(ACTIVE_FILE, "r") as f:
            return json.load(f)
    except:
        return None


def stop_animation(persist=True):
    state["fn"] = None
    state["name"] = "off"
    if persist:
        save_active()


def start_preset_by_name(name, persist=True):
    if name == "off":
        stop_animation(persist=persist)
        clear()
        return
    cls = presets.PRESETS.get(name)
    if cls is None:
        return
    try:
        inst = cls()
    except Exception as e:
        print("preset init err:", e)
        return
    clear()
    state["fn"] = inst.step
    state["name"] = name
    state["frame"] = 0
    if persist:
        save_active()


def start_preset_by_index(idx):
    if idx == 0 or idx >= len(PRESET_ORDER):
        stop_animation()
        clear()
        return
    start_preset_by_name(PRESET_ORDER[idx])


OP_SET_PIXEL  = 0x01
OP_FILL       = 0x02
OP_CLEAR      = 0x03
OP_PRESET     = 0x05
OP_BRIGHTNESS = 0x06
OP_BATCH      = 0x07
OP_STOP       = 0x08
OP_FPS        = 0x09


def handle_command(buf):
    if not buf:
        return
    op = buf[0]
    if op == OP_SET_PIXEL and len(buf) >= 5:
        stop_animation()
        idx = buf[1]
        if 0 <= idx < COUNT:
            np[LOOKUP[idx]] = (buf[2], buf[3], buf[4])
            write_np()
    elif op == OP_FILL and len(buf) >= 4:
        stop_animation()
        fill(buf[1], buf[2], buf[3])
    elif op == OP_CLEAR:
        stop_animation()
        clear()
    elif op == OP_PRESET and len(buf) >= 2:
        start_preset_by_index(buf[1])
    elif op == OP_BRIGHTNESS and len(buf) >= 2:
        state["brightness"] = buf[1] / 255
        write_np()
    elif op == OP_BATCH and len(buf) >= 2:
        stop_animation()
        count = buf[1]
        off = 2
        for _ in range(count):
            if off + 4 > len(buf):
                break
            idx = buf[off]
            if 0 <= idx < COUNT:
                np[LOOKUP[idx]] = (buf[off + 1], buf[off + 2], buf[off + 3])
            off += 4
        write_np()
    elif op == OP_STOP:
        stop_animation()
    elif op == OP_FPS and len(buf) >= 2:
        fps = buf[1]
        if fps < 1: fps = 1
        if fps > 30: fps = 30
        state["tick_ms"] = 1000 // fps


_SVC_UUID = bluetooth.UUID("f64a0001-7e1e-4f0a-9b2d-1c3a5a8d2e10")
_CMD_UUID = bluetooth.UUID("f64a0002-7e1e-4f0a-9b2d-1c3a5a8d2e10")

_FLAG_WRITE = 0x0008
_FLAG_WRITE_NO_RESPONSE = 0x0004

ble = bluetooth.BLE()
_CMD_CHAR = (_CMD_UUID, _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,)
_SVC = (_SVC_UUID, (_CMD_CHAR,))
cmd_handle = None


def _adv_payload(name, services):
    p = bytearray()
    p += bytes([2, 0x01, 0x06])
    if name:
        n = name.encode()
        p += bytes([len(n) + 1, 0x09]) + n
    for u in services:
        b = bytes(u)
        if len(b) == 16:
            p += bytes([len(b) + 1, 0x07]) + b
    return p


ADV = _adv_payload(DEVICE_NAME, [_SVC_UUID])

_IRQ_CENTRAL_CONNECT = 1
_IRQ_CENTRAL_DISCONNECT = 2
_IRQ_GATTS_WRITE = 3


def _irq(event, data):
    if event == _IRQ_CENTRAL_CONNECT:
        print("CONNECT")
        ble_state["connected"] = True
        set_indicator(BLUE)
    elif event == _IRQ_CENTRAL_DISCONNECT:
        print("DISCONNECT")
        ble_state["connected"] = False
        ble_state["shutdown_requested"] = True
    elif event == _IRQ_GATTS_WRITE:
        _, attr_handle = data
        if attr_handle == cmd_handle:
            try:
                handle_command(ble.gatts_read(cmd_handle))
            except Exception as e:
                print("cmd err:", e)


def set_indicator(color, red_until=0):
    indicator["color"] = color
    indicator["red_until"] = red_until
    indicator["dirty"] = True


def draw_indicator():
    np[LOOKUP[INDICATOR_IDX]] = indicator["color"] if indicator["color"] else (0, 0, 0)
    write_np()
    indicator["dirty"] = False


def ble_on():
    global cmd_handle
    ble.active(True)
    try:
        ble.config(gap_name=DEVICE_NAME)
    except:
        pass
    ((cmd_handle,),) = ble.gatts_register_services((_SVC,))
    ble.gatts_set_buffer(cmd_handle, 250)
    ble.irq(_irq)
    ble.gap_advertise(100_000, ADV)
    ble_state["on"] = True
    ble_state["started_at"] = time.ticks_ms()
    set_indicator(GREEN)
    print("BLE_ADVERTISING name=" + DEVICE_NAME)


def ble_off():
    try:
        ble.gap_advertise(None)
    except:
        pass
    try:
        ble.active(False)
    except:
        pass
    ble_state["on"] = False
    set_indicator(RED, red_until=time.ticks_add(time.ticks_ms(), RED_HOLD_MS))
    print("BLE_OFF")


ble_on()
clear()

saved = load_active()
if saved and saved.get("name") and saved["name"] != "off":
    try:
        start_preset_by_name(saved["name"], persist=False)
    except Exception as e:
        print("restore err:", e)

while True:
    now = time.ticks_ms()

    if ble_state["shutdown_requested"]:
        ble_state["shutdown_requested"] = False
        ble_off()
    elif ble_state["on"] and not ble_state["connected"]:
        if time.ticks_diff(now, ble_state["started_at"]) >= BLE_CONNECT_WINDOW_MS:
            ble_off()

    if indicator["color"] == RED and indicator["red_until"] and time.ticks_diff(now, indicator["red_until"]) >= 0:
        set_indicator(None)

    if state["fn"]:
        if time.ticks_diff(now, state["last_tick"]) >= state["tick_ms"]:
            try:
                state["fn"](state["frame"], np, LOOKUP)
                if indicator["color"]:
                    np[LOOKUP[INDICATOR_IDX]] = indicator["color"]
                write_np()
                indicator["dirty"] = False
                state["frame"] += 1
                state["last_tick"] = now
            except Exception as e:
                state["fn"] = None
                state["name"] = "off"
                print("animate err:", e)
            gc.collect()
    elif indicator["dirty"]:
        draw_indicator()

    time.sleep_ms(10)
