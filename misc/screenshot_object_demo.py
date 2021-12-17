import os
import magnetovis as mvz
import paraview.simple as pvs

time = [2015, 1, 1, 0, 0]
coord_sys = "GEO"

_, _, earthSource = mvz.earth(time, coord_sys=coord_sys)
_, _, mpauseSource = mvz.magnetopause(time=time, coord_sys=coord_sys)

# Take a screenshot of only earthSource
mvz.screenshot_object(obj=earthSource, fileName='docs/screenshot_object_demo-1.png')

# Take a screenshot of both objects
pvs.WriteImage("docs/screenshot_object_demo-2.png")

renderView = pvs.GetActiveViewOrCreate('RenderView')

renderView.CameraPosition = [0, 0, 5]
renderView.CameraFocalPoint = [0, 0, 0]
renderView.CameraViewUp = [0, 0, 1]
renderView.CameraViewAngle = 45

#pvs.Show(sphereVTK, renderView)
pvs.Show()

