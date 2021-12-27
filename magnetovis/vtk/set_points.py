def set_points(output, points, dimensions=None):


    import magnetovis as mvs
    mvs.logger.info("Called.")

    import vtk
    from vtk.numpy_interface import dataset_adapter as dsa

    OutputDataSetType = output.VTKObject.GetClassName()

    if OutputDataSetType == "vtkImageData":

        output.SetDimensions(*dimensions)
        Nx, Ny, _ = dimensions        

        # See comment in vtkRectilinearGrid
        dx = points[1,0]-points[0,0]
        dy = points[Nx,1]-points[0,1]
        dz = points[Nx*Ny,2]-points[0,2]
        output.SetSpacing(dx, dy, dz)
    elif OutputDataSetType == "vtkRectilinearGrid":
        # Takes the full set of points needed for a structured
        # grid and extracts only what is needed for a rectilinear
        # grid. In general, we will need the full set of points
        # when creating point and cell array data, and so the option
        # of allowing `points` to only contain the information needed
        # to create a rectilinear grid is not implemented.
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
