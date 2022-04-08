% This m-file is called by the simulink model after running.
% You can find it's reference in ModelProperties/Callbacks

% Deleting figures
delete(get(0,'Children'));
ScrSize = get(0,'ScreenSize');

% Plotting analog system response
wfig = 500;
hfig = 250;
Fig1 = figure('Position',[(ScrSize(3)-wfig)/2-wfig/2 (ScrSize(4)-hfig)/2+hfig/2+30 wfig hfig]);
axes(Fig1,...
    'Position',[0.1 0.16 0.84 0.74],...
    'YLim',[0 12],...
    'XGrid','on',...
    'YGrid','on',...
    'FontName','Arial',...
    'FontSize',10,...
    'NextPlot','add');
Curve = plot(tout, xSP);
Curve.Color = [0.1 0.1 0.1];
Curve = plot(tout, xOL);
Curve.Color = [0.122 0.467 0.706];
Curve.LineWidth = 1;
Curve = plot(tout, xCL);
Curve.Color = [1 0.498 0.055];
Curve.LineWidth = 1;
xlabel('Time (s)')
ylabel('Motor Speed (rad/s)')
legend('Step Input','Open-Loop','Closed-Loop','Location','SouthEast');

% Plotting analog system / digital controller response
Fig2 = figure('Position',[(ScrSize(3)-wfig)/2+wfig/2 (ScrSize(4)-hfig)/2+hfig/2+30 wfig hfig]);
axes(Fig2,...
    'Position',[0.1 0.16 0.84 0.74],...
    'YLim',[0 12],...
    'XGrid','on',...
    'YGrid','on',...
    'FontName','Arial',...
    'FontSize',10,...
    'NextPlot','add');
Curve = plot(tout, xSP);
Curve.Color = [0.1 0.1 0.1];
Curve = plot(tout, xCL);
Curve.Color = [1 0.498 0.055];
Curve.LineWidth = 1;
Curve.LineStyle = '-.';
Curve = plot(tout, xCLd);
Curve.Color = [0.7 0.15 0.055];
Curve.LineWidth = 1.5;
xlabel('Time (s)')
ylabel('Motor Speed (rad/s)')
legend('Step Input','Analog Controller','Discrete Controller','Location','SouthEast');

% Plotting analog controller effort
Fig3 = figure('Position',[(ScrSize(3)-wfig)/2-wfig/2 (ScrSize(4)-hfig)/2-hfig/2-55 wfig hfig]);
axes(Fig3,...
    'Position',[0.1 0.16 0.84 0.74],...
    'XGrid','on',...
    'YGrid','on',...
    'FontName','Arial',...
    'FontSize',10,...
    'NextPlot','add');
Curve = plot(tout, uCL);
Curve.Color = [0.1 0.1 0.1];
Curve.LineWidth = 2;
Curve = plot(tout, up);
Curve.Color = [0.2 0.3 0.7];
Curve.LineWidth = 1;
Curve = plot(tout, ui);
Curve.Color = [0.7 0.2 0.3];
Curve.LineWidth = 1;
Curve = plot(tout, ud);
Curve.Color = [0.3 0.7 0.2];
Curve.LineWidth = 1;
xlabel('Time (s)')
ylabel('Armature Voltage (V)')
legend('Controller Output','Proportional Term','Integral Term','Derivative Term','Location','NorthEast');

% Plottin digital controller effort
Fig4 = figure('Position',[(ScrSize(3)-wfig)/2+wfig/2 (ScrSize(4)-hfig)/2-hfig/2-55 wfig hfig]);
axes(Fig4,...
    'Position',[0.1 0.16 0.84 0.74],...
    'XGrid','on',...
    'YGrid','on',...
    'FontName','Arial',...
    'FontSize',10,...
    'NextPlot','add');
Curve = plot(tout, uCL);
Curve.Color = [1 0.498 0.055];
Curve.LineWidth = 1;
Curve.LineStyle = '-.';
Curve = plot(tout, uCLd);
Curve.Color = [0.7 0.15 0.055];
Curve.LineWidth = 1.5;
xlabel('Time (s)')
ylabel('Armature Voltage (V)')
legend('Analog Controller','Discrete Controller','Location','NorthEast');

