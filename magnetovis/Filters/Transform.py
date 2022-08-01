def Script(time, x=[1, 0, 0], y=[0, 1, 0], z=[0, 1, 0], xinputs=None, xoutput=None):

    matrix = [*x, 0, *y, 0, *z, 0, 0, 0, 0, 1]
    #matrix = [1, 0, 0, 0,
    #          0, 1, 0, 0,
    #          0, 0, 1, 0,
    #          0, 0, 0, 1]
    import vtk
    transform = vtk.vtkTransform()
    #transform.Identity()
    #print(transform.GetMatrix())
    transform.SetMatrix(matrix)
    transformFilter = vtk.vtkTransformFilter()
    transformFilter.SetTransform(transform)
    transformFilter.SetInputDataObject(inputs[0].VTKObject)
    transformFilter.Update()
    output.ShallowCopy(transformFilter.GetOutputDataObject(0))
