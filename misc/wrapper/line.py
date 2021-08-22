# This program demonstrates how to use programmable source to create a
# VTK object that could not be created using paraview.simple.

def line(n_pts=10, length=10):
   from exec_programmable_source import exec_programmable_source
   exec_programmable_source('line.py', n_pts=n_pts, length=length)


def _line(self, n_pts=10, length=10):
   # Content that one could enter into the Programmable Source
   # text area in the ParaView GUI.
   import vtk
   import paraview.simple as pvs    

   pvs.RenameSource('Line')

   pdo = self.GetPolyDataOutput()

   points = vtk.vtkPoints()

   # TODO: Show how this can be done without a loop.
   for i in range(0, n_pts):
      x = i*length/n_pts
      y = x
      z = x
      points.InsertPoint(i, x,y,z)

   pdo.SetPoints(points)

   aPolyLine = vtk.vtkPolyLine()

   aPolyLine.GetPointIds().SetNumberOfIds(n_pts)
   for i in range(0, n_pts):
      aPolyLine.GetPointIds().SetId(i, i)

   pdo.Allocate(1, 1)
   pdo.InsertNextCell(aPolyLine.GetCellType(), aPolyLine.GetPointIds())


if 'kwargs' in vars():
   _line(self, **kwargs)
