import numpy as np
import serial
import sys
import time
import struct


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

PACKET_SIZE = 26

SYNC = b'\xAA\x55'

def quatToInertial( accImu ):
    accGravity = np.array([0.0, 0.0, -1.0])
    accImuUnit = accImu / np.linalg.norm(accImu)
    scProd = np.dot( accImuUnit, accGravity )
    vcProd = np.cross( accImuUnit, accGravity )
    q = 1/(np.sqrt(2*(1+scProd)))*np.array([1+scProd, vcProd[0], vcProd[1], vcProd[2]])
    return q

def rotByQuat( q, u ):
    qt = np.array([q[0], -q[1], -q[2], -q[3]])
    return np.cross( np.cross( q, u ), qt )

def calibrate( ser ):
    print("Calibrating...")
    t0 = time.time()
    t = t0
    buffer = bytearray()
    avgs = np.array([0.0, 0.0, 0.0])
    counter = 0
    while counter<10000:

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

            _, _, _, ax, ay, az, _, _, _ = struct.unpack(
                "<HIQhhhhhh",
                packet
            )
            avgs[0] += ax
            avgs[1] += ay
            avgs[2] += az
            counter +=1
    avgs /= counter
    print(counter)
    print("Calibration finished!")
    return avgs

# def integrateOneStep( x, dx ):
