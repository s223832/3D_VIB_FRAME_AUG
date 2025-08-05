import numpy as np
from functions.indata.buildC import buildC
from functions.indata.buildX import buildX

def indata(width_mudline, width_top, height, nn_levels, nne_per_beam, mill = False):
    """
    Function to build the input data, both node coordinate matrix and connectivity matrix for 
    the jacket foundation in 3D for the FE frame program. Creates subdivision of beam elements. 
    Pulls the node coordinates from buildX and the connectivity matrix from buildC.

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
    nne_per_beam: int
        Number of elements per beam
    mill : bool, optional
        If True, the mill tower is included in the coordinates and connectivity (default is False)

    Returns
    --------
    X : np.array
        Array of node coordinates in global coordinates
    C : np.array
        Array of element connectivity and assignment of material properties
    """

    # Node coordinates and connectivity matrix
    X, X_mill = buildX(width_mudline, width_top, height, nn_levels, mill)
    C, C_mill = buildC(nn_levels, nne_per_beam, mill)
    
    nno = X.shape[0]            # Number of nodes
    nne = C.shape[0]            # Number of elements

    # If only one element per beam
    if nne_per_beam == 1:
        X_full = X
        C_full = C
    
    # For all other number of elements per beam
    else:
        # Start index 
        idx = 0

        # Loop over each element
        for i in range(C.shape[0]):
            # Initialize matrices 
            X_i = np.zeros(((nne_per_beam - 1),3))
            C_i = np.zeros((nne_per_beam, 3), dtype=int)

            # Retrieve values from connectivity matrix
            dn_start = int(C[i,0])          # Start node 
            dn_end = int(C[i,1])            # End node
            propno = int(C[i,2])            # Prop number

            # Loop over the additional nodes in the beam
            for k in range(1, nne_per_beam):
                # Define node coordinates
                X_i[k - 1,:] = X[dn_start - 1, :] + k / nne_per_beam * (X[dn_end - 1, :] - X[dn_start - 1, :])
            
            # Loop over the number of elements in the beam
            for j in range(nne_per_beam):
                # Define connectivity 
                if j == 0:
                    C_i[j,:] = [dn_start, nno + idx + 1, propno]
                    idx += 1
                elif j == nne_per_beam - 1:
                    C_i[j,:] = [nno + idx, dn_end, propno]
                else:
                    C_i[j,:] = [nno + idx, nno + idx + 1, propno]
                    idx += 1

            # Assemble full matrices
            if i == 0:
                C_full = C_i
                X_full = np.vstack((X, X_i))
            else:
                X_full = np.vstack((X_full, X_i))
                C_full = np.vstack((C_full, C_i))

    # Add the mill coordinates and connectivity to the full matrices
    if X_mill.size > 0:
        X_full = np.vstack((X_full, X_mill))
        C_full = np.vstack((C_full, C_mill))

    return X_full, C_full