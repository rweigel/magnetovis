## Axis.py
Source file: [Axis.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Axis.py) | Demo file: [Axis_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Axis_demo.py)

### Demo 1

```python
import magnetovis as mvs
mvs.Axis()
#mvs.PrintSourceDefaults('Axis')
mvs.SetTitle("Axis with default options")
#mvs.PrintDisplayDefaults('Axis', all=True)
```

![Axis_demo.py](magnetovis/Test/Figures/Axis_demo-1.png)

### Demo 2

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()

skwargs = {
            "time": "2001-01-01",
            "coord_sys": "GSM",
            "tube": True,
            "tubeAndCone": True,
            "tubeFilterSettings": ["Radius: 0.5", "Capping: 1"]
        }

dkwargs = {
            "display": {
                "Representation": "Surface",
                "Opacity": 1.0,
                "AmbientColor": [1, 1, 0],
                "DiffuseColor": [1, 1, 0],
                "Visibility": 1
            },

            "label":
                {
                    "source": {"Text": r"$\alpha^2$/β"},
                    "display": {
                        "FontSize": 24,
                        "Color": [1, 1, 0]
                    }
                }
        }


skwargs['direction'] = "X"
skwargs['extent'] = [-40, 40]
xAxis = mvs.Axis()

skwargs['direction'] = "Y"
skwargs['extent'] = [-40, 40]
yAxis = mvs.Axis(registrationName="s^2/β Axis", **skwargs)
mvs.SetDisplayProperties(source=yAxis, **dkwargs)
mvs.SetTitle("Three Axes")

skwargs['direction'] = "Z"
skwargs['extent'] = [-40, 40]
zAxis = mvs.Axis(**skwargs)
```

![Axis_demo.py](magnetovis/Test/Figures/Axis_demo-2.png)

## BATSRUS.py
Source file: [BATSRUS.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/BATSRUS.py) | Demo file: [BATSRUS_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/BATSRUS_demo.py)

### Demo 1

```python
url = 'http://mag.gmu.edu/git-data/swmfio/3d__var_2_e20190902-041000-000'
vtkfile = '/tmp/mag.gmu.edu/git-data/swmfio/3d__var_2_e20190902-041000-000.vtk'
import os
if not os.path.exists(vtkfile):
  try:
    import swmfio
  except:
    print('\n\nInstall swmfio using')
    print('pip install "swmfio@git+https://github.com/GaryQ-physics/swmfio@main#egg=swmfio"\n')
    raise ModuleNotFoundError("Package swmfio must be installed.")

  import logging
  swmfio.logger.setLevel(logging.INFO)
  vtkfile = swmfio.write_vtk(url)

import magnetovis as mvs
batsrus = mvs.BATSRUS(file=vtkfile)
mvs.SetTitle("Default")
```

![BATSRUS_demo.py](magnetovis/Test/Figures/BATSRUS_demo-1.png)

### Demo 2

```python
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

mvs.SetColoring(source=sliceYDisplay, display=sliceYDisplay, **ckwargs)

sliceZDisplay.SetScalarBarVisibility(view, False)
```

![BATSRUS_demo.py](magnetovis/Test/Figures/BATSRUS_demo-2.png)

### Demo 3

```python
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
```

![BATSRUS_demo.py](magnetovis/Test/Figures/BATSRUS_demo-3.png)

### Demo 4

```python
import magnetovis as mvs
import paraview.simple as pvs
mvs.CreateViewAndLayout()
batsrus = mvs.BATSRUS(file=vtkfile)
pvs.Hide(batsrus)

akwargs = {"label": {"display": {"Color": [0, 0, 0]}}}
xAxis = mvs.Axis(direction="X", extent=[0, 70], vtkTubeFilter=['Radius: 2'])
mvs.SetDisplayProperties(xAxis, **akwargs)
yAxis = mvs.Axis(direction="Y", extent=[0, 70], vtkTubeFilter=['Radius: 2'])
mvs.SetDisplayProperties(yAxis, **akwargs)
zAxis = mvs.Axis(direction="Z", extent=[0, 140], vtkTubeFilter=['Radius: 2'])
mvs.SetDisplayProperties(zAxis, **akwargs)

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
    'colorBy': ('CELLS', 'Δ'),
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

