import os
import sys
import tempfile
import numpy as np

from magnetovis import util

def earth(time,
            coord_sys='GSM',
            renderView=None,
            render=True,
            show=True,
            out_dir=tempfile.gettempdir(),
            topo_url='http://mag.gmu.edu/git-data/magnetovis/topography/world.topo.2004{0:02d}.3x5400x2700.png',
            debug=False):
    """Show Earth sphere in a given coordinat system with a topographic overlay"""

    def writevtk(time, coord_sys=coord_sys,
                    Nt=100, Np=100,
                    out_dir=out_dir, debug=debug, ftype='BINARY'):
        """Write VTK file for a sphere rotated into a given coordinate system"""

        import numpy as np

        from magnetovis import cxtransform as cx
        from vtk_export import vtk_export


        fnameVTK = os.path.join(out_dir, 'earth-' + util.tstr(time, length=5) +'.vtk')
        if os.path.exists(fnameVTK):
            return fnameVTK

        R = 1.
        theta = np.linspace(0., np.pi, Nt)
        phi = np.linspace(0., 2.*np.pi, Np)
    
        B1, B2 = np.meshgrid(phi, theta)
        B1 = B1.flatten(order='C')
        B2 = B2.flatten(order='C')
    
        normPhi = np.linspace(0., 1., Np)
        normTheta = np.flipud(np.linspace(0., 1., Nt))
        u, v = np.meshgrid(normPhi, normTheta)
        u = u.flatten(order='C')
        v = v.flatten(order='C')
        UV = np.column_stack((u, v))
    
        PI = np.pi*np.ones((B1.size, ))
        x = R*np.cos(B1+PI)*np.sin(B2)
        y = R*np.sin(B1+PI)*np.sin(B2)
        z = R*np.cos(B2)
        XYZ = np.column_stack((x, y, z))

        # TODO: Use this:
        # XYZr = cx.transform(XYZ, time, 'GEO', coord_sys)
        XYZr = cx.GEOtoGSM(XYZ, time, 'car', 'car')

        vtk_export(fnameVTK, XYZr,
                    dataset = 'STRUCTURED_GRID',
                    connectivity = (Nt, Np, 1),
                    point_data = UV,
                    texture = 'TEXTURE_COORDINATES',
                    point_data_name = 'TextureCoordinates',
                    title='Earth',
                    ftype=ftype,
                    debug=debug)

        return fnameVTK
    
    urlPNG = topo_url.format(time[1])
    filePNG = os.path.join(out_dir, os.path.split(topo_url)[1].format(time[1]))
    from hapiclient.util import urlretrieve

    # Download topographic overlay file if not found.
    if not os.path.exists(filePNG):
        if debug:
            print("Downloading " + urlPNG)
        urlretrieve(urlPNG, filePNG)
        if debug:
            print("Downloaded " + urlPNG + "\nto\n" + filePNG)

    # Save VTK file
    fileVTK = writevtk(time)

    # Import statement down here so we can test above code w/o paraview.
    import paraview.simple as pvs

    # Create VTK object
    # TODO: It should be possible to not need to write a file. See
    # https://stackoverflow.com/questions/59273490/python-read-vtk-file-add-data-set-then-write-vtk
    # https://blog.kitware.com/improved-vtk-numpy-integration/
    sphereVTK = pvs.LegacyVTKReader(FileNames=[fileVTK])
    
    if not renderView:
        renderView = pvs.GetActiveViewOrCreate('RenderView')

    # Create a display object in the renderView
    sphereDisplay = pvs.Show(sphereVTK, renderView)
    
    # Defaults shown by Python trace for the display properties of a sphere
    sphereDisplay.Representation = 'Surface'
    sphereDisplay.ColorArrayName = [None, '']
    sphereDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    sphereDisplay.SelectOrientationVectors = 'None'
    sphereDisplay.ScaleFactor = 0.4
    sphereDisplay.SelectScaleArray = 'None'
    sphereDisplay.GlyphType = 'Arrow'
    sphereDisplay.GlyphTableIndexArray = 'None'
    sphereDisplay.DataAxesGrid = 'GridAxesRepresentation'
    sphereDisplay.PolarAxes = 'PolarAxesRepresentation'
    sphereDisplay.ScalarOpacityUnitDistance = 0.15493986305312726
    
    # Apply overlay
    textureProxy = pvs.servermanager.CreateProxy("textures", "ImageTexture")
    textureProxy.GetProperty("FileName").SetElement(0, filePNG)
    textureProxy.UpdateVTKObjects()
    sphereDisplay.Texture = textureProxy

    if not show:
        pvs.Hide(sphereVTK, renderView)

    if render:
        # Render all display objects in renderView
        pvs.Render()

    return sphereDisplay, renderView, sphereVTK

def field_data(time, Xgrid, values, dims, texture, # dims = [Nx,Ny,Nz]
                    var = 'dummy_variable',
                    out_filename = os.path.join(tempfile.gettempdir(), 'structured_grid_dummy'),
                    renderView=None,
                    render=True,
                    show=True,
                    debug=True, sum_total=False):

    from vtk_export import vtk_export

    if os.path.exists(out_filename):
        if debug: print(out_filename + ' ALREADY EXISTS')
    else:
        if sum_total:
            tot = np.sum(values, axis=0)
            tot = ' ' + str(tot)
        else:
            tot = ''
        vtk_export(out_filename, Xgrid,
                        dataset='STRUCTURED_GRID',
                        connectivity=dims,
                        point_data=values,
                        texture=texture,
                        point_data_name=var,
                        title=var + 'field' + tot,
                        ftype='BINARY',
                        debug=debug)

    import paraview.simple as pvs

    if not renderView:
        renderView = pvs.GetActiveViewOrCreate('RenderView')

    # create a new 'Legacy VTK Reader'
    structured_gridvtk = pvs.LegacyVTKReader(FileNames=[out_filename])

    # show data in view
    structured_gridvtkDisplay = pvs.Show(structured_gridvtk, renderView)
    
    # trace defaults for the display properties.
    structured_gridvtkDisplay.Representation = 'Points'
    structured_gridvtkDisplay.ScaleFactor = 21.0
    structured_gridvtkDisplay.ScalarOpacityUnitDistance = 5.766431907

    if not show:
        pvs.Hide(structured_gridvtk, renderView)

    if render:
        # print title of structured grid vtk (including total if summed)
        title = 'structured_gridvtk.'
        print('\n\n########################\n########################')
        print('\n\n' + title + '\n\n')
        print('\n\n########################\n########################')
        # Render all display objects in renderView
        pvs.Render()

    return structured_gridvtk

def plane_data(time, Ugrid, values, dims, texture,
                    var = 'dummy_variable',
                    out_filename = os.path.join(tempfile.gettempdir(), 'plane_grid_dummy'),
                    renderView=None,
                    render=True,
                    show=True,
                    debug=True, sum_total=False):
    pass
    



def slice(structured_grid, origin, normal,
                                renderView=None,
                                render=True,
                                show=True,
                                debug=True, vector_component=None):

    import paraview.simple as pvs
    if not renderView:
        renderView = pvs.GetActiveViewOrCreate('RenderView')

    # create a new 'Slice'
    slice1 = pvs.Slice(Input=structured_grid)
    slice1.SliceType = 'Plane'
    slice1.SliceOffsetValues = [0.0]

    # init the 'Plane' selected for 'SliceType'
    slice1.SliceType.Origin = origin
    slice1.SliceType.Normal = normal

    # get color transfer function/color map for var
    point_data_name = structured_grid.PointData.keys()[0]
    print('point_data_name = ' + point_data_name)

    colorMap = pvs.GetColorTransferFunction(point_data_name)

    # show data in view
    slice1Display = pvs.Show(slice1, renderView)

    # trace defaults for the display properties.
    slice1Display.Representation = 'Surface'
    slice1Display.LookupTable = colorMap
    slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'

    if vector_component is not None:
        #https://kitware.github.io/paraview-docs/latest/python/_modules/paraview/simple.html
        pvs.ColorBy(slice1Display, ('POINTS', point_data_name, vector_component))

    slice1Display.RescaleTransferFunctionToDataRange(False)

    # show color bar/color legend
    slice1Display.SetScalarBarVisibility(renderView, True)


    # https://docs.paraview.org/en/latest/ReferenceManual/colorMapping.html
    # apply custom color transfer function
    if False:
        colorMap.RGBPoints = get_color_transfer_function()

    #slice1Display.RescaleTransferFunctionToDataRange(False) #screws everything up if put here

    return colorMap


def get_color_transfer_function(scale='continuous_log', highest_val = 100., unit = 1., n = 5001):

    # write color transfer function with numpy
    def transfunc(x_units):
        x = x_units/log_units
        try:
            assert(len(x.shape) == 1)
            ret = []
            for i in range(x.size):
                ret.append(transfunc(x[i]))
            return np.array(ret)
        except:
            if 0<=x and x <= p:
                return B*x
            if x>p:
                return np.log10(x) + 1.
            if x<0:
                #return -transfunc(-x)
                return 0.

    def transfunc(x_units):
        x = x_units/unit
        if scale=='continuous_log':
            B = 10./(np.e*np.log(10.)) # log is nat log (base e) 
            p = np.e/10.
            if 0<=x and x <= p:
                return B*x
            if x>p:
                return np.log10(x) + 1.
            if x<0:
                #return -transfunc(-x)
                return 0.
        if scale=='linear':
            if x>0:
                return x
            else:
                #return -x
                return 0
        if scale == 'kinked_log':
            if 0 <= x and x <= 1.:
                return x
            if x>1:
                return np.log10(x) + 1.
            if x<0:
                return 0

    #val_range = highest_val*np.linspace(-1, 1, 100)
    #CAREFUL: with above val_range, it made the magnitude look slightly
    #         blue (so slightly negative) on the outskirts where it 
    #         should be zero. Note zero was point.
    #         TODO: find what interpolation inbetween paraview uses
    val_range = highest_val*np.linspace(-1, 1, n)

    mx = np.max(val_range)
    norm = transfunc(mx)
    #print('mx',mx)
    #print('norm',norm)
    #print(transfunc(val_range))

    red_range = np.zeros(n)
    for i in range(n):
        red_range[i] = (1./norm)*transfunc(val_range[i])

    blue_range = np.zeros(n)
    for i in range(n):
        blue_range[i] = (1./norm)*transfunc(-val_range[i])

    green_range = np.zeros(n)

    transfunc_array = np.column_stack([val_range,
                                        red_range,
                                        green_range, blue_range])
    return transfunc_array.flatten()


