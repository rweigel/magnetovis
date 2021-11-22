import vtk
cube = vtk.vtkWaveletSource()
plane = vtk.vtkPlane()
plane.SetOrigin(cube.GetCenter())
plane.SetNormal(0, 0, 1)
      
output = self.GetPolyDataOutput()
#create cutter
cutter=vtk.vtkCutter()
cutter.SetCutFunction(plane)
cutter.SetInputConnection(cube.GetOutputPort())
cutter.Update()
#output = cutter.GetOutput()
#output.DeepCopy(cutter.GetOutput())
output.DeepCopy(cube.GetOutput())