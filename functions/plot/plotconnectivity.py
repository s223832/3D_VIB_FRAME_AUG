import matplotlib.pyplot as plt
import numpy as np
from functions.plot.utils import getPlotAxsLim, plotSettings, plotStructure, plotNodes, plotNodeNumbering, plotElementNumbering, set_axes_equal

def plotconnectivity(Model, figsizevec=[10, 10], dpi=100, mainscale=0.015):

    ### SETUP###
    # Import model parameters
    X = Model.X
    C = Model.C
    bound = Model.bound
    spring_support = Model.spring_support

    # Define scaling parameter and axis limits for plots
    fscale = max(figsizevec) 
    axisscale = 10 * 6.4 / fscale 
    pscale, axlim = getPlotAxsLim(X, mainscale, axisscale)
    pscale *= 6.4 / fscale  # Main scaling parameter

    # Close all open plots
    plt.close('all')
    fig = plt.figure(dpi=dpi)
    fig = plotSettings(fig)

    ax = plotStructure(X, C, fig, linestyle='-', linewidth=1.8, color='k')
    ax = plotNodes(X, ax, bound, spring_support)
    ax = plotNodeNumbering(X, ax, dsup=pscale, size=9)
    ax = plotElementNumbering(X, C, ax, dsup=pscale, color='black', size=9)
    
    # Set axis limits to ensure proper scaling
    x_min, x_max = np.min(X[:, 0]), np.max(X[:, 0])
    y_min, y_max = np.min(X[:, 1]), np.max(X[:, 1])
    z_min, z_max = np.min(X[:, 2]), np.max(X[:, 2])
    
    # Adjust limits to keep aspect ratio equal
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])
    ax.set_zlim([z_min, z_max])

    # Apply equal scaling
    set_axes_equal(ax)  # Apply equal axis scaling

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title('Node and Element Numbering')

    plt.show()


def plotindata(X, C, figsizevec = [6.4,4.8], dpi = 100, mainscale=0.015):
    
    # Define scaling parameter and axis limits for plots
    fscale = max(figsizevec) 
    axisscale = 10 * 6.4 / fscale 
    pscale, axlim = getPlotAxsLim(X, mainscale, axisscale)
    pscale *= 6.4 / fscale  # Main scaling parameter

    # Close all open plots
    plt.close('all')
    fig = plt.figure(dpi=dpi)
    fig = plotSettings(fig)

    ax = plotStructure(X, C, fig, linestyle='-', linewidth=1.8, color='k')
    ax = plotNodes(X, ax, [], [])
    ax = plotNodeNumbering(X, ax, dsup=pscale, size=9)
    
    # Set axis limits to ensure proper scaling
    x_min, x_max = np.min(X[:, 0]), np.max(X[:, 0])
    y_min, y_max = np.min(X[:, 1]), np.max(X[:, 1])
    z_min, z_max = np.min(X[:, 2]), np.max(X[:, 2])
    
    # Adjust limits to keep aspect ratio equal
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])
    ax.set_zlim([z_min, z_max])

    # Apply equal scaling
    set_axes_equal(ax)  # Apply equal axis scaling

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title('Structure incl. Node Numbering')

    plt.show()