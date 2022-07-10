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
