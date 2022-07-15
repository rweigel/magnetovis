'''
# Demo #3
'''
import magnetovis as mvs
mvs.CreateViewAndLayout()
batsrus = mvs.BATSRUS()


# http://davis.lbl.gov/Manuals/VTK-4.5/classvtkStreamTracer.html
# OUT_OF_DOMAIN = 1
# NOT_INITIALIZED = 2
# UNEXPECTED_VALUE = 3
# OUT_OF_TIME = 4
# OUT_OF_STEPS = 5
# STAGNATION =6

from paraview.simple import *
# find source
bATSRUS3d__var_2_e20190902041000000GSM = FindSource('BATSRUS/3d__var_2_e20190902-041000-000/GSM')

# create a new 'Stream Tracer'
streamTracer1 = StreamTracer(registrationName='StreamTracer1', Input=bATSRUS3d__var_2_e20190902041000000GSM,
    SeedType='Line')
streamTracer1.Vectors = ['CELLS', 'b']
streamTracer1.MaximumStreamlineLength = 256.0

# Bug to report: When these are changed in the GUI, the
# changed values don't show in Python trace
# init the 'Line' selected for 'SeedType'
streamTracer1.SeedType.Point1 = [-3, 0, 0]
streamTracer1.SeedType.Point2 = [-10, 0, 0]
streamTracer1.SeedType.Resolution = 10

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=streamTracer1.SeedType)

# Properties modified on bATSRUS3d__var_2_e20190902041000000GSM
bATSRUS3d__var_2_e20190902041000000GSM.ScriptRequestInformation = ''
bATSRUS3d__var_2_e20190902041000000GSM.PythonPath = ''

# get active view
renderView2 = GetActiveViewOrCreate('RenderView')

# show data in view
streamTracer1Display = Show(streamTracer1, renderView2, 'GeometryRepresentation')

# trace defaults for the display properties.
streamTracer1Display.Representation = 'Surface'
streamTracer1Display.ColorArrayName = [None, '']
streamTracer1Display.SelectTCoordArray = 'None'
streamTracer1Display.SelectNormalArray = 'None'
streamTracer1Display.SelectTangentArray = 'None'
streamTracer1Display.OSPRayScaleArray = 'AngularVelocity'
streamTracer1Display.OSPRayScaleFunction = 'PiecewiseFunction'
streamTracer1Display.SelectOrientationVectors = 'Normals'
streamTracer1Display.ScaleFactor = 5.130233970252448
streamTracer1Display.SelectScaleArray = 'AngularVelocity'
streamTracer1Display.GlyphType = 'Arrow'
streamTracer1Display.GlyphTableIndexArray = 'AngularVelocity'
streamTracer1Display.GaussianRadius = 0.2565116985126224
streamTracer1Display.SetScaleArray = ['POINTS', 'AngularVelocity']
streamTracer1Display.ScaleTransferFunction = 'PiecewiseFunction'
streamTracer1Display.OpacityArray = ['POINTS', 'AngularVelocity']
streamTracer1Display.OpacityTransferFunction = 'PiecewiseFunction'
streamTracer1Display.DataAxesGrid = 'GridAxesRepresentation'
streamTracer1Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
streamTracer1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
streamTracer1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]

# hide data in view
Hide(bATSRUS3d__var_2_e20190902041000000GSM, renderView2)

# update the view to ensure updated data information
renderView2.Update()

# set active source
SetActiveSource(bATSRUS3d__var_2_e20190902041000000GSM)

# show data in view
bATSRUS3d__var_2_e20190902041000000GSMDisplay = Show(bATSRUS3d__var_2_e20190902041000000GSM, renderView2, 'UnstructuredGridRepresentation')

# get separate color transfer function/color map for 'b'
separate_bATSRUS3d__var_2_e20190902041000000GSMDisplay_bLUT = GetColorTransferFunction('b', bATSRUS3d__var_2_e20190902041000000GSMDisplay, separate=True)
separate_bATSRUS3d__var_2_e20190902041000000GSMDisplay_bLUT.RGBPoints = [0.0984629991587708, 0.231373, 0.298039, 0.752941, 156029167.90937236, 0.865003, 0.865003, 0.865003, 312058335.7202817, 0.705882, 0.0156863, 0.14902]
separate_bATSRUS3d__var_2_e20190902041000000GSMDisplay_bLUT.NumberOfTableValues = 32
separate_bATSRUS3d__var_2_e20190902041000000GSMDisplay_bLUT.ScalarRangeInitialized = 1.0

