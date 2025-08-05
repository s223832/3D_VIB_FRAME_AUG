import numpy as np

def Bint(s, L):
   """Strain interpolation for a beam element in local coordinates
   Parameters
   ----------
   s : float
      Local coordinate (interpolation point)

   Returns
   -------
   B : np.array
      Strain interpolation matrix
   """
   
   # Functions defined for interpolation matrix
   B1 = -1/L
   B4 = 1/L
   B2 = 6*s/L**2
   B3 = (-1 + 3*s)/L
   B5 = -6*s/L**2
   B6 = (1 + 3*s)/L

   # Build strain interpolation matrix
   B = np.array([[B1, 0,  0,  0,  0,  0,  B4, 0,  0,  0,  0,  0 ],
                 [0,  B2, 0,  0,  0,  B3, 0,  B5, 0,  0,  0,  B6],
                 [0,  0,  B2, 0, -B3, 0,  0,  0,  B5, 0, -B6, 0 ],
                 [0,  0,  0,  B1, 0,  0,  0,  0,  0,  B4, 0,  0 ]])
   
   return B