mvs.SetColoring(source=clip1, view=renderView2, display=clip1Display, **ckwargs)
```

![BATSRUS_demo.py](magnetovis/Test/Figures/BATSRUS_demo-4.png)

### Demo 5

```python
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
```

![BATSRUS_demo.py](magnetovis/Test/Figures/BATSRUS_demo-5.png)

## Bowshock.py
Source file: [Bowshock.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Bowshock.py) | Demo file: [Bowshock_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Bowshock_demo.py)

### Demo 1

```python
import magnetovis as mvs
bowshock = mvs.Bowshock()
```

![Bowshock_demo.py](magnetovis/Test/Figures/Bowshock_demo-1.png)

## Curve.py
Source file: [Curve.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Curve.py) | Demo file: [Curve_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Curve_demo.py)

### Demo 1

```python
import magnetovis as mvs
mvs.Curve()
#mvs.PrintSourceDefaults('Curve')
mvs.SetTitle("Curve with default options")
#mvs.PrintDisplayDefaults('Curve', all=True)
```

![Curve_demo.py](magnetovis/Test/Figures/Curve_demo-1.png)

### Demo 2

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()

skwargs = {
            "time": "2001-01-01",
            "coord_sys": "GSM",
            "Npts": 5,
            "closed": True,
            "point_function": "circle(radius=1.0, origin=(0.0, 0.0, 0.0), orientation=(0, 0, 1))"
        }

dkwargs = {
        "display": {
            "Representation": "Surface",
            "Opacity": 1.0,
            "AmbientColor": [1, 1, 0],
            "DiffuseColor": [1, 1, 0],
            "Visibility": 1
        },
        'coloring': {
            'colorBy': None
        }
}

curve = mvs.Curve(**skwargs)
mvs.SetDisplayProperties(source=curve, **dkwargs)
mvs.SetTitle("Curve using alt kwargs for point fn")
```

![Curve_demo.py](magnetovis/Test/Figures/Curve_demo-2.png)

### Demo 3

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()

skwargs['closed'] = False
skwargs['Npts'] = 100
skwargs['point_function'] = "helix(radius=1.0, length=10, rounds=5)"

curve = mvs.Curve(**skwargs)
mvs.SetDisplayProperties(source=curve, **dkwargs)
mvs.SetTitle("Curve using alt point fn")
```

![Curve_demo.py](magnetovis/Test/Figures/Curve_demo-3.png)

### Demo 4

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()

def _randpts(Npts):

	import numpy as np
	return  -0.5 + np.random.random_sample([Npts,3])

from magnetovis import functions as mvsfunctions
mvsfunctions._randpts = _randpts

skwargs = {
            "time": "2001-01-01",
            "coord_sys": "GSM",
            "Npts": 100,
            "closed": False,
            "point_function": "_randpts()"
        }

dkwargs = {
        "display": {
            "Representation": "Surface",
            "Opacity": 1.0,
            "AmbientColor": [1, 1, 0],
            "DiffuseColor": [1, 1, 0],
            "Visibility": 1
        },
        'tube': None,
        'coloring': {
            'colorBy': None
        }
}

curve = mvs.Curve(**skwargs)
mvs.SetDisplayProperties(source=curve, **dkwargs)
mvs.SetTitle("Points from user-defined function; no tube.")
```

![Curve_demo.py](magnetovis/Test/Figures/Curve_demo-4.png)

### Demo #5

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()

def _parabola(Npts):

  import numpy as np
  xyz = np.zeros([Npts,3])

  xyz[:,1] = 40*np.linspace(-1,1,Npts)
  xyz[:,2] = xyz[:,1]**2/40

  return xyz 

from magnetovis import functions as mvsfunctions
mvsfunctions._parabola = _parabola

