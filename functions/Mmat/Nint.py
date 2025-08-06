import numpy as np

def Nint(s, L):
    """
    Shape functions for a bar element in local coordinates

    Parameters
    ----------
    s : float
       Local coordinate (interpolation point)

    Returns
    -------
    : np.array
      Shape functions matrix
    """

    # Shape functions for element in local coordinates
    N1 = (1 - s)/2
    N4 = (1 + s)/2  
    N2 = 1 - 3*((1 + s)/2)**2 + 2*((1 + s)/2)**3
    N3 = L*((1 + s)/2 - 2*((1 + s)/2)**2 + ((1 + s)/2)**3)
    N5 = 3*((1 + s)/2)**2 - 2*((1 + s)/2)**3
    N6 = L*(-((1 + s)/2)**2 + ((1 + s)/2)**3)

    # Shape functions matrix in local coordinates
    N = np.array([[N1, 0,  0,  0,  0,  0,  N4, 0,  0,  0,  0,  0 ],
                  [0,  N2, 0,  0,  0,  N3, 0,  N5, 0,  0,  0,  N6],
                  [0,  0,  N2, 0, -N3, 0,  0,  0,  N5, 0, -N6, 0 ],
                  [0,  0,  0,  N1, 0,  0,  0,  0,  0,  N4, 0,  0 ]])

    return N