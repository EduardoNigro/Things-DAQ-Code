""" post_digital_filtering_bandpass.py

Contains a first-order band-pass digital filter.
You can use this to understand the effects of filter parameters.

Read more at:
https://thingsdaq.org/2022/12/11/band-pass-filter/

Author: Eduardo Nigro
    rev 0.0.1
    2022-12-11

"""
# Importing modules and classes
import numpy as np
from utils import plot_line

# "Continuous" signal parameters
tstop = 20  # Signal duration (s)
Ts0 = 0.0002  # Time step (s)
fs0 = 1/Ts0  # Sampling frequency (Hz)
# Discrete signal parameters
tsample = 0.01  # Sampling period for code execution (s)
# Preallocating output arrays for plotting
tn = []
xn = []
yn = []

# Creating arbitrary signal with multiple sine functions
freq = [0.01, 0.5, 25]  # Sine frequencies (Hz)
ampl = [0.4, 1.0, 0.2]  # Sine amplitudes
t = np.arange(0, tstop+Ts0, Ts0)
xs = np.zeros(len(t))
for ai, fi in zip(ampl, freq):
    xs = xs + ai*np.sin(2*np.pi*fi*t)

# First order digital band-pass filter parameters
fc = np.array([0.1, 2])  # Band-pass cutoff frequencies (Hz)
tau = 1/(2*np.pi*fc)  # Filter time constants (s)
# Filter difference equation coefficients
a0 = tau[0]*tau[1]+(tau[0]+tau[1])*tsample+tsample**2
a1 = -(2*tau[0]*tau[1]+(tau[0]+tau[1])*tsample)
a2 = tau[0]*tau[1]
b0 = tau[0]*tsample
b1 = -tau[0]*tsample
# Defining normalized coefficients
a = np.array([1, a1/a0, a2/a0])
b = np.array([b0/a0, b1/a0])
# Initializing filter values
x = np.array([0.0]*(len(b)))  # x[n], x[n-1], x[n-2], ...
y = np.array([0.0]*(len(a)))  # y[n], y[n-1], y[n-2], ...

# Executing DAQ loop
tprev = 0
tcurr = 0
while tcurr <= tstop:
    # Doing I/O computations every `tsample` seconds
    if (np.floor(tcurr/tsample) - np.floor(tprev/tsample)) == 1:
        # Simulating DAQ device signal acquisition
        x[0] = xs[int(tcurr/Ts0)]
        # Filtering signal
        y[0] = -np.sum(a[1::]*y[1::]) + np.sum(b*x)
        # Updating previous input values
        for i in range(len(b)-1, 0, -1):
            x[i] = x[i-1]
        # Updating previous output values
        for i in range(len(a)-1, 0, -1):
            y[i] = y[i-1]
    # Updating output arrays
    tn.append(tcurr)
    xn.append(x[0])
    yn.append(y[0])
    # Incrementing time step
    tcurr += Ts0
    tprev = tcurr

# Plotting results
plot_line(
    [t, tn], [xs, yn], yname=['X Input', 'Y Output'],
    legend=['Raw', 'Filtered'], figsize=(1300, 250)
)
