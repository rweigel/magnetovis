
vtk_options = {"a": 1, "b": 2, "c": 3}
render_options = {"render": True, "show": False}

def cube(vtk_options, render_options):
	# Creates a vtk object using programmable source or a 
	# VTK python library, whichever make sense.
	vtkobj = cube_vtk(**vtk_options) 

	# Render the vtk object in ParaView.
	cube_render(vtkobj, **render_options)

def cube_vtk(a=0, b=0, c=0):
	print(a)
	print(b)
	print(c)
	return {}

def cube_render(vtkobj, render=False, show=True):
	print(vtkobj)
	print(render)
	print(show)


cube(vtk_options, render_options)