#!/bin/bash
set -e

cd "$(dirname "$0")"
source venv/bin/activate

PORT=/dev/tty.usbserial-0001

echo "Uploading boot.py, config.py, presets.py, main.py..."
mpremote connect $PORT fs rm :rmt_neopixel.py 2>/dev/null || true
mpremote connect $PORT \
    fs cp src/boot.py :boot.py + \
    fs cp src/config.py :config.py + \
    fs cp src/presets.py :presets.py + \
    fs cp src/main.py :main.py + \
    reset

echo "Done."
