""" post_dac_input_output.py

Contains the DAC input-output example from my post:
https://thingsdaq.org/2022/02/02/digital-to-analog-conversion/

You can use this to simulate the input-output siganl relationship on a simple
low-pass filter DAC.

"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Creating general plotting function
def plot_general(x, y, x1=None, y1=None):
    # Creating Matplotlib figure
    fig = plt.figure(
        figsize=(6, 2.2),
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
fpwm = 20  # PWM frequency (Hz)
tpwm = 1/fpwm  # PWM period (s)
vref = 3.3  # Reference TTL voltage (V)
dutycycle = 0.25  # Duty cycle (0 to 1)

# First-order digital low-pass filter parameters
order = 1  # Filter order (number of cascaded first-order filters)
fc = 1  # Filter cutoff frequency (Hz) - Adjust this when changing order
# Creating digital filter and initial conditions state
# (Initial state is an approximation for cascaded filters
#  and will cause some initial oscillations for order > 1)
b, a = signal.butter(2, fc, fs=fs0)
zi = signal.lfilter_zi(b, a)

# Initializing output arrays
t = [0]
vin = [0]

# Creating PWM signal
tcurr = 0
while tcurr <= tstop:
    t.append(tcurr)
    if tcurr-tpwm*np.floor(tcurr/tpwm) < dutycycle*tpwm:
        vin.append(vref)
    else:
        vin.append(0)
    tcurr += Ts0

# Filtering output with non-zero initial conditions
vout, _ = signal.lfilter(b, a, vin, zi=zi*vref*dutycycle)
# Applying cascaded filtering
for _ in range(order-1):
    vout, _ = signal.lfilter(b, a, vout, zi=zi*vref*dutycycle)
    
# Plotting signals
plot_general(t, vin, t, vout)