from paraview.simple import *

MagnetovisStructuredGrid1 = MagnetovisStructuredGrid()

SetActiveSource(MagnetovisStructuredGrid1)

renderView1 = GetActiveViewOrCreate('RenderView')

renderView1.CameraPosition = [529., 282., 247.]
renderView1.CameraViewUp = [-0.33, -0.19, 0.92]

MagnetovisStructuredGrid1Display = Show(MagnetovisStructuredGrid1, renderView1, 'GeometryRepresentation')

# change representation type
MagnetovisStructuredGrid1Display.SetRepresentationType('Surface')

# set scalar coloring
ColorBy(MagnetovisStructuredGrid1Display, ('CELLS', 'cell_index'))

# rescale color and/or opacity maps used to include current data range
MagnetovisStructuredGrid1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
MagnetovisStructuredGrid1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'cell_index'
cell_indexLUT = GetColorTransferFunction('cell_index')
cell_indexLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 3.5, 0.865003, 0.865003, 0.865003, 7.0, 0.705882, 0.0156863, 0.14902]
cell_indexLUT.ScalarRangeInitialized = 1.0

ResetCamera()