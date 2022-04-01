import matplotlib.pyplot as plt
from numpy import ndarray

def view(vertices: ndarray, quad_faces: ndarray, tri_vert, tri_faces) -> None:
    plt.figure()
    
    for i in range(len(quad_faces[:, 0])):
        i = quad_faces[i, :]
        plt.plot([vertices[i[0], 0], vertices[i[1], 0], vertices[i[2], 0], vertices[i[3], 0], vertices[i[0], 0]], [vertices[i[0], 1], vertices[i[1], 1], vertices[i[2], 1], vertices[i[3], 1], vertices[i[0], 1]], 'k')
        plt.fill([vertices[i[0], 0], vertices[i[1], 0], vertices[i[2], 0], vertices[i[3], 0], vertices[i[0], 0]], [vertices[i[0], 1], vertices[i[1], 1], vertices[i[2], 1], vertices[i[3], 1], vertices[i[0], 1]], 'b', alpha=0.5)

    for i in range(len(tri_faces[:, 0])):
        i = tri_faces[i, :]
        plt.plot([tri_vert[i[0], 0], tri_vert[i[1], 0], tri_vert[i[2], 0], tri_vert[i[0], 0]], [tri_vert[i[0], 1], tri_vert[i[1], 1], tri_vert[i[2], 1], tri_vert[i[0], 1]], 'k')
        plt.fill([tri_vert[i[0], 0], tri_vert[i[1], 0], tri_vert[i[2], 0], tri_vert[i[0], 0]], [tri_vert[i[0], 1], tri_vert[i[1], 1], tri_vert[i[2], 1], tri_vert[i[0], 1]], 'r', alpha=0.5)

    plt.grid()
    plt.axis('equal')
    plt.show()
    return