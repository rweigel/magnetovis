from magnetovis import objects2
import paraview.simple as pvs

"""
Usage:
    magnetovis --script=magnetovis_demo2.py
"""

# these are the times and coordinate system of the demo
demo_time = [2015, 1, 1, 0, 0]
demo_coord = 'GSM'


#objects2.trajectory() # Plot a particle trajectory from Blake's code (not urgent)

neutDisplay, renderView, neutSource =  objects2.neutralsheet(time = demo_time, coord_sys=demo_coord)
objects2.screenshot(obj=neutSource)

plasShDisp, renderView, plasShSource = objects2.plasmasheet(time = demo_time, coord_sys=demo_coord)
objects2.screenshot(obj=plasShSource)

mpauseDisplay, renderView, mpauseSource =objects2.magnetopause(time=demo_time, coord_sys=demo_coord)
objects2.screenshot(obj=mpauseSource)

bowDisp, renderView, bowSource = objects2.bowshock(time=demo_time, coord_sys=demo_coord)
objects2.screenshot(obj=bowSource)

satDisp, renderView, satSource = objects2.satellite(time_o = '2005-01-01T00:00:00.000Z', 
                  time_f = '2005-01-06T00:15:00.000Z', 
                  satellite_id = 'geotail', coord_sys=demo_coord,
                  color=None, tube_radius=1,
                  region_colors = {
                      'D_Msheath' : (230./255, 25./255,  75./255,  0.7), # red
                      'N_Msheath' : (245./255, 130./255, 48./255,  0.7), # orange
                      'D_Msphere' : (255./255, 255./255, 25./255,  0.7), # yellow
                      'N_Msphere' : (220./255, 190./255, 255./255, 0.7), # lavender
                      'D_Psphere' : (60./255,  180./255, 75./255,  0.7), # green
                      'N_Psphere' : (70./255,  240./255, 240./255, 0.7), # cyan
                      'Tail_Lobe' : (0,        130./255, 200./255, 0.7), # blue
                      'Plasma_Sh' : (145./255, 30./255,  180./255, 0.7), # purple
                      'HLB_Layer' : (240./255, 50./255,  230./255, 0.7), # magenta
                      'LLB_Layer' : (128./255, 128./255, 128./255, 0.7), # grey
                      'Intpl_Med' : (255./255, 255./255, 255./255, 0.7)  # white
                      }
                  )
objects2.screenshot(obj=satSource)

earthDisp, renderView, earthSource = objects2.earth(demo_time, coord_sys=demo_coord)
objects2.screenshot(obj=earthSource)


# #objects2.latitude_lines(time=demo_time, coord_sys=demo_coord)
# #objects2.longitude_lines(time=demo_time, coord_sys=demo_coord)
# objects2.axis(time=demo_time, val='Y', lims=[-55,55],coord_sys=demo_coord)
# objects2.axis(time=demo_time, val='X', lims=[-55,25], coord_sys=demo_coord)
# objects2.axis(time=demo_time, val='Z', lims=[-55,55], coord_sys=demo_coord)
# objects2.plane(time=demo_time, val='XY', extend=[[-55,25],[-55,55]], coord_sys=demo_coord)
# #objects2.plane(time=demo_time, val='XZ', extend=[[-55,25],[-55,55]], coord_sys=demo_coord)
# objects2.plane(time=demo_time, val='YZ', extend=[[-55,55],[-55,55]], coord_sys=demo_coord)

# stylize background
renderView = pvs.GetActiveViewOrCreate('RenderView')
renderView.UseGradientBackground = 1
renderView.Background2 = [0.07023727779049363, 0.07129015030136568, 0.471976806286717]
renderView.Background = [0.0865796902418555, 0.35515373464560923, 0.48921950102998396]

if False:

  renderView = pvs.GetActiveViewOrCreate('RenderView')

  for name_id, pObject in pvs.GetSources().items():
      clip = pvs.Clip(Input=pObject)
      clip.ClipType= 'Plane'
      clip.Invert = 0
      clip.ClipType.Origin = [0,-1,0]
      clip.ClipType.Normal = [0,1,0]
      clipDisplay = pvs.Show(clip, renderView)
      
      pvs.Hide3DWidgets(proxy=clip.ClipType)
      pvs.Hide(pObject)
      
  renderView.Update()

# objects2.cutplane()

screenshot=False
if screenshot:
  pvs.savescreenshot(renderView, 'path.png', 'resolution')
