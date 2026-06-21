#!/bin/bash
cd "$(dirname "$0")/web"
echo "Open http://localhost:8000 in Chrome or Edge (Safari does not support Web Bluetooth)."
python3 -m http.server 8000
