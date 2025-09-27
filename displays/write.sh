source ./venv/bin/activate
for file in src/*.py; do
    filename=$(basename $file)
    echo "Uploading $filename"
    ampy --port /dev/tty.usbserial-0001 rm $filename 2>/dev/null || true
    ampy --port /dev/tty.usbserial-0001 put $file
    ampy --port /dev/tty.usbserial-0001 reset
done

echo "Resetting device to run new code..."
esptool.py --port /dev/tty.usbserial-0001 run

