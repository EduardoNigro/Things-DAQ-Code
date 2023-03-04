# Things DAQ

This repository contains the Python code used throughout the posts in my blog
[Things DAQ](https://thingsdaq.org/).

## Posts with code
This is a living list and it is updated as posts containing example code are created:
GitHub Folder | Things DAQ Post
------------- | ---------------
Pulse-Rate-Monitor | [Pulse Rate Monitor with Raspberry Pi](https://thingsdaq.org/2023/03/03/pulse-rate-monitor-with-raspberry-pi/)
thingsdaq | [Python Modules and Packages](https://thingsdaq.org/2023/01/29/python-modules-and-packages/)
LED Dimmer | [LED Dimmer with Raspberry Pi](https://thingsdaq.org/2023/01/16/led-dimmer-with-raspberry-pi/)
Curve Fitting | [Curve Fitting with Tangent and Inverse Tangent](https://thingsdaq.org/2022/12/29/curve-fitting-with-tangent-and-inverse-tangent/)
Line Sensor | [Line Tracking Sensor for Raspberry Pi](https://thingsdaq.org/2022/12/24/line-tracking-sensor-for-raspberry-pi/)
Joystick | [Joystick with Raspberry Pi](https://thingsdaq.org/2022/11/24/joystick-with-raspberry-pi/)
Ultrasonic-Sensor | [Ultrasonic Sensor with Raspberry Pi](https://thingsdaq.org/2022/11/04/ultrasonic-sensor-with-raspberry-pi/)
Temperature-Sensor | [Temperature Sensor with Raspberry Pi](https://thingsdaq.org/2022/10/15/temperature-sensor-with-raspberry-pi/)
LED-Display | [7-Segment LED Display with Raspberry Pi](https://thingsdaq.org/2022/10/02/7-segment-led-display-with-raspberry-pi/)
Motor-Characterization | [DC Motor Characterization](https://thingsdaq.org/2022/07/05/dc-motor-characterization-1-of-2/)
Event-Detection | [Event Detection in Signal Processing](https://thingsdaq.org/2022/06/21/event-detection-in-signal-processing/)
Motor-Position-Tracking | [DC Motor Position Tracking](https://thingsdaq.org/2022/06/02/dc-motor-position-tracking/)
Motor-Position-Control | [Motor Position Control with Raspberry Pi](https://thingsdaq.org/2022/05/15/motor-position-control-with-raspberry-pi/)
Motor-Speed-Control | [Motor Speed Control with Raspberry Pi](https://thingsdaq.org/2022/04/17/motor-speed-control-with-raspberry-pi/)
Digital-PID | [Digital PID Controller](https://thingsdaq.org/2022/04/07/digital-pid-controller/)
Digital-Filtering | [Digital Filtering](https://thingsdaq.org/2022/03/23/digital-filtering/)
DAC-Class | [Python DAC Class](https://thingsdaq.org/2022/03/17/python-dac-class/)
Encoder-Pi | [Encoder with Raspberry Pi](https://thingsdaq.org/2022/03/09/encoder-with-raspberry-pi/)
H-Bridge-Pi | [H-Bridge and DC Motor with Raspberry Pi](https://thingsdaq.org/2022/03/01/h-bridge-and-dc-motor-with-raspberry-pi/)
Class-vs-Function | [Classes vs. Functions in Python](https://thingsdaq.org/2022/02/23/classes-vs-functions-in-python/)
DAC-Pi | [DAC with Rapsberry Pi](https://thingsdaq.org/2022/02/08/dac-with-raspberry-pi/)
DAC | [Digital-to-Analog Conversion](https://thingsdaq.org/2022/02/02/digital-to-analog-conversion/)
MCP3008-Pi | [MCP3008 with Raspberry Pi](https://thingsdaq.org/2022/01/24/mcp3008-with-raspberry-pi/)
ADC | [Analog-to-Digital Conversion](https://thingsdaq.org/2022/01/17/analog-to-digital-conversion/)
Prescribed-PWM | [Prescribed PWM duty cycle](https://thingsdaq.org/2022/01/02/prescribed-pwm-duty-cycle/)


## Important note:
I use two plotting libraries in my code examples: ***matplotlib*** and ***plotly***

One way I got them to work with the right ***numpy*** version was running the following
commands in a Pi terminal:

```
sudo apt update
```
```
sudo apt remove python3-numpy
```
```
sudo apt-get install libatlas-base
```
```
sudo apt install python3-matplotlib
```
```
sudo apt install python3-plotly
```

- Installing ***matlplotlib*** will automatically install the right ***numpy*** version.
- To my understanding, ***libatlas-base*** insures compatiblity with the Pi-based ***numpy*** installation.
