# Ideally instead of the following three lines, would do
#   from magnetovis.paraview.CreatePlugin import CreatePlugin
# However, this does not work. Why?
import os
from magnetovis.paraview import CreatePlugin
exec(open(os.path.abspath(CreatePlugin.__file__)).read())

name = "StructuredGrid"
Plugin = CreatePlugin(name)
