""" post_example_class.py

Contains the basic code for an example on how to use a class.
https://thingsdaq.org/2022/02/23/classes-vs-functions-in-python/

fitclass.py has to be in a folder named modules, which has to in the
Python path or be the working folder.

Author: Eduardo Nigro
    rev 0.0.1
    2022-02-23

"""
from modules.fitclass import FitData

# Creating class instances
fitdata1 = FitData()
fitdata2 = FitData()

# Defining first data set
x1 = [0, 1, 2, 3, 4]
y1 = [2.1, 2.8, 4.2, 4.9, 5.1]
fitdata1.define_data(x1, y1, xname='x1', yname='y1')
# Fitting data
fitdata1.fit_data()
# Plotting results
fitdata1.plot_data()

# Defining second data set
x2 = [0, 1, 2, 3, 4]
y2 = [3, 5.1, 6.8, 8.9, 11.2]
fitdata2.define_data(x2, y2, xname='x2', yname='y2')
# Fitting data
fitdata2.fit_data()
# Plotting results
fitdata2.plot_data()
