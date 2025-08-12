#### Plotting mode shapes for experiment ####

# Basis functions
import numpy as np
from matplotlib import pyplot as plt

# Functions for defining main structure
from functions.indata.indata import indata
from functions.indata.mprop import mprop

# Functions for plotting
from functions.plot.utils import getPlotAxsLim, plotSettings, plotStructure, set_axes_equal, plotModeShape
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
rho = 7870

# Build mprop dictionary using mprop 
mprop = mprop(nn_levels,dim_brace, dim_leg, E, rho, mill)


####################### Define structure #######################
X, C = indata(width_mudline, width_top, height, nn_levels, nne_per_beam, mill)

# Note: no bounds
scale = 0.2          # Scaling factor
nno = X.shape[0]     # Number of nodes
nne = C.shape[0]     # Number of elements


# Import deformations from experiment
#U_mode = np.array([[0.0033158973, 0.0190424136, 0.9834775691, 0.0028746391, 1., 0.05245329], 
#                   [0.7664218763, 1., 0.0948692644, 0.7680447163, 0.1302072702, 0.8855924672],
#                   [0.0171884885, 0.9952296695, 0.0534945561, 0.0409159193, 0.0641903487, 1.],
#                   [0.0423174896, 1., 0.5689389261, 0.0495471582, 0.9480250557, 0.7086670158]])
# nat_freq = np.array([46.06320531641615, 174.08743589331564, 184.9504005951157, 195.15740622255157, 209.49144312131676])


U_mode = np.array([[ 0.00335835  , -0.0116942908,  0.9942662344, -0.0031045895, 1. , -0.0037534021],
                   [-0.7692870096,  1. ,  0.1172336208, -0.7710737323, -0.1342059816,  0.8895465998],
                   [ 0.0172246509,  1. ,  0.056315751 , -0.0412170377, 0.0621376082, -1.0055219386],
                   [ 0.0423483148,  1. , -0.5704355246,  0.0495598884, -0.9457986023,  0.7082710758]])
nat_freq = np.array([ 46.1123116769, 174.0872930201, 184.9497509719, 195.1507128885])

# Placements of nodes
U_plac = np.array([[21, 0],
                   [14 , 0], 
                   [14, 1],
                   [12, 1],
                   [1, 0],
                   [1, 1]])

# Make correct size and shape
U = np.zeros((nno, 3))  

# Choose mode to plot
for k in range(U_mode.shape[1]):
    mode_nn = k  # Mode number to plot

    for i in range(U_plac.shape[0]):
        U[U_plac[i, 0], U_plac[i, 1]] = U_mode[mode_nn, i]

    X_deformed = X + scale * U


    ############# Plotting #############
    fig = plt.figure(dpi= 100)
    fig = plotSettings(fig)

    # Plot the deformed structure
    ax = plotStructure(X, C, fig, linestyle='--', linewidth=1.0, color='k')
    ax = plotModeShape(X_deformed, C, nne, ax=ax)

    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c='k', label="Original Nodes")
    ax.scatter(X_deformed[:, 0], X_deformed[:, 1], X_deformed[:, 2], c='b', marker='o', label="Deformed Nodes")

    # Set axis limits to ensure proper scaling
    x_min, x_max = np.min(X_deformed[:, 0]), np.max(X_deformed[:, 0])
    y_min, y_max = np.min(X_deformed[:, 1]), np.max(X_deformed[:, 1])
    z_min, z_max = np.min(X_deformed[:, 2]), np.max(X_deformed[:, 2])
    
    # Adjust limits to keep aspect ratio equal
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])
    ax.set_zlim([z_min, z_max])

    # Apply equal scaling
    set_axes_equal(ax)  # Apply equal axis scaling

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.legend()                   
    ax.set_title(f"Mode Shape {mode_nn + 1} (Frequency: {nat_freq[mode_nn] :.2f} Hz) - Scaled by {scale}")
    plt.show()


