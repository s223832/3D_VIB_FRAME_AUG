import numpy as np
import math
import matplotlib.pyplot as plt
from functions.plot.utils import getPlotAxsLim, plotSettings, plotStructure, set_axes_equal, plotModeShape

def plotmodeshapes(Model, mode=0, scale=1.0, figsize=[6.4,4.8], dpi=100,  mainscale=0.015):
    """
    Plots the original and deformed mode shape of a Frame.
    
    Parameters
    -----------
    X : ndarray
        Node coordinates (nno x 2)
    C : ndarray
        Connectivity matrix (n_elements x 2 or n_elements x 3 if properties exist)
    U : ndarray
        Mode shapes matrix (ndof x n_modes)
    df : list
        List of free DOFs
    mode : int
        Mode shape index to plot (0-based index)
    scale : float
        Scaling factor for deformation visualization
    """

    X, C, U, nno, bound, ldof, nne, omega = Model.X, Model.C, Model.U, Model.nno, Model.bound, Model.ldof, Model.nne, Model.omega

    # Initialize a full DOF vector (including constrained DOFs)
    U_mode = np.zeros(ldof * nno)  # Full DOF array (3 DOFs per node)

    if np.any(bound):
        dof = list(range(0, ldof * nno))        # Index of total degrees of freedom
        du = [int((bound[i,0] - 1)*ldof + bound[i,1] - 1) for i in range(bound.shape[0])]
        df = list(set(dof) - set(du))           # Index for unknown displacements

        # Assign only the free DOFs
        U_mode[df] = U[:, mode]  # Map free DOFs to the correct locations

    else:
        U_mode = U[:, mode]

    # Reshape to (nno, 2) for visualization
    U_mode = U_mode.reshape((nno, 6))
    U_mode = U_mode[:, 0:3]  # Only consider the first 3 DOFs (x, y, z)
    # Deformed positions (scaled)
    X_deformed = X + scale * U_mode

    # Define scaling parameter and axis limits for plots
    fscale = max(figsize)
    axisscale = 10 * 6.4 / fscale
    pscale, axlim = getPlotAxsLim(X, mainscale, axisscale)
    pscale *= 6.4 / fscale  # Main scaling parameter

    # Close all open plots
    plt.close('all')
    fig = plt.figure(dpi=dpi)
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
    ax.set_title(f"Mode Shape {mode + 1} (Frequency: {(omega[mode])/(2*math.pi) :.2f} Hz) - Scaled by {scale}")
    plt.show()