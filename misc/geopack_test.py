def t89c(points, iopt=0, ps=0.0):

    import numpy as np
    from geopack.geopack import dip, recalc
    from geopack import t89

    ut = 100    # 1970-01-01/00:01:40 UT.

    ps = recalc(ut)
    print(ps)

    B = np.zeros(points.shape)
    for i in range(points.shape[0]):
        r = np.linalg.norm(points[i,:])
        if r < 1:
            B[i,0] = np.nan
            B[i,1] = np.nan
            B[i,2] = np.nan
        else:
            b0xgsm,b0ygsm,b0zgsm = dip(points[i,0], points[i,1], points[i,2])
            dbxgsm,dbygsm,dbzgsm = t89.t89(2, ps, points[i,0], points[i,1], points[i,2])
            B[i,0] = b0xgsm + dbxgsm
            B[i,1] = b0ygsm + dbygsm
            B[i,2] = b0zgsm + dbzgsm

    return B

import numpy as np
print(t89c(np.ones((2,3))))