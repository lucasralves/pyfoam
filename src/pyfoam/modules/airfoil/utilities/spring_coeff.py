from numpy import copy, ndarray, max, exp, linspace, flip, zeros

def spring_coeff(curvature: ndarray,
                 factor: float) -> ndarray:

    # Number of points
    n = len(curvature)

    # Normalize
    curvature = curvature / max(curvature)

    # Remove border values
    exp_var = exp( - linspace(0, 25, num=n) )
    div = exp_var + flip(exp_var)
    curvature = curvature / (1e3 * div + 1)

    # Smooth curvature
    smooth_curv = zeros(n)

    for _ in range(10):

        for i in range(n):
            if i == 0:
                smooth_curv[i] = (curvature[i] + curvature[i + 1] + curvature[i + 2]) / 3
            elif i == n - 1:
                smooth_curv[i] = (curvature[i - 2] + curvature[i - 1] + curvature[i]) / 3
            else:
                smooth_curv[i] = (curvature[i - 1] + curvature[i] + curvature[i + 1]) / 3
        
        curvature = copy(smooth_curv)
    
    # Normalize again
    curvature = curvature / max(curvature)

    # Border
    curvature = curvature + div
    
    # # Refinement factor
    curvature = 1 + curvature * factor

    return curvature