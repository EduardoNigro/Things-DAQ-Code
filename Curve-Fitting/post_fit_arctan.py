""" post_fit_arctan.py 

This code shows how to fit an arctangent function to (x, y) data points.
There's also an option to use a logistics function, just for comparison.

For more details go to my post:
https://thingsdaq.org/2022/12/29/curve-fitting-with-tangent-and-inverse-tangent/

Author: Eduardo Nigro
    rev 0.0.1
    2022-12-29

"""
# Importing modules and classes
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Defining function to generate Matplotlib figure with axes
def make_fig():
    #
    # Creating figure
    fig = plt.figure(
        figsize=(5, 4.2),
        facecolor='#f8f8f8',
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

# Defining parametrized function options
# 0 -> arctangent
# 1 -> logistic
option = 0
if option == 0:
    def f(x, k, w, x0, y0):
        return k * np.arctan(w*(x-x0)) + y0
else:
    def f(x, k, w, x0, y0):
        return k/(1+np.exp(-w*(x-x0))) + y0

# Defining data points
xdata = [0, 2, 4, 6, 8, 10, 12, 14, 16]
ydata = [0.432, 0.448, 0.477, 0.547, 0.653, 0.800, 0.908, 0.933, 0.955]

# Estimating initial parameter values
p0 = [1, 1]
p0.append(0.5*(max(xdata)+min(xdata)))
p0.append(0.5*(max(ydata)+min(ydata)))
# Fitting data
output = curve_fit(f, xdata, ydata, p0=p0, full_output=True)
# Extracting relevant information from output
copt = output[0]
res = output[2]['fvec']
numeval = output[2]['nfev']
msg = output[3]

# Plotting data and fitted function
xi = np.linspace(min(xdata), max(xdata), 100)
yi = f(xi, *copt)
ax = make_fig()
ax.set_xlabel('x', fontsize=12)
ax.set_ylabel('y', fontsize=12)
ax.scatter(xdata, ydata)
ax.plot(xi, yi, linestyle=':')

# Calculating residual sum of squares (RSS)
rss = np.sum(res**2)
# Calculating root mean squared error (RMSE) from RSS
rmse = np.sqrt(rss/len(ydata))
# Calculating R-square
r2 = 1 - rss/np.sum((ydata-np.mean(ydata))**2)
# Displaying fit info
print('Found solution in {:d} function evaluations.'.format(numeval))
print(msg)
print('R-square = {:1.4f}, RMSE = {:1.4f}'.format(r2, rmse))
print('')
print('Coefficients:')
print('  k  = {:1.3f}'.format(copt[0]))
print('  w  = {:1.3f}'.format(copt[1]))
print('  x0 = {:1.3f}'.format(copt[2]))
print('  y0 = {:1.3f}'.format(copt[3]))
