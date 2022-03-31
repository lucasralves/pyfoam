import matplotlib.pyplot as plt
from numpy import ndarray

def view(foil: ndarray) -> None:
    plt.figure()
    plt.plot(foil[:, 0], foil[:, 1])
    plt.scatter(foil[:, 0], foil[:, 1])
    plt.grid()
    plt.axis('equal')
    plt.show()
    return