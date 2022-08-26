def OutputDataSetType():

  return "vtkPolyData"


def Script(_output=None):

  if _output is not None:
    output = _output
    inputs = [_output]

  import vtk

  probeFilter = vtk.vtkProbeFilter()
  probeFilter.SetInputData(inputs[1].VTKObject)
  probeFilter.SetSourceData(inputs[0].VTKObject)
  probeFilter.Update()

  output.ShallowCopy(probeFilter.GetOutputDataObject(0))

  import magnetovis as mvs
  #if _output is None:
  print("++++++")
  print(locals())
  mvs.ProxyInfo.SetInfo(output, locals())
