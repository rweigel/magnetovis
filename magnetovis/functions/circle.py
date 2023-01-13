def circle(resolution, radius=1.0, center=(0.0, 0.0, 0.0)):

    import numpy as np

    idx = np.arange(resolution)

    points = np.zeros((resolution, 3))
    points[:,0] = center[0] + radius*np.cos(idx*2*np.pi/resolution)
    points[:,1] = center[1] + radius*np.sin(idx*2*np.pi/resolution)
    points[:,2] = center[2]

    return points
