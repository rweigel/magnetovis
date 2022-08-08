def OutputDataSetType():

  return "vtkPolyData"


def Script(time="2001-01-01", coord_sys="GSM", coord_sys_view=None,
            Resolution=6,
            Closed=False,
            point_function="circle",
            point_array_functions=["xyz: position()"],
            _output=None):

  assert isinstance(point_array_functions, list), "point_array_functions must be a list"
  assert isinstance(point_function, str), "point_function must be a str"

  if _output is not None:
    output = _output

  import vtk
  import numpy as np

  import magnetovis as mvs

  points = mvs.vtk.get_arrays(point_function, Resolution)

  vtkPolyLine = vtk.vtkPolyLine()
  if Closed == True:
    vtkPolyLine.GetPointIds().SetNumberOfIds(Resolution+1)
  else:
    vtkPolyLine.GetPointIds().SetNumberOfIds(Resolution)

  for i in range(Resolution):
    vtkPolyLine.GetPointIds().SetId(i, i) 

  if Closed == True:
    vtkPolyLine.GetPointIds().SetId(i+1, 0)

  output.Allocate(1)
  output.InsertNextCell(vtkPolyLine.GetCellType(), vtkPolyLine.GetPointIds())

  point_arrays = mvs.vtk.get_arrays(point_array_functions, points)
  mvs.vtk.set_points(output, points)
  mvs.vtk.set_arrays(output, point_data=point_arrays)

  mvs._TransformByNames(in_name=coord_sys_view, out_name=coord_sys, time=time, _output=output, _inputs=[output])

  if _output is None:
    mvs.ProxyInfo.SetInfo(output, locals())


def GetPresentationDefaults():

   defaults = {
     'display': {
         'Representation': 'Surface',
         'AmbientColor': [0.5, 0.5, 0.5],
         'DiffuseColor': [0.5, 0.5, 0.5]
     },
     'tube': {
         "source": {
            'Scalars': [None, ''],
            'Vectors': ['POINTS', 'xyz'],
            'Radius': 0.1
         },
         "display": {
            'AmbientColor': [0, 0, 1],
            'DiffuseColor': [0, 0, 1]
         }
     } 
   }

   return defaults

def SetPresentationProperties(source, view=None, **kwargs):

  import logging
  import paraview.simple as pvs
  import magnetovis

  info = magnetovis.ProxyInfo.GetInfo(source)
  magnetovis.logger.info("Source info: {}".format(info))
  magnetovis.logger.info("kwargs: {}".format(kwargs))

  # Default keyword arguments
  dkwargs = GetPresentationDefaults()

  # Source defaults
  tubeSettings = dkwargs['tube']['source']

  if 'tube' in kwargs:
    if kwargs['tube'] is None:
       return
    if 'source' in kwargs['tube']:
       # Update defaults 
       tubeSettings = {**tubeSettings, **kwargs['tube']['source']}

  # Display defaults
  tubeDisplaySettings = dkwargs['tube']['display']

  # Update defaults 
  if 'tube' in kwargs and 'display' in kwargs['tube']:
    tubeDisplaySettings = {**tubeDisplaySettings, **kwargs['tube']['display']}

  registrationName = "  Tube for " + info['registrationName']
  tube = pvs.Tube(registrationName=registrationName, Input=source, **tubeSettings)
  pvs.Show(tube, view, 'GeometryRepresentation', **tubeDisplaySettings)

  return [{'tube': tube}]
