# Demo 1
import paraview.simple as pvs
import magnetovis as mvs
mvs.ClearPipeline()
grid = mvs.GridData()

mvs.SetRepresentation('Wireframe')
mvs.SetColor('blue')

# TODO:
#   1. Code that looks for number of unique values in SetTransferFunctionDefaults
#      should round numbers for annotations.
#   2. The coloring of the tube here is based on interpolation. Create
#      mvs.SegmentedTube() that gives a tube with uniform color for each
#      segment. 
line = pvs.Line(Point1=[0.9, 0.0, 0.0], Point2=[0.0, 0.9, 0.9], Resolution=3)
curve = mvs.CurveProbe(Input=[grid, line])
tube = pvs.Tube(Input=curve, Radius=0.01)
mvs.SetColoring(["POINTS", "xyz", "X"])
mvs.SetCamera(viewType='isometric')