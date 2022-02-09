""" post_ad_quantization.py

Contains the quantization example used in my post:
https://thingsdaq.org/2022/01/17/analog-to-digital-conversion/

You can use this to plot the transfer function of an ADC with different bit
resolutions.

Author: Eduardo Nigro
    rev 0.0.1
    2022-01-17

"""
import numpy as np
import matplotlib.pyplot as plt

# Creating plotting function
def plot_tf(x, xtick=None, xlabel=None, ylabel=None):
    # Creating Matplotlib figure
    fig = plt.figure(
        figsize=(5, 4.2),
        facecolor='#ffffff',
        edgecolor='#f8f8f8',
        linewidth=3,
        tight_layout=True)
    # Adding and confguring axes
    ax = fig.add_subplot(
        frameon=False,
        xlabel='Analog Input (V)',
        ylabel='Digital Output Code'
        )
    ax.set(
        xlim=(0, max(x)),
        ylim=(1, len(ylabel))
        )
    ax.grid(
        linestyle=':',
        )
    ax.set_xticks(xtick, labels=xlabel)
    ax.set_yticks(np.arange(len(ylabel))+1, labels=ylabel)
    # Plotting ideal ADC transfer function
    ax.plot([0, xtick[-2]], [1, len(x)-1], linewidth=1.5, linestyle='--', color='#303030')
    # Plotting perfect ADC transfer function
    ax.step(x, np.arange(len(x)), linewidth=3)

# Defining number of bits and reference voltage
# (Transfer function for a single-ended perfect ADC)
nbits = 4
vref = 2
# Generating y axis tick strings
nval = 2**nbits
fbit = '{:0'+str(nbits)+'b}'
sbit = [fbit.format(n) for n in range(nval)]

# Perfect ADC (single-ended mode) analog inputs (x axis)
v = np.linspace(0, vref, nval+1)
vtick = v
# Perfect ADC (single-ended mode with adjusted quantization)
v = v - 0.5*np.diff(v)[0]
v[-1] = v[-1] + 0.5*np.diff(v)[0]
# Creating x axis tick strings
sref = []
for i, tick in enumerate(vtick):
    if np.mod(i, 2) == 0:
        sref.append(str(tick))
    else:
        sref.append('')
# Plotting transfer function
plot_tf(v, xtick=vtick, xlabel=sref, ylabel=sbit)
