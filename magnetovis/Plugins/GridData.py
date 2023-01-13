name = "GridData"

if False:
	from magnetovis.paraview.CreatePlugin import CreatePlugin
	Plugin = CreatePlugin(name)

# Ideally instead of the following three lines, would do as above.
# However, this does not work. Why? See also
# https://github.com/OpenGeoVis/PVGeo/blob/main/PVPlugins/PVGeo_All.py

import os
from magnetovis.paraview import CreatePlugin
exec(open(os.path.abspath(CreatePlugin.__file__)).read())
Plugin = CreatePlugin(name)
