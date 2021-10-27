def OutputDataSetType():

    # What is set in the drop-down menu for Output Data Set Type for a Programmable Source
    return "vtkPolyData"

def ScriptRequestInformation(self):
    pass

def Script(self, time="2001-01-01", coord_sys="GSM", Npts=6, closed=False, point_function={"circle": {}}, point_array_functions=None, cell_array_functions=None):

   # What is entered in the Script box for a Programmable Source

   import vtk
   import numpy as np

   from magnetovis.vtk.set_arrays import set_arrays
   from magnetovis.vtk.get_arrays import get_arrays
   from hxform import hxform as hx

   if (len(point_function) > 1):
      # TODO: Error
      pass
   
   function_name = list(point_function.keys())[0]
   points = get_arrays(point_function, Npts)[function_name]

   if closed in point_function:
      closed = point_function['closed']

   if coord_sys != 'GSM':
      assert time != None, 'magnetovis.Curve(): If coord_sys in not GSM, time cannot be None'
      points = hx.transform(points, time, 'GSM', coord_sys, 'car', 'car')

   point_data = get_arrays(point_array_functions, points)
   #cell_data = get_arrays(cell_array_functions, cell_centers)

   try:
      # Being executed in Programmable Source
      output = self.GetPolyDataOutput()
   except:
      # Being executed in Plugin
      from vtkmodules.vtkCommonDataModel import vtkPolyData
      output = vtkPolyData.GetData(outInfo, 0)

   vtkPolyLine = vtk.vtkPolyLine()
   vtkPolyLine.GetPointIds().SetNumberOfIds(Npts)
   if closed == True:
      for i in range(Npts-1):
         vtkPolyLine.GetPointIds().SetId(i, i) 
      vtkPolyLine.GetPointIds().SetId(i+1, 0)
   else:
      for i in range(Npts):
         vtkPolyLine.GetPointIds().SetId(i, i) 

   output.Allocate(1, 1)
   output.InsertNextCell(vtkPolyLine.GetCellType(), vtkPolyLine.GetPointIds())

   output = set_arrays(self, output, points, point_data=point_data)

def Display(source, display, renderView, **displayArguments):

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


def _Display(self, displayArguments):
    self.displayProperties = Display(self.programmableSource, self.displayProperties, self.renderView, **displayArguments)
