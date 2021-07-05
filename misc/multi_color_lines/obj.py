import vtk

def _lines(self, n):
    
    pdo = self.GetPolyDataOutput()
    pdo.Allocate(n, 1)
    
    # color section
    colors = vtk.vtkUnsignedCharArray();
    # The number of components in the tuple to be inserted must be declared first
    colors.SetNumberOfComponents(1);
    colors.SetName("regions2");
    
    # Store the points
    newPts = vtk.vtkPoints()

    # The first number is the id of point; the next three numbers are the
    # x,y,z values
    for i in range(0, n):
        newPts.InsertPoint(2*i, 0, 0,i)
        newPts.InsertPoint(2*i+1, 1, 0, i)
        
    # Add the points to the vtkPolyData object
    pdo.SetPoints(newPts)
    
    # create line objects and assign them points based on the id of the point
    for i in range(n):
        aPolyLine = vtk.vtkPolyLine()
        aPolyLine.GetPointIds().SetNumberOfIds(2)
        aPolyLine.GetPointIds().SetId(0, 2*i) 
        aPolyLine.GetPointIds().SetId(1, 2*i+1)
        pdo.InsertNextCell(aPolyLine.GetCellType(), aPolyLine.GetPointIds())
        colors.InsertNextTuple([i])
        colors.InsertNextTuple([i])
    
    pdo.GetPointData().AddArray(colors)


def wrapper(**kwargs):
   import paraview.simple as pvs

   # create a new 'Programmable Source'
   programmableSource1 = pvs.ProgrammableSource()
   programmableSource1.Script = "kwargs="+str(kwargs)+";execfile('" + __file__ + "',globals(),locals())"
   programmableSource1.ScriptRequestInformation = ''
   programmableSource1.PythonPath = ''

   # get active view
   renderView1 = pvs.GetActiveViewOrCreate('RenderView')

   # show data in view
   programmableSource1Display = pvs.Show(programmableSource1, renderView1)
   
   # coloring the lines
   pvs.ColorBy(programmableSource1Display, ('POINTS', 'regions2'))
   programmableSource1Display.SetScalarBarVisibility(renderView1, True)
   regions2LUT = pvs.GetColorTransferFunction('regions2')
   regions2LUT.InterpretValuesAsCategories = 1
   regions2LUT.AnnotationsInitialized = 1
   
   # trace defaults for the display properties.
   programmableSource1Display.Representation = 'Surface'

   # update the view to ensure updated data information
   renderView1.Update()


def lines(n=10):
   wrapper(n=n, obj='line')


if 'kwargs' in vars():   
   if 'line' == kwargs['obj']:
      _lines(self,kwargs['n'])
      
      
      
      
      
      
      