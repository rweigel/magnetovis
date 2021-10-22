from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

MagnetovisAxis1 = MagnetovisAxis()

SetActiveSource(MagnetovisAxis1)

renderView1 = GetActiveViewOrCreate('RenderView')

MagnetovisAxis1Display = Show(MagnetovisAxis1, renderView1, 'GeometryRepresentation')

from magnetovis.Axis import Display
MagnetovisLine1Display = Display(MagnetovisAxis1, MagnetovisAxis1Display, renderView1)
