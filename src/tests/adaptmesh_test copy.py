def main():
    import meshpy.triangle as triangle
    import numpy as np

    points = [(1, 1), (-1, 1), (-1, -1), (1, -1)]

    for pt in np.random.randn(100, 2):
        points.append(pt * 0.1)

    def round_trip_connect(start, end):
        result = []
        for i in range(start, end):
            result.append((i, i + 1))
        result.append((end, start))
        return result

    info = triangle.MeshInfo()
    info.set_points(points)
    info.set_facets(round_trip_connect(0, 3))

    mesh = triangle.build(
        info, allow_volume_steiner=False, allow_boundary_steiner=False
    )

    mesh_points = np.array(mesh.points)
    mesh_tris = np.array(mesh.elements)

    import matplotlib.pyplot as pt

    pt.triplot(mesh_points[:, 0], mesh_points[:, 1], mesh_tris)
    pt.axis('equal')
    pt.grid()
    pt.show()


if __name__ == "__main__":
    main()