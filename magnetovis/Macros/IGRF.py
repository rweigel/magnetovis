# trace generated using paraview version 5.9.1

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'MagnetovisDipole'
IGRF = MagnetovisIGRF(registrationName='MagnetovisIGRF')

# Properties modified on IGRF
IGRF.NxNyNz = [10, 10, 10]

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
IGRFDisplay = Show(IGRF, renderView1, 'StructuredGridRepresentation')

# trace defaults for the display properties.
IGRFDisplay.Representation = 'Outline'
IGRFDisplay.ColorArrayName = [None, '']
IGRFDisplay.SelectTCoordArray = 'None'
IGRFDisplay.SelectNormalArray = 'None'
IGRFDisplay.SelectTangentArray = 'None'
IGRFDisplay.OSPRayScaleArray = 'B'
IGRFDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
IGRFDisplay.SelectOrientationVectors = 'None'
IGRFDisplay.ScaleFactor = 8.0
IGRFDisplay.SelectScaleArray = 'None'
IGRFDisplay.GlyphType = 'Arrow'
IGRFDisplay.GlyphTableIndexArray = 'None'
IGRFDisplay.GaussianRadius = 0.4
IGRFDisplay.SetScaleArray = ['POINTS', 'B']
IGRFDisplay.ScaleTransferFunction = 'PiecewiseFunction'
IGRFDisplay.OpacityArray = ['POINTS', 'B']
IGRFDisplay.OpacityTransferFunction = 'PiecewiseFunction'
IGRFDisplay.DataAxesGrid = 'GridAxesRepresentation'
IGRFDisplay.PolarAxes = 'PolarAxesRepresentation'
IGRFDisplay.ScalarOpacityUnitDistance = 15.396007178390022

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
IGRFDisplay.ScaleTransferFunction.Points = [-1.707228354432908e+20, 0.0, 0.5, 0.0, 1.707228354432908e+20, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
IGRFDisplay.OpacityTransferFunction.Points = [-1.707228354432908e+20, 0.0, 0.5, 0.0, 1.707228354432908e+20, 1.0, 0.5, 0.0]

# reset view to fit data
renderView1.ResetCamera()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(IGRFDisplay, ('POINTS', 'B', 'Magnitude'))

# rescale color and/or opacity maps used to include current data range
IGRFDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
IGRFDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'B'
BLUT = GetColorTransferFunction('B')
BLUT.RGBPoints = [3.311914256388093e+17, 0.231373, 0.298039, 0.752941, 8.94216849224786e+18, 0.865003, 0.865003, 0.865003, 2.414385492906925e+20, 0.705882, 0.0156863, 0.14902]
BLUT.UseLogScale = 1
BLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'B'
BPWF = GetOpacityTransferFunction('B')
BPWF.Points = [3.311914256388087e+17, 0.0, 0.5, 0.0, 2.41438549290692e+20, 1.0, 0.5, 0.0]
BPWF.ScalarRangeInitialized = 1

# change representation type
IGRFDisplay.SetRepresentationType('Surface')

# convert from log to linear
BLUT.MapControlPointsToLinearSpace()

# convert to log space
BLUT.MapControlPointsToLogSpace()
