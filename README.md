<!-- TOC -->
[1 About](#1-about)<br/>
[2 Install](#2-install)<br/>
[3 Getting started](#3-getting-started)<br/>
[4 Approach](#4-approach)<br/>
[5 Notes](#5-notes)<br/>
[6 Demos](#6-demos)
<!-- \TOC -->
# 1 About

`magnetovis` is a set of Python scripts that display magnetosphere-related objects, regions, and data in [ParaView](https://www.paraview.org/) that was initially developed under NASA Grant Number 80NSSC21K0305.

The objects created by `magnetovis` scripts are displayed in the `ParaView` GUI where the can be inspected, manipulated, and modified.

See the demo files in https://github.com/rweigel/magnetovis for example usage.

# 2 Install

An existing installation of [ParaView 5.9+](https://www.paraview.org/download/) is required. 

ParaView includes a Python 3 version. Because `magnetovis` requires packages that are not distributed with ParaView, you should execute `magnetovis` in a enviroment with the same Python version number as that used by ParaView.

Installation has been only tested in OS-X and Linux. 

Please provide feedback by submitting an [issue](https://github.com/rweigel/magnetovis/issues).

```
git clone https://github.com/rweigel/magnetovis
cd magnetovis
pip install --editable .
magnetovis --script=magnetovis_demo.py
```

# 3 Getting started

`magnetovis` has three distinct parts

1. A collection of helper functions for creating objects ("Sources" in Paraview/VTK terminology). The functions are in the `vtk` folder.
2. A set of default display options that are applied automatically to objects. In Paraview, when a source is added to the pipeline, no display options are set and the user must select the options in the GUI or write a script that sets the options. `magnetovis` objects have default display options that are applied when the object is added to the pipeline.
3. A collection of Programmable Sources and Plugins that create and filter Heliophyiscs-related objects.

# 4 Approach

The objects (e.g, Earth, Plasmapause, etc.) in `magnetovis` are created using `ParaView` [`Programmable Sources`](https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html). Programmable Sources are short Python scripts that create [`VTK`](https://vtk.org) objects.

When a a `magnetovis` Programmable Source is created in a Macro or one the Python command line in Paraview, the user can see and modify the script that created the object. Each Programmable Source in the [Sources](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources) directory has a corresponding `Plugin` that is automatically created from the Programmable Source file at startup.

The objects were developed using the ParaView GUI and the [Programmable Source editor](https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#recipes-for-programmable-source). The final scripts are then placed in a file in the [Sources](https://github.com/rweigel/magnetovis/tree/main/magnetovis/Sources) directory. Each file in this directory is associated with a object and the code that is used to genereate the object is in a function called `Script()`.

%To demonstrate the general procedure by which magnetovis object are created, we will use the [Helix](https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#helix-source) example from the ParaView user's guide.

%Magnetovis objects are listed in the ParaView `Sources` drop-down menu. 

%Selection of these sources creates an unstyled object that can be modified using the `Display (GeometryRepresentation)` menu in the `Properties` window.

%In `magnetovis`, each Programmable Source object has an associated script that adds attributes to the display object such as colors and annotations. To apply these attributes, execute a `Macro` associated with the Programmable Source.

# 5 Notes

See `docs/Satellite_Region_Notes.md` for documentation on how magnetosphere regions were computed and a comparison with regions reported by SSCWeb.

# 6 Demos

The demos can be run using

```
git clone https://github.com/rweigel/magnetovis
cd magnetovis/Test
magnetovis FILENAME
```

where `FILENAME` is the name of a demo file listed below, e.g., `Axis_demo.py`.

<!-- Demos Start -->

## Axis_demo.py
### Demo #1

```
import magnetovis as mvs
mvs.Axis()
#mvs.PrintSourceDefaults('Axis')
mvs.SetTitle("Axis with default options")
#mvs.PrintDisplayDefaults('Axis', all=True)
```

![Axis_demo.py](magnetovis/Test/Figures/Axis_demo-1.png)

### Demo #2

```
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

