# Execute using magnetovis.sh --script=magnetovis_demo.py

import sys
if sys.maxunicode > 65535:
    print('UCS4 build')
else:
    print('UCS2 build')

from magnetovis import objects

mvs.earth([2000, 1, 1, 0, 0, 0], debug=True)

mvs.latitude_lines([2000, 1, 1, 0, 0, 0], debug=True)

mvs.longitude_lines([2000, 1, 1, 0, 0, 0], debug=True)

mvs.magnetic_dipole([2000, 1, 1, 0, 0, 0])

mvs.axis(None, 'x', length_positive=15., length_negative=0)

# TODO: Fix
#mvs.axes(None)


mvs.neutralsheet([2017, 11, 15, 3, 0, 0], coord_sys='GSM',
                      color=[1,0,0,0.5], representation='Wireframe')

mvs.magnetopause(time=[2000, 1, 1, 0, 0, 0], Bz=None, Psw=None, 
                      model='Roelof_Sibeck93', coord_sys='GSM', 
                      color=[0.1,0.8,0.3,0.5],
                      representation='Surface')

mvs.satellite(time_o = '2017-01-01T01:00:00.000Z', 
                  time_f = '2017-01-01T06:00:00.000Z', 
                  satellite_id = 'geotail', coord_sys='GSM', 
                  color=[0,0,0,0.3], tube_radius=0.1,
                  )

mvs.satellite(time_o = '2017-01-01T01:00:00.000Z', 
                  time_f = '2017-01-01T06:00:00.000Z', 
                  satellite_id = 'geotail', coord_sys='GSM', 
                  color=None, tube_radius=0.1, 
                  region_colors = {
                      'D_Msheath' : [0.0,0.0,0.0,0.3],
                      'N_Msheath' : [0.5,0.0,0.0,0.3],
                      'D_Msphere' : [1.0,0.0,0.0,0.3],
                      'N_Msphere' : [1.0,0.5,0.0,0.3],
                      'D_Psphere' : [0.0,1.0,0.0,0.3],
                      'N_Psphere' : [0.0,1.0,0.5,0.3],
                      'Tail_Lobe' : [0.0,0.0,1.0,0.3],
                      'Plasma_Sh' : [1.0,1.0,0.0,0.3],
                      'HLB_Layer' : [0.0,1.0,1.0,0.3],
                      'LLB_Layer' : [1.0,0.0,1.0,0.3],
                      'Intpl_Med' : [1.0,1.0,1.0,0.3]
                      },
                  )