def location_on_earth(time, mlat, mlon,
                                renderView=None,
                                render=True,
                                show=True,
                                debug=True):

    import cxtransform as cx
    import paraview.simple as pvs

    center = cx.MAGtoGSM([1., mlat, mlon], time, 'sph', 'car')

    if not renderView:
        renderView = pvs.GetActiveViewOrCreate('RenderView')

    sph = pvs.Sphere()
    # Properties modified on sph
    sph.Center = center
    sph.Radius = 0.2
    sph.ThetaResolution = 10
    sph.PhiResolution = 10

    # show data in view
    sphDisplay = pvs.Show(sph, renderView)
    # trace defaults for the display properties.
    sphDisplay.Representation = 'Surface'
    sphDisplay.ColorArrayName = [None, '']
    sphDisplay.OSPRayScaleArray = 'Normals'
    sphDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    sphDisplay.SelectOrientationVectors = 'None'
    sphDisplay.ScaleFactor = 0.2
    sphDisplay.SelectScaleArray = 'None'
    sphDisplay.GlyphType = 'Arrow'
    sphDisplay.GlyphTableIndexArray = 'None'
    sphDisplay.DataAxesGrid = 'GridAxesRepresentation'
    sphDisplay.PolarAxes = 'PolarAxesRepresentation'
    # change solid color
    sphDisplay.DiffuseColor = [1.0, 0.0, 1.0]

    if not show:
        pvs.Hide(structured_gridvtk, renderView)

    if render:
        # Render all display objects in renderView
        pvs.Render()


def axis(time, val, coord_sys='GSM',
        length_positive=15., length_negative=0., 
        tick_spacing=1, label=True,
            renderView=None,
            render=True,
            show=True,
            out_dir=tempfile.gettempdir(),
            debug=False):
    """Show coordinate axis with origin at center of Earth"""

    h = length_positive
    assert(length_negative == 0.)

    import paraview.simple as pvs
    if not renderView:
        renderView = pvs.GetActiveViewOrCreate('RenderView')

    #------------------
    # x axis
    #------------------
    cylinder = pvs.Cylinder()
    cylinder.Radius = 0.05
    cylinder.Center = [0., (length_positive-length_negative)/2., 0.]
    cylinder.Height = length_positive + length_negative
    cylinderDisplay = pvs.Show(cylinder, renderView)
    cylinderDisplay.ColorArrayName = [None, '']

    if val == 'x':
        cylinderDisplay.DiffuseColor = [1.0, 0.0, 0.0]
    if val == 'y':
        cylinderDisplay.DiffuseColor = [1.0, 1.0, 0.5]
    if val == 'z':
        cylinderDisplay.DiffuseColor = [0.0, 1.0, 0.0]

    if val == 'x':
        # Default Cylinder is orientated along y-axis.
        # To get x cylinder, rotate by -90 around z-axis.
        cylinderDisplay.Orientation = [0.0, 0.0, -90.0]
    if val == 'y':
        # Default Cylinder is orientated along y-axis, so 
        # the following statement is not needed.
        cylinderDisplay.Orientation = [0.0, 0.0, 0.0]
    if val == 'z':
        # Default Cylinder is orientated along y-axis.
        # To get z cylinder, rotate by 90 around x-axis.
        cylinderDisplay.Orientation = [90.0, 0.0, 0.0]

    # cone x
    cone = pvs.Cone()
    # Properties modified on coneX
    cone.Resolution = 30
    cone.Radius = 0.2
    cone.Height = 0.4
    if val == 'x':
        cone.Center = [length_positive, 0.0, 0.0]
        cone.Direction = [1., 0., 0.]
    if val == 'y':
        cone.Center = [0.0, length_positive, 0.0]
        cone.Direction = [0., 1., 0.]
    if val == 'z':
        cone.Center = [0.0, 0.0, length_positive]
        cone.Direction = [0., 0., 1.]
    # show data in view
    coneDisplay = pvs.Show(cone, renderView)
    # trace defaults for the display properties.
    coneDisplay.Representation = 'Surface'
    coneDisplay.ColorArrayName = [None, '']
    coneDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    coneDisplay.SelectOrientationVectors = 'None'
    coneDisplay.ScaleFactor = 0.04000000357627869
    coneDisplay.SelectScaleArray = 'None'
    coneDisplay.GlyphType = 'Arrow'
    coneDisplay.GlyphTableIndexArray = 'None'
    coneDisplay.DataAxesGrid = 'GridAxesRepresentation'
    coneDisplay.PolarAxes = 'PolarAxesRepresentation'
    # change solid color
    if val == 'x':
        coneDisplay.DiffuseColor = [1.0, 0.0, 0.0]
    if val == 'y':
        coneDisplay.DiffuseColor = [1.0, 1.0, 0.5]
    if val == 'z':
        coneDisplay.DiffuseColor = [0.0, 1.0, 0.0]

    for i in range(int(h)-1):
        # create a new 'Sphere'
        sph = pvs.Sphere()

        # Properties modified on sph
        if val == 'x':
            sph.Center = [i+1, 0.0, 0.0]
        elif val == 'y':
            sph.Center = [0., i+1, 0.]
        elif val == 'z':
            sph.Center = [0., 0., i+1]

        sph.Radius = 0.2
        sph.ThetaResolution = 10
        sph.PhiResolution = 10

        # show data in view
        sphDisplay = pvs.Show(sph, renderView)
        # trace defaults for the display properties.
        sphDisplay.Representation = 'Surface'
        sphDisplay.ColorArrayName = [None, '']
        sphDisplay.OSPRayScaleArray = 'Normals'
        sphDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
        sphDisplay.SelectOrientationVectors = 'None'
        sphDisplay.ScaleFactor = 0.2
        sphDisplay.SelectScaleArray = 'None'
        sphDisplay.GlyphType = 'Arrow'
        sphDisplay.GlyphTableIndexArray = 'None'
        sphDisplay.DataAxesGrid = 'GridAxesRepresentation'
        sphDisplay.PolarAxes = 'PolarAxesRepresentation'
        # change solid color
        if val == 'x':
            sphDisplay.DiffuseColor = [1.0, 0.0, 0.0]
        elif val == 'y':
            sphDisplay.DiffuseColor = [1.0, 1.0, 0.5]
        elif val == 'z':
            sphDisplay.DiffuseColor = [0.0, 1.0, 0.0]

    if not show:
        #pvs.Hide(sphereVTK, renderView)
        assert(True)
    if render:
        # Render all display objects in renderView
        pvs.Render()


    return None

    #pass


def axes(time,
            lengths_positive=[15., 15., 15.],
            lengths_negative=[0.,0.,0.],
            labels=[True, True, True],
            coord_sys='GSM',
            tick_spacing=1,
            renderView=None,
            render=True,
            show=True,
            out_dir=tempfile.gettempdir(),
            debug=False): 

    axis(time, 'x', length_positive=lengths_positive[0], length_negative=lengths_negative[0], label=labels[0],
        coord_sys=coord_sys, tick_spacing=tick_spacing, renderView=renderView, render=render, show=show, out_dir=out_dir, debug=debug)
    axis(time, 'y', length_positive=lengths_positive[1], length_negative=lengths_negative[1], label=labels[1],
        coord_sys=coord_sys, tick_spacing=tick_spacing, renderView=renderView, render=render, show=show, out_dir=out_dir, debug=debug)
    axis(time, 'z', length_positive=lengths_positive[1], length_negative=lengths_negative[1], label=labels[1],
        coord_sys=coord_sys, tick_spacing=tick_spacing, renderView=renderView, render=render, show=show, out_dir=out_dir, debug=debug)


def magnetic_dipole(time,
            renderView=None,
            render=True,
            show=True,
            out_dir=tempfile.gettempdir(),
            debug=False):
    axis(time, 'z', coord_sys='MAG',
            length_positive=15., length_negative=0., tick_spacing=1, label=False,
            renderView=renderView,
            render=render,
            show=show,
            out_dir=out_dir,
            debug=debug)



