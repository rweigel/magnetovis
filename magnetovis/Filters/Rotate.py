def Script(angle=0, axis=[0, 0, 1], _output=None):

  if _output is not None:
    output = _output
    inputs = [_output]

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

  if _output is None:
    mvs.ProxyInfo.SetInfo(output, locals())

def DefaultRegistrationName(**kwargs):

  import magnetovis as mvs

  angle = mvs.util.trim_nums(kwargs['angle'], 3, style='string')

  axis = kwargs['axis']
  if not isinstance(kwargs['axis'], str):
    axis = mvs.util.trim_nums(kwargs['axis'], 3, style='string')

  return "{}/angle={}/axis={}".format("Rotate", angle, axis)
