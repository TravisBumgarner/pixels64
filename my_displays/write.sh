source ./venv/bin/activate
for file in src/*.py; do
    filename=$(basename $file)
    echo "Uploading $filename"
    ampy --port /dev/tty.usbserial-0001 rm $filename 2>/dev/null || true
    ampy --port /dev/tty.usbserial-0001 put $file
done


