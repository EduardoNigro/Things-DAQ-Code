""" post_joystick_filtered_bandpass.py 

Uses keyestudio joystick KS0008

This example shows how to use the KS0008 joystick with the Raspberry Pi,
where the voltage output is filtered with a band-pass digital filter.
An MCP3008 ADC chip is required to read the analog joystick outputs.

The first-order band-pass filter can be used to remove both the joystick
low frequency output drift as well as the high frequency output jitter.

For more details go to my post:
https://thingsdaq.org/2022/11/24/joystick-with-raspberry-pi/

Author: Eduardo Nigro
    rev 0.0.1
    2022-11-24

"""
# Importing modules and classes
import time
import numpy as np
from utils import plot_line
from gpiozero import MCP3008

# Creating ADC channel objects for the joystick inputs
joyLR = MCP3008(channel=0, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
joyFB = MCP3008(channel=1, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
# Assigning some parameters
tsample = 0.02  # Sampling period for code execution (s)
tstop = 30  # Total execution time (s)
vref = 3.3  # Reference voltage for MCP3008
# Preallocating output arrays for plotting
t = []  # Time (s)
xLRn = []  # Joy stick X direction output (-1 to 1)
xFBn = []  # Joy stick Y direction output (-1 to 1)
yLRn = []  # Filtered X direction output (-1 to 1)
yFBn = []  # Filtered Y direction output (-1 to 1)

# First order digital band-pass filter parameters
fc = np.array([0.005, 2])  # Filter cutoff frequencies (Hz)
tau = 1/(2*np.pi*fc)  # Filter time constants (s)
# Filter difference equation coefficients
a0 = tau[0]*tau[1]+(tau[0]+tau[1])*tsample+tsample**2
a1 = -(2*tau[0]*tau[1]+(tau[0]+tau[1])*tsample)
a2 = tau[0]*tau[1]
b0 = tau[0]*tsample
b1 = -tau[0]*tsample
# Assigning normalized coefficients
a = np.array([1, a1/a0, a2/a0])
b = np.array([b0/a0, b1/a0])
# Initializing filter values
xLR = [joyLR.value] * len(b)  # x[n], x[n-1]
xFB = [joyFB.value] * len(b)  # x[n], x[n-1]
yLR = [0] * len(a)  # y[n], y[n-1], y[n-2]
yFB = [0] * len(a)  # y[n], y[n-1], y[n-2]
time.sleep(tsample)

# Initializing variables and starting main clock
tprev = 0
tcurr = 0
tstart = time.perf_counter()
# Running execution loop
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    # Getting current time (s)
    tcurr = time.perf_counter() - tstart
    # Doing I/O and computations every `tsample` seconds
    if (np.floor(tcurr/tsample) - np.floor(tprev/tsample)) == 1:
        # Getting joy stick normalized voltage output
        xLR[0] = joyLR.value
        xFB[0] = joyFB.value
        # Filtering signals
        yLR[0] = -np.sum(a[1::]*yLR[1::]) + np.sum(b*xLR)
        yFB[0] = -np.sum(a[1::]*yFB[1::]) + np.sum(b*xFB)
        # Updating output arrays with normalized output
        # (The filtered values have no DC component)
        t.append(tcurr)
        xLRn.append(-1 + 2*xLR[0])
        xFBn.append(-1 + 2*xFB[0])
        yLRn.append(2*yLR[0])
        yFBn.append(2*yFB[0])
        # Updating previous filter output values
        for i in range(len(a)-1, 0, -1):
            yLR[i] = yLR[i-1]
            yFB[i] = yFB[i-1]
        # Updating previous filter input values
        for i in range(len(b)-1, 0, -1):
            xLR[i] = xLR[i-1]
            xFB[i] = xFB[i-1]
    # Updating previous time value
    tprev = tcurr

print('Done.')
# Releasing pins
joyLR.close()
joyFB.close()
# Plotting results
plot_line([t]*2, [xLRn, yLRn], yname='X Output', legend=['Raw', 'Filtered'])
plot_line([t]*2, [xFBn, yFBn], yname='Y Output', legend=['Raw', 'Filtered'])
