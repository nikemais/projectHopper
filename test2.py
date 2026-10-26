import serial
import time

ser = serial.Serial(
    "/dev/ttyACM0",
    921600,
    timeout=1
)

print("opened")

while True:
    data = ser.read(4096)

    if data:
        print("received", len(data), "bytes")
    else:
        print("TIMEOUT")