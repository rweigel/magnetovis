def Script(time, angle=0, axis=[0, 0, 1], xinputs=None, xoutput=None):

    if isinstance(axis, str):
        assert axis in ["X", "Y", "Z"], "angle must be one of 'X', 'Y', or 'Z'"
        if axis == "X":
            axis = [1, 0, 0]
        if axis == "Y":
            axis = [0, 1, 0]
        if axis == "Z":
            axis = [1, 0, 0]

    import vtk
    transform = vtk.vtkTransform()
    transform.RotateWXYZ(angle, *axis)
    transformFilter = vtk.vtkTransformFilter()
    transformFilter.SetTransform(transform)
    transformFilter.SetInputDataObject(inputs[0].VTKObject)
    transformFilter.Update()
    output.ShallowCopy(transformFilter.GetOutputDataObject(0))


if False:
    #print(transform.GetMatrix())
    matrix = [1, 0, 0, 0,
              0, 1, 0, 0,
              0, 0, 1, 0,
              0, 0, 0, 1]
    #transform.SetMatrix(matrix)
    #print(transform.GetMatrix())
    # http://www.euclideanspace.com/maths/geometry/affine/matrix4x4/    
    import vtk
    transform = vtk.vtkTransform()
    transform.RotateWXYZ(90, 1, 0, 0)
    print(transform.GetMatrix())
    #transform.RotateWXYZ(90, 0, 1, 0)
    matrix = [1, 0, 0, 0,
              0, 1, 0, 0,
              0, 0, 1, 0,
              0, 0, 0, 1]
    transform.SetMatrix(matrix)
    print(transform.GetMatrix())
    transformFilter = vtk.vtkTransform()
    transformFilter.SetTransform(transform)
    transformFilter.SetInputDataObject(output.VTKObject)
    transformFilter.Update()
    output.ShallowCopy(transformFilter.GetOutputDataObject(0))

    if False:
        import vtk
        transform = vtk.vtkTransform()
        transform.RotateWXYZ(90, 0, 1, 0)
        transform.RotateWXYZ(90, 0, 1, 0)
        matrix = [1, 0, 0, 0,
                  0, 1, 0, 0,
                  0, 0, 1, 0,
                  0, 0, 0, 1]
        #transform.SetMatrix(matrix)
        transformFilter = vtk.vtkTransform()
        #transformFilter = vtk.vtkTransformPolyDataFilter()
        transformFilter.SetTransform(transform)
        transformFilter.SetInputDataObject(input[0].VTKObject)
        transformFilter.Update()
        output.ShallowCopy(transformFilter.GetOutputDataObject(0))
