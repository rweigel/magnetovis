def OutputDataSetType():

  return "vtkPolyData"


def Script(_output=None):

  import vtk

  probeFilter = vtk.vtkProbeFilter()
  probeFilter.SetSourceData(inputs[0].VTKObject)
  probeFilter.SetInputData(inputs[1].VTKObject)
  probeFilter.Update()

  output.ShallowCopy(probeFilter.GetOutputDataObject(0))
