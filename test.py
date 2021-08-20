"""
Usage:
    magnetovis --script=test.py
"""

import magnetovis as mvs
import paraview.simple as pvs
from hxform import hxform as hx

# according to our code the sun right above the prime meridan on
# 2015-3-20 12:09:10
# but according to https://gml.noaa.gov/grad/solcalc/
# it should be 2015-3-20 12:07:32

csys = 'GSE'
# for GSE the x axis is always pointing at the sun therefore we expect
month = 9
time = [2015,3,20,0,9,10]
mvs.earth(time, coord_sys=csys)
# time = [2015,3,20,3,9,10]
# mvs.earth(time, coord_sys=csys)
# time = [2015,3,20,6,9,10]
# mvs.earth(time, coord_sys=csys)
# time = [2015,3,20,9,9,10]
# mvs.earth(time, coord_sys=csys)
# time = [2015,3,20,12,9,10] # time when geo and gei give same answer[2015,3,20,12,9,10]
# mvs.earth(time, coord_sys=csys)
# time = [2015,3,20,15,9,10]
# mvs.earth(time, coord_sys=csys)
# time = [2015,3,20,18,9,10]
# mvs.earth(time, coord_sys=csys)
# time = [2015,3,20,21,9,10]
# mvs.earth(time, coord_sys=csys)

# mvs.plane(time=time, val='XY', extend=[[-55, 25], [-55, 55]], coord_sys=csys)
# mvs.plane(time=time, val='XZ', extend=[[-55, 25], [-55, 55]], coord_sys=csys)
# mvs.plane(time=time, val='YZ', extend=[[-55, 55], [-55, 55]], coord_sys=csys)
#
_, _, xAxisSource = mvs.axis(time=time, val='X', lims=[-55, 25], coord_sys=csys)
mvs.tube(xAxisSource, vary_radius='By Scalar', tube_radius=0.05)

_, _, yAxisSource = mvs.axis(time=time, val='Y', lims=[-55, 55], coord_sys=csys)
mvs.tube(yAxisSource, vary_radius='By Scalar', tube_radius=0.05)

_, _, zAxisSource = mvs.axis(time=time, val='Z', lims=[-55, 55], coord_sys=csys)
mvs.tube(zAxisSource, vary_radius='By Scalar', tube_radius=0.05)


# if csys != 'GSM':
#     gsm_text = pvs.Text(registrationName='GSM')
#     gsm_text.Text = 'GSM'
#     renderView = pvs.GetActiveViewOrCreate('RenderView')
#     gsm_text_display = pvs.Show(gsm_text)
#     gsm_text_display.WindowLocation = 'AnyLocation'
#     gsm_text_display.Position = [0.04, 0.04]
#     gsm_text_display.Interactivity = 0

# setting up proper viewing properties
cam_pos = [180,250,100]
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
