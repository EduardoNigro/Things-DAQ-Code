""" post_joystick.py 

Uses keyestudio joystick KS0008

This example shows how to use the KS0008 joystick with the Raspberry Pi.
An MCP3008 ADC chip is required to read the analog joystick outputs.

For more details go to my post:
https://thingsdaq.org/2022/11/24/joystick-with-raspberry-pi/

Author: Eduardo Nigro
    rev 0.0.1
    2022-11-24

"""
# Importing modules and classes
import time
import numpy as np
from gpiozero import MCP3008, DigitalInputDevice

# Creating objects for the joystick outputs
joyLR = MCP3008(channel=0, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
joyFB = MCP3008(channel=1, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
joyB = DigitalInputDevice(18)
# Assigning some parameters
tsample = 0.02  # Sampling period for code execution (s)
tdisp = 0.5  # Output display period (s)
tstop = 30  # Total execution time (s)
vref = 3.3  # Reference voltage for MCP3008

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
        valLRcurr = joyLR.value
        valFBcurr = joyFB.value
        # Calculating current time raw voltages
        vLRcurr = vref*valLRcurr
        vFBcurr = vref*valFBcurr
        # Getting the Z axis state
        Bcurr = joyB.value
        # Displaying output voltages every `tdisp` seconds
        if (np.floor(tcurr/tdisp) - np.floor(tprev/tdisp)) == 1:
            print("X = {:0.2f} V , Y = {:0.2f} V , B = {:d}".
            format(vLRcurr, vFBcurr, Bcurr))
    # Updating previous time value
    tprev = tcurr

print('Done.')
# Releasing pins
joyLR.close()
joyFB.close()
joyB.close()
