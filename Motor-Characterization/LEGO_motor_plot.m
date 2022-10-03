% This m-file is called by the simulink model after running.
% You can find it's reference in ModelProperties/Callbacks

% Deleting figures
delete(get(0,'Children'));
ScrSize = get(0,'ScreenSize');
FigColor = [0.98 0.98 0.98];

% Plotting rotor speed
wfig = 450;
hfig = 200;
Fig1 = figure('Position',[(ScrSize(3)-wfig)/2-wfig/2 (ScrSize(4)-hfig)/2+hfig/2+30 wfig hfig]);
axes(Fig1,...
    'Color',FigColor,...
    'Position',[0.12 0.21 0.84 0.71],...
    'XGrid','on',...
    'YGrid','on',...
    'FontName','Arial',...
    'FontSize',10,...
    'NextPlot','add');
Curve = plot(tout, w);
Curve.Color = [0.122 0.467 0.706];
Curve.LineWidth = 1;
xlabel('Time (s)')
ylabel('Rotor Speed (rad/s)')

csvwrite('Motor Data.csv',[tout w])

