""" post_dac_pi_cal.py

Contains the modified code to calibrate a PWM-based DAC for Raspberry Pi.
https://thingsdaq.org/2022/02/08/dac-with-raspberry-pi/

You can use this to calibrate the output of the DAC.

Author: Eduardo Nigro
    rev 0.0.1
    2022-02-08
    
"""
import time
import numpy as np
from utils import plot_line
from gpiozero import PWMOutputDevice, MCP3008
from scipy.stats import linregress

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

# Defining analog output calibration parameters
ts = 0.25  # Sample collection start time after step event (s)
td = 0.20  # Sample collection duration (s)  
flagmeas = False  # Measurement enable flag
vmeas = []  # Measured output array of sample averages (V)

# Defining calibration flag and transfer function coefficients
# flagcal = True (calibration calculations are performed)
# flagcal = False (uses calibration coefficients from calibration)
flagcal = True
if flagcal:
    # Unit transfer function
    coeff = [1.0, 0.0]
else:
    # Put the coefficients from the calibration output here
    coeff = [1.0934, -0.0490]

# Initializing timers and starting main clock
tprev = 0
tcurr = 0
tstart = time.perf_counter()

# initializing other variables used in the loop
count = 1  # PWM step counter
dacvaluecurr = pwmvalue[0]  # Initial DAC output value
dac0.value = coeff[0]*dacvaluecurr+coeff[1]

# Running execution loop
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    # Updating PWM output every `tstep` seconds
    # with values from prescribed sequence
    if (np.floor(tcurr/tstep) - np.floor(tprev/tstep)) == 1:
        dacvaluecurr = pwmvalue[count]
        dac0.value = coeff[0]*dacvaluecurr+coeff[1]
        count += 1
    # Acquiring digital data every `tsample` seconds
    # and appending values to output arrays
    # (values are converted from normalized to 0 to Vref)
    if (np.floor(tcurr/tsample) - np.floor(tprev/tsample)) == 1:
        t.append(tcurr)
        dacvalue.append(vref*dacvaluecurr)
        adcvalue.append(vref*adc0.value)
    # Checking for calibration option
    if flagcal:
        # Starting sample collection `ts` seconds after step event
        if not flagmeas and (
            (np.floor((tcurr-ts)/tstep) - np.floor((tprev-ts)/tstep)) == 1):
            flagmeas = True
            vsample = []
        # Stopping sample collection `ts+td` seconds after step event
        # (Data is averaged here and stored in the `vmeas` array)
        if flagmeas and (
            (np.floor((tcurr-(ts+td))/tstep) - np.floor((tprev-(ts+td))/tstep)) == 1):
            flagmeas = False
            vmeas.append(np.median(np.array(vsample)))
        # Appending values to the sample collection array
        if flagmeas:
            vsample.append(adcvalue[-1])
    # Updating previous time and getting new current time (s)
    tprev = tcurr
    tcurr = time.perf_counter() - tstart

print('Done.')
# Releasing pins
dac0.value = 0
dac0.close()
adc0.close()

# Checking for calibration option
if flagcal:
    # Converting arrays (lists) to numpy arrays
    vmeas = np.array(vmeas)
    pwmvalue = np.array(pwmvalue)
    # Calculating linear regression
    fit = linregress(vmeas, vref*pwmvalue)
    print('Slope (coeff[0]) = {:1.4f}'.format(fit.slope))
    print('Intercept (coeff[1]) = {:1.4f}'.format(fit.intercept/vref))
    print('R-squared = {:1.4f}'.format(fit.rvalue**2))
    # Creating fitted output for plotting
    vfit = fit.slope*vmeas + fit.intercept

# Plotting results 
plot_line([t]*2, [dacvalue, adcvalue], yname='DAC Output (V)')
if flagcal:
    plot_line(
        [vmeas]*2, [vref*pwmvalue, vfit],
        line=[False, True], marker=[True, False],
        xname='Meas DAC Output (V)', yname='DAC Output (V)'
        )
else:
    plot_line([t[1::]], [1000*np.diff(t)], yname='Sampling Period (ms)')