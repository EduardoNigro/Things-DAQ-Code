""" post_linesensor_fit.py 

This code can be used to confirm the accuracy of the transfer function fitted
to test data obtained from the line sensor class.

For more details go to my post:
https://thingsdaq.org/2022/12/24/line-tracking-sensor-for-raspberry-pi/

Author: Eduardo Nigro
    rev 0.0.1
    2022-12-24

"""
# Importing modules and classes
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial as P

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


# Defining data values `s`` (bracket position) and `se` (estimated position)
# # from sensor confirmation test
s = np.array([0, 2, 4, 6, 8, 10, 12, 14, 16])
se = np.array([-1.0, 1.0, 4.2, 5.8, 7.8, 10.2, 13.1, 15.0, 16.1])

# Plotting data and fitted line
ax = make_fig()
ax.set_xlabel('Sensor Actual Position (u)', fontsize=12)
ax.set_ylabel('Sensor Measured Position (mm)', fontsize=12)
ax.scatter(s, se)
ax.plot([0, 16], [0, 16], linestyle=':')

# Calculating and displayin root mean squared error
rmse = np.sqrt(np.sum((s-se)**2)/len(se))
print('RMSE (mm) = {:1.3f}'.format(rmse))

