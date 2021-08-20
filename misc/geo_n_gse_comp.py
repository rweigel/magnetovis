import magnetovis as mvs

csys = 'GEO'

time = [2015, 1,12, 12, 9, 13]
_, _, xAxisSource = mvs.axis(time=time, val='X', lims=[-10, 10], coord_sys=csys)
mvs.tube(xAxisSource, vary_radius='By Scalar', tube_radius=0.05)

_, _, yAxisSource = mvs.axis(time=time, val='Y', lims=[-10, 10], coord_sys=csys)
mvs.tube(yAxisSource, vary_radius='By Scalar', tube_radius=0.05)

_, _, zAxisSource = mvs.axis(time=time, val='Z', lims=[-10, 10], coord_sys=csys)
mvs.tube(zAxisSource, vary_radius='By Scalar', tube_radius=0.05)

########
csys = 'GSE'
for m in range(1,13):
    time = [2015, m, 20, 12, 9, 10]
    _, _, xAxisSource = mvs.axis(time=time, val='X', lims=[-5, 5], coord_sys=csys)
    mvs.tube(xAxisSource, vary_radius='By Scalar', tube_radius=0.05)

    _, _, yAxisSource = mvs.axis(time=time, val='Y', lims=[-5, 5], coord_sys=csys)
    mvs.tube(yAxisSource, vary_radius='By Scalar', tube_radius=0.05)

    _, _, zAxisSource = mvs.axis(time=time, val='Z', lims=[-5, 5], coord_sys=csys)
    mvs.tube(zAxisSource, vary_radius='By Scalar', tube_radius=0.05)
