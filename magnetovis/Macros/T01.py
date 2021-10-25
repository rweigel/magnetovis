# trace generated using paraview version 5.9.1

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'MagnetovisDipole'
magnetovisT01 = MagnetovisT01(registrationName='MagnetovisT01')

# Properties modified on magnetovisT01
magnetovisT01.NxNyNz = [10, 10, 10]

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
magnetovisT01Display = Show(magnetovisT01, renderView1, 'StructuredGridRepresentation')

# trace defaults for the display properties.
magnetovisT01Display.Representation = 'Outline'
magnetovisT01Display.ColorArrayName = [None, '']
magnetovisT01Display.SelectTCoordArray = 'None'
magnetovisT01Display.SelectNormalArray = 'None'
magnetovisT01Display.SelectTangentArray = 'None'
magnetovisT01Display.OSPRayScaleArray = 'B'
magnetovisT01Display.OSPRayScaleFunction = 'PiecewiseFunction'
magnetovisT01Display.SelectOrientationVectors = 'None'
magnetovisT01Display.ScaleFactor = 8.0
magnetovisT01Display.SelectScaleArray = 'None'
magnetovisT01Display.GlyphType = 'Arrow'
magnetovisT01Display.GlyphTableIndexArray = 'None'
magnetovisT01Display.GaussianRadius = 0.4
magnetovisT01Display.SetScaleArray = ['POINTS', 'B']
magnetovisT01Display.ScaleTransferFunction = 'PiecewiseFunction'
magnetovisT01Display.OpacityArray = ['POINTS', 'B']
magnetovisT01Display.OpacityTransferFunction = 'PiecewiseFunction'
magnetovisT01Display.DataAxesGrid = 'GridAxesRepresentation'
magnetovisT01Display.PolarAxes = 'PolarAxesRepresentation'
magnetovisT01Display.ScalarOpacityUnitDistance = 15.396007178390022

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
magnetovisT01Display.ScaleTransferFunction.Points = [-1.707228354432908e+20, 0.0, 0.5, 0.0, 1.707228354432908e+20, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
magnetovisT01Display.OpacityTransferFunction.Points = [-1.707228354432908e+20, 0.0, 0.5, 0.0, 1.707228354432908e+20, 1.0, 0.5, 0.0]

# reset view to fit data
renderView1.ResetCamera()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(magnetovisT01Display, ('POINTS', 'B', 'Magnitude'))

# rescale color and/or opacity maps used to include current data range
magnetovisT01Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
magnetovisT01Display.SetScalarBarVisibility(renderView1, True)

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
magnetovisT01Display.SetRepresentationType('Surface')

# convert from log to linear
BLUT.MapControlPointsToLinearSpace()

# convert to log space
BLUT.MapControlPointsToLogSpace()
