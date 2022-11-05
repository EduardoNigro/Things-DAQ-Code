""" post_ultrasonic_sensor_gpiozero.py 

Uses ultrasonic sensor HC-SR04.

This example shows how to use the `DistanceSensor` class in GPIOZero.
The class takes advantage of multi-threading for improved measurement accuracy.

For more details go to my post:
https://thingsdaq.org/2022/11/04/ultrasonic-sensor-with-raspberry-pi/

Author: Eduardo Nigro
    rev 0.0.1
    2022-11-04

"""
# Importing modules and classes
import time
from gpiozero import DistanceSensor

# Assigning some parameters
tsample = 1  # Sampling period for code execution (s)
tstop = 10  # Total execution time (s)
# Creating ultrasonic sensor object
usensor = DistanceSensor(echo=27, trigger=4, max_distance=2)
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
    # Displaying measured distance (with unit conversion)
    print("Distance = {:0.1f} cm".format(100*usensor.distance))    

print('Done.')
# Deleting sensor
del usensor