def trace_lines(points, connectivity,
                    out_fname=os.path.join(tempfile.gettempdir(),'line_tmp.vtk'),
                    ftype='BINARY',
                    color=[1,0,0],
                    renderView=None,
                    render=True,
                    show=True,
                    debug=False):

    # connectivity = [0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,2,2,2,3,3,3,3,3] 
    # ?or? connectivity = [5,7,7,5]


    # Save line as VTK file
    sys.path.append('../')
    from vtk_export import vtk_export
    #vtk_export(out_fname, line, None, connectivity, 'line', None, title='Title', ftype=ftype, grid='POLYDATA') # modify
    if os.path.exists(out_fname):
        print(out_fname + ' ALREADY EXISTS')
    else:
        vtk_export(out_fname, points,
                        dataset = 'POLYDATA',
                        connectivity = connectivity,
                        ftype=ftype)

    # Import statement down here so we can test above code w/o paraview.
    import paraview.simple as pvs

    if renderView is None:
        renderView = pvs.GetActiveViewOrCreate('RenderView')

    fileVTK = out_fname
    # create a new 'Legacy VTK Reader'
    field_linevtk = pvs.LegacyVTKReader(FileNames=[fileVTK])
    # show data in view
    field_linevtkDisplay = pvs.Show(field_linevtk, renderView)
    # trace defaults for the display properties.
    field_linevtkDisplay.Representation = 'Surface'
    field_linevtkDisplay.ColorArrayName = [None, '']
    field_linevtkDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    field_linevtkDisplay.SelectOrientationVectors = 'None'
    field_linevtkDisplay.ScaleFactor = 0.20896326303482057
    field_linevtkDisplay.SelectScaleArray = 'None'
    field_linevtkDisplay.GlyphType = 'Arrow'
    field_linevtkDisplay.GlyphTableIndexArray = 'None'
    field_linevtkDisplay.DataAxesGrid = 'GridAxesRepresentation'
    field_linevtkDisplay.PolarAxes = 'PolarAxesRepresentation'

    # create a new 'Tube'
    tube1 = pvs.Tube(Input=field_linevtk, guiName=fileVTK)
    tube1.Scalars = [None, '']
    tube1.Vectors = [None, '1']
    tube1.Radius = 0.05
    # Properties modified on tube1
    tube1.Vectors = [None, '']
    # show data in view
    tube1Display = pvs.Show(tube1, renderView)
    # trace defaults for the display properties.
    tube1Display.Representation = 'Surface'
    tube1Display.ColorArrayName = [None, '']
    tube1Display.OSPRayScaleArray = 'TubeNormals'
    tube1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    tube1Display.SelectOrientationVectors = 'None'
    tube1Display.ScaleFactor = 0.2129082262516022
    tube1Display.SelectScaleArray = 'None'
    tube1Display.GlyphType = 'Arrow'
    tube1Display.GlyphTableIndexArray = 'None'
    tube1Display.DataAxesGrid = 'GridAxesRepresentation'
    tube1Display.PolarAxes = 'PolarAxesRepresentation'

    # hide data in view
    pvs.Hide(field_linevtk, renderView)
    # change solid color
    tube1Display.DiffuseColor = color


def latitude_lines(time, coord_sys='GEO', increment=15,
                    color=[1,0,0],
                    renderView=None,
                    render=True,
                    show=True,
                    out_dir=tempfile.gettempdir(),
                    debug=False):

    npts = 100

    lat_array = np.arange(-90., 90. + increment, increment)
    lon = np.linspace(0,360,npts)
    #np.einstum('',lat_array,lon)

    import cxtransform as cx

    points = np.zeros((npts*lat_array.size, 3))
    for i in range(lat_array.size):
        a = np.column_stack([np.ones(npts, ), lat_array[i]*np.ones(npts, ), lon])
        line = cx.transform(a, time, coord_sys, 'GSM', ctype_in='sph', ctype_out='car')
        points[i*npts : (i+1)*npts, :] = line

    conn = npts*np.ones(lat_array.size, dtype=int)

    out_fname = os.path.join(out_dir, coord_sys + '_latitude_lines.vtk')

    trace_lines(points, {'LINES' : conn}, out_fname=out_fname,
                                        color=color, ftype='BINARY',
                                            renderView=renderView,
                                            render=render,
                                            show=show,
                                            debug = debug)


def longitude_lines(time, coord_sys='GEO', increment=30, color=[0,0,1],
                                        renderView=None,
                                        render=True,
                                        show=True,
                                        out_dir=tempfile.gettempdir(),
                                        debug=False):

    npts = 100

    lon_array = np.arange(0., 360. + increment, increment)
    lat = np.linspace(-90,90,npts)
    #np.einstum('',lat_array,lon)

    import cxtransform as cx

    points = np.zeros((npts*lon_array.size, 3))
    for i in range(lon_array.size):
        a = np.column_stack([np.ones(npts, ), lat, lon_array[i]*np.ones(npts, )])
        line = cx.transform(a, time, coord_sys, 'GSM', ctype_in='sph', ctype_out='car')
        points[i*npts : (i+1)*npts, :] = line

    conn = npts*np.ones(lon_array.size, dtype=int)

    out_fname = os.path.join(out_dir, coord_sys + '_longitude_lines.vtk')

    trace_lines(points, {'LINES' : conn}, out_fname=out_fname,
                                        color=color, ftype='BINARY',
                                            renderView=renderView,
                                            render=render,
                                            show=show,
                                            debug = debug)


def plane(time, val, extend=[[-15,15],[-15,15]], coord_sys='GSE', labels=True,
          renderView=None, render=True, show=True,):
    # val='XY', 'XZ', 'YZ'
    import paraview.simple as pvs
    import numpy as np
    from cxtransform import transform
    
    assert isinstance(extend, list or tuple or np.ndarray), \
        'extend has to be either an list, tuple, or numpy.ndarray'
    extend = np.array(extend)
    assert extend[0,0] < extend[0,1], \
        'lower bounds for {}-axis is higher than upper bound for {}-axis'\
            +'\n extend[0]={} '.format(val[0], val[0], extend[0])
    assert extend[1,0] < extend[1,1], \
        'lower bounds for {}-axis is higher than upper bound for {}-axis'\
            + '\n extend[1]={}'.format(val[1], val[1], extend[1])
    
    col1 = np.array((extend[0,0], extend[0,1], extend[0,0]))
    col2 = np.array((extend[1,0], extend[1,0], extend[1,1]))
    if val == 'XY':
        c1 = 0
        c2 = 1
    elif val == 'XZ':
        c1 = 0
        c2 = 2
    elif val == 'YZ':
        c1 = 1
        c2 = 2
    else:
        assert False, 'val should be "XY", "XZ", or "YZ"'
    exarray = np.zeros((3,3))    
    exarray[:,c1] = col1
    exarray[:,c2] = col2

    if coord_sys != 'GSE':
        assert time != None, 'If coord_sys in not GSM then time cannot be None'
        exarray = transform(exarray, time, 'GSE', coord_sys, 'car', 'car')

    plane = pvs.Plane()
    
    if not renderView:
        renderView = pvs.GetActiveViewOrCreate('RenderView')
    
    plane.Origin = exarray[0]
    plane.Point1 = exarray[1]
    plane.Point2 = exarray[2]
    
    planeDisplay = pvs.Show(plane, renderView)
    planeDisplay.Representation = 'Surface'
    
    pvs.RenameSource('{}-plane {}'.format(val, coord_sys))  
    
    if not show:
        pvs.Hide()
    if render:
        pvs.Render()
    
    return planeDisplay, renderView
        


'''
def fieldlines(time, start_points, model='IGRF', # or SCARR ect
                                   model_function=None,
                                   #stop_function=None,
                                   line_color=[1,0,0],
                                   tube_color=[1,0,1], # 4 values?
                                   tube_radius=0.01,
                                   s_grid=None,
                                                max_iterations=100,
                                                renderView=None,
                                                render=True,
                                                show=True,
                                                out_dir=tempfile.gettempdir(),
                                                debug=True):
#def fieldlines(time, start_points, model='IGRF', model_function=None, stop_function=None, line_color=[1,0,0], tube_color=[1,0,0,1], tube_radius=0.01):
    
    analytic = ['IGRF','T1995','T2000'] # Ones SpacePy knows
    if model not in analytic:
        import scipy.odeint
    
    analytic = ['IGRF','T1995','T2000'] # Ones SpacePy knows
    if model not in analytic:
        # TODO: Modify cutplane.fieldlines to accept stop_function.
        # TODO: Modify cutplane.fieldlines to accept run_id.
        # TODO: Move fieldlines out of cutplane and put it in fieldlines.py
        lines = cutplane.fieldlines(time, ..., stop_function=stop_function)
    else:
        # TODO: Use spacepy to get field lines for analytic model
        # (May need to extend their code to handle 3-D field lines _but_
        # we should consider using vtk 3-D interpolator (pass grid and triangulate
        # then use the vtk 3-D interpolation lib which will probably be fast, See
        # https://stackoverflow.com/a/21990296)
    # If stop_function=None, define our own stop function.
    # model_function returns the field given time, X, Y, Z. Will used to connect to simulation.s
    #(time, mag, fieldvar='b', s_grid=None, max_iterations=100, debug=False)
    if s_grid is None:
        s_grid = np.arange(0., 10., 0.1)
    # Trace field line for a total length of smax, and check if stop conditions
    # satified. If not satified, trace for another total length of smax.
    # Note that Python 3 version of integration library has stop function
    # that can be passed so this won't be needed.
    linenum = 0
    conn = np.zeros(start_points.shape[0], dtype=int)
    #points = np.zeros((?, 3))
    points = np.empty((0, 3)) # combined flines to pass to trace_lines
    try:
        from scipy.integrate import odeint
        for k in range(start_points.shape[0]):
            X0 = start_points[k, :]
            if debug:
                print('linenum = ' + str(linenum))
                print('k =' + str(k))
            done = False
            sol = np.empty((0, 3)) # Combined segments until stopped
            i = 0
            while not done:
                if debug:
                    print('i = ' + str(i))
                sol_seg = odeint(model_function, X0, s_grid)
                R = sol_seg[:, 0]**2+sol_seg[:, 1]**2 + sol_seg[:, 2]**2
                # define condition on the field line points
                # Find first location where soln steps out-of-bounds
                #tr = np.where( False == (R >= 1) & (soln[:,0] > -30.) & (np.abs(soln[:, 2]) < 20.) )        
                # Boolean array.
                tr = (R >= 1) & (sol_seg[:,0] > -30.) & (np.abs(sol_seg[:, 2]) < 20.)
                # RuntimeWarning: invalid value encountered in greater_equal
                # Indices where stop conditions satisfied
                tr_out = np.where(tr == False)
                if debug:
                    print(tr)
                if tr_out[0].size > 0:
                    # Stop condition found at least once. Use solution up to that point.s
                    sol = np.vstack((sol, sol_seg[0:tr_out[0][0] + 1, :]))
                    done = True
                elif max_iterations == i + 1:
                    sol = np.vstack((sol, sol_seg))   # return soln   faster?
                    done = True
                else:
                    # New initial condition is stop point.
                    X0 = sol_seg[-1, :]
                    # Append solution but exclude last value, which is the
                    # new initial condition.
                    sol = np.vstack((sol, sol_seg[0:-1, :]))
                i = i + 1
            #points[i*npts : (i+1)*npts, :] = line
            points = np.vstack((points, sol)) 
            conn[k] = sol.shape[0]
            linenum += 1
    except ImportError:
        pass
    out_fname = os.path.join(out_dir, 'test_field_lines.vtk')
    trace_lines(points, {'LINES' : conn}, out_fname=out_fname,
                                        color=tube_color, ftype='BINARY',
                                            renderView=renderView,
                                            render=render,
                                            show=show,
                                            debug = debug)
    # If stop_function=None, define our own stop function.
    # model_function returns the field given time, X, Y, Z. Will used to connect to simulation.s
'''


