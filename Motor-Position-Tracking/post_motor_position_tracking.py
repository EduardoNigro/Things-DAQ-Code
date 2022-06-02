""" post_motor_position_tracking.py

Contains the example code to run a DC motor that has an integrated shaft
encoder as a closed-loop position tracking system with a PID controller.
Three path calculation methods are available in the module path.py
https://thingsdaq.org/2022/06/02/dc-motor-position-tracking/

Run this in a terminal instead of an interactive window.

Author: Eduardo Nigro
    rev 0.0.1
    2022-06-102

"""
# Importing modules and classes
import time
import numpy as np
from scipy.interpolate import interp1d
from path import path_quad
from utils import plot_line
from gpiozero_extended import Motor, PID

# Setting path parameters
thetastart = 0  # Start shaft angle (rad)
thetaend = 3*np.pi  # End shaft angle (rad)
wmax = 4*np.pi  # Max angular speed (rad/s)
ta = 0.45  # Acceleration time (s)
tsample = 0.01  # Sampling period (s)

# Calculating path
t, x, _, _ = path_quad(thetastart, thetaend, wmax, ta)
f = interp1d(t, 180/np.pi*x)  # Interpolation function
tstop = t[-1]  # Execution duration (s)

# Creating PID controller object
kp = 0.036
ki = 0.260
kd = 0.0011
taupid = 0.01
pid = PID(tsample, kp, ki, kd, tau=taupid)

# Creating motor object using GPIO pins 16, 17, and 18
# (using SN754410 quadruple half-H driver chip)
# Integrated encoder on GPIO pins 24 and 25.
mymotor = Motor(
    enable1=16, pwm1=17, pwm2=18,
    encoder1=24, encoder2=25, encoderppr=300.8)
mymotor.reset_angle()

# Pre-allocating output arrays
t = []  # Time (s)
theta = []  # Measured shaft position (deg)
thetasp = []  # Set point shft position (deg)
u = []  # Controler output

# Initializing variables and starting clock
thetaprev = 0
tprev = 0
tcurr = 0
tstart = time.perf_counter()

# Running execution loop
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    # Pausing for `tsample` to give CPU time to process encoder signal
    time.sleep(tsample)
    # Getting current time (s)
    tcurr = time.perf_counter() - tstart
    # Getting motor shaft angular position
    thetacurr = mymotor.get_angle()
    # Interpolating set point angle at current time step
    if tcurr <= tstop:
        thetaspcurr = f(tcurr)
    # Calculating closed-loop output
    ucurr = pid.control(thetaspcurr, thetacurr)
    # Assigning motor output
    mymotor.set_output(ucurr)
    # Updating output arrays
    t.append(tcurr)
    thetasp.append(thetaspcurr)
    theta.append(thetacurr)
    u.append(ucurr)
    # Updating previous values
    thetaprev = thetacurr
    tprev = tcurr

print('Done.')
# Stopping motor and releasing GPIO pins
mymotor.set_output(0, brake=True)
del mymotor

# Calculating motor angular velocity (rad/s)
wsp = np.pi/180 * np.gradient(thetasp, t)
w = np.pi/180 * np.gradient(theta, t)

# Calculating error
e = np.array(thetasp) - np.array(theta)

# Plotting results
plot_line(
    [t]*2, [thetasp, theta], yname=['Shaft Position (deg.)'],
    legend=['Set Point', 'Actual'])
plot_line(
    [t]*2, [wsp, w], yname=['Shaft Speed (rad/s)'],
    legend=['Set Point', 'Actual'])
plot_line(
    [t[1::], t, t], [1000*np.diff(t), u, e], marker=True, axes='multi',
    yname=['Sampling Period (ms)', 'Control Output (-)', 'Position Error (deg.)'])
