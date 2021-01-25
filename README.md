This project is in a "pre-alpha" stage. Expect major changes and inconsistencies between the documentation and code.

# About

`magnetovis` is a set of Python scripts that display magnetosphere-related objects, regions, and data in ParaView.

See the demo files in https://github.com/rweigel/magnetovis for example usage.

This project is not ready for general use. Development is on-going.

# Install

An existing installation of [ParaView](https://www.paraview.org/download/) is required. 

The set-up script in `magnetovis` will check for compatability between the Python version distributed with an existing install of ParaView and the Python version used for the `magnetovis` installation.

Installation has been tested only on OS-X. 

## User

To install and test, use

```
pip install 'git+https://github.com/rweigel/magnetovis' --upgrade
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

## Manual

```
git clone https://github.com/rweigel/magnetovis
cd magnetovis; 
conda create --name python2.7 python=2.7
conda install numpy; pip install spacepy hapiclient
# In the following, change the path /opt to the location of your anaconda3 or miniconda3 install
# Also change /Applications/ParaView-5.7.0.app/Contents/MacOS/ to be the directory where
# Paraview is installed.
PYTHONPATH=/opt/anaconda3/envs/python2.7/lib/python2.7/site-packages:/opt/anaconda3/envs/python2.7/lib/site-python:. /Applications/ParaView-5.7.0.app/Contents/MacOS/paraview --script=demo.py
```

# Use

```
magnetovis --script=magnetovis_demo.py
```

This script

1. checks for compatability between the user's version of Python and the Python distributed with the installed version of ParaView, and
2. forms and executes a command line command, e.g., `PYTHONPATH=... paraview --script=magnetovis_demo.py`. All command line arguments are passed through to the ParaView command line program.

# Notes

See `docs/Region_Notes.md` for documentation on how magnetosphere regions were computed.
