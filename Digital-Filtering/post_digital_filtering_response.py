""" post_digital_filtering_response.py

Creates the step response of a digital low pass filter.
I use the backward difference approximation for the discretization.

Read more at:
https://thingsdaq.org/2022/03/23/digital-filtering/

Author: Eduardo Nigro
    rev 0.0.1
    2022-03-23

"""
import numpy as np
import matplotlib.pyplot as plt

# Creating time array for "continuous" signal
tstop = 1  # Signal duration (s)
Ts0 = 0.001  # "Continuous" time step (s)
Ts = 0.02  # Sampling period (s)
t = np.arange(0, tstop+Ts0, Ts0)

# First order continuous system response to unit step input
tau = 0.1  # Response time (s)
y = 1 - np.exp(-t/tau)  # y(t)

# Preallocating signal arrays for digital filter
tf = []
yf = []

# Initializing previous and current values
xcurr = 1  # x[n] (step input)
yfprev = 0  # y[n-1]
yfcurr = 0  # y[n]

# Executing 
tprev = 0
tcurr = 0
while tcurr <= tstop:
    # Doing filter computations every `Ts` seconds
    if (np.floor(tcurr/Ts) - np.floor(tprev/Ts)) == 1:
        yfcurr = tau/(tau+Ts)*yfprev + Ts/(tau+Ts)*xcurr
        yfprev = yfcurr
    # Updating output arrays
    tf.append(tcurr)
    yf.append(yfcurr)
    # Updating previous and current "continuous" time steps
    tprev = tcurr
    tcurr += Ts0

# Creating Matplotlib figure
fig = plt.figure(
    figsize=(6.3, 2.8),
    facecolor='#f8f8f8',
    tight_layout=True)
# Adding and configuring axes
ax = fig.add_subplot(
    xlim=(0, max(t)),
    xlabel='Time (s)',
    ylabel='Output ( - )',
    )
ax.grid(linestyle=':')
# Plotting signals
ax.plot(t, y, linewidth=1.5, label='Continuous', color='#1f77b4')
ax.plot(tf, yf, linewidth=1.5, label='Discrete', color='#ff7f0e')
ax.legend(loc='lower right')