skwargs = {
            "time": "2001-01-01",
            "coord_sys": "GSM",
            "Npts": 100,
            "closed": False,
            "point_function": "_parabola()"
        }

dkwargs = {
        "display": {
            "Representation": "Surface",
            "Opacity": 1.0,
            "AmbientColor": [1, 1, 0],
            "DiffuseColor": [1, 1, 0],
            "Visibility": 1
        },
        'tube': {
            'source': {
                'Radius': 1.0
            }
        },
        'coloring': {
            'colorBy': ('POINTS', 'xyz', 'Z')
        }
}

mvs.Axis(direction="X")
mvs.Axis(direction="Y")
mvs.Axis(direction="Z")
curve = mvs.Curve(**skwargs)
mvs.SetDisplayProperties(source=curve, **dkwargs)
mvs.SetTitle("Parabola in Y-Z plane colored by Z")

# Color bar that appears by default has a minimum of 4.1e-3
# even though min of xyz >= 0. Not sure why this is. The max
# value is correct, however. The following resets
#import paraview.simple as pvs
import paraview.simple as pvs
curve1 = pvs.GetActiveSource()
renderView1 = pvs.GetActiveViewOrCreate('RenderView')
curve1Display = pvs.GetDisplayProperties(curve1, view=renderView1)
LUT = pvs.GetColorTransferFunction('xyz', curve1Display, separate=True)
LUT.RescaleTransferFunction(0.0, 40.0)
```

![Curve_demo.py](magnetovis/Test/Figures/Curve_demo-5.png)

## DifferentialDisk.py
Source file: [DifferentialDisk.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/DifferentialDisk.py) | Demo file: [DifferentialDisk_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/DifferentialDisk_demo.py)

### Demo 1

```python
import magnetovis as mvs
mvs.DifferentialDisk()
mvs.SetTitle("Differential Disk with Default Options")
```

![DifferentialDisk_demo.py](magnetovis/Test/Figures/DifferentialDisk_demo-1.png)

### Demo 2

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.DifferentialDisk(Nr=1)
mvs.SetTitle("Nr=1")
```

![DifferentialDisk_demo.py](magnetovis/Test/Figures/DifferentialDisk_demo-2.png)

### Demo 3

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.DifferentialDisk(ro=1, rf=2, Nφ=10, φo=0, φf=360)
mvs.SetTitle("ro=1, rf=2, Nφ=10, φo=0, φf=360")
```

![DifferentialDisk_demo.py](magnetovis/Test/Figures/DifferentialDisk_demo-3.png)

### Demo 4

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.DifferentialDisk(ro=1, rf=2, Nφ=10, φo=0, φf=80, closed=False)
mvs.SetTitle("$ro=1, rf=2, Nφ=10, φo=0, φf=80, closed=False$")
```

![DifferentialDisk_demo.py](magnetovis/Test/Figures/DifferentialDisk_demo-4.png)

## Dipole.py
Source file: [Dipole.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Dipole.py) | Demo file: [Dipole_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Dipole_demo.py)

### Demo 1

```python
import magnetovis as mvs
mvs.Dipole()
mvs.SetTitle("Dipole with Default Options")
```

![Dipole_demo.py](magnetovis/Test/Figures/Dipole_demo-1.png)

### Demo 2

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
dipole = mvs.Dipole(OutputDataSetType="vtkRectilinearGrid", dimensions=[10, 10, 10])
mvs.SetTitle("Dipole with Stream Trace and Slice")

import paraview.simple as pvs
pvs.Hide(dipole)

streamTracer1 = pvs.StreamTracer(registrationName='StreamTracer1', Input=dipole, SeedType='Line')
streamTracer1.Vectors = ['POINTS', 'B']
streamTracer1.MaximumStreamlineLength = 50.0

#pvs.ColorBy(streamTracer1Display, ('POINTS', 'B', 'Magnitude'))

