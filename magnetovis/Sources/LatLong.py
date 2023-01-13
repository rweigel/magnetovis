def OutputDataSetType():

  # What is set in the drop-down menu for Output Data Set Type for
  # Programmable Source.
  return "vtkPolyData"


def Script(time="2000-01-01", coord_sys="GSM", coord_sys_view=None,
           phis=[0, 45, 90, 135],
           thetas=[-75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75]):

  import math
  import vtk

  combinedSources = vtk.vtkAppendPolyData()
  for t in thetas:
    polygonSource = vtk.vtkRegularPolygonSource()
    polygonSource.GeneratePolygonOff()
    polygonSource.SetNumberOfSides(90)
    polygonSource.SetRadius(math.cos(math.pi*t/180.0))
    polygonSource.SetCenter(0, 0, math.sin(math.pi*t/180.0))
    polygonSource.Update()
    combinedSources.AddInputData(polygonSource.GetOutput())

  for p in phis:
    polygonSource = vtk.vtkRegularPolygonSource()
    polygonSource.GeneratePolygonOff()
    polygonSource.SetNumberOfSides(90)
    polygonSource.SetRadius(1)
    polygonSource.SetCenter(0, 0, 0)
    polygonSource.Update()

    transform = vtk.vtkTransform()
    transform.RotateWXYZ(90, [1, 0, 0])
    transform.RotateWXYZ(p, [0, 1, 0])
    transform.Update()
    transformFilter = vtk.vtkTransformFilter()
    transformFilter.SetTransform(transform)
    transformFilter.SetInputDataObject(polygonSource.GetOutput())
    transformFilter.Update()
    combinedSources.AddInputData(transformFilter.GetOutput())

  combinedSources.Update()

  import magnetovis as mvs

  output.ShallowCopy(combinedSources.GetOutputDataObject(0))
  #mvs.vtk.set_arrays(output, include=["CellId"])

  mvs._TransformByNames(in_name=coord_sys_view, out_name=coord_sys, time=time, _output=output, _inputs=[output])


# Everything that follows is optional
def GetPresentationDefaults():

    defaults = {
        'display': {
            'Representation': 'Surface',
            'AmbientColor': [0, 1, 0],
            'DiffuseColor': [0, 1, 0]
        },
        'tube': {
            'source': {
              'Radius': 0.005
            },
            "display": {
              "AmbientColor": [1, 0, 0],
              "DiffuseColor": [1, 0, 0]
            }
        } 
    }

    return defaults


def DefaultRegistrationName(**kwargs):

    import magnetovis as mvs

    if kwargs['coord_sys'] == "GEO":
        # Ttime independent so exclude time.
        return "{}/{}".format("Lat & Long lines", kwargs['coord_sys'])
    else:
        # Orientation depends on time, so include it.
        return "{}/{}/{}" \
                    .format("Lat & Long lines", mvs.util.trim_iso(kwargs['time']), kwargs['coord_sys'])


def SetPresentationProperties(source, view=None, **kwargs):

  import logging
  import paraview.simple as pvs
  import magnetovis

  # Get kwargs used for source
  info = magnetovis.ProxyInfo.GetInfo(source)

  # Default keyword arguments
  dkwargs = GetPresentationDefaults()

  # Update defaults 
  displayProperties = dkwargs['display']
  if 'display' in kwargs:
      displayProperties = {**displayProperties, **kwargs['display']}
  sourceProperties = dkwargs['tube']['source']
  if 'source' in kwargs:
      sourceProperties = {**sourceProperties, **kwargs['tube']['source']}

  registrationName = "Tube for " + info['registrationName']
  tube = pvs.Tube(registrationName=registrationName, Input=source, **sourceProperties)
  pvs.Show(tube, view, 'GeometryRepresentation', **displayProperties)

  return [{'tube': tube}]


