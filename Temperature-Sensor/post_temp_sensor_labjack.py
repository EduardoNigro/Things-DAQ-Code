""" post_temp_sensor_labjack.py 

Uses type `K` thermocouple with LabJack T7.

This example shows how to use a LabJack T7 to measure temperature.

For more details go to my post:
https://thingsdaq.org/2022/10/15/temperature-sensor-with-raspberry-pi/

Author: Eduardo Nigro
    rev 0.0.1
    2022-10-15

"""
# Importing modules and classes
import time
import numpy as np
from labjack_unified.devices import LabJackT7

# Creating LabJack object
ljt7 = LabJackT7()
# Assigning `K` type thermocouple to channel AIN0
ljt7.set_TC('AIN0', 'K')
# Assigning some parameters
tsample = 0.5  # Sampling period for code execution (s)
tdisp = 1  # Sampling period for value display (s)
tstop = 20  # Total execution time (s)

# Initializing variables and starting main clock
tprev = 0
tcurr = 0
tstart = time.perf_counter()

# Execution loop
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    # Pausing for `tsample`
    time.sleep(tsample)
    # Getting current time (s)
    tcurr = time.perf_counter() - tstart
    # Getting current temperature
    tempcurr = ljt7.get_TCtemp()
    # Displaying temperature every `tdisp` seconds
    if (np.floor(tcurr/tdisp) - np.floor(tprev/tdisp)) == 1:
        print("Temperature = {:d} deg C".format(int(np.round(tempcurr))))
    # Updating previous time value
    tprev = tcurr

print('Done.')
# Closing LabJack object
ljt7.close()
