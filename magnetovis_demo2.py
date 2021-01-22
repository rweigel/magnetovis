from magnetovis import objects2
import paraview.simple as pvs

"""
Usage:
    magnetovis --script=magnetovis_demo2.py
"""

# these are the times and coordinate system of the demo
demo_time = [2015, 1, 1, 0, 0]
demo_coord = 'GSM'

objects2.cutplane() # Urgent: plot cutplane of rho from SWMF (any run, any time) - make same size as XZ plane plotted below.

objects2.trajectory() # Plot a particle trajectory from Blake's code (not urgent)

objects2.neutralsheet(time = demo_time, coord_sys=demo_coord)
objects2.plasmasheet(time = demo_time, coord_sys=demo_coord)
objects2.magnetopause(time=demo_time, coord_sys=demo_coord)

objects2.bowshock(time=demo_time, coord_sys=demo_coord)

objects2.satellite(time_o = '2005-01-01T00:00:00.000Z', 
                  time_f = '2005-01-06T00:15:00.000Z', 
                  satellite_id = 'geotail', coord_sys=demo_coord,
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

objects2.earth(demo_time, coord_sys=demo_coord)
objects2.latitude_lines(time=demo_time, coord_sys=demo_coord)
objects2.longitude_lines(time=demo_time, coord_sys=demo_coord)
objects2.axis(time=demo_time, val='Y', lims=[-55,55],coord_sys=demo_coord)
objects2.axis(time=demo_time, val='X', lims=[-55,25], coord_sys=demo_coord)
objects2.axis(time=demo_time, val='Z', lims=[-55,55], coord_sys=demo_coord)
objects2.plane(time=demo_time, val='XY', extend=[[-55,25],[-55,55]], coord_sys=demo_coord)
objects2.plane(time=demo_time, val='XZ', extend=[[-55,25],[-55,55]], coord_sys=demo_coord)
objects2.plane(time=demo_time, val='YZ', extend=[[-55,55],[-55,55]], coord_sys=demo_coord)

# stylize background
renderView = pvs.GetActiveViewOrCreate('RenderView')
renderView.UseGradientBackground = 1
renderView.Background2 = [0.07023727779049363, 0.07129015030136568, 0.471976806286717]
renderView.Background = [0.0865796902418555, 0.35515373464560923, 0.48921950102998396]

