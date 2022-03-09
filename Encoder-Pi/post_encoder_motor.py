""" post_encoder_motor.py

Contains the example code to run a DC motor that has an integrated shaft
enocder. Run this in a terminal instead of an interactive window.
https://thingsdaq.org/2022/03/09/encoder-with-raspberry-pi/

Author: Eduardo Nigro
    rev 0.0.1
    2022-03-09

"""
# Importing modules and classes
import time
import numpy as np
from utils import plot_line
from gpiozero_extended import Motor

# Assigning parameter values
T = 2  # Period of sine wave (s)
u0 = 1  # Motor output amplitude
tstop = 2  # Sine wave duration (s)
tsample = 0.01  # Sampling period for code execution (s)

# Creating motor object using GPIO pins 16, 17, and 18
# (using SN754410 quadruple half-H driver chip)
# Integrated encoder in on GPIO pins 24 and 25.
mymotor = Motor(
    enable1=16, pwm1=17, pwm2=18,
    encoder1=24, encoder2=25, encoderppr=300.8)
mymotor.reset_angle()

# Pre-allocating output arrays
t = []
theta = []

# Initializing current time step and starting clock
tprev = 0
tcurr = 0
tstart = time.perf_counter()

# Running motor sine wave output
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    # Pausing for `tsample` to give CPU time to process encoder signal
    time.sleep(tsample)
    # Getting current time (s)
    tcurr = time.perf_counter() - tstart
    # Assigning motor sinusoidal output using the current time step
    mymotor.set_output(u0 * np.sin((2*np.pi/T) * tcurr))
    # Updating output arrays
    t.append(tcurr)
    theta.append(mymotor.get_angle())
    # Updating previous time value
    tprev = tcurr

print('Done.')
# Stopping motor and releasing GPIO pins
mymotor.set_output(0, brake=True)
del mymotor

# Calculating motor angular velocity (rpm)
w = 60/360 * np.gradient(theta, t)

# Plotting results
plot_line([t, t, t[1::]], [theta, w, 1000*np.diff(t)], axes='multi',
          yname=[
              'Angular Position (deg.)',
              'Angular velocity (rpm)',
              'Sampling Period (ms)'])