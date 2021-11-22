import os
from magnetovis.paraview import CreatePlugin
exec(open(os.path.abspath(CreatePlugin.__file__)).read())

name = "RectilinearGrid"
Plugin = CreatePlugin(name)
#Plugin.__name__ = name + "Plugin"



