# About

`magnetovis` is a set of Python scripts that display magnetosphere-related objects, regions, and data in [ParaView](https://www.paraview.org/) that was initially developed under NASA Grant Number 80NSSC21K0305.

The objects created by `magnetovis` scripts are displayed in the `ParaView` GUI where the can be inspected, manipulated, and modified.

See the demo files in https://github.com/rweigel/magnetovis for example usage.

# Install

An existing installation of [ParaView 5.9+](https://www.paraview.org/download/) is required. 

ParaView includes a Python 3 version. Because `magnetovis` requires packages that are not distributed with ParaView, you should execute `magnetovis` in a enviroment with the same Python version number as that used by ParaView.

Installation has been only tested in OS-X and Linux. 

Please provide feedback by submitting an [issue](https://github.com/rweigel/magnetovis/issues).

```
git clone https://github.com/rweigel/magnetovis
cd magnetovis
pip install numpy
pip install --editable .
magnetovis --script=magnetovis_demo.py
```

# Getting started


# Approach

The objects (e.g, Earth, Plasmapause, etc.) in `magnetovis` are created using `ParaView` [`Programmable Sources`](https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html). Programmable sources are short Python scripts that create [`VTK`](https://vtk.org) objects.

The objects were developed using the ParaView GUI and the [Programmable Source editor](https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#recipes-for-programmable-source). The final scripts are then placed in a file in `magnetovis/Sources/`. Each file in this directory is associated with a object and the code that is used to genereate the object is in a function called `Script()`. When a file is executed, the content of `Script()` is placed in the `Programmable Source` editor and executed.

To demonstrate the general procedure by which magnetovis object are created, we will use the [Helix](https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html#helix-source) example from the ParaView user's guide.


%Magnetovis objects are listed in the ParaView `Sources` drop-down menu. 

%Selection of these sources creates an unstyled object that can be modified using the `Display (GeometryRepresentation)` menu in the `Properties` window.

%In `magnetovis`, each Programmable Source object has an associated script that adds attributes to the display object such as colors and annotations. To apply these attributes, execute a `Macro` associated with the Programmable Source.

# Notes

See `docs/Satellite_Region_Notes.md` for documentation on how magnetosphere regions were computed and a comparison with regions reported by SSCWeb.
