
# Demo 1
import paraview.simple as pvs
import magnetovis as mvs

mvs.ClearPipeline()
# grid = mvs.GridData()
# mvs.SetRepresentation('Wireframe')
# mvs.SetColor('blue')

from urllib.request import urlretrieve
url = 'http://mag.gmu.edu/git-data/swmfio/3d__var_2_e20190902-041000-000.vtk'
vtkfile = "/tmp/" + url.split("/")[-1]

import os
if not os.path.exists(vtkfile):
  print("Downloading " + url, flush=True)
  urlretrieve(url, vtkfile)

import magnetovis as mvs
batsrus = mvs.BATSRUS(file=vtkfile)

    
# find source
registrationName = list(pvs.GetSources().keys())\
    [list(pvs.GetSources().values()).index(pvs.GetActiveSource())][0]
batsrus_source = pvs.FindSource(registrationName)


mvs.SetTitle("Default")


line = pvs.Line(Point1=[-10.0, 0.0, 0.0], Point2=[-3, 0.0, 0.0], Resolution=9)

fieldlines = mvs.Fieldlines(Input=[batsrus_source, line])

