from magnetovis import objects2, objects
import paraview.simple as pvs
"""
This script shows a demonstration of magnetovis if ran with: demo = True

Instructions for running 
From the terminal run command:
    PYTHONPATH=/.../site-packages:. paraview --script=magnetovis_demo2.py

"""

# these are the times and coordinate system of the demo
demo_time = [2005, 1, 1, 0, 0]
demo_coord = 'GSM'


demo = True
axis = False
mpause = False
bowshock = False
satellite_path = False
neutralsheet = False
plasmasheet = False


if demo:
    objects2.neutralsheet(time = demo_time, coord_sys=demo_coord)
    objects2.plasmasheet(time = demo_time, coord_sys=demo_coord)
    objects2.magnetopause(time=demo_time,
                          model='Roelof_Sibeck93', coord_sys=demo_coord, 
                          color=[.5,.5,0.3,0.5],
                          representation='Surface')
    
    objects2.bowshock(time=demo_time, color=[0,0,1,.5], coord_sys=demo_coord)
    
    objects2.pro_satellite(time_o = '2005-01-01T00:00:00.000Z', 
                      time_f = '2005-01-06T00:15:00.000Z', 
                      satellite_id = 'geotail', coord_sys=demo_coord,
                      representation='Surface',
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
                          }
                      )
    
    objects2.earth(demo_time, debug=True, coord_sys='GSM')
    objects2.axis(time=demo_time, val='Y', lims=[-55,55],coord_sys=demo_coord)
    objects2.axis(time=demo_time, val='X', lims=[-55,25], coord_sys=demo_coord)
    objects2.axis(time=demo_time, val='Z', lims=[-55,55], coord_sys=demo_coord)
    objects2.plane(time=demo_time, val='XY', extend=[[-55,25],[-55,55]], coord_sys=demo_coord)
    objects2.plane(time=demo_time, val='XZ', extend=[[-55,25],[-55,55]], coord_sys=demo_coord)
    objects2.plane(time=demo_time, val='YZ', extend=[[-55,55],[-55,55]], coord_sys=demo_coord)

if axis:
    objects2.axis(time=demo_time, val='X', coord_sys=demo_coord)
    objects2.axis(time=demo_time, val='Y', coord_sys=demo_coord)
    objects2.axis(time=demo_time, val='Z', coord_sys=demo_coord)


if plasmasheet:
    objects2.plasmasheet(time = [2000,1,1,1,1])

if neutralsheet:
    objects2.neutralsheet(time = [2000,1,1,1,1])
    objects.neutralsheet(time=[2000,1,1,1,1])
    objects2.neutralsheet(time = None, psi=28)
    objects.neutralsheet(time=None, psi=28)

if mpause:
    objects2.magnetopause(time=None, Bz=0, Psw=2.04, 
                          model='Shue97', coord_sys='GSE', 
                          color=[.5,.5,0.3,0.5],
                          representation='Surface')
if bowshock:
    objects2.bowshock(Bz = 0, Psw=2, color=[0,0,1,.5])
    

renderView = pvs.GetActiveViewOrCreate('RenderView')
renderView.UseGradientBackground = 1
renderView.Background2 = [0.07023727779049363, 0.07129015030136568, 0.471976806286717]
renderView.Background = [0.0865796902418555, 0.35515373464560923, 0.48921950102998396]

if satellite_path:

    objects2.pro_satellite(time_o = '2005-01-01T10:50:00.000Z', 
                      time_f = '2005-01-06T00:15:00.000Z', 
                      satellite_id = 'aura', coord_sys='GSE',
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
                          }
                      )
