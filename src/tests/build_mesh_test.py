import sys
sys.path.append('./src/')

import pyfoam
import numpy as np

if __name__ == '__main__':
    foil = np.loadtxt('./data/NACA-6409.txt', skiprows=1)
    model = pyfoam.redefine_airfoil(foil, refinement=10, n=100)
    
    mesh = pyfoam.build_mesh(model.points, 0.1, 1.1, 1e-2, 50, 20, trailing_edge_points=10)
    mesh.view