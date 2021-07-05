from magnetovis import objects2
import paraview.simple as pvs

"""
Usage:
    magnetovis --script=magnetovis_demo2.py
"""

# these are the times and coordinate system of the demo
demo_time = [2015, 1, 1, 0, 0]
demo_coord = 'GSM'

# stylize background
renderView = pvs.GetActiveViewOrCreate('RenderView')
renderView.UseGradientBackground = 1
renderView.Background2 = [0.070, 0.07, 0.47]
renderView.Background =  [0.087, 0.36, 0.49]
renderView = pvs.GetActiveViewOrCreate('RenderView')
renderView.OrientationAxesVisibility = 0

earthDisp, renderView, earthSource = objects2.earth(demo_time, coord_sys=demo_coord)
objects2.screenshot(obj=earthSource)

latDis, renderView, latSource = objects2.latitude_lines(time=demo_time, coord_sys=demo_coord)
latDisTube, renderView, latTubeFilter = objects2.tube(latSource,tube_radius=0.02)
objects2.screenshot(obj=latTubeFilter)
lonDis, renderView, lonSource = objects2.longitude_lines(time=demo_time, coord_sys=demo_coord)
lonDisTue, renderView, lonTubeFilter = objects2.tube(lonSource, tube_radius=0.02)
objects2.screenshot(obj=lonTubeFilter)


yAxisDis, renderView, yAxisSource = objects2.axis(time=demo_time, val='Y', lims=[-15,15],coord_sys=demo_coord)
yDisTube, renderView, yTubeFilter = objects2.tube(yAxisSource, vary_radius='By Scalar', tube_radius=0.05)
objects2.screenshot(obj=yTubeFilter)
xAxisDis, renderView, xAxisSource = objects2.axis(time=demo_time, val='X', lims=[-15,15], coord_sys=demo_coord)
xDisTube, renderView, xTubeFilter = objects2.tube(xAxisSource, vary_radius='By Scalar', tube_radius=0.05)
objects2.screenshot(obj=xTubeFilter)
zAxisDis, renderView, zAxisSource = objects2.axis(time=demo_time, val='Z', lims=[-15,15], coord_sys=demo_coord)
zDisTube, renderView, zTubeFilter = objects2.tube(zAxisSource, vary_radius='By Scalar', tube_radius=0.05)
objects2.screenshot(obj=zTubeFilter)

# objects2.screenshot(fileName='axes')
## have the demo show regular small ticks and then the x,y ticks longer to create a grid, z-axis ticks still small
# try to get the ticks to be a different thickness then the axis 



#objects2.trajectory() # Plot a particle trajectory from Blake's code (not urgent)

neutDisplay, renderView, neutSource = objects2.neutralsheet(time = demo_time, coord_sys=demo_coord)
objects2.screenshot(obj=neutSource)

# Plasmapause does not have a time parameter. 
# TODO: Raise warning that time not being used unless changing coord systems
ppauseDisp, renderView, ppauseSource = objects2.plasmapause(N=25,
                                                            time=[1984,1,1,0,0],
                                                            coord_sys=demo_coord)
conDis, renderView, contourFilter = objects2.contour(ppauseSource, isosurface=[1.5])
objects2.screenshot(obj=contourFilter)

plasShDisp, renderView, plasShSource = objects2.plasmasheet(time = demo_time, coord_sys=demo_coord,)
objects2.screenshot(obj=plasShSource)

mpauseDisplay, renderView, mpauseSource =objects2.magnetopause(time=demo_time, coord_sys=demo_coord)
objects2.screenshot(obj=mpauseSource)

bowDisp, renderView, bowSource = objects2.bowshock(time=demo_time, coord_sys=demo_coord)
objects2.screenshot(obj=bowSource)

satDisp, renderView, satSource = objects2.satellite(time_o = '2005-01-01T00:00:00.000Z', 
                  time_f = '2005-01-06T00:15:00.000Z', 
                  satellite_id = 'geotail', coord_sys=demo_coord,
                  color=None, tube_radius=None,
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
tubeDis, renderView, tubeFilter = objects2.tube(satSource)
objects2.screenshot(obj=tubeFilter)
satDisp, renderView, satSource = objects2.satellite(time_o = '1984-01-01T00:00:00.000Z', 
                  time_f = '1984-01-01T04:00:00.000Z', 
                  satellite_id = 'de1', coord_sys=demo_coord,
                  color=None, tube_radius=None,
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

tubeDis, renderView, tubeFilter = objects2.tube(satSource)
objects2.screenshot(obj=tubeFilter)


# objects2.plane(time=demo_time, val='XY', extend=[[-55,25],[-55,55]], coord_sys=demo_coord)
# objects2.plane(time=demo_time, val='XZ', extend=[[-55,25],[-55,55]], coord_sys=demo_coord)
# objects2.plane(time=demo_time, val='YZ', extend=[[-55,55],[-55,55]], coord_sys=demo_coord)



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
