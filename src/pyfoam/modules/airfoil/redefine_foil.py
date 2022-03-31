from numpy import ndarray, copy, mean

from pyfoam.models.abstract import model
from pyfoam.modules.airfoil.utilities.curvature import curvature
from pyfoam.modules.airfoil.utilities.spring_coeff import spring_coeff
from pyfoam.modules.airfoil.utilities.interpolate_and_refine import interpolate_and_refine
from pyfoam.modules.airfoil.utilities.view import view


class redefine_airfoil(model):
    """
    Redefine the airfoil based on the refinement factor (refinement) and
    surface number of points (n).
    """

    @model.action
    def __init__(self, foil: ndarray,
                       refinement: float = 10.0,
                       n: int = None) -> None:
        self.__foil: ndarray = copy(foil)
        self.__foil[:, 0] = self.__foil[:, 0] - mean(self.__foil[:, 0])
        self.__foil[:, 1] = self.__foil[:, 1] - mean(self.__foil[:, 1])
        self.__refinement: float = refinement
        self.__n: int = n if n is not None else len(foil[:, 0])
        return
    
    @model.action
    def update_refinement(self, value: float) -> None:
        self.__refinement = value
        return
    
    @model.action
    def update_n(self, value: int) -> None:
        self.__n = value
        return
    
    @property
    def view(self) -> None:
        view(self.__foil)
        return

    @property
    def points(self) -> ndarray:
        return self.__foil
    
    def run(self) -> None:
        
        # Curvature
        curv = curvature(self.__foil)

        # Spring coefficient
        spring = spring_coeff(curv, self.__refinement)

        # Calculate the new curve
        new_curve = interpolate_and_refine(self.__foil, spring, self.__n)
        
        # Refine
        self.__foil = copy(new_curve)

        return