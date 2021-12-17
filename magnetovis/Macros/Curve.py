from paraview.simple import *

MagnetovisCurve1 = MagnetovisCurve()

SetActiveSource(MagnetovisCurve1)

renderView1 = GetActiveViewOrCreate('RenderView')

MagnetovisCurve1Display = Show(MagnetovisCurve1, renderView1, 'GeometryRepresentation')


