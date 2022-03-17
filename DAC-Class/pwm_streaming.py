""" pwm_streaming.py

Collects Raspberry Pi DAC data using streaming. 

Author: Eduardo Nigro
    rev 0.0.1
    2022-03-17

"""
import time
import numpy as np
from labjack_unified.utils import plot_line
from labjack_unified.devices import LabJackU3

# Assigning streaming parameters
samplerate = 50000 # Samples/s
readrate = 0.5 # Block size (s)
nblocks = 10 # Number of acquired blocks
portlist = ['AIN0']
# Creating array with dummy values to enable concatenation
data = np.zeros((1, len(portlist)))

# Configuring and starting streaming
lj = LabJackU3()
lj.set_stream(portlist, scanrate=samplerate, readrate=readrate)
# Waiting for first block to become available
time.sleep(readrate)
# Executing acquisition loop
for i in range(nblocks):
    # Starting computational overhead time watch
    t0 = time.time()
    # Getting one block of data
    dt, datablock, numscans, commbacklog, U3backlog = lj.get_stream()
    # Concatenating new data
    data = np.vstack((data, datablock))
    # Showing statistics
    print('Block :', i+1)
    print('Scans :', numscans)
    print('Comm Backlog : {:0.1f}'.format(commbacklog))
    print('U3 Backlog   : {:0.1f}'.format(U3backlog))
    # Pausing taking into account computation overhead
    thead = time.time()-t0
    time.sleep(readrate-thead)
# Stopping streaming
lj.stop_stream()
# Closing LabJack
lj.close()
del lj

# Removing first row of dummy data
data = data[1::, :]
# Creating time array
t = dt * np.linspace(0, data.shape[0]-1, data.shape[0])
# Setting x and y arrays for plotting
naxes = len(portlist)
x = [t] * naxes
y = [data[:, i] for i in range(naxes)]
# Plotting results
plot_line(x, y, yname=portlist, axes='multi', figsize=(1000, 350))
