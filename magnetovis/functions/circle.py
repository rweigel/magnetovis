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
