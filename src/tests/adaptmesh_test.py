import meshpy.triangle as triangle
import numpy as np
import numpy.linalg as la


def round_trip_connect(start, end):
    return [(i, i + 1) for i in range(start, end)] + [(end, start)]


def main():
    points = [(1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)]
    facets = round_trip_connect(0, len(points) - 1)

    circ_start = len(points)
    points.extend(
        (3 * np.cos(angle), 3 * np.sin(angle))
        for angle in np.linspace(0, 2 * np.pi, 100, endpoint=False)
    )

    facets.extend(round_trip_connect(circ_start, len(points) - 1))

    def needs_refinement(vertices, area):
        bary = np.sum(np.array(vertices), axis=0) / 3
        max_area = 0.001 + (la.norm(bary, np.inf) - 1) * 0.05
        return bool(area > max_area)

    info = triangle.MeshInfo()
    info.set_points(points)
    info.set_holes([(0, 0)])
    info.set_facets(facets)

    mesh = triangle.build(info, min_angle=35, quality_meshing=0.9, mesh_order=0.5)

    mesh_points = np.array(mesh.points)
    mesh_tris = np.array(mesh.elements)

    import matplotlib.pyplot as pt

    pt.triplot(mesh_points[:, 0], mesh_points[:, 1], mesh_tris)
    pt.axis('equal')
    pt.grid()
    pt.show()


if __name__ == "__main__":
    main()