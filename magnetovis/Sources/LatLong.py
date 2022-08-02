def OutputDataSetType():

  # What is set in the drop-down menu for Output Data Set Type for
  # Programmable Source.
  return "vtkPolyData"


def Script(coord_sys="GEO",
           φ=[0, 45, 90, 135],
           θ=[-75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75]):

  import math
  import vtk

  combinedSources = vtk.vtkAppendPolyData()
  for t in θ:
    polygonSource = vtk.vtkRegularPolygonSource()
    polygonSource.GeneratePolygonOff()
    polygonSource.SetNumberOfSides(90)
    polygonSource.SetRadius(math.cos(math.pi*t/180.0))
    polygonSource.SetCenter(0, 0, math.sin(math.pi*t/180.0))
    polygonSource.Update()
    combinedSources.AddInputData(polygonSource.GetOutput())

  for p in φ:
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

  if False:
    import vtk
    transform = vtk.vtkTransform()
    transform.RotateWXYZ(angle, *axis)
    transformFilter = vtk.vtkTransformFilter()
    transformFilter.SetTransform(transform)
    transformFilter.SetInputDataObject(inputs[0].VTKObject)
    transformFilter.Update()

  output.ShallowCopy(combinedSources.GetOutputDataObject(0))

  import magnetovis as mvs

  # Store kwargs
  mvs.ProxyInfo.SetInfo(output, locals())


# Everything that follows is optional
def GetDisplayDefaults():

    defaults = {
        'display': {
            'Representation': 'Surface',
            'AmbientColor': [0, 1, 0],
            'DiffuseColor': [0, 1, 0]
        },
        'tube': {
            'source': {
              'Radius': 0.001
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


def SetDisplayProperties(source, view=None, **kwargs):

  import logging
  import paraview.simple as pvs
  import magnetovis

  # Get kwargs used for source
  info = magnetovis.ProxyInfo.GetInfo(source)

  # Default keyword arguments
  dkwargs = GetDisplayDefaults()

  # Update defaults 
  displayProperties = dkwargs['display']
  if 'display' in kwargs:
      displayProperties = {**displayProperties, **kwargs['display']}
  sourceProperties = dkwargs['tube']['source']
  if 'source' in kwargs:
      sourceProperties = {**sourceProperties, **kwargs['tube']['source']}

  registrationName = "  Tube for " + info['registrationName']
  tube = pvs.Tube(registrationName=registrationName, Input=source, **sourceProperties)
  pvs.Show(tube, view, 'GeometryRepresentation', **displayProperties)

  return [{'tube': tube}]


