def helix(Npts, radius=1.0, length=10, rounds=3):

    import numpy as np

    idx = np.arange(Npts)

    points = np.full((Npts, 3), np.nan)
    points[:,0] = idx*length/(Npts-1)
    points[:,1] = radius*np.sin(idx*rounds*2*np.pi/Npts)
    points[:,2] = radius*np.cos(idx*rounds*2*np.pi/Npts)

    return points
