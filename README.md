# About

`magnetovis` is a set of Python scripts that display magnetosphere-related objects, regions, and data in [ParaView](https://www.paraview.org/) that was initially developed under NASA Grant Number 80NSSC21K0305.

The objects created by `magnetovis` scripts are displayed in the `ParaView` GUI where the can be inspected, manipulated, and modified.

See the [demo files](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Demos) for example usage.

# Install

An existing installation of [ParaView 5.9+](https://www.paraview.org/download/) is required. 

ParaView includes a Python 3 version. Because `magnetovis` requires packages that are not distributed with ParaView, you should execute `magnetovis` in a enviroment with the same Python version number as that used by ParaView.

Installation has been only tested in OS-X and Linux. 

Please provide feedback by submitting an [issue](https://github.com/rweigel/magnetovis/issues).

```
git clone https://github.com/rweigel/magnetovis
cd magnetovis
pip install --editable .
magnetovis magnetovis_demo.py
```

# Getting started

`magnetovis` has three distinct parts

1. A collection of Programmable Sources, Filters and Plugins that create and filter Heliophyiscs-related objects. See the [demos](#demos) for a full list and example usage. Most Magnetovis programmable sources (and their associated Plugins) have a set of default display options that are applied automatically when they are created. In Paraview, when a source is added to the pipeline, no display options are set and the user must select the options in the GUI or write a script that sets the options. `magnetovis` objects have default display options that are applied when the object is added to the pipeline.
2. A collection of helper functions for reducing the amount of code needed to modify view properties, the camera, and color bars. See the files starting with "Set" in [the `paraview` directory](https://github.com/rweigel/magnetovis/tree/main/magnetovis/paraview).
3. A collection of helper functions for reducing the amount of code needed for creating programmable sources and filters. The functions are in the `vtk` folder.

# Approach

The objects (e.g, Earth, Plasmapause, etc.) in `magnetovis` are created using `ParaView` [`Programmable Sources`](https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html). Programmable Sources are short Python scripts that create [`VTK`](https://vtk.org) objects.

When a a `magnetovis` Programmable Source is created in a Macro or one the Python command line in Paraview, the user can see and modify the script that created the object. Each Programmable Source in the [Sources](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources) directory has a corresponding `Plugin` that is automatically created from the Programmable Source file at startup.

The objects were developed using the ParaView GUI and the [Programmable Source editor](https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#recipes-for-programmable-source). The final scripts are then placed in a file in the [Sources](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources) directory. Each file in this directory is associated with a object and the code that is used to genereate the object is in a function called `Script()`.

%To demonstrate the general procedure by which magnetovis object are created, we will use the [Helix](https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#helix-source) example from the ParaView user's guide.

%Magnetovis objects are listed in the ParaView `Sources` drop-down menu. 

%Selection of these sources creates an unstyled object that can be modified using the `Display (GeometryRepresentation)` menu in the `Properties` window.

%In `magnetovis`, each Programmable Source object has an associated script that adds attributes to the display object such as colors and annotations. To apply these attributes, execute a `Macro` associated with the Programmable Source.

# Development Notes

## Terminology

**ParaView**

* Proxy
* Plugin
* Source (Sometime used for filter, e.g, GetActiveSource() can return a filter)
* Filter
* Display/Representation
* View - types include _Render View_, ...
* Pipeline
* Transfer function/lookup table
* Camera

**Magnetovis**

* Presentation


## Testing and Developing Scripts

ParaView has a script and macro editor. However, the editor is basic and limited. To test scripts created using a different editor, enter the following on ParaView's Python Shell command line.

```python
import magnetovis; magnetovis.ClearPipeline() # Optional
exec(open("/absolute/path/to/script.py").read())
```

## Testing and Developing Programmable Sources

On start-up, `magnetovis` creates Programmable Sources based on the files in `magnetovis/Sources`. To create and test your own `magnetovis` programmable source, start with the following template

`/tmp/MySource.py`

```python
def MySource(**kwargs):
  import magnetovis
  return magnetovis.CreateProgrammableSource('/tmp/MySource.py')

def OutputDataSetType():

  # What is set in the drop-down menu for Output Data Set Type for
  # Programmable Source.
  return "vtkPolyData"

def Script(point1=0.0, point2=1.0, resolution=10):

  # What entered into the Script text area for a Programmable Source

  vtkLineSource = vtk.vtkLineSource()
  vtkLineSource.SetPoint1(point1)
  vtkLineSource.SetPoint2(point2)
  vtkLineSource.SetResolution(resolution)
  vtkLineSource.Update()

  output.ShallowCopy(vtkLineSource.GetOutputDataObject(0))

```

To use the source, enter the following in a script or on the Python Shell command line

```python
exec(open("/tmp/MySource.py").read())
source = MySource()
```

After entering the above command, you should see `MySource` in the ParaView pipeline and the content of `Script` will be the in the script text area under the `Properties` tab. Modifications to your source can be tested by either executing the above two commands in the ParaView Python Shell or by modifying the content of `Script` in the ParaView GUI.

# Notes

See `docs/Satellite_Region_Notes.md` for documentation on how magnetosphere regions were computed and a comparison with regions reported by SSCWeb.

# Demos

The demos can be run using

```
git clone https://github.com/rweigel/magnetovis
magnetovis magnetovis/Sources/FILENAME.py
```

where `FILENAME.py` is the name of a demo file listed below, e.g., `Axis_demo.py`.

<!-- Demos Start -->
# About

`magnetovis` is a set of Python scripts that display magnetosphere-related objects, regions, and data in [ParaView](https://www.paraview.org/) that was initially developed under NASA Grant Number 80NSSC21K0305.

The objects created by `magnetovis` scripts are displayed in the `ParaView` GUI where the can be inspected, manipulated, and modified.

See the [demo files](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Demos) for example usage.

# Install

An existing installation of [ParaView 5.9+](https://www.paraview.org/download/) is required. 

ParaView includes a Python 3 version. Because `magnetovis` requires packages that are not distributed with ParaView, you should execute `magnetovis` in a enviroment with the same Python version number as that used by ParaView.

Installation has been only tested in OS-X and Linux. 

Please provide feedback by submitting an [issue](https://github.com/rweigel/magnetovis/issues).

```
git clone https://github.com/rweigel/magnetovis
cd magnetovis
pip install --editable .
magnetovis magnetovis_demo.py
```

# Getting started

`magnetovis` has three distinct parts

1. A collection of Programmable Sources, Filters and Plugins that create and filter Heliophyiscs-related objects. See the [demos](#demos) for a full list and example usage. Most Magnetovis programmable sources (and their associated Plugins) have a set of default display options that are applied automatically when they are created. In Paraview, when a source is added to the pipeline, no display options are set and the user must select the options in the GUI or write a script that sets the options. `magnetovis` objects have default display options that are applied when the object is added to the pipeline.
2. A collection of helper functions for reducing the amount of code needed to modify view properties, the camera, and color bars. See the files starting with "Set" in [the `paraview` directory](https://github.com/rweigel/magnetovis/tree/main/magnetovis/paraview).
3. A collection of helper functions for reducing the amount of code needed for creating programmable sources and filters. The functions are in the `vtk` folder.

# Approach

The objects (e.g, Earth, Plasmapause, etc.) in `magnetovis` are created using `ParaView` [`Programmable Sources`](https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html). Programmable Sources are short Python scripts that create [`VTK`](https://vtk.org) objects.

When a a `magnetovis` Programmable Source is created in a Macro or one the Python command line in Paraview, the user can see and modify the script that created the object. Each Programmable Source in the [Sources](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources) directory has a corresponding `Plugin` that is automatically created from the Programmable Source file at startup.

The objects were developed using the ParaView GUI and the [Programmable Source editor](https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#recipes-for-programmable-source). The final scripts are then placed in a file in the [Sources](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources) directory. Each file in this directory is associated with a object and the code that is used to genereate the object is in a function called `Script()`.

%To demonstrate the general procedure by which magnetovis object are created, we will use the [Helix](https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#helix-source) example from the ParaView user's guide.

%Magnetovis objects are listed in the ParaView `Sources` drop-down menu. 

%Selection of these sources creates an unstyled object that can be modified using the `Display (GeometryRepresentation)` menu in the `Properties` window.

%In `magnetovis`, each Programmable Source object has an associated script that adds attributes to the display object such as colors and annotations. To apply these attributes, execute a `Macro` associated with the Programmable Source.

# Development Notes

## Terminology

**ParaView**

* Proxy
* Plugin
* Source (Sometime used for filter, e.g, GetActiveSource() can return a filter)
* Filter
* Display/Representation
* View - types include _Render View_, ...
* Pipeline
* Transfer function/lookup table
* Camera

**Magnetovis**

* Presentation


## Testing and Developing Scripts

ParaView has a script and macro editor. However, the editor is basic and limited. To test scripts created using a different editor, enter the following on ParaView's Python Shell command line.

```python
import magnetovis; magnetovis.ClearPipeline() # Optional
exec(open("/absolute/path/to/script.py").read())
```

## Testing and Developing Programmable Sources

On start-up, `magnetovis` creates Programmable Sources based on the files in `magnetovis/Sources`. To create and test your own `magnetovis` programmable source, start with the following template

`/tmp/MySource.py`

```python
def MySource(**kwargs):
  import magnetovis
  return magnetovis.CreateProgrammableSource('/tmp/MySource.py')

def OutputDataSetType():

  # What is set in the drop-down menu for Output Data Set Type for
  # Programmable Source.
  return "vtkPolyData"

def Script(point1=0.0, point2=1.0, resolution=10):

  # What entered into the Script text area for a Programmable Source

  vtkLineSource = vtk.vtkLineSource()
  vtkLineSource.SetPoint1(point1)
  vtkLineSource.SetPoint2(point2)
  vtkLineSource.SetResolution(resolution)
  vtkLineSource.Update()

  output.ShallowCopy(vtkLineSource.GetOutputDataObject(0))

```

To use the source, enter the following in a script or on the Python Shell command line

```python
exec(open("/tmp/MySource.py").read())
source = MySource()
```

After entering the above command, you should see `MySource` in the ParaView pipeline and the content of `Script` will be the in the script text area under the `Properties` tab. Modifications to your source can be tested by either executing the above two commands in the ParaView Python Shell or by modifying the content of `Script` in the ParaView GUI.

# Notes

See `docs/Satellite_Region_Notes.md` for documentation on how magnetosphere regions were computed and a comparison with regions reported by SSCWeb.

# Demos

The demos can be run using

```
git clone https://github.com/rweigel/magnetovis
magnetovis magnetovis/Sources/FILENAME.py
```

where `FILENAME.py` is the name of a demo file listed below, e.g., `Axis_demo.py`.

<!-- Demos Start -->
## NEZ

Source file: [NEZ.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Demos/NEZ.py) | Demo file: [NEZ_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Demos/NEZ_demo.py)

### Demo 1

```python
import paraview.simple as pvs
import magnetovis as mvs
import numpy as np

def nez(time, pos, csys):
  """Unit vectors in geographic north, east, and zenith dirs"""

  from hxform import hxform as hx

  # Geographic z axis in csys
  Z = hx.transform(np.array([0, 0, 1]), time, 'GEO', csys, lib='cxform')

  # zenith direction ("up")
  z_geo = pos/np.linalg.norm(pos)

  e_geo = np.cross(Z, z_geo)
  e_geo = e_geo/np.linalg.norm(e_geo)

  n_geo = np.cross(z_geo, e_geo)
  n_geo = n_geo/np.linalg.norm(n_geo)

  print(f"Unit vectors for Geographic N, E, and Z at {pos} in {csys} at {time}:")
  print("North: {}".format(n_geo))
  print("East:  {}".format(e_geo))
  print("Z:     {}".format(z_geo))

  return n_geo, e_geo, z_geo

def showaxis(pos, n_geo, e_geo, z_geo):

  def showlabel(dir,base,top):

    Label = pvs.Text(registrationName=dir+'_GEO Label', Text=dir+"$_{GEO}$")
    text1Display = pvs.Show(Label, pvs.GetActiveViewOrCreate('RenderView'), 'TextSourceRepresentation',
      TextPropMode='Flagpole Actor',BasePosition=base,TopPosition=top)

  north = pvs.Line(registrationName="N", Point1=pos, Point2=pos+n_geo)
  north_tube = pvs.Tube(north, Radius=0.02)
  mvs.SetColor('blue')
  pvs.Show(north_tube)
  showlabel('N',pos+n_geo,pos+1.05*n_geo)

  east = pvs.Line(registrationName="E", Point1=pos, Point2=pos+e_geo)
  east_tube = pvs.Tube(east, Radius=0.02)
  mvs.SetColor('green')
  pvs.Show(east_tube)
  showlabel('E',pos+e_geo,pos+e_geo+0.05*n_geo)

  up = pvs.Line(registrationName="Z", Point1=pos, Point2=pos+z_geo)
  up_tube = pvs.Tube(up, Radius=0.02)
  mvs.SetColor('red')
  pvs.Show(up_tube)
  showlabel('Z',pos+z_geo,pos+z_geo+0.05*n_geo)

  s = pvs.Sphere(Radius=0.05, Center=pos)
  pvs.Show(s)
```

![NEZ_demo.py](magnetovis/Test/Demos/NEZ_demo-1.png)

### Demo 1

```python
time = "2010-01-01T06:00:00"
pos = (1, 0, 0)
csys = "GEO"
n_geo, e_geo, z_geo = nez(time, pos, csys)

showaxis(pos, n_geo, e_geo, z_geo)
mvs.SetOrientationAxisLabel(Text="GEO")
mvs.Earth(time=time, coord_sys=csys)
mvs.LatLong(coord_sys=csys, coord_sys_view=csys)
```

![NEZ_demo.py](magnetovis/Test/Demos/NEZ_demo-2.png)

## Arc

Source file: [Arc.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Arc.py) | Demo file: [Arc_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Arc_demo.py)

### Demo 1

```python
import paraview.simple as pvs
import magnetovis as mvs
arc = mvs.Arc()
tube = pvs.Tube(arc)
pvs.Show(tube)
```

![Arc_demo.py](magnetovis/Test/Sources/Arc_demo-1.png)

### Demo 2

```python
import paraview.simple as pvs
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.Earth(coord_sys="GEO", coord_sys_view="GEO")
arc = mvs.Arc(Radisus=1.01, Direction=[0, 1, 0], StartPhi=-90, EndPhi=90)

color = [1.0, 0.0, 0.0]
tube = pvs.Tube(arc)
pvs.Show(tube, DiffuseColor=color)

text = pvs.Text(Text='Prime Meridian')
pvs.Show(text, TextPropMode='Billboard 3D Text', BillboardPosition=[0, 0, 1.05], Color=[1.0, 0.0, 0.0])
```

![Arc_demo.py](magnetovis/Test/Sources/Arc_demo-2.png)

## Axis

Source file: [Axis.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Axis.py) | Demo file: [Axis_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Axis_demo.py)

### Demo 1

```python
import magnetovis as mvs
mvs.Axis()
#mvs.PrintSourceDefaults('Axis')
mvs.SetTitle("Axis with default options")
#mvs.PrintPresentationDefaults('Axis', all=True)
```

![Axis_demo.py](magnetovis/Test/Sources/Axis_demo-1.png)

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
mvs.SetPresentationProperties(source=yAxis, **dkwargs)
mvs.SetTitle("Three Axes")

skwargs['direction'] = "Z"
skwargs['extent'] = [-40, 40]
zAxis = mvs.Axis(**skwargs)
```

![Axis_demo.py](magnetovis/Test/Sources/Axis_demo-2.png)

## BATSRUS

Source file: [BATSRUS.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/BATSRUS.py) | Demo file: [BATSRUS_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/BATSRUS_demo.py)

### Demo 1

```python
import magnetovis as mvs
# See BATSRUS_prep.py for downloading this file.
vtkfile = "/tmp/3d__var_2_e20190902-041000-000.vtk"

batsrus = mvs.BATSRUS(file=vtkfile)
mvs.SetTitle("Default")
```

![BATSRUS_demo.py](magnetovis/Test/Sources/BATSRUS_demo-1.png)

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

mvs.SetColoring(source=sliceY, display=sliceYDisplay, **ckwargs)

sliceZDisplay.SetScalarBarVisibility(view, False)
```

![BATSRUS_demo.py](magnetovis/Test/Sources/BATSRUS_demo-2.png)

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

![BATSRUS_demo.py](magnetovis/Test/Sources/BATSRUS_demo-3.png)

### Demo 4

```python
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
```

![BATSRUS_demo.py](magnetovis/Test/Sources/BATSRUS_demo-4.png)

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

![BATSRUS_demo.py](magnetovis/Test/Sources/BATSRUS_demo-5.png)

## Bowshock

Source file: [Bowshock.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Bowshock.py) | Demo file: [Bowshock_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Bowshock_demo.py)

### Demo 1

```python
import magnetovis as mvs
bowshock = mvs.Bowshock()
```

![Bowshock_demo.py](magnetovis/Test/Sources/Bowshock_demo-1.png)

## Circle

Source file: [Circle.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Circle.py) | Demo file: [Circle_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Circle_demo.py)

### Demo 1

```python
import magnetovis as mvs
mvs.Circle()
```

![Circle_demo.py](magnetovis/Test/Sources/Circle_demo-1.png)

## Curve

Source file: [Curve.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Curve.py) | Demo file: [Curve_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Curve_demo.py)

### Demo 1

```python
import magnetovis as mvs
mvs.Curve()
mvs.SetCamera(viewType="isometric", Zoom=10)

#mvs.PrintSourceDefaults('Curve')
mvs.SetTitle("Curve with default options")
#mvs.PrintPresentationDefaults('Curve', all=True)

if False:
```

![Curve_demo.py](magnetovis/Test/Sources/Curve_demo-1.png)

## DifferentialDisk

Source file: [DifferentialDisk.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/DifferentialDisk.py) | Demo file: [DifferentialDisk_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/DifferentialDisk_demo.py)

### Demo 1

```python
import magnetovis as mvs
mvs.DifferentialDisk()
mvs.SetColoring(colorTransferFunction={"separate": True})
mvs.SetTitle("Differential Disk with Default Options")
```

![DifferentialDisk_demo.py](magnetovis/Test/Sources/DifferentialDisk_demo-1.png)

### Demo 2

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.DifferentialDisk(Nr=1)
mvs.SetColoring(colorTransferFunction={"separate": True})
mvs.SetTitle("Nr=1")
```

![DifferentialDisk_demo.py](magnetovis/Test/Sources/DifferentialDisk_demo-2.png)

### Demo 3

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.DifferentialDisk(ro=1, rf=2, Nφ=10, φo=0, φf=360)
mvs.SetColoring(colorTransferFunction={"separate": True})
mvs.SetTitle("ro=1, rf=2, Nφ=10, φo=0, φf=360")
```

![DifferentialDisk_demo.py](magnetovis/Test/Sources/DifferentialDisk_demo-3.png)

### Demo 4

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.DifferentialDisk(ro=1, rf=2, Nφ=10, φo=0, φf=80, closed=False)
mvs.SetColoring(colorTransferFunction={"separate": True})
mvs.SetTitle("$ro=1, rf=2, Nφ=10, φo=0, φf=80, closed=False$")
```

![DifferentialDisk_demo.py](magnetovis/Test/Sources/DifferentialDisk_demo-4.png)

## Dipole

Source file: [Dipole.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Dipole.py) | Demo file: [Dipole_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Dipole_demo.py)

### Demo 1

```python
import magnetovis as mvs
mvs.Dipole()
mvs.SetTitle("Dipole with Default Options")
```

![Dipole_demo.py](magnetovis/Test/Sources/Dipole_demo-1.png)

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
print("First 3 x, y, z values for first trace:")
print(trace0[0:3,:])

pvs.Hide3DWidgets(proxy=slice1.SliceType)
```

![Dipole_demo.py](magnetovis/Test/Sources/Dipole_demo-2.png)

## Earth

Source file: [Earth.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Earth.py) | Demo file: [Earth_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Earth_demo.py)

### Demo 1

```python
import magnetovis as mvs
mvs.Earth()
mvs.SetTitle("  Earth with Default Options")
mvs.SetOrientationAxisLabel('GSM')
```

![Earth_demo.py](magnetovis/Test/Sources/Earth_demo-1.png)

### Demo 2

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.Earth(style="daynight")
mvs.SetTitle('  Earth with style="daynight"')
mvs.SetOrientationAxisLabel('GSM')
```

![Earth_demo.py](magnetovis/Test/Sources/Earth_demo-2.png)

### Demo 3

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.Earth()
mvs.SetTitle("  Earth with Axes")
mvs.SetOrientationAxisLabel('GSM')

xAxis = mvs.Axis(direction="X", extent=[-3, 3])
mvs.SetPresentationProperties(source=xAxis, 
		**{"label": {"source": {"Text": "$X_{GSM}$"}}})

yAxis = mvs.Axis(direction="Y", extent=[-3, 3])
mvs.SetPresentationProperties(source=yAxis, 
		**{"label": {"source": {"Text": "$Y_{GSM}$"}}})

zAxis = mvs.Axis(direction="Z", extent=[-3, 3])
mvs.SetPresentationProperties(source=zAxis, 
		**{"label": {"source": {"Text": "$Z_{GSM}$"}}})

dkwargs = {
			"display": {
				"AmbientColor": [0.5,0.5,0.5],
				"DiffuseColor": [0.5,0.5,0.5]
			},
			"label": {
				"source": {"Text": "$Z_{GEO}$"},
				"display": {"Color": [0.5,0.5,0.5]}
			}
		}
zAxis2 = mvs.Axis(direction="Z", extent=[-3, 3], coord_sys="GEO")
mvs.SetPresentationProperties(source=zAxis2, **dkwargs)
```

![Earth_demo.py](magnetovis/Test/Sources/Earth_demo-3.png)

## GridData

Source file: [GridData.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/GridData.py) | Demo file: [GridData_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/GridData_demo.py)

### Demo 1

```python
import magnetovis as mvs
mvs.GridData(OutputDataSetType="vtkImageData")
mvs.SetTitle("Dataset Type = vtkImageData")
```

![GridData_demo.py](magnetovis/Test/Sources/GridData_demo-1.png)

### Demo 2

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.GridData(OutputDataSetType="vtkRectilinearGrid")
mvs.SetTitle("Dataset Type = vtkRectilinearGrid")
```

![GridData_demo.py](magnetovis/Test/Sources/GridData_demo-2.png)

### Demo 3

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.GridData(OutputDataSetType="vtkStructuredGrid")
mvs.SetTitle("Dataset Type = vtkStructuredGrid")
```

![GridData_demo.py](magnetovis/Test/Sources/GridData_demo-3.png)

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
                            'ScalarBarLength': 0.8,
                        },
            'colorTransferFunction': {
                                        'UseLogScale': 1,
                                        'AutomaticRescaleRangeMode': 1,
                                        'AutomaticRescaleRangeMode': "Grow and update on 'Apply'",
                                        'NumberOfTableValues': 16
                                    }
        }
}

mvs.SetPresentationProperties(**dkwargs)
mvs.SetCamera(Azimuth=225.0, Elevation=30)
mvs.SetTitle()
```

![GridData_demo.py](magnetovis/Test/Sources/GridData_demo-4.png)

## LatLong

Source file: [LatLong.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/LatLong.py) | Demo file: [LatLong_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/LatLong_demo.py)

### Demo 1

```python
import magnetovis as mvs
mvs.SetOrientationAxisLabel()
mvs.Earth()
mvs.LatLong(coord_sys="GEO")
mvs.SetTitle()
```

![LatLong_demo.py](magnetovis/Test/Sources/LatLong_demo-1.png)

### Demo 2

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.SetOrientationAxisLabel(Text="GEO")
mvs.Earth(coord_sys="GEO", coord_sys_view="GEO")
mvs.LatLong(coord_sys="GEO", coord_sys_view="GEO")
mvs.SetTitle()
```

![LatLong_demo.py](magnetovis/Test/Sources/LatLong_demo-2.png)

### Demo 3

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.SetOrientationAxisLabel()
mvs.Earth()
mvs.LatLong(coord_sys="GEO")
mvs.SetTitle()
mvs.SetOrientationAxisLabel()
zAxis = mvs.Axis(direction="Z", coord_sys="GEO", extent=[-3, 3])
mvs.SetPresentationProperties(source=zAxis, 
    **{"label": {"source": {"Text": "$Z_{GEO}$"}}})
```

![LatLong_demo.py](magnetovis/Test/Sources/LatLong_demo-3.png)

### Demo 4

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.SetOrientationAxisLabel()
mvs.Earth()
mvs.LatLong(coord_sys="MAG")
mvs.SetTitle()
mvs.SetOrientationAxisLabel()
zAxis = mvs.Axis(direction="Z", coord_sys="MAG", extent=[-3, 3])
mvs.SetPresentationProperties(source=zAxis, 
    **{"label": {"source": {"Text": "$Z_{MAG}$"}}})
```

![LatLong_demo.py](magnetovis/Test/Sources/LatLong_demo-4.png)

## Lines

Source file: [Lines.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Lines.py) | Demo file: [Lines_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Lines_demo.py)

### Demo 1

```python
import magnetovis as mvs
mvs.Lines()
#mvs.PrintSourceDefaults('Lines')
mvs.SetTitle("Line with default options")
#mvs.PrintPresentationDefaults('Lines', all=True)
```

![Lines_demo.py](magnetovis/Test/Sources/Lines_demo-1.png)

### Demo #2

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()

kwargs = {
            "time": "2001-01-01",
            "coord_sys": "GSM",
            "Nlines": 3,
            "closed": True,
            "point_function": "circle(radius=1.0, center=(0.0, 0.0, 0.0))"
        }

mvs.Lines(**kwargs)
```

![Lines_demo.py](magnetovis/Test/Sources/Lines_demo-2.png)

## Plasmasphere

Source file: [Plasmasphere.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Plasmasphere.py) | Demo file: [Plasmasphere_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Plasmasphere_demo.py)

### Demo 1

```python
import magnetovis as mvs
plasmasphere = mvs.Plasmasphere()
mvs.SetTitle()
mvs.SetOrientationAxisLabel('GSM')
```

![Plasmasphere_demo.py](magnetovis/Test/Sources/Plasmasphere_demo-1.png)

### Demo #2

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
plasmasphere = mvs.Plasmasphere(coord_sys='SM', coord_sys_view='SM')
mvs.SetTitle()
mvs.Earth(coord_sys='SM', coord_sys_view='SM')
mvs.SetOrientationAxisLabel('SM')

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
contour1 = pvs.Contour(registrationName='1.5 Contour', Input=slice1)
contour1.ContourBy = ['POINTS', 'H+ log density [cm^-3]']
contour1.Isosurfaces = [1.5]
contour1.PointMergeMethod = 'Uniform Binning'
pvs.Show(contour1)

color = [1.0, 0.0, 0.0]
tube = pvs.Tube(contour1)
pvs.Show(tube)
mvs.SetColor(color)

text = pvs.Text(Text='log(n) = 1.5')
pvs.Show(text, TextPropMode='Billboard 3D Text', BillboardPosition=[-5, 0.1, 0.0], Color=color)

mvs.SetCamera(viewType="-Y")
```

![Plasmasphere_demo.py](magnetovis/Test/Sources/Plasmasphere_demo-2.png)

### Demo #3

```python
import magnetovis as mvs
import paraview.simple as pvs
mvs.CreateViewAndLayout()
plasmasphere = mvs.Plasmasphere()
pvs.Hide(plasmasphere)
mvs.SetTitle("log$(n)=1.5$", source=plasmasphere)
mvs.Earth()
mvs.SetOrientationAxisLabel('GSM')

# Add slice
import paraview.simple as pvs

# Add countour
contour1 = pvs.Contour(registrationName='1.5 Contour', Input=plasmasphere)
contour1.ContourBy = ['POINTS', 'H+ log density [cm^-3]']
contour1.Isosurfaces = [1.5]
contour1.PointMergeMethod = 'Uniform Binning'
pvs.Hide3DWidgets(proxy=slice1.SliceType)

clip1 = pvs.Clip(registrationName='y=0 slice', Input=contour1)
clip1.ClipType = 'Plane'
clip1.Value = [0.0]
clip1.ClipType.Origin = [0.0, 1.0, 0.0]
clip1.ClipType.Normal = [0.0, 1.0, 0.0]
pvs.Hide3DWidgets(proxy=clip1.ClipType)
pvs.Show(clip1)
mvs.SetCamera(viewType="isometric")
```

![Plasmasphere_demo.py](magnetovis/Test/Sources/Plasmasphere_demo-3.png)

## Satellite

Source file: [Satellite.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Satellite.py) | Demo file: [Satellite_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/Satellite_demo.py)

### Demo 1

```python
import magnetovis as mvs
mvs.Satellite()
```

![Satellite_demo.py](magnetovis/Test/Sources/Satellite_demo-1.png)

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
mvs.SetPresentationProperties(source=themisa, **dkwargs)

dkwargs['label']['source']['Text'] = 'THEMIS B'
dkwargs['label']['display']['Color'] = [1, 0, 0]
mvs.SetPresentationProperties(source=themisb, **dkwargs)

mvs.SetCamera(Azimuth=45, Elevation=45)

mvs.SetTitle(mvs.util.trim_iso(skwargs["start"]) \
			+ " - " + mvs.util.trim_iso(skwargs["stop"]) \
			+ " " + skwargs["coord_sys"], registrationName="Title")
```

![Satellite_demo.py](magnetovis/Test/Sources/Satellite_demo-2.png)

## T89c

Source file: [T89c.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/T89c.py) | Demo file: [T89c_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/T89c_demo.py)

### Demo 1

```python
import magnetovis as mvs
t89c = mvs.T89c(dimensions=[20, 20, 20])
mvs.SetTitle()
```

![T89c_demo.py](magnetovis/Test/Sources/T89c_demo-1.png)

### Demo 2

```python
import magnetovis as mvs
mvs.CreateViewAndLayout()
t89c = mvs.T89c(dimensions=[20, 20, 20])
mvs.SetTitle()

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

![T89c_demo.py](magnetovis/Test/Sources/T89c_demo-2.png)

## T95CurrentSheet

Source file: [T95CurrentSheet.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/T95CurrentSheet.py) | Demo file: [T95CurrentSheet_demo.py](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources/T95CurrentSheet_demo.py)

### Demo 1

```python
import magnetovis as mvs
s = mvs.T95CurrentSheet()
```

![T95CurrentSheet_demo.py](magnetovis/Test/Sources/T95CurrentSheet_demo-1.png)

