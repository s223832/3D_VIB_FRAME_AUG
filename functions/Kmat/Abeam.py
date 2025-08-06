import numpy as np

def Abeam(n1, n2):
    """
    Function calculates the transformation matrix abar for a single element \n
    Note: There is a special case when the xl || z - In this case the cross product will be zero, and yl is calculated as the following:
    yl = 0i + 1j + 0k

    Parameters
    ----------
    n1 : np.array
        nodal coordinates for start node of element (GLOB)
    n2 : np.array
        nodal coordinates for end node of element (GLOB)
    
    Returns
    -------
    A : np.array
        Transformation matrix for element
    L : float
        Length of element
    """

    # Preallocate the z(global) vector
    z = np.array([0.0, 0.0, 1.0])

    # Find the x,y,z (local)
    x = n2 - n1
    xl = x / np.linalg.norm(x)

    # Use np.allclose to compare vectors
    # Special case: np.cross(z, xl) = 0
    if np.allclose(abs(xl), z):
        y = np.array([0.0, 1.0, 0.0])
    else:
        y = np.cross(z, xl)

    yl = y / np.linalg.norm(y)
    zl = np.cross(xl, yl)

    # Create the elements transformation matrix
    c = np.stack((xl, yl, zl))
    A = np.block([[c, np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3))],
                  [np.zeros((3, 3)), c, np.zeros((3, 3)), np.zeros((3, 3))],
                  [np.zeros((3, 3)), np.zeros((3, 3)), c, np.zeros((3, 3))],
                  [np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3)), c]])
    L = np.linalg.norm(x)
    
    return A, L