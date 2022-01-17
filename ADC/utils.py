""" utils.py 

Contains a useful plotting function that is used in the coding examples.
The function was built using Plotly instead of Matplotlib due to its
interactive graphs.

Author: Eduardo Nigro
    rev 0.0.5
    2021-12-26
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
    x, y, xname="Time (s)", yname=None, axes="single", marker=False, legend=None):
    """
    Plot lines using plotly.

    :param x: x values for plotting.
    :type x: list(float)

    :param y: y values for plotting.
    :type y: list(float)

    :param xname: The x axis title. Default value is ``'Time (s)'``.
    :type xname: str

    :param yname: The y axis title.
        A string or list of strings containing the names of the y axis titles.
        If ``None``, the y axis titles will be ``'y0'``, ``'y1'``, etc.
    :type yname: str, list(str)

    :param axes: The configuration of axis on the plot.
        If ``'single'``, multiple curves are plotted on the same axis.
        If ``'multi'``, each curve is plotted on its own axis.
    :type axes: str

    :param marker: Displays markers on the curves if ``True``.
    :type marker: bool

    :param legend: List of legend names for multiple curves.
        Length of `legend` must be the same as length of `y`.
    :type legend: list(str)


    """
    # Adjusting inputs
    if type(x) != list:
        x = [x]
    if type(y) != list:
        y = [y]
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
    # Checking for marker options
    if marker:
        mode = "lines+markers"
    else:
        mode = "lines"
    # Setting figure parameters
    m0 = 10
    margin = dict(l=6 * m0, r=3 * m0, t=3 * m0, b=3 * m0)
    wfig = 750
    hfig = 100 + 150 * naxes
    # Plotting results
    fig = make_subplots(rows=naxes, cols=1)
    for i, xi, yi, ynamei, legendi, color in zip(iaxes, x, y, yname, legend, colors):
        fig.add_trace(
            go.Scatter(
                x=xi,
                y=yi,
                name=legendi,
                mode=mode,
                line=dict(width=1, color=color),
                marker=dict(size=2, color=color),
            ),
            row=i + 1,
            col=1,
        )
        fig.update_yaxes(title_text=ynamei, row=i + 1, col=1)
        if xname.lower().find("angle") < 0:
            fig.update_xaxes(matches="x", row=i + 1, col=1)
        else:
            fig.update_xaxes(
                tickmode="array",
                tickvals=np.arange(0, np.round(xi[-1]) + 360, 360),
                matches="x",
                row=i + 1,
                col=1,
            )

    fig.update_xaxes(title_text=xname, row=i + 1, col=1)
    fig.update_layout(margin=margin, width=wfig, height=hfig, showlegend=showlegend)
    fig.show()
