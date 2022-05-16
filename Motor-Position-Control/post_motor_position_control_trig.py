""" post_motor_position_control_trig.py

Contains the example code to run a DC motor that has an integrated shaft
encoder as a closed-loop position system with a PID controller.
Two trigonometric functions (sine and cosine) can be used to explore the
effects of the initial velocity of the position set point function.
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
tstop = 1  # Execution duration (s)
tsample = 0.01  # Sampling period (s)
thetamax = 180  # Motor position amplitude (deg)

# Setting motion parameters
# (Valid options: 'sin', 'cos')
option = 'cos'
if option == 'sin':
    T = 2*tstop  # Period of sine wave (s)
    theta0 = thetamax  # Reference angle
elif option == 'cos':
    T = tstop  # Period of cosine wave (s)
    theta0 = 0.5*thetamax  # Reference angle

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
    # Calculating current set point angle
    if option == 'sin':
        thetaspcurr = theta0 * np.sin((2*np.pi/T) * tcurr)
    elif option == 'cos':
        thetaspcurr = theta0 * (1-np.cos((2*np.pi/T) * tcurr))
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

# Plotting results
plot_line(
    [t]*2, [thetasp, theta], marker=True, yname=['Shaft Position (deg.)'],
    legend=['Set Point', 'Actual'])
plot_line(
    [t]*2, [wsp, w], marker=True, yname=['Shaft Speed (rad/s)'],
    legend=['Set Point', 'Actual'])
plot_line(
    [t[1::], t], [1000*np.diff(t), u], marker=True, axes='multi',
    yname=['Sampling Period (ms)', 'Control Output (-)'])