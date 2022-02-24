from modules.fitfunctions import define_data, fit_data, plot_data

# Defining first data set
x1 = [0, 1, 2, 3, 4]
y1 = [2.1, 2.8, 4.2, 4.9, 5.1]
data1 = define_data(x1, y1, xname='x1', yname='y1')
# Fitting data
fit1 = fit_data(data1)
# Plotting results
plot_data(data1, fit1)

# Defining second data set
x2 = [0, 1, 2, 3, 4]
y2 = [3, 5.1, 6.8, 8.9, 11.2]
data2 = define_data(x2, y2, xname='x2', yname='y2')
# Fitting data
fit2 = fit_data(data2)
# Plotting results
plot_data(data2, fit2)
