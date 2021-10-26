from paraview.simple import *

MagnetovisCurve1 = MagnetovisCurve(Npts=5)

SetActiveSource(MagnetovisCurve1)

renderView1 = GetActiveViewOrCreate('RenderView')

MagnetovisCurve1Display = Show(MagnetovisCurve1, renderView1, 'GeometryRepresentation')


