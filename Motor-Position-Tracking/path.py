""" 
path.py contains functions for path calculation between two end points.
Three functions are defined based on the speed profile:
    * linear
    * quadratic
    * trigonometric

For more info, go to:
https://thingsdaq.org/2022/06/02/dc-motor-position-tracking/

Author: Eduardo Nigro
    rev 0.0.1
    2021-06-02

"""
import numpy as np

def path_linear(xstart, xstop, vmax, ta, nstep=1000):
    """
    Calculate linear velocity path.


    :param xstart: The starting point of the path.
    :type xstart: float

    :param xstop: The stopping point of the path.
    :type xstop: float

    :param vmax: The maximum allowed velocity.
    :type vmax: float

    :param ta: The acceleration and decelration times in seconds.
    :type ta: float

    :param nstep: The number of path discretization points.
    :type nstep: float


    Example:
        >>> from path import path_linear
        >>> t, x, v, a = path_linear(0, 1, 1, 0.4)

    """
    # Adjusting velocity based on end points
    if xstop < xstart:
        vmax = -vmax
    # Assigning time at max velocity
    if (xstop-xstart)/vmax > ta:
        # There's enough time for constant velocity section
        tmax = (xstop-xstart)/vmax - ta
    else:
        # There isn't (triangular velocity profile)
        tmax = 0
        vmax = (xstop-xstart)/ta
    # Assigning important time stamps
    t1 = ta  # End of acceleration section
    t2 = ta + tmax  # End of constant velocity section
    t3 = 2*ta + tmax  # End of motion (deceleration) section
    # Creating time array for path discretization
    t = np.linspace(0, t3, nstep+1)
    # Finding transition indices
    i1 = np.nonzero(t<=t1)
    i2 = np.nonzero((t>t1)&(t<=t2))
    i3 = np.nonzero(t>t2)
    # Calculating accelereration section array
    v1 = vmax/ta*t[i1]
    # Calculating constant velocity section array
    if len(i2[0]) > 0:
        v2 = np.array([vmax]*len(i2[0]))
    else:
        v2 = np.array([])
    # Calculating deceleration section array
    v3 = vmax - vmax/ta*(t[i3]-t2)
    # Concatenating arrays
    v = np.concatenate((v1, v2, v3))
    # Calculating numeric integral (position)
    x = xstart + t[-1]/nstep * np.cumsum(v)
    # Calculating numeric derivative (acceleration)
    a = np.gradient(v, t)
    # Returning time, position, velocity, and acceleration arrays
    return t, x, v, a

def path_quad(xstart, xstop, vmax, ta, nstep=1000):
    """
    Calculate quadratic velocity path.

    """
    # Adjusting velocity based on end points
    if xstop < xstart:
        vmax = -vmax
    # Assigning time at max velocity
    if (xstop-xstart)/vmax > 4/3*ta:
        # There's enough time for constant velocity section
        tmax = (xstop-xstart)/vmax - 4/3*ta
    else:
        # There isn't (triangular velocity profile)
        tmax = 0
        vmax = (xstop-xstart)/(4/3*ta)
    # Assigning important time stamps
    t1 = ta  # End of acceleration section
    t2 = ta + tmax  # End of constant velocity section
    t3 = 2*ta + tmax  # End of motion (deceleration) section
    # Creating time array for path discretization
    t = np.linspace(0, t3, nstep+1)
    # Finding transition indices
    i1 = np.nonzero(t<=t1)
    i2 = np.nonzero((t>t1)&(t<=t2))
    i3 = np.nonzero(t>t2)
    # Calculating accelereration section array
    v1 = (2*vmax/ta)*t[i1] - (2*vmax/ta)/(2*ta)*t[i1]**2
    # Calculating constant velocity section array
    if len(i2[0]) > 0:
        v2 = np.array([vmax]*len(i2[0]))
    else:
        v2 = np.array([])
    # Calculating deceleration section array
    v3 = vmax - (2*vmax/ta)/(2*ta)*(t[i3]-t2)**2
    # Concatenating arrays
    v = np.concatenate((v1, v2, v3))
    # Calculating numeric integral (position)
    x = xstart + t[-1]/nstep * np.cumsum(v)
    # Calculating numeric derivative (acceleration)
    a = np.gradient(v, t)
    # Returning time, position, velocity, and acceleration arrays
    return t, x, v, a

def path_trig(xstart, xstop, vmax, ta, nstep=1000):
    """
    Calculate trigonometric velocity path.

    """
    # Adjusting velocity based on end points
    if xstop < xstart:
        # There's enough time for constant velocity section
        vmax = -vmax
    # Assigning time at max velocity
    if (xstop-xstart)/vmax > ta:
        tmax = (xstop-xstart)/vmax - ta
    else:
        # There isn't (triangular velocity profile)
        tmax = 0
        vmax = (xstop-xstart)/ta
    # Assigning important time stamps
    t1 = ta  # End of acceleration section
    t2 = ta + tmax  # End of constant velocity section
    t3 = 2*ta + tmax  # End of motion (deceleration) section
    # Creating time array for path discretization
    t = np.linspace(0, t3, nstep+1)
    # Finding transition indices
    i1 = np.nonzero(t<=t1)
    i2 = np.nonzero((t>t1)&(t<=t2))
    i3 = np.nonzero(t>t2)
    # Calculating accelereration section array
    v1 = vmax/2*(1-np.cos(np.pi/ta*t[i1]))
    # Calculating constant velocity section array
    if len(i2[0]) > 0:
        v2 = np.array([vmax]*len(i2[0]))
    else:
        v2 = np.array([])
    # Calculating deceleration section array
    v3 = vmax/2*(1+np.cos(np.pi/ta*(t[i3]-t2)))
    # Concatenating arrays
    v = np.concatenate((v1, v2, v3))
    # Calculating numeric integral (position)
    x = xstart + t[-1]/nstep * np.cumsum(v)
    # Calculating numeric derivative (acceleration)
    a = np.gradient(v, t)
    # Returning time, position, velocity, and acceleration arrays
    return t, x, v, a
