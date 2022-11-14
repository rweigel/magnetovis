# The following if statement prevents this demo from being
# executed at startup. We could simply put the demos in
# a different directory so that this is not needed. Or,
# in the launch script, we can build a list of plugins to
# load and pass them as --plugins instead of passing a 
# directory name.

# Demo 1
if not '__file__' in globals():

	import paraview.simple as pvs
	pvs.Text()
	grid = pvs.MagnetovisGridData()
	pvs.Show(grid)
