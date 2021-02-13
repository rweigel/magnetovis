"""
This code gives a simple example of how to create screen shot using two different methods.
The first method hides all objects in the render view except for the object that
is provided in the argument, takes a screen shot, then brings back all those objects
that were visible.

The second method creates a new template and render view. It imports the object from
the previous renderview into the newly created one. it transfers over the display properties
to the new render view (this part still gives a little problem), takes a screenshot,
then deletes the new template and renderview. 

"""

import paraview.simple as pvs
import os

def sphere(r, representation, renderView=None, fName=None):
	sphere = pvs.Sphere()
	sphere.Radius = r 
	if not renderView:
		renderView = pvs.GetActiveViewOrCreate('RenderView')

	sphereDisplay = pvs.Show(sphere, renderView)
	sphereDisplay.Representation = representation

	if False:
		screenshot_hide_show(object=sphere, renderView=renderView, fName=fName)
	if True:
		screenshot_new_renderView(object=sphere, renderView=renderView, fName=fName)


def screenshot_hide_show(renderView=None, object=None, fName=None, tempCamera=None):

	visible_objs = []

	originalCam = pvs.GetActiveCamera()
	# option 1 hide all the objects except for the current one
	for name_id, pObject in pvs.GetSources().items():
		objDislay = pvs.GetRepresentation(proxy=pObject, view=renderView)
		if objDisplay.Visibility:
			visible_objs.append(pObject)
		if pObject != object:
			pvs.Hide(pObject)

	if not tempCamera:
		renderView.ResetCamra()
		tempCamera = pvs.GetActiveCamera()
		tempCamera.Azimuth(30)
		tempCamera.Elevation(30)

	pvs.SaveScreenshot(fName, renderView, ImageResolution=[1800, 1220])

	tempCamera.SetPosition(originalCam.GetPositon())
	tempCamera.SetFolcalPoint(originalCam.GetFocalPoint())

	for pObject in visible_objs:
		pvs.Show(pObject, renderView)

	# pvs.ShowAll()

def screenshot_new_renderView(object=None, renderView=None, fName=None, camera=None):
	
	# option 2 create a new renderView
	# input option and 
	# https://www.paraview.org/Wiki/ParaView/Python_Scripting
	# https://discourse.paraview.org/t/feature-request-clone-renderview/2370/3
	# https://docs.paraview.org/en/latest/UsersGuide/displayingData.html

	if not renderView:
		renderView = pvs.GetActiveViewOrCreate('RenderView')


	objDisplay = pvs.GetRepresentation(proxy=object, view=renderView) # with this we don't need to  pass around objectDisplay variable
	tempLayout = pvs.CreateLayout('Temp Layout')
	tempRenderView = pvs.CreateRenderView()
	pvs.AssignViewToLayout(view=tempRenderView, layout=tempLayout, hint=0)
	pvs.SetActiveView(tempRenderView)
	pvs.SetActiveSource(object)

	# show data in view
	tempObjDisplay = pvs.Show(object, tempRenderView)
	for property in objDisplay.ListProperties():
		# print('\n')
		# print(property)
		# print(display.GetPropertyValue(property))
		# RepresentationTypesInfo gives a Runtime Error message. this is a list of strings
		# BlockColor and Block Opacity both give attribute error. they are blank {}
		# ColorArrayName produces TypeError: SetElement argument 2: string or None required. this gives [None, ''] might have to use color transfer function
		# OpacityArray produces TypeError: SetElement argument 2: string or None required. this gives ['POINTS', 'Normals']
		# SetScaleArray producecs TypeError: SetElement argument 2: string or None required. this gives ['POINTS', 'Normals']

		problems = ['RepresentationTypesInfo','BlockColor', 'BlockOpacity', 'ColorArrayName','OpacityArray',
					'SetScaleArray']
					# do try except to catch the problems 
		if property not in problems:
		try: 
			tempObjDisplay.SetPropertyWithName(property, objDisplay.GetPropertyValue(property))
		except...
	pvs.Show()

	if not camera:
		tempRenderView.ResetCamera()
		tempCamera = pvs.GetActiveCamera()
		tempCamera.Azimuth(30) # Horizontal rotation
		tempCamera.Elevation(30) # Vertical rotation
	else: 
		tempCamera = pvs.GetActiveCamera()
		tempCamera.SetPosition(camera.GetPosition())
		tempCamera.SetFocalPoint(camera)

	fname = fname.repalce(' ','_').replace(':','')
	pvs.SaveScreenshot(fName, tempRenderView, ImageResolution=[1800, 1220])
	
	# # destroy temps 
	pvs.Delete(tempRenderView)
	del tempRenderView
	pvs.RemoveLayout(tempLayout)
	del tempLayout

	pvs.SetActiveView(renderView)



