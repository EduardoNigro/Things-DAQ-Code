""" post_ad_aliasing.py

Contains the aliasing example used in my post:
https://thingsdaq.org/2022/01/18/analog-to-digital-conversion/

You can use this to plot a sine wave and observe the effect of different
sampling frequencies in the resulting sampled signal.

"""
import numpy as np
import matplotlib.pyplot as plt

# Creating plotting function
def plot_general(x, y, x1=None, y1=None):
    # Creating Matplotlib figure
    fig = plt.figure(
        figsize=(12, 3),
        facecolor='#ffffff',
        edgecolor='#f8f8f8',
        linewidth=3,
        tight_layout=True)
    # Adding and confguring axes
    ax = fig.add_subplot()
    ax.set(
        xlabel='Time (s)',
        ylabel='Amplitude (V)',
        xlim=(0, max(x)),
        ylim=(-1.5, 1.5)
        )
    ax.grid(
        linestyle=':'
        )
    # Plotting signals
    if x1 is None:
        # Single "continuous" signal
        ax.plot(x, y, linewidth=1.5)
    else:
        # "Continuous" and sampled signals
        ax.plot(x, y, linewidth=1.5, color='#c0c0c0')
        ax.plot(x1, y1, linewidth=1.5, linestyle=':')
        ax.stem(x1, y1)

# Creating time array for "continuous" signal
tstop = 2  # Signal duration (s)
Ts0 = 0.0001  # "Continuous" time step
t = np.arange(0, tstop+Ts0, Ts0)

# Creating signal with a single sine wave
f0 = [20]  # Sine frequency (Hz)
a0 = [1]  # Sine amplitude
x = np.zeros(len(t))
for a, f in zip(a0, f0):
    x = x + a*np.sin(2*np.pi*f*t)

# Creating sampled signal
fs = 7  # Sampling frequency (Hz)
Ts = 1/fs  # Sampling period (s)
tprev = 0  # Previous time step
# Initializing sampled arrays
tsample = [0]
xsample = [0]
# Simulating a sampling execution loop
for tcurr, xcurr in zip(t, x):
    # Sampling data every `Ts` seconds
    if np.floor(tcurr/Ts) != np.floor(tprev/Ts):
        tsample.append(tcurr)
        xsample.append(xcurr)
    # Updating previous time step
    tprev = tcurr

# Displaying alias frequencies
print("Alias frequencies: {:1.2f}, {:1.2f}".
      format(np.mod(f0[0], fs), np.mod(-f0[0], fs)))

# Plotting results
plot_general(t, x)
plot_general(t, x, tsample, xsample)