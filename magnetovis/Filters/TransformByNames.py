def Script(in_name=None, out_name=None, time=None, _output=None, _inputs=None):

  import magnetovis as mvs
  mvs.logger.info("Called.")

  if in_name == out_name:
    mvs.logger.info("in_name == out_name. Not transforming.")
    return

  if _output is not None or inputs is not None:
      assert _output is not None and _inputs is not None
      output = _output
      inputs = _inputs

  if in_name is None:
    in_name = mvs.coord_sys_view

  from hxform import hxform as hx
  assert time != None, 'magnetovis.TransformByNames(): If coord_sys in not GSM, time cannot be None'
  matrix = hx.get_transform_matrix(time, in_name, out_name, lib='cxform')
  matrix = [*matrix[:,0], 0, 
            *matrix[:,1], 0, 
            *matrix[:,2], 0, 
            0, 0, 0     , 1]

  import vtk
  transform = vtk.vtkTransform()
  transform.SetMatrix(matrix)
  transformFilter = vtk.vtkTransformFilter()
  transformFilter.SetTransform(transform)
  transformFilter.SetInputDataObject(inputs[0].VTKObject)
  transformFilter.Update()

  #mvs.logger.info("Transform matrix = {}".format(transform.GetMatrix()))

  output.ShallowCopy(transformFilter.GetOutputDataObject(0))


def DefaultRegistrationName(**kwargs):

  import magnetovis as mvs

  return "{}/In={}/Out={}".format("Transform", kwargs['in_name'], kwargs['out_name'])