streamTracer1.SeedType.Point1 = [-20.0, 0.0, 0.0]
streamTracer1.SeedType.Point2 = [-10.0, 0.0, 0.0]
streamTracer1.SeedType.Resolution = 10

pvs.SetActiveSource(streamTracer1)

streamTracer1Display = pvs.Show(streamTracer1)

slice1 = pvs.Slice(registrationName='Slice1', Input=dipole)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.SliceOffsetValues = [0.0]

slice1.SliceType.Normal = [0.0, 1.0, 0.0]

renderView1 = pvs.GetActiveViewOrCreate('RenderView')
slice1Display = pvs.Show(slice1, renderView1, 'GeometryRepresentation')
pvs.ColorBy(slice1Display, ('CELLS', 'B', 'Magnitude'))

sourceData = pvs.servermanager.Fetch(streamTracer1)
trace0 = sourceData.GetCell(0)
trace0Array = trace0.GetPoints().GetData()
from vtk.util import numpy_support
trace0 = numpy_support.vtk_to_numpy(trace0Array)
print("x, y, z for first trace:")
print(trace0)

pvs.Hide3DWidgets(proxy=slice1.SliceType)
```

![Dipole_demo.py](magnetovis/Test/Figures/Dipole_demo-2.png)

## Earth.py
Source file: [Earth.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Earth.py) | Demo file: [Earth_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Earth_demo.py)

### Demo 1

```python
import magnetovis as mvs
mvs.Earth()
mvs.SetTitle("  Earth with Default Options")
```

![Earth_demo.py](magnetovis/Test/Figures/Earth_demo-1.png)

### Demo 2

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.Earth()
mvs.SetTitle("  Earth with Axes")

xAxis = mvs.Axis(direction="X", extent=[-3, 3])
mvs.SetDisplayProperties(source=xAxis, 
		**{"label": {"source": {"Text": "$X_{GSM}$"}}})

yAxis = mvs.Axis(direction="Y", extent=[-3, 3])
mvs.SetDisplayProperties(source=yAxis, 
		**{"label": {"source": {"Text": "$Y_{GSM}$"}}})

zAxis = mvs.Axis(direction="Z", extent=[-3, 3])
mvs.SetDisplayProperties(source=zAxis, 
		**{"label": {"source": {"Text": "$Z_{GSM}$"}}})

dkwargs = {
			"display": {
				"AmbientColor": [0,0,0],
				"DiffuseColor": [0,0,0]
			},
			"label": {
				"source": {"Text": "$Z_{GEO}$"},
				"display": {"Color": [0,0,0]}
			}
		}
zAxis2 = mvs.Axis(direction="Z", extent=[-3, 3], coord_sys="GEO")
mvs.SetDisplayProperties(source=zAxis2, **dkwargs)
```

![Earth_demo.py](magnetovis/Test/Figures/Earth_demo-2.png)

## GridData.py
Source file: [GridData.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/GridData.py) | Demo file: [GridData_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/GridData_demo.py)

### Demo 1

```python
import magnetovis as mvs
mvs.GridData(OutputDataSetType="vtkImageData")
mvs.SetTitle("Dataset Type = vtkImageData")
```

![GridData_demo.py](magnetovis/Test/Figures/GridData_demo-1.png)

### Demo 2

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.GridData(OutputDataSetType="vtkRectilinearGrid")
mvs.SetTitle("Dataset Type = vtkRectilinearGrid")
```

![GridData_demo.py](magnetovis/Test/Figures/GridData_demo-2.png)

### Demo 3

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.GridData(OutputDataSetType="vtkStructuredGrid")
mvs.SetTitle("Dataset Type = vtkStructuredGrid")
```

![GridData_demo.py](magnetovis/Test/Figures/GridData_demo-3.png)

### Demo 4

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()

kwargs = {
        "time": "2001-01-01T00:00:00",
        "coord_sys": "GSM",
        "dimensions": [4,4,4],
        "point_array_functions": [
                                "dipole()",
                                "radius()"
                            ],
        "cell_array_functions": [
                                "r: radius()"
                            ],
        "dimensions": [10, 10, 10]
    }

