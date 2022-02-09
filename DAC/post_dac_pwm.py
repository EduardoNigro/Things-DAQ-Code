""" post_dac_pwm.py

Contains the basic PWM signal example used in my post:
https://thingsdaq.org/2022/02/02/digital-to-analog-conversion/

You can use this to create a PWM pulse train.

Author: Eduardo Nigro
    rev 0.0.1
    2022-02-02

"""
import numpy as np
import matplotlib.pyplot as plt

# Creating general plotting function
def plot_general(x, y, x1=None, y1=None):
    # Creating Matplotlib figure
    fig = plt.figure(
        figsize=(6, 3),
        facecolor='#f8f8f8',
        edgecolor='#ffffff',
        linewidth=3,
        tight_layout=True)
    # Adding and confguring axes
    ax = fig.add_subplot(
        frameon=False,
        xlabel='Time (s)',
        ylabel='Amplitude (V)',
        )
    ax.set(
        ylim=(0, 4)
        )
    ax.grid(
        linestyle=':'
        )
    # Plotting signals
    if x1 is None:
        ax.plot(x, y, linewidth=1.5, color='#1f77b4')
    else:
        ax.plot(x, y, linewidth=1.5, label='Input', color='#1f77b4')
        ax.plot(x1, y1, linewidth=1.5, label='Output', color='#ff7f0e')
        ax.legend(loc='upper right')
        
# Creating time array for "continuous" signal
tstop = 1  # Signal duration (s)
Ts0 = 0.0005  # "Continuous" time step (s)
fs0 = 1/Ts0  # "Continuous" sampling frequency (Hz)
t = np.arange(0, tstop+Ts0, Ts0)

# Defining PWM parameters
fpwm = 10  # PWM frequency (Hz)
tpwm = 1/fpwm  # PWM period (s)
vref = 3.3  # Reference TTL voltage (V)
dutycycle = 0.25  # Duty cycle (0 to 1)

# Initializing output arrays
t = [0]
v = [0]

# Creating PWM signal
tcurr = 0
while tcurr <= tstop:
    t.append(tcurr)
    if tcurr-tpwm*np.floor(tcurr/tpwm) < dutycycle*tpwm:
        v.append(vref)
    else:
        v.append(0)
    tcurr += Ts0

# Plotting signal
plot_general(t, v)