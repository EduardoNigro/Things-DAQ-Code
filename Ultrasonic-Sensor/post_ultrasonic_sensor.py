""" post_ultrasonic_sensor.py 

Uses ultrasonic sensor HC-SR04.

This example shows the operating principle of HC-SR04 to measure distance
through the implementation of a very simple class.

For more details go to my post:
https://thingsdaq.org/2022/11/04/ultrasonic-sensor-with-raspberry-pi/

Author: Eduardo Nigro
    rev 0.0.1
    2022-11-04

"""
# Importing modules and classes
import time
from gpiozero import DigitalInputDevice, DigitalOutputDevice

class UltraSonic:
    """
    Simple class that illustrates the ultrasonic sensor operating principle.

    """
    def __init__(self, echo, trigger):
        # Assingning ultrasonic sensor echo and trigger GPIO pins
        self._usoundecho = DigitalInputDevice(echo)
        self._usoundtrig = DigitalOutputDevice(trigger)
        # Assigning speed of sound (cm/s)
        self.speedofsound = 34300

    @property
    def distance(self):
        # Sending trigger pulse (~10 us)
        self._usoundtrig.on()
        time.sleep(0.000010)
        self._usoundtrig.off()
        # Detecting echo pulse start
        while self._usoundecho.value == 0:
            trise = time.perf_counter()
        # Detecting echo pulse end
        while self._usoundecho.value == 1:
            tfall = time.perf_counter()
        # Returning distance (cm)
        return 0.5 * (tfall-trise) * self.speedofsound

    @distance.setter
    def distance(self, _):
        print('"value" is a read only attribute.')
    
    def __del__(self):
        self._usoundecho.close()
        self._usoundtrig.close()

# Assigning some parameters
tsample = 1  # Sampling period for code execution (s)
tstop = 10  # Total execution time (s)
# Creating ultrasonic sensor object
usensor = UltraSonic(echo=27, trigger=4)
# Initializing variable and starting main clock
tcurr = 0
tstart = time.perf_counter()

# Execution loop
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    print('Waiting for sensor...')
    time.sleep(tsample)
    # Getting current time (s)
    tcurr = time.perf_counter() - tstart
    # Displaying measured distance
    print("Distance = {:0.1f} cm".format(usensor.distance))    

print('Done.')
# Deleting sensor
del usensor
