def OutputDataSetType():

    return "vtkPolyData"


def Script(time="2001-01-01", coord_sys="GSM",
            Npts=6,
            closed=True,
            point_function="circle",
            point_array_functions=["xyz: position()"],
            cell_array_functions=["xyz: position()"]):

   assert isinstance(point_array_functions, list), "point_array_functions must be a list"
   assert isinstance(point_function, str), "point_function must be a str"

   import vtk
   import numpy as np

   from hxform import hxform as hx
   import magnetovis as mvs

   points = mvs.vtk.get_arrays(point_function, Npts)

   if coord_sys != 'GSM':
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
   mvs.vtk.set_arrays(output, point_data=point_arrays, include=["CellId"])

