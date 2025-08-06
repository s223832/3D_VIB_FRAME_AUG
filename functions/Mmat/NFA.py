import numpy as np
from scipy import linalg

def NFA(K, M, nno, ldof, bound, solve_subset=None):
    """
    Natural frequency analysis program for a 3D frame structure. Solves the eigenvalue problem
    for the system stiffness and mass matrices, taking into account nodal boundary conditions.

    Parameters
    ----------
    K : np.array
        System stiffness matrix
    M : np.array
        System mass matrix
    nno : int
        Total number of nodes
    bound : np.array
        Nodal boundary conditions
    solve_subset : list, optional
        Subset of eigenvalues to solve for

    Returns
    -------
    omega : np.array
        Natural frequencies
    U : np.array
        Mode shapes
    """  

    if np.any(bound):
        # Initialize index for constrained (du) and unconstrained (df) dofs
        dof = list(range(0, ldof * nno))        # Index of total degrees of freedom

        du = [int((bound[i,0] - 1)*ldof + bound[i,1] - 1) for i in range(bound.shape[0])]
        df = list(set(dof) - set(du))           # Index for unknown displacements
        
        # Solve the generalised eigenvalue problem
        D, U = linalg.eigh(K[np.ix_(df,df)],M[np.ix_(df,df)], subset_by_index = solve_subset)

    else:
        # Solve the generalised eigenvalue problem
        D, U = linalg.eigh(K,M, subset_by_index = solve_subset)
        
    # Calculate natural frequencies som eigenvalues
    omega = np.sqrt(D).real

    # Normalize mode shape for max displacement of +1
    for i in range(U.shape[1]):             # Loop through each mode
        max_disp = np.max(np.abs(U[:, i]))  # Find max absolute displacement
        if max_disp != 0:                   # Avoid division by zero
            U[:, i] /= max_disp             # Normalize mode shape
    
    return omega, U