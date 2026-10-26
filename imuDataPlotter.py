import numpy as np
import serial

acc_scale = 0.488 * 9.80665 /1e3
gyro_scale = 140 * np.pi / 180 /1e3

ser = serial.Serial()
ser.port = "/dev/ttyACM0"
ser.baudrate = 921600
ser.timeout = 1

ser.dtr = False
ser.rts = False

dtype = np.dtype([
    ("sequence",    "<u4"),
    ("timestamp_us","<u8"),

    ("ax",          "<i2"),
    ("ay",          "<i2"),
    ("az",          "<i2"),

    ("gx",          "<i2"),
    ("gy",          "<i2"),
    ("gz",          "<i2"),
])


HEADER = b'\xAA\x55'

while True:

    # Find packet beginning
    while True:
        byte = ser.read(1)

        if byte == b'\xAA':
            if ser.read(1) == b'\x55':
                break

    # Read packet
    data = ser.read(24)

    packet = np.frombuffer(data, dtype=dtype)[0]

    print(packet["sequence"], packet["timestamp_us"])

    print(packet["ax"]*acc_scale, packet["ay"]*acc_scale, packet["az"]*acc_scale)
    print(packet["gx"]*gyro_scale, packet["gy"]*gyro_scale, packet["gz"]*gyro_scale)

ser.close()