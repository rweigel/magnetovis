# This program demonstrates how to use programmable source to create a
# VTK object that could not otherwise be created using paraview.simple.

def OutputDataSetType():

   # What is set in the drop-down menu for Output Data Set Type for a Programmable Source
   return "vtkPolyData"

def ScriptRequestInformation(self):

   # What is entered in the Script (RequestInformation) box for a Programmable Source
   pass

def Script(self, n_pts=10, length=10):

   try:
      # Being executed in Programmable Source
      output = self.GetPolyDataOutput()
   except:
      # Being executed in Plugin
      from vtkmodules.vtkCommonDataModel import vtkPolyData
      output = vtkPolyData.GetData(outInfo, 0)

   import vtk
   points = vtk.vtkPoints()

   # TODO: Show how this can be done without a loop.
   for i in range(0, n_pts):
      x = i*length/n_pts
      y = 0
      z = 0
      points.InsertPoint(i, x,y,z)

   output.SetPoints(points)

   if False:
      aPolyLine = vtk.vtkPolyLine()

      aPolyLine.GetPointIds().SetNumberOfIds(n_pts)
      for i in range(0, n_pts):
         aPolyLine.GetPointIds().SetId(i, i)

      output.Allocate(1, 1)
      output.InsertNextCell(aPolyLine.GetCellType(), aPolyLine.GetPointIds())

   return output

def Display(magnetovisPlane, magnetovisPlaneDisplayProperties, magnetovisPlaneRenderView, **displayArguments):

    # Base this on code that is displayed by trace in ParaView GUI

    import paraview
    import paraview.simple as pvs

    if "displayRepresentation" in displayArguments:
        magnetovisPlaneDisplayProperties.Representation = displayArguments['displayRepresentation']

    if "opacity" in displayArguments:
        magnetovisPlaneDisplayProperties.Opacity = displayArguments['opacity']

    return magnetovisPlaneDisplayProperties

def _Display(self, displayArguments):
    self.displayProperties = Display(self.programmableSource, self.displayProperties, self.renderView, **displayArguments)
