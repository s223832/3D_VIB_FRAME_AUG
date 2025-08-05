import numpy as np
from math import cos, sin
from scipy.optimize import minimize_scalar

def intersection(X1, X2, X3, X4):
    """
    Helper function to find the intersection point between two lines in 2D space. 

    Parameters
    ----------
    X1 : np.array
        Start point for line 1
    X2 : np.array
        End point for line 1
    X3 : np.array
        Start point for line 2
    X4 : np.array
        End point for line 2
    
    Returns
    -------
    [x,y] : np.array
        Intersection point.
    """

    # Calculate the slopes
    m1 = (X2[1] - X1[1]) / (X2[0] - X1[0])
    m2 = (X4[1] - X3[1]) / (X4[0] - X3[0])

    # Calculate y-intercepts
    b1 = X1[1] - m1 * X1[0]
    b2 = X3[1] - m2 * X3[0]

    # Find the intersection point
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1 
    return np.array([x,y])

def phibrace(width_mudline, width_top, height, nn_levels):
    """
    Helper function to find the angle between the leg and bars for all levels.
    Tests different angles and finds the one that minimizes the height difference
    between the height to the corresponding angle and the height of the structure.

    Parameters
    ----------
    width_mudline : float
        Width of the structure at mudline.
    width_top : float
        Width of the structure at top.
    height : float
        Height of the structure.
    nn_levels : int
        Number of levels.

    Returns
    -------
    x : float
        The angle in radians that minimizes the height difference.
    """

    # Function to find the height difference between the height to corresponding angle
    # and the height of the structure
    def height_difference(phi):
        # Initialize the four corner nodes
        n1 = np.array([0, 0])
        n2 = np.array([width_mudline, 0])
        n3 = np.array([(width_mudline - width_top) / 2, height])
        n4 = np.array([(width_mudline + width_top) / 2, height])
        
        # Calculate the height for the given angle
        start_node = n1
        for i in range(nn_levels):
            vec = np.array([cos(phi) * n3[0] - sin(phi) * n3[1],
                            sin(phi) * n3[0] + cos(phi) * n3[1]])
            a = intersection(start_node, (vec + start_node), n2, n4)
            start_node = np.array([n2[0] - a[0], a[1]])
        return abs(a[1] - height)
    
    # Use the minimize_scalar function to find the angle that minimizes the height difference
    result = minimize_scalar(height_difference, bounds=(np.pi, 2*np.pi), method='bounded')
    return result.x