registrationName = "Dipole on Structured Grid/{}/{}" \
                    .format(mvs.util.trim_iso(kwargs['time']), kwargs['coord_sys'])
kwargs["registrationName"] = registrationName

mvs.Axis(direction="X", extent=[0, 1.5], vtkTubeFilter=['Radius: 0.02'])
mvs.Axis(direction="Y", extent=[0, 1.5], vtkTubeFilter=['Radius: 0.02'])
mvs.Axis(direction="Z", extent=[0, 1.5], vtkTubeFilter=['Radius: 0.02'])

sg2 = mvs.GridData(**kwargs)

dkwargs = {
        "display": {
            "Representation": "Surface With Edges",
            "Opacity": 1.0,
            "AmbientColor": [1, 1, 0],
            "DiffuseColor": [1, 1, 0],
            "Visibility": 1
        },
        'coloring': {
            'colorBy': ('POINTS', 'dipole'),
            'scalarBar': {
                            'Title': r"$\|\mathbf{B}\|$ [nT]",
                            'ComponentTitle': '',
                            'HorizontalTitle': 1,
                            'TitleJustification': 'Left',
                            'Visibility': 1,
                            'DrawNanAnnotation': 1,
                            'ScalarBarLength': 0.8
                        },
            'colorTransferFunction': {
                                        'UseLogScale': 1,
                                        'AutomaticRescaleRangeMode': 1,
                                        'AutomaticRescaleRangeMode': "Grow and update on 'Apply'",
                                        'NumberOfTableValues': 4
                                    }
        }
}

mvs.SetDisplayProperties(**dkwargs)
mvs.SetCamera(Azimuth=225.0)
mvs.SetTitle(r"$\alpha$/β", title=registrationName)
```

![GridData_demo.py](magnetovis/Test/Figures/GridData_demo-4.png)

## Lines.py
Source file: [Lines.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Lines.py) | Demo file: [Lines_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Lines_demo.py)

### Demo 1

```python
import magnetovis as mvs
mvs.Lines()
#mvs.PrintSourceDefaults('Lines')
mvs.SetTitle("Line with default options")
#mvs.PrintDisplayDefaults('Lines', all=True)
```

![Lines_demo.py](magnetovis/Test/Figures/Lines_demo-1.png)

### Demo #2

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()

kwargs = {
            "time": "2001-01-01",
            "coord_sys": "GSM",
            "Nlines": 3,
            "closed": True,
            "point_function": "circle(radius=1.0, origin=(0.0, 0.0, 0.0), orientation=(0, 0, 1))"
        }

mvs.Lines(**kwargs)
```

![Lines_demo.py](magnetovis/Test/Figures/Lines_demo-2.png)

## MySource.py
Source file: [MySource.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/MySource.py) | Demo file: [MySource_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/MySource_demo.py)

### Demo 1

```python
exec(open("MySource.py").read())
MySource()
```

![MySource_demo.py](magnetovis/Test/Figures/MySource_demo-1.png)

## Plasmasphere.py
Source file: [Plasmasphere.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Plasmasphere.py) | Demo file: [Plasmasphere_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Plasmasphere_demo.py)

### Demo 1

```python
import magnetovis as mvs
mvs.Plasmasphere()
mvs.SetTitle('GCC88 Plasmasphere')
```

![Plasmasphere_demo.py](magnetovis/Test/Figures/Plasmasphere_demo-1.png)

### Demo #2

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.Earth(coord_sys='SM')

plasmasphere = mvs.Plasmasphere()

# Add slice
import paraview.simple as pvs
pvs.Hide(plasmasphere)

slice1 = pvs.Slice(registrationName=' y=0 slice', Input=plasmasphere)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.SliceOffsetValues = [0.0]
slice1.SliceType.Normal = [0.0, 1.0, 0.0]

renderView1 = pvs.GetActiveViewOrCreate('RenderView')
slice1Display = pvs.Show(slice1, renderView1, 'GeometryRepresentation')

