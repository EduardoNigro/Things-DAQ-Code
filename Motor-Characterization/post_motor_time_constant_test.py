""" post_motor_time_constant_test.py

Runs the test to determine the time constant for the LEGO EV3 large motor.

Read more at:
http://thingsdaq.org/2022/08/26/dc-motor-characterization-2-of-2/

Author: Eduardo Nigro
    rev 0.0.1
    2022-08-26

"""
# Importing modules and classes
import time
import numpy as np
from pyev3.brick import LegoEV3
from pyev3.devices import Motor
from utils import plot_line
from scipy import signal

# Creating low-pass Butterworth filter
fs0 = 100  # Approximate sampling frequency (Hz)
fc = 10  # Cutoff frequency (Hz)
b0, a0 = signal.butter(1, fc, fs=fs0)

# Assiging test parameters
u = [40, 60, 80, 100]  # Motor output levels (%)
thetastop = 900  # Test stop angular position (deg.)
thetamargin = 180  # Angular margin for braking (deg.)
tau = []  # Time constant array (s)

# Creating LEGO EV3 objects
ev3 = LegoEV3()
motor = Motor(ev3, port='A')

# Initializing motor
motor.outputmode = 'power'
motor.output = 0

# Running five sets of data
for _ in range(5):
    # Pre-allocating time constant array for i-th data set
    taui = []
    for ui in u:
        # Resetting angular position and starting motor
        motor.reset_angle()
        motor.start()
        # Pre-allocating output arrays
        t = []
        theta = []
        # Initializing current time stamp and starting clock
        tcurr = 0
        thetacurr = 0
        tstart = time.perf_counter()
        # Running motor until stop angle is reached
        while thetacurr <= thetastop:
            # Assigning output level
            motor.output = ui
            # Updating output arrays
            t.append(tcurr)
            theta.append(thetacurr)
            # Storing previous angular position
            thetaprev = thetacurr
            # Getting current values
            tcurr = time.perf_counter() - tstart
            thetacurr = motor.angle
        # Setting output to ZERO
        motor.output = 0
        # Letting motor spin for angular margin
        # if needed before applyin the brakes
        if thetacurr > thetastop:
            flagstop = False
            while not flagstop:
                thetaprev = thetacurr
                thetacurr = motor.angle
                if (thetaprev == thetacurr) | (thetacurr > thetastop+thetamargin):
                    flagstop = True
        # Stopping motor
        print(thetacurr)
        motor.stop(brake='on')
        # Returning motor to original position
        motor.output = -20
        motor.start()
        while motor.angle > 0:
            pass
        motor.output = 0
        motor.stop(brake='on')
        time.sleep(1)
        # Calculating motor angular velocity (rad/s)
        t = np.array(t)
        w = np.pi/180*np.gradient(theta, t)
        # Doing zero-phase digital filtering
        wf = signal.filtfilt(b0, a0, w, method='gust')
        # Finding index of last 0.5 seconds of
        # data and extracting median speed value
        istart = np.nonzero(t>t[-1]-0.5)[0][0]
        iend = len(t)
        wmax = np.median(wf[istart:iend])
        # Determnining time constant (s)
        i63 = np.nonzero(wf>=0.6321*wmax)[0][0]
        taui.append(t[i63])
    tau.append(taui)

# Stopping motor and closing brick connection
motor.stop(brake='off')
ev3.close()

# Displaying results
print('Motor input (%) and average response times (s):')
print(u)
print(np.mean(tau, axis=0))

# Plotting results for last output level of last data set
plot_line(
    [t]*2, [w, wf],
    yname='Motor Speed (rad/s)', legend=['Raw', 'Filtered']
)
