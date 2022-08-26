""" post_motor_max_speed_test.py

Runs the test to collect zero-load speed data for the LEGO EV3 large motor.

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

# Assiging test parameters
u = [40, 60, 80, 100]  # Motor output levels (%)
tstop = 3  # Test duration (s)
w = []  # Measured angular speed array (rad/s)

# Creating LEGO EV3 objects
ev3 = LegoEV3()
motor = Motor(ev3, port='A')

# Initializing motor
motor.outputmode = 'power'
motor.output = 0
motor.reset_angle()
motor.start()

# Running three sets of data
for _ in range(3):
    # Pre-allocating angular speed array for i-th data set
    wi = []
    for ui in u:
        # Pre-allocating output arrays
        t = []
        theta = []
        # Initializing current time stamp and starting clock
        tcurr = 0
        tstart = time.perf_counter()
        # Running motor for test duration
        while tcurr <= tstop:
            # Assigning output level
            motor.output = ui
            # Updating output arrays
            t.append(tcurr)
            theta.append(motor.angle)
            # Getting current time (s)
            tcurr = time.perf_counter() - tstart
        # Calculating motor angular velocity (rad/s)
        # (0.5 s after start and 0.5 s before stop)
        t = np.array(t)
        theta = np.array(theta)
        istart = np.nonzero(t>0.5)[0][0]
        iend = np.nonzero(t<t[-1]-0.5)[0][-1]
        wi.append(np.median(np.pi/180*np.gradient(theta[istart:iend], t[istart:iend])))
    w.append(wi)

# Stopping motor and closing brick connection
motor.stop()
ev3.close()

# Displaying results to be used in:
# post_motor_max_speed_plot.py
print('Motor input (%) and average speeds (rad/s):')
print(u)
print(np.mean(w, axis=0))