# Show slice color bar
slice1Display.SetScalarBarVisibility(renderView1, True)
pvs.Hide3DWidgets(proxy=slice1.SliceType)

# Add countour
contour1 = pvs.Contour(registrationName=' 3.0 Contour', Input=slice1)
contour1.ContourBy = ['POINTS', 'H+ log density (cm^-3)']
contour1.Isosurfaces = [3.0]
contour1.PointMergeMethod = 'Uniform Binning'
pvs.Show(contour1)

mvs.SetCamera(viewType="+Y")
```

![Plasmasphere_demo.py](magnetovis/Test/Figures/Plasmasphere_demo-2.png)

## Satellite.py
Source file: [Satellite.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Satellite.py) | Demo file: [Satellite_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Satellite_demo.py)

### Demo 1

```python
import magnetovis as mvs
mvs.Satellite()
```

![Satellite_demo.py](magnetovis/Test/Figures/Satellite_demo-1.png)

### Demo #2

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
skwargs = {
	"start": "2010-01-04T00:00:00",
	"stop": "2010-01-05T00:00:00",
	"coord_sys": "GSM"
}
themisa = mvs.Satellite(id='themisa', **skwargs)
themisb = mvs.Satellite(id='themisb', **skwargs)

dkwargs = {
            "label":
                {
                    "source": {"Text": ""},
                    "display": {
                        "FontSize": 24,
                        "Color": [0.5, 0.5, 0.5]
                    }
                }
            }

dkwargs['label']['source']['Text'] = 'THEMIS A'
dkwargs['label']['display']['Color'] = [0, 0, 1]
mvs.SetDisplayProperties(source=themisa, **dkwargs)

dkwargs['label']['source']['Text'] = 'THEMIS B'
dkwargs['label']['display']['Color'] = [1, 0, 0]
mvs.SetDisplayProperties(source=themisb, **dkwargs)

mvs.SetCamera(Azimuth=45, Elevation=45)

mvs.SetTitle(mvs.util.trim_iso(skwargs["start"]) \
			+ " - " + mvs.util.trim_iso(skwargs["stop"]) \
			+ " " + skwargs["coord_sys"], registrationName="Title")
```

![Satellite_demo.py](magnetovis/Test/Figures/Satellite_demo-2.png)

## T89c.py
Source file: [T89c.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/T89c.py) | Demo file: [T89c_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/T89c_demo.py)

### Demo 1

```python
import magnetovis as mvs
t89c = mvs.T89c(dimensions=[20, 20, 20])
mvs.SetTitle("Default")
```

![T89c_demo.py](magnetovis/Test/Figures/T89c_demo-1.png)

### Demo 2

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
t89c = mvs.T89c(dimensions=[20, 20, 20])

import paraview.simple as pvs
pvs.Hide(t89c)
streamTracer1 = pvs.StreamTracer(registrationName='StreamTracer1', Input=t89c, SeedType='Line')
streamTracer1.Vectors = ['POINTS', 'B']
streamTracer1.MaximumStreamlineLength = 20.0

# init the 'Line' selected for 'SeedType'
streamTracer1.SeedType.Point1 = [-10.0, 0.0, 0.0]
streamTracer1.SeedType.Point2 = [-2.0, 0.0, 0.0]
streamTracer1.SeedType.Resolution = 10

# set active source
pvs.SetActiveSource(streamTracer1)

# show data in view
streamTracer1Display = pvs.Show(streamTracer1)
```

![T89c_demo.py](magnetovis/Test/Figures/T89c_demo-2.png)

## T95CurrentSheet.py
Source file: [T95CurrentSheet.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/T95CurrentSheet.py) | Demo file: [T95CurrentSheet_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/T95CurrentSheet_demo.py)

### Demo 1

```python
import magnetovis as mvs
s = mvs.T95CurrentSheet()
```

![T95CurrentSheet_demo.py](magnetovis/Test/Figures/T95CurrentSheet_demo-1.png)
