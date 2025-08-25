import numpy as np
from math import atan, cos, sin, pi, sqrt
from functions.indata.buildX2D import buildX2D

def buildX(width_mudline, width_top, height, nn_levels, TP = False):
    """
    Function to build the node coordinates for the jacket foundation in 3D for the FE frame program.
    Utilizes the 2D geometry from buildX2D and rotates it to create a 3D jacket structure.

    Parameters
    -----------
    width_mudline : float
        Width of the structure at mudline
    width_top : float
        Width of the structure at top
    height : float
        Height of the structure
    nn_levels : int
        Number of levels
    nne_per_beam: int
        Number of elements per beam
    TP : bool, optional
        If True, the transition piece is included in the coordinates (default is False)

    Returns
    --------
    X_full : np.array
        Array of node coordinates in global coordinates for jacket structure
        np.array = [x, y, z] for each node in the jacket foundation
    X_TP : np.array
        Array of transition piece coordinates, if TP is True
        np.array = [x, y, z] for each node in the transition piece
    """

    ########### Calculation for one side of the jacket ##############
    # Calculate the height if the jacket is lifted up to align with the x,z axis
    l_xy = (width_mudline-width_top)/2                      # Length in x,y plane
    l_z = height                                            # Length in z direction
    len_leg = np.linalg.norm(np.array([l_xy,l_xy,l_z]))     # Length of the leg
    # Calculate height in x,z plane
    height_xz = np.sqrt(len_leg**2 - l_xy**2)               # Height in x,z plane
    
    # Import the 2D geometry 
    X = buildX2D(width_mudline, width_top, height_xz, nn_levels)

    # Add the y-coordinate and a zeros vector
    zeros_col = np.zeros((X.shape[0],1))
    X = np.hstack((X[:, :1], zeros_col, X[:, 1:]))

    # Rotate around z-axis to correct placement in x,y plane around the z-axis by pi/4 degrees 
    M_z = np.array([[cos(pi/4), -sin(pi/4), 0],
                    [sin(pi/4), cos(pi/4),  0],
                    [   0,        0,        1]])
    # Rotate around the x-axis to correct for the angle between the mudline and the top
    phi = -(pi/2 - atan(l_z/l_xy))
    M_x = np.array([[1,    0,         0    ],
                    [0, cos(phi), -sin(phi)],
                    [0, sin(phi),  cos(phi)]])
    # Rotate X-matrix
    Rot_M = np.dot(M_x,M_z)
    X = np.dot(X,Rot_M)
    # Translate to correct placement in x,y plane
    X += np.array([0, width_mudline/sqrt(2), 0])

    ############### Build the full jacket ################
    # Add the remaining 3 sides of the jacket foundation
    X_full = X.copy()
    for i in range(1, 4):
        # Rotation matrix for pi/2 * i around the z-axis
        theta = i * pi / 2
        M_z = np.array([[cos(theta), -sin(theta), 0],
                        [sin(theta),  cos(theta), 0],
                        [0,           0,          1]])
        X_rotated = np.dot(X, M_z)
        X_full = np.vstack((X_full, X_rotated))
    
    # Round the coordinates to a certain number of decimal places
    X_full = np.round(X_full, decimals=8)

    # Remove duplicate nodes but keep original order
    X_uni, indices = np.unique(X_full, axis=0, return_index=True)
    X_full = X_uni[np.argsort(indices)]

    # Add transition piece if present
    if TP == True:
        X_TP = np.array([
                            [X_full[0, 0], X_full[0, 1], -0.06592],                                                                        # Pile at nno 1 (+1)
                            [X_full[1, 0], X_full[1, 1], -0.06592],                                                                        # Pile at nno 2 (+2)
                            [X_full[5 + (nn_levels-1)*3, 0], X_full[5 + (nn_levels-1)*3, 1], -0.06592],                                    # Pile at nno 15 (+3)
                            [X_full[8 + (nn_levels-1)*5, 0], X_full[8 + (nn_levels-1)*5, 1], -0.06592],                                    # Pile at nno 24 (+4)

                            [X_full[nn_levels*3 - 1, 0], X_full[nn_levels*3 - 1, 1] - 0.01447, X_full[nn_levels*3 - 1, 2] + 0.10592],      # Pile at nno 12 (+5)
                            [X_full[nn_levels*3, 0] - 0.01447, X_full[nn_levels*3, 1], X_full[nn_levels*3, 2] + 0.10592],                  # Pile at nno 13 (+6)
                            [X_full[nn_levels*5 + 1, 0], X_full[nn_levels*5 + 1, 1] + 0.01447, X_full[nn_levels*5 + 1, 2] + 0.10592],      # Pile at nno 22 (+7)
                            [X_full[7*nn_levels + 2, 0] + 0.01447, X_full[7*nn_levels + 2, 1], X_full[7*nn_levels + 2, 2] + 0.10592],     # Pile at nno 31 (+8)
                            [0, 0, X[nn_levels*3, 2] + 0.10592]])                                                                          # Center (+9)
    
        return X_full, X_TP

    else:
        X_TP = np.array([
                            [X_full[0, 0], X_full[0, 1], -0.06592],                                                                        # Pile at nno 1 (+1)
                            [X_full[1, 0], X_full[1, 1], -0.06592],                                                                        # Pile at nno 2 (+2)
                            [X_full[5 + (nn_levels-1)*3, 0], X_full[5 + (nn_levels-1)*3, 1], -0.06592],                                    # Pile at nno 15 (+3)
                            [X_full[8 + (nn_levels-1)*5, 0], X_full[8 + (nn_levels-1)*5, 1], -0.06592],                                    # Pile at nno 24 (+4)

                            [X_full[nn_levels*3 - 1, 0], X_full[nn_levels*3 - 1, 1] - 0.01447, X_full[nn_levels*3 - 1, 2] + 0.10592],      # Pile at nno 12 (+5)
                            [X_full[nn_levels*3, 0] - 0.01447, X_full[nn_levels*3, 1], X_full[nn_levels*3, 2] + 0.10592],                  # Pile at nno 13 (+6)
                            [X_full[nn_levels*5 + 1, 0], X_full[nn_levels*5 + 1, 1] + 0.01447, X_full[nn_levels*5 + 1, 2] + 0.10592],      # Pile at nno 22 (+7)
                            [X_full[7*nn_levels + 2, 0] + 0.01447, X_full[7*nn_levels + 2, 1], X_full[7*nn_levels + 2, 2] + 0.10592]])     # Pile at nno 31 (+8)                                                                          # Center (+9) 

        return X_full, X_TP