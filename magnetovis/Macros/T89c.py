# trace generated using paraview version 5.9.1

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'MagnetovisDipole'
magnetovisT89c = MagnetovisT89c(registrationName='MagnetovisT89c')
