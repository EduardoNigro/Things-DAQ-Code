""" post_pwm_step_fig.py

Contains the PWM input outpu signal generation for a step sequence
https://thingsdaq.org/2022/01/02/prescribed-pwm-duty-cycle/

I used this to create the graph on the post featured image!

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
        xlabel='Time (s)',
        ylabel='Amplitude (V)',
        )
    ax.grid(
        linestyle=':'
        )
    # Plotting signals
    if x1 is None:
        ax.plot(x, y, linewidth=1.5, color='#1f77b4')
    else:
        ax.plot(x, y, linewidth=1.5, label='Input', color='#1f77b4')
        ax.plot(x1, y1, linewidth=2.5, label='Output', color='#ff7f0e')
        ax.legend(loc='upper left')

# Assigning parameter values
vref = 3.3  # Reference TTL voltage (V)
pwmfreq = 10  # PWM frequency (Hz)
pwmvalue = [0.5, 0.8]
tpwm = 1/pwmfreq  # PWM period (s)
tstep = 1.0  # Interval between step changes (s)
tsample = 0.0005  # Sampling period for code execution (s)
tstop = tstep * (len(pwmvalue)+1)  # Total execution time (s)

# Initializing output arrays
t = [0]
vin = [0]
value = [0.2]

# Running execution loop
count = 0
tprev = 0
tcurr = 0
valuecurr = value[0]
while tcurr <= tstop:
    # Appending current values to output arrays
    t.append(tcurr)
    value.append(valuecurr)
    # Updating PWM pulse train signal
    if tcurr-tpwm*np.floor(tcurr/tpwm) < valuecurr*tpwm:
        vin.append(vref)
    else:
        vin.append(0)
    # Updating PWM output every `tstep` seconds
    # with values from prescribed sequence
    if (np.floor(tcurr/tstep) - np.floor(tprev/tstep)) == 1:
        valuecurr = pwmvalue[count]
        count += 1
    # Updating previous and current times (s)
    tprev = tcurr
    tcurr += tsample

# Plotting signals
plot_general(t, vin, t, vref*np.array(value))
