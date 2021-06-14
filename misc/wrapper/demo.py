# Two file approach
if False:
	from objs_wrapper import objs_wrapper
	objs_wrapper(nPts=10,obj='helix')

# Single file approach #1:
if False:
	from objs import wrapper
	wrapper(nPts=10,obj='helix')

# Single file approach #2:
if True:
	from objs import line
	line(nPts=10)

# When executed, both result in n lines connected lines with n different colors showing in ParaView.
#line_currentmethod(n=2)
# Usine paraview.simple lines or saving vtk files.

#line_programablesource(n=2)
