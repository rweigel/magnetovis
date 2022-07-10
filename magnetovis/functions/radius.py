def radius(points):
    import numpy as np
    r = np.linalg.norm(points, axis=1)
    return r
