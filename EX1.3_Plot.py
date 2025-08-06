############################## Plotting ###############################
# Import packages
# Import functions for data
from classes.VIBdata import VIBdata

# Import functions for plotting
from functions.plot.plotconnectivity import plotconnectivity
from functions.plot.plotmodeshapes import plotmodeshapes


# Import data from database
# Load the FEA object from the database
data_vib = VIBdata(name='VIB_DataBase.db')
####################### Plotting #####################
# Plot the connectivity of the truss from data in the database
# plotconnectivity(data_vib)

plot_subset = [0, 10]                 # Plot the first 30 modes
for i in range(plot_subset[0], plot_subset[1]):
    plotmodeshapes(data_vib, mode=i, scale=1.0)

#plotmodeshapes(data_vib, mode=17, scale=3.0)  