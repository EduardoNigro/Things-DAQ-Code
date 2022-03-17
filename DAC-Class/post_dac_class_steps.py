""" post_dac_class_steps.py

Contains the example code to run the DAC class through a sequence of stpes.
https://thingsdaq.org/2022/03/17/python-dac-class/

Use this code in conjuction with a LabJack or an oscilloscope.

Author: Eduardo Nigro
    rev 0.0.1
    2022-03-17

"""
import time
import numpy as np
from gpiozero_extended import DAC

# Assigning parameter values
tstep = 0.5 # Interval between step changes (s)
tstop = 10 # Total execution time (s)

# Creating DAC object on GPIO pin 18
dac = DAC(dacpin=18)
dac.set_calibration(1.116, -0.185)

# Initializing timers and starting main clock
tprev = 0
tcurr = 0
tstart = time.perf_counter()

# Running execution loop
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    # Updating analog output every `tstep` seconds with
    # random voltages between 0 and 3 V every 0.5 V
    if (np.floor(tcurr/tstep) - np.floor(tprev/tstep)) == 1:
        dac.set_output(np.round(6*np.random.rand())/2)
    # Updating previous time and getting new current time (s)
    tprev = tcurr
    tcurr = time.perf_counter() - tstart

print('Done.')
# Releasing pins
del dac
