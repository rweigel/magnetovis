def structured_grid(self, output, points, data_arrays):

    # https://discourse.paraview.org/t/problem-displaying-structured-grid-when-loading-from-programmable-source/3051/2
    import vtk
    from vtk.numpy_interface import dataset_adapter as dsa

    # Communication between "script" and "script (RequestInformation)"
    executive = self.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    exts = [executive.UPDATE_EXTENT().Get(outInfo, i) for i in range(6)]
    dims = [exts[1]+1, exts[3]+1, exts[5]+1]

    output.SetExtent(exts)

    pvtk = dsa.numpyTovtkDataArray(points)
    pts = vtk.vtkPoints()
    pts.Allocate(dims[0]*dims[1]*dims[2])
    pts.SetData(pvtk)
    output.SetPoints(pts)
    for name, array in data_arrays.items():
        vtkArray = dsa.numpyTovtkDataArray(array)
        vtkArray.SetName(name)
        output.GetPointData().AddArray(vtkArray)
