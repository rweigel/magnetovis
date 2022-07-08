name = "GridData"

if False:
	from magnetovis.paraview.CreatePlugin import CreatePlugin
	Plugin = CreatePlugin(name)

# Ideally instead of the following three lines, would do as above.
# However, this does not work. Why?
import os
from magnetovis.paraview import CreatePlugin
exec(open(os.path.abspath(CreatePlugin.__file__)).read())
Plugin = CreatePlugin(name)
