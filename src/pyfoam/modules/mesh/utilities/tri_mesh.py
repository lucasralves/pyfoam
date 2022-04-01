from typing import List
from numpy import array, asarray, cos, linspace, ndarray, pi, power, sin, sum
from numpy.linalg import norm
import meshpy.triangle as triangle


class tri_mesh:

    def __init__(self, surf_points: ndarray, external_n: float, external_radius: float) -> None:
        self.__surf_points = surf_points
        self.__external_n = external_n
        self.__external_radius = external_radius
        return
    
    def __round_trip_connect(self, start, end):
        return [(i, i + 1) for i in range(start, end)] + [(end, start)]

    def build(self) -> List[ndarray]:

        # Refinement
        dif_x = self.__surf_points[1:, 0] - self.__surf_points[:len(self.__surf_points) - 1, 0]
        dif_y = self.__surf_points[1:, 1] - self.__surf_points[:len(self.__surf_points) - 1, 1]
        max_l_surf = max(power(power(dif_x, 2) + power(dif_y, 2), 0.5))
        max_l_ext = 2 * pi * self.__external_radius / (self.__external_n - 1)

        max_area_surf = max_l_surf * max_l_surf * (3 ** 0.5) / 4
        max_area_ext = max_l_ext * max_l_ext * (3 ** 0.5) / 4

        # Mesh
        points = []  
        for i in range(len(self.__surf_points)):
            points.append((self.__surf_points[i, 0], self.__surf_points[i, 1]))
        
        points.append((self.__surf_points[0, 0], self.__surf_points[0, 1]))

        circ_start = len(points)
        facets = self.__round_trip_connect(0, circ_start - 1)

        points.extend(
            (self.__external_radius * cos(angle), self.__external_radius * sin(angle))
            for angle in linspace(0, 2 * pi, self.__external_n, endpoint=False)
        )
        facets.extend(self.__round_trip_connect(circ_start, len(points) - 1))

        info = triangle.MeshInfo()
        info.set_points(points)
        info.set_holes([(0, 0)])
        info.set_facets(facets)

        def needs_refinement(vertices, area):
            v = asarray(vertices)
            center = (v[0, :] + v[1, :] + v[2, :]) / 3
            dist = norm(center)
            dist = 0 if dist < 0.5 else dist - 0.5
            max_area = max_area_surf + (max_area_ext - max_area_surf) * ((dist / (self.__external_radius - 0.5)) ** 3)

            return bool(area > max_area * 1.1)

        mesh = triangle.build(info, quality_meshing=0.9, min_angle=25, refinement_func=needs_refinement)

        mesh_points = array(mesh.points)
        mesh_tris = array(mesh.elements)

        return mesh_points, mesh_tris