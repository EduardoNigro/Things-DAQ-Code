""" post_event_detection_trigger.py

Contains a usage example of find_cluster for trigger detection.

Read more at:
https://thingsdaq.org/2022/06/21/event-detection-in-signal-processing/

Author: Eduardo Nigro
    rev 0.0.1
    2022-06-21

"""
import numpy as np
import matplotlib.pyplot as plt
from utils import find_cluster

def make_fig():
    #
    # Creating Matplotlib figure
    fig = plt.figure(
        figsize=(6.3, 2.4),
        facecolor='#f8f8f8',
        tight_layout=True)
    # Adding and configuring axes
    ax = fig.add_subplot(
        xlim=(0, max(t)),
        xlabel='Time (s)',
        )
    ax.grid(linestyle=':')
    # Returning axes handle
    return ax

# Creating time array for "continuous" signal
tstop = 1  # Signal duration (s)
Ts0 = 0.0005  # "Continuous" time step (s)
fs0 = 1/Ts0  # "Continuous" sampling frequency (Hz)
t = np.arange(0, tstop+Ts0, Ts0)

# Defining PWM parameters
fpwm0 = 10  # PWM frequency (Hz)
tpwm0 = 1/fpwm0  # PWM period (s)
xref = 3.3  # Reference high value

dutycycle = 0.2
a0 = 0.1
f0 = 1
n0 = 0.1

# Initializing output arrays
t = [0]
x = [0]

# Creating PWM signal with variable pulse width
tcurr = 0
while tcurr <= tstop:
    tpwm = tpwm0*(1+a0*np.sin(2*np.pi*f0*tcurr))
    xnoise = n0*(np.random.random()-0.5)
    if tcurr-tpwm*np.floor(tcurr/tpwm) > (1-dutycycle)*tpwm:
        x.append(xref+xnoise)
    else:
        x.append(xnoise)
    tcurr += Ts0
    t.append(tcurr)

t = np.array(t)
x = np.array(x)

# Calculating and normalizing trigger signal derivative
dxdt = np.gradient(x, t)
dxdt = dxdt/np.max(dxdt)

# Finding trigger event times
icl, ncl = find_cluster(dxdt>0.5, 1)
ttrigger = t[icl]

ax = make_fig()
ax.set_ylabel('Trigger signal (V)')
ax.plot(t, x, linewidth=1.5, color='#1f77b4', zorder=0)
for ik, nk in zip(icl, ncl):
    ax.plot(t[ik:ik+nk], x[ik:ik+nk], color='#aa0000')
    ax.scatter(t[ik+1], x[ik+1], s=25, c='#aa0000')

ax = make_fig()
ax.set_ylabel('Normalized Derivative ( - )')
ax.plot(t, dxdt, linewidth=1.5, color='#1f77b4', zorder=0)
for ik, nk in zip(icl, ncl):
    ax.plot(t[ik:ik+nk], dxdt[ik:ik+nk], color='#aa0000')
