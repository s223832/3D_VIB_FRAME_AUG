import numpy as np

def mprop(nn_levels, dim_brace, dim_leg, E, G, rho, TP = False):
    """
    Function to build the mprop library from given dimensions and material properties.

    Parameters
    -----------
    nn_levels : int
        Number of levels
    dim_braces : np.array
        Dimension for braces 
        np.array = [outer diameter, thickness]
    dim_leg : np.array
        Dimension for leg 
        np.array = [outer diameter, thickness]
    E : float
        Modulus of elasticity for steel elements
    G : float 
        Shear modulus for steel elements
    rho : float
        Density of steel elements
    TP : bool, optional
        If True, the transition piece is included in the material properties (default is False)

    Returns
    --------
    mprop : dict 
        Dictionary for material properties   
        dict = {level number : {'E': modulus of elasticity, 'A': cross-sectional area,
                            'rho': density, 'Iy': second moment of area, 
                            'Iz': second moment of area, 'J': torsional constant,
                            'G': shear modulus, 'type': type of element}}
    """
    
    # Initialize arrays for storing cross section area
    A_brace = np.zeros(nn_levels)
    A_leg = np.zeros(nn_levels)
    Iyz_brace = np.zeros(nn_levels)
    Iyz_leg = np.zeros(nn_levels)
    J_brace = np.zeros(nn_levels)
    J_leg = np.zeros(nn_levels)

    if nn_levels != len(dim_brace) and nn_levels != len(dim_leg):
        print('List dimension of brace/leg properties does not match number of levels')
        return None
    
    # Calculate cross-sectional area, second moment area and torsinal constant
    for i in range(nn_levels):
        A_brace[i] = np.pi*((dim_brace[i,0] / 2)**2 - ((dim_brace[i,0] / 2 - dim_brace[i,1]))**2)
        A_leg[i] = np.pi*((dim_leg[i,0] / 2)**2 - ((dim_leg[i,0] / 2 - dim_leg[i,1]))**2)
        Iyz_brace[i] = (np.pi/4*((dim_brace[i,0] / 2)**4 - ((dim_brace[i,0] / 2 - dim_brace[i,1]))**4))
        Iyz_leg[i] = np.pi/4*((dim_leg[i,0] / 2)**4 - ((dim_leg[i,0] / 2 - dim_leg[i,1]))**4)
        J_brace[i] = np.pi/2*((dim_brace[i,0] / 2)**4 - ((dim_brace[i,0] / 2 - dim_brace[i,1]))**4)
        J_leg[i] = np.pi/2*((dim_leg[i,0] / 2)**4 - ((dim_leg[i,0] / 2 - dim_leg[i,1]))**4)
    
    # Assign material properties 
    mprop = {}
    for i in range(nn_levels):
        mprop[i + 1] = {'E': 195e9, 'A': A_brace[i], 'rho': rho, 'Iy': Iyz_brace[i], 'Iz' :  Iyz_brace[i],
                           'J' : J_brace[i] ,'G' : G, 'type': f'Steel rod brace level {chr(65 + i)}'}
        mprop[i + 1 + nn_levels] = {'E': 215e9, 'A': A_leg[i], 'rho': rho, 'Iy': Iyz_leg[i], 'Iz' : Iyz_leg[i],
                          'J' : J_leg[i], 'G' : G, 'type': f'Steel rod leg level {chr(65 + i)}'}

    # Add materials to mprop if transition piece is present
    if TP == True:
        mprop[nn_levels*2 + 1] = {'E': E, 'A': 0.00368, 'rho': rho, 'Iy':5.120e-6, 'Iz': 4.500e-8, 'J': 1.650e-7, 'G': G, 'type': f'Transition piece'}    
    
    return mprop