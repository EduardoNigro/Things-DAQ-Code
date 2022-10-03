""" post_motor_torque_speed_curves.py

Generates a graph of typical torque-speed curves for a DC motor.

Read more at:
http://thingsdaq.org/2022/08/26/dc-motor-characterization-2-of-2/

Author: Eduardo Nigro
    rev 0.0.1
    2022-08-26

"""
# Importing modules and classes
import matplotlib.pyplot as plt

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
    # Returning axes handle
    return ax

# Defining arbitrary motor parameters
torque = [0.13, 0.2, 0.27, 0.34]
speed = [7.03, 10.81, 14.59, 18.38]
u = [40, 60, 80, 100]

# Defining custom axis labels
xlabel = ['N'+str(ui) for ui in u]
ylabel = ['T'+str(ui) for ui in u]

# Generating torque-speed curves
x = []
y = []
for ti, si in zip(torque, speed):
    x.append([si, 0])
    y.append([0, ti])

# Plotting curves
ax = make_fig()
ax.set_xticks(speed, labels=xlabel)
ax.set_yticks(torque, labels=ylabel)
ax.set_xlabel('Speed', fontsize=12)
ax.set_ylabel('Torque', fontsize=12)
ax.set_xlim((0, 20))
ax.set_ylim((0, 0.4))
for xi, yi in zip(x, y):
    ax.plot(xi, yi, linewidth=1.5, color='#1f77b4', zorder=0)

