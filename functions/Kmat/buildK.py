import numpy as np
from functions.Kmat.kbeam import kbeam
from functions.Kmat.kspring import kspring

def buildK(X, C, mprop, spring_support, nno, nne, ldof):
    """
    Builds the system stiffness matrix from element stiffness matrices

    Parameters
    -----------
    X : np.array
        Nodal coordinates
    C : np.array
        Connectivity matrix
    mprop : dict
        Dictionary with element properties
    spring_support : np.array
        Spring support matrix
    nno : int
        Number of nodes
    nne : int
        Number of elements
    ldof : int
        Number of degrees of freedom per node
    
    Returns
    --------
    Kmat : np.array
        System stiffness matrix in global coordinates
    """

    # Initialize K matrix
    Kmat = np.zeros((nno*ldof,nno*ldof))

    # Loop over elements
    for i in range(nne):
        # Define element properties
        propno = C[i,2]
        Ge = [mprop[propno]['E'], mprop[propno]['A'], mprop[propno]['Iz'], mprop[propno]['Iy'], mprop[propno]['G'], mprop[propno]['J']]

        # Define element coordinates
        n1 = X[C[i,0]-1]
        n2 = X[C[i,1]-1]

        # Define element stiffness matrix
        k = kbeam(n1,n2,Ge,3)

        # Define element degrees of freedom
        de = np.array([6*C[i,0]-5, 6*C[i,0]-4, 6*C[i,0]-3, 6*C[i,0]-2, 6*C[i,0]-1, 6*C[i,0],
                       6*C[i,1]-5, 6*C[i,1]-4, 6*C[i,1]-3, 6*C[i,1]-2, 6*C[i,1]-1, 6*C[i,1]])

        # Add element stiffness matrix to system stiffness matrix
        Kmat[np.ix_(de - 1, de - 1)] += k

    if np.any(spring_support):
        Kkmat = kspring(spring_support, nno, ldof)
        Kmat += Kkmat
    
    return Kmat