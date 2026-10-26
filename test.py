import serial
import struct
import numpy as np
import time

PORT = "/dev/ttyACM0"
BAUD = 3000000
#acc_scale = 0.488 * 9.80665 /1e3 #16g
#gyro_scale = 140 * np.pi / 180 /1e3 #400dpi
acc_scale = 0.061 * 9.80665 /1e3 #16g
gyro_scale = 8.75 * np.pi / 180 /1e3 #400dpi

PACKET_SIZE = 26
SYNC = b"\xAA\x55"   # little-endian uint16_t 0x55AA

ser = serial.Serial(
    PORT,
    BAUD,
    timeout=1
)
time.sleep(0.05) 
ser.reset_input_buffer() 

f = open("data/static.dat", "w")
buffer = bytearray()
packetCount = 0
while packetCount < 1e4:

    # Read whatever is currently available
    n = ser.in_waiting

    if n:
        buffer.extend(ser.read(n))

    # Search for packet sync
    while len(buffer) >= PACKET_SIZE:

        index = buffer.find(SYNC)

        if index < 0:
            # Keep the final byte in case it is
            # the beginning of the sync word
            buffer = buffer[-1:]
            break

        # Discard garbage before sync
        if index > 0:
            del buffer[:index]

        # Wait until complete packet is available
        if len(buffer) < PACKET_SIZE:
            break

        packet = bytes(buffer[:PACKET_SIZE])
        del buffer[:PACKET_SIZE]

        # ----------------------------------------------------
        # Decode
        # ----------------------------------------------------

        sync, sequence, timestamp, ax, ay, az, gx, gy, gz = struct.unpack(
            "<HIQhhhhhh",
            packet
        )

        # print(
        #     sequence,
        #     timestamp,
        #     ax*acc_scale, ay*acc_scale, az*acc_scale,
        #     gx*gyro_scale, gy*gyro_scale, gz*gyro_scale
        # )
        line = f"{sequence} {timestamp} {ax*acc_scale} {ay*acc_scale} {az*acc_scale} {gx*gyro_scale} {gy*gyro_scale} {gz*gyro_scale}\n"
        f.write(line)
        packetCount += 1
ser.close()
f.close()