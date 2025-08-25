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
spring_support = []
bound = []
# bound = np.array([[117, 1, 0.0],
#                  [117, 2, 0.0],
#                  [117, 3, 0.0],
#                  [118, 1, 0.0],
#                  [118, 2, 0.0],
#                  [118, 3, 0.0],
#                  [119, 1, 0.0],
#                  [119, 2, 0.0],
#                  [119, 3, 0.0],
#                  [120, 1, 0.0],
#                  [120, 2, 0.0],
#                  [120, 3, 0.0]])

# kxx = 1.5e8
# kyy = 1.5e8
# kzz = 1.5e8
# spring_support = np.array([[125, 1 , kxx],
#                            [125, 2 , kyy],
#                            [125, 3 , kzz]])

####################### Import indata ######################
X = np.load('indata_X.npy')
C = np.load('indata_C.npy')
# Load the dictionary from the file using pickle
with open('indata_mprop.pkl', 'rb') as f:
    mprop = pickle.load(f)


#################### Vibration analysis ######################
solve_subset = [0, 25]     # Solve for the first 25 modes
VIB = VIBframe(X, C, mprop, bound, spring_support,solve_subset)


###################### Store and load data ###################
# Store the VIB object in the database
basestore(VIB, name='VIB_DataBase.db')

################## Generate output files #####################
output(VIB,"VIB_results.txt")
