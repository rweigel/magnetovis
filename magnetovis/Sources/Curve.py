def OutputDataSetType():

  return "vtkPolyData"


def Script(time="2001-01-01", coord_sys="GSM",
            Npts=6,
            closed=True,
            tube=True,
            vtkTubeFilterSettings=None,
            point_function="circle",
            point_array_functions=["xyz: position()"],
            cell_array_functions=["xyz: position()"]):

  assert isinstance(point_array_functions, list), "point_array_functions must be a list"
  assert isinstance(point_function, str), "point_function must be a str"

  import vtk
  import numpy as np

  import magnetovis as mvs

  points = mvs.vtk.get_arrays(point_function, Npts)

  if coord_sys != 'GSM':
    from hxform import hxform as hx
    assert time != None, 'magnetovis.Curve(): If coord_sys in not GSM, time cannot be None'
    points = hx.transform(points, time, 'GSM', coord_sys, 'car', 'car')

  vtkPolyLine = vtk.vtkPolyLine()
  if closed == True:
    vtkPolyLine.GetPointIds().SetNumberOfIds(Npts+1)
  else:
    vtkPolyLine.GetPointIds().SetNumberOfIds(Npts)

  for i in range(Npts):
    vtkPolyLine.GetPointIds().SetId(i, i) 

  if closed == True:
    vtkPolyLine.GetPointIds().SetId(i+1, 0)

  output.Allocate(1, 1)
  output.InsertNextCell(vtkPolyLine.GetCellType(), vtkPolyLine.GetPointIds())

  point_arrays = mvs.vtk.get_arrays(point_array_functions, points)
  mvs.vtk.set_points(output, points)
  mvs.vtk.set_arrays(output, point_data=point_arrays)

  mvs.ProxyInfo.SetInfo(output, locals())

def GetDisplayDefaults():

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

def SetDisplayProperties(source, view=None, display=None, **kwargs):

  import logging
  import paraview.simple as pvs
  import magnetovis

  info = magnetovis.ProxyInfo.GetInfo(source)
  magnetovis.logger.info("Source info: {}".format(info))
  magnetovis.logger.info("kwargs: {}".format(kwargs))

  # Default keyword arguments
  dkwargs = GetDisplayDefaults()

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