# get separate opacity transfer function/opacity map for 'b'
separate_bATSRUS3d__var_2_e20190902041000000GSMDisplay_bPWF = GetOpacityTransferFunction('b', bATSRUS3d__var_2_e20190902041000000GSMDisplay, separate=True)
separate_bATSRUS3d__var_2_e20190902041000000GSMDisplay_bPWF.Points = [0.0984629991587708, 0.0, 0.5, 0.0, 312058335.7202817, 1.0, 0.5, 0.0]
separate_bATSRUS3d__var_2_e20190902041000000GSMDisplay_bPWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
bATSRUS3d__var_2_e20190902041000000GSMDisplay.Representation = 'Surface'
bATSRUS3d__var_2_e20190902041000000GSMDisplay.AmbientColor = [0.5, 0.5, 0.5]
bATSRUS3d__var_2_e20190902041000000GSMDisplay.ColorArrayName = ['CELLS', 'b']
bATSRUS3d__var_2_e20190902041000000GSMDisplay.DiffuseColor = [0.5, 0.5, 0.5]
bATSRUS3d__var_2_e20190902041000000GSMDisplay.LookupTable = separate_bATSRUS3d__var_2_e20190902041000000GSMDisplay_bLUT
bATSRUS3d__var_2_e20190902041000000GSMDisplay.SelectTCoordArray = 'None'
bATSRUS3d__var_2_e20190902041000000GSMDisplay.SelectNormalArray = 'None'
bATSRUS3d__var_2_e20190902041000000GSMDisplay.SelectTangentArray = 'None'
bATSRUS3d__var_2_e20190902041000000GSMDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
bATSRUS3d__var_2_e20190902041000000GSMDisplay.SelectOrientationVectors = 'b'
bATSRUS3d__var_2_e20190902041000000GSMDisplay.ScaleFactor = 25.6
bATSRUS3d__var_2_e20190902041000000GSMDisplay.SelectScaleArray = 'rho'
bATSRUS3d__var_2_e20190902041000000GSMDisplay.GlyphType = 'Arrow'
bATSRUS3d__var_2_e20190902041000000GSMDisplay.GlyphTableIndexArray = 'rho'
bATSRUS3d__var_2_e20190902041000000GSMDisplay.GaussianRadius = 1.28
bATSRUS3d__var_2_e20190902041000000GSMDisplay.SetScaleArray = [None, '']
bATSRUS3d__var_2_e20190902041000000GSMDisplay.ScaleTransferFunction = 'PiecewiseFunction'
bATSRUS3d__var_2_e20190902041000000GSMDisplay.OpacityArray = [None, '']
bATSRUS3d__var_2_e20190902041000000GSMDisplay.OpacityTransferFunction = 'PiecewiseFunction'
bATSRUS3d__var_2_e20190902041000000GSMDisplay.DataAxesGrid = 'GridAxesRepresentation'
bATSRUS3d__var_2_e20190902041000000GSMDisplay.PolarAxes = 'PolarAxesRepresentation'
bATSRUS3d__var_2_e20190902041000000GSMDisplay.ScalarOpacityFunction = separate_bATSRUS3d__var_2_e20190902041000000GSMDisplay_bPWF
bATSRUS3d__var_2_e20190902041000000GSMDisplay.ScalarOpacityUnitDistance = 2.4543889495772016
bATSRUS3d__var_2_e20190902041000000GSMDisplay.OpacityArrayName = ['CELLS', 'rho']

# show color bar/color legend
bATSRUS3d__var_2_e20190902041000000GSMDisplay.SetScalarBarVisibility(renderView2, True)

# hide data in view
Hide(bATSRUS3d__var_2_e20190902041000000GSM, renderView2)

# reset view to fit data
renderView2.ResetCamera(False)

# set active source
SetActiveSource(streamTracer1)

# set scalar coloring
ColorBy(streamTracer1Display, ('CELLS', 'ReasonForTermination'))

# rescale color and/or opacity maps used to include current data range
streamTracer1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
streamTracer1Display.SetScalarBarVisibility(renderView2, True)

# get color transfer function/color map for 'ReasonForTermination'
reasonForTerminationLUT = GetColorTransferFunction('ReasonForTermination')
reasonForTerminationLUT.RGBPoints = [1.0, 0.231373, 0.298039, 0.752941, 3.0, 0.865003, 0.865003, 0.865003, 5.0, 0.705882, 0.0156863, 0.14902]
reasonForTerminationLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'ReasonForTermination'
reasonForTerminationPWF = GetOpacityTransferFunction('ReasonForTermination')
reasonForTerminationPWF.Points = [1.0, 0.0, 0.5, 0.0, 5.0, 1.0, 0.5, 0.0]
reasonForTerminationPWF.ScalarRangeInitialized = 1

# Properties modified on reasonForTerminationLUT
reasonForTerminationLUT.InterpretValuesAsCategories = 1
reasonForTerminationLUT.AnnotationsInitialized = 1

# Properties modified on reasonForTerminationLUT
reasonForTerminationLUT.Annotations = ['1', '1', '5', '5']
reasonForTerminationLUT.IndexedColors = [1.0, 1.0, 1.0, 1.0, 0.0, 0.0]
reasonForTerminationLUT.IndexedOpacities = [1.0, 1.0]