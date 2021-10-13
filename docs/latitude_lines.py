import os
import magnetovis as mvz
import paraview.simple as pvs

time = [2015, 1, 1, 0, 0]
coord_sys = "GEO"

_, _, earthSource = mvz.earth(time, coord_sys=coord_sys)

_, _, latSource = mvz.latitude_lines(time=demo_time, coord_sys=demo_coord)
_, _, latTubeFilter = mvz.tube(latSource,tube_radius=0.02)
mvz.screenshot_object(obj=latTubeFilter)

if False:
    lonDis, renderView, lonSource = mvs.longitude_lines(time=demo_time, coord_sys=demo_coord)
    lonDisTue, renderView, lonTubeFilter = mvs.tube(lonSource, tube_radius=0.02)
    mvs.screenshot_object(obj=lonTubeFilter)