def magnetopause(time, Bz=None, Psw=None, model='Shue97', coord_sys='GSM',
                 color=[0,1,0,0.5], representation='Surface',
                 out_dir=tempfile.gettempdir(),
                 renderView=None, render=True, show=True,
                 return_x_max = False):
    """Show magnetopause surface"""
    # If time is an array, show surface for each time (with varying opacity or color)
    
    import pytz 
    import numpy as np
    import numpy.matlib
    from datetime import datetime
    from magnetovis.util import tstrTimeDelta, tstr, time2datetime
    from vtk_export import vtk_export
    from magnetovis.cxtransform import transform


    def mpause_Shue97(Bz, Psw, return_x_max = False):
        """
        Magntopause positions from Shue et al. 1997.  
        [https://doi.org/10.1029/98JA01103] 
    
        The magnetopause distance from Earth's center from Shue et al. 1997
        is
       
        r = r_0(2/(1+cos(theta)))**alpha
    
        where
        r is the location of the magnetopause surface in GSM coordinates.
        r_0 depends on the interplanetary magnetic field Bz and the solar wind
            dynamic pressure Psw units in Re.
        theta is The angle between positive x-axis in GSM coordinates and the r vector
        alpha depends on the interplanetary magnetic field Bz and the solar wind
            dynamic pressure Psw units in Re.
    
        Parameters:
        ----------
        Bz  : float 
            Interplanetary magnetic field in nT
        Psw  : float
            Solar wind dynamic pressure in nPa.
    
        Returns:
        -------
        3 numpy array's 
        
            Creates 3 numpy array's of the X, Y, and Z coordinates of the 
            magnetopause according to the Shue et al. 1997 model based on the 
            solar wind dynamic pressure Psw and the interplanetary magnetic field Bz. 
        """
        
        if Bz >= 0:
            r_0 = 11.4 + 0.013*Bz * (Psw**(-1/6.6))       # Eqn 12 of Shue et al. 1997
        else:
            r_0 = 11.4 + 0.14*Bz * (Psw**(-1/6.6))        # Eqn 12 of Shue et al. 1997
        
        alpha = (0.58 - 0.010 * Bz) * (1 + 0.010 * Psw)  #  Eqn 14 of Shue et al. 1997
        
        phi_step = 1
        theta_step = 1
        last_phi = 360
        stopping_constant = 40/(2**alpha * r_0)
        theta_finder_array = np.arange(np.pi/2 , np.pi, 0.01)
        
        for theta in theta_finder_array: 
            stopping_value = np.cos(theta)/((1 + np.cos(theta))**alpha)
            if abs(stopping_value) < stopping_constant:
                last_theta = theta
            else:
                break
        last_theta = np.rad2deg(last_theta)
        theta_array = np.arange(0, last_theta, theta_step)
        phi_array = np.arange(0, last_phi, phi_step)
        phi_repeat = len(theta_array)
        theta_repeat = len(phi_array)
        theta_array = np.repeat(theta_array, theta_repeat)    
        phi_array = np.matlib.repmat(phi_array, 1, phi_repeat).flatten()
        theta_array = np.radians(theta_array)
        phi_array = np.radians(phi_array)
        
        r_array = r_0*( (2/(1+np.cos(theta_array)))**alpha)
        
        X = r_array * np.cos(theta_array)
        Y = r_array * np.sin(theta_array) * np.sin(phi_array)
        Z = r_array * np.sin(theta_array) * np.cos(phi_array)
        points = np.column_stack([X, Y, Z])
        connectivity = {'HYPERBOLOID TRIANGLE': phi_repeat}
        print('Created Magnetopause model from Shue et al. 1997.')
        return points, connectivity 
    
    def mpause_Roelof_Sibeck93(Bz, Psw, return_x_max = False):
    
        """
        The magnetopause model from Roelof and Sibeck 1993 paper. 
        DOI: https://doi.org/10.1029/93JA02362
       
        r**2 * s1 * X**2 + s2 * X + s3 = 0 
    
        where
        r**2 = Y**2 + Z**2
        s1 = exp(a00 + a10 * x + a01 * y + a20 * x**2 + a11 * x * y + a02 * y**2)
        s2 = exp(b00 + b10 * x + b01 * y + b20 * x**2 + b11 * x * y + b02 * y**2)
        s3 = -exp(c00 + c10 * x + c01 * y + c20 * x**2 + c11 * x * y + c02 * y**2)
        x = np.log(Psw/P0)/sigma_lnp
        y = (Bz - Bz0)/sigma_Bz
        
        a00, a01, a20, a11,... etc are all constants calculated by Roelof and Sibeck
        1993.
        
    
        Parameters:
        ----------
        Bz : float
            Interplanetary magnetic field in nT.
        
        Psw  : float
            Solar wind dynamic pressure in nPa.
            
        return_x_max : bool, optional
            When True the function does not create a magnetopause surface. Instead
            it only returns the maximum value of X in GSE coordinates so that the 
            bow shock can use it to calculate the appropriate sub solar distance.
    
    
        Returns:
        -------
        3 numpy array's 
        
            Creates 3 numpy array's of the X, Y, and Z coordinates of the 
            magnetopause according to the Roelof and Sibeck 1993 model in GSE. 
            
        float
            
            when return_x_max = True, this function returns the max value of X in 
            GSE coordinates. This is used by Fairfield 1971
        
        """
        
        P0 = 2.088 # nPa
        sigma_lnp = 0.6312 # unit less
        Bz0 = -0.1635 # nT
        sigma_Bz = 3.489
        
        a00 = -1.764
        a10 = -0.299
        a01 = -0.151
        a20 = -0.246
        a11 = 0.050
        a02 = 0.476
        
        b00 = 2.934
        b10 = -0.076
        b01 = -0.129
        b20 = -0.012
        b11 = 0.079
        b02 = 0.0026
        
        c00 = 5.397
        c10 = -0.183
        c01 = -0.041
        c20 = -0.044
        c11 = 0.040
        c02 = 0.020
        
        x = np.log(float(Psw)/P0)/sigma_lnp
        y = (Bz - Bz0)/sigma_Bz
        
        lnA = a00 + a10 * x + a01 * y + a20 * x**2 + a11 * x * y + a02 * y**2
        lnB = b00 + b10 * x + b01 * y + b20 * x**2 + b11 * x * y + b02 * y**2
        ln_negC = c00 + c10 * x + c01 * y + c20 * x**2 + c11 * x * y + c02 * y**2
        
        s1 = np.exp(lnA)
        s2 = np.exp(lnB)
        s3 = - np.exp(ln_negC)
        
        sqrt_descriminate = np.sqrt(s2**2 - 4 * (-s1) * (-s3))
        x_max = (s2 - sqrt_descriminate)/ (-2 * s1)
        x_min = (s2 + sqrt_descriminate)/ (-2 * s1)
        if x_min < -40:
            x_min = -40
        
        # used to get the max X value of the magnetopause in order to calculate the
        # appropriate sub solar distance of the bow shock. 
        if return_x_max:
            return x_max
    
        steps = 200
        x_repeats = 300
    
        X = np.linspace(x_max, x_min ,steps)
        X = X.repeat(x_repeats)
        
        r = -s1 * X **2 - s2 * X - s3
        r[r<0] = 0
        r = np.sqrt(r)
        
        phi = np.linspace(0, 2 * np.pi, x_repeats)
        phi = np.matlib.repmat(phi, 1, steps).flatten()
        
        Y = r * np.cos(phi)
        Z = r * np.sin(phi)
        points = np.column_stack([X, Y, Z])
        connectivity = {'HYPERBOLOID TRIANGLE': x_repeats}
        
        
        # flag pole for text label in paraview
        base_coords = np.array([[-15, np.sqrt(-s1*(-15)**2 -s2*(-15)-s3 ), 0]])
        base_coords = rot_mat(base_coords)[0]
        top_coords = np.copy(base_coords) 
        top_coords[1] = top_coords[1] +30
        flagpole_coords = [base_coords, top_coords]
        print('Created Magnetopause model from Roelof and Sibeck 1993.')
        return points, connectivity, flagpole_coords
    
    def mpause_Sibeck_Lopez_Roelof1991(Bz=None, Psw=None,
                                        return_x_max = False):
    
        """
        The magnetopause model from Sibeck, Lopez, and Roelof 1991 paper. 
        DOI: https://doi.org/10.1029/93JA02362
       
        r**2 * s1 * X**2 + s2 * X + s3 = 0 
    
        where
        r**2 = Y**2 + Z**2
        s1 = 0.14
        s2 = 18.2
        s3 = -217.2
        p0 = 2.04  # 
        rho =  (p0/Psw)**(1/6) #
    
        Parameters:
        ----------
        Bz_or_Psw : float
            The parameter has the option of being the interplanetary magnetic field
            Bz in nT or the dynamic solar wind pressure Psw in nPa. The choice is 
            made by the second parameter "option".
            
        option : string, optional
            This has two possible values "Bz" or "Psw" which specifies how Bz_or_Psw
            should be interpreted as. The default is "Bz".
            
        return_x_max : bool, optional
            When True the function does not create a magnetopause surface. Instead
            it only returns the maximum value of X in GSE coordinates so that the 
            bow shock can use it to calculate the appropriate sub solar distance.
    
        Returns:
        -------
        3 numpy array's 
        
            Creates 3 numpy array's of the X, Y, and Z coordinates of the 
            magnetopause according to the Siebeck, Lopez and Roelof 1991 model 
            based on the solar wind dynamic pressure or interplanetary magnetic
            field in GSE coordinates. 
        
        """
        if Psw != None:
            s1, s2, s3 = 0.14, 18.2, -217.2
            p_0 = 2.04
            rho = (p_0 / Psw) ** (1./6)
            print('Creating Sibeck Lopez Roelof 1991 mpause model'+ 
                  ' with Psw = {}'.format(Psw))
        elif Bz != None:
            rho = 1
            print('Creating Sibeck Lopez Roelof 1991' +
                  ' mpause model with Bz = {}'.format(Bz))
            if Bz <= -4:
                s1, s2, s3 = 0.12, 19.9, -200.6
                if Bz < -6:
                    print('WARNING Bz={}nT which is out of range of valid values'+
                          'for Sibeck Lopez Roelof 91 magnetopause model. \n'+
                          'valid values are [-6,6] \n'+ 
                          'Using values for Bz in [-6,-4] bin.'.format(Bz))
            elif Bz <= -2:
                s1, s2, s3 = 0.22, 18.2, -213.4
            elif Bz <= 0:
                s1, s2, s3 = 0.11, 17.9, -212.8
            elif Bz <= 2:
                s1, s2, s3 = 0.2, 17.1, -211.5
            elif Bz <= 4:
                s1, s2, s3 = 0.09, 15.7, -198.3
            else:
                s1, s2, s3 = 0.13, 13.1, -179.2
                if Bz > 6:
                    print('WARNING Bz={}nT which is out of range of valid values'+
                          'for Sibeck Lopez Roelof 91 magnetopause model. \n'+
                          'valid values are [-6,6] \n'+ 
                          'Using values for Bz in [4,6] bin.'.format(Bz))

        sqrt_descriminate = np.sqrt((s2*rho)**2 - 4 * (s1) * (s3) * rho**2)
        x_max = (-s2*rho + sqrt_descriminate)/ (2 * s1)
        x_min = (-s2*rho - sqrt_descriminate)/ (2 * s1)
        if x_min < -40:
            x_min = -40
        
        # used for getting the max value for magnetopause to get proper bowshock
        # distance to magnetopause distance ratio
        if return_x_max:
            return x_max
    
        steps = 50
        x_repeats = 100
        connectivity = {'HYPERBOLOID TRIANGLE': x_repeats}
        X = np.linspace(x_max, x_min ,steps)
        X = X.repeat(x_repeats)
        
        r = -s1 * X **2 - s2 * rho * X - s3 * rho ** 2
        r[r<0] = 0
        r = np.sqrt(r)
        
        phi = np.linspace(0, 2 * np.pi, x_repeats)
        phi = np.matlib.repmat(phi, 1, steps).flatten()
        
        Y = r * np.cos(phi)
        Z = r * np.sin(phi)
        
        # flag pole for text label in paraview
        base_coords = np.array([[0, np.sqrt(-s3 * rho ** 2), 0]])        
        
        base_coords = rot_mat(base_coords)[0]
        top_coords = np.copy(base_coords) 
        top_coords[1] = top_coords[1] + 10
        flagpole_coords = [base_coords, top_coords]
        
        print('Created Magnetopause model from Sibeck Lopez Roelof 1991.')
        points = np.column_stack([X, Y, Z])
        return points, connectivity, flagpole_coords
    
    r, g, b, opacity = color
    year_limit = datetime(1995, 1, 1)
    
    valid_rep = ['Surface', '3D Glyphs', 'Feature Edges', 
                   'Outline' 'Point Gaussian', 'Points', 'Surface With Edges',
                   'Wireframe', 'Volume']
    assert representation in valid_rep,\
    """representation must be one of the following {}""".format(valid_rep)
    
    if not return_x_max:
        if time == None:
           assert Bz != None and Psw != None, 'If time is None then  '+\
               'neither Psw or Bz can be None.'
           assert coord_sys == 'GSE', 'If time is None then Coord_sys cannot ' +\
               'be None.'
        
        if model == 'Sibeck_Lopez_Roelof91':
            assert (isinstance(Psw,bool) and Psw == False) \
                or (isinstance(Bz, bool) and  Bz == False), \
                    'If model=Sibeck_Lopez_Roelof91 Psw or Bz has to be False but not both.'
            assert not (isinstance(Psw,bool) and Psw == 999 \
                        and Bz == False and isinstance(Bz, bool)),\
                'when model=Siebck_Lopez_Roelof Both Psw and Bz cannot be False.'
        
        
        if time != None:
            time_str = tstr(time,5).replace(':','-')
            if Bz == None or Psw == None:
                from hapiclient import hapi, hapitime2datetime
                server     = 'https://cdaweb.gsfc.nasa.gov/hapi';
                dataset    = 'OMNI_HRO2_1MIN';
                parameters = 'BZ_GSE,Pressure';
                opts = {'logging': True, 'usecache': True}
                start = tstrTimeDelta(time, -30)
                stop =  tstrTimeDelta(time, +30)
                data, meta = hapi(server, dataset, parameters, start, stop, **opts)
                time_arr = hapitime2datetime(data['Time'])
                data['Pressure'][data['Pressure'] == 99.99] = np.nan
                data['BZ_GSE'][data['BZ_GSE'] == 9999.99] = np.nan
                unixZero = datetime(1970,1,1,tzinfo = time_arr[0].tzinfo)
                t1 = np.empty(time_arr.shape)
                time_to_interpolate = \
                    (time2datetime(time).replace(tzinfo=pytz.UTC) - unixZero).total_seconds()
                for i in range(len(time_arr)):
                    t1[i] = (time_arr[i] - unixZero).total_seconds()
            else:
                if return_x_max == False:
                    print('Ignoring time because Bz and Psw were given')   
        else:
            time_str = ''
                    
        if Bz == False and isinstance(Bz, bool) \
            and model == 'Sibeck_Lopez_Roelof91':
            Bz = None
            Bz_str = ''
            print('Ignoring Bz to produce magnetopause becuase Bz=999 and '+
                  'model = Sibeck_Lopez_Roelof91')
        else:
            if Bz == None:
                if hapitime2datetime(start) < year_limit:
                    Bz = 0 # Nominal Value
                    print('Current Dataset OMNI_HRO2_1MIN does not go back further')
                    print('than 1995. Using Nominal Value Bz=0')
                elif all(np.isnan(data['BZ_GSE'])):
                    Bz = 0 # Nomnal Value
                    print('No values of Bz from OMNI_HRO2_1MIN dataset given.')
                    print('using nominal value Bz=0')
                else:
                    nans = np.isnan(data['BZ_GSE'])
                    BZ_GSE_OMNI= np.interp(t1, t1[~nans], data['BZ_GSE'][~nans])
                    Bz = np.interp(time_to_interpolate, t1, BZ_GSE_OMNI)
                
            Bz_str = 'Bz {:.3g}'.format(Bz)
        
        if Psw == False and isinstance(Psw, bool) \
            and model == 'Sibeck_Lopez_Roelof91':
            Psw = None
            Psw_str = ''
            print('Ignoring Psw to produce magnetopause becuase Psw=999 and '+
                  'model = Sibeck_Lopez_Roelof91')
        else:
            if Psw == None:
                if hapitime2datetime(start) < year_limit:
                    Psw = 2.04 
                    print('Current Dataset OMNI_HRO2_1MIN does not go back further')
                    print('than 1995. Using Nominal Value Psw=2')
                elif all(np.isnan(data['Pressure'])):
                    Psw = 2.04 # nominal value. check later.
                    print('No values of Pressure from OMNI_HRO2_1MIN dataset given.')
                    print('using nominal value Psw=2 (nPa)')
                else:
                    nans = np.isnan(data['Pressure'])
                    pressure_OMNI = np.interp(t1, t1[~nans], data['Pressure'][~nans])
                    Psw = np.interp(time_to_interpolate, t1, pressure_OMNI)
            Psw_str = 'Psw {:.3g}'.format(Psw)
    
    if model == "Shue97":
        if return_x_max:
            return mpause_Shue97(Bz, Psw, return_x_max)
        points, connectivity, flagpole_coords = mpause_Shue97(Bz, Psw)
    elif model == "Roelof_Sibeck93":
        if return_x_max:
            return mpause_Roelof_Sibeck93(Bz,Psw, return_x_max)
        points, connectivity, flagpole_coords = mpause_Roelof_Sibeck93(Bz, Psw)
    elif model == 'Sibeck_Lopez_Roelof91':
        if return_x_max:
            return mpause_Sibeck_Lopez_Roelof1991(Bz=Bz, Psw=Psw, 
                                                  return_x_max=return_x_max)
        points, connectivity, flagpole_coords = mpause_Sibeck_Lopez_Roelof1991(Bz, Psw)
    
    if coord_sys != 'GSE':
        points = transform(points, time, 'GSE', coord_sys, 'car', 'car')
        Bz = transform([0,0,Bz], time, 'GSE', coord_sys, 'car', 'car')[0]
    
    points = rot_mat(points)

    filename = 'mPause_{}_{}_{}_{}_{}'\
        .format(model, Bz_str, Psw_str, coord_sys, time_str)\
        .replace(' ', '')
    flagpole_text = 'mPause {} \n{} {}\n{} {}'\
        .format(model, Bz_str, Psw_str, coord_sys, time_str)
    fnameVTK = os.path.join(out_dir, filename + '.vtk') 
    vtk_export(out_filename =fnameVTK,
                   points = points, dataset = 'POLYDATA',
                   connectivity=connectivity,
                   title=filename, ftype='ASCII')
    
    import paraview.simple as pvs
    
    """
    # Properties modified on text1Display
    
    
    # Properties modified on text1Display
    text1Display.TopPosition = [0.0, 15.0, 0.0]
    """
    magnetopauseVTK = pvs.LegacyVTKReader(FileNames=[fnameVTK])
    
    if not renderView:
        renderView = pvs.GetActiveViewOrCreate('RenderView')
    
    magnetopauseDisplay = pvs.Show(magnetopauseVTK, renderView)
    magnetopauseDisplay.Representation = representation
    magnetopauseDisplay.Opacity = opacity
    magnetopauseDisplay.DiffuseColor = [r, g, b]
    
    renderView.ResetCamera()
    
    text = pvs.Text()
    textDisplay = pvs.Show(text, renderView)
    textDisplay.FontSize = 12
    textDisplay.TextPropMode = 'Flagpole Actor'
    textDisplay.TopPosition = flagpole_coords[1]
    textDisplay.BasePosition = flagpole_coords[0]

    textDisplay.Color = [r, g, b]
    text.Text = flagpole_text 
    
    renderView.Update()
    pvs.RenameSource(filename, magnetopauseVTK)
    pvs.RenameSource('TEXT - ' + flagpole_text.strip('\n'))
    
    if not show:
        pvs.Hide(magnetopauseVTK, renderView)
        pvs.Hide(text, renderView)
    if render:
        pvs.RenderAllViews()
    
    return magnetopauseDisplay, renderView, magnetopauseVTK
    

