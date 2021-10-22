def structured_grid(self, output, points, point_data=None, cell_data=None):

    import vtk
    from vtk.numpy_interface import dataset_adapter as dsa

    pts = vtk.vtkPoints()
    pts.Allocate(points.shape[0])
    pvtk = dsa.numpyTovtkDataArray(points)
    pts.SetData(pvtk)
    output.SetPoints(pts)

    if point_data is not None:
        for name, array in point_data.items():
            vtkArray = dsa.numpyTovtkDataArray(array)
            vtkArray.SetName(name)
            output.GetPointData().AddArray(vtkArray)

    if cell_data is not None:
        for name, array in cell_data.items():
            vtkArray = dsa.numpyTovtkDataArray(array)
            vtkArray.SetName(name)
            output.GetCellData().AddArray(vtkArray)

    return output
