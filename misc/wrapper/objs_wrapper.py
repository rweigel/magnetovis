def objs_wrapper(**kwargs):
    import paraview.simple as pvs
    import os
    file = os.path.join(os.getcwd(), 'objs.py')

	# create a new 'Programmable Source'
    programmableSource1 = pvs.ProgrammableSource()
    programmableSource1.Script = "kwargs="+str(kwargs)+";execfile('{}',globals(),locals())".format(file)

	# get active view
    renderView1 = pvs.GetActiveViewOrCreate('RenderView')

	# show data in view
    programmableSource1Display = pvs.Show(programmableSource1, renderView1)

	# trace defaults for the display properties.
    programmableSource1Display.Representation = 'Surface'

	# update the view to ensure updated data information
    renderView1.Update()
