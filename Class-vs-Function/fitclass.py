""" fitclass.py

Contains the class for the example on how to use a class.
https://thingsdaq.org/2022/02/23/classes-vs-functions-in-python/

fitfunctions.py has to be in a folder named modules, which has to in the
Python path or be the working folder.

Author: Eduardo Nigro
    rev 0.0.1
    2022-02-23

"""
import numpy as np
import plotly.graph_objects as go
from scipy.stats import linregress


class FitData:
    def __init__(self):
        """
        Class constructor.

        """
        self.data = dict()
        self.fit = dict()

    def define_data(self, x, y, xname=None, yname=None):
        """
        Creates dictionary containing data information.

        """
        if len(x) == len(y):
            self.data['x'] = x
            self.data['y'] = y
            self.data['xname'] = xname
            self.data['yname'] = yname
        else:
            raise Exception("'x' and 'y' must have the same length.")

    def fit_data(self):
        """
        Calculates linear regression to data points.

        """
        f = linregress(self.data['x'], self.data['y'])
        self.fit['slope'] = f.slope
        self.fit['intercept'] = f.intercept
        self.fit['r2'] = f.rvalue**2
        print('Slope = {:1.3f}'.format(self.fit['slope']))
        print('Intercept = {:1.3f}'.format(self.fit['intercept']))
        print('R-squared = {:1.3f}'.format(self.fit['r2']))

    def plot_data(self):
        """
        Creates scatter plot of data and best fit regression line.

        """
        # Making sure x and y values are numpy arrays
        x = np.array(self.data['x'])
        y = np.array(self.data['y'])
        # Creating plotly figure
        fig = go.Figure()
        # Adding data points
        fig.add_trace(
            go.Scatter(
                name='data',
                x=x,
                y=y,
                mode='markers',
                marker=dict(size=10, color='#FF0F0E')
            )
        )
        # Adding regression line
        fig.add_trace(
            go.Scatter(
                name='fit',
                x=x,
                y=self.fit['slope']*x+self.fit['intercept'],
                mode='lines',
                line=dict(dash='dot', color='#202020')
            )
        )
        # Adding other figure objects
        fig.update_xaxes(title_text=self.data['xname'])
        fig.update_yaxes(title_text=self.data['yname'])
        fig.update_layout(
            paper_bgcolor='#F8F8F8',
            plot_bgcolor='#FFFFFF',
            width=600, height=300,
            margin=dict(l=60, r=30, t=30, b=30),
            showlegend=False
        )
        fig.show()
