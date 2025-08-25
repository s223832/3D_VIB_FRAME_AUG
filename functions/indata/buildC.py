import numpy as np

def buildC(nn_levels, nne_per_beam, TP = False):
    """
    Function builds connectivity matrix with assignment of number according to material property
    for the 3D frame jacket foundation.

    Parameters
    -----------
    nn_levels : int
        Number of levels
    nne_per_beam : int
        Number of elements per beam
    TP : bool, optional
        If True, the transition piece is included in the connectivity matrix (default is False)

    Returns
    --------
    C : np.array
        Array of element connectivity and assignment of material properties
        np.array = [node number 1, node number 2, material property number] 

    C_TP : np.array
        Array of connectivity for the transition piece, if TP is True
        np.array = [node number 1, node number 2, material property number]

    """

    # Define number of elemements
    nne = 20 * nn_levels                        # Total number of elements

    # Initialize 
    C = np.zeros((nne, 3), dtype=int)           # Connectivity matrix
    idx_nne = 0                                 # Element index
    nno_per_side = 5 + 3 * (nn_levels - 1)      # Number of base nodes per side

    # Loop over each side of the jacket
    for side in range(4):
        
        # Special case for base nodes side 1
        if side == 0:
            # Create index for base nodes 
            idx = np.arange(1, 6 + 3 * (nn_levels - 1))
        
        # Special case for base nodes side 4
        elif side == 3:
            # Update the node numbers
            update_idx = np.zeros(nn_levels + 1, dtype=int)
            update_idx[1:] = 2 + 3 * np.arange(nn_levels,dtype=int)
            for i in update_idx:
                idx[i] = idx[i + 1]

            # Nodes for side 1
            side1nodes_idx = np.ones(nn_levels + 1, dtype=int)
            side1nodes_idx[1:] = 3 + 3*np.arange(nn_levels, dtype=int)
            idx[side1nodes_idx] = side1nodes_idx
            # Add to updated indices, in order to find difference
            update_idx = np.hstack((update_idx,side1nodes_idx))
        
            # Find the difference in index lists
            all_idx = np.arange(0,nno_per_side, dtype=int)
            update_idx = np.setdiff1d(all_idx,update_idx)

            # Define new values
            nno = int(C[idx_nne - 1,0])
            nno_values = int(len(update_idx) + 1)
            new_values = np.arange(nno + 1, nno + nno_values, dtype=int)
            idx[update_idx] = new_values

        # Case for side 2 and 3
        else:
            # Update the node numbers for the current side
            update_idx = np.zeros(nn_levels + 1,dtype=int)
            update_idx[1:] = 2 + 3 * np.arange(nn_levels, dtype=int)
            for i in update_idx:
                idx[i] = idx[i + 1]
            
            # Remaining indices
            all_idx = np.arange(0,nno_per_side, dtype=int)
            update_idx = np.setdiff1d(all_idx,update_idx)

            # Define new values
            nno_values = int(len(update_idx) + 1)
            nno = int(C[idx_nne - 1,0])
            new_values = np.arange(nno + 1, nno + nno_values, dtype=int)
            idx[update_idx] = new_values

        # Define element connectivity, level 1
        C[idx_nne:idx_nne + 5,:] = [[idx[0], idx[4], 1], [idx[1], idx[3], nn_levels + 1], 
                                    [idx[1], idx[4], 1], [idx[4], idx[2], 1], [idx[4], idx[3], 1]]
        idx_nne += 5
        # Define element connectivity at rest of levels
        for i in range(1,nn_levels):
            # For Node 3i
            C[idx_nne] = np.array([idx[3*i-1], idx[3*(i+1)+1], (i+1)])
            idx_nne += 1
            # For Node 3i + 1
            C[idx_nne] = np.array([idx[3*i], idx[3*(i+1)], (i+1) + nn_levels])
            idx_nne += 1
            C[idx_nne] = np.array([idx[3*i], idx[3*(i+1)+1], (i+1)])
            idx_nne += 1
            # For Node 3i + 5
            C[idx_nne] = np.array([idx[3*i+4], idx[3*i+2], (i+1)])
            idx_nne += 1
            C[idx_nne] = np.array([idx[3*i+4], idx[3*i+3], (i+1)])
            idx_nne += 1

    # Add transition piece if present
    if TP == True:
       nno_max = (4+8*nn_levels) + (nne_per_beam-1)*20*nn_levels                 # Total number of nodes

       C_TP = np.array([[1, nno_max+1, nn_levels + 1],                       # Pile 1 (bottom)
                        [2, nno_max+2, nn_levels + 1],                       # Pile 2 (bottom)
                        [6 + (nn_levels-1)*3, nno_max+3, nn_levels + 1],     # Pile 3 (bottom)
                        [9 + (nn_levels-1)*5, nno_max+4, nn_levels + 1],     # Pile 4 (bottom)
                        [nn_levels*3, nno_max+5, nn_levels*2],               # Pile 1 (top)
                        [nn_levels*3+1, nno_max+6, nn_levels*2],             # Pile 2 (top)
                        [2+5*nn_levels, nno_max+7, nn_levels*2],             # Pile 3 (top)
                        [3+7*nn_levels, nno_max+8, nn_levels*2],             # Pile 4 (top)

                        [nno_max+5, nno_max+9, nn_levels*2 + 1],             # Transition Braces
                        [nno_max+6, nno_max+9, nn_levels*2 + 1],
                        [nno_max+7, nno_max+9, nn_levels*2 + 1],
                        [nno_max+8, nno_max+9, nn_levels*2 + 1]])
    
    # If transition piece is not present, add only piles
    else: 
        nno_max = (4+8*nn_levels) + (nne_per_beam-1)*20*nn_levels                # Total number of nodes

        C_TP = np.array([[1, nno_max+1, nn_levels + 1],                          # Pile 1 (bottom)
                            [2, nno_max+2, nn_levels + 1],                       # Pile 2 (bottom)
                            [6 + (nn_levels-1)*3, nno_max+3, nn_levels + 1],     # Pile 3 (bottom)
                            [9 + (nn_levels-1)*5, nno_max+4, nn_levels + 1],     # Pile 4 (bottom)
                            [nn_levels*3, nno_max+5, nn_levels*2],               # Pile 1 (top)
                            [nn_levels*3+1, nno_max+6, nn_levels*2],             # Pile 2 (top)
                            [2+5*nn_levels, nno_max+7, nn_levels*2],             # Pile 3 (top)
                            [3+7*nn_levels, nno_max+8, nn_levels*2]])            # Pile 4 (top)


    return C, C_TP

