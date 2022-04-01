from typing import List
from numpy import asarray, copy, concatenate, delete, ndarray, isclose, power, zeros
from numpy.linalg import norm

import matplotlib.pyplot as plt

class quad_mesh:

    def __init__(self, foil: ndarray,
                       bl_height: float,
                       bl_expansion_ratio: float,
                       bl_first_element: float,
                       trailing_edge_points: int) -> None:
        
        self.__foil: ndarray = foil
        self.__bl_height: float = bl_height
        self.__bl_expansion_ratio: float = bl_expansion_ratio
        self.__bl_first_element: float = bl_first_element
        self.__trailing_edge_points: int = trailing_edge_points
        self.__n = len(self.__foil[:, 0])

        return
    
    def build(self) -> List[ndarray]:

        # Verify if the start and end point are equal end add the trailing edge points
        if not False in isclose(self.__foil[0, :], self.__foil[self.__n - 1, :], rtol=1e-8):
            self.__foil = delete(self.__foil, self.__n - 1, 0)
            self.__n += -1
        else:
            vec = (self.__foil[0, :] - self.__foil[self.__n - 1, :]) / (self.__trailing_edge_points - 1)
            te_points = zeros((self.__trailing_edge_points - 2, 2))
            for i in range(self.__trailing_edge_points - 2):
                te_points[i, :] = self.__foil[self.__n - 1, :] + vec * (i + 1)
            self.__foil = concatenate([self.__foil, te_points])
            self.__n += self.__trailing_edge_points - 2

        # Create layers
        vertices = []
        faces = []
        height = 0.0
        height_increment = 0.0
        curve = copy(self.__foil)
        count = 0

        while height <= self.__bl_height or count == 1:

            # Normals
            normals = self.__normals(curve, count)

            # Increment
            inc = normals * height_increment

            # Layer
            curve = curve + inc

            # Save vertices
            for i in range(self.__n):
                vertices.append([curve[i, 0], curve[i, 1]])
            
            # Save face
            if count != 0:
                for i in range(self.__n):
                    if i == self.__n - 1:
                        faces.append([i + self.__n * (count - 1), i + self.__n * count, self.__n * count, self.__n * (count - 1)])
                    else:
                        faces.append([i + self.__n * (count - 1), i + self.__n * count, i + self.__n * count + 1, i + 1 + self.__n * (count - 1)])

            # Next increment
            height_increment = self.__layer_increment(count)
            height += height_increment
            count += 1

        return [asarray(vertices), asarray(faces), self.__n]
    
    def __layer_increment(self, index: int) -> float:
        return self.__bl_first_element * (self.__bl_expansion_ratio ** index)
    
    def __normals(self, curve: ndarray, count: int) -> ndarray:

        x_new = asarray([[curve[self.__n - 1, 0]] + curve[:, 0].tolist() + [curve[0, 0]]]).reshape(self.__n + 2)
        y_new = asarray([[curve[self.__n - 1, 1]] + curve[:, 1].tolist() + [curve[0, 1]]]).reshape(self.__n + 2)
        new_curve = zeros((self.__n + 2, 2))
        new_curve[:, 0], new_curve[:, 1] = x_new, y_new

        dx_1 = x_new[1:self.__n + 1] - x_new[0:self.__n]
        dy_1 = y_new[1:self.__n + 1] - y_new[0:self.__n]
        dx_2 = x_new[2:] - x_new[1:self.__n + 1]
        dy_2 = y_new[2:] - y_new[1:self.__n + 1]
        l_1 = power(power(dx_1, 2) + power(dy_1, 2), 0.5)
        l_2 = power(power(dx_2, 2) + power(dy_2, 2), 0.5)

        dx = dx_1 / l_1 + dx_2 / l_2
        dy = dy_1 / l_1 + dy_2 / l_2
        l = power(power(dx, 2) + power(dy, 2), 0.5)

        normals = zeros((self.__n, 2))
        normals[:, 0], normals[:, 1] = dy / l, - dx / l

        if count == 1:
            n = self.__trailing_edge_points - 2
            f_1 = normals[0, :]
            vecs = normals[self.__n - n:, :]
            f_2 = normals[self.__n - 1 - n, :]

            aux = copy(vecs)
            for _ in range(10):
                for i in range(len(vecs[:, 0])):
                    if i == 0:
                        aux[i, :] = (f_2 + vecs[i, :] + vecs[i + 1, :]) / norm(f_2 + vecs[i, :] + vecs[i + 1, :])
                    elif i == len(vecs[:, 0]) - 1:
                        aux[i, :] = (vecs[i - 1, :] + vecs[i, :] + f_1) / norm(vecs[i - 1, :] + vecs[i, :] + f_1)
                    else:
                        aux[i, :] = (vecs[i - 1, :] + vecs[i, :] + vecs[i + 1, :]) / norm(vecs[i - 1, :] + vecs[i, :] + vecs[i + 1, :])
                    vecs = copy(aux)

            for i in range(len(vecs[:, 0])):
                normals[self.__n - i - 1, :] = vecs[n - i - 1, :]

        return normals