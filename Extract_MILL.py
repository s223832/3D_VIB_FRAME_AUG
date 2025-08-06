# File to extract the data from the mill model for 3D Truss

# Import packages
import numpy as np
from functions.plot.plotconnectivity import plotconnectivity
from functions.plot.plotmodeshapes import plotmodeshapes
from classes.VIBframe import VIBframe
from functions.plot.utils import plotSettings
import math

# Steel properties
E = 210e9
rho = 8500
G = E/(2*(1+0.3))

# Build the mprop dictionary
mprop = {}
A = [1.746251135, 1.584569069, 1.430398551, 1.283447413, 1.173070697, 1.039640974, 0.913581427, 0.794989446, 0.681637641]
I = [25.9298216, 21.87108746, 18.30480114, 15.17937956, 12.77823344, 10.39595554, 8.354127163, 6.621817883, 5.116353816]
J = [51.8596432, 43.74217493, 36.60960228, 30.35875912, 25.55646688, 20.79191109, 16.70825433, 13.24363577, 10.23270763]

for i in range(1, 10):
    mprop[i] = {'E': E, 'A': A[i-1], 'rho': rho, 'Iy': I[i-1], 'Iz': I[i-1], 'J': J[i-1], 'G': 8.08e10, 'type': f'Tower element {i}'}   # Tower element

# Define boundary conditions 
bound = np.array([[1, 1, 0.0],
                  [1, 2, 0.0],
                  [1, 3, 0.0],
                  [1, 4, 0.0],
                  [1, 5, 0.0],
                  [1, 6, 0.0]])

spring_support = []

# Define X and C matrices
offset = 0.0
X = np.array([[0, 0, offset],
            [0, 0, offset + 6.14],
            [0, 0, offset + 6.14+16.26*1],
            [0, 0, offset + 6.14+16.26*2],
            [0, 0, offset + 6.14+16.26*3],
            [0, 0, offset + 6.14+16.26*4],
            [0, 0, offset + 6.14+16.26*5],
            [0, 0, offset + 6.14+16.26*6],
            [0, 0, offset + 6.14+16.26*7],
            [0, 0, offset + 6.14+16.26*7+17.17]])

C = np.array([[1, 2, 1],
            [2, 3, 2],
            [3, 4, 3],
            [4, 5, 4],
            [5, 6, 5],
            [6, 7, 6],
            [7, 8, 7],
            [8, 9, 8],
            [9, 10, 9]])


#################### Run program to extract data ########################
VIB = VIBframe(X, C, mprop, bound, spring_support)

print(VIB.K.shape)
print(f"Natural Freq.: {VIB.omega/(2*math.pi)} Hz")
for i in range(20):
    plotmodeshapes(VIB, i, 5)

L = X[0,:] - X[-1,:]
L = np.linalg.norm(L)
frequency1_exact = (1.87510407/L)**2 * math.sqrt(mprop[1]['E']*mprop[1]['Iy']/(mprop[1]['rho']*mprop[1]['A']))  # First Bending mode

print(f"Frequency 1: {VIB.omega[0]}")
print(f"Exact Frequency 1: {frequency1_exact}")