""" post_ad_process.py

Contains the ADC steps used in my post:
https://thingsdaq.org/2022/01/17/analog-to-digital-conversion/

You can use this to plot an arbitrary continuous function composed of
multiple sine waves and the outcome of each step in the ADC process.

Author: Eduardo Nigro
    rev 0.0.1
    2022-01-17

"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

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

# Creating discrete signal plotting function
def plot_digital(z, ylabel=None):
    # Creating color map dictionary with only 2 colors
    cdict = {
        'red': ((0.0, 1.0, 1.0), (1.0, 0.121, 0.121)),
        'green': ((0.0, 1.0, 1.0), (1.0, 0.465, 0.465)),
        'blue': ((0.0, 1.0, 1.0), (1.0, 0.703, 0.703))
    }
    quantum = LinearSegmentedColormap('Quantum', cdict)
    # Creating Matplotlib figure
    fig = plt.figure(
        figsize=(6, 4),
        facecolor='#ffffff',
        edgecolor='#f8f8f8',
        linewidth=3,
        tight_layout=True)
    # Adding and confguring axes
    ax = fig.add_subplot()
    ax.set(
        ylim=(len(ylabel), 0)
        )
    ax.grid(
        linestyle=':'
        )
    ax.set_yticks(np.arange(-1,len(ylabel)+1), labels=['']+ylabel+[''])
    ax.invert_yaxis()
    # Plotting signal as a 2-D map
    ax.imshow(z, cmap=quantum)

# Creating time array for "continuous" signal
tstop = 2  # Signal duration (s)
Ts0 = 0.001  # "Continuous" time step
t = np.arange(0, tstop+Ts0, Ts0)

# Creating signal with multiple sine waves
f0 = [1, 1.5, 2.3]  # Sine frequencies (Hz)
a0 = [1, 0.2, 0.4]  # Sine amplitude
x = np.zeros(len(t))
for a, f in zip(a0, f0):
    x = x + a*np.sin(2*np.pi*f*t)

# Defining number of bits and reference voltage
nbits = 5
vref = 2
# Generating discrete signal y axis tick strings
nval = 2**nbits
fbit = '{:0'+str(nbits)+'b}'
sbit = [''] * (nval)
for i in [0, int(nval/2), nval-1]:
    sbit[i] = fbit.format(i)

# Creating sampled signal
xlo = -1.5  # Low end voltage (V)
xhi = 1.5  # High end voltage (V)
fs = 30  # Sampling frequency (Hz)
Ts = 1/fs  # Sampling period (s)
tprev = 0  # Previous time step
# Preallocating sampled arrays
tsample = []
xsample = []
xbit = []
xquant = []
# Simulating a sampling execution loop
for tcurr, xcurr in zip(t, x):
    # Sampling data every `Ts` seconds
    if np.floor(tcurr/Ts) != np.floor(tprev/Ts):
        # ADC sampling
        tsample.append(tcurr)
        xsample.append(xcurr)
        # ADC quantization
        xbit.append(np.round((xcurr-xlo)/((xhi-xlo)/nval)))
        xquant.append(xlo+(xhi-xlo)/nval*xbit[-1])
    # Updating previous time step
    tprev = tcurr

# Creating 2-D map representing discrete signal
X, Y = np.meshgrid(np.arange(0, len(tsample)+1), np.arange(0, nval+1))
Z = np.zeros(X.shape)
for i, val in enumerate(xbit):
    Z[int(val), i+1] = 1

# Plotting signals
plot_general(t, x)
plot_general(t, x, tsample, xsample)
plot_digital(Z, ylabel=sbit)
