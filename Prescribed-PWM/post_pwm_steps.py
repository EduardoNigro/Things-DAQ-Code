""" post_pwm_steps.py

Runs a prescribed PWM duty cycle sequence of steps on a Raspberry Pi.
Please go to this post for more info:
https://thingsdaq.org/2022/01/02/prescribed-pwm-duty-cycle/

Setup:
    Connect one leg of the LED (with a series resistor of 300 to 1000 Ohm)
    to GPIO 17 and the other leg to GND.

Author: Eduardo Nigro
    rev 0.0.1
    2022-01-02

"""
import time
import numpy as np
from utils import plot_line
from gpiozero import PWMOutputDevice

# Assigning parameter values
pinled = 17  # PWM output (LED input) pin
pwmfreq = 200  # PWM frequency (Hz)
pwmvalue = [0.4, 0.6, 0.8, 1.0, 0.1, 0.3, 0.5, 0.7, 0.9]
tstep = 1.0  # Interval between step changes (s)
tsample = 0.02  # Sampling period for code execution (s)
tstop = tstep * (len(pwmvalue)+1)  # Total execution time (s)
# Preallocating output arrays for plotting
t = []  # Time (s)
value = []  # PWM output duty cycle value

# Creating PWM output object (LED input)
led = PWMOutputDevice(pinled, frequency=pwmfreq)
# initializing other variables used in the loop
count = 0
valuecurr = 0.2

# Initializing timers and starting main clock
tprev = 0
tcurr = 0
tstart = time.perf_counter()

# Running execution loop
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    # Updating PWM output every `tstep` seconds
    # with values from prescribed sequence
    if (np.floor(tcurr/tstep) - np.floor(tprev/tstep)) == 1:
        valuecurr = pwmvalue[count]
        led.value = valuecurr
        count += 1
    # Acquiring digital data every `tsample` seconds
    # and appending values to output arrays
    if (np.floor(tcurr/tsample) - np.floor(tprev/tsample)) == 1:
        t.append(tcurr)
        value.append(valuecurr)
    # Updating previous time and getting new current time (s)
    tprev = tcurr
    tcurr = time.perf_counter() - tstart

# Releasing pins
led.close()
print('Done.')

# Plotting results 
plot_line([t], [value], yname='PWM OUtput')
plot_line([t[1::]], [1000*np.diff(t)], yname='Sampling Period (ms)')
