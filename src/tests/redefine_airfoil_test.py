import sys
sys.path.append('./src/')

import pyfoam
import numpy as np

if __name__ == '__main__':
    foil = np.loadtxt('./data/NACA-0009.txt', skiprows=1)
    model = pyfoam.redefine_airfoil(foil, refinement=0)
    model.view