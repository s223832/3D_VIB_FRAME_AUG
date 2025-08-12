############################## FEM and Dynamic Analysis ###############################
# Import packages
import numpy as np
import pickle

# Import functions for data
from functions.data.output import output

# Import classes
from classes.VIBframe import VIBframe

# Import functions for datastoring
from functions.data.basestore import basestore

################# Boundary conditions #####################
# Boundary conditions mat(node,ldof,disp)
#bound = np.array([[ 37 , 3 , 0.0 ],
#                  [ 38 , 3 , 0.0 ],
#                  [ 39 , 3 , 0.0 ],
#                  [ 40 , 3 , 0.0 ]])

# bound = np.array([[117, 1, 0.0],
#                  [117, 2, 0.0],
#                  [117, 3, 0.0],
#                  [117, 4, 0.0],
#                  [117, 5, 0.0],
#                  [117, 6, 0.0],
#                  [118, 1, 0.0],
#                  [118, 2, 0.0],
#                  [118, 3, 0.0],
#                  [118, 4, 0.0],
#                  [118, 5, 0.0],
#                  [118, 6, 0.0],
#                  [119, 1, 0.0],
#                  [119, 2, 0.0],
#                  [119, 3, 0.0],
#                  [119, 4, 0.0],
#                  [119, 5, 0.0],
#                  [119, 6, 0.0],
#                  [120, 1, 0.0],
#                  [120, 2, 0.0],
#                  [120, 3, 0.0],
#                  [120, 4, 0.0],
#                  [120, 5, 0.0],
#                  [120, 6, 0.0]])

spring_support = []
bound =[]

# Uncomment the following lines to define spring supports
# Spring supports mat(node, ldof, stiffness)
    #bound = []

# kzz = 1.50e6

# spring_support = np.array([[ 37 , 3 , kzz],
#                            [ 38 , 3 , kzz],
#                            [ 39 , 3 , kzz],
#                            [ 40 , 3 , kzz]])

####################### Import indata ######################
X = np.load('indata_X.npy')
C = np.load('indata_C.npy')
# Load the dictionary from the file using pickle
with open('indata_mprop.pkl', 'rb') as f:
    mprop = pickle.load(f)


#################### Vibration analysis ######################
solve_subset = [0, 30]     # Solve for the first 30 modes
VIB = VIBframe(X, C, mprop, bound, spring_support,solve_subset)


###################### Store and load data ###################
# Store the VIB object in the database
basestore(VIB, name='VIB_DataBase.db')

################## Generate output files #####################
output(VIB,"VIB_results.txt")

v = np.tile([0, 0, 1, 0, 0, 0], VIB.nno)  
print(v.T @ VIB.M @ v)  # Calculate the total mass of the structure