r = 2
representation = 'Surface With Edges'
fName = os.path.join(os.getcwd(),'testimg.png')
sphere(r, representation, fName=fName)





if False:
	# trace generated using paraview version 5.7.0
	#
	# To ensure correct image size when batch processing, please search 
	# for and uncomment the line `# renderView*.ViewSize = [*,*]`

	#### import the simple module from the paraview
	from paraview.simple import *
	#### disable automatic camera reset on 'Show'
	paraview.simple._DisableFirstRenderCameraReset()

	# create a new 'Sphere'
	sphere1 = Sphere()
	sphere1.Radius = 2.0

	# get active view
	renderView1 = GetActiveViewOrCreate('RenderView')

	# show data in view
	sphere1Display = Show(sphere1, renderView1)
	sphere1Display.Representation = 'Surface'

	# reset view to fit data
	renderView1.ResetCamera()

	# get the material library - not sure what the materials library is
	materialLibrary1 = GetMaterialLibrary()
	renderView1.Update()

	sphere1Display.SetRepresentationType('Surface With Edges')

	# get camera animation track for the view
	cameraAnimationCue1 = GetCameraTrack(view=renderView1)

	# current camera placement for renderView1
	renderView1.CameraPosition = [0.0, 12.0, 14.3577]
	renderView1.CameraParallelScale = 3.73729

	# save screenshot
	SaveScreenshot('/Users/Angel/Desktop/pic.png', renderView1, ImageResolution=[1112, 1220], 
	    # PNG options
	    CompressionLevel='4')

	#### saving camera placements for all active views

	# current camera placement for renderView1
	renderView1.CameraPosition = [0.0, 12.0, 14.3577]
	renderView1.CameraParallelScale = 3.73729

if False:
	# trace generated using paraview version 5.7.0
	#
	# To ensure correct image size when batch processing, please search 
	# for and uncomment the line `# renderView*.ViewSize = [*,*]`

	#### import the simple module from the paraview
	from paraview.simple import *
	#### disable automatic camera reset on 'Show'
	paraview.simple._DisableFirstRenderCameraReset()

	# create a new 'Sphere'
	sphere1 = Sphere()

	# get active view
	renderView1 = GetActiveViewOrCreate('RenderView')

	# show data in view
	sphere1Display = Show(sphere1, renderView1)
	sphere1Display.Representation = 'Surface'

	renderView1.ResetCamera()

	# get the material library
	materialLibrary1 = GetMaterialLibrary()

	# update the view to ensure updated data information
	renderView1.Update()

	CreateLayout('Layout #2')

	# set active view
	SetActiveView(None)

	# Create a new 'Render View'
	renderView2 = CreateView('RenderView')
	renderView2.OSPRayMaterialLibrary = materialLibrary1

	# get layout
	layout2 = GetLayoutByName("Layout #2")

	# assign view to a particular cell in the layout
	AssignViewToLayout(view=renderView2, layout=layout2, hint=0)

	# set active source
	SetActiveSource(sphere1)

	# show data in view
	sphere1Display_1 = Show(sphere1, renderView2)

	# trace defaults for the display properties.
	sphere1Display_1.Representation = 'Surface'

	# reset view to fit data
	renderView2.ResetCamera()

	# Properties modified on sphere1
	sphere1.Radius = 1.0

	# update the view to ensure updated data information
	renderView1.Update()

	# update the view to ensure updated data information
	renderView2.Update()

	# destroy renderView2
	Delete(renderView2)
	del renderView2

	RemoveLayout(layout2)

	# Properties modified on sphere1
	sphere1.Radius = 0.75

	# update the view to ensure updated data information
	renderView1.Update()

	#### saving camera placements for all active views

	# current camera placement for renderView1
	renderView1.CameraPosition = [0.0, 0.0, 3.2903743041222895]
	renderView1.CameraParallelScale = 0.8516115354228021

	#### uncomment the following to render all views
	# RenderAllViews()
	# alternatively, if you want to write images, you can use SaveScreenshot(...).
