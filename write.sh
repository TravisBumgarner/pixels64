source ./venv/bin/activate
ampy --port /dev/tty.usbserial-0001 rm main.py 2>/dev/null || true
ampy --port /dev/tty.usbserial-0001 put main.py
