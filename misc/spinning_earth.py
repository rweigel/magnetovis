# creates a spinning Earth
import paraview.simple as pvs

# create a new 'Programmable Source'
earth = pvs.ProgrammableSource(registrationName='earth')

# Properties modified on earth
earth.OutputDataSetType = 'vtkStructuredGrid'
earth.Script = """
from magnetovis.util import time2datetime
from datetime import timedelta


def createvtk(output, time, coord_sys,
                Nt=100, Np=100):

    import numpy as np
    import vtk
    from vtk.numpy_interface import dataset_adapter as dsa
    from hxform import hxform as hx

    executive = self.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    exts = [executive.UPDATE_EXTENT().Get(outInfo, i) for i in range(6)]
    dims = [exts[1]+1, exts[3]+1, exts[5]+1]

    R = 1.
    Nt, Np = 100, 100
    theta = np.linspace(0., np.pi, Nt)
    phi = np.linspace(0.,2.*np.pi, Np)

    B1, B2 = np.meshgrid(phi,theta)
    B1 = B1.flatten(order='C')
    B2 = B2.flatten(order='C')

    PI = np.pi*np.ones((B1.size,))
    x = R*np.cos(B1+PI)*np.sin(B2)
    y = R*np.sin(B1+PI)*np.sin(B2)
    z = R*np.cos(B2)
    points = np.column_stack((x,y,z))
    if coord_sys != 'GEO':
        points = hx.transform(points, time, 'GEO', coord_sys)
    pvtk = dsa.numpyTovtkDataArray(points)
    pts = vtk.vtkPoints()
    pts.Allocate(points.shape[0])
    pts.SetData(pvtk)
    output.SetPoints(pts)

    normPhi = np.linspace(0.,1.,Np)
    normTheta = np.flipud(np.linspace(0.,1.,Nt))
    u, v = np.meshgrid(normPhi, normTheta)
    u = u.flatten(order='C')
    v = v.flatten(order='C')
    UV = np.column_stack((u,v))

    fvtk = dsa.numpyTovtkDataArray(UV)
    fvtk.SetName('Angular Coords for PNG')
    output.GetPointData().AddArray(fvtk)

    output.SetExtent(exts)

outInfo = self.GetOutputInformation(0)
if outInfo.Has(vtk.vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP()):
  day_delta = outInfo.Get(vtk.vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP())
else:
  day_delta = 0

coord_sys = 'GEI'
start = (2015, 1, 1, 0, 0, 0)
time = list((time2datetime(start) + timedelta(days=day_delta)).timetuple())[:6]

createvtk(output, time, coord_sys)
"""
earth.ScriptRequestInformation = """
executive = self.GetExecutive()
outInfo = executive.GetOutputInformation(0)
dims = [100,100,1]# Nt, Np, 1
outInfo.Set(executive.WHOLE_EXTENT(), 0, dims[0]-1, 0, dims[1]-1, 0, dims[2]-1)

timeSteps = range(100)
timeRange = [timeSteps[0], timeSteps[-1]]
outInfo.Set(vtk.vtkStreamingDemandDrivenPipeline.TIME_RANGE(), timeRange, 2)
outInfo.Set(vtk.vtkStreamingDemandDrivenPipeline.TIME_STEPS(), timeSteps, len(timeSteps))
"""

# get active view
renderView = pvs.GetActiveViewOrCreate('RenderView')

# show data in view
earthDisplay = pvs.Show(earth, renderView, 'StructuredGridRepresentation')

# trace defaults for the display properties.
earthDisplay.Representation = 'Surface'
earthDisplay.ColorArrayName = [None, '']
earthDisplay.SelectTCoordArray = 'Angular Coords for PNG'
earthDisplay.SelectNormalArray = 'None'
earthDisplay.SelectTangentArray = 'None'
earthDisplay.ScaleFactor = 0.2

# reset view to fit data
renderView.ResetCamera()

# update the view to ensure updated data information
renderView.Update()

# add texture
import os
import tempfile
from hapiclient.util import urlretrieve

topo_url='http://mag.gmu.edu/git-data/magnetovis/topography/world.topo.2004{0:02d}.3x5400x2700.png'
time = (2015, 1, 1, 0, 0, 0)
urlPNG = topo_url.format(time[1])

out_dir=tempfile.gettempdir()
filePNG = os.path.join(out_dir, os.path.split(topo_url)[1].format(time[1]))
urlretrieve(urlPNG, filePNG)
earth2 = pvs.CreateTexture(filePNG)

# change texture
earthDisplay.Texture = earth2







###
