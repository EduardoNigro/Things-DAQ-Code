""" post_pulse_rate_filtered.py 

Uses keyestudio pulse rate monitor KS0015

This example shows how to use the KS0015 sensor with the Raspberry Pi.
An MCP3008 ADC chip is required to read the analog sensor output.

A band-pass digital filter is used to improve the signal for further
processing. The signal derivative is used to detect the pulse rate.

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
from utils import find_cluster


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
tsample = 0.1  # Sampling period for code execution (s)
tstop = 30  # Total execution time (s)
vref = 3.3  # Reference voltage for MCP3008
# Preallocating output arrays for plotting
t = np.array([])  # Time (s)
v = np.array([])  # Sensor output voltage (V)
vfilt = np.array([])  # Filtered sensor output voltage (V)

# Waiting for 5 seconds for signal stabilization
time.sleep(5)

# First order digital band-pass filter parameters
fc = np.array([0.5, 5])  # Filter cutoff frequencies (Hz)
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
x = [vref*vch.value] * len(b)  # x[n], x[n-1]
y = [0] * len(a)  # y[n], y[n-1], y[n-2]
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
        # Getting current sensor voltage
        valuecurr = vref * vch.value
        # Assigning sensor voltage output to input signal array
        x[0] = valuecurr
        # Filtering signals
        y[0] = -np.sum(a[1::]*y[1::]) + np.sum(b*x)
        # Updating output arrays
        t = np.concatenate((t, [tcurr]))
        v = np.concatenate((v, [x[0]]))
        vfilt = np.concatenate((vfilt, [y[0]]))
        # Updating previous filter output values
        for i in range(len(a)-1, 0, -1):
            y[i] = y[i-1]
        # Updating previous filter input values
        for i in range(len(b)-1, 0, -1):
            x[i] = x[i-1]
    # Updating previous time value
    tprev = tcurr

print('Done.')
# Releasing pins
vch.close()

# Calculating and normalizing sensor signal derivative
dvdt = np.gradient(vfilt, t)
dvdt = dvdt/np.max(dvdt)
# Finding heart rate trigger event times
icl, ncl = find_cluster(dvdt>0.25, 1)
ttrigger = t[icl]
# Calculating heart rate (bpm)
bpm = 60/np.median(np.diff(ttrigger))
print("Heart rate = {:0.0f} bpm".format(bpm))    

# Plotting results 
ax = make_fig()
ax.set_ylabel('Normalized Derivative ( - )', fontsize=12)
ax.plot(t, dvdt, linewidth=1.5, color='#1f77b4', zorder=0)
for ik, nk in zip(icl, ncl):
    if ik+nk < len(t):
        ax.plot(t[ik:ik+nk], dvdt[ik:ik+nk], color='#aa0000')
ax = make_fig()
ax.set_ylabel('Filtered Output (V)', fontsize=12)
ax.plot(t, vfilt, linewidth=1.5, color='#1f77b4', zorder=0)
for ik, nk in zip(icl, ncl):
    ax.plot(t[ik:ik+nk], vfilt[ik:ik+nk], color='#aa0000')
    ax.scatter(t[ik+1], vfilt[ik+1], s=25, c='#aa0000')
