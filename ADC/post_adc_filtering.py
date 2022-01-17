""" post_ad_filtering.py

Contains a low-pass digital filter.

You can use this to understand the effects of a Butterworth filter.

"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Creating general plotting function
def plot_general(x, y, x1=None, y1=None):
    # Creating Matplotlib figure
    fig = plt.figure(
        figsize=(6, 3),
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
        ax.stem(x1, y1)

# Creating time array for "continuous" signal
tstop = 2  # Signal duration (s)
Ts0 = 0.001  # "Continuous" time step (s)
fs0 = 1/Ts0  # "Continuous" sampling frequency (Hz)
t = np.arange(0, tstop+Ts0, Ts0)

# Creating signal with multiple sine waves
f0 = [1, 1.5, 2.3]  # Sine frequencies (Hz)
a0 = [1, 0.2, 0.4]  # Sine amplitude
x = np.zeros(len(t))
for a, f in zip(a0, f0):
    x = x + a*np.sin(2*np.pi*f*t)

# Adding somewhat random noise to the signal
kn = 10  # Frequency multiplier
xn = x  # Assigning base signal
for _ in range(20):
    c = np.random.random(3)
    xn = xn + 0.02*c[0]*np.sin(2*np.pi*(kn*(f0[0]+kn*c[1]))*t + c[2])

# Doing phase-preserving digital filtering
fc = 10  # Low-pass cutoff frequency (Hz)
b, a = signal.butter(1, fc, fs=fs0)
xf = signal.filtfilt(b, a, xn, method='gust')

# Plotting signals
plot_general(t, xn)
plot_general(t, xf)
