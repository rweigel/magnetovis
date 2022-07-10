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
