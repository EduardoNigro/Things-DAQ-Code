""" post_encoder_signal.py 

Contains the example code to investigate the signal of an incremental encoder.
Run this in a terminal instead of an interactive window.
https://thingsdaq.org/2022/03/09/encoder-with-raspberry-pi/

Author: Eduardo Nigro
    rev 0.0.1
    2022-03-09

"""
# Importing modules and classes
import time
import numpy as np
from utils import plot_line
from gpiozero import DigitalInputDevice

# Assigning parameters
tstop = 0.5 # Total execution time (s)
t = [] # Output time array
s1 = [] # Output sampled state 1 array
s2 = [] # Output sampled state 2 array

# Creating digital input objects
ports = [24, 25]
pins = [DigitalInputDevice(port) for port in ports]

# Detecting when encoder is turned to start execution loop
statecurr = pins[0].value
stateprev = statecurr
print('Turn encoder.')
while statecurr == stateprev:
    statecurr = pins[0].value

# Initializing timers and starting main clock
tcurr = 0
tstart = time.perf_counter()

# Executing acquisition loop
print('Running code for', tstop, 'second(s) ...')
while tcurr <= tstop:
    # Acquiring digital data as fast as possible
    # and appending values to output arrays
    t.append(tcurr)
    s1.append(pins[0].value)
    s2.append(pins[1].value)
    # Updating current time
    tcurr = time.perf_counter() - tstart

print('Done.')
# Releasing pins
[pin.close() for pin in pins]

# Plotting results 
plot_line([t, t, t[1::]], [s1, s2, 1000*np.diff(t)], axes='multi',
          yname=['GPIO '+str(p) for p in ports] + ['Sampling Period (ms)'])

