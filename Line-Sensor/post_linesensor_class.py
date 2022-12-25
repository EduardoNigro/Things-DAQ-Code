""" post_linesensor_class.py 

Implements a class for a line tracking sensor using keyestudio white LED
KS0016 and photocell sensor KS0028.

The class can be used as part of a closed-loop control system for a line
tracking robot.

For more details go to my post:
https://thingsdaq.org/2022/12/24/line-tracking-sensor-for-raspberry-pi/

Author: Eduardo Nigro
    rev 0.0.1
    2022-12-24

"""
# Importing modules and classes
import time
import numpy as np
from gpiozero import MCP3008, DigitalOutputDevice

class LineSensor:
    """
    Class that implements a line tracking sensor.

    """
    def __init__(self, lightsource, photosensor):
        #
        # Defining transfer function parameters
        self._k = 335.5
        self._w = 5.821
        self._u0 = 0.700
        # Creating GPIOZero objects
        self._lightsource = DigitalOutputDevice(lightsource)
        self._photosensor = MCP3008(
            channel=photosensor,
            clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
        # Turning light source on
        self._lightsource.value = 1

    @property
    def position(self):
        # Getting sensor output
        u = self._photosensor.value
        # Calculating position using transfer function
        return self._k*(u-self._u0)**3 + self._w*(u-self._u0)

    @position.setter
    def position(self, _):
        print('"position" is a read only attribute.')
    
    def __del__(self):
        self._lightsource.close()
        self._photosensor.close()


# Assigning some parameters
tsample = 0.1  # Sampling period for code execution (s)
tdisp = 0.5  # Output display period (s)
tstop = 60  # Total execution time (s)
# Creating line tracking sensor object on GPIO pin 18 for
# light source and MCP3008 channel 0 for photocell output
linesensor = LineSensor(lightsource=18, photosensor=0)

# Initializing variables and starting main clock
tprev = 0
tcurr = 0
tstart = time.perf_counter()
# Execution loop
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    # Getting current time (s)
    tcurr = time.perf_counter() - tstart
    # Doing I/O and computations every `tsample` seconds
    if (np.floor(tcurr/tsample) - np.floor(tprev/tsample)) == 1:
        poscurr = linesensor.position
        #
        # Insert control action here using gpiozero_extended.PID()
        #
        # Displaying sensor position every `tdisp` seconds
        if (np.floor(tcurr/tdisp) - np.floor(tprev/tdisp)) == 1:
            print("Position = {:0.1f} mm".format(poscurr))    
    # Updating previous time value
    tprev = tcurr

print('Done.')
# Deleting sensor
del linesensor
