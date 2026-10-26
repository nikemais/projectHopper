import numpy as np
import serial
import matplotlib.pyplot as plt
from matplotlib import animation
from genericFunctions import calibrate
import sys

acc_scale = 0.488 * 9.80665 /1e3
gyro_scale = 140 * np.pi / 180 /1e3

ser = serial.Serial(
    "/dev/ttyACM0",
    921600,
    timeout=1,
    dsrdtr=False,
    rtscts=False
)

# CALIBRATION
startIntegration = input("Start calibration? [y/n] ")
if ( startIntegration == "y" ):
    acc0 = calibrate( ser )
else:
    ser.close()
    sys.exit()

print(acc0*acc_scale)



#INTEGRATION
startIntegration = input("Start integration? [y/n] ")


ser.close()

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Begin plotting.
wframe = None




def animate(i):
    global wframe
    # If a line collection is already there, remove it before drawing.
    if wframe:
        wframe.remove()
    # Generate data.
    phi = i / FRAMES * 2 * np.pi
    Z = np.cos(2 * np.pi * X + phi) * (1 - np.hypot(X, Y))
    # Plot the new wireframe.
    wframe = ax.plot_wireframe(X, Y, Z, rstride=2, cstride=2)
    if i == FRAMES - 1:  # Print FPS at the end of the loop.
        global tstart
        fps = FRAMES / (time.time() - tstart)
        print(f'Expected FPS: {FPS}; Average FPS: {fps}')
        tstart = time.time()


ani = animation.FuncAnimation(fig, animate, interval=1000 / FPS, frames=FRAMES)

plt.show()
