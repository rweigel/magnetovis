# When executed, all result in n lines connected lines with n different colors showing in ParaView.
# Magnetovis uses "Single file approach #2".

# From this directory, execute
#   magnetovis demo.py

# Two file approach
if False:
	from objs_wrapper import objs_wrapper
	objs_wrapper(nPts=10, obj='helix')

# Single file approach #1:
if False:
	from objs import wrapper
	wrapper(nPts=10, obj='helix')

# Single file approach #2 (used by magnetovis):
if True:
	from objs import line
	line(nPts=10)

