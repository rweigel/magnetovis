This project is in a "alpha" stage. Expect major changes and inconsistencies between the documentation and code. This project is not ready for general use. Development is on-going.

# About

`magnetovis` is a set of Python scripts that display magnetosphere-related objects, regions, and data in [ParaView](https://www.paraview.org/) that was initially developed under NASA Grant Number 80NSSC21K0305.

The objects created by `magnetovis` scripts are displayed in the `ParaView` GUI where the can be inspected, manipulated, and modified.

See the demo files in https://github.com/rweigel/magnetovis for example usage.

# Install

An existing installation of [ParaView 5.9+](https://www.paraview.org/download/) is required. Since version 5.9, ParaView includes a version of Python 3. Because `magnetovis` requires packages that are not distributed with ParaView, you should execute `magnetovis` in a enviroment with the same Python version number as that used by ParaView.

%The set-up script in `magnetovis` will check for compatability between the Python version distributed with the ParaView version that is installed and the Python version used for the `magnetovis` installation using `pip`. A warning will be generated if there is a known incompatability between the user's Python version and that shipped with `ParaView`.

Installation has been only tested in OS-X and Linux. 

## User

To install and run a demo script, use

```
pip install -U 'git+https://github.com/rweigel/magnetovis'
cd magnetovis; magnetovis --script=magnetovis_demo.py
```

A PyPi package will not be available until the project is ready for general use.

## Developer

```
git clone https://github.com/rweigel/magnetovis
cd magnetovis; pip install --editable .
cd magnetovis; magnetovis --script=magnetovis_demo.py
```

Please provide feedback by submitting an [issue](https://github.com/rweigel/magnetovis/issues).

# Approach

The objects (e.g, Earth, plasmapause) in `magnetovis` are created using `ParaView` [`Programmable Filters`](https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html). Programmable filters are short Python scripts that create a `VTK` object. `Programmable Filters` can also be used to modify (filter) an object.

In `magnetovis`, each function associated with an object generates a `VTK` object with a Programmable Filter, converts it to a `ParaView` display object, and then adds attributes to the display object such as colors, annotations, and display properties prior to rendering in `ParaView`.

A Programmable Filter script is typically entered in the `ParaView` GUI. To execute a programmable filter within a Python script that has input parameters, a script containing the input parameters is generated and then passed to `ParaView`. The general method of operation is demonstrated in [misc/wrapper/demo.py](https://github.com/rweigel/magnetovis/blob/main/misc/wrapper/demo.py). An example of creating a `VTK` object and then modifying attributes is given in [misc/multi_color_lines](https://github.com/rweigel/magnetovis/blob/main/misc/multi_color_lines/demo.py).

# Notes

See `docs/Region_Notes.md` for documentation on how magnetosphere regions were computed.
