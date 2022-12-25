""" post_linesensor_fit.py 

Uses keyestudio white LED KS0016 and photocell sensor KS0028

This code can be used to characterize a line tracking sensor made with the
two keyestudio components above.

For more details about the test setup go to my post:
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


# Defining data values `u` (sensor output) and `s` (bracket position)
# from sensor characterization test
u = [0.432,	0.448, 0.477, 0.547, 0.653, 0.800, 0.908, 0.933, 0.955]
s = [0, 2, 4, 6, 8, 10, 12, 14, 16]

# Fitting 3rd order polynomial to the data
p, stats = P.fit(u, s, 3, full=True)
# Evaluating polynomial for plotting
ui = np.linspace(0.45, 0.95, 100)
si = p(ui)
# Plotting data and fitted polynomial
ax = make_fig()
ax.set_xlabel('Sensor Output (u)', fontsize=12)
ax.set_ylabel('Position (mm)', fontsize=12)
ax.scatter(u, s)
ax.plot(ui, si, linestyle=':')

# Getting polynomial coefficients
c = p.convert().coef
# Calculating coefficients for transfer function
# (shift and offset representation)
k = c[3]
u0 = -c[2]/(3*k)
w = c[1] - 3*k*u0**2
s0 = c[0] + k*u0**3 + w*u0
# Defining transfer function for plotting
stf = k*(ui-u0)**3 + w*(ui-u0)
# Plotting transfer function
ax = make_fig()
ax.set_xlabel('Sensor Output (u)', fontsize=12)
ax.set_ylabel('Transfer Function Output (mm)', fontsize=12)
ax.plot(ui, stf)

# Calculating root mean squared error from residual sum of squares
rss = stats[0]
rmse = np.sqrt(rss[0]/len(s))
# Calculating R-square
r2 = 1 - rss[0]/np.sum((s-np.mean(s))**2)
# Displaying fit info
print('R-square = {:1.3f}'.format(r2))
print('RMSE (mm) = {:1.3f}'.format(rmse))
print('')
print('Shift (-) = {:1.3f}, Offset (mm) = {:1.3f}'.format(u0, s0))
