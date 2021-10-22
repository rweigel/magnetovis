# trace generated using paraview version 5.9.1

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

MagnetovisLine1 = MagnetovisLine(Npts=5)

SetActiveSource(MagnetovisLine1)

renderView1 = GetActiveViewOrCreate('RenderView')

MagnetovisLine1Display = Show(MagnetovisLine1, renderView1, 'GeometryRepresentation')

from magnetovis.Line import Display
MagnetovisLine1Display = Display(MagnetovisLine1, MagnetovisLine1Display, renderView1)

