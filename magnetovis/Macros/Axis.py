from paraview.simple import *

paraview.simple._DisableFirstRenderCameraReset()

MagnetovisAxis1 = MagnetovisAxis()

SetActiveSource(MagnetovisAxis1)

renderView1 = GetActiveViewOrCreate('RenderView')

MagnetovisAxis1Display = Show(MagnetovisAxis1, renderView1, 'GeometryRepresentation')

