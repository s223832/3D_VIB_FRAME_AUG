import numpy as np

# Import functions
from functions.Mmat.buildM import buildM
from functions.Kmat.buildK import buildK
from functions.Mmat.NFA import NFA

class VIBframe():
    def __init__(self, X, C, mprop, bound, spring_support, solve_subset = None):
        """
        Vibration analysis program for a 3D frame structure. Calculates the natural 
        frequencies and mode shapes of the structure.

        Parameters
        ----------
        X : np.array
            Array of node coordinates in global coordinates
        C : np.array
            Array of element connectivity and assignment of material properties
        mprop : dict
            Dictionary with material properties: E = Young's modulus, A = Cross-sectional area, rho = Density,
            Iy = Second moment area (y-axis), Iz = Second moment area (z-axis), J = Torsional constant, 
            G = Shear modulus, type = description of the material
        bound : np.array
            Array of nodal boundary conditions
        spring_support : np.array
            Array of spring supports
        solve_subset : list, optional
            Subset of eigenvalues (modes) to solve for
        """

        # Assign input to object
        self.X = X
        self.C = C
        self.mprop = mprop
        self.bound = bound
        self.spring_support = spring_support
        self.solve_subset = solve_subset

        # Initialize
        self.ldof = 6                           # Number of dofs per node
        self.nno = np.size(X, 0)                # Total number of nodes
        self.nne = np.size(C, 0)                # Total number of elements
        self.ndof = self.nno * self.ldof        # Total number of dofs

        # Control if the mill is the last type in the dictionary (whether mill is present)
        last_type = None
        for d in mprop.values():
            if isinstance(d, dict) and 'type' in d:
                last_type = d['type']
        self.mill = (last_type == 'Tower element 9')

        # Run analysis
        self.buildM()
        self.buildK()
        self.NFA()

    # Functions
    # Build the system mass matrix, M
    def buildM(self):
        self.M = buildM(self.X, self.C, self.mprop, self.nno, self.nne, self.ldof, self.mill)

    # Build the system stiffness matrix, K
    def buildK(self):
        self.K = buildK(self.X, self.C, self.mprop, self.spring_support, self.nno, self.nne, self.ldof)

    # Solve the eigenvalue problem
    def NFA(self):
        self.omega, self.U = NFA(self.K, self.M, self.nno, self.ldof, self.bound, self.solve_subset)