#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 12:06:23 2020

@author: Angel
"""

# Execute using ./magnetovis.sh --script=magnetovis_demo.py

from magnetovis import objects

# mvs.earth([2000, 1, 1, 0, 0, 0], debug=True)

# mvs.latitude_lines([2000, 1, 1, 0, 0, 0], debug=True)

# mvs.longitude_lines([2000, 1, 1, 0, 0, 0], debug=True)

# mvs.magnetic_dipole([2000, 1, 1, 0, 0, 0])

# mvs.axis(None, 'x', length_positive=15., length_negative=15.)

# mvs.axes(None)


# mvs.neutralsheet([2017, 11, 15, 3, 0, 0], coord_sys='GSM',
#                       color=[1,0,0,0.5], representation='Wireframe')

mpause_test = False
plasma_sh = False
bowshock_test = False
bowshock_tipsod_test = False
plane = False
satellites = False
demo = True

if demo:
    
    mvs.magnetopause(time=None, Bz=False, Psw=2.04, 
                          model='Sibeck_Lopez_Roelof91', coord_sys='GSE', 
                          color=[0.1,0.8,0.3,0.5],
                          representation='Surface')
    
    mvs.bowshock(time=None,Bz=False, Psw=2.04, 
                      model='Fairfield71',
                      mpause_model='Sibeck_Lopez_Roelof91', coord_sys='GSE', 
                      color=[1,1,0,.5])
    mvs.plasmasheet([2002, 1, 1, 8, 18, 0], coord_sys='GSM',
                          color=[.6,.1,.07,0.5], representation='Surface')
    
    mvs.satellite(time_o = '2000-01-01T10:50:00.000Z', 
                      time_f = '2000-01-06T00:15:00.000Z', 
                      satellite_id = 'geotail', coord_sys='GSE',
                      representation='Point Gaussian',
                      shader_preset='Sphere',
                      color=None, tube_radius=1,
                      region_colors = {
                          'D_Msheath' : [0.0,0.0,0.0,0.7],
                          'N_Msheath' : [0.5,0.0,0.0,0.7],
                          'D_Msphere' : [1.0,0.0,0.0,0.7],
                          'N_Msphere' : [1.0,0.5,0.0,0.7],
                          'D_Psphere' : [0.0,1.0,0.0,0.7],
                          'N_Psphere' : [0.0,1.0,0.5,0.7],
                          'Tail_Lobe' : [0.0,0.0,1.0,0.7],
                          'Plasma_Sh' : [1.0,1.0,0.0,0.7],
                          'HLB_Layer' : [0.0,1.0,1.0,0.7],
                          'LLB_Layer' : [1.0,0.0,1.0,0.7],
                          'Intpl_Med' : [1.0,1.0,1.0,0.7]
                          },
                      )
    
    mvs.plane([2000,1,1,0,0,0],'XY', [[-30,30],[-30,30]])
    mvs.plane([2000,1,1,0,0,0],'XZ', [[-30,30],[-30,30]])
    mvs.plane([2000,1,1,0,0,0],'YZ', [[-30,30],[-30,30]])
    # mvs.axis(None, 'x', length_positive=15., length_negative=15.)
    mvs.earth([2000, 1, 1, 0, 0, 0], debug=True)

if satellites:
    mvs.satellite(time_o = '2000-01-01T10:50:00.000Z', 
                      time_f = '2000-01-06T00:15:00.000Z', 
                      satellite_id = 'geotail', coord_sys='GSE',
                      representation='Point Gaussian',
                      shader_preset='Sphere',
                      color=None, tube_radius=1,
                      region_colors = {
                          'D_Msheath' : [0.0,0.0,0.0,0.7],
                          'N_Msheath' : [0.5,0.0,0.0,0.7],
                          'D_Msphere' : [1.0,0.0,0.0,0.7],
                          'N_Msphere' : [1.0,0.5,0.0,0.7],
                          'D_Psphere' : [0.0,1.0,0.0,0.7],
                          'N_Psphere' : [0.0,1.0,0.5,0.7],
                          'Tail_Lobe' : [0.0,0.0,1.0,0.7],
                          'Plasma_Sh' : [1.0,1.0,0.0,0.7],
                          'HLB_Layer' : [0.0,1.0,1.0,0.7],
                          'LLB_Layer' : [1.0,0.0,1.0,0.7],
                          'Intpl_Med' : [1.0,1.0,1.0,0.7]
                          },
                      )

    

if mpause_test:
    
    # checking Sibeck 91 combos - all passed 
    mvs.magnetopause(time=None, Bz=False, Psw=2.04, 
                          model='Sibeck_Lopez_Roelof91', coord_sys='GSE', 
                          color=[0.1,0.8,0.3,0.5],
                          representation='Surface')
    # mvs.magnetopause(time=None, Bz=2, Psw=False, 
    #                       model='Sibeck_Lopez_Roelof91', coord_sys='GSE', 
    #                       color=[0.1,0.8,0.3,0.5],
    #                       representation='Surface')
    # mvs.magnetopause(time=[2002,1,1,20,2,0], Bz=False, Psw=None, 
    #                       model='Sibeck_Lopez_Roelof91', coord_sys='GSE', 
    #                       color=[0.1,0.8,0.3,0.5], 
    #                       representation='Surface')
    # mvs.magnetopause(time=[2002,1,1,20,2,0], Bz=None, Psw=False, 
    #                       model='Sibeck_Lopez_Roelof91', coord_sys='GSE', 
    #                       color=[0.1,0.8,0.3,0.5], 
    #                       representation='Surface')
    
    # # checking non-sibeck 91 work - all passed 
    # mvs.magnetopause(time=None, Bz=3, Psw=2.04, 
    #                       model='Roelof_Sibeck93', coord_sys='GSE', 
    #                       color=[0.1,0.8,0.3,0.5],
    #                       representation='Surface')
    # mvs.magnetopause(time=[2002,1,1,20,2,0], Bz=2, Psw=None, 
    #                       model='Roelof_Sibeck93', coord_sys='GSE', 
    #                       color=[0.1,0.8,0.3,0.5], 
    #                       representation='Surface')
    # mvs.magnetopause(time=[2002,1,1,20,2,0], Bz=None, Psw=5, 
    #                       model='Roelof_Sibeck93', coord_sys='GSE', 
    #                       color=[0.1,0.8,0.3,0.5], 
    #                       representation='Surface')
    # mvs.magnetopause(time=[2002,1,1,20,2,0], Bz=None, Psw=None, 
    #                       model='Roelof_Sibeck93', coord_sys='GSE', 
    #                       color=[0.1,0.8,0.3,0.5], 
    #                       representation='Surface')



if plane:
    # mvs.plane([2000,1,1,0,0,0],'XZ', extend=[[10,15],[4,15]])
    mvs.plane([2000,1,1,0,0,0],'XZ')



if bowshock_tipsod_test:
    # if rotation = -4.82 and trans = (0, 0.3131, 0)
    # crossing is around 13:00 with translation
    # 
    '''
    according to SSCWEB the bowshock surface occurs at
        dBowShk                 10:51
        Spacecraft Region       10:11
    according to Tipsod the bowshock surface occurs at 10:55 - 11:10 
        
        
    NOTE: all these translations were with respect to the x-axis orientation.
    if rot = -4.82 , trans = (0, 0.3131, 0)
        crossing around 13
    if rot = -4.82, trans = None
        crossing around 11:50
    if rot = -4.82, trans = (0, -0.3131, 0)
        crossing around 10:56               BEST MATCH TO dBowShk
    if rot = -4, trans = (0, 0.3131, 0)
        corssing around 12:00
    if rot = -4, trans = (0, 0, 0)
        crossing around 11:06               BEST MATCH TO TIPSOD
    if rot = -4, trans = (0, -0.3131, 0)
        crossing around 10:16               BEST MATCH TO SPACECRAFT REGION
    if rot = 0 , trans = (0,  0.3131, 0)
        crossing around  9:06
    if rot = 0 , trans = (0,  0, 0)
        crossing around  8:26
    if rot = 0 , trans = (0, -0.3131, 0)
        crossing around 7:49
    if rot = 4,  trans = (0, 0.3131, 0)
        crossing around 7:10
    if rot = 4,  trans = (0, 0, 0)
        crossing way before 7
    if rot = 4,  trans = (0, -0.3131, 0)
        crossing around way before 7
        
    '''
    # 2000 Psw Bz = None
    
    mvs.bowshock(time=None, Bz=False, Psw=2.04, 
                     model='Fairfield71', coord_sys='GSE', 
                     mpause_model='Sibeck_Lopez_Roelof91',
                     color=[0.1,0.8,0.3,0.7], 
                     representation='Surface')
    
    mvs.satellite(time_o = '2002-01-02T10:50:00.000Z', 
                      time_f = '2002-01-02T11:15:00.000Z', 
                      satellite_id = 'cluster1', coord_sys='GSE',
                      representation='Point Gaussian',
                      shader_preset='Sphere',
                      color=None, tube_radius=None,
                      region_colors = {
                          'D_Msheath' : [0.0,0.0,0.0,0.7],
                          'N_Msheath' : [0.5,0.0,0.0,0.7],
                          'D_Msphere' : [1.0,0.0,0.0,0.7],
                          'N_Msphere' : [1.0,0.5,0.0,0.7],
                          'D_Psphere' : [0.0,1.0,0.0,0.7],
                          'N_Psphere' : [0.0,1.0,0.5,0.7],
                          'Tail_Lobe' : [0.0,0.0,1.0,0.7],
                          'Plasma_Sh' : [1.0,1.0,0.0,0.7],
                          'HLB_Layer' : [0.0,1.0,1.0,0.7],
                          'LLB_Layer' : [1.0,0.0,1.0,0.7],
                          'Intpl_Med' : [1.0,1.0,1.0,0.7]
                          },
                      )





if bowshock_test:
    # change unused value Psw or Bz = False -> this means not used. 
    # check to make sure Bz is a boolean. Zero creates problem - interpreted as boolean
    
    # checking all bowshock combos - passed
    mvs.bowshock(time=None,Bz=False, Psw=2.04, 
                      model='Fairfield71',
                      mpause_model='Sibeck_Lopez_Roelof91', coord_sys='GSE', 
                      color=[1,1,0,.5])
    
    # mvs.bowshock(time=None,Bz=-2, Psw=False, 
    #                   model='Fairfield71',
    #                   mpause_model='Sibeck_Lopez_Roelof91', coord_sys='GSE', 
    #                   color=[1,1,0,1])    
    
    # mvs.bowshock(time=[2002,1,1,20,2,0],Bz=0, Psw=False, 
    #                   model='Fairfield71', 
    #                   mpause_model='Sibeck_Lopez_Roelof91', coord_sys='GSE', 
    #                   color=[1,1,0,1])
    
    # mvs.bowshock(time=[2002,1,1,20,2,0],Bz=False, Psw=None, 
    #                   model='Fairfield71',
    #                   mpause_model='Sibeck_Lopez_Roelof91', coord_sys='GSE', 
    #                   color=[1,1,0,1])




if plasma_sh:
    mvs.plasmasheet([2002, 1, 1, 8, 18, 0], coord_sys='GSM',
                          color=[1,0,0,0.5], representation='Wireframe')

    mvs.satellite(time_o = '2002-01-01T06:47:00.000Z', 
                      time_f = '2002-01-01T08:16:00.000Z', 
                      satellite_id = 'cluster1', coord_sys='GSM',
                      representation='Point Gaussian',
                      shader_preset='Sphere',
                      color=None, tube_radius=.5,
                      region_colors = {
                          'D_Msheath' : [0.0,0.0,0.0,0.7],
                          'N_Msheath' : [0.5,0.0,0.0,0.7],
                          'D_Msphere' : [1.0,0.0,0.0,0.7],
                          'N_Msphere' : [1.0,0.5,0.0,0.7],
                          'D_Psphere' : [0.0,1.0,0.0,0.7],
                          'N_Psphere' : [0.0,1.0,0.5,0.7],
                          'Tail_Lobe' : [0.0,0.0,1.0,0.7],
                          'Plasma_Sh' : [1.0,1.0,0.0,0.7],
                          'HLB_Layer' : [0.0,1.0,1.0,0.7],
                          'LLB_Layer' : [1.0,0.0,1.0,0.7],
                          'Intpl_Med' : [1.0,1.0,1.0,0.7]
                          },
                      )
    
    mvs.satellite(time_o = '2017-01-01T01:22:00.000Z', 
                      time_f = '2017-01-01T01:37:00.000Z', 
                      satellite_id = 'aerocube6a', coord_sys='GSM',
                      representation='Point Gaussian',
                      shader_preset='Sphere',
                      color=None, tube_radius=.5,
                      region_colors = {
                          'D_Msheath' : [0.0,0.0,0.0,0.7],
                          'N_Msheath' : [0.5,0.0,0.0,0.7],
                          'D_Msphere' : [1.0,0.0,0.0,0.7],
                          'N_Msphere' : [1.0,0.5,0.0,0.7],
                          'D_Psphere' : [0.0,1.0,0.0,0.7],
                          'N_Psphere' : [0.0,1.0,0.5,0.7],
                          'Tail_Lobe' : [0.0,0.0,1.0,0.7],
                          'Plasma_Sh' : [1.0,1.0,0.0,0.7],
                          'HLB_Layer' : [0.0,1.0,1.0,0.7],
                          'LLB_Layer' : [1.0,0.0,1.0,0.7],
                          'Intpl_Med' : [1.0,1.0,1.0,0.7]
                          },
                      )
    
    mvs.satellite(time_o = '2008-01-01T00:39:00.000Z', 
                      time_f = '2008-01-01T00:58:00.000Z', 
                      satellite_id = 'aim', coord_sys='GSM',
                      representation='Point Gaussian',
                      shader_preset='Sphere',
                      color=None, tube_radius=.5,
                      region_colors = {
                          'D_Msheath' : [0.0,0.0,0.0,0.7],
                          'N_Msheath' : [0.5,0.0,0.0,0.7],
                          'D_Msphere' : [1.0,0.0,0.0,0.7],
                          'N_Msphere' : [1.0,0.5,0.0,0.7],
                          'D_Psphere' : [0.0,1.0,0.0,0.7],
                          'N_Psphere' : [0.0,1.0,0.5,0.7],
                          'Tail_Lobe' : [0.0,0.0,1.0,0.7],
                          'Plasma_Sh' : [1.0,1.0,0.0,0.7],
                          'HLB_Layer' : [0.0,1.0,1.0,0.7],
                          'LLB_Layer' : [1.0,0.0,1.0,0.7],
                          'Intpl_Med' : [1.0,1.0,1.0,0.7]
                          },
                      )
    
    mvs.satellite(time_o = '2017-01-01T20:08:00.000Z', 
                      time_f = '2017-01-01T20:59:00.000Z', 
                      satellite_id = 'themisa', coord_sys='GSM',
                      representation='Point Gaussian',
                      shader_preset='Sphere',
                      color=None, tube_radius=.5,
                      region_colors = {
                          'D_Msheath' : [0.0,0.0,0.0,0.7],
                          'N_Msheath' : [0.5,0.0,0.0,0.7],
                          'D_Msphere' : [1.0,0.0,0.0,0.7],
                          'N_Msphere' : [1.0,0.5,0.0,0.7],
                          'D_Psphere' : [0.0,1.0,0.0,0.7],
                          'N_Psphere' : [0.0,1.0,0.5,0.7],
                          'Tail_Lobe' : [0.0,0.0,1.0,0.7],
                          'Plasma_Sh' : [1.0,1.0,0.0,0.7],
                          'HLB_Layer' : [0.0,1.0,1.0,0.7],
                          'LLB_Layer' : [1.0,0.0,1.0,0.7],
                          'Intpl_Med' : [1.0,1.0,1.0,0.7]
                          },
                      )
    
    mvs.satellite(time_o = '2017-01-23T08:00:00.000Z', 
                      time_f = '2017-01-23T09:12:00.000Z', 
                      satellite_id = 'geotail', coord_sys='GSM',
                      representation='Point Gaussian',
                      shader_preset='Sphere',
                      color=None, tube_radius=.5,
                      region_colors = {
                          'D_Msheath' : [0.0,0.0,0.0,0.7],
                          'N_Msheath' : [0.5,0.0,0.0,0.7],
                          'D_Msphere' : [1.0,0.0,0.0,0.7],
                          'N_Msphere' : [1.0,0.5,0.0,0.7],
                          'D_Psphere' : [0.0,1.0,0.0,0.7],
                          'N_Psphere' : [0.0,1.0,0.5,0.7],
                          'Tail_Lobe' : [0.0,0.0,1.0,0.7],
                          'Plasma_Sh' : [1.0,1.0,0.0,0.7],
                          'HLB_Layer' : [0.0,1.0,1.0,0.7],
                          'LLB_Layer' : [1.0,0.0,1.0,0.7],
                          'Intpl_Med' : [1.0,1.0,1.0,0.7]
                          },
                      )


