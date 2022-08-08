def OutputDataSetType():

  # What is set in the drop-down menu for Output Data Set Type for a Programmable Source
  return "vtkPolyData"


def Script(time="2001-01-01", coord_sys="GSM",
            Nlines=6,
            closed=True,
            point_function="circle",
            point_array_functions=["position"],
            cell_array_functions=None):

   debug = False

   assert isinstance(point_array_functions, list), "point_array_functions must be a list"
   assert isinstance(point_function, str), "point_function must be a str"

   import vtk
   import numpy as np

   from hxform import hxform as hx
   import magnetovis as mvs

   if closed:
      points = mvs.vtk.get_arrays(point_function, Nlines)
   else:
      points = mvs.vtk.get_arrays(point_function, Nlines+1)

   if coord_sys != 'GSM':
     from hxform import hxform as hx
     assert time != None, 'magnetovis.Lines(): If coord_sys in not GSM, time cannot be None'
     points = hx.transform(points, time, 'GSM', coord_sys, 'car', 'car')

   point_data = mvs.vtk.get_arrays(point_array_functions, points)
   #cell_data = get_arrays(cell_array_functions, cell_centers)

   Npts = points.shape[0]

   if debug:
      np.set_printoptions(precision=1, floatmode='fixed')
      print("Nlines = {}; closed={}; Npts = {}\n".format(Nlines, closed, Npts))

   points2 = np.zeros((2*Npts, 3))
   output.Allocate(Nlines, 1)

   for i in range(Nlines-1):
      points2[2*i, :] = points[i, :]
      points2[2*i+1, :] = points[i+1, :]
      vtkPolyLine = vtk.vtkPolyLine()
      vtkPolyLine.GetPointIds().SetNumberOfIds(2)
      vtkPolyLine.GetPointIds().SetId(0, 2*i) 
      vtkPolyLine.GetPointIds().SetId(1, 2*i+1)
      output.InsertNextCell(vtkPolyLine.GetCellType(), vtkPolyLine.GetPointIds())
      if debug:
         print("p{} = {}".format(2*i, points2[2*i, :]))
         print("p{} = {}".format(2*i+1, points2[2*i+1, :]))
         print("Line {}: p{}-p{}\n".format(i, 2*i, 2*i+1))

   vtkPolyLine = vtk.vtkPolyLine()
   vtkPolyLine.GetPointIds().SetNumberOfIds(2)
   i = i + 1
   if closed:
      points2[2*i, :] = points[i, :]
      points2[2*i+1, :] = points[0, :]
      vtkPolyLine.GetPointIds().SetId(0, 2*i) 
      vtkPolyLine.GetPointIds().SetId(1, 0)
      if debug:
         print("p{} = {}".format(2*i, points2[2*i, :]))
         print("p{} = {}".format(0, points2[2*i+1, :]))
         print("Line {}: p{}-p{}".format(i, 2*i, 0))
   else:
      points2[2*i, :] = points[i, :]
      points2[2*i+1, :] = points[i+1, :]
      vtkPolyLine.GetPointIds().SetId(0, 2*i) 
      vtkPolyLine.GetPointIds().SetId(1, 2*i+1)
      if debug:
         print("p{} = {}".format(2*i, points2[2*i, :]))
         print("p{} = {}".format(2*i+1, points2[2*i+1, :]))
         print("Line {}: p{}-p{}".format(i, 2*i, 2*i+1))

   output.InsertNextCell(vtkPolyLine.GetCellType(), vtkPolyLine.GetPointIds())

   mvs.vtk.set_points(output, points2)
   point_arrays = mvs.vtk.get_arrays(point_array_functions, points)
   mvs.vtk.set_arrays(output, point_data=point_arrays, include=["CellId"])

   mvs.ProxyInfo.SetInfo(output, locals())