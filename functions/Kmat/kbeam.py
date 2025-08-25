import numpy as np
from functions.Kmat.Abeam import Abeam
from functions.Kmat.intpL import intpL
from functions.Kmat.Bint import Bint


def kbeam(n1, n2, Ge, PolDeg):
    """
    Builds local stiffnes matrix from element properties

    Parameters
    -----------
    n1 : np.array
        Coordinate for node 1
    n2 : np.array
        Coordinate for node 2
    Ge : list
        Material properies for element 
        list = [E, A, Iz, Iy, G, J]
    PolDeg : int
        Polynomial degree 

    Returns
    --------
    k : np.array
        Local stiffness matrix for element
    """
    
    # Define length and transformation matrix
    A, L = Abeam(n1, n2)

    # Gauss-Legrendre interpolation points
    xip, wip = intpL(PolDeg)

    # Jacobi function
    J = L/2

    # Init. material matrix
    D = np.array([[Ge[0]*Ge[1], 0, 0, 0],
                  [0, Ge[0]*Ge[2], 0, 0],
                  [0, 0, Ge[0]*Ge[3], 0],
                  [0, 0, 0, Ge[4]*Ge[5]]])
    
    # Initialize k for element in local coordinates
    k_l = np.zeros((12,12))
    
    for i in range(len(xip)):
        B = Bint(xip[i],L)
        k_l += B.T @ D @ B * wip[i] * J
    
    k = A.T @ k_l @ A
    
    return k