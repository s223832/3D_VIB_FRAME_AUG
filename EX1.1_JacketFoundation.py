############################## Build indata file ###############################
# Import packages
import numpy as np
import pickle

# Import functions for indata
from functions.indata.indata import indata
from functions.indata.mprop import mprop
from functions.plot.plotconnectivity import plotindata

####################### Define properties #######################
# Coordinates of base variables for the jacket foundation
width_mudline = 0.753            # Width of the structure at mudline
width_top = 0.406                # Width of the structure at top
height = 1.27                    # Height of the structure
nn_levels = 4                    # Number of levels
nne_per_beam = 1                 # Number of elements per beam
mill = False                     # Mill present (True/False)


################## Build property dictionary ##################
# Rod dimensions [outerdiameter, thicknes] (SI-units)
dim_brace = np.array([[12.7, 1],           # Level A - brace [outer diameter,thickness]
                      [12.7, 1],           # Level B - brace [outer diameter,thickness]
                      [12.7, 1],           # Level C - brace [outer diameter,thickness]
                      [12.7, 1]])*1e-3     # Level D - brace [outer diameter,thickness]

dim_leg = np.array([[50, 1.5],             # Level A - leg [outer diameter,thickness]
                    [50, 1.5],             # Level B - leg [outer diameter,thickness]
                    [50, 1.5],             # Level C - leg [outer diameter,thickness]
                    [50, 1.5]])*1e-3       # Level D - leg [outer diameter,thickness]


# Define steel material properties
E = 205e9
rho = 7850

# Build mprop dictionary using mprop 
mprop = mprop(nn_levels,dim_brace, dim_leg, E, rho, mill)

####################### Define structure #######################
X, C = indata(width_mudline, width_top, height, nn_levels, nne_per_beam, mill)


####################### Store and load data ####################
# Saving numpys
np.save('indata_X.npy',X)
np.save('indata_C.npy',C)

# Save the dictionary to a file using pickle
with open('indata_mprop.pkl', 'wb') as f:
    pickle.dump(mprop, f)

######################## Plot structure #########################
plotindata(X,C)