def bowshock(time, model='Fairfield71', Bz = None, Psw = None,
             mpause_model='Roelof_Sibeck93',
             coord_sys='GSE',
             color=[0,1,0,1], representation='Surface',
             out_dir=tempfile.gettempdir(),
             renderView=None, render=True, show=True):
    """Show bowshock suraface"""

    from datetime import datetime
    import pytz 
    from magnetovis.util import tstrTimeDelta, tstr, time2datetime
    from vtk_export import vtk_export
    from magnetovis.cxtransform import transform
    
    def bowshock_Fairfield71(Bz, Psw,
                             mpause_model='Roelof_Sibeck93'):
        """
        Bow shock surface model from Fairfield 1971 paper. 
        https://doi.org/10.1029/JA076i028p06700
    
        The equation of the Bow Shock is given by:
            
       
        r = ...
    
        where
        
        Parameters
        ----------
        Bz : float
            The interplanetary magnetic field in nano Tesla.
        Psw : float
            The solar wind dynamic pressure in nano Pascals. 
    
        Returns
        -------
        3 nd.array
            3 spatial coordiante arrays of the surface of the bow shock in GSE 
            coordinate system.
    
        """
        A = 0.0296
        B = -0.0381
        C = -1.280
        D = 45.644
        E = -652.10
        
        x_max_pause = magnetopause(time=None, Bz=Bz, Psw=Psw, 
                                   model=mpause_model,
                                   coord_sys='GSE', return_x_max=True)

        
        c1 = (A * C - 2 * D)/(A**2 - 4 * B)
        c2 = (4 * E - C**2)/(A**2 - 4 * B)
        
        x_steps = 128
        x_min = -40
        bowshock_subs_ratio = 1.3 * x_max_pause
        x_max = - np.sqrt(c1**2 + c2) - c1
        shift = x_max - bowshock_subs_ratio
        x_max = x_max - shift
        X = np.linspace(x_max,x_min, x_steps)
        repeat = len(X)
        X = X.repeat(repeat)
        
        m = (A * (X + shift) + C)/2 
        s = m**2 - B * (X + shift)**2 - D * (X + shift) - E
        s = np.where(s < 0, 0, s) # to account for negatives under the radical
        
    
        remainder = -(A * (X + shift) + C)/2
        r = np.sqrt(s) + remainder 
        
        r = np.where(r== remainder, 0, r)
        phi = np.linspace(0, 2 * np.pi, repeat)
        phi = np.matlib.repmat(phi, 1, repeat).flatten()
    
        Y = r * np.cos(phi)
        Z = r * np.sin(phi)
        # print('\n\n')
        print('This is the xmax distance of the bowshock {}'.format(x_max))
        print('This is the xmax distance of the mpause {}'.format(x_max_pause))
        points = np.column_stack([X, Y, Z])
        connectivity = {'HYPERBOLOID TRIANGLE': repeat}
        print('Created Magnetopause model from Fairfield 1971.')
        
        # flag pole for text label in paraview
        base_coords = np.array([[x_max, 0, 0]])        
        
        base_coords = rot_mat(base_coords)[0]
        top_coords = np.copy(base_coords) 
        top_coords[1] = top_coords[1] + 45
        flagpole_coords = [base_coords, top_coords]
    
        return points, connectivity, flagpole_coords
    year_limit = datetime(1995, 1, 1)
    r, g, b, opacity = color
    
    if time == None:
       assert Bz != None and Psw != None, \
           'If time is None then neither Psw or Bz can be None.'
       assert coord_sys == 'GSE', \
           'If time is None then Coord_sys cannot be None.'
    
    if mpause_model == 'Sibeck_Lopez_Roelof91':
        assert (isinstance(Psw, bool) and Psw == False) \
            or (isinstance(Bz, bool) and Bz == False), \
            'if model=Sibeck_Lopez_Roelof Psw or Bz has to be False but not both.'
        assert not ((isinstance(Psw, bool) and Psw == False) \
                    and (isinstance(Bz, bool) and Bz == False)), \
            'when model=Siebck_Lopez_Roelof Both Psw and Bz cannot be False.'
    
    if time != None:
        time_str = tstr(time,5).replace(':','-')
        if Bz == None or Psw == None:
            from hapiclient import hapi, hapitime2datetime
            
            server     = 'https://cdaweb.gsfc.nasa.gov/hapi';
            dataset    = 'OMNI_HRO2_1MIN';
            parameters = 'BZ_GSE,Pressure';
            opts = {'logging': True, 'usecache': True}
            start = tstrTimeDelta(time, -30)
            stop =  tstrTimeDelta(time, +30)
            data, meta = hapi(server, dataset, parameters, start, stop, **opts)
            
            time_arr = hapitime2datetime(data['Time'])
            data['Pressure'][data['Pressure'] == 99.99] = np.nan
            data['BZ_GSE'][data['BZ_GSE'] == 9999.99] = np.nan
            unixZero = datetime(1970,1,1,tzinfo = time_arr[0].tzinfo)
            t1 = np.empty(time_arr.shape)
            time_to_interpolate = (time2datetime(time).\
                                   replace(tzinfo=pytz.UTC) - unixZero).\
                                   total_seconds()
            for i in range(len(time_arr)):
                t1[i] = (time_arr[i] - unixZero).total_seconds()
        else:
            print('Ignoring time because Bz and Psw were given')
    else:
        time_str = ''
     
    if isinstance(Bz, bool) and Bz == False \
        and mpause_model == 'Sibeck_Lopez_Roelof91':
        Bz = None
        Bz_str = ''
    else:
        if Bz == None:
            if hapitime2datetime(start) < year_limit:
                Bz = 0 
                print('Current Dataset OMNI_HRO2_1MIN does not go back further')
                print('than 1995. Using Nominal Value Bz=0')
            elif all(np.isnan(data['BZ_GSE'])):
                Bz = 0 # nominal value. check later.
                print('No values of Bz from OMNI_HRO2_1MIN dataset given.')
                print('using nominal value Bz=0')
            else:
                nans = np.isnan(data['BZ_GSE'])
                BZ_GSE_OMNI= np.interp(t1, t1[~nans], data['BZ_GSE'][~nans])
                Bz = np.interp(time_to_interpolate, t1, BZ_GSE_OMNI)
        Bz_str = 'Bz {:.3g}'.format(Bz)
    
    if isinstance(Psw, bool)  and Psw == False \
        and mpause_model == 'Sibeck_Lopez_Roelof91':
        Psw = None
        Psw_str = ''
    else:
        if Psw == None:
            if hapitime2datetime(start) < year_limit:
                Psw = 2 
                print('Current Dataset OMNI_HRO2_1MIN does not go back further')
                print('than 1995. Using Nominal Value Psw=2')
            elif all(np.isnan(data['Pressure'])):
                Psw = 2 # nominal value. check later.
                print('No values of Pressure from OMNI_HRO2_1MIN dataset given.')
                print('using nominal value Psw=2 (nPa)')
            else:
                nans = np.isnan(data['Pressure'])
                pressure_OMNI = np.interp(t1, t1[~nans], data['Pressure'][~nans])
                Psw = np.interp(time_to_interpolate, t1, pressure_OMNI)
        Psw_str = 'Psw {:.3g}'.format(Psw)

    
    if model == 'Fairfield71':
        points, connectivity, flagpole_coords = bowshock_Fairfield71(Bz, Psw,
                                                    mpause_model=mpause_model)
        
    
    
    
    # Although Fairfield 1971 state that the abberation
    # is 4 degrees later Fairfield revised the number to be 4.82 degrees 
    # according to Tipsod Fortran code notes. 
    if model == 'Fairfield71':
        points = rot_mat(points, angle=-4.82)
        # deg = np.deg2rad(-4.82)
        # a = 0#0.3131
        # h, k = 0,0#-a*np.sin(deg), a*np.cos(deg)

    else:
        points = rot_mat(points)
    
    if coord_sys != 'GSE':
        points = transform(points, time, 'GSE', coord_sys, 'car', 'car')
        Bz = transform([0,0,Bz], time, 'GSE', coord_sys, 'car', 'car')[0]

    
    filename = 'Bowshock_{}_w-{}_{}_{}_{}_{}'\
        .format(model, mpause_model, Bz_str, Psw_str, coord_sys, time_str)\
        .replace(' ', '')
    mpause_model = mpause_model.replace('_', " ")
    flagpole_text = "bshock {} {} \n{} {}\n{} {}"\
        .format(model, mpause_model, Bz_str, Psw_str, coord_sys, time_str)
        
    fnameVTK = os.path.join(out_dir, filename + '.vtk') 
    vtk_export(out_filename =fnameVTK,
                   points = points, dataset = 'POLYDATA',
                   connectivity=connectivity,
                   title=filename, ftype='ASCII')    
    
    import paraview.simple as pvs
    
    bowshockVTK = pvs.LegacyVTKReader(FileNames=[fnameVTK])
    
    if not renderView:
        renderView = pvs.GetActiveViewOrCreate('RenderView')
    
    bowshockDisplay = pvs.Show(bowshockVTK, renderView)
    bowshockDisplay.Representation = representation
    bowshockDisplay.Opacity = opacity
    bowshockDisplay.DiffuseColor = [r, g, b]
    
    renderView.ResetCamera()
    
    text = pvs.Text()
    textDisplay = pvs.Show(text, renderView)
    textDisplay.FontSize = 12
    textDisplay.Color = [r, g, b]
    text.Text = flagpole_text
    textDisplay.TextPropMode = 'Flagpole Actor'
    textDisplay.TopPosition = flagpole_coords[1]
    textDisplay.BasePosition = flagpole_coords[0]
    renderView.Update()
    pvs.RenameSource(filename, bowshockVTK)
    pvs.RenameSource('TEXT - ' + flagpole_text.strip('\n'))
    
    if not show:
        pvs.Hide(bowshockVTK, renderView)
        pvs.Hide(text, renderView)
    if render:
        pvs.RenderAllViews()
    
    return bowshockDisplay, renderView, bowshockVTK
                            
