def set_points(output, points, dimensions=None, grid_type='structured'):

    import logging

    import vtk
    from vtk.numpy_interface import dataset_adapter as dsa

    if grid_type == 'uniform':
        pass
    elif grid_type == 'rectilinear':
        # Take the full set of points needed for a structured
        # grid and reduce it to only the points needed for a rectilinear
        # grid. In general, we will need the full set of points
        # when computing point and cell array data, and so the option
        # of providing an input of only the reduced set of points
        # needed for a rectilinear grid is not given.
        output.SetDimensions(*dimensions)

        Nx, Ny, Nz = dimensions        

        vtkDataArray = dsa.numpyTovtkDataArray(points[0:Nx,0])
        output.SetXCoordinates(vtkDataArray)

        vtkDataArray = dsa.numpyTovtkDataArray(points[0:Nx*Ny:Nx,1])
        output.SetYCoordinates(vtkDataArray)

        vtkDataArray = dsa.numpyTovtkDataArray(points[0:Nx*Ny*Nz:Nx*Ny,2])
        output.SetZCoordinates(vtkDataArray)
    else:
        vtkPoints = vtk.vtkPoints()
        vtkPoints.Allocate(points.shape[0])
        vtkDataArray = dsa.numpyTovtkDataArray(points)
        vtkPoints.SetData(vtkDataArray)
        output.SetPoints(vtkPoints)
