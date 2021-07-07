"""
Usage:
    magnetovis --script=test.py
"""

import magnetovis as mvs

time = [2015, 1, 1, 0, 0]
csys = 'GSM'

#mvs.earth(time, coord_sys=csys)

mvs.plane(time=time, val='XY', extend=[[-55, 25], [-55, 55]], coord_sys=csys)
mvs.plane(time=time, val='XZ', extend=[[-55, 25], [-55, 55]], coord_sys=csys)
mvs.plane(time=time, val='YZ', extend=[[-55, 55], [-55, 55]], coord_sys=csys)

_, _, xAxisSource = mvs.axis(time=time, val='X', lims=[-55, 25], coord_sys=csys)
mvs.tube(xAxisSource, vary_radius='By Scalar', tube_radius=0.05)

_, _, yAxisSource = mvs.axis(time=time, val='Y', lims=[-55, 55], coord_sys=csys)
mvs.tube(yAxisSource, vary_radius='By Scalar', tube_radius=0.05)

_, _, zAxisSource = mvs.axis(time=time, val='Z', lims=[-55, 55], coord_sys=csys)
mvs.tube(zAxisSource, vary_radius='By Scalar', tube_radius=0.05)
