def OutputDataSetType():

    return "vtkStructuredGrid"


def ScriptRequestInformation(self, dimensions=None):

    import magnetovis as mvs

    if dimensions is None:
        import magnetovis as mvs
        function = "magnetovis.Sources.Earth.Script"
        kwargs = mvs.extract.extract_kwargs(function)
        dimensions = [kwargs['Nt'], kwargs['Np']]
    
    dimensions.append(1)
    return mvs.Sources.GridData.ScriptRequestInformation(self, dimensions=dimensions)


def Script(output, time="2001-01-01", coord_sys="GSM", R=1, Nt=180, Np=180):

    # See also
    # https://pvgeo.org/_modules/PVGeo/model_build/earth.html

    from magnetovis.util import time2datetime
    from datetime import timedelta

    import vtk
    import paraview.simple as pvs
    import numpy as np
    from vtk.numpy_interface import dataset_adapter as dsa

    # Needed for UniformGrid, RectilinearGrid, and StructuredGrid.
    # See explanation in GridData.py
    output.SetExtent([0, Nt-1, 0, Np-1, 0, 0])

    theta = np.linspace(0., np.pi, Nt)
    phi = np.linspace(0., 2.*np.pi, Np)

    B1, B2 = np.meshgrid(phi, theta)
    B1 = B1.flatten(order='C')
    B2 = B2.flatten(order='C')

    PI = np.pi*np.ones((B1.size,))
    x = R*np.cos(B1+PI)*np.sin(B2)
    y = R*np.sin(B1+PI)*np.sin(B2)
    z = R*np.cos(B2)
    points = np.column_stack((x,y,z))

    if coord_sys != 'GEO':
        from hxform import hxform as hx
        points = hx.transform(points, mvs.util.iso2ints(time), 'GEO', 'GSM', lib='cxform')
        points = hx.transform(points, mvs.util.iso2ints(time), 'GSM', coord_sys, lib='cxform')

    pvtk = dsa.numpyTovtkDataArray(points)
    pts = vtk.vtkPoints()
    pts.Allocate(points.shape[0])
    pts.SetData(pvtk)
    output.SetPoints(pts)

    normPhi = np.linspace(0., 1., Np)
    normTheta = np.flipud(np.linspace(0., 1., Nt))
    u, v = np.meshgrid(normPhi, normTheta)
    u = u.flatten(order='C')
    v = v.flatten(order='C')
    UV = np.column_stack((u,v))

    fvtk = dsa.numpyTovtkDataArray(UV)
    fvtk.SetName('TCoordArray')
    output.GetPointData().AddArray(fvtk)

    mvs.ProxyInfo.SetInfo(output, locals())


def DefaultRegistrationName(**kwargs):

    import magnetovis as mvs

    return "{}/{}/{}" \
                .format("Earth", mvs.util.trim_iso(kwargs['time']), kwargs['coord_sys'])

def SetDisplayProperties(source, view=None, **kwargs):

    import os
    import urllib3
    import shutil
    import tempfile
    import magnetovis as mvs
    import paraview.simple as pvs

    time = source.GetProperty('time')
    png_url = 'http://mag.gmu.edu/git-data/magnetovis/topography/world.topo.2004{}.3x5400x2700.png'
    png_url = png_url.format(time[5:7])

    try:
        png_file = mvs.util.dlfile(png_url)
        display = pvs.GetDisplayProperties(proxy=source, view=view)
        display.SelectTCoordArray = 'TCoordArray'
        display.Texture = pvs.CreateTexture(png_file)
    except:
        mvs.SetTitle("\n\n" + "Could not download\n" + png_url, display={"FontSize": 12, "Justification": "Left"})
