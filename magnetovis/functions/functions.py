def circle(Npts, radius=1.0, origin=(0.0, 0.0, 0.0), orientation=(0, 0, 1)):

    import numpy as np

    idx = np.arange(Npts)

    points = np.zeros((Npts, 3))
    points[:,0] = origin[0] + radius*np.cos(idx*2*np.pi/Npts)
    points[:,1] = origin[1] + radius*np.sin(idx*2*np.pi/Npts)

    if not np.all(np.array(orientation) == np.array((0, 0, 1))):
        pass # TODO: Rotate

    points[:,2] = origin[2]

    return points

def helix(Npts, radius=1.0, length=10, rounds=3):

    import numpy as np

    idx = np.arange(Npts)

    points = np.full((Npts, 3), np.nan)
    points[:,0] = idx*length/(Npts-1)
    points[:,1] = radius*np.sin(idx*rounds*2*np.pi/Npts)
    points[:,2] = radius*np.cos(idx*rounds*2*np.pi/Npts)

    return points


def curve(Npts, coord_sys="GSM"):
    import numpy as np

    points = np.zeros((Npts,3))
    points[:,0] = np.arange(Npts)
    points[:,1] = np.zeros(Npts)
    points[:,2] = np.zeros(Npts)

    return points


def position(points, coord_sys="GSM"):
    return points


def radius(points):
    import numpy as np
    r = np.linalg.norm(points, axis=1)
    return r


def IGRF(points, time="2001-01-01", coord_sys="GSM"):

    import numpy as np
    M=7.788E22
    r = np.linalg.norm(points, axis=1)
    B = np.zeros(points.shape)
    r[r < 1] = np.nan
    B[:,0] = 3*M*points[:,0]*points[:,2]/r**5 # Bx = 3*M*x*z/r^5
    B[:,1] = 3*M*points[:,1]*points[:,2]/r**5 # By = 3*M*y*z/r^5
    B[:,2] = M*(3*points[:,2]**2-r**2)/r**5   # Bz = M(3*z^2 - r^2)/r^5

    return B


def T01(points, M=7.788E22, parmod=None, ps=0.0):

    import numpy as np
    r = np.linalg.norm(points, axis=1)
    B = np.zeros(points.shape)
    r[r < 1] = np.nan
    B[:,0] = 3*M*points[:,0]*points[:,2]/r**5 # Bx = 3*M*x*z/r^5
    B[:,1] = 3*M*points[:,1]*points[:,2]/r**5 # By = 3*M*y*z/r^5
    B[:,2] = M*(3*points[:,2]**2-r**2)/r**5   # Bz = M(3*z^2 - r^2)/r^5

    return B


def T89c(points, iopt=0, ps=0.0):

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
            dbxgsm,dbygsm,dbzgsm = t89.t89(iopt, ps, points[i,0], points[i,1], points[i,2])
            B[i,0] = b0xgsm + dbxgsm
            B[i,1] = b0ygsm + dbygsm
            B[i,2] = b0zgsm + dbzgsm

    return B


def dipole(points, M=7.788E22):
    import numpy as np
    r = np.linalg.norm(points, axis=1)
    B = np.zeros(points.shape)
    r[r < 1] = np.nan
    #r[r==0] = np.nan
    B[:,0] = 3*M*points[:,0]*points[:,2]/r**5 # Bx = 3*M*x*z/r^5
    B[:,1] = 3*M*points[:,1]*points[:,2]/r**5 # By = 3*M*y*z/r^5
    B[:,2] = M*(3*points[:,2]**2-r**2)/r**5   # Bz = M(3*z^2 - r^2)/r^5

    return B