def satellite(time_o, time_f, satellite_id, 
              coord_sys='GSM',
              color=[1,0,0,1],
              representation='Surface',
              tube_radius=None, 
              shader_preset=None,
              region_colors=None,
              out_dir=tempfile.gettempdir(),
              renderView=None,
              render=True,
              show=True
              ):
    """Show satellite path
    line is shown if tube_radius = None. Otherwise tube is shown.
    color keyword ignored if region_colors is not None.
    region_colors={'Tail_lobe': [1,0,0,1], 'Psphere': [],...} 
    """
    
    valid_rep = ['Surface', '3D Glyphs', 'Feature Edges', 
                   'Outline', 'Point Gaussian', 'Points', 'Surface With Edges',
                   'Wireframe', 'Volume']
    assert representation in valid_rep,\
    "representation must be one of the following\n{}".format(valid_rep)
    
    from hapiclient import hapi
    
    def poly_line(points, color, title, tube_radius, text_y_loc,
                  representation, shader_preset, flagpole_text,
                  renderView=None, render=True, show=True):
        import paraview.simple as pvs  
        
        rgb, opacity = color[0:3], color[3]

        if not renderView:
            renderView = pvs.GetActiveViewOrCreate('RenderView')
        trace_path = pvs.PolyLineSource()
        trace_path.Points = points
        trace_display = pvs.Show(trace_path, renderView)
        trace_display.Opacity = opacity
        trace_display.DiffuseColor = rgb
        pvs.Hide3DWidgets(proxy=trace_path)
        
        if representation == 'Point Gaussian':
            valid_shader_presets = ['Plain Circle', 'Triangle', 
                                    'Square Outline', 'Custom',
                                    'Gaussian Blur', 'Sphere',
                                    'Black-edged circle']
            assert shader_preset in valid_shader_presets,\
                'shader_preset must be one of the following\n{}'.format(
                    valid_shader_presets)
            trace_display.Representation = representation
            trace_display.ShaderPreset = shader_preset 
            trace_display.GaussianRadius = 0.005
        
        text = pvs.Text()
        textDisplay = pvs.Show(text, renderView)
        textDisplay.FontSize = 12
        textDisplay.Color = color[0:3]
        text.Text = flagpole_text
        textDisplay.TextPropMode = 'Flagpole Actor'
        textDisplay.BasePosition = points[0:3]
        top = np.copy(points[0:3])
        top[2] =+ text_y_loc
        textDisplay.TopPosition = top
        textDisplay.Bold = 1
        pvs.RenameSource("text " + title.replace('tube ',''), text)
        pvs.RenameSource(title.replace('tube ','line '), trace_path)
        
        if tube_radius != None:      
            tube = pvs.Tube(Input=trace_path)
            tube.Radius = tube_radius 
            tubeDisplay = pvs.Show(tube, renderView)
            tubeDisplay.Opacity = opacity
            tubeDisplay.AmbientColor = rgb
            tubeDisplay.DiffuseColor = rgb
            pvs.RenameSource(title, tube)
            pvs.Hide(trace_path, renderView)
            if not show:
                pvs.Hide(tube, renderView)
            
        else: 
            text.Text = title.replace('tube ', '')
            
        
        
        if not show:
            pvs.Hide(trace_path, renderView)
            pvs.Hide(text, renderView)
        
        if render:
            pvs.RenderAllViews() 
        
        renderView.ResetCamera()
        
        return trace_display, renderView, trace_path
        
    
    server     = 'http://hapi-server.org/servers/SSCWeb/hapi';
    opts       = {'logging': True, 'usecache': True}
    parameters = "X_{},Y_{},Z_{},Spacecraft_Region"\
                .format(coord_sys, coord_sys, coord_sys)
    data, meta = hapi(server, satellite_id, parameters, 
                      time_o, time_f, **opts)
    first = True
    if isinstance(region_colors, dict):
            
        title = '{} {} tube'.format(satellite_id, coord_sys)   
        text_y_loc = 5
        start = 0
        last_region = data['Spacecraft_Region'][0]
        
        for i in range(len(data['Spacecraft_Region'])): 
            if last_region != data['Spacecraft_Region'][i] or i == len(data)-1:
                if i != len(data)-1:
                    adder = 0
                else:
                    adder = 1
                if first:
                    flagpole_text = '{} {}\n {}'.format(title, last_region, 
                                                        data['Time'][start])
                    first = False
                else:
                    flagpole_text = '{}\n{}'.format(last_region,
                                                    data['Time'][start])
                poly_line(
                    points=np.dstack((data['X_'+coord_sys][start:i+adder],
                                      data['Y_'+coord_sys][start:i+adder],
                                      data['Z_'+coord_sys][start:i+adder])).flatten(),
                    title="{} {} {}-{}".format(last_region, title,
                                                        data['Time'][start],
                                                        data['Time'][i]),
                    flagpole_text = flagpole_text,
                    tube_radius=tube_radius,
                    representation=representation,
                    shader_preset=shader_preset,
                    text_y_loc=text_y_loc,
                    color=region_colors[last_region],
                    renderView=renderView, 
                    render=render, 
                    show=show
                    )
                if text_y_loc == 5:
                    text_y_loc += 5
                else:
                    text_y_loc = 5
                last_region = data['Spacecraft_Region'][i]
                start = i
        
    else:

        points = np.column_stack((data['X_' + coord_sys],
                                  data['Y_' + coord_sys],
                                  data['Z_' + coord_sys])).flatten()
        
        text_time = data['Time'][0] + '-' + data['Time'][-1]

        text = "{} {} tube continuous {}".format(satellite_id, coord_sys,
                                                text_time)
        poly_line(points, color, title=text, 
                  tube_radius=tube_radius, text_y_loc=0.95,
                  renderView=renderView, render=render, show=show)
        
           
    
