""" post_dac_pi_basic.py

Contains the basic code for a PWM-based DAC for Raspberry Pi.
https://thingsdaq.org/2022/02/08/dac-with-raspberry-pi/

You can use this to explore the behavior of a DAC using a Raspberry Pi.

Author: Eduardo Nigro
    rev 0.0.1
    2022-02-08

"""
import time
import numpy as np
from utils import plot_line
from gpiozero import PWMOutputDevice, MCP3008

# Assigning parameter values
pwmfreq = 700 # PWM frequency (Hz)
pwmvalue = [0.05, 0.2, 0.4, 0.6, 0.8, 0.95, 0.9, 0.7, 0.5, 0.3, 0.1]
tsample = 0.002 # Sampling period for data acquisition (s)
tstep = 0.5 # Interval between PWM output step changes (s)
tstop = tstep * len(pwmvalue) # Total execution time (s)
vref = 3.3  # Reference voltage for the PWM and MCP3008

# Preallocating output arrays for plotting
t = []  # Time (s)
dacvalue = []  # Desired DAC output
adcvalue = []  # Measured DAC output

# Creating DAC PWM and ADC channel (using hardware implementations)
dac0 = PWMOutputDevice(12, frequency=pwmfreq)
adc0 = MCP3008(channel=0, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)

# Initializing timers and starting main clock
tprev = 0
tcurr = 0
tstart = time.perf_counter()

# initializing other variables used in the loop
count = 1  # PWM step counter
dacvaluecurr = pwmvalue[0]  # Initial DAC output value
dac0.value = dacvaluecurr  # Sending initial value to GPIO pin

# Running execution loop
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    # Updating PWM output every `tstep` seconds
    # with values from prescribed sequence
    if (np.floor(tcurr/tstep) - np.floor(tprev/tstep)) == 1:
        dacvaluecurr = pwmvalue[count]
        dac0.value = dacvaluecurr
        count += 1
    # Acquiring digital data every `tsample` seconds
    # and appending values to output arrays
    # (values are converted from normalized to 0 to Vref)
    if (np.floor(tcurr/tsample) - np.floor(tprev/tsample)) == 1:
        t.append(tcurr)
        dacvalue.append(vref*dacvaluecurr)
        adcvalue.append(vref*adc0.value)
    # Updating previous time and getting new current time (s)
    tprev = tcurr
    tcurr = time.perf_counter() - tstart

print('Done.')
# Releasing pins
dac0.value = 0
dac0.close()
adc0.close()

# Plotting results 
plot_line([t]*2, [dacvalue, adcvalue], yname='DAC Output (V)')
plot_line(t[1::], 1000*np.diff(t), yname='Sampling Period (ms)')