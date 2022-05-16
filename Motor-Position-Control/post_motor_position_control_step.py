""" post_motor_position_control_step.py

Contains the example code to run a DC motor that has an integrated shaft
encoder as a closed-loop position system with a PID controller.
A step input is applied and can be used to tune the PID gains.
https://thingsdaq.org/2022/05/15/motor-position-control-with-raspberry-pi/

Run this in a terminal instead of an interactive window.

Author: Eduardo Nigro
    rev 0.0.1
    2022-05-15

"""
# Importing modules and classes
import time
import numpy as np
from utils import plot_line
from gpiozero_extended import Motor, PID

# Setting general parameters
tstop = 2  # Execution duration (s)
tsample = 0.01  # Sampling period (s)
thetasp = 60  # Motor position set point (deg)
tau = 0.1  # Speed low-pass filter response time (s)

# Creating PID controller object
kp = 0.036
ki = 0.379
kd = 0.0009
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
    # Getting motor shaft angular position: I/O (data in)
    thetacurr = mymotor.get_angle()
    # Calculating closed-loop output
    ucurr = pid.control(thetasp, thetacurr)
    # Assigning motor output: I/O (data out)
    mymotor.set_output(ucurr)
    # Updating output arrays
    t.append(tcurr)
    theta.append(thetacurr)
    u.append(ucurr)
    # Updating previous values
    thetaprev = thetacurr
    tprev = tcurr

print('Done.')
# Stopping motor and releasing GPIO pins
mymotor.set_output(0, brake=True)
del mymotor

# Plotting results
plot_line(
    [t]*2, [theta, u], marker=True, axes='multi',
    yname=['Shaft Position (deg.)', 'Control Output (-)'])
plot_line(t[1::], 1000*np.diff(t), marker=True, yname='Sampling Period (ms)')
