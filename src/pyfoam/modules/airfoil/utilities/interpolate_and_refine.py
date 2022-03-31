from scipy.interpolate import splprep, splev, interp1d
from scipy.optimize import fsolve
from numpy import asarray, linspace, ndarray, zeros


def __func(x, *data):
    
    spring_func, n = data

    eqs = [0 for _ in range(n)]

    for i in range(n):
        if i == 0:
            k_minus = 0.5 * ( spring_func(0) + spring_func(x[0]) )
            k_plus = 0.5 * ( spring_func(1) + spring_func(x[n - 1]) )
            eqs[i] = k_plus * ( x[1] - x[0] ) - k_minus * ( x[0] - 0 )
        elif i == n - 1:
            k_minus = 0.5 * ( spring_func(x[n - 2]) + spring_func(x[n - 1]) )
            k_plus = 0.5 * ( spring_func(x[n - 1]) + spring_func(1) )
            eqs[i] = k_plus * ( 1 - x[n - 1] ) - k_minus * ( x[n - 1] - x[n - 2] )
        else:
            k_minus = 0.5 * ( spring_func(x[i]) + spring_func(x[i - 1]) )
            k_plus = 0.5 * ( spring_func(x[i]) + spring_func(x[i + 1]) )
            eqs[i] = k_plus * ( x[i + 1] - x[i] ) - k_minus * ( x[i] - x[i - 1] )

    return eqs

def interpolate_and_refine(curve: ndarray,
                           spring: ndarray,
                           n: int) -> ndarray:

    # Curve interpolation
    tck, u = splprep([curve[:, 0], curve[:, 1]], s=0)
    
    # Spring function
    u_interp = asarray([-1] + u.tolist() + [2])
    spring_interp = asarray([spring[0]] + spring.tolist() + [spring[len(spring) - 1]])
    spring_func = interp1d(u_interp, spring_interp)

    # Optimize position
    du = 1 / (n - 1)
    x0 = linspace(du, 1 - du, num=n - 2)
    sol = fsolve(__func, x0, (spring_func, n - 2))

    # # Interpolate airfoil
    tulple_points = splev(asarray([0] + sol.tolist() + [1]), tck)
    new_points = zeros((n, 2))
    new_points[:, 0], new_points[:, 1] = asarray(list(tulple_points[0])), asarray(list(tulple_points[1]))

    return new_points