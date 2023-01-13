def plasmasphere(N=10):
    """

    Plasmasphere model of D. Gallagher, P. Craven, R. H. Comfort, 1988
    (https://doi.org/10.1016/0273-1177%2888%2990258-X)

    Implementation by Angel Gutarra-Leon and Gary Quaresima

    Coordinate system is SM

    log(n) = a1 * F(L) * G(L) * H(L) = 1.5

    where,

    F(L) = a2 - e ** (a3 * (1 -a4 * e ** (-h(L,Lambda) / a5)))

    G(L) = a6 * L + a7

    H(L) = (1 + (L / a8) ** (2 * (a9 - 1))) ** (-a9 / (a9 - 1))

    L = R/cos^2(Lambda)

    Lambda is the geomagnetic latitude

    L is the McIlwain L-Shell parameter.

    h(L, Lambda) is the height above the Earth's surface

    h = 6371.2*(1.-R)  # according to SSCWEB

    constants:
        a1 = 1.4
        a2 = 1.53
        a3 = -0.036
        a4 = 30.76
        a5 = 159.9
        a6 = -0.87 + 0.12 * e ** (-x**2 / 9)
        a7 = 6.27
        a8 = 0.7 * cos(2 * pi * ((MLT - 21) / 24)) + 4.4
        a9 = 15.3 * cos(2 * pi * MLT / 24) + 19.7

    MLT = (PHI*RAD/15.) - 12.
    x = MLT
    MLT is the magnetic local time measured in HH MLT=0=24 is midnight
    and MLT=12 is noon.
    MLT domain is [0, 24)
    x domain is [-12, 12]

    PHI is the longitude
    THETA is the latitude

    """

    import vtk
    import numpy as np

    from copy import deepcopy

    def logDen(r, theta, phi):
        a1 = 1.4
        a2 = 1.53
        a3 = -0.036
        a4 = 30.76
        a5 = 159.9
        a7 = 6.27

        MLT = (phi*180/np.pi/15.) - 12.
        x = deepcopy(MLT)
        if MLT >= 24: MLT = MLT - 24
        if MLT <   0: MLT = MLT + 24
        if x >  12: x = x - 24
        if x < -12: x = x + 24

        a6 = -0.87 + 0.12 * np.exp(-x*x/9.)
        a8 = 0.7 * np.cos(2*np.pi* (MLT-21.)/24.) + 4.4
        a9 = 15.3 * np.cos(2*np.pi*MLT/24.) + 19.7

        F = a2 - np.exp(a3 * (1.-a4 * np.exp(6371.2*(1.-r)/a5)))
        C2LAM = np.cos(theta)*np.cos(theta)
        G = (a6*r/C2LAM) + a7
        H = (1. + (r /(C2LAM*a8)) ** (2. * (a9 - 1.))) ** (-a9 / (a9 - 1.))

        n_log = a1*F*G*H

        return n_log

    rmin = 1.05
    r_ax = np.arange(rmin,6,(6-rmin)/N) # make radius out to 6.

    theta_i = 28*np.pi/180
    theta_f = 152*np.pi/180
    theta_step = (theta_f-theta_i)/N
    theta_ax = np.arange(theta_i, theta_f, theta_step)
    theta_ax = np.pi/2. - theta_ax # Convert from colatitude to latitude

    dphi = 2.*np.pi/N
    phi_ax = dphi*np.arange(N)

    phi = np.kron(np.ones(N),phi_ax)
    theta = np.kron(theta_ax,np.ones(N))
    r = np.kron(r_ax, np.ones(N**2))

    phi = np.kron(np.ones(N), phi)
    theta = np.kron(np.ones(N), theta)

    # rtp = r, theta, phi locations
    rtp = np.column_stack([r, theta, phi])

    # d = log(H+ density)
    d = np.empty(rtp.shape[0])
    for i in range(rtp.shape[0]):
        d[i] = logDen(rtp[i,0], rtp[i,1], rtp[i,2])

    # Cartesian points
    xyz = np.empty(rtp.shape)

    # x = r cos(phi) cos(theta)
    xyz[:,0] = rtp[:,0]*np.cos(rtp[:,2])*np.cos(rtp[:,1])  
    # y = r sin(phi) cos(theta)
    xyz[:,1] = rtp[:,0]*np.sin(rtp[:,2])*np.cos(rtp[:,1])  
    # z = r sin(theta)
    xyz[:,2] = rtp[:,0]*np.sin(rtp[:,1])                 

    debug = False
    if debug:
        print("Columns are r, theta, phi, log(density)")
        print(np.column_stack([r, theta, phi, d]))

    return xyz, cells(N=N), d

def cells(N=2):
    import numpy as np

    # Periodic in phi (indexed by k)
    ind = np.arange(N**3).reshape((N, N, N))
    indPeriodic = np.zeros((N, N, N+1), dtype=int)

    # the same as ind except with an extra column of zeros
    indPeriodic[:,:,:-1] = ind 

    # the last row which was all zeros is now a copy of the first row
    indPeriodic[:,:,-1] = ind[:,:,0] 

    hex_list = []
    for i in range(N-1):
        for j in range(N-1):
            for k in range(N):
                hex_points = [indPeriodic[i,j,k],
                              indPeriodic[i+1,j,k],
                              indPeriodic[i+1,j+1,k],
                              indPeriodic[i,j+1,k],
                              indPeriodic[i,j,k+1],
                              indPeriodic[i+1,j,k+1],
                              indPeriodic[i+1,j+1,k+1],
                              indPeriodic[i,j+1,k+1]]
                hex_list.append(hex_points)

    # size = (N-1)*(N-1)*N
    hex_list = np.array(hex_list, dtype=int) 

    return hex_list


if __name__ == "__main__":
    
    plasmasphere(N=2)
    print(cells(N=2))
