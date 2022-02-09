""" post_mcp3008_example.py 

Uses MCP3008 ADC to measure potentiometer analog output.

This example shows how to use an MCP3008 to measure the analog output of a
potentiometer. It also attaches an LED to a PWM output that is proportional
to the measured pot. voltage.

For more details go to my post:
https://thingsdaq.org/2022/01/24/mcp3008-with-raspberry-pi/

Author: Eduardo Nigro
    rev 0.0.1
    2022-01-24

"""
import time
import numpy as np
from utils import plot_line
from gpiozero import PWMOutputDevice, MCP3008

# Creating LED PWM object
led = PWMOutputDevice(16)
# Creating ADC channel object
pot = MCP3008(channel=0, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
# Assining some parameters
tsample = 0.02  # Sampling period for code execution (s)
tstop = 10  # Total execution time (s)
vref = 3.3  # Reference voltage for MCP3008
# Preallocating output arrays for plotting
t = []  # Time (s)
v = []  # Potentiometer voltage output value (V)
vfilt = []  # Fitlered voltage output value (V)
# First order digital low-pass filter parameters
fc = 2  # Filter cutoff frequency (Hz)
wc = 2*np.pi*fc  # Cutoff frequency (rad/s)
tau = 1/wc  # Filter time constant (s)
c0 = tsample/(tsample+tau)  # Digital filter coefficient
c1 = tau/(tsample+tau)  # Digital filter coefficient
# Initializing filter previous value
valueprev = pot.value
time.sleep(tsample)
# Initializing variables and starting main clock
tprev = 0
tcurr = 0
tstart = time.perf_counter()

# Execution loop
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    # Getting current time (s)
    tcurr = time.perf_counter() - tstart
    # Doing I/O and computations every `tsample` seconds
    if (np.floor(tcurr/tsample) - np.floor(tprev/tsample)) == 1:
        # Getting potentiometer normalized voltage output
        valuecurr = pot.value
        # Filtering value
        valuefilt = c0*valuecurr + c1*valueprev
        # Calculating current raw and filtered voltage
        vcurr = vref*valuecurr
        vcurrfilt = vref*valuefilt
        # Updating LED PWM output
        led.value = valuefilt
        # Updating output arrays
        t.append(tcurr)
        v.append(vcurr)
        vfilt.append(vcurrfilt)
        # Updating previous filtered value
        valueprev = valuefilt
    # Updating previous time value
    tprev = tcurr

print('Done.')
# Releasing pins
pot.close()
led.close()
# Plotting results
plot_line([t]*2, [v, vfilt], yname='Pot Output (V)', legend=['Raw', 'Filtered'])
plot_line([t[1::]], [1000*np.diff(t)], yname='Sampling Period (ms)')