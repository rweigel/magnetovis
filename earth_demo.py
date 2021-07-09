import magnetovis as mvs

time = (2015, 1, 1, 0, 0, 0)
csys = 'GEO'

mvs.earth(time,
            coord_sys=csys,
            topo_url='http://mag.gmu.edu/git-data/magnetovis/topography/world.topo.2004{0:02d}.3x5400x2700.png',
            debug=True)
