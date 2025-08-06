import numpy as np

def kspring(spring_support, nno, ldof):
    """
    Calculate the stiffness matrix for the spring support.

    Parameters
    -----------
    spring_support : np.array
        Spring support matrix = [nodeno, dof, stiffness]
    nno : int
        Number of nodes
    ldof : int
        Number of degrees of freedom per node

    Returns
    --------
    Kkmat : np.array
        Stiffness matrix for spring support
    """

    # Initialize stiffness matrix
    Kkmat = np.zeros((nno*ldof,nno*ldof))

    # Loop over spring support and add stiffness values
    for i in range(spring_support.shape[0]):
        dof = int((spring_support[i,0] - 1)*ldof + spring_support[i,1] - 1)
        Kkmat[dof, dof] = spring_support[i, 2]

    return Kkmat