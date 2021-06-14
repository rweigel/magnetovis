import magnetovis as mvz

time = [2015, 1, 1, 0, 0]
coord_sys = "GEO"

_, _, earthSource = mvz.earth(time, coord_sys=coord_sys)
mvz.screenshot(obj=earthSource)
