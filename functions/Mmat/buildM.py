import numpy as np
from functions.Mmat.mbeam import mbeam

def buildM(X, C, mprop, nno, nne, ldof, TP=False):
    """
    Builds the system mass matrix from element mass matrices

    Parameters
    ----------
    X : np.array
        Nodal coordinates
    C : np.array
        Connectivity matrix
    mprop : dict
        Dictionary with element properties
    nno : int
        Total number of nodes
    nne : int
        Total number of elements
    ldof : int
        Number of degrees of freedom per node
    TP : bool, optional
        If True, the additional mass and inertia is added to the mass matrix (default is False)

    Returns
    -------
    Mmat : np.array
        System consistent mass matrix in global coordinates
    """

    # Initialize M matrix
    Mmat = np.zeros((nno*ldof,nno*ldof))

    # Loop over elements
    for i in range(nne):
        # Define element properties
        propno = C[i,2]
        # Cross section area and material density
        Ge = [mprop[propno]['A'], mprop[propno]['rho'], mprop[propno]['J']]

        # Define element coordinates
        n1 = X[C[i,0]-1]
        n2 = X[C[i,1]-1]

        # Define element mass matrix (global coordinates)
        # NOTE: The polynomial order is hardcoded to 6
        m = mbeam(n1, n2, Ge, 6)

        # Define element degrees of freedom
        de = np.array([6*C[i,0]-5, 6*C[i,0]-4, 6*C[i,0]-3, 6*C[i,0]-2, 6*C[i,0]-1, 6*C[i,0],
                       6*C[i,1]-5, 6*C[i,1]-4, 6*C[i,1]-3, 6*C[i,1]-2, 6*C[i,1]-1, 6*C[i,1]])
        
        # Add element stiffness matrix to system stiffness matrix
        Mmat[np.ix_(de - 1, de - 1)] += m
    
    # Additional mass to footings
    Mmat[6*116, 6*116] += 0.787
    Mmat[6*116+1, 6*116+1] += 0.787
    Mmat[6*116+2, 6*116+2] += 0.787

    Mmat[6*117, 6*117] += 0.787
    Mmat[6*117+1, 6*117+1] += 0.787
    Mmat[6*117+2, 6*117+2] += 0.787

    Mmat[6*118, 6*118] += 0.787
    Mmat[6*118+1, 6*118+1] += 0.787
    Mmat[6*118+2, 6*118+2] += 0.787

    Mmat[6*119, 6*119] += 0.787
    Mmat[6*119+1, 6*119+1] += 0.787
    Mmat[6*119+2, 6*119+2] += 0.787
    
    return Mmat