% This m-file is called by the simulink model before running.
% You can find it's reference in ModelProperties/Callbacks

% Step input definition
TsSim = 1e-5;   % Simulation time step (s)
tTot = 1.0;     % Total simulation time
tStep = 0.0;    % Step time (s) 

% DC Motor parameters (Moog C23-L33-W10)
uStep = 70;         % Step input final value (%)
K = 0.0032;         % Torque sensitivity (N.m/%)
Beff = 0.0189;      % Effective damping (N.m/rad/s)
J0 = 0.0014;        % Motor moment of inertia (kg.m2)
Jm = 0.00034;       % Counter-weight moment of inertia (kg.m2)
Jeff = J0 + Jm;     % Effective inertia (kg.m2)
TqDist = 0.055;     % Disturbance Torque (N.m)

