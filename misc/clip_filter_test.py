import sys
import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.join(os.path.dirname('__file__'), '..'))
from magnetovis import objects
import paraview.simple as pvs

"""
This script shows a simple example of applying a filter to all
objects in the pipeline through the use of GetSources()
for any number of arbitrary objects in the pipeline browswer.

to use:
    $ magnetovis --script=clip_filter_test.py
"""

# create a render view object
renderView = pvs.GetActiveViewOrCreate('RenderView')

# create a list of objects
sphere = pvs.Sphere()
disk = pvs.Disk()
cylinder = pvs.Cylinder()

# GetSources() returns a dictionary where the key is
# a 2 item tuple and the value is the python object.
# the first value of the tuple is the name of the object
# as seen in the pipeline browswer.and the second value is the id
# example:
# {('Disk1', '8659'): <paraview.servermanager.Disk object at 0x12c600ad0> }
for name_id, pObject in pvs.GetSources().items():
    # create a new clip
    clip = pvs.Clip(Input=pObject)
    clip.ClipType = 'Plane'
    clip.Invert = 0
    clip.ClipType.Normal = [0,1,0]
    clipDisplay = pvs.Show(clip, renderView)
    
    # to hide plane widget in paraview
    pvs.Hide3DWidgets(proxy=clip.ClipType)

renderView.Update()


