# trace generated using paraview version 5.9.1
# https://blog.kitware.com/defining-time-varying-sources-with-paraviews-programmable-source/

import paraview.simple as pvs

# create a new 'Programmable Source'
sphere = pvs.ProgrammableSource(registrationName='sphere')

sphere.Script = """
import vtk

outInfo = self.GetOutputInformation(0)
if outInfo.Has(vtk.vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP()):
  time = outInfo.Get(vtk.vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP())
else:
  time = 0

radius = math.sin(time * 2 * math.pi / 100) + 1.0
sphere = vtk.vtkSphereSource()
sphere.SetRadius(radius)
sphere.Update()

pd = self.GetPolyDataOutput()
pd.ShallowCopy(sphere.GetOutput())"""
sphere.ScriptRequestInformation = """
timeSteps = range(100)
outInfo = self.GetOutputInformation(0)
timeRange = [timeSteps[0], timeSteps[-1]]
outInfo.Set(vtk.vtkStreamingDemandDrivenPipeline.TIME_RANGE(), timeRange, 2)
outInfo.Set(vtk.vtkStreamingDemandDrivenPipeline.TIME_STEPS(), timeSteps, len(timeSteps))"""

# get active view
renderView = pvs.GetActiveViewOrCreate('RenderView')

# show data in view
sphereDisplay = pvs.Show(sphere, renderView, 'GeometryRepresentation')

# trace defaults for the display properties.
sphereDisplay.Representation = 'Surface'

# get animation scene
animationScene1 = pvs.GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# update the view to ensure updated data information
renderView.Update()
