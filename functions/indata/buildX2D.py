import numpy as np
from math import cos, sin
from functions.indata.geometry import phibrace, intersection

def buildX2D(width_mudline, width_top, height, nn_levels):
    """
    Function to build the node coordinates for the jacket foundation in 2D for the FEM program

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

    Returns
    --------
    X : np.array
        Array of node coordinates in global coordinates
    """

    # Define number of nodes and elements
    nno = 5 + 3 * (nn_levels - 1) + 4    # Total number of nodes
    
    # Initialize array
    X = np.zeros((nno,2))                           

    # Create coordinates for each of the four corner nodes
    n1 = np.array([0,0])
    n2 = np.array([width_mudline,0])
    n3 = np.array([(width_mudline - width_top)/2 , height])
    n4 = np.array([(width_mudline + width_top)/2 , height])

    # Calculate the angle between leg and brace bars
    phi = phibrace(width_mudline, width_top, height, nn_levels)
    # Create base nodes for all levels
    for i in range(nn_levels):
        if i == 0:
            # Special case for level A
            X[0,:] = n1
            X[1,:] = n2
            # Find vector rotated by angle phi
            vec = np.array([cos(phi)*n3[0]-sin(phi)*n3[1],
                    sin(phi)*n3[0]+cos(phi)*n3[1]])
            # Coordinates for node 4 & 3
            X[3,:] = intersection(n1,vec,n2,n4)
            X[2,:] = np.array([n2[0]-X[3,0], X[3,1]])
            # Coordinats for node 5
            X[4,:] = intersection(n1, X[3,:], n2, X[2,:])
        else:
            start_node = X[3*i-1,:]
            # Coordinate for node 3*i + 3
            X[3*i + 3,:] = intersection(start_node,(vec+start_node),n2,n4)
            # Coordinate for node 3*i + 2
            X[3*i + 2,:] = np.array([n2[0]-X[3+3*i,0], X[3+3*i,1]])
            # Coordinate for node 3*i + 4
            X[3*i + 4,:] = intersection(X[3*i - 1],X[3*i +3], X[3*i], X[3*i + 2])
        

    return X

