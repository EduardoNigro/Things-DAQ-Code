import numpy as np
import plotly.graph_objects as go
from scipy.stats import linregress


def define_data(x, y, xname=None, yname=None):
    """
    Creates dictionary containing data information.

    """
    if len(x) == len(y):
        data = {
            'xname': xname,
            'yname': yname,
            'x': x,
            'y': y,
        }
    else:
        raise Exception("'x' and 'y' must have the same length.")
    return data


def fit_data(data):
    """
    Calculates linear regression to data points.

    """
    f = linregress(data['x'], data['y'])
    fit = {
        'slope': f.slope,
        'intercept': f.intercept,
        'r2': f.rvalue**2
    }
    print('Slope = {:1.3f}'.format(fit['slope']))
    print('Intercept = {:1.3f}'.format(fit['intercept']))
    print('R-squared = {:1.3f}'.format(fit['r2']))
    return fit


def plot_data(data, fit):
    """
    Creates scatter plot of data and best fit regression line.

    """
    # Making sure x and y values are numpy arrays
    x = np.array(data['x'])
    y = np.array(data['y'])
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
            y=fit['slope']*x+fit['intercept'],
            mode='lines',
            line=dict(dash='dot', color='#202020')
        )
    )
    # Adding other figure objects
    fig.update_xaxes(title_text=data['xname'])
    fig.update_yaxes(title_text=data['yname'])
    fig.update_layout(
        paper_bgcolor='#F8F8F8',
        plot_bgcolor='#FFFFFF',
        width=600, height=300,
        margin=dict(l=60, r=30, t=30, b=30),
        showlegend=False)
    fig.show()
