import numpy as np

def mprop(nn_levels, dim_brace, dim_leg, E, rho, mill = False):
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
    rho : float
        Density of steel elements
    mill : bool, optional
        If True, the mill tower is included in the material properties (default is False)

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
    
    # Calculate shear modulus
    G = E/(2*(1+0.3))

    # Calculate cross-sectional area, second moment area and torsinal constant
    for i in range(nn_levels):
        A_brace[i] = np.pi*((dim_brace[i,0] / 2)**2 - ((dim_brace[i,0] / 2 - dim_brace[i,1]))**2)
        A_leg[i] = np.pi*((dim_leg[i,0] / 2)**2 - ((dim_leg[i,0] / 2 - dim_leg[i,1]))**2)
        Iyz_brace[i] = np.pi/4*((dim_brace[i,0] / 2)**4 - ((dim_brace[i,0] / 2 - dim_brace[i,1]))**4)
        Iyz_leg[i] = np.pi/4*((dim_leg[i,0] / 2)**4 - ((dim_leg[i,0] / 2 - dim_leg[i,1]))**4)
        J_brace[i] = np.pi/2*((dim_brace[i,0] / 2)**4 - ((dim_brace[i,0] / 2 - dim_brace[i,1]))**4)
        J_leg[i] = np.pi/2*((dim_leg[i,0] / 2)**4 - ((dim_leg[i,0] / 2 - dim_leg[i,1]))**4)

    
    # Assign material properties 
    mprop = {}
    for i in range(nn_levels):
        mprop[i + 1] = {'E': E, 'A': A_brace[i], 'rho': rho, 'Iy': Iyz_brace[i], 'Iz' :  Iyz_brace[i],
                           'J' : J_brace[i] ,'G' : G, 'type': f'Steel rod brace level {chr(65 + i)}'}
        mprop[i + 1 + nn_levels] = {'E': E, 'A': A_leg[i], 'rho': rho, 'Iy': Iyz_leg[i], 'Iz' : Iyz_leg[i],
                          'J' : J_brace[i], 'G' : G, 'type': f'Steel rod leg level {chr(65 + i)}'}
    
    # Add materials to mprop if mill is present
    if mill == True:
        mprop[nn_levels*2 + 1] = {'E': E, 'A': 8, 'rho': 385.9, 'Iy': 42.67, 'Iz': 0.6667, 'J': 2.444, 'G': 8.08e10, 'type': f'Transition piece mill'}
        
        A = [1.746251135, 1.584569069, 1.430398551, 1.283447413, 1.173070697, 1.039640974, 0.913581427, 0.794989446, 0.681637641]
        I = [25.9298216, 21.87108746, 18.30480114, 15.17937956, 12.77823344, 10.39595554, 8.354127163, 6.621817883, 5.116353816]
        J = [51.8596432, 43.74217493, 36.60960228, 30.35875912, 25.55646688, 20.79191109, 16.70825433, 13.24363577, 10.23270763]

        for i in range(1, 10):
            mprop[nn_levels*2 + 1 + i] = {'E': E, 'A': A[i-1], 'rho': rho, 'Iy': I[i-1], 'Iz': I[i-1], 'J': J[i-1], 'G': 8.08e10, 'type': f'Tower element {i}'}
    # If mill is not present, add only a transition piece for the mill
    else:
        mprop[nn_levels*2 + 1] = {'E': E, 'A': 0.0024, 'rho': rho, 'Iy': 5.12e-6, 'Iz': 4.5e-8, 'J': 1.65e-7, 'G': G, 'type': f'Transition piece mill'}
    return mprop