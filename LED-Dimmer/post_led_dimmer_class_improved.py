""" post_led_dimmer_class_improved.py

Creates a class to represent an (improved) LED dimmer.

This example is derived from `post_led_dimmer.py` where the dimmer
functionality is packaged into a class, so it's much easier to create and
use multiple dimmers. Two dimmers are created to illustrate the concept.

You can turn the dimmer off by pressing and releasing the button.

For more details go to my post:
https://thingsdaq.org/2023/01/16/led-dimmer-with-raspberry-pi/

Author: Eduardo Nigro
    rev 0.0.1
    2023-01-16

"""
# Importing modules and classes
import time
import numpy as np
from gpiozero import DigitalInputDevice, PWMOutputDevice


class Dimmer:
    """
    Class that represents an LED dimmer.

    """
    def __init__(self, pinbutton=None, pinled=None):
        # Assigning GPIO pins
        self._pinbutton = pinbutton  # button input pin
        self._pinled = pinled  # PWM output (LED input) pin
        # Assigning dimmer parameter values
        self._pwmfreq = 200  # PWM frequency (Hz)
        self._tshift = 0  # PWM ramp time shift (to start where it left off)
        self._tramp = 3  # PWM output 0 to 100% ramp time (s)
        self._toff = 0.3  # Time window that turns dimmer off (s)
        # Resetting dimmer
        self._reset_timer()
        # Creating button and PWM output (LED input) objects
        self._button = DigitalInputDevice(self._pinbutton, pull_up=True, bounce_time=0.1)
        self._led = PWMOutputDevice(self._pinled, frequency=self._pwmfreq)

    def _calc_ramp_value(self, t):
        # Creating linear output so the value is 1 when t=tramp
        valuelin = t/self._tramp
        # Creating time segment counter
        self._kcurr = t//self._tramp
        # Shifting output down by number of segment counts
        value = valuelin - self._kcurr
        # Flipping odd count output to create triangular wave
        if (self._kcurr % 2) == 1:
            value = 1 - value
        return value

    def _reset_timer(self):
        # Resets timer parameters
        self._tshift = 0  # PWM ramp time shift (to start where it left off)
        self._tpressed = 0  # Time button was pressed (s)
        self._pressed = False  # Current button pressed state
        self._pressedbefore = False  # Previous button pressed state
        self._valueprev = 0  # Previous PWM value
        self._kcurr = -1  # Current PWM ramp segment counter
        self._kprev = 0  # Previous PWM ramp segmment counter
        self._tdown = 0  # Time when button was pressed
        self._tup = np.inf  # Time when button was released

    def start_timer(self, tstart):
        # Starts dimmer execution timer
        self._tstart = tstart

    def update_value(self, t):
        # Getting button properties only once
        self._pressed = self._button.is_active
        # Checking for button press
        if self._pressed and not self._pressedbefore:
            # Calculating ramp time shift based on last PWM value
            if (self._kprev % 2) == 0:
                self._tshift = self._valueprev*self._tramp
            else:
                self._tshift = (1-self._valueprev)*self._tramp + self._tramp
            # Starting pressed button timer
            self._tpressed = time.perf_counter() - self._tstart
            # Updating previous button state
            self._pressedbefore = True
            # Storing time when button was pressed
            self._tdown = time.perf_counter()
        # Checking for button release
        if not self._pressed and self._pressedbefore:
            # Storing PWM value and ramp segment counter
            self._valueprev = self._led.value
            self._kprev = self._kcurr
            # Updating previous button state
            self._pressedbefore = False
            # Storing time when button was released
            self._tup = time.perf_counter()
        # Updating PWM output (LED intensity)
        if self._pressed:
            self._led.value = self._calc_ramp_value(t-self._tpressed+self._tshift)
        if (not self._pressed) and (self._tup-self._tdown < self._toff):
            self._reset_timer()
            self._led.value = 0

    def __del__(self):
        self._button.close()
        self._led.close()


# Assigning execution loop parameter values
tsample = 0.02 # Sampling period for code execution (s)
tstop = 30 # Total execution time (s)

# Creating dimmer objects
dimmer = Dimmer(pinled=17, pinbutton=5)

# Initializing timers and starting main clock
tprev = 0
tcurr = 0
tstart = time.perf_counter()
# Resettting dimmer timer
dimmer.start_timer(tstart)

# Executing loop
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    # Executing code every `tsample` seconds
    if (np.floor(tcurr/tsample) - np.floor(tprev/tsample)) == 1:
        # Updating dimmer output
        dimmer.update_value(tcurr)
    # Updating previous time and getting new current time (s)
    tprev = tcurr
    tcurr = time.perf_counter() - tstart
print('Done.')

# Releasing pins
del dimmer
