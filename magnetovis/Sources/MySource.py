def MySource(**kwargs):

  import magnetovis as mvs
  return mvs.CreateProgrammableSource("MySource.py")


def OutputDataSetType():

  # What is set in the drop-down menu for Output Data Set Type for
  # Programmable Source.
  return "vtkPolyData"


def Script(point1=(0.0, 0.0, 0.0), point2=(1.0, 0.0, 0.0), resolution=10):

  # What entered into the Script text area for a Programmable Source
  import vtk

  vtkLineSource = vtk.vtkLineSource()
  vtkLineSource.SetPoint1(point1)
  vtkLineSource.SetPoint2(point2)
  vtkLineSource.SetResolution(resolution)
  vtkLineSource.Update()

  output.ShallowCopy(vtkLineSource.GetOutputDataObject(0))

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
            'source': {},
            "display": {
              "AmbientColor": [1, 0, 0],
              "DiffuseColor": [1, 0, 0]
            }
        } 
    }

    return defaults


def SetDisplayProperties(source, view=None, **kwargs):

  import logging
  import paraview.simple as pvs
  import magnetovis

  # Get kwargs used for source
  info = magnetovis.ProxyInfo.GetInfo(source)

  # Default keyword arguments
  dkwargs = GetDisplayDefaults()

  # Update defaults 
  displayProperties = {}
  if 'display' in kwargs:
      displayProperties = {**dkwargs['display'], **kwargs['display']}
  sourceProperties = {}
  if 'source' in kwargs:
      sourceProperties = {**dkwargs['source'], **kwargs['source']}

  registrationName = "  Tube for " + info['registrationName']
  tube = pvs.Tube(registrationName=registrationName, Input=source, **sourceProperties)
  pvs.Show(tube, view, 'GeometryRepresentation', **displayProperties)

  return [{'tube': tube}]


