% This m-file is called by the simulink model before running.
% You can find it's reference in ModelProperties/Callbacks

% Step input definition
TsSim = 1e-5;  % Simulation time step (s)
tTot = 1.0;  % Total simulation time
xStep = 10;  % Step input final value (rad/s)

% Discrete system parameters
Ts = 0.01;  % Sampling period (s)
AntiWindup = 0;  % Anti-windup flag (0: off, 1: on)

% DC Motor parameters
Km = 0.04;
Kb = 0.03;
L = 0.02;
R = 1;
Jm = 0.0015;
Bm = 0.01;

% PID gains
kp = 0.7; % 
ki = 5.7; % 
kd = 0.008; % 

% Saturation parameters
ka = 0.1;  % Continuous system dead-zone gain
umin = -12;  % Lower saturation limit
umax =  12;  % Upper saturation limit

% Discrete PID derivative term low-pass filter parameters
Taud = 0.01;  % Response time (s)
a1 = Taud/(Taud+Ts);  % y[n-1] coefficient
b0 = Ts/(Taud+Ts);  % x[n] coefficient

