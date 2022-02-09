""" post_mcp3008_sampling_test.py 

Runs a sampling speed test for SPI with software or hardware implementations.

This is the code used to generate the data for the implementation comparison
in my post: https://thingsdaq.org/2022/01/24/mcp3008-with-raspberry-pi/

Note: Use the utils.py module located in the same folder as this file.

Author: Eduardo Nigro
    rev 0.0.1
    2022-01-24

"""
import time
import numpy as np
from utils import plot_line
from gpiozero import MCP3008

# Defining test type
# 'SW' or 'HW'
testtype = 'SW'

# Assigning some test parameters
vref = 3.3  # Reference voltage for MCP3008
tstop = 5  # Total execution time of each data point (s)
# Assining outer loop parameters
nmeas = 3  # Number of repeat measurements per test point
chnummax = 8  # Number of test channels
chts = []  # Output array with mean sampling period
for i in range(chnummax):
    # Assigning inner loop parameters
    chnums = range(0, i+1)
    if testtype == 'SW':
        channels = [
            MCP3008(channel=ch, clock_pin=17, miso_pin=5, mosi_pin=6, select_pin=18)
            for ch in chnums]
    elif testtype == 'HW':
        channels = [
            MCP3008(channel=ch, clock_pin=11, miso_pin=9, mosi_pin=10, select_pin=8)
            for ch in chnums]
    # Doing repeat measurements for each data point
    chtsmeas = 0
    for j in range(nmeas):
        # Preallocating output arrays for plotting
        t = [[] for _ in range(len(channels))]
        # Initializing variables and starting main clock
        tcurr = 0
        tstart = time.perf_counter()
        # Execution loop that does the actual data sampling
        print('Running sampling test point', str(j+1), 'for', str(i+1), 'channel(s) ...')
        while tcurr <= tstop:
            for j, channel in enumerate(channels):
                # Getting current time (s)
                tcurr = time.perf_counter() - tstart
                # Getting potentiometer voltage (dummy sample)
                vcurr = vref*channel.value
                # Storing elapsed time (s)
                t[j].append(tcurr)
        # Calculating median sampling period (ms) for each channel
        chtsgrp = [1000*np.median(np.diff(tch)) for tch in t]
        # Calculating sum of sampling period (ms) for all channels
        chtsmeas += np.mean(chtsgrp)
    # Calculating mean sampling period for `i` channels
    chts.append(chtsmeas/nmeas)
    # Releasing pins
    [ch.close() for ch in channels]

# Plotting results
plot_line(
    [np.arange(1, chnummax+1)], [chts], line=False, marker=True,
    figsize=(500, 500),
    xname='Number of Input Channels',
    yname='Sampling Period per Channel (ms)'
)