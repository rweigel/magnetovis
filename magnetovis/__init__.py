from magnetovis import vtk
from magnetovis import util
from magnetovis import functions
from magnetovis.log import logger

from magnetovis.paraview import ProxyInfo
from magnetovis.paraview.CreateProgrammableSource import CreateProgrammableSource
from magnetovis.paraview.CreateViewAndLayout import CreateViewAndLayout

from magnetovis.paraview.GetDisplayDefaults import GetDisplayDefaults
from magnetovis.paraview.GetDisplayDefaults import PrintDisplayDefaults
from magnetovis.paraview.GetSourceDefaults import GetSourceDefaults
from magnetovis.paraview.GetSourceDefaults import PrintSourceDefaults

from magnetovis.paraview.GetRegistrationName import GetRegistrationName
from magnetovis.paraview.SetDisplayProperties import SetDisplayProperties
from magnetovis.paraview.SetCamera import SetCamera
from magnetovis.paraview.SetColoring import SetColoring
from magnetovis.paraview.ClearPipeline import ClearPipeline
from magnetovis.paraview.SetTitle import SetTitle
from magnetovis.paraview.UniqueName import UniqueName

def programmable_defs(ptype):

  # Generate Programmable Sources from files in ./Sources.
  # Technique based on
  # https://philip-trauner.me/blog/post/python-tips-dynamic-function-definition
  # Result of the following is equivalent writing a function definition in __init__.py for
  # every file in Sources. So for Sources/StructuredGrid.py, we would otherwise write
  # def StructuredGrid(**kwargs):
  #    return CreateProgrammableSource("StructuredGrid", **kwargs)

  assert ptype in ["source", "filter"]

  import os
  import glob
  root = os.path.dirname(os.path.abspath(__file__))
  if ptype == "source":
    path = "Sources"
    logger.info(f"Creating programmable sources using files in {root}")
    ignore = "MySource"
  if ptype == "filter":
    path = "Filters"
    logger.info(f"Creating programmable filters using files in {root}")
    ignore = "MyFilter"

  sources = glob.glob(os.path.join(root, os.path.join(path, "*.py")))
  def_strs = []
  for source in sources:
    file = os.path.basename(os.path.splitext(source)[0])
    exclude = file.endswith("_demo")
    exclude = exclude and file.startswith("__")
    exclude = exclude and file.startswith(ignore)
    if not exclude:
      def_strs.append('def ' + file + "(**kwargs): return CreateProgrammableSource('" + source + "', '" + ptype + "', **kwargs)")

  return def_strs

for def_str in programmable_defs("source"):
  exec(def_str)

for def_str in programmable_defs("filter"):
  exec(def_str)
