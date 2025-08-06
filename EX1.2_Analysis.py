############################## FEM and Dynamic Analysis ###############################
# Import packages
import numpy as np
import pickle
import time
# Import functions for data
from functions.data.output import output

# Import classes
from classes.VIBframe import VIBframe

# Import functions for datastoring
from functions.data.basestore import basestore

################# Boundary conditions #####################
# Boundary conditions mat(node,ldof,disp)
bound = np.array([[ 1 , 1 , 0.0 ],
                  [ 1 , 2 , 0.0 ],
                  [ 1 , 3 , 0.0 ],
                  [ 1 , 4 , 0.0 ],
                  [ 1 , 5 , 0.0 ],
                  [ 1,  6 , 0.0 ],
                  [ 2 , 1 , 0.0 ],
                  [ 2 , 2 , 0.0 ],
                  [ 2 , 3 , 0.0 ],
                  [ 2 , 4 , 0.0 ],
                  [ 2 , 5 , 0.0 ],
                  [ 2,  6 , 0.0 ],
                  [ 15 , 1 , 0.0 ],
                  [ 15 , 2 , 0.0 ],
                  [ 15 , 3 , 0.0 ],
                  [ 15 , 4 , 0.0 ],
                  [ 15 , 5 , 0.0 ],
                  [ 15, 6 , 0.0 ],
                  [ 24 , 1 , 0.0 ],
                  [ 24 , 2 , 0.0 ],
                  [ 24 , 3 , 0.0 ],
                  [ 24 , 4 , 0.0 ],
                  [ 24 , 5 , 0.0 ],
                  [ 24 , 6 , 0.0 ]])


spring_support = []

# Uncomment the following lines to define spring supports
# Spring supports mat(node, ldof, stiffness)
    #bound = []

    #kxx = 1e16
    #kyy = 1e16
    #kzz = 1e16
    #spring_support = np.array([[ 1 , 1 , kxx],
    #                           [ 1 , 2 , kyy],
    #                           [ 1 , 3 , kzz],
    #                           [ 2 , 1 , kxx],
    #                           [ 2 , 2 , kyy],
    #                           [ 2 , 3 , kzz],
    #                           [15 , 1 , kxx],
    #                           [15 , 2 , kyy],
    #                           [15 , 3 , kzz],
    #                           [24 , 1 , kxx],
    #                           [24 , 2 , kyy],
    #                           [24 , 3 , kzz]])
                 

####################### Import indata ######################
X = np.load('indata_X.npy')
C = np.load('indata_C.npy')
# Load the dictionary from the file using pickle
with open('indata_mprop.pkl', 'rb') as f:
    mprop = pickle.load(f)


#################### Vibration analysis ######################
solve_subset = [0, 25]     # Solve for the first 26 modes
VIB = VIBframe(X, C, mprop, bound, spring_support,solve_subset)


###################### Store and load data ###################
# Store the VIB object in the database
basestore(VIB, name='VIB_DataBase.db')

################## Generate output files #####################
output(VIB,"VIB_results.txt")

v = np.tile([0, 0, 1, 0, 0, 0], VIB.nno)  # Define a velocity vector for the first node
print(v.T @ VIB.M @ v)  # Calculate the kinetic energy for the first node