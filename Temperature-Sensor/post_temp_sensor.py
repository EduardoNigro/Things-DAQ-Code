""" post_temp_sensor.py 

Uses LM35 temperature sensor with MCP3008 A/D chip.

This example shows how to use an MCP3008 to measure the analog output of an
analog linear temperature sensor.

For more details go to my post:
https://thingsdaq.org/2022/10/15/temperature-sensor-with-raspberry-pi/

Author: Eduardo Nigro
    rev 0.0.1
    2022-10-15

"""
# Importing modules and classes
import time
import numpy as np
from gpiozero import MCP3008

# Creating ADC channel object for temperature sensor
chtemp = MCP3008(channel=0, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
# Assigning some parameters
tsample = 0.5  # Sampling period for code execution (s)
tdisp = 1  # Sampling period for value display (s)
tstop = 20  # Total execution time (s)
vref = 3.3  # Reference voltage for MCP3008
ktemp = 100  # Temperature sensor gain (degC/V)

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
    # Getting sensor normalized voltage output
    valuecurr = chtemp.value
    # Calculating temperature
    tempcurr = vref*ktemp*valuecurr
    # Displaying temperature every `tdisp` seconds
    if (np.floor(tcurr/tdisp) - np.floor(tprev/tdisp)) == 1:
        print("Temperature = {:d} deg C".format(int(np.round(tempcurr))))
    # Updating previous time value
    tprev = tcurr

print('Done.')
# Releasing GPIO pins
chtemp.close()
