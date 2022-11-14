def OutputDataSetType():

    return "vtkStructuredGrid"


def ScriptRequestInformation(self, dimensions=None):

    import magnetovis as mvs

    if dimensions is None:
        import magnetovis as mvs
        function = "magnetovis.Sources.Earth.Script"
        kwargs = mvs.extract.extract_kwargs(function)
        dimensions = [kwargs['ThetaResolution'], kwargs['PhiResolution']]
    
    dimensions.append(1)
    return mvs.Sources.GridData.ScriptRequestInformation(self, dimensions=dimensions)


def Script(time="2001-01-01", coord_sys="GSM", coord_sys_view=None,
            style="map", Radius=1.0, ThetaResolution=180, PhiResolution=180):

    import vtk
    import magnetovis as mvs

    # TODO: 1. This implementation seems overly complex. Can a 
    #          programmable calculator be used?
    #       2. Assert {Theta, Phi}Resolution > 3
    # See also
    # https://pvgeo.org/_modules/PVGeo/model_build/earth.html

    # By G. Quarisima

    from magnetovis.util import time2datetime
    from datetime import timedelta

    import numpy as np
    import paraview.simple as pvs
    from vtk.numpy_interface import dataset_adapter as dsa

    # Needed for UniformGrid, RectilinearGrid, and StructuredGrid.
    # See explanation in GridData.py
    output.SetExtent([0, ThetaResolution-1, 0, PhiResolution-1, 0, 0])

    theta = np.linspace(0., np.pi, ThetaResolution)
    phi = np.linspace(0., 2.*np.pi, PhiResolution)

    B1, B2 = np.meshgrid(phi, theta)
    B1 = B1.flatten(order='C')
    B2 = B2.flatten(order='C')

    PI = np.pi*np.ones((B1.size,))
    x = Radius*np.cos(B1+PI)*np.sin(B2)
    y = Radius*np.sin(B1+PI)*np.sin(B2)
    z = Radius*np.cos(B2)
    points = np.column_stack((x,y,z))

    if coord_sys != 'GEO':
        from hxform import hxform as hx
        points_gsm = hx.transform(points, mvs.util.iso2ints(time), 'GEO', 'GSM', lib='cxform')
        # req = requested coordinate system
        points_req = hx.transform(points_gsm, mvs.util.iso2ints(time), 'GSM', coord_sys, lib='cxform')
        points_hee = hx.transform(points_gsm, mvs.util.iso2ints(time), 'GEO', "HEE", lib='cxform')
    else:
        points_req = points
        points_hee = points

    vtkDataArray = dsa.numpyTovtkDataArray(points_req)
    vtkPoints = vtk.vtkPoints()
    vtkPoints.Allocate(points_req.shape[0])
    vtkPoints.SetData(vtkDataArray)
    output.SetPoints(vtkPoints)

    normals = dsa.numpyTovtkDataArray(points_hee/Radius)
    normals.SetName('Normals')
    output.GetPointData().AddArray(normals)

    normPhi = np.linspace(0., 1., PhiResolution)
    normTheta = np.flipud(np.linspace(0., 1., ThetaResolution))
    u, v = np.meshgrid(normPhi, normTheta)
    u = u.flatten(order='C')
    v = v.flatten(order='C')
    UV = np.column_stack((u, v))

    fvtk = dsa.numpyTovtkDataArray(UV)
    fvtk.SetName('TCoordArray')
    output.GetPointData().AddArray(fvtk)


def DefaultRegistrationName(**kwargs):

    import magnetovis as mvs

    return "{}/{}/{}" \
                .format("Earth", mvs.util.trim_iso(kwargs['time']), kwargs['coord_sys'])


def SetPresentationProperties(source, view=None, **kwargs):

    import paraview.simple as pvs

    style = source.GetProperty('style')
    if style == "daynight":
        sourceDisplay = pvs.GetDisplayProperties(source, view=view)
        pvs.ColorBy(sourceDisplay, ('POINTS', 'Normals', 'Magnitude'))
        sourceDisplay.RescaleTransferFunctionToDataRange(True, False)
        sourceDisplay.SetScalarBarVisibility(view, False)

        normalsLUT = pvs.GetColorTransferFunction('Normals')
        normalsPWF = pvs.GetOpacityTransferFunction('Normals')

        pvs.ColorBy(sourceDisplay, ('POINTS', 'Normals', 'X'))

        normalsLUT.ApplyPreset('X Ray', True)
        normalsLUT.NumberOfTableValues = 2
        normalsLUT.InvertTransferFunction()
        view.Update()
        return

    import os
    import urllib3
    import shutil
    import tempfile
    import magnetovis as mvs

    time = source.GetProperty('time')

    if False:
        png_url = 'http://mag.gmu.edu/git-data/magnetovis/topography/world.topo.2004{}.3x5400x2700.png'
        png_url = png_url.format(time[5:7])

        try:
            png_file = mvs.util.dlfile(png_url)
        except:
            mvs.SetTitle("\n\n" + "Could not download\n" + png_url, display={"FontSize": 12, "Justification": "Left"})
    else:
        mvs_dir = os.path.dirname(os.path.abspath(mvs.__file__))
        png_file = os.path.join(mvs_dir,'Sources','Earth.png')

    display = pvs.GetDisplayProperties(proxy=source, view=view)
    display.SelectTCoordArray = 'TCoordArray'
    display.Texture = pvs.CreateTexture(png_file)

    # Set Sphere color; if not set, image is dimmed. Not sure why
    # given that texture is applied over sphere.
    mvs.SetColor('white', proxy=source, view=view)
