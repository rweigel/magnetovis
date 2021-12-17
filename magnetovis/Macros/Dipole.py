# trace generated using paraview version 5.9.1

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'MagnetovisDipole'
magnetovisDipole1 = MagnetovisDipole(registrationName='MagnetovisDipole1')

if True:
    # Properties modified on magnetovisDipole1
    magnetovisDipole1.NxNyNz = [10, 10, 10]

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')

    # show data in view
    magnetovisDipole1Display = Show(magnetovisDipole1, renderView1, 'StructuredGridRepresentation')

    # trace defaults for the display properties.
    magnetovisDipole1Display.Representation = 'Outline'
    magnetovisDipole1Display.ColorArrayName = [None, '']
    magnetovisDipole1Display.SelectTCoordArray = 'None'
    magnetovisDipole1Display.SelectNormalArray = 'None'
    magnetovisDipole1Display.SelectTangentArray = 'None'
    magnetovisDipole1Display.OSPRayScaleArray = 'B'
    magnetovisDipole1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    magnetovisDipole1Display.SelectOrientationVectors = 'None'
    magnetovisDipole1Display.ScaleFactor = 8.0
    magnetovisDipole1Display.SelectScaleArray = 'None'
    magnetovisDipole1Display.GlyphType = 'Arrow'
    magnetovisDipole1Display.GlyphTableIndexArray = 'None'
    magnetovisDipole1Display.GaussianRadius = 0.4
    magnetovisDipole1Display.SetScaleArray = ['POINTS', 'B']
    magnetovisDipole1Display.ScaleTransferFunction = 'PiecewiseFunction'
    magnetovisDipole1Display.OpacityArray = ['POINTS', 'B']
    magnetovisDipole1Display.OpacityTransferFunction = 'PiecewiseFunction'
    magnetovisDipole1Display.DataAxesGrid = 'GridAxesRepresentation'
    magnetovisDipole1Display.PolarAxes = 'PolarAxesRepresentation'
    magnetovisDipole1Display.ScalarOpacityUnitDistance = 15.396007178390022

    # init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
    magnetovisDipole1Display.ScaleTransferFunction.Points = [-1.707228354432908e+20, 0.0, 0.5, 0.0, 1.707228354432908e+20, 1.0, 0.5, 0.0]

    # init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
    magnetovisDipole1Display.OpacityTransferFunction.Points = [-1.707228354432908e+20, 0.0, 0.5, 0.0, 1.707228354432908e+20, 1.0, 0.5, 0.0]

    # reset view to fit data
    renderView1.ResetCamera()

    # get the material library
    materialLibrary1 = GetMaterialLibrary()

    # update the view to ensure updated data information
    renderView1.Update()

    # set scalar coloring
    ColorBy(magnetovisDipole1Display, ('POINTS', 'B', 'Magnitude'))

    # rescale color and/or opacity maps used to include current data range
    magnetovisDipole1Display.RescaleTransferFunctionToDataRange(True, False)

    # show color bar/color legend
    magnetovisDipole1Display.SetScalarBarVisibility(renderView1, True)

    # get color transfer function/color map for 'dipole'
    dipoleLUT = GetColorTransferFunction('B')
    dipoleLUT.RGBPoints = [3.311914256388093e+17, 0.231373, 0.298039, 0.752941, 8.94216849224786e+18, 0.865003, 0.865003, 0.865003, 2.414385492906925e+20, 0.705882, 0.0156863, 0.14902]
    dipoleLUT.UseLogScale = 1
    dipoleLUT.ScalarRangeInitialized = 1.0

    # get opacity transfer function/opacity map for 'dipole'
    dipolePWF = GetOpacityTransferFunction('B')
    dipolePWF.Points = [3.311914256388087e+17, 0.0, 0.5, 0.0, 2.41438549290692e+20, 1.0, 0.5, 0.0]
    dipolePWF.ScalarRangeInitialized = 1

    # change representation type
    magnetovisDipole1Display.SetRepresentationType('Surface')

    # convert from log to linear
    dipoleLUT.MapControlPointsToLinearSpace()

    # convert to log space
    dipoleLUT.MapControlPointsToLogSpace()
