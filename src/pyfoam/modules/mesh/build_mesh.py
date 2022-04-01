from numpy import ndarray

from pyfoam.models.abstract import model
from pyfoam.modules.mesh.utilities.quad_mesh import quad_mesh
from pyfoam.modules.mesh.utilities.tri_mesh import tri_mesh
from pyfoam.modules.mesh.utilities.view import view


class build_mesh(model):
    
    @model.action
    def __init__(self, foil: ndarray,
                       bl_height: float,
                       bl_expansion_ratio: float,
                       bl_first_element: float,
                       external_radius: float,
                       external_n: int,
                       trailing_edge_points: int = 5) -> None:
        
        self.__foil: ndarray = foil
        self.__bl_height: float = bl_height
        self.__bl_expansion_ratio: float = bl_expansion_ratio
        self.__bl_first_element: float = bl_first_element
        self.__trailing_edge_points: int = trailing_edge_points
        self.__external_radius: float = external_radius
        self.__external_n: float = external_n

        self.__vertices: ndarray = None
        self.__tri_faces: ndarray = None
        self.__quad_faces: ndarray = None
        super().__init__()
        return
    
    @model.action
    def update_foil(self, value: ndarray) -> None:
        self.__foil = value
        return
    
    @model.action
    def update_bl_height(self, value: float) -> None:
        self.__bl_height = value
        return
    
    @model.action
    def update_bl_expansion_ratio(self, value: float) -> None:
        self.__bl_expansion_ratio = value
        return
    
    @model.action
    def update_bl_first_element(self, value: float) -> None:
        self.__bl_first_element = value
        return
    
    @model.action
    def update_external_radius(self, value: float) -> None:
        self.__external_radius = value
        return
    
    @model.action
    def update_external_expansion_ratio(self, value: float) -> None:
        self.__external_expansion_ratio = value
        return

    @property
    def view(self) -> None:
        view(self.__vertices, self.__quad_faces, self.__tri_vert, self.__tri_faces)
        return
    
    @property
    def vertices(self) -> ndarray:
        return self.__vertices
    
    @property
    def tri_faces(self) -> ndarray:
        return
    
    @property
    def quad_faces(self) -> ndarray:
        return self.__quad_faces

    def run(self) -> None:

        # Boundary leyer mesh
        quad = quad_mesh(
            self.__foil, self.__bl_height,
            self.__bl_expansion_ratio,
            self.__bl_first_element,
            self.__trailing_edge_points,
        )

        self.__vertices, self.__quad_faces, quad_n = quad.build()
        a = self.__vertices[-quad_n:, :]

        # Enternal mesh
        tri = tri_mesh(
            self.__vertices[-quad_n:, :],
            self.__external_n,
            self.__external_radius,
        )

        self.__tri_vert, self.__tri_faces = tri.build()

        return