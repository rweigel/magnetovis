#from magnetovis.objects import *

from magnetovis import util
from magnetovis import vtk
from magnetovis.logging import logger

from magnetovis.paraview import ProxyInfo
from magnetovis.paraview.CreateProgrammableSource import CreateProgrammableSource
from magnetovis.paraview.CreateViewAndLayout import CreateViewAndLayout

from magnetovis.paraview.GetDisplayDefaults import GetDisplayDefaults
from magnetovis.paraview.GetDisplayDefaults import PrintDisplayDefaults
from magnetovis.paraview.GetProperties import GetProperties
from magnetovis.paraview.GetRegistrationName import GetRegistrationName
from magnetovis.paraview.SetDisplayProperties import SetDisplayProperties
from magnetovis.paraview.SetCamera import SetCamera
from magnetovis.paraview.SetColoring import SetColoring
from magnetovis.paraview.SetTitle import SetTitle

# Generate Programmable Sources from files in ./Sources.
# Technique based on
# https://philip-trauner.me/blog/post/python-tips-dynamic-function-definition
# Result of the following is equivalent writing a function definition in __init__.py for
# every file in Sources. So for Sources/StructuredGrid.py, we would otherwise write
# def StructuredGrid(**kwargs):
#    return CreateProgrammableSource("StructuredGrid", **kwargs)
import os
import glob
root = os.path.dirname(os.path.abspath(__file__))
sources = glob.glob(os.path.join(root, os.path.join("Sources", "*.py")))
for source in sources:
    file = os.path.basename(os.path.splitext(source)[0])
    #logging.info("Creating programmable source function from " + source)
    exec('def ' + file + "(**kwargs): return CreateProgrammableSource('" + file + "', **kwargs)")

del os
del glob
del root
del sources
del source
del file