def OutputDataSetType():

    # What is set in the drop-down menu for Output Data Set Type for a Programmable Source
    return "vtkPolyData"


def Script(time="2001-01-01", coord_sys="GSM",
            Npts=6,
            closed=True,
            point_function="circle",
            point_array_functions=["position"],
            cell_array_functions=None):

   assert isinstance(point_array_functions, list), "point_array_functions must be a list"
   assert isinstance(point_function, str), "point_function must be a str"

   import vtk
   import numpy as np

   from hxform import hxform as hx

   from magnetovis.vtk.set_arrays import set_arrays
   from magnetovis.vtk.get_arrays import get_arrays
   from magnetovis.vtk.set_points import set_points

   points = get_arrays(point_function, Npts)

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

   point_arrays = get_arrays(point_array_functions, points)
   set_points(self, output, points)
   set_arrays(self, output, point_data=point_arrays)


def Display(self, source, display, renderView, **displayArguments):

    # Base this on code that is displayed by trace in ParaView GUI

    import paraview
    import paraview.simple as pvs

    if "displayRepresentation" in displayArguments:
        display.Representation = displayArguments['displayRepresentation']

    scalarBarVisibility = True
    if "scalarBarVisibility" in displayArguments:
        scalarBarVisibility = displayArguments['scalarBarVisibility']

    #name = 'point_positions'
    #pvs.ColorBy(display, ('POINTS', name))
    #display.SetScalarBarVisibility(renderView, scalarBarVisibility)

    return display
