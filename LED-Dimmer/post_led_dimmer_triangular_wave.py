""" post_led_dimmer_triangular_wave.py

Plots how a triangular wave generation function works.

For more details go to my post:
https://thingsdaq.org/2023/01/16/led-dimmer-with-raspberry-pi/

Author: Eduardo Nigro
    rev 0.0.1
    2023-01-16

"""
# Importing modules and classes
import time
import numpy as np
import matplotlib.pyplot as plt

# Assigning time parameter values
tramp = 2  # PWM output 0 to 100% ramp time (s)
tsample = 0.02  # Sampling period for code execution (s)
tstop = 8  # Total execution time (s)

# Preallocating output arrays for plotting
t = [] # Time (s)
valuelin = [] # Linear output value
valuetooth = [] # Tooth saw output value
valuetri = [] # Triangular output value


# Defining function to generate Matplotlib figure with axes
def make_fig():
    #
    # Creating figure
    fig = plt.figure(
        figsize=(4.3, 3),
        facecolor='#f8f8f8',
        tight_layout=True)
    # Adding and configuring axes
    ax = fig.add_subplot(
        facecolor='#ffffff',
        )
    ax.grid(
    linestyle=':',
    )
    # Returning axes handle
    return ax


# Defining triangular wave generator funciton
def calc_ramp(t, tramp):
    #
    # Creating linear output so the value is 1 when t=tramp
    valuelin = t/tramp
    # Creating time segment counter
    k = t//tramp
    # Shifting output down by number of segment counts
    valuetooth = valuelin - k
    # Flipping odd count output to create triangular wave
    valuetri = valuetooth
    if (k % 2) == 1:
        valuetri = 1 - valuetri
    return valuelin, valuetooth, valuetri


# Initializing timers and starting main clock
tprev = 0
tcurr = 0
tstart = time.perf_counter()

# Executing loop
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop+tsample:
    # Executing code every `tsample` seconds
    if (np.floor(tcurr/tsample) - np.floor(tprev/tsample)) == 1:
        # Getting button properties only once
        valuelincurr, valuetoothcurr, valuetricurr = calc_ramp(tcurr, tramp)
        # Appending current values to output arrays
        t.append(tcurr)
        valuelin.append(valuelincurr)
        valuetooth.append(valuetoothcurr)
        valuetri.append(valuetricurr)
    # Updating previous time and getting new current time (s)
    tprev = tcurr
    tcurr = time.perf_counter() - tstart
print('Done.')

# Plotting results
ylist = [valuelin, valuetooth, valuetri]
namelist = ['Linear Output', 'Tooth Saw Output', 'Triangular Output']
for y, yname in zip(ylist, namelist):
    ax = make_fig()
    ax.set_xlabel('Time (s)', fontsize=12)
    ax.set_ylabel(yname, fontsize=12)
    ax.plot(t, y)
