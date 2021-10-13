# This program demonstrates how to use programmable source to create a
# VTK object that could not otherwise be created using paraview.simple.

def _source(self, n_pts=10, length=10):

   # Sources, readers, and filters all produce data.
   # https://docs.paraview.org/en/latest/UsersGuide/understandingData.html

   # Content that one could enter into the Programmable Source
   # text area in the ParaView GUI.
   import vtk

   pdo = self.GetPolyDataOutput()

   points = vtk.vtkPoints()

   # TODO: Show how this can be done without a loop.
   for i in range(0, n_pts):
      x = i*length/n_pts
      y = 0
      z = 0
      points.InsertPoint(i, x,y,z)

   pdo.SetPoints(points)

   aPolyLine = vtk.vtkPolyLine()

   aPolyLine.GetPointIds().SetNumberOfIds(n_pts)
   for i in range(0, n_pts):
      aPolyLine.GetPointIds().SetId(i, i)

   pdo.Allocate(1, 1)
   pdo.InsertNextCell(aPolyLine.GetCellType(), aPolyLine.GetPointIds())


def _display(self, displayProperties, displayRepresentation='Surface'):  

   # VTK/Paraview Terminology
   #
   # Rendering Views are views that render geometries or volumes in a graphical context.
   # The Render View is one such view. Other Render View-based views, such as Slice View
   # and Quad View , extend the basic render view to add the ability to add mechanisms to
   # easily inspect slices or generate orthogonal views.
   # https://docs.paraview.org/en/latest/UsersGuide/displayingData.html#displaying-data

   # Display properties refers to available parameters that control how data from a pipeline
   # module is displayed in a view, e.g., choosing to view the output mesh as a wireframe,
   # coloring the mesh using a data attribute, and selecting which attributes to plot in
   # chart view. A set of display properties is associated with a particular pipeline module
   # and view. Thus, if the data output from a source is shown in two views, there will be
   # two sets of display properties used to control the appearance of the data in each of 
   # the two views.

   import paraview.simple as pvs

   # Set representation of display object
   displayProperties.Representation = displayRepresentation

   return displayProperties
