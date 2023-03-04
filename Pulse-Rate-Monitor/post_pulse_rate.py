""" post_pulse_rate.py 

Uses keyestudio pulse rate monitor KS0015

This example shows how to use the KS0015 sensor with the Raspberry Pi.
An MCP3008 ADC chip is required to read the analog sensor output.

For more details go to my post:
https://thingsdaq.org/2023/03/03/pulse-rate-monitor-with-raspberry-pi/

Author: Eduardo Nigro
    rev 0.0.1
    2023-03-03

"""
# Importing modules and classes
import time
import numpy as np
import matplotlib.pyplot as plt
from gpiozero import MCP3008


# Defining function for plotting
def make_fig():
    # Creating Matplotlib figure
    fig = plt.figure(
        figsize=(8, 3),
        facecolor='#f8f8f8',
        tight_layout=True)
    # Adding and configuring axes
    ax = fig.add_subplot(xlim=(0, max(t)))
    ax.set_xlabel('Time (s)', fontsize=12)
    ax.grid(linestyle=':')
    # Returning axes handle
    return ax


# Creating object for the pulse rate sensor output
vch = MCP3008(channel=0, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)

# Assigning some parameters
tsample = 0.02  # Sampling period for code execution (s)
tstop = 30  # Total execution time (s)
vref = 3.3  # Reference voltage for MCP3008
# Preallocating output arrays for plotting
t = []  # Time (s)
v = []  # Sensor output voltage (V)

# Waiting for 5 seconds for signal stabilization
time.sleep(5)

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
        # Getting current sensor voltage
        valuecurr = vref * vch.value
        # Assigning current values to output arrays
        t.append(tcurr)
        v.append(valuecurr)
    # Updating previous time value
    tprev = tcurr

print('Done.')
# Releasing GPIO pins
vch.close()

# Plotting results 
ax = make_fig()
ax.set_ylabel('Sensor Output (V)', fontsize=12)
ax.plot(t, v, linewidth=1.5, color='#1f77b4')
ax = make_fig()
ax.set_ylabel('Sampling Period (ms)', fontsize=12)
ax.plot(t[1::], 1000*np.diff(t), linewidth=1.5, color='#1f77b4')
