# This program demonstrates how to use programmable source to create a complex VTK object
# that could not be created using paraview.simple.

# Usage:
#   from objs import helix
#   line(nPts=10)

def _line(self, numPts):
   # Content that one would enter into the Programmable Source text area in the ParaView GUI.
   import vtk

   length = 8.0
   pdo = self.GetPolyDataOutput()

   newPts = vtk.vtkPoints()
   for i in range(0, numPts):
      x = i*length/numPts
      y = x
      z = x
      newPts.InsertPoint(i, x,y,z)

   pdo.SetPoints(newPts)

   aPolyLine = vtk.vtkPolyLine()

   aPolyLine.GetPointIds().SetNumberOfIds(numPts)
   for i in range(0, numPts):
      aPolyLine.GetPointIds().SetId(i, i)

   pdo.Allocate(1, 1)
   pdo.InsertNextCell(aPolyLine.GetCellType(), aPolyLine.GetPointIds())


def wrapper(renderView=None, **kwargs):
   import paraview.simple as pvs 

   # create a new 'Programmable Source'
   programmableSource1 = pvs.ProgrammableSource()

   # Generate programmable source script. The script is this file with 
   # a dict named 'kwargs' prepended. When this script is executed and
   # 'kwargs' is defined, the function _line(self, nPts=kwargs['nPts'])
   # is called.
   programmableSource1.Script = "kwargs=" +  str(kwargs) + ";execfile('" + __file__ + "', globals(),locals())"
   
   if not 'RenderView' in kwargs:
      renderView1 = pvs.GetActiveViewOrCreate('RenderView')
   else:
      renderView1 = kwargs['renderView']
   
   # show data
   programmableSource1Display = pvs.Show(programmableSource1, renderView1)

   # update the view
   renderView1.Update()

def line(nPts=10):
   import paraview.simple as pvs    
   renderView1 = pvs.GetActiveViewOrCreate('RenderView')
   wrapper(nPts=10, obj='line', renderView=renderView1)

if 'kwargs' in vars():   
   if 'line' == kwargs['obj']:
      _line(self, kwargs['nPts'])