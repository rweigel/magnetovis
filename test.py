"""
Usage:
    magnetovis --script=test.py
"""

import magnetovis as mvs
import paraview.simple as pvs
from hxform import hxform as hx

csys = 'GSE'
# for GSE the x axis is always pointing at the sun therefore we expect
time = [2015,3,20,12,9,10] # time when geo and gei give same answer[2015,3,20,12,9,10]
mvs.earth(time, coord_sys=csys)



_, _, latSource = mvs.latitude_lines(time, csys)
mvs.tube(latSource, tube_radius=0.025, opacity=0.3)
_, _, lonSource = mvs.longitude_lines(time, csys)
mvs.tube(lonSource, tube_radius=0.025, opacity=0.3)

_, _, xAxisSource = mvs.axis(time=time, val='X', lims=[-20, 20], coord_sys=csys)
mvs.tube(xAxisSource, vary_radius='By Scalar', tube_radius=0.025, opacity=0.2)
_, _, yAxisSource = mvs.axis(time=time, val='Y', lims=[-20, 20], coord_sys=csys)
mvs.tube(yAxisSource, vary_radius='By Scalar', tube_radius=0.025, opacity=0.2)
_, _, zAxisSource = mvs.axis(time=time, val='Z', lims=[-20, 20], coord_sys=csys)
mvs.tube(zAxisSource, vary_radius='By Scalar', tube_radius=0.025, opacity=0.2)

mvs.plane(time, 'XY', extend=[[-20,20],[-20,20]], coord_sys=csys, opacity=.2)
mvs.plane(time, 'XZ', extend=[[-20,20],[-20,20]], coord_sys=csys, opacity=.2)
mvs.plane(time, 'YZ', extend=[[-20,20],[-20,20]], coord_sys=csys, opacity=.2)


if csys != 'GSM':
    gsm_text = pvs.Text(registrationName='GSM')
    gsm_text.Text = 'GSM'
    renderView = pvs.GetActiveViewOrCreate('RenderView')
    gsm_text_display = pvs.Show(gsm_text)
    gsm_text_display.WindowLocation = 'AnyLocation'
    gsm_text_display.Position = [0.04, 0.04]
    gsm_text_display.Interactivity = 0

# setting up proper viewing properties
cam_pos = [45,45,50]
cam_view_up = [0,0,1]
cam = pvs.GetActiveCamera()
if csys != 'GSM':
    cam_view_up = hx.transform(cam_view_up, time, 'GSM', csys, 'car', 'car')
    cam_pos = hx.transform(cam_pos, time, 'GSM', csys, 'car', 'car')
cam.SetPosition(*cam_pos)
cam.SetViewUp(*cam_view_up)
cam.SetFocalPoint(0,0,0)
pvs.Render()

# setting the center of rotation
view = pvs.GetActiveViewOrCreate("RenderView")
view.CenterOfRotation = [0,0,0]
