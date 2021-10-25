import os
import magnetovis as mvz
import paraview.simple as pvs

time = [2015, 1, 1, 0, 0]
coord_sys = "MAG"

_, _, earthSource = mvz.earth(time, coord_sys=coord_sys)

_, _, zAxisSource = mvz.axis(time=time, val='Z', lims=[-3,3], coord_sys=coord_sys)
_, _, zTubeFilter = mvz.tube(zAxisSource, vary_radius='By Scalar')

_, _, latSource = mvz.latitude_lines(time=time, coord_sys=coord_sys)
pvs.WriteImage('docs/latitude_lines_demo-1.png')

_, _, latTubeFilter = mvz.tube(latSource, tube_radius=0.01)
pvs.WriteImage('docs/latitude_lines_demo-2.png')

