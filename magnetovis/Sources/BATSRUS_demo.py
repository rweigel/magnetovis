# Execute using
#   magnetovis BATSRUS_demo.py

# Demo 1
import magnetovis as mvs
# See BATSRUS_prep.py for downloading this file.
vtkfile = "/tmp/3d__var_2_e20190902-041000-000.vtk"

batsrus = mvs.BATSRUS(file=vtkfile)
mvs.SetTitle("Default")

# Demo 2
import magnetovis as mvs
mvs.CreateViewAndLayout()
batsrus = mvs.BATSRUS(file=vtkfile)
mvs.SetTitle("Run files: http://mag.gmu.edu/git-data/swmfio/3d__var_2_e20190902-041000-000.*")

# Add slice
import paraview.simple as pvs
pvs.Hide(batsrus)

view = pvs.GetActiveViewOrCreate('RenderView')

sliceY = pvs.Slice(registrationName=' y=0 slice', Input=batsrus)
sliceY.SliceType = 'Plane'
sliceY.SliceType.Normal = [0.0, 1.0, 0.0]

sliceZ = pvs.Slice(registrationName=' z=0 slice', Input=batsrus)
sliceZ.SliceType = 'Plane'
sliceZ.SliceType.Normal = [0.0, 0.0, 1.0]

sliceYDisplay = pvs.Show(sliceY, view, 'GeometryRepresentation')
sliceZDisplay = pvs.Show(sliceZ, view, 'GeometryRepresentation')

pvs.Hide3DWidgets(proxy=sliceY.SliceType)
pvs.Hide3DWidgets(proxy=sliceZ.SliceType)

ckwargs =  {
    'colorBy': ('CELLS', 'rho'),
    'scalarBar': {
                    'Title': r"ρ [m$_p$/cm$^3$]",
                    'ComponentTitle': '',
                    'HorizontalTitle': 1,
                    'TitleJustification': 'Left',
                    'Visibility': 1,
                    'ScalarBarLength': 0.8
                },
    'colorTransferFunction': {
                                "UseLogScale": 1 
                            }
}

mvs.SetColoring(source=sliceY, display=sliceYDisplay, **ckwargs)

sliceZDisplay.SetScalarBarVisibility(view, False)


# Demo 3
import magnetovis as mvs
mvs.CreateViewAndLayout()
batsrus = mvs.BATSRUS(file=vtkfile)
mvs.SetTitle("Cells colored by block_id")

# See next example for setting coloring using mvs.SetColoring()
import paraview.simple as pvs
view = pvs.GetActiveViewOrCreate('RenderView')
display = pvs.GetDisplayProperties(proxy=batsrus, view=view)
pvs.ColorBy(display, ('CELLS', 'block_id'), separate=True)
pvs.UpdateScalarBars(view=view)
view.Update()

# Demo 4
import magnetovis as mvs
import paraview.simple as pvs
mvs.CreateViewAndLayout()
batsrus = mvs.BATSRUS(file=vtkfile)
pvs.Hide(batsrus)

akwargs = {"label": {"display": {"Color": [0, 0, 0]}}}
xAxis = mvs.Axis(direction="X", extent=[0, 70], vtkTubeFilter=['Radius: 2'])
mvs.SetPresentationProperties(xAxis, **akwargs)
yAxis = mvs.Axis(direction="Y", extent=[0, 70], vtkTubeFilter=['Radius: 2'])
mvs.SetPresentationProperties(yAxis, **akwargs)
zAxis = mvs.Axis(direction="Z", extent=[0, 140], vtkTubeFilter=['Radius: 2'])
mvs.SetPresentationProperties(zAxis, **akwargs)

mvs.SetTitle('Simulation Grid Cube Side Length')

# Compute Cell volumes
cellSize1 = pvs.CellSize(registrationName='CellSize', Input=batsrus)
cellSize1.ComputeVertexCount = 0
cellSize1.ComputeLength = 0
cellSize1.ComputeArea = 0
cellSize1.ComputeVolume = 1

# Compute Cell side length
calculator1 = pvs.Calculator(registrationName='Calculator1', Input=cellSize1)
calculator1.AttributeType = 'Cell Data'
calculator1.ResultArrayName = 'Δ'
calculator1.Function = 'round(10000*Volume^(1/3))/10000'

# The use of Volume^(1/3) calculation leads to values such as 
# 06250000000000001. The use of round(...) above addresses this.

