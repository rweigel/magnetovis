# trace generated using paraview version 5.9.1

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'MagnetovisDipole'
magnetovisT89c = MagnetovisT89c(registrationName='MagnetovisT89c')

# Properties modified on magnetovisT89c
magnetovisT89c.NxNyNz = [10, 10, 10]

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
magnetovisT89cDisplay = Show(magnetovisT89c, renderView1, 'StructuredGridRepresentation')

# trace defaults for the display properties.
magnetovisT89cDisplay.Representation = 'Outline'
magnetovisT89cDisplay.ColorArrayName = [None, '']
magnetovisT89cDisplay.SelectTCoordArray = 'None'
magnetovisT89cDisplay.SelectNormalArray = 'None'
magnetovisT89cDisplay.SelectTangentArray = 'None'
magnetovisT89cDisplay.OSPRayScaleArray = 'B'
magnetovisT89cDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
magnetovisT89cDisplay.SelectOrientationVectors = 'None'
magnetovisT89cDisplay.ScaleFactor = 8.0
magnetovisT89cDisplay.SelectScaleArray = 'None'
magnetovisT89cDisplay.GlyphType = 'Arrow'
magnetovisT89cDisplay.GlyphTableIndexArray = 'None'
magnetovisT89cDisplay.GaussianRadius = 0.4
magnetovisT89cDisplay.SetScaleArray = ['POINTS', 'B']
magnetovisT89cDisplay.ScaleTransferFunction = 'PiecewiseFunction'
magnetovisT89cDisplay.OpacityArray = ['POINTS', 'B']
magnetovisT89cDisplay.OpacityTransferFunction = 'PiecewiseFunction'
magnetovisT89cDisplay.DataAxesGrid = 'GridAxesRepresentation'
magnetovisT89cDisplay.PolarAxes = 'PolarAxesRepresentation'
magnetovisT89cDisplay.ScalarOpacityUnitDistance = 15.396007178390022

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
magnetovisT89cDisplay.ScaleTransferFunction.Points = [-1.707228354432908e+20, 0.0, 0.5, 0.0, 1.707228354432908e+20, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
magnetovisT89cDisplay.OpacityTransferFunction.Points = [-1.707228354432908e+20, 0.0, 0.5, 0.0, 1.707228354432908e+20, 1.0, 0.5, 0.0]

# reset view to fit data
renderView1.ResetCamera()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(magnetovisT89cDisplay, ('POINTS', 'B', 'Magnitude'))

# rescale color and/or opacity maps used to include current data range
magnetovisT89cDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
magnetovisT89cDisplay.SetScalarBarVisibility(renderView1, True)

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
magnetovisT89cDisplay.SetRepresentationType('Surface')

# convert from log to linear
BLUT.MapControlPointsToLinearSpace()

# convert to log space
BLUT.MapControlPointsToLogSpace()
