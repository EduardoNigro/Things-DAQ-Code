% This m-file is called by the simulink model before running.
% You can find it's reference in ModelProperties/Callbacks

% Step input definition
TsSim = 1e-5;   % Simulation time step (s)
tTot = 0.5;     % Total simulation time
tStep = 0.1;    % Step time (s) 

% Motor option switch
Option = 1;

if Option == 1
    
    % DC Motor parameters (Moog C23-L33-W10)
    VStep = 12;         % Step input final value (V)
    Km = 0.0187;        % Torque sensitivity (N.m/A)
    Kb = 0.0191;        % Back EMF (V/rad/s)
    L = 0.35e-3;        % Terminal inductance (H)
    R = 0.6;            % Terminal resistance (Ohm)
    Jm = 1.554e-5;      % Rotor inertia (kg.m2)
    Bm = 1e-5;          % Damping factor (N.m/rad/s)
    TqDist = 0.05+0.02; % Disturbance Torque (N.m)

else
    
    % DC Motor parameters (Moog C42-L90-W30)
    VStep = 90;         % Step input final value (V)
    Km = 0.5791;        % Torque sensitivity (N.m/A)
    Kb = 0.5730;        % Back EMF (V/rad/s)
    L = 5.4e-3;         % Terminal inductance (H)
    R = 1.45;           % Terminal resistance (Ohm)
    Jm = 2.189e-3;      % Rotor inertia (kg.m2)
    Bm = 6.8e-4;        % Damping factor (N.m/rad/s)
    TqDist = 2.26+0.17; % Disturbance Torque (N.m)

end

% Displaying some motor parameters
disp(['Stall Current           (A) = ' num2str(VStep/R)])
disp(['Stall Torque          (N.m) = ' num2str(VStep/R*Km)])
disp(['Electric Time Const.   (ms) = ' num2str(1000*L/R)])
disp(['Mechanical Time Const. (ms) = ' num2str(1000*Jm/(Bm+Kb*Km/R))])

