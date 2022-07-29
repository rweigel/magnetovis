def Script():

    transform = vtk.vtkTransform()
    transform.RotateWXYZ(90, 0, 1, 0)
    #transform.RotateWXYZ(90, 0, 1, 0)
    transformFilter = vtk.vtkTransform()
    transformFilter.SetTransform(transform)
    transformFilter.SetInputDataObject(input[0].VTKObject)
    transformFilter.Update()
    output.ShallowCopy(transformFilter.GetOutputDataObject(0))

if False:
    transform = vtk.vtkTransform()
    transform.RotateWXYZ(90, 0, 1, 0)
    #transform.RotateWXYZ(90, 0, 1, 0)
    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetTransform(transform)
    transformFilter.SetInputDataObject(output.VTKObject)
    transformFilter.Update()
    output.ShallowCopy(transformFilter.GetOutputDataObject(0))
