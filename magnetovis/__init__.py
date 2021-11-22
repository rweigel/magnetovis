#from magnetovis.objects import *

import logging
logging.basicConfig(format='%(asctime)s.%(msecs)03d:%(filename)s:%(funcName)s(): %(message)s',
                    level=logging.INFO, datefmt='%S')
logging.info("Called.")

from magnetovis import util
from magnetovis import vtk
from magnetovis.paraview import ProxyInfo
from magnetovis.paraview.SetDisplayProperties import SetDisplayProperties
from magnetovis.paraview.ColorByCellId import ColorByCellId
from magnetovis.paraview.CreateProgrammableSource import CreateProgrammableSource
from magnetovis.paraview.SetCamera import SetCamera

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