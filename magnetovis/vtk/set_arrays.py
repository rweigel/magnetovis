def set_arrays(self, output, points, point_data=None, cell_data=None, debug=False):

    import vtk
    from vtk.numpy_interface import dataset_adapter as dsa

    vtkPoints = vtk.vtkPoints()
    vtkPoints.Allocate(points.shape[0])
    vtkDataArray = dsa.numpyTovtkDataArray(points)
    vtkPoints.SetData(vtkDataArray)

    output.SetPoints(vtkPoints)

    if point_data is not None:
        for name, array in point_data.items():
            if debug:
                print("set_arrays(): setting point_data array named " + name)
            vtkArray = dsa.numpyTovtkDataArray(array)
            vtkArray.SetName(name)
            output.GetPointData().AddArray(vtkArray)

    if cell_data is not None:
        for name, array in cell_data.items():
            vtkArray = dsa.numpyTovtkDataArray(array)
            vtkArray.SetName(name)
            output.GetCellData().AddArray(vtkArray)

    import numpy as np
    Ncells = output.GetNumberOfCells()
    if debug:
        print("set_arrays(): Ncells = " + str(Ncells))
    vtkArray = dsa.numpyTovtkDataArray(np.arange(Ncells))
    vtkArray.SetName('cell_index')
    output.GetCellData().AddArray(vtkArray)

    return output
