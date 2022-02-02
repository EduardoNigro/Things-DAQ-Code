""" post_pwm_ramp.py

Runs a prescribed PWM duty cycle sequence of ramps on a Raspberry Pi.
Please go to this post for more info:
https://thingsdaq.org/2022/01/02/prescribed-pwm-duty-cycle/


Setup:
    Connect one leg of the LED (with a series resistor of 300 to 1000 Ohm)
    to GPIO 17 and the other leg to GND.

"""
import time
import numpy as np
from utils import plot_line
from scipy.interpolate import interp1d
from gpiozero import PWMOutputDevice

# Assigning parameter values
pinled = 17  # PWM output (LED input) pin
pwmfreq = 200  # PWM frequency (Hz)
rampduration = [0, 0.5, 1.5, 0.5, 1.5, 0.5, 1.5, 0.5, 1.5, 0.5, 1.5]
rampvalue = [0, 0.2, 0.0, 0.4, 0.0, 0.6, 0.0, 0.8, 0.0, 1.0, 0.0]
tsample = 0.02  # Sampling period data sampling (s)
tstop = np.sum(rampduration)  # Total execution time (s)
# Preallocating output arrays for plotting
t = []  # Time (s)
value = []  # PWM output duty cycle value

# Creating interpolation function for ramp sequence
tramp = np.cumsum(rampduration)
framp = interp1d(tramp, rampvalue)
# Creating PWM output object (LED input)
led = PWMOutputDevice(pinled, frequency=pwmfreq)

# Initializing timers and starting main clock
tprev = 0
tcurr = 0
tstart = time.perf_counter()

# Running execution loop
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    # Updating PWM output every loop step with
    # interpolated ramp values at the current time
    valuecurr = framp(tcurr)
    led.value = valuecurr
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
