# trace generated using paraview version 5.9.1

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

MagnetovisParticleTrajectory1 = MagnetovisParticleTrajectory(registrationName="Proton/α=60°/L=2/Dipole")

SetActiveSource(MagnetovisParticleTrajectory1)

renderView1 = GetActiveViewOrCreate('RenderView')

MagnetovisParticleTrajectory1Display = Show(MagnetovisParticleTrajectory1, renderView1, 'GeometryRepresentation')

import magnetovis as mvs

time = (2015, 1, 1, 0, 0, 0)
csys = 'GEO'

mvs.earth(time, coord_sys=csys)

# current camera placement for renderView1
renderView1.CameraPosition = [-2.5499022410923478, -12.677872114404632, 2.2432731004085125]
renderView1.CameraFocalPoint = [0.0003783702850341797, 0.00016391277313232422, 0.0]
renderView1.CameraViewUp = [-0.0140770940904503, 0.17696300455483305, 0.9841168276383119]
renderView1.CameraParallelScale = 3.4194424668122876

MagnetovisParticleTrajectory1Display.AmbientColor = [1.0, 1.0, 0.0]
MagnetovisParticleTrajectory1Display.DiffuseColor = [1.0, 1.0, 0.0]

mvs.latitude_lines(time, coord_sys='GEO')