def plasmapause(time):
    pass


def neutralsheet(time, psi=None, 
                 Rh=8, G=10, Lw=10, d=4,
                 xlims = (-40,-10), ylims = (-18,18),
                 coord_sys='GSM',
                 model='tsyganenko95',
                 color = [1,0,0,0.5],
                 representation='Surface With Edges',
                 return_sheet=False,
                 renderView=None,
                 render=True,
                 show=True,
                 out_dir=tempfile.gettempdir(),
                 debug=False):

    """
    Show neutral sheet surface.
    
    Creates the position of the Current Sheet from model outlined in Tsyganenko 1995
    [https://doi.org/10.1029/94JA03193]
    
    Uses the parameters Rh = 8, d = 4, G = 10, Lw = 10 used by
    https://sscweb.gsfc.nasa.gov/users_guide/ssc_reg_doc.shtml
    
    Z = z1 + z2
    
    z1 = 0.5 * np.tan(psi) \
            * (np.sqrt((X - Rh * np.cos(psi))**2 + (d * np.cos(psi))**2)
            -  np.sqrt((X + Rh * np.cos(psi))**2 + (d * np.cos(psi))**2)) 
            
    z2 = -G*np.sin(psi) * Y**4/(Y**4 + Lw**4)
    
    Parameters:
    ----------
    psi (float): 
        Angle of the dipole moment and z-axis in GSM in degrees.
    Rh (float): 
        "hinging distance"
    G (float): 
        Amplitude of the current sheet warping.
    Lw (float): 
        Defines the extension in the dawn-dusk direction.
        
    Returns:
    -------
    
    """
    
    import numpy as np
    import numpy.matlib
    import magnetovis.cxtransform as cx
    from vtk_export import vtk_export
    from util import tstr
    
    valid_rep = ['Surface', '3D Glyphs', 'Feature Edges', 
                   'Outline' 'Point Gaussian', 'Points', 'Surface With Edges',
                   'Wireframe', 'Volume']
    assert representation in valid_rep,\
    """representation must be one of the following {}""".format(valid_rep)
    
    # retrieving psi value based on time.
    if psi == None:
        assert time != None, \
            'if psi is None then time cannot be None.'
        dipole = cx.MAGtoGSM(np.array([0., 0., 1.]), time, 'car', 'sph') # [radius, latitude,longitude]
        psi = 90 - dipole[1]
        psi = np.deg2rad(psi)
        time_str = tstr(time,5).replace(':','-')
    else:
        time_str = 'None'
    
    sheet_file = \
            "Neut_Sh_{}_psi{}_{}_{}Rh{}G{}Lw{}d{}x{},{}y{},{}.vtk"\
                        .format(model, np.rad2deg(psi), time_str, coord_sys, Rh, G, Lw, d, 
                                xlims[0], xlims[1], ylims[0], ylims[1])
    flagpole_text = 'Neut_Sh {} psi{} {} \n{} Rh{} G{} Lw{} d{}'\
        .format(model, np.rad2deg(psi), time_str, coord_sys, Rh, G, Lw, d)
    fileVTK = os.path.join(out_dir, sheet_file +'.vtk') 
    
    if not os.path.exists(fileVTK) or return_sheet:   
        
        dx = 1
        dy = 1
        X = np.arange(xlims[0], xlims[1], dx)
        Y = np.arange(ylims[0], ylims[1], dy)
        Ny = len(Y)
        Nx = len(X)
        Nz = int(len(X) / Nx / Ny)       
        
        X = np.matlib.repmat(X,1 , Ny).flatten()
        Y = np.repeat(Y, Nx)
        Nz = int(len(X) / Nx / Ny)

        # Tsyganenko 1995 eq.
        z1 = 0.5 * np.tan(psi) \
            * (np.sqrt((X - Rh * np.cos(psi))**2 + (d * np.cos(psi))**2)
            -  np.sqrt((X + Rh * np.cos(psi))**2 + (d * np.cos(psi))**2))
            
        z2 = - G * np.sin(psi) * Y**4/(Y**4 + Lw**4)
        Z = z1 + z2
        points = np.column_stack([X, Y, Z])
        
        if return_sheet:
            connectivity = {'DIMENSIONS': (Nx, Ny, Nz + 2)}
            return points, connectivity, psi 
        else:
            connectivity = {'DIMENSIONS': (Nx, Ny, Nz)}
        
        print('created Tsyganenko 1995 currentsheet model')
        
        if coord_sys != 'GSM':
            points = cx.transform(points, time, 'GSM', 
                                  coord_sys, 'car', 'car')
        
        vtk_export(out_filename= fileVTK, 
                   points = np.column_stack([X, Y, Z]),
                   dataset = 'STRUCTURED_GRID',
                   connectivity=connectivity,
                   point_data = None,
                   title = sheet_file.replace('.vtk',''),
                   ftype='ASCII')
    
    import paraview.simple as pvs
    
    r, g, b, opacity = color
    neutralShVTK = pvs.LegacyVTKReader(FileNames=[fileVTK])
    if not renderView:
        renderView = pvs.GetActiveViewOrCreate('RenderView')
    
    neutralSheetDisplay = pvs.Show(neutralShVTK, renderView)
    neutralSheetDisplay.Representation = representation
    neutralSheetDisplay.Opacity = opacity
    neutralSheetDisplay.DiffuseColor = [r, g, b]
    renderView.ResetCamera()
    pvs.RenameSource(sheet_file, neutralShVTK)
    
    if render:
        pvs.Render()
    if not show:
        pvs.Hide(neutralShVTK, renderView)
    
    text = pvs.Text()
    textDisplay = pvs.Show(text, renderView)
    textDisplay.FontSize = 12
    textDisplay.Color = [r, g, b]
    text.Text = flagpole_text
    textDisplay.TextPropMode = 'Flagpole Actor'
    top = np.copy(points[0,0:3])
    textDisplay.BasePosition = top
    base = np.copy(top)
    base[2] += 5
    pvs.RenameSource('text ' + flagpole_text.strip('\n'))
    renderView.Update()
    
    if render:
        pvs.Render()
    if not show:
        pvs.Hide(neutralShVTK, renderView)
    
    return neutralSheetDisplay, renderView, neutralShVTK
    

