import network
import time
from wifi_config import SSID, PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    print("Connecting to", SSID)
    wlan.connect(SSID, PASSWORD)
    for _ in range(40):
        if wlan.isconnected():
            break
        time.sleep(0.5)

if wlan.isconnected():
    ip = wlan.ifconfig()[0]
    print("WIFI_OK ip=" + ip)
else:
    print("WIFI_FAIL status=" + str(wlan.status()))
