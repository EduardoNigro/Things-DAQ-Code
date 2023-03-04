""" post_pulse_rate_realtime.py 

Uses keyestudio pulse rate monitor KS0015 and 7-segment LED display KS0445.

This example shows how to use the KS0015 sensor with the Raspberry Pi.
An MCP3008 ADC chip is required to read the analog sensor output. The KS0445
display is used to show the pulse rate in real-time.

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
import tm1637
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


# Creating object for the pulse rate sensor output and LED display
vch = MCP3008(channel=0, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
tm = tm1637.TM1637(clk=18, dio=17)

# Assigning some parameters
tsample = 0.1  # Sampling period for code execution (s)
tstop = 60  # Total execution time (s)
tbuffer = 20  # Data buffer length(s)
tdisp = 1  # Display update period (s)
vref = 3.3  # Reference voltage for MCP3008
# Preallocating circular buffer arrays for real-time processing
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
tm.show('Hold')
print('Running code for', tstop, 'seconds ...')
print('Waiting', tbuffer, 'seconds for buffer fill.')
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
        # Updating circular buffer arrays
        if len(t) == tbuffer/tsample:
            t = t[1::]
            v = v[1::]
            vfilt = vfilt[1::]
        t = np.concatenate((t, [tcurr]))
        v = np.concatenate((v, [x[0]]))
        vfilt = np.concatenate((vfilt, [y[0]]))
        # Updating previous filter output values
        for i in range(len(a)-1, 0, -1):
            y[i] = y[i-1]
        # Updating previous filter input values
        for i in range(len(b)-1, 0, -1):
            x[i] = x[i-1]
    # Processing signal in the buffer every `tdisp` seconds
    if ((np.floor(tcurr/tdisp) - np.floor(tprev/tdisp)) == 1) & (tcurr > tbuffer):
        # Calculating and normalizing sensor signal derivative
        dvdt = np.gradient(vfilt, t)
        dvdt = dvdt/np.max(dvdt)
        # Finding heart rate trigger event times
        icl, ncl = find_cluster(dvdt>0.25, 1)
        ttrigger = t[icl]
        # Calculating and displaying pulse rate (bpm)
        bpm = 60/np.median(np.diff(ttrigger))
        tm.number(int(bpm))
    # Updating previous time value
    tprev = tcurr

print('Done.')
tm.show('Done')
# Releasing pins
vch.close()
