def arc(resolution, radius=1.0, center=(0.0, 0.0, 0.0), start_phi=0.0, end_phi=90.0):

    import numpy as np

    angles = (np.pi/180.0)*np.linspace(start_phi, end_phi, resolution)

    points = np.zeros((resolution, 3))
    points[:,0] = center[0] + radius*np.cos(angles)
    points[:,1] = center[1] + radius*np.sin(angles)
    points[:,2] = center[2]

    return points
