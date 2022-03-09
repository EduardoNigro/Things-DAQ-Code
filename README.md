# Things DAQ

This repository contains the Python code used throughout the posts in my blog
[Things DAQ](https://thingsdaq.org/).

## Posts with code
This is a living list and it is updated as posts containing example code are created:
GitHub Folder | Things DAQ Post
------------- | ---------------
Encoder-Pi | [Encoder with Raspberry Pi](https://thingsdaq.org/2022/03/09/encoder-with-raspberry-pi/)
H-Bridge-Pi | [H-Bridge and DC Motor with Raspberry Pi](https://thingsdaq.org/2022/03/01/h-bridge-and-dc-motor-with-raspberry-pi/)
Class-vs-Function | [Classes vs. Functions in Python](https://thingsdaq.org/2022/02/23/classes-vs-functions-in-python/)
DAC-Pi | [DAC with Rapsberry Pi](https://thingsdaq.org/2022/02/08/dac-with-raspberry-pi/)
DAC | [Digital-to-Analog Conversion](https://thingsdaq.org/2022/02/02/digital-to-analog-conversion/)
MCP3008-Pi | [MCP3008 with Raspberry Pi](https://thingsdaq.org/2022/01/24/mcp3008-with-raspberry-pi/)
ADC | [Analog-to-Digital Conversion](https://thingsdaq.org/2022/01/17/analog-to-digital-conversion/)
Prescribed-PWM | [Prescribed PWM duty cycle](https://thingsdaq.org/2022/01/02/prescribed-pwm-duty-cycle/)


## Important note:
In case the Raspberry Pi doesn't recognize the correct numpy package, you might have to install it:

```
sudo pip3 install numpy
```

Since that may conflict with the pre-installed version of numpy, you might have to run
the following installation after installing numpy:

```
sudo apt-get install libatlas-base-dev
```

