url = 'http://mag.gmu.edu/git-data/swmfio/3d__var_2_e20190902-041000-000.vtk'
vtkfile = "/tmp/" + url.split("/")[-1]

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
                    'TitleJustification': 'Left',
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
