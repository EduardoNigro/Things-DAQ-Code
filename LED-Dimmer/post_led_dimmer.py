""" post_led_dimmer.py

Creates a dimmed LED that can be modulated by pressing and holding a button.

This example shows how to modulate the duty cycle of a PWM signal using the
time a button is pressed. To make things more interesting, if you let go of
the button and then press it again, the duty cycle modulation continues from
where it was left off at the moment of buttone release. The PWM output is used
to light an LED.

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
from utils import plot_line

# Assigning dimmer parameter values
pinled = 17  # PWM output (LED input) pin
pinbutton = 5  # button input pin
pwmfreq = 200  # PWM frequency (Hz)
pressedbefore = False  # Previous button pressed state
valueprev = 0  # Previous PWM value
kprev = 0  # Previous PWM ramp segmment counter
tshift = 0  # PWM ramp time shift (to start where it left off)
tramp = 2  # PWM output 0 to 100% ramp time (s)
# Assigning execution loop parameter values
tsample = 0.02  # Sampling period for code execution (s)
tstop = 30  # Total execution time (s)

# Preallocating output arrays for plotting
t = [] # Time (s)
value = [] # PWM output duty cycle value
k = [] # Ramp segment counter


def calc_ramp(t, tramp):
    """
    Creates triangular wave output with amplitude 0 to 1 and period 2 x tramp.

    """
    # Creating linear output so the value is 1 when t=tramp
    valuelin = t/tramp
    # Creating time segment counter
    k = t//tramp
    # Shifting output down by number of segment counts
    value = valuelin - k
    # Flipping odd count output to create triangular wave
    if (k % 2) == 1:
        value = 1 - value
    return value, k


# Creating button and PWM output (LED input) objects
button = DigitalInputDevice(pinbutton, pull_up=True, bounce_time=0.1)
led = PWMOutputDevice(pinled, frequency=pwmfreq)

# Initializing timers and starting main clock
tpressed = 0
tprev = 0
tcurr = 0
tstart = time.perf_counter()
# Initializing PWM value and ramp time segment counter
valuecurr = 0
kcurr = -1

# Executing loop
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    # Executing code every `tsample` seconds
    if (np.floor(tcurr/tsample) - np.floor(tprev/tsample)) == 1:
        # Getting button properties only once
        pressed = button.is_active
        # Checking for button press
        if pressed and not pressedbefore:
            # Calculating ramp time shift based on last PWM value
            if (kprev % 2) == 0:
                tshift = valueprev*tramp
            else:
                tshift = (1-valueprev)*tramp + tramp
            # Starting pressed button timer
            tpressed = time.perf_counter() - tstart
            # Updating previous button state
            pressedbefore = True
        # Checking for button release
        if not pressed and pressedbefore:
            # Storing PWM value and ramp segment counter
            valueprev = led.value
            kprev = kcurr
            # Updating previous button state
            pressedbefore = False
        # Updating PWM output (LED intensity)
        if pressed:
            valuecurr, kcurr = calc_ramp(tcurr-tpressed+tshift, tramp)
            led.value = valuecurr
        # Appending current values to output arrays
        t.append(tcurr)
        value.append(valuecurr)
        k.append(kcurr)
    # Updating previous time and getting new current time (s)
    tprev = tcurr
    tcurr = time.perf_counter() - tstart
print('Done.')
# Releasing pins
led.close()
button.close()

# Plotting results 
plot_line([t]*2, [value, k],
          yname=['PWM Output', 'Segment Counter'], axes='multi')
plot_line([t[1::]], [1000*np.diff(t)], yname=['Sampling Period (ms)'])
