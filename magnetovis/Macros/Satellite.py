from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

MagnetovisSatellite1 = MagnetovisSatellite()

SetActiveSource(MagnetovisSatellite1)

renderView1 = GetActiveViewOrCreate('RenderView')

MagnetovisSatellite1Display = Show(MagnetovisSatellite1, renderView1, 'GeometryRepresentation')

ResetCamera()