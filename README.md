This project is in a "beta" stage. 

# About

`magnetovis` is a set of Python scripts that display magnetosphere-related objects, regions, and data in [ParaView](https://www.paraview.org/) that was initially developed under NASA Grant Number 80NSSC21K0305.

The objects created by `magnetovis` scripts are displayed in the `ParaView` GUI where the can be inspected, manipulated, and modified.

See the demo files in https://github.com/rweigel/magnetovis for example usage.

# Install

An existing installation of [ParaView 5.9+](https://www.paraview.org/download/) and Python 3.8.8+ is required. 

ParaView 5.9 includes a Python 3 version (3.8.8). Because `magnetovis` requires packages that are not distributed with ParaView, you should execute `magnetovis` in a enviroment with the same Python version number as that used by ParaView.

Installation has been only tested in OS-X and Linux. 

Please provide feedback by submitting an [issue](https://github.com/rweigel/magnetovis/issues).

## User

To install and run a demo script, use

```
conda create --name 3.8.8 python=3.8.8
conda activate 3.8.8
pip install -U 'git+https://github.com/rweigel/magnetovis'
cd magnetovis; magnetovis --script=magnetovis_demo.py
```

A PyPi package will eventually be made available.

## Developer

```
conda create --name 3.8.8 python=3.8.8
conda activate 3.8.8
git clone https://github.com/rweigel/magnetovis
cd magnetovis; pip install --editable .
magnetovis --script=magnetovis_demo.py
```

# Getting started


# Approach

The objects (e.g, Earth, plasmapause, etc.) in `magnetovis` are created using `ParaView` [`Programmable Sources`](https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html). Programmable sources are short Python scripts that create a [`VTK`](https://vtk.org) object. Magnetovis objects are listed in the ParaView `Sources` drop-down menu. 

%Selection of these sources creates an unstyled object that can be modified using the `Display (GeometryRepresentation)` menu in the `Properties` window.

In `magnetovis`, each Programmable Source object has an associated script that adds attributes to the display object such as colors and annotations. To apply these attributes, execute a `Macro` associated with the Programmable Source.

# Notes

See `docs/Satellite_Region_Notes.md` for documentation on how magnetosphere regions were computed and a comparison with regions reported by SSCWeb.
