import numpy as np
from functions.Kmat.Abeam import Abeam
from functions.Kmat.intpL import intpL
from functions.Mmat.Nint import Nint


def mbeam(n1, n2, Ge, PolDeg):
    """
    Creates the element mass matrix for a beam element in global coordinates

    Parameters
    ----------
    n1 : np.array
        Coordinates of node 1
    n2 : np.array
        Coordinates of node 2
    Ge : list
        Element properties 
        list = [A, rho, J]
    PolDeg : int
        Polynomial degree of the integration rule

    Returns
    -------
    m : np.array
        Element mass matrix in global coordinates
    """

    A, L = Abeam(n1,n2)
    xip, wip = intpL(PolDeg)
    J = L/2

    m_l = np.zeros((12,12))

    D = np.array([[Ge[0]*Ge[1], 0, 0, 0],
                  [0, Ge[0]*Ge[1], 0, 0],
                  [0, 0, Ge[0]*Ge[1], 0],
                  [0, 0, 0, Ge[1]*Ge[2]]])

    for i in range(len(xip)):
        N = Nint(xip[i], L)
        m_l += N.T @ D @ N * wip[i] * J

    # The mass matrix is transformed to global coordinates
    m = A.T @ m_l @ A

    return m