def linspace(dimensions, starts=(0.0, 0.0, 0.0), stops=(1.0, 1.0, 1.0), grid_type='structured'):

    import numpy as np

    assert len(dimensions) == len(starts) == len(stops), "Required: len(dimensions) == len(starts) == len(stops)" 

    x = np.linspace(starts[0], stops[0], dimensions[0])
    y = np.linspace(starts[1], stops[1], dimensions[1])

    if len(starts) == 2:
        if grid_type == 'rectilinear':
            points = {'x': x, 'y': y}
        else:
            X, Y = np.meshgrid(x, y, indexing='xy')
            points = np.column_stack([X.flatten(), Y.flatten()])
        
        return points

    z = np.linspace(starts[2], stops[2], dimensions[2])

    if grid_type == 'rectilinear':
        return {'x': x, 'y': y, 'z': z}

    Y, Z, X = np.meshgrid(y, z, x)

    points = np.column_stack([X.flatten(), Y.flatten(), Z.flatten()])

    # Points has x varying the fastest, then y, then z
    return points

def cylinder(dimensions, radius=1.0, origin=(0.0, 0.0, 0.0)):

    import numpy as np

    N = dimensions

    r = 1+radius*np.arange(0, N[0], dtype=np.float)
    #print(r)
    theta = np.pi*np.arange(0, N[1], dtype=np.float)/(N[1]-1)
    #print(theta)
    phi = 2*np.pi*np.arange(0, N[2], dtype=np.float)/(N[2]-1)
    #print(phi)

    xax = np.arange(N[0])
    yax = np.arange(N[1])
    zax = np.arange(N[2])
    Y, Z, X = np.meshgrid(yax, zax, xax)
    S = np.sqrt(X**2 + Y**2)
    Sf = np.floor(np.sqrt(X**2 + Y**2))
    Phi = np.arccos(X/S)
    Phi = np.nan_to_num(Phi, nan=0.0)
    Xc = Sf*np.cos(Phi)
    Yc = Sf*np.sin(Phi)
    points2 = np.column_stack([X.flatten(), Y.flatten(), Z.flatten(), Sf.flatten(), (180/np.pi)*Phi.flatten(), Xc.flatten(), Yc.flatten()])
    points = np.column_stack([X.flatten(), Y.flatten(), Z.flatten()])
    points = np.column_stack([Xc.flatten(), Yc.flatten(), Z.flatten()])

    #np.set_printoptions(precision=1, suppress=True)
    #print(points2)

    #points[0] = points[0]*np.sin(points[1])*np.cos(points[2])
    #points[1] = points[0]*np.sin(points[1])*np.sin(points[2])
    #points[2] = points[0]*np.cos(points[2])

    return points

def circle(Npts, radius=1.0, origin=(0.0, 0.0, 0.0), orientation=(0.0, 0.0, 1.0)):

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


def position(points):
    return points


def radius(points):
    import numpy as np
    r = np.linalg.norm(points, axis=1)
    return r


def IGRF(points, time="2001-01-01"):

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


def t89c(points, ut=100, iopt=0, ps=0.0):

    import numpy as np
    from geopack import geopack
    from geopack import t89

    # ut = 100  => # 1970-01-01/00:01:40 UT.

    print(ps)
    import datetime
    ut = (datetime.datetime(2001,1,1,2,3,4)-datetime.datetime(1970,1,1)).total_seconds()    
    #ut = 100
    ps = geopack.recalc(ut)
    print(ps*180.0/np.pi)
    print(geopack.dip(-5.1,0.3,2.8))
    print(geopack.igrf_gsm(-5.1,0.3,2.8))
    B = np.zeros(points.shape)
    for i in range(points.shape[0]):
        r = np.linalg.norm(points[i,:])
        if r < 1:
            B[i,0] = np.nan
            B[i,1] = np.nan
            B[i,2] = np.nan
        else:
            b0xgsm,b0ygsm,b0zgsm = geopack.igrf_gsm(points[i,0], points[i,1], points[i,2])
            dbxgsm,dbygsm,dbzgsm = t89.t89(iopt, ps, points[i,0], points[i,1], points[i,2])
            B[i,0] = b0xgsm + dbxgsm
            B[i,1] = b0ygsm + dbygsm
            B[i,2] = b0zgsm + dbzgsm

    return B


def magnetic_dipole(r, m=[0, 0, 1], vectorized=True):

    # Coordinate-free form of B for magnetic dipole
    # B = k_m ( 3(m dot r_hat)r_hat - m )/|r|^3
    #   = k_m ( 3(m dot r)r/|r|^5 - m/|r|^3 )
    #   = k_m ( 3(m_x*r_x + m_y*r_y + m_z*r_z)r - m/|r|^3)
    # 
    # where
    # r = [x, y, z]
    # k_m = mu_o/4\pi = 1e-7 [H/m] ([H/m] = [N/A^2])

    import numpy as np

    k_m = 1e-7

    r = np.array(r)

    if vectorized == True:
        r_mag = np.linalg.norm(r, axis=1)
        r_mag = np.reshape(r_mag, (r_mag.shape[0], 1))
        r_mag = np.tile(r_mag, (1, 3))
        m_dot_r = np.dot(r, m)
        m_dot_r = np.reshape(m_dot_r, (m_dot_r.shape[0], 1))
        m_dot_r = np.tile(m_dot_r, (1, 3))
        m = np.tile(m, (r.shape[0], 1))
        return k_m * ( 3.0*(m_dot_r/np.power(r_mag, 5.0))*r - m/np.power(r_mag, 3.0) )
    else:
        B = np.full(r.shape, np.nan)
        for i in range(r.shape[0]):
            r_mag = np.linalg.norm(r[i,:], axis=0)
            for j in range(3):
                B[i,j] = k_m*(  3*(m[0]*r[i,0] + m[1]*r[i,1] + m[2]*r[i,2])*r[i,j]/np.power(r_mag, 5) \
                              - m[j]/np.power(r_mag, 5) )
        return B

if False:
    print(magnetic_dipole([[1, 0, 0], [-1, 0, 0]], m=[1, 0, 0], vectorized=False))
    print(magnetic_dipole([[1, 0, 0], [-1, 0, 0]], m=[1, 0, 0], vectorized=True))

    print(magnetic_dipole([[0, 1, 0], [0, -1, 0]], m=[0, 1, 0], vectorized=False))
    print(magnetic_dipole([[0, 1, 0], [0, -1, 0]], m=[0, 1, 0], vectorized=True))

    print(magnetic_dipole([[0, 0, 1], [0, 0, -1]], m=[0, 0, 1], vectorized=False))
    print(magnetic_dipole([[0, 0, 1], [0, 0, -1]], m=[0, 0, 1], vectorized=True))


def dipole(points, M=7.788E22, r_nan=0.):
    import numpy as np
    r = np.linalg.norm(points, axis=1)
    B = np.zeros(points.shape)
    r[r <= r_nan] = np.nan
    B[:,0] = 3*M*points[:,0]*points[:,2]/r**5 # Bx = 3*M*x*z/r^5
    B[:,1] = 3*M*points[:,1]*points[:,2]/r**5 # By = 3*M*y*z/r^5
    B[:,2] = M*(3*points[:,2]**2-r**2)/r**5   # Bz = M(3*z^2 - r^2)/r^5

    return B
