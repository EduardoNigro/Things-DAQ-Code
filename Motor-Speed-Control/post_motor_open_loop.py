# Importing modules and classes
import time
import numpy as np
from scipy import signal
from utils import plot_line
from gpiozero_extended import Motor

# Creating time array for "continuous" signal
tstop = 2  # Signal duration (s)
tsample = 0.01  # Sampling period (s)
u0 = 0.5  # Motor step input amplitude

# First order filter parameters
tau = 0.1  # Response time (s)

# Creating motor object using GPIO pins 16, 17, and 18
# (using SN754410 quadruple half-H driver chip)
# Integrated encoder in on GPIO pins 24 and 25.
mymotor = Motor(
    enable1=16, pwm1=17, pwm2=18,
    encoder1=24, encoder2=25, encoderppr=300.8)
mymotor.reset_angle()

# Pre-allocating output arrays
t = []
w = []
wf = []

# Initializing previous and current values
ucurr = u0  # x[n] (step input)
wfprev = 0  # y[n-1]
wfcurr = 0  # y[n]

# Initializing variables and starting clock
thetaprev = 0
tprev = 0
tcurr = 0
tstart = time.perf_counter()

# Running motor sine wave output
print('Running code for', tstop, 'seconds ...')
while tcurr <= tstop:
    # Pausing for `tsample` to give CPU time to process encoder signal
    time.sleep(tsample)
    # Getting current time (s)
    tcurr = time.perf_counter() - tstart
    # Assigning motor sinusoidal output using the current time step
    mymotor.set_output(u0)
    # Calculating motor speed (rad/s)
    thetacurr = mymotor.get_angle()
    wcurr = np.pi/180 * (thetacurr-thetaprev)/(tcurr-tprev)
    # Filtering motor speed signal
    wfcurr = tau/(tau+tsample)*wfprev + tsample/(tau+tsample)*wcurr
    wfprev = wfcurr
    # Updating output arrays
    t.append(tcurr)
    w.append(wcurr)
    wf.append(wfcurr)
    # Updating previous values
    thetaprev = thetacurr
    tprev = tcurr

print('Done.')
# Stopping motor and releasing GPIO pins
mymotor.set_output(0, brake=True)
del mymotor

# Creating low-pass Butterworth filter
fc = 5  # Cutoff frequency (Hz)
b0, a0 = signal.butter(1, fc, fs=1/tsample)
# Doing basic phase-preserving digital filtering
wff = signal.filtfilt(b0, a0, w, method='gust')
# Estimating response time (s)
i63 = np.nonzero(wff >= 0.6321*np.max(wff))[0][0]
t63 = t[i63]
# Estimating steady-state gain for the last 0.5 s (rad/s/u)
k = np.mean(wff[-int(0.5/tsample)::])/u0

# Displaying results
print(t63, k)
# Plotting results
plot_line(
    [t]*2, [w, wff], marker=True, legend=['Raw', 'Filtered'],
    yname='Angular velocity (rad/s)')
plot_line(t[1::], 1000*np.diff(t), marker=True, yname='Sampling Period (ms)')