def plasmasheet(time, psi=None, 
                 Rh=8, G=10, Lw=10, d=4,
                 xlims = (-40,0), ylims = (-18,18),
                 coord_sys='GSM',
                 model='tsyganenko95',
                 color = [1,0,0,0.5],
                 representation='Surface With Edges',
                 return_sheet=False,
                 renderView=None,
                 render=True,
                 show=True,
                 out_dir=tempfile.gettempdir(),
                 debug=False):
    """Show plasma sheet volume"""    
    
    from magnetovis.util import tstr
    import magnetovis.cxtransform as cx
    from vtk_export import vtk_export
    
    if psi == None:
        assert time != None, \
            'if psi is None then time cannot be None.'
        dipole = cx.MAGtoGSM(np.array([0., 0., 1.]), time, 'car', 'sph') # [radius, latitude,longitude]
        psi = 90 - dipole[1]
        psi = np.deg2rad(psi)
        time_str = tstr(time,5).replace(':','-')
    else:
        time_str = None
    psi_deg = np.copy(np.rad2deg(psi))
    psi_deg = np.around(psi_deg, decimals=3)
    sheet_file = \
            "Plas_Sh_{}_psi{}_time{}_{}_Rh{}G{}Lw{}d{}x{},{}y{},{}"\
                        .format(model, psi_deg, time_str, coord_sys, Rh, G, Lw, d, 
                                xlims[0], xlims[1], ylims[0], ylims[1])
    flagpole_text = 'Neut_Sh {} \npsi{} {} \n{} Rh{} G{} Lw{} d{}'\
        .format(model, psi_deg, time_str, coord_sys, Rh, G, Lw, d)
    fileVTK = os.path.join(out_dir, sheet_file + '.vtk') 
    if True:# not os.path.exists(fileVTK):
    
        sheet, connectivity, psi = neutralsheet(time=time, psi=psi, Rh=Rh, G=G, 
                                           Lw=Lw, d=d, xlims=xlims, ylims=ylims, 
                                           coord_sys=coord_sys, model=model, 
                                           color=color, 
                                           representation=representation, 
                                           return_sheet=True)
        
        low_sheet = np.copy(sheet)
        low_sheet[:,2] = sheet[:,2]-3
        high_sheet = np.copy(sheet)
        high_sheet[:,2] = sheet[:,2]+3
        points = np.concatenate((low_sheet, sheet, high_sheet))
        
        print('created Tsyganenko 1995 current sheet model with 3 Re width' 
              +' above and below')
        
        if coord_sys != 'GSM':
            points = cx.transform(points, time, 'GSM', 
                                  coord_sys, 'car', 'car')
        
        vtk_export(out_filename= fileVTK, 
                   points = points,
                   dataset = 'STRUCTURED_GRID',
                   connectivity=connectivity,
                   point_data = None,
                   title = sheet_file.replace('.vtk',''),
                   ftype='ASCII')

    import paraview.simple as pvs
    
    r, g, b, opacity = color
    plasmaShVTK = pvs.LegacyVTKReader(FileNames=[fileVTK])
    if not renderView:
        renderView = pvs.GetActiveViewOrCreate('RenderView')
    
    plasmaSheetDisplay = pvs.Show(plasmaShVTK, renderView)
    plasmaSheetDisplay.Representation = representation
    plasmaSheetDisplay.Opacity = opacity
    plasmaSheetDisplay.DiffuseColor = [r, g, b]
    renderView.ResetCamera()
    pvs.RenameSource(sheet_file, plasmaShVTK)
    
    if render:
        pvs.Render()
    if not show:
        pvs.Hide(plasmaShVTK, renderView)
    
    text = pvs.Text()
    textDisplay = pvs.Show(text, renderView)
    textDisplay.FontSize = 16
    textDisplay.Color = [r, g, b]
    text.Text = flagpole_text
    textDisplay.TextPropMode = 'Flagpole Actor'
    base = np.copy(points[0,0:3])
    base[2] += 6
    textDisplay.BasePosition = base
    top = np.copy(base)
    top[2] += 5
    textDisplay.TopPosition = top
    textDisplay.Bold = 1
    
    pvs.RenameSource('text ' + flagpole_text.strip('\n'))
    renderView.Update()
    
    if render:
        pvs.Render()
    if not show:
        pvs.Hide(plasmaShVTK, renderView)
    
    return plasmaSheetDisplay, renderView, plasmaShVTK
        
def rot_mat(points, angle=-4, h=0, k=0):
    deg = np.deg2rad(angle)
    
    points = np.pad(points, ((0,0),(0,1)), 'constant', constant_values=1)
    
    rot_trans_mat = np.array(
                [[np.cos(deg), -np.sin(deg), 0, h],
                 [np.sin(deg),  np.cos(deg), 0, k],
                 [0          ,  0          , 1, 0],
                 [0          ,  0          , 0, 0]]
                )
    
    points = np.matmul(rot_trans_mat, points.transpose()).transpose()
    points = np.delete(points, 3, 1)
    return points    