clip1 = pvs.Clip(registrationName='Clip1', Input=calculator1)
clip1.ClipType = 'Plane'
clip1.HyperTreeGridClipper = 'Plane'
clip1.Scalars = ['CELLS', 'Δ']
clip1.Value = 0.0
clip1.ClipType.Origin = [0.0, 0.0, 0.0]
clip1.ClipType.Origin = [0.0, 0.0, 0.0]
clip1.ClipType.Normal = [0.0, 1.0, 0.0]


ckwargs =  {
    'scalarBar': {
                    'Title': r"Δ [R$_E$]",
                    'ComponentTitle': '',
                    'HorizontalTitle': 1,
                    'TitleJustification': 'Centered',
                    'Visibility': 1,
                    'ScalarBarLength': 0.8
                },
    'colorTransferFunction': {
                                'InterpretValuesAsCategories': 1,
                                'Annotations': ['0.0625', '1/16', '0.125', '1/8', '0.25', '1/4', '0.5', '1/2', '1', '1', '2', '2', '4.0', '4', '8.0', '8']
                            }
}

from paraview.simple import *

# get active view
renderView2 = GetActiveViewOrCreate('RenderView')

# get display properties
clip1Display = GetDisplayProperties(clip1, view=renderView2)

# get active source.
clip1 = GetActiveSource()


pvs.ResetCamera()
pvs.Hide3DWidgets(proxy=clip1.ClipType)

mvs.SetColoring(('CELLS', 'Δ'), source=clip1, view=renderView2, display=clip1Display, **ckwargs)

# Demo 5
# This demo shows an issue with the VTK StreamTracer when tracing line
# in the native BATSRUS grid. Some of the stream lines stop and the
# reason for stopping does not seem to be correct. In Demo 5, the
# data are interpolated to a uniform grid and then the stream tracing
# works as expected.
import magnetovis as mvs
import paraview.simple as pvs
from paraview.simple import *

mvs.CreateViewAndLayout()
batsrus = mvs.BATSRUS(file=vtkfile)

# http://davis.lbl.gov/Manuals/VTK-4.5/classvtkStreamTracer.html
# OUT_OF_DOMAIN = 1
# NOT_INITIALIZED = 2
# UNEXPECTED_VALUE = 3
# OUT_OF_TIME = 4
# OUT_OF_STEPS = 5
# STAGNATION =6

pvs.Hide(batsrus)

# create a new 'Stream Tracer'
streamTracer1 = StreamTracer(registrationName='StreamTracer1', Input=batsrus, SeedType='Line')
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

view = GetActiveViewOrCreate('RenderView')

# show data in view
streamTracer1Display = Show(streamTracer1, view, 'GeometryRepresentation')

# set active source
SetActiveSource(streamTracer1)

# set scalar coloring
ColorBy(streamTracer1Display, ('CELLS', 'ReasonForTermination'), separate=True)

# rescale color and/or opacity maps used to include current data range
streamTracer1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
streamTracer1Display.SetScalarBarVisibility(view, True)

# get color transfer function/color map for 'ReasonForTermination'
reasonForTerminationLUT = GetColorTransferFunction('ReasonForTermination', streamTracer1Display, separate=True)
reasonForTerminationLUT.RGBPoints = [1.0, 0.231373, 0.298039, 0.752941, 3.0, 0.865003, 0.865003, 0.865003, 5.0, 0.705882, 0.0156863, 0.14902]
reasonForTerminationLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'ReasonForTermination'
reasonForTerminationPWF = GetOpacityTransferFunction('ReasonForTermination', streamTracer1Display, separate=True)
reasonForTerminationPWF.Points = [1.0, 0.0, 0.5, 0.0, 5.0, 1.0, 0.5, 0.0]
reasonForTerminationPWF.ScalarRangeInitialized = 1

# Properties modified on reasonForTerminationLUT
reasonForTerminationLUT.InterpretValuesAsCategories = 1
reasonForTerminationLUT.AnnotationsInitialized = 1

# Properties modified on reasonForTerminationLUT
reasonForTerminationLUT.Annotations = ['1', '1', '5', '5']
reasonForTerminationLUT.IndexedColors = [1.0, 1.0, 1.0, 1.0, 0.0, 0.0]
reasonForTerminationLUT.IndexedOpacities = [1.0, 1.0]

pvs.ResetCamera()
