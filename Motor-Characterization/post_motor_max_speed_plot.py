""" post_motor_max_speed_plot.py

Plots the data collected for the LEGO EV3 motor zero-load speed test.

Read more at:
http://thingsdaq.org/2022/08/26/dc-motor-characterization-2-of-2/

Author: Eduardo Nigro
    rev 0.0.1
    2022-08-26

"""
# Importing modules and classes
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Defining function to generate Matplotlib figure with axes
def make_fig():
    #
    # Creating figure
    fig = plt.figure(
        figsize=(5, 4.2),
        facecolor='#ffffff',
        tight_layout=True)
    # Adding and configuring axes
    ax = fig.add_subplot(
        facecolor='#ffffff',
        )
    ax.grid(
    linestyle=':',
    )
    # Returning axes handle
    return ax

# Assigning motor output levels for plotting
u = [40, 60, 80, 100]
# Assigning measured motor unloaded speed values
# - Each row correponds to a different motor
# - Each column corresponds to a different output level
speed = [
    [7.076, 10.578, 13.979, 17.343],
    [6.990, 10.469, 13.592, 17.003],
    [7.073, 10.555, 13.958, 17.453],
    [7.033, 10.450, 13.401, 17.148],
]

# Fitting stall torque data
ufit = np.array([0]+u)
speedfit = []
kfit = []
for si in speed:
    # Calculating linear regression
    fit = linregress(np.array(u), np.array(si))
    print('Slope (coeff[0]) = {:1.5f}'.format(fit.slope))
    print('R-squared = {:1.4f}'.format(fit.rvalue**2))
    # Appending speed constant values for current motor
    kfit.append(fit.slope)
    # Creating fitted output for plotting
    speedfit.append(fit.slope*ufit + fit.intercept)

# Displaying torque constant
print('')
print('Mean speed constant (rad/s/%) = {:1.4f}'.format(np.average(kfit)))

# Plotting data points and fitted curves
ax = make_fig()
ax.set_xlabel('Motor Output (%)', fontsize=12)
ax.set_ylabel('Zero Load Speed (rad/s)', fontsize=12)
for si, tifit in zip(speed, speedfit):
    ax.scatter(u, si)
    ax.plot(ufit, tifit, linestyle=':')

