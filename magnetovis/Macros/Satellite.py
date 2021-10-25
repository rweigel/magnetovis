from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

MagnetovisSatellite1 = MagnetovisSatellite()

SetActiveSource(MagnetovisSatellite1)

renderView1 = GetActiveViewOrCreate('RenderView')
renderView1.ResetCamera()

MagnetovisSatellite1Display = Show(MagnetovisSatellite1, renderView1, 'GeometryRepresentation')

#from magnetovis.Satellite.Axis import Display
#MagnetovisSatellite1Display = Display(MagnetovisSatellite1Display, MagnetovisSatellite1Display, renderView1)
