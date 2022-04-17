""" utils.py 

Contains a useful plotting function that is used in the coding examples.
The function was built using Plotly instead of Matplotlib due to its
interactive graphs and because it runs better on Raspberry Pi Linux.

Author: Eduardo Nigro
    rev 0.0.6
    2022-01-24
    
"""
import numpy as np
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Setting plotting modified template as default
mytemplate = pio.templates["plotly_white"]
mytemplate.layout["paper_bgcolor"] = "rgb(250, 250, 250)"
pio.templates.default = mytemplate


def plot_line(
    x, y, xname="Time (s)", yname=None, axes="single",
    figsize=None, line=True, marker=False, legend=None):
    """
    Plot lines using plotly.

    :param x: x values for plotting.
        List or ndarray. List of lists or ndarrays is also supported. 
    :type x: list(float), list(list), list(ndarray)

    :param y: y values for plotting.
        List or ndarray. List of lists or ndarrays is also supported. 
    :type y: list(float), list(list), list(ndarray)

    :param xname: The x axis title. Default value is ``'Time (s)'``.
        If ``'Angle (deg.)'`` is used, axes ticks are configured in 360 degree
        increments.
    :type xname: str

    :param yname: The y axis title.
        A string or list of strings containing the names of the y axis titles.
        If ``None``, the y axis titles will be ``'y0'``, ``'y1'``, etc.
    :type yname: str, list(str)

    :param axes: The configuration of axis on the plot.
        If ``'single'``, multiple curves are plotted on the same axis.
        If ``'multi'``, each curve is plotted on its own axis.
    :type axes: str

    :param figsize: The figure size (``width``, ``height``) in pixels.
    :type figsize: tuple(int)

    :param line: Displays the curves if ``True``.
    :type line: bool, list(bool)

    :param marker: Displays markers on the curves if ``True``.
    :type marker: bool, list(bool)

    :param legend: List of legend names for multiple curves.
        Length of `legend` must be the same as length of `y`.
    :type legend: list(str)

    Example:
        >>> import numpy as np
        >>> from utils import plot_line
        >>> t = np.linspace(0,2,100)
        >>> y0 = np.sin(1*np.pi*t)
        >>> y1 = np.cos(1*np.pi*t)    
        >>> plot_line(
                [t]*2, [y0, y1],
                yname=['sin & cos'],
                legend=['sin(pi x t)', 'cos(pi x t)']
                )
                
    """
    # Making sure x and y inputs are put in lists if needed
    if type(x) != list:
        x = [x]
    else:
        if type(x[0]) not in [list, np.ndarray]:
            x = [x]
    if type(y) != list:
        y = [y]
    else:
        if type(y[0]) not in [list, np.ndarray]:
            y = [y]
    # Doing a simple check for consistent x and y inputs
    if len(x) != len(y):
        raise Exception("'x' and 'y' inputs must have the same length.")
    # Adjusting y axis title based on input
    if not yname:
        yname = ["y" + str(i) for i in range(len(y))]
    elif type(yname) != list:
        yname = [yname]
    if (len(yname) == 1) and (len(y) > 1):
        yname = yname * len(y)
    # Setting legend display option
    if legend is not None:
        if len(legend) == len(y):
            showlegend = True
        else:
            raise Exception("'y' and 'legend' must have the same length.")
    else:
        showlegend = False
        legend = [None] * len(y)
    # Checking for single (with multiple curves)
    # or multiple axes with one curve per axes
    if axes == "single":
        naxes = 1
        iaxes = [0] * len(y)
        colors = [
            "#1F77B4",
            "#FF7F0E",
            "#2CA02C",
            "#D62728",
            "#9467BD",
            "#8C564B",
            "#E377C2",
            "#7F7F7F",
            "#BCBD22",
            "#17BECF",
        ]
    elif axes == "multi":
        naxes = len(y)
        iaxes = range(0, len(y))
        colors = ["rgb(50, 100, 150)"] * len(y)
    else:
        raise Exception("Valid axes options are: 'single' or 'multi'.")
    # Checking for line and marker options
    if type(line) != list:
        line = [line] * len(y)
    if type(marker) != list:
        marker = [marker] * len(y)
    mode = []
    markersize = []
    for linei, markeri in zip(line, marker):
        if linei and markeri:
            mode.append("lines+markers")
            markersize.append(2)
        elif linei and not markeri:
            mode.append("lines")
            markersize.append(2)
        elif not linei and markeri:
            mode.append("markers")
            markersize.append(8)
    # Setting figure parameters
    if figsize:
        wfig, hfig = figsize
    else:
        wfig = 650
        hfig = 100 + 150*naxes
    m0 = 10
    margin = dict(l=6 * m0, r=3 * m0, t=3 * m0, b=3 * m0)
    # Plotting results
    fig = make_subplots(rows=naxes, cols=1)
    for i, xi, yi, ynamei, legendi, colori, modei, markersizei in zip(
            iaxes, x, y, yname, legend, colors, mode, markersize):
        # Adding x, y traces to appropriate plot
        fig.add_trace(
            go.Scatter(
                x=xi,
                y=yi,
                name=legendi,
                mode=modei,
                line=dict(width=1, color=colori),
                marker=dict(size=markersizei, color=colori),
            ),
            row=i + 1,
            col=1,
        )
        # Adding x axes ticks
        if xname.lower().find("angle") < 0:
            # Regular x axes
            fig.update_xaxes(matches="x", row=i + 1, col=1)
        else:
            # Special case where x axes has angular values
            fig.update_xaxes(
                tickmode="array",
                tickvals=np.arange(0, np.round(xi[-1]) + 360, 360),
                matches="x",
                row=i + 1,
                col=1,
            )
        # Adding y axis title to all plots
        fig.update_yaxes(title_text=ynamei, row=i + 1, col=1)
    # Adding x axis title to bottom plot only
    fig.update_xaxes(title_text=xname, row=i + 1, col=1)
    # Applying figure size, margins, and legend
    fig.update_layout(
        margin=margin, width=wfig, height=hfig, showlegend=showlegend)
    fig.show()
