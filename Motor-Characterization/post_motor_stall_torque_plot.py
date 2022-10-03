""" post_motor_stall_torque_plot.py

Plots the data collected for the LEGO EV3 motor stall test, using a linear
force gauge.

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
# Assigning measured motor stall torque values
# - Each row correponds to a different motor
# - Each column corresponds to a different output level
torque = [
    [0.130, 0.196, 0.261, 0.319],
    [0.136, 0.203, 0.267, 0.329],
    [0.138, 0.207, 0.270, 0.333],
    [0.131, 0.200, 0.262, 0.326],
]

# Fitting stall torque data
ufit = np.array([0]+u)
torquefit = []
kfit = []
# Looping through different motors
for ti in torque:
    # Calculating linear regression
    fit = linregress(np.array(u), np.array(ti))
    print('Slope (coeff[0]) = {:1.5f}'.format(fit.slope))
    print('R-squared = {:1.4f}'.format(fit.rvalue**2))
    # Appending torque constant values for current motor
    kfit.append(fit.slope)
    # Creating fitted output for plotting
    torquefit.append(fit.slope*ufit + fit.intercept)

# Displaying torque constant
print('')
print('Mean torque constant (N.m/%) = {:1.4f}'.format(np.average(kfit)))

# Plotting data points and fitted curves
ax = make_fig()
ax.set_xlabel('Motor Output (%)', fontsize=12)
ax.set_ylabel('Stall Torque (N.m)', fontsize=12)
for ti, tifit in zip(torque, torquefit):
    ax.scatter(u, ti)
    ax.plot(ufit, tifit, linestyle=':')