"""
    code from paraview trace
    
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

    # Properties modified on sphere1
    sphere1.Radius = 2.0

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')
    # uncomment following to set a specific view size
    # renderView1.ViewSize = [1506, 496]

    # show data in view
    sphere1Display = Show(sphere1, renderView1)

    # trace defaults for the display properties.
    sphere1Display.Representation = 'Surface'
    sphere1Display.ColorArrayName = [None, '']
    sphere1Display.OSPRayScaleArray = 'Normals'
    sphere1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    sphere1Display.SelectOrientationVectors = 'None'
    sphere1Display.ScaleFactor = 0.4
    sphere1Display.SelectScaleArray = 'None'
    sphere1Display.GlyphType = 'Arrow'
    sphere1Display.GlyphTableIndexArray = 'None'
    sphere1Display.GaussianRadius = 0.02
    sphere1Display.SetScaleArray = ['POINTS', 'Normals']
    sphere1Display.ScaleTransferFunction = 'PiecewiseFunction'
    sphere1Display.OpacityArray = ['POINTS', 'Normals']
    sphere1Display.OpacityTransferFunction = 'PiecewiseFunction'
    sphere1Display.DataAxesGrid = 'GridAxesRepresentation'
    sphere1Display.PolarAxes = 'PolarAxesRepresentation'

    # init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
    sphere1Display.ScaleTransferFunction.Points = [-0.9749279022216797, 0.0, 0.5, 0.0, 0.9749279022216797, 1.0, 0.5, 0.0]

    # init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
    sphere1Display.OpacityTransferFunction.Points = [-0.9749279022216797, 0.0, 0.5, 0.0, 0.9749279022216797, 1.0, 0.5, 0.0]

    # reset view to fit data
    renderView1.ResetCamera()

    # get the material library
    materialLibrary1 = GetMaterialLibrary()

    # update the view to ensure updated data information
    renderView1.Update()

    # create a new 'Disk'
    disk1 = Disk()

    # Properties modified on disk1
    disk1.OuterRadius = 3.0

    # show data in view
    disk1Display = Show(disk1, renderView1)

    # trace defaults for the display properties.
    disk1Display.Representation = 'Surface'
    disk1Display.ColorArrayName = [None, '']
    disk1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    disk1Display.SelectOrientationVectors = 'None'
    disk1Display.ScaleFactor = 0.6000000000000001
    disk1Display.SelectScaleArray = 'None'
    disk1Display.GlyphType = 'Arrow'
    disk1Display.GlyphTableIndexArray = 'None'
    disk1Display.GaussianRadius = 0.03
    disk1Display.SetScaleArray = [None, '']
    disk1Display.ScaleTransferFunction = 'PiecewiseFunction'
    disk1Display.OpacityArray = [None, '']
    disk1Display.OpacityTransferFunction = 'PiecewiseFunction'
    disk1Display.DataAxesGrid = 'GridAxesRepresentation'
    disk1Display.PolarAxes = 'PolarAxesRepresentation'

    # update the view to ensure updated data information
    renderView1.Update()

    # create a new 'Cylinder'
    cylinder1 = Cylinder()

    # Properties modified on cylinder1
    cylinder1.Height = 5.0

    # show data in view
    cylinder1Display = Show(cylinder1, renderView1)

    # trace defaults for the display properties.
    cylinder1Display.Representation = 'Surface'
    cylinder1Display.ColorArrayName = [None, '']
    cylinder1Display.OSPRayScaleArray = 'Normals'
    cylinder1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    cylinder1Display.SelectOrientationVectors = 'None'
    cylinder1Display.ScaleFactor = 0.5
    cylinder1Display.SelectScaleArray = 'None'
    cylinder1Display.GlyphType = 'Arrow'
    cylinder1Display.GlyphTableIndexArray = 'None'
    cylinder1Display.GaussianRadius = 0.025
    cylinder1Display.SetScaleArray = ['POINTS', 'Normals']
    cylinder1Display.ScaleTransferFunction = 'PiecewiseFunction'
    cylinder1Display.OpacityArray = ['POINTS', 'Normals']
    cylinder1Display.OpacityTransferFunction = 'PiecewiseFunction'
    cylinder1Display.DataAxesGrid = 'GridAxesRepresentation'
    cylinder1Display.PolarAxes = 'PolarAxesRepresentation'

    # init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
    cylinder1Display.ScaleTransferFunction.Points = [-1.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]

    # init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
    cylinder1Display.OpacityTransferFunction.Points = [-1.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]

    # update the view to ensure updated data information
    renderView1.Update()

    # set active source
    SetActiveSource(sphere1)

    # create a new 'Clip'
    clip1 = Clip(Input=sphere1)
    clip1.ClipType = 'Plane'
    clip1.Scalars = [None, '']

    # Properties modified on clip1
    clip1.Scalars = ['POINTS', '']

    # Properties modified on clip1.ClipType
    clip1.ClipType.Normal = [0.0, 1.0, 0.0]

    # show data in view
    clip1Display = Show(clip1, renderView1)

    # trace defaults for the display properties.
    clip1Display.Representation = 'Surface'
    clip1Display.ColorArrayName = [None, '']
    clip1Display.OSPRayScaleArray = 'Normals'
    clip1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    clip1Display.SelectOrientationVectors = 'None'
    clip1Display.ScaleFactor = 0.4
    clip1Display.SelectScaleArray = 'None'
    clip1Display.GlyphType = 'Arrow'
    clip1Display.GlyphTableIndexArray = 'None'
    clip1Display.GaussianRadius = 0.02
    clip1Display.SetScaleArray = ['POINTS', 'Normals']
    clip1Display.ScaleTransferFunction = 'PiecewiseFunction'
    clip1Display.OpacityArray = ['POINTS', 'Normals']
    clip1Display.OpacityTransferFunction = 'PiecewiseFunction'
    clip1Display.DataAxesGrid = 'GridAxesRepresentation'
    clip1Display.PolarAxes = 'PolarAxesRepresentation'
    clip1Display.ScalarOpacityUnitDistance = 1.628097375536559

    # init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
    clip1Display.ScaleTransferFunction.Points = [-0.9749279022216797, 0.0, 0.5, 0.0, 0.9749279022216797, 1.0, 0.5, 0.0]

    # init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
    clip1Display.OpacityTransferFunction.Points = [-0.9749279022216797, 0.0, 0.5, 0.0, 0.9749279022216797, 1.0, 0.5, 0.0]

    # hide data in view
    Hide(sphere1, renderView1)

    # update the view to ensure updated data information
    renderView1.Update()

    # Properties modified on clip1
    clip1.Invert = 0

    # update the view to ensure updated data information
    renderView1.Update()

    #### saving camera placements for all active views

    # current camera placement for renderView1
    renderView1.CameraPosition = [0.0, 0.0, 13.161497216489158]
    renderView1.CameraParallelScale = 3.4064461416912084

    #### uncomment the following to render all views
    # RenderAllViews()
    # alternatively, if you want to write images, you can use SaveScreenshot(...).
"""
