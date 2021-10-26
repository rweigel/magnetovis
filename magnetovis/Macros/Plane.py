# trace generated using paraview version 5.9.1

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

MagnetovisPlane1 = MagnetovisPlane()

SetActiveSource(MagnetovisPlane1)

renderView1 = GetActiveViewOrCreate('RenderView')

MagnetovisPlane1Display = Show(MagnetovisPlane1, renderView1, 'GeometryRepresentation')
