#!/bin/bash
set -e

cd "$(dirname "$0")"
source venv/bin/activate

set -a
source .env
set +a

cat > src/wifi_config.py <<EOF
SSID = "${WIFI_SSID}"
PASSWORD = "${WIFI_PASSWORD}"
EOF

PORT=/dev/tty.usbserial-0001

echo "Uploading boot.py, wifi_config.py, config.py, main.py..."
mpremote connect $PORT \
    fs cp src/boot.py :boot.py + \
    fs cp src/wifi_config.py :wifi_config.py + \
    fs cp src/config.py :config.py + \
    fs cp src/presets.py :presets.py + \
    fs cp src/rmt_neopixel.py :rmt_neopixel.py + \
    fs cp src/main.py :main.py + \
    reset

echo "Done."
