from numpy import gradient, ndarray, abs

def curvature(curve: ndarray) -> ndarray:

    # Curvature
    x_t = gradient(curve[:, 0])
    y_t = gradient(curve[:, 1])

    xx_t = gradient(x_t)
    yy_t = gradient(y_t)

    curv = abs(xx_t * y_t - x_t * yy_t) / (x_t * x_t + y_t * y_t)**1.5

    return curv