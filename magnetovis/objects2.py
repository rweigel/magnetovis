import os
import sys
import tempfile
# it's never used so I should take this away. 
# from magnetovis import util
import numpy as np


def rot_mat(points, angle=-4, (h,k)= (0,0), translate=True, axis='Z'):
    deg = np.deg2rad(angle)
    
    if translate:
        points = np.pad(points, ((0,0),(0,1)), 'constant', constant_values=1)
        
        
        rot_trans_mat = np.array(
                    [[np.cos(deg), -np.sin(deg), 0, h],
                     [np.sin(deg),  np.cos(deg), 0, k],
                     [0          ,  0          , 1, 0],
                     [0          ,  0          , 0, 0]]
                    )
        
        points = np.matmul(rot_trans_mat, points.transpose()).transpose()
        points = np.delete(points, 3, 1)
    else:
        if axis == 'Z':
            rot_mat = np.array(
                [[np.cos(deg), -np.sin(deg), 0],
                 [np.sin(deg),  np.cos(deg), 0],
                 [0           , 0          , 1]])
        if axis == 'Y':
            rot_mat = np.array(
                [[np.cos(deg), 0, -np.sin(deg)],
                 [0          , 1,  0          ],
                 [np.sin(deg), 0,  np.cos(deg)]])
        points = np.matmul(rot_mat, points.transpose()).transpose()
    return points    


def cutplane(run='DIPTSUR2', time=(2019,9,2,4,10,0,0), plane='xz', var='p',
                    renderView=None,
                    render=True,
                    show=True,
                    debug=True):
    # read http://mag.gmu.edu/git-data/magnetovis/simulation/demo.vtk and plot it
    # due to permissions, now on http://mag.gmu.edu/git-data/sblake/magnetovisVTK/

    if plane == 'xz':
        extend=[[-55,25],[-55,55]]
    else:
        raise ValueError ('only xz plane currently supported')


    from hapiclient.util import urlretrieve

    '''
    def log(msg, opts):
        print(msg)

    def modified(url, fname, **kwargs):
        """Check if timestamp on file is later than Last-Modifed in HEAD request"""

        from os import stat, path
        from time import mktime, strptime

        debug = False

        if not path.exists(fname):
            return True

        # HEAD request on url
        log('Making head request on ' + url, kwargs)
        headers = head(url)

        # TODO: Write headers to file.head
        if debug:
            print("Header:\n--\n")
            print(headers)
            print("--")

        # TODO: Get this from file.head if found
        fileLastModified = stat(fname).st_mtime
        if "Last-Modified" in headers:
            urlLastModified = mktime(strptime(headers["Last-Modified"],
                                              "%a, %d %b %Y %H:%M:%S GMT"))

            if debug:
                print("File Last Modified = %s" % fileLastModified)
                print("URL Last Modified = %s" % urlLastModified)

            if urlLastModified > fileLastModified:
                return True
            return False
        else:
            if debug:
                print("No Last-Modified header. Will re-download")
            # TODO: Read file.head and compare etag
            return True

    def urlretrieve(url, fname, check_last_modified=False, **kwargs):
        """Download URL to file
        urlretrieve(url, fname, check_last_modified=False, **kwargs)
        If check_last_modified=True, `fname` is found, URL returns Last-Modfied
        header, and `fname` timestamp is after Last-Modfied timestamp, the URL
        is not downloaded.
        """

        import shutil
        from os import path, utime, makedirs
        from time import mktime, strptime

        if check_last_modified:
            if modified(url, fname, **kwargs):
                log('Downloading ' + url + ' to ' + fname, kwargs)
                res = urlretrieve(url, fname, check_last_modified=False)
                if "Last-Modified" in res.headers:
                    # Change access and modfied time to match that on server.
                    # TODO: Won't need if using file.head in modified().
                    urlLastModified = mktime(strptime(res.headers["Last-Modified"],
                                                      "%a, %d %b %Y %H:%M:%S GMT"))
                    utime(fname, (urlLastModified, urlLastModified))
            else:
                log('Local version of ' + fname + ' is up-to-date; using it.', kwargs)

        dirname = path.dirname(fname)
        if not path.exists(dirname):
            makedirs(dirname)

        with open(fname, 'wb') as out:
            res = urlopen(url)
            shutil.copyfileobj(res, out)
            return res
    '''

    def urlretrieveWRAP(url, fname, check_last_modified=False):
        try:
            urlretrieve(url, fname, check_last_modified=check_last_modified)
        except:
            return 'ERROR'

    '''
    def urlretrieveWRAP(url, fname, check_last_modified=False): #TODO: mostly duplicated in magnetosphere/util/util.py
        """Python 2/3 urlretrieve compatability function.

        If Python 3, returns
        urllib.request.urlretrieve(url, fname)

        If Python 2, returns
        urllib.urlretrieve(url, fname)
        """

        import sys
        if (not os.path.exists(fname)) or (not check_last_modified):
            if sys.version_info[0] > 2:
                import urllib.request, urllib.error
                try:
                    res = urllib.request.urlretrieve(url, fname)
                    return res
                except urllib.error.URLError as e:
                    print(e)
                except ValueError as e:
                    print("'" + url + "' is not a valid URL")
            else:
                import urllib, urllib2, ssl
                try:
                    context = ssl._create_unverified_context()
                    urllib2.urlopen(url) 
                    res = urllib.urlretrieve(url, fname, context=context)
                    return res
        #https://stackoverflow.com/questions/16778435/python-check-if-website-exists
                except urllib2.HTTPError, e: 
                    return(e.code)
                except urllib2.URLError, e:
                    return(e.args)
                except ValueError:
                    print("'" + url + "' is not a valid URL")
            return 'ERROR'
    '''

    vtk_fname = '%s_GSM_plane_%s_demo.vtk'%(plane,var)

    #dowload demo vtk from online server and save to /tmp/
    vtk_url = 'http://mag.gmu.edu/git-data/magnetovis/simulation/' \
              + vtk_fname
    retd = urlretrieveWRAP(vtk_url, '/tmp/'+vtk_fname, check_last_modified=True)
    if debug: print(retd)
    if retd in ['ERROR', 404]:
        vtk_url = 'http://mag.gmu.edu/git-data/sblake/magnetovisVTK/' \
                  + vtk_fname
        retd = urlretrieveWRAP(vtk_url, '/tmp/'+vtk_fname, check_last_modified=True)
        if debug: print(retd)

    #import for paraview
    import paraview.simple as pvs
    if not renderView:
        renderView = pvs.GetActiveViewOrCreate('RenderView')
    # load vtk from /tmp/ into reader object
    cutplane_vtk = pvs.LegacyVTKReader(FileNames=['/tmp/'+vtk_fname])
    # show data in view
    cutplane_vtkDisplay = pvs.Show(cutplane_vtk, renderView)
    
    if not show:
        pvs.Hide(cutplane_vtk, renderView)
    if render:
        # Render all display objects in renderView
        pvs.Render()


def trajectory():
    # read http://mag.gmu.edu/git-data/magnetovis/trajectory/demo.vtk and plot it
    pass


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

        import cxtransform as cx
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
        XYZr = np.column_stack((x, y, z))

        # TODO: Use this:
        # XYZr = cx.transform(XYZ, time, 'GEO', coord_sys)
        if coord_sys != 'GSM':
            XYZr = cx.transform(XYZr, time, 'GEO', coord_sys)
#        XYZr = cx.GEOtoGSM(XYZ, time, 'car', 'car')

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
    print(urlPNG)
    filePNG = os.path.join(out_dir, os.path.split(topo_url)[1].format(time[1]))
    import util # i needed to add this line to make it work
    from hapiclient.util import urlretrieve
    # Download topographic overlay file if not found.
    if not os.path.exists(filePNG):
        if debug:
            print("Downloading " + urlPNG)
        # TODO: Use d/l function in hapiclient.util
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
    pvs.RenameSource('Earth - {} {}'.format(coord_sys, util.tstr(time,6)))
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
    

if False:
    """
    # def slice(structured_grid, origin, normal,
    #                                 renderView=None,
    #                                 render=True,
    #                                 show=True,
    #                                 debug=True, vector_component=None):
    
    #     import paraview.simple as pvs
    #     if not renderView:
    #         renderView = pvs.GetActiveViewOrCreate('RenderView')
    
    #     # create a new 'Slice'
    #     slice1 = pvs.Slice(Input=structured_grid)
    #     slice1.SliceType = 'Plane'
    #     slice1.SliceOffsetValues = [0.0]
    
    #     # init the 'Plane' selected for 'SliceType'
    #     slice1.SliceType.Origin = origin
    #     slice1.SliceType.Normal = normal
    
    #     # get color transfer function/color map for var
    #     point_data_name = structured_grid.PointData.keys()[0]
    #     print('point_data_name = ' + point_data_name)
    
    #     colorMap = pvs.GetColorTransferFunction(point_data_name)
    
    #     # show data in view
    #     slice1Display = pvs.Show(slice1, renderView)
    
    #     # trace defaults for the display properties.
    #     slice1Display.Representation = 'Surface'
    #     slice1Display.LookupTable = colorMap
    #     slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    
    #     if vector_component is not None:
    #         #https://kitware.github.io/paraview-docs/latest/python/_modules/paraview/simple.html
    #         pvs.ColorBy(slice1Display, ('POINTS', point_data_name, vector_component))
    
    #     slice1Display.RescaleTransferFunctionToDataRange(False)
    
    #     # show color bar/color legend
    #     slice1Display.SetScalarBarVisibility(renderView, True)
    
    
    # # https://docs.paraview.org/en/latest/ReferenceManual/colorMapping.html
    #     # apply custom color transfer function
    #     if False:
    #         colorMap.RGBPoints = get_color_transfer_function()
    
    #     #slice1Display.RescaleTransferFunctionToDataRange(False) #screws everything up if put here
    
    #     return colorMap
    
    
    # def get_color_transfer_function(scale='continuous_log', highest_val = 100., unit = 1., n = 5001):
    
    #     # write color transfer function with numpy
    #     def transfunc(x_units):
    #         x = x_units/log_units
    #         try:
    #             assert(len(x.shape) == 1)
    #             ret = []
    #             for i in range(x.size):
    #                 ret.append(transfunc(x[i]))
    #             return np.array(ret)
    #         except:
    #             if 0<=x and x <= p:
    #                 return B*x
    #             if x>p:
    #                 return np.log10(x) + 1.
    #             if x<0:
    #                 #return -transfunc(-x)
    #                 return 0.
    
    #     def transfunc(x_units):
    #         x = x_units/unit
    #         if scale=='continuous_log':
    #             B = 10./(np.e*np.log(10.)) # log is nat log (base e) 
    #             p = np.e/10.
    #             if 0<=x and x <= p:
    #                 return B*x
    #             if x>p:
    #                 return np.log10(x) + 1.
    #             if x<0:
    #                 #return -transfunc(-x)
    #                 return 0.
    #         if scale=='linear':
    #             if x>0:
    #                 return x
    #             else:
    #                 #return -x
    #                 return 0
    #         if scale == 'kinked_log':
    #             if 0 <= x and x <= 1.:
    #                 return x
    #             if x>1:
    #                 return np.log10(x) + 1.
    #             if x<0:
    #                 return 0
    
    #     #val_range = highest_val*np.linspace(-1, 1, 100)
    #     #CAREFUL: with above val_range, it made the magnitude look slightly
    #     #         blue (so slightly negative) on the outskirts where it 
    #     #         should be zero. Note zero was point.
    #     #         TODO: find what interpolation inbetween paraview uses
    #     val_range = highest_val*np.linspace(-1, 1, n)
    
    #     mx = np.max(val_range)
    #     norm = transfunc(mx)
    #     #print('mx',mx)
    #     #print('norm',norm)
    #     #print(transfunc(val_range))
    
    #     red_range = np.zeros(n)
    #     for i in range(n):
    #         red_range[i] = (1./norm)*transfunc(val_range[i])
    
    #     blue_range = np.zeros(n)
    #     for i in range(n):
    #         blue_range[i] = (1./norm)*transfunc(-val_range[i])
    
    #     green_range = np.zeros(n)
    
    #     transfunc_array = np.column_stack([val_range,
    #                                         red_range,
    #                                         green_range, blue_range])
    #     return transfunc_array.flatten()
    
    
    # def location_on_earth(time, mlat, mlon,
    #                                 renderView=None,
    #                                 render=True,
    #                                 show=True,
    #                                 debug=True):
    
    #     import cxtransform as cx
    #     import paraview.simple as pvs
    
    #     center = cx.MAGtoGSM([1., mlat, mlon], time, 'sph', 'car')
    
    #     if not renderView:
    #         renderView = pvs.GetActiveViewOrCreate('RenderView')
    
    #     sph = pvs.Sphere()
    #     # Properties modified on sph
    #     sph.Center = center
    #     sph.Radius = 0.2
    #     sph.ThetaResolution = 10
    #     sph.PhiResolution = 10
    
    #     # show data in view
    #     sphDisplay = pvs.Show(sph, renderView)
    #     # trace defaults for the display properties.
    #     sphDisplay.Representation = 'Surface'
    #     sphDisplay.ColorArrayName = [None, '']
    #     sphDisplay.OSPRayScaleArray = 'Normals'
    #     sphDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    #     sphDisplay.SelectOrientationVectors = 'None'
    #     sphDisplay.ScaleFactor = 0.2
    #     sphDisplay.SelectScaleArray = 'None'
    #     sphDisplay.GlyphType = 'Arrow'
    #     sphDisplay.GlyphTableIndexArray = 'None'
    #     sphDisplay.DataAxesGrid = 'GridAxesRepresentation'
    #     sphDisplay.PolarAxes = 'PolarAxesRepresentation'
    #     # change solid color
    #     sphDisplay.DiffuseColor = [1.0, 0.0, 1.0]
    
    #     if not show:
    #         pvs.Hide(structured_gridvtk, renderView)
    
    #     if render:
    #         # Render all display objects in renderView
    #         pvs.Render()"""
    pass





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



def trace_lines(points, connectivity, out_fname=os.path.join(tempfile.gettempdir(),'line_tmp.vtk'),
                                        color=[1,0,0], ftype='BINARY',
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


def _latitude_lines(self, time, coord_sys='GSM', increment=15, color=[1,0,0]):

    import numpy as np
    import numpy.matlib
    import vtk
    from magnetovis import cxtransform as cx
    
    lon = np.arange(0,360 + 5, 5)#360/npts) # [0, 90, 180, 270]
    lat = np.arange(-90,90 + increment,increment) # [-90, -45, 0, 45, 90]
    lon_repeat = len(lat) # 5
    lat_repeat = len(lon) # 4
    lon = np.matlib.repmat(lon, 1, lon_repeat).flatten()
    lat = np.repeat(lat,lat_repeat)
    r = np.ones(lon_repeat*lat_repeat)
    
    sph_coords = np.column_stack((r,lat,lon))
    points = cx.transform(sph_coords, time, 'GSM', coord_sys, ctype_in='sph', ctype_out='car')
    
    ### start of vtk
    
    pdo = self.GetPolyDataOutput()
    pdo.Allocate(len(r), 1)
    pts = vtk.vtkPoints()
    lon_size = np.unique(lon).size
    lat_size = np.unique(lat).size
    for i in range(lat_size): # 4
        polyline = vtk.vtkPolyLine()
        polyline.GetPointIds().SetNumberOfIds(lon_size)
        for j in range(lon_size): # 5
            pts_index = j+i*lon_size
            pts.InsertPoint(pts_index, points[pts_index,0], points[pts_index,1], points[pts_index,2] )
            polyline.GetPointIds().SetId(j,pts_index)
        pdo.InsertNextCell(polyline.GetCellType(), polyline.GetPointIds())
    pdo.SetPoints(pts)

    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(1)
    colors.SetName('lat_lon')
    
    for n in range(r.size):
        colors.InsertNextTuple([0]) # 0 for lat, # 1 for lon
    pdo.GetPointData().AddArray(colors)
    
def _longitude_lines(self, time, coord_sys='GSM', increment=15, color=[1,0,0]):

    import numpy as np
    import numpy.matlib
    import vtk
    from magnetovis import cxtransform as cx
    
    lon = np.arange(0,360 + increment, increment) #360/npts) # [0, 90, 180, 270]
    lat = np.arange(-90,90 + 5, 5) # [-90, -45, 0, 45, 90]
    lon_repeat = len(lat) # 5
    lat_repeat = len(lon) # 4
    lat = np.matlib.repmat(lat, 1, lat_repeat).flatten()
    lon = np.repeat(lon,lon_repeat)
    r = np.ones(lon_repeat*lat_repeat)
    
    sph_coords = np.column_stack((r,lat,lon))
    points = cx.transform(sph_coords, time, 'GSM', coord_sys, ctype_in='sph', ctype_out='car')
    
    ### start of vtk
    
    pdo = self.GetPolyDataOutput()
    pdo.Allocate(len(r), 1)
    pts = vtk.vtkPoints()
    lon_size = np.unique(lon).size
    lat_size = np.unique(lat).size
    for i in range(lon_size): # 4
        polyline = vtk.vtkPolyLine()
        polyline.GetPointIds().SetNumberOfIds(lat_size)
        for j in range(lat_size): # 5
            pts_index = j+i*lat_size
            pts.InsertPoint(pts_index, points[pts_index,0], points[pts_index,1], points[pts_index,2] )
            polyline.GetPointIds().SetId(j,pts_index)
        pdo.InsertNextCell(polyline.GetCellType(), polyline.GetPointIds())
    pdo.SetPoints(pts)

    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(1)
    colors.SetName('lat_lon')
    
    for n in range(r.size):
        colors.InsertNextTuple([1]) # 0 for lat, # 1 for lon
    pdo.GetPointData().AddArray(colors)


def latitude_lines(time, coord_sys='GEO', increment=15, color=[0,0,1],
                   representation='Surface', tube_radius=.02, renderView=None,
                   render=True, show=True, show_annotations=False):
                   
    objs_wrapper(time=time, coord_sys=coord_sys, increment=increment,
                color=color, representation=representation, tube_radius=tube_radius,
                renderView=renderView, render=render, show=show,
                show_annotations=show_annotations, obj='latitude')


def longitude_lines(time, coord_sys='GEO', increment=15, color=[0,.5,1],
                   representation='Surface', tube_radius=.02, renderView=None,
                   render=True, show=True, show_annotations=False):
                   
    objs_wrapper(time=time, coord_sys=coord_sys, increment=increment,
                color=color, representation=representation, tube_radius=tube_radius,
                renderView=renderView, render=render, show=show,
                show_annotations=show_annotations, obj='longitude')


def plane(time, val, extend=[[-40,40],[-40,40]], coord_sys='GSM', labels=True,
          renderView=None, render=True, show=True,):
    # val='XY', 'XZ', 'YZ'
    import paraview.simple as pvs
    import numpy as np
    from util import tstr
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

    if coord_sys != 'GSM':
        assert time != None, 'If coord_sys in not GSM then time cannot be None'
        exarray = transform(exarray, time, 'GSM', coord_sys, 'car', 'car')

    plane = pvs.Plane()
    
    if not renderView:
        renderView = pvs.GetActiveViewOrCreate('RenderView')
    
    plane.Origin = exarray[0]
    plane.Point1 = exarray[1]
    plane.Point2 = exarray[2]
    
    planeDisplay = pvs.Show(plane, renderView)
    planeDisplay.Representation = 'Surface'
    planeDisplay.Opacity = 0.5
    
    pvs.RenameSource('{}-plane {} {}'.format(val, coord_sys, tstr(time, length=5)))  
    
    if not show:
        pvs.Hide()
    if render:
        pvs.Render()
    
    return planeDisplay, renderView
        

if False:
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
    pass    

  
    
def _plasmapause(self, output, time):
    
    """
    coordinate system is in Spherical SM coordinates with angle in radians
    
    log(n) = a1 * F(L) * G(L) * H(L) = 1.5
    
    where,
    F(L) = a2 - e ** (a3 * (1 -a4 * e ** (-h(L,Lambda) / a5)))
    
    G(L) = a6 * L + a7
    
    H(L) = (1 + (L / a8) ** (2 * (a9 - 1))) ** (-a9 / (a9 - 1))
    
    L = R/cos**2(Lambda) # used by SSCWEB
    
    L is the McIlwain L-Shell parameter.
    
    h(L, Lambda) is the height above the Earth's surface
    
    h = 6371.2*(1.-R)  # according to SSCWEB
    
    and Lambda is the geomagnetic latitude 
    
    constants:
        a1 = 1.4
        a2 = 1.53
        a3 = -0.036
        a4 = 30.76
        a5 = 159.9
        a7 = 6.27
        
    also,
    a6 = -0.87 + 0.12 * e ** (-x**2 / 9)
    
    a8 = 0.7 * cos(2 * pi * ((MLT - 21) / 24)) + 4.4
    
    a9 = 15.3 * cos(2 * pi * MLT / 24) + 19.7
    
    
    also, also
    MLT = (PHI*RAD/15.) - 12.
    x = MLT
    MLT is the magnetic local time measured in HH MLT=0=24 is midnight
    and MLT=12 is noon. 
    MLT domain is [0,24)
    x domain is [-12,12]
    
    PHI is the longitude 
    THETA is the latitude
    
    """
    
    import numpy as np
    import numpy.matlib
    
    # constants
    a1 = 1.4
    a2 = 1.53
    a3 = -0.036
    a4 = 30.76
    a5 = 159.9
    a7 = 6.27
    
    # obtained from SSCWEB fortran
    Re = 6371 # radius of Earth in km according to fortran SSCWEB
    R = np.linspace(1.05* Re,6, 10).repeat(10)
    THETA = 0
    PHI = np.linspace(0,2*np.pi,10)
    PHI = np.matlib.repmat(PHI, 1, 10).flatten()
    RAD = 180/np.pi
    MLT = (PHI*RAD/15.) - 12.
    x = MLT 
    MLT[MLT>=24] = MLT[MLT>=24] - 24
    MLT[MLT<0] = MLT[MLT<0] + 24
    x[x>12] = x[x>12] - 24
    x[x<12] = x[x<12] + 24
    
    a6 = -0.87 + 0.12 * np.exp(-x**2/9.)
    a8 = 0.7 * np.cos(2*np.pi* (MLT-21.)/24.) + 4.4
    a9 = 15.3 * np.cos(2*np.pi*MLT/24.) + 19.7
    
    F = a2 - np.exp(a3 * (1.-a4 * np.exp(Re*(1.-R)/a5)))
    
    L2LAM = (np.cos(THETA))**2
    
    G = (a6*R/L2LAM) + a7
    # L = R/np.cos(Lambda)**2
    
    

def plasmapause(time, representation='Surface', renderView=None, render=True,
                show=True):
    
    objs_wrapper(time=time, representation=representation, 
                 renderView=renderView, render=render, show=show, 
                 obj='Plasmapause')
    
def _neutralsheet(self, output, time, psi, 
                 Rh, G, Lw, d,
                 xlims, ylims,
                 coord_sys,
                 model,
                 return_sheet):

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
    from magnetovis import cxtransform as cx
    import paraview.simple as pvs
    
    # retrieving psi value based on time.
    if psi == None:
        assert time != None, \
            'if psi is None then time cannot be None.'
        dipole = cx.MAGtoGSM(np.array([0., 0., 1.]), time, 'car', 'sph') # [radius, latitude,longitude]
        psi = 90 - dipole[1]
        psi = np.deg2rad(psi)


    dx = 100
    dy = 100
    X = np.linspace(xlims[0], xlims[1], dx)
    Y = np.linspace(ylims[0], ylims[1], dy)
    Ny = 100
    Nx = 100    
    
    X = np.matlib.repmat(X,1 , Ny).flatten()
    Y = np.repeat(Y, Nx)

    # Tsyganenko 1995 eq.
    z1 = 0.5 * np.tan(psi) \
        * (np.sqrt((X - Rh * np.cos(psi))**2 + (d * np.cos(psi))**2)
        -  np.sqrt((X + Rh * np.cos(psi))**2 + (d * np.cos(psi))**2))
        
    z2 = - G * np.sin(psi) * Y**4/(Y**4 + Lw**4)
    Z = z1 + z2
    points = np.column_stack([X, Y, Z])
    
    if return_sheet:
        return points, psi 
    
    print('created Tsyganenko 1995 currentsheet model')
    
    if coord_sys != 'GSM':
        points = cx.transform(points, time, 'GSM', 
                              coord_sys, 'car', 'car')
    

    ############################################################
    ####### start of the code to use programmable source #######
    ############################################################
    import vtk
    if False:
        # this is never meant to run. it is only to get rid of error message
        # that output is not defined. output is defined when running
        # this script in the programmable source text box. 
        output = ''
    # communication between "script" and "script (RequestInformation)"
    executive = self.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    exts = [executive.UPDATE_EXTENT().Get(outInfo, i) for i in range(6)]
    dims = [exts[1]+1, exts[3]+1, exts[5]+1]
    
    # setting the sgrid exent
    output.SetExtent(exts)
    
    # setting up the points and allocate the number of points
    pts = vtk.vtkPoints()
    pts.Allocate(dims[0] * dims[1] * dims[2])
    
    # color sections
    lut = pvs.GetColorTransferFunction('Magnetosphere Surface')
    value = int(len(lut.Annotations)/2)
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(1)
    colors.SetName("Magnetosphere Surface")
    
    # insert points into vtkPoints
    i = 0
    for point in points:
        pts.InsertPoint(i, point[0], point[1], point[2])
        i += 1
        colors.InsertNextTuple([value])

    output.SetPoints(pts)
    output.GetPointData().AddArray(colors)

def plasmasheet(time, psi=None, 
                 Rh=8, G=10, Lw=10, d=4,
                 xlims = (-40,-5), ylims = (-15,15),
                 coord_sys='GSM',
                 model='tsyganenko95',
                 color = [.6,.3,.2,0.5],
                 representation='Surface',
                 out_dir=tempfile.gettempdir(), png_fn=None,
                 return_sheet=False,
                 renderView=None,
                 render=True,
                 show=True):
    
    objs_wrapper(time=time, psi=psi, Rh=Rh, G=G, Lw=Lw, d=d, xlims=xlims,
                 ylims=ylims, coord_sys=coord_sys, model=model, color=color,
                 representation=representation,
                 out_dir=out_dir, png_fn=png_fn,
                 return_sheet=return_sheet,
                 renderView=renderView, render=render, show=show, 
                 obj='Plasmasheet')
    

def _plasmasheet(self, output, time, psi,
                 Rh, G, Lw, d,
                 xlims, ylims,
                 coord_sys,
                 model,
                 return_sheet):
    
    """Show plasma sheet volume"""    
    
    import numpy as np
    import numpy.matlib
    from magnetovis import cxtransform as cx
    import paraview.simple as pvs
    from magnetovis.objects2 import _neutralsheet
    
    if psi == None:
        assert time != None, \
            'if psi is None then time cannot be None.'
        dipole = cx.MAGtoGSM(np.array([0., 0., 1.]), time, 'car', 'sph') # [radius, latitude,longitude]
        psi = 90 - dipole[1]
        psi = np.deg2rad(psi)

    psi_deg = np.copy(np.rad2deg(psi))
    psi_deg = np.around(psi_deg, decimals=3)

    sheet, psi = _neutralsheet(self=False, output=False, time=time, psi=psi, Rh=Rh, G=G, 
                              Lw=Lw, d=d, xlims=xlims, ylims=ylims, 
                              coord_sys=coord_sys, model=model, 
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
    
    ############################################################
    ####### start of the code to use programmable source #######
    ############################################################
    import vtk
    if False:
        # this is never meant to run. it is only to get rid of error message
        # that output is not defined. output is defined when running
        # this script in the programmable source text box. 
        output = ''
    # communication between "script" and "script (RequestInformation)"
    executive = self.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    exts = [executive.UPDATE_EXTENT().Get(outInfo, i) for i in range(6)]
    dims = [exts[1]+1, exts[3]+1, exts[5]+1]
    
    # setting the sgrid exent
    output.SetExtent(exts)
    
    # setting up the points and allocate the number of points
    pts = vtk.vtkPoints()
    pts.Allocate(dims[0] * dims[1] * dims[2])
    
    # color sections
    lut = pvs.GetColorTransferFunction('Magnetosphere Surface')
    value = int(len(lut.Annotations)/2)
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(1)
    colors.SetName("Magnetosphere Surface")
    
    # insert points into vtkPoints
    i = 0
    for point in points:
        pts.InsertPoint(i, point[0], point[1], point[2])
        i += 1
        colors.InsertNextTuple([value])

    output.SetPoints(pts)
    output.GetPointData().AddArray(colors)
        

def objs_wrapper(**kwargs):

    import paraview.simple as pvs
    import re
    import cxtransform as cx
    from util import tstr
    
    valid_rep = ['Surface', '3D Glyphs', 'Feature Edges', 
                   'Outline' 'Point Gaussian', 'Points', 'Surface With Edges',
                   'Wireframe', 'Volume']
    assert kwargs['representation'] in valid_rep,\
    """representation must be one of the following {}""".format(valid_rep)
    
    path = os.path.join(os.getcwd() + "/magnetovis/objects2.py")    
    programmableSource = pvs.ProgrammableSource()
    
    mag_surfaces = ['Magnetopause','Bowshock','Neutralsheet', 'Plasmasheet']
    
    if 'png_fn' in kwargs.keys():
        if kwargs['png_fn']:
            png_fn_fp = os.path.join(kwargs['out_dir'],kwargs['png_fn'])
    
    if kwargs['obj'] == 'axis':
        x_dim = 300
        y_dim = 300
        z_dim = 1
        
        scalar_data = kwargs['val']
        
        programmableSource.OutputDataSetType = 'vtkStructuredGrid'
        programmableSource.ScriptRequestInformation = """
        executive = self.GetExecutive()
        outInfo = executive.GetOutputInformation(0)
        dims = [{}, {}, {}] # x-dims, y-dims, z-dims
        outInfo.Set(executive.WHOLE_EXTENT(), 0, dims[0]-1 , 0, dims[1]-1 , 0, dims[2]-1)
        """.format(x_dim, y_dim, z_dim)
        
        programmableSource.Script = "kwargs="+str(kwargs)+";execfile('{}',globals(),locals())".format(path)
        
        if not kwargs['renderView']:
            renderView = pvs.GetActiveViewOrCreate('RenderView')
            
        
        programmableSourceDisplay = pvs.Show(programmableSource, renderView)
        programmableSourceDisplay.Representation = kwargs['representation']
        if kwargs['val'] == 'X':
            diffuse_color = [1,0,0]
        elif kwargs['val'] == 'Y':
            diffuse_color = [1,1,0.5]
        elif kwargs['val'] == 'Z':
            diffuse_color = [0,1,0]

        programmableSourceDisplay.DiffuseColor = diffuse_color
        
        
        if not kwargs['show']:
            pvs.Hide(programmableSource, renderView)
            
        if kwargs['render']:
            pvs.Render()
            renderView.Update()
            
        title = "{}-axis {} {}".format(kwargs['val'], 
                                                  kwargs['coord_sys'],
                                                  tstr(kwargs['time'],5))
        
        renderView = pvs.GetActiveViewOrCreate('RenderView')
        programmableSourceDisplay = pvs.Show(programmableSource, renderView)
        programmableSourceDisplay.Representation = kwargs['representation']
    
    if kwargs['obj'] in mag_surfaces:
        if kwargs['obj'] == 'Magnetopause' or kwargs['obj'] == 'Bowshock':
            x_dim = 1
            y_dim = 101
            z_dim = 101
        elif kwargs['obj'] == 'Neutralsheet':
            x_dim = 200
            y_dim = 50
            z_dim = 1
        elif kwargs['obj'] == 'Plasmasheet':
            x_dim = 200
            y_dim = 50
            z_dim = 3
            
        scalar_data = 'Magnetosphere Surface'
            
        programmableSource.OutputDataSetType = 'vtkStructuredGrid'
        programmableSource.ScriptRequestInformation = """
        executive = self.GetExecutive()
        outInfo = executive.GetOutputInformation(0)
        dims = [{}, {}, {}] # x-dims, y-dims, z-dims
        outInfo.Set(executive.WHOLE_EXTENT(), 0, dims[0]-1 , 0, dims[1]-1 , 0, dims[2]-1)
        """.format(x_dim, y_dim, z_dim)
        
        programmableSource.Script = "kwargs="+str(kwargs)+";execfile('{}',globals(),locals())".format(path)
        
        if not kwargs['renderView']:
            renderView = pvs.GetActiveViewOrCreate('RenderView')
        else:
            renderView = kwargs['renderView']
#            renderView = pvs.GetActiveViewOrCreate(kwargs['renderView']['name'])
#            if "CameraPosition" in kwargs['renderView'].keys():
#                renderView.CameraPosition = kwargs['renderView']["CameraPosition"]
#            if "CameraFocalPoint" in kwargs['renderView'].keys():
#                renderView.CameraFocalPoint = kwargs['renderView']["CameraFocalPoint"]
#            if "CameraViewUp" in kwargs['renderView']['CameraViewUp']:
#                renderView.CameraViewUp = kwargs['renderView']['CameraViewUp']
#            renderView = kwargs['renderView']
        programmableSourceDisplay = pvs.Show(programmableSource, renderView)
        programmableSourceDisplay.Representation = kwargs['representation']
        
        if not kwargs['show']:
            pvs.Hide(programmableSource, renderView)
            
        if kwargs['render']:
            pvs.Render()
            renderView.Update()
        
        if not kwargs['time']:
            kwargs['time'] = ''
            
        if kwargs['obj'] == 'Magnetopause':
            time_str, Bz_str, Psw_str = \
                _magnetopause(self='', output='', time=kwargs['time'],
                              Bz=kwargs['Bz'], Psw=kwargs['Psw'],
                              model=kwargs['model'],
                              coord_sys=kwargs['coord_sys'], 
                              return_x_max=False, return_title=True)
            
            title = "{} {} {} {} Bz={} Psw={}".format(
                kwargs['obj'], kwargs['model'], kwargs['coord_sys'], 
                time_str, Bz_str, Psw_str)
        
        elif kwargs['obj'] == 'Bowshock':
            time_str, Bz_str, Psw_str = \
                _bowshock(self='', output='', time=kwargs['time'], Bz=kwargs['Bz'],
                          Psw=kwargs['Psw'], model=kwargs['model'], 
                          mpause_model=kwargs['mpause_model'], 
                          coord_sys=kwargs['coord_sys'], return_title=True)
            
            title = "{} {} {} {} {} {} mpause_model={}".format(
                kwargs['obj'], kwargs['model'], kwargs['coord_sys'], 
                time_str, Bz_str, Psw_str, kwargs['mpause_model'])
            
        elif kwargs['obj'] == 'Neutralsheet' or kwargs['obj'] == 'Plasmasheet':
            if kwargs['psi'] == None:
                dipole = cx.MAGtoGSM(np.array([0., 0., 1.]), kwargs['time'], 'car', 'sph') # [radius, latitude,longitude]
                kwargs['psi'] = 90 - dipole[1]
                time_str = ''
            else:
                time_str = tstr(kwargs['time'], 5)
            title = '{} {} {} {} psi={:.3g} Rh={:.3g} G={:.3g} Lw={:.3g} d={:.3g}'\
                .format(kwargs['obj'], kwargs['model'], kwargs['coord_sys'],
                        tstr(kwargs['time'],length=5), kwargs['psi'], kwargs['Rh'], 
                        kwargs['G'], kwargs['Lw'], kwargs['d'])\
                    .replace('  ', ' ')
        regionsLUT = pvs.GetColorTransferFunction(scalar_data)
        regionsLUT.InterpretValuesAsCategories = 1
        regionsLUT.AnnotationsInitialized = 1
        
        index_colored_list = kwargs['color'][0:3]
        regionsLUT.IndexedColors = np.concatenate((regionsLUT.IndexedColors,index_colored_list))

        annotations = list(regionsLUT.Annotations)
        annotations.append(str(int(len(regionsLUT.Annotations)/2)))
        annotations.append(kwargs['obj'])
        
        regionsLUT.Annotations = annotations   
        
#        renderView = pvs.GetActiveViewOrCreate('RenderView')
        programmableSourceDisplay = pvs.Show(programmableSource, renderView)
        programmableSourceDisplay.Representation = kwargs['representation']
        
        pvs.ColorBy(programmableSourceDisplay, ('POINTS', scalar_data))
        programmableSourceDisplay.SetScalarBarVisibility(renderView, True)
        
        # current camera placement for renderView1
        if kwargs['png_fn']:
#            if False:
#                renderView.CameraPosition = [70, 80, 130]
#                renderView.CameraFocalPoint = [-15, 2, 0]
#                renderView.CameraViewUp = [0, 1, 0]
#                renderView.CameraParallelScale = 45
#                # save screenshot
#                pvs.SaveScreenshot(png_fn_fp, renderView, ImageResolution=[1676, 1220])
            if not kwargs['renderView']:
                renderView.CameraPosition = [11, -80, 42]
                renderView.CameraFocalPoint = [-22, 0, 0]
                renderView.CameraViewUp = [-0.3, 0.3, 0.8]
                renderView.CameraParallelScale = 25.245512504246587
                if kwargs['obj'] == 'Bowshock':
                    renderView.ResetCamera()
                # save screenshot
            pvs.SaveScreenshot(png_fn_fp, renderView, ImageResolution=[1676, 1220])
        
    
    if kwargs['obj'] == 'satellite':
        
        from hapiclient import hapi
        
        scalar_data = kwargs['satellite_id'] +  ' Spacecraft Region'    
        programmableSource.Script = "kwargs="+str(kwargs)+";execfile('{}',globals(),locals())".format(path)
        
        if not kwargs['renderView']:
            renderView = pvs.GetActiveViewOrCreate('RenderView')
            programmableSourceDisplay = pvs.Show(programmableSource, renderView)
            programmableSourceDisplay.Representation = kwargs['representation']
        
        if not kwargs['show']:
            pvs.Hide(programmableSource, renderView)
            
        if kwargs['render']:
            pvs.Render()
            renderView.Update()
        
        server     = 'http://hapi-server.org/servers/SSCWeb/hapi';
        opts       = {'logging': True, 'usecache': True}
        parameters = "X_{},Y_{},Z_{},Spacecraft_Region"\
                    .format(kwargs["coord_sys"], kwargs["coord_sys"], kwargs["coord_sys"])
        data, meta = hapi(server, kwargs["satellite_id"], parameters, 
                          kwargs["time_o"], kwargs["time_f"], **opts)
        
        if re.search('.*(?=:00.000Z)|.*(?=.000Z)', kwargs['time_o']):
                kwargs['time_o'] = re.search\
                    ('.*(?=:00.000Z)|.*(?=.000Z)', kwargs['time_o']).group()+'Z'
        if re.search('.*(?=:00.000Z)|.*(?=.000Z)', kwargs['time_f']):
            kwargs['time_f'] = re.search\
                ('.*(?=:00.000Z)|.*(?=.000Z)', kwargs['time_f']).group()+'Z'
        
        title = '{} line {} {} to {}'.format(kwargs['satellite_id'],
                                            kwargs['coord_sys'],
                                            kwargs['time_o'],
                                            kwargs['time_f'])
        
        
        unique_regions = np.unique(data['Spacecraft_Region'])
        
        regionsLUT = pvs.GetColorTransferFunction(scalar_data)
        regionsLUT.InterpretValuesAsCategories = 1
        regionsLUT.AnnotationsInitialized = 1
        
        annotations = []
        index_colored_list = []
        for i in range(len(unique_regions)):
            annotations.append(str(i))
            annotations.append(unique_regions[i])
            if kwargs['region_colors'] != None:
                index_colored_list.append(kwargs['region_colors'][unique_regions[i]])
            else:
                index_colored_list.append(kwargs['color'])

        regionsLUT.Annotations = annotations
        index_colored_list = np.array(index_colored_list).flatten()
        
        if kwargs['tube_radius'] != None:
            tube = pvs.Tube(Input=programmableSource)
            tube.Scalars = ['POINTS', scalar_data]
            tube.Radius = kwargs['tube_radius']
            
            spacecraftRegionLUT = pvs.GetColorTransferFunction(scalar_data)
            spacecraftRegionLUT.InterpretValuesAsCategories = 1
            spacecraftRegionLUT.AnnotationsInitialized = 1
            spacecraftRegionLUT.Annotations = annotations
            spacecraftRegionLUT.IndexedColors = index_colored_list
            
            tubeDisplay = pvs.Show(tube, renderView)
            tubeDisplay.Representation = kwargs['representation']
            tubeDisplay.ColorArrayName = ['POINTS', scalar_data]
            tubeDisplay.LookupTable = spacecraftRegionLUT
            tubeDisplay.OpacityArray = ['POINTS', scalar_data]
            
            pvs.Hide(programmableSource, renderView)
            tubeDisplay.SetScalarBarVisibility(renderView, True)
            renderView.Update()
            
            pvs.RenameSource(title.replace('line','tube'), tube)
            
    if kwargs['obj'] == "latitude" or kwargs['obj'] == 'longitude':
        scalar_data = 'lat_lon'
        programmableSource.Script = "kwargs="+str(kwargs)+";execfile('{}',globals(),locals())".format(path)
        
        if not kwargs['renderView']:
            renderView = pvs.GetActiveViewOrCreate('RenderView')
            programmableSourceDisplay = pvs.Show(programmableSource, renderView)
            programmableSourceDisplay.Representation = kwargs['representation']
            
        if not kwargs['show']:
            pvs.Hide(programmableSource, renderView)
            
        if kwargs['render']:
            pvs.Render()
            renderView.Update()
        
        title = "{} line {} {}".format(kwargs['obj'], kwargs['coord_sys'], tstr(kwargs['time'],5))
            
        lat_lonLUT = pvs.GetColorTransferFunction(scalar_data)
        lat_lonLUT.InterpretValuesAsCategories = 1
        lat_lonLUT.AnnotationsInitialized = 1
        
        lat_lonLUT.Annotations = ['0', 'latitude', '1', 'longitude']
        if list(lat_lonLUT.IndexedColors) != []: 
            if kwargs['obj'] == 'latitude':
                lat_lonLUT.IndexedColors = np.concatenate((kwargs['color'], lat_lonLUT.IndexedColors[3:]))
            else:
                lat_lonLUT.IndexedColors = np.concatenate((lat_lonLUT.IndexedColors[0:3], kwargs['color']))
        else: 
            if kwargs['obj'] == 'latitude':
                lat_lonLUT.IndexedColors = np.concatenate((kwargs['color'],.5*np.array(kwargs['color'])))
            else:
                lat_lonLUT.IndexedColors = np.concatenate((.5*np.array(kwargs['color']),kwargs['color']))
        
        if kwargs['tube_radius'] != None:
            tube = pvs.Tube(Input=programmableSource)
            tube.Scalars = ['POINTS',scalar_data]
            tube.Radius = kwargs['tube_radius']
            
            tubeDisplay = pvs.Show(tube, renderView)
            tubeDisplay.Representation = kwargs['representation']
            tubeDisplay.ColorArrayName = ['POINTS', scalar_data]
            tubeDisplay.LookupTable = lat_lonLUT
            tubeDisplay.OpacityArray = ['POINTS', scalar_data]
            
            pvs.Hide(programmableSource, renderView)
            if kwargs['show_annotations']:
                tubeDisplay.SetScalarBarVisibility(renderView, True)
            renderView.Update()
            
            pvs.RenameSource(title.replace('line','tube'), tube)
        
        if kwargs['show_annotations']:
            programmableSourceDisplay.SetScalarBarVisibility(renderView, True)
    
    pvs.RenameSource(title, programmableSource)

    renderView.ResetCamera()

def _satellite(self, time_o, time_f, satellite_id, coord_sys, region_colors):
    
    import vtk
    import numpy as np    
    from hapiclient import hapi
    
    server     = 'http://hapi-server.org/servers/SSCWeb/hapi';
    opts       = {'logging': True, 'usecache': True}
    parameters = "X_{},Y_{},Z_{},Spacecraft_Region"\
                .format(coord_sys, coord_sys, coord_sys)
    data, meta = hapi(server, satellite_id, parameters, 
                      time_o, time_f, **opts)

    pdo = self.GetPolyDataOutput()
    pdo.Allocate(len(data), 1)
    pts = vtk.vtkPoints()
    polyline = vtk.vtkPolyLine()
    polyline.GetPointIds().SetNumberOfIds(len(data['Spacecraft_Region']))
    for i in range(len(data['Spacecraft_Region'])):
        pts.InsertPoint(i,data['X_'+coord_sys][i], data['Y_'+coord_sys][i],
                          data['Z_'+coord_sys][i])
        polyline.GetPointIds().SetId(i,i)
    pdo.InsertNextCell(polyline.GetCellType(), polyline.GetPointIds())
    pdo.SetPoints(pts)
    
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(1)
    colors.SetName( satellite_id + ' Spacecraft Region')
    region_dict = {}
    unique_regions = np.unique(data['Spacecraft_Region'])

    for i in range(len(unique_regions)):
        region_dict[unique_regions[i]] = int(i)
    
    for region in data['Spacecraft_Region']:
        if region_colors == None:
            colors.InsertNextTuple([0])
        else:
            colors.InsertNextTuple([region_dict[region]])
            
    pdo.GetPointData().AddArray(colors)
    
def _magnetopause(self, output, time, Bz, Psw, model, coord_sys, return_x_max,
                  return_title=False):
    
    import numpy as np
    import numpy.matlib
    from datetime import datetime, timedelta
    import pytz 
    from magnetovis.util import tstr, time2datetime
    from magnetovis.cxtransform import transform, rot_mat
    import paraview.simple as pvs

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
        
        stopping_constant = 40/(2**alpha * r_0)
        theta_finder_array = np.arange(np.pi/2 , np.pi, 0.01)
        for theta in theta_finder_array: 
            stopping_value = np.cos(theta)/((1 + np.cos(theta))**alpha)
            if abs(stopping_value) < stopping_constant:
                last_theta = theta
            else:
                break
        last_theta = np.rad2deg(last_theta)
        theta_array = [[0]]
        all_theta_values = np.flipud(np.linspace(last_theta,0,50))
        for theta in all_theta_values:
            theta_array = np.pad(theta_array,((1,1),(1,1)),'constant', 
                                 constant_values=((theta,theta),(theta,theta)))
        theta_array = theta_array.flatten()
        m = np.linspace(1,-1,2*len(all_theta_values)+1,endpoint=True)
        u = np.matlib.repmat(m,1,len(m)).flatten()
        v = np.repeat(m,len(m))
        phi_array = np.arctan2(v,u)
        theta_array = np.radians(theta_array)
        
        r_array = r_0*( (2/(1+np.cos(theta_array)))**alpha)
        
        X = r_array * np.cos(theta_array)
        Y = r_array * np.sin(theta_array) * np.sin(phi_array)
        Z = r_array * np.sin(theta_array) * np.cos(phi_array)
        points = np.column_stack([X, Y, Z])

        print('Created Magnetopause model from Shue et al. 1997.')
        return points
    
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
    
        X = [[x_max]]
        all_x_values = np.flipud(np.linspace(x_min,x_max,50))
        
        for x in all_x_values:
            X = np.pad(X,((1,1),(1,1)),'constant',constant_values=((x,x),(x,x)))
        X = X.flatten()
        
        r = -s1 * X **2 - s2 * X - s3
        r[r<0] = 0
        r = np.sqrt(r)
        
        m = np.linspace(1,-1,2*len(all_x_values)+1,endpoint=True)
        u = np.matlib.repmat(m,1,len(m)).flatten()
        v = np.repeat(m,len(m))
        phi = np.arctan2(v,u)
        
        Y = r * np.cos(phi)
        Z = r * np.sin(phi)
        points = np.column_stack([X, Y, Z])

        print('Created Magnetopause model from Roelof and Sibeck 1993.')
        return points
    
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
        

        X = [[x_max]]
        all_x_values = np.flipud(np.linspace(x_min,x_max,50))
        
        for x in all_x_values:
            X = np.pad(X,((1,1),(1,1)),'constant',constant_values=((x,x),(x,x)))
        X = X.flatten()
        
        r = -s1 * X **2 - s2 * rho * X - s3 * rho ** 2
        r[r<0] = 0
        r = np.sqrt(r)
        
        m = np.linspace(1,-1,2*len(all_x_values)+1,endpoint=True)
        u = np.matlib.repmat(m,1,len(m)).flatten()
        v = np.repeat(m,len(m))
        phi = np.arctan2(v,u)
        
        Y = r * np.cos(phi)
        Z = r * np.sin(phi)

        
        print('Created Magnetopause model from Sibeck Lopez Roelof 1991.')
        points = np.column_stack([X, Y, Z])
        print('\n\n',np.shape(points),'\n\n')
        return points
    
    
    year_limit = datetime(1995, 1, 1, tzinfo=pytz.utc)
    
    if not return_x_max:
        if time == None:
           assert Bz != None and Psw != None, 'If time is None then  '+\
               'neither Psw or Bz can be None.'
           assert coord_sys != None, 'If time is None then Coord_sys cannot ' +\
               'be None.'
        
        if model == 'Sibeck_Lopez_Roelof91':
            assert (isinstance(Psw,bool) and Psw == False) \
                or (isinstance(Bz, bool) and  Bz == False), \
                    'If model=Sibeck_Lopez_Roelof91 Psw or Bz has to be False but not both.'
            ## TODO: recheck this 999 should not be there anymore
            assert not (isinstance(Psw,bool) and Psw == False \
                        and Bz == False and isinstance(Bz, bool)),\
                'when model=Siebck_Lopez_Roelof Both Psw and Bz cannot be False.'
        
        
        if time != None:
            time_str = ""+tstr(time,5)
            if Bz == None or Psw == None:
                from hapiclient import hapi, hapitime2datetime
                server     = 'https://cdaweb.gsfc.nasa.gov/hapi';
                dataset    = 'OMNI_HRO2_1MIN';
                parameters = 'BZ_GSE,Pressure';
                opts = {'logging': True, 'usecache': True}
                start = tstr(time2datetime(time) + timedelta(minutes=-30)) 
                stop =  tstr(time2datetime(time) + timedelta(minutes= 30))
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
                
            Bz_str = 'Bz={:.3g}'.format(Bz)
        
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
            Psw_str = 'Psw={:.3g}'.format(Psw)
            
    if return_title:
        return (time_str, Bz_str, Psw_str)
    
    if model == "Shue97":
        if return_x_max:
            return mpause_Shue97(Bz, Psw, return_x_max)
        points = mpause_Shue97(Bz, Psw)
    elif model == "Roelof_Sibeck93":
        if return_x_max:
            return mpause_Roelof_Sibeck93(Bz,Psw, return_x_max)
        points = mpause_Roelof_Sibeck93(Bz, Psw)
    elif model == 'Sibeck_Lopez_Roelof91':
        if return_x_max:
            return mpause_Sibeck_Lopez_Roelof1991(Bz=Bz, Psw=Psw, 
                                                  return_x_max=return_x_max)
        points = mpause_Sibeck_Lopez_Roelof1991(Bz, Psw)
    
    if coord_sys != 'GSE':
        points = transform(points, time, 'GSE', coord_sys, 'car', 'car')
        Bz = transform([0,0,Bz], time, 'GSE', coord_sys, 'car', 'car')[0]
    
    points = np.array(rot_mat(points))
    ############################################################
    ####### start of the code to use programmable source #######
    ############################################################
    import vtk
    if False:
        # this is never meant to run. it is only to get rid of error message
        # that output is not defined. output is defined when running
        # this script in the programmable source text box. 
        output = ''
    # communication between "script" and "script (RequestInformation)"
    executive = self.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    exts = [executive.UPDATE_EXTENT().Get(outInfo, i) for i in range(6)]
    dims = [exts[1]+1, exts[3]+1, exts[5]+1]
    
    # setting the sgrid exent
    output.SetExtent(exts)
    
    # setting up the points and allocate the number of points
    pts = vtk.vtkPoints()
    pts.Allocate(dims[0] * dims[1] * dims[2])
    
    # color sections
    lut = pvs.GetColorTransferFunction('Magnetosphere Surface')
    value = int(len(lut.Annotations)/2)
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(1)
    colors.SetName("Magnetosphere Surface")
    
    # insert points into vtkPoints
    i = 0
    for point in points:
        pts.InsertPoint(i, point[0], point[1], point[2])
        i += 1
        colors.InsertNextTuple([value])

    output.SetPoints(pts)
    output.GetPointData().AddArray(colors)
    
def _bowshock(self, output, time, model, Bz, Psw, mpause_model, 
              coord_sys, return_title=False):
    """Show bowshock suraface"""

    from datetime import datetime, timedelta
    import pytz 
    from magnetovis.util import tstr, time2datetime
    from magnetovis.cxtransform import transform
    from magnetovis.objects2 import _magnetopause
    from magnetovis.objects2 import rot_mat
    import numpy as np
    import paraview.simple as pvs

    
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
        
        x_max_pause = _magnetopause(self=None, output=None, time=None, Bz=Bz, Psw=Psw, 
                                   model=mpause_model,
                                   coord_sys='GSE', return_x_max=True, return_title=False)

        
        c1 = (A * C - 2 * D)/(A**2 - 4 * B)
        c2 = (4 * E - C**2)/(A**2 - 4 * B)
        
        x_min = -40
        bowshock_subs_ratio = 1.3 * x_max_pause
        x_max = - np.sqrt(c1**2 + c2) - c1
        shift = x_max - bowshock_subs_ratio
        x_max = x_max - shift
        X = [[x_max]]
        all_x_values = np.flipud(np.linspace(x_min,x_max,50))
        for x in all_x_values:
            X = np.pad(X,((1,1),(1,1)),'constant',constant_values=((x,x),(x,x)))
        X = X.flatten()

        
        g = (A * (X + shift) + C)/2 
        s = g**2 - B * (X + shift)**2 - D * (X + shift) - E
        s = np.where(s < 0, 0, s) # to account for negatives under the radical
        
    
        remainder = -(A * (X + shift) + C)/2
        r = np.sqrt(s) + remainder # 5,000
        
        r = np.where(r== remainder, 0, r)
        m = np.linspace(1,-1,2*len(all_x_values)+1,endpoint=True)
        u = np.matlib.repmat(m,1,len(m)).flatten()
        v = np.repeat(m,len(m))
        phi = np.arctan2(v,u)
        
        
        Y = r * np.cos(phi)
        Z = r * np.sin(phi)
        
        points = np.column_stack([X, Y, Z])
        print('Created Magnetopause model from Fairfield 1971.')
 
    
        return points
    year_limit = datetime(1995, 1, 1,tzinfo=pytz.utc)
    
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
        time_str = tstr(time,5)
        if Bz == None or Psw == None:
            from hapiclient import hapi, hapitime2datetime
            
            server     = 'https://cdaweb.gsfc.nasa.gov/hapi';
            dataset    = 'OMNI_HRO2_1MIN';
            parameters = 'BZ_GSE,Pressure';
            opts = {'logging': True, 'usecache': True}
            start = tstr(time2datetime(time) + timedelta(minutes=-30)) 
            stop =  tstr(time2datetime(time) + timedelta(minutes= 30)) 
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
        Bz_str = 'Bz={:.3g}'.format(Bz)
    
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
        Psw_str = 'Psw={:.3g}'.format(Psw)

    if return_title:
        return (time_str, Bz_str, Psw_str)
    
    if model == 'Fairfield71':
        points = bowshock_Fairfield71(Bz, Psw, mpause_model=mpause_model)
        
    
    
    
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

    ############################################################
    ####### start of the code to use programmable source #######
    ############################################################
    import vtk
    if False:
        # this is never meant to run. it is only to get rid of error message
        # that output is not defined. output is defined when running
        # this script in the programmable source text box. 
        output = ''
    # communication between "script" and "script (RequestInformation)"
    executive = self.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    exts = [executive.UPDATE_EXTENT().Get(outInfo, i) for i in range(6)]
    dims = [exts[1]+1, exts[3]+1, exts[5]+1]
    
    # setting the sgrid exent
    output.SetExtent(exts)
    
    # setting up the points and allocate the number of points
    pts = vtk.vtkPoints()
    pts.Allocate(dims[0] * dims[1] * dims[2])
    
    # color sections
    lut = pvs.GetColorTransferFunction('Magnetosphere Surface')
    value = int(len(lut.Annotations)/2)
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(1)
    colors.SetName("Magnetosphere Surface")
    
    # insert points into vtkPoints
    i = 0
    for point in points:
        pts.InsertPoint(i, point[0], point[1], point[2])
        i += 1
        colors.InsertNextTuple([value])

    output.SetPoints(pts)
    output.GetPointData().AddArray(colors)

def magnetopause(time, Bz=None, Psw=None, model='Shue97', coord_sys='GSM',
                 color=[0,1,0,0.5], representation='Surface',
                 out_dir=tempfile.gettempdir(), png_fn=None,
                 renderView=None, render=True, show=True,
                 return_x_max = False):
    objs_wrapper(time=time, Bz=Bz, Psw=Psw, model=model, coord_sys=coord_sys,
                 color=color, representation=representation,
                 out_dir=out_dir, png_fn=png_fn, renderView=renderView, render=render,
                 show=show, return_x_max=return_x_max, obj='Magnetopause')
    
def bowshock(time, model='Fairfield71', Bz = None, Psw = None,
             mpause_model='Roelof_Sibeck93',
             coord_sys='GSM',
             color=[0,.3,.35,1], representation='Surface',
             out_dir=tempfile.gettempdir(), png_fn=None,
             renderView=None, render=True, show=True):
    
    objs_wrapper(time=time, Bz=Bz, Psw=Psw, model=model, 
                 mpause_model=mpause_model, coord_sys=coord_sys,
                 color=color, representation=representation,
                 out_dir=out_dir, png_fn=png_fn,
                 renderView=renderView, render=render,
                 show=show, obj='Bowshock')
    
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
              show=True):
    
    objs_wrapper(time_o=time_o, time_f=time_f, satellite_id=satellite_id, 
              coord_sys=coord_sys,
              color=color,
              representation=representation,
              tube_radius=tube_radius, 
              shader_preset=shader_preset,
              region_colors=region_colors,
              out_dir=tempfile.gettempdir(),
              renderView=renderView,
              render=render,
              show=show, obj = 'satellite')
    

def axis(time, val, coord_sys='GSM', lims=[-20,20], tick_spacing=1, 
         label=True, representation = 'Surface', 
         renderView=None,render=True,show=True, debug=False):

    objs_wrapper(time=time, val=val, coord_sys=coord_sys, 
                 lims=lims, tick_spacing=tick_spacing,
                 label=label, representation=representation, 
                 renderView=renderView, render=render, show=show,
                 debug=debug, obj='axis')
    
def _axis(self, output, time, val, coord_sys, lims,
          tick_spacing, label):
    
    import numpy as np
    import numpy.matlib
    from magnetovis.objects2 import rot_mat
    from magnetovis.cxtransform import transform
    
    X = np.linspace(lims[0],lims[1], 300)
    X = X.repeat(300)
    
    r = 0.25
    
    theta = np.linspace(0,2*np.pi, 300)
    theta = np.matlib.repmat(theta, 1, 300).flatten()
    
    Y = r * np.cos(theta)
    Z = r * np.sin(theta)
    
    Y[np.floor(X)%2==0] *= .8
    Z[np.floor(X)%2==0] *= .8

    
    points = np.column_stack([X, Y, Z])
    if val == "Y":
        points = rot_mat(points, angle=90, translate=False, axis='Z')
    elif val == "Z":
        points = rot_mat(points, angle=90, translate=False, axis="Y")
        
    if coord_sys != 'GSM':
        points = transform(points, time, 'GSM', coord_sys, 'car', 'car')
    
    ############################################################
    ####### start of the code to use programmable source #######
    ############################################################
    import vtk
    if False:
        # this is never meant to run. it is only to get rid of error message
        # that output is not defined. output is defined when running
        # this script in the programmable source text box. 
        output = ''
    # communication between "script" and "script (RequestInformation)"
    executive = self.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    exts = [executive.UPDATE_EXTENT().Get(outInfo, i) for i in range(6)]
    dims = [exts[1]+1, exts[3]+1, exts[5]+1]
    
    # setting the sgrid exent
    output.SetExtent(exts)
    
    # setting up the points and allocate the number of points
    pts = vtk.vtkPoints()
    pts.Allocate(dims[0] * dims[1] * dims[2])
    
    # color sections
    # lut = pvs.GetColorTransferFunction('Magnetosphere Surface')
    # value = int(len(lut.Annotations)/2)
    # colors = vtk.vtkUnsignedCharArray()
    # colors.SetNumberOfComponents(1)
    # colors.SetName("Magnetosphere Surface")
    
    # insert points into vtkPoints
    i = 0
    for point in points:
        pts.InsertPoint(i, point[0], point[1], point[2])
        i += 1
        # colors.InsertNextTuple([value])

    output.SetPoints(pts)
    # output.GetPointData().AddArray(colors)
    

def neutralsheet(time=None, psi=None, 
                 Rh=8, G=10, Lw=10, d=4,
                 xlims = (-40,-5), ylims = (-15,15),
                 coord_sys='GSM',
                 model='tsyganenko95',
                 color = [1,0,0,0.5],
                 representation='Surface',
                 out_dir=tempfile.gettempdir(), png_fn=None,
                 return_sheet=False,
                 renderView=None,
                 render=True,
                 show=True,
                 debug=False):
    objs_wrapper(time=time, psi=psi, Rh=Rh, G=G, Lw=Lw, d=d, xlims=xlims,
                 ylims=ylims, coord_sys=coord_sys, model=model, color=color,
                 representation=representation,
                 out_dir=out_dir, png_fn=png_fn,
                 return_sheet=return_sheet,
                 renderView=renderView, render=render, show=show, debug=debug,
                 obj='Neutralsheet')
    
# used to execute code inside of the programmable source script box.
if False:
    # the assignment below is to get rid of warning and error messages.
    kwargs = '' 
    # the variables below are defined inside of programmable source not here.
    self = ''
    output = ''


if "kwargs" in vars():         
        
    if kwargs['obj'] == 'satellite':
        _satellite(self, time_o=kwargs['time_o'], time_f=kwargs['time_f'],
                       satellite_id=kwargs['satellite_id'],
                       coord_sys=kwargs['coord_sys'],
                       region_colors=kwargs['region_colors'])
    
    elif kwargs['obj'] == 'Magnetopause':
        _magnetopause(self, output, time=kwargs['time'], Bz=kwargs['Bz'], 
                      Psw=kwargs['Psw'], model=kwargs['model'],
                      coord_sys=kwargs['coord_sys'],
                      return_x_max=kwargs['return_x_max'])
    
    elif kwargs['obj'] == 'Bowshock':
        _bowshock(self, output, time=kwargs['time'], Bz=kwargs['Bz'], 
                      Psw=kwargs['Psw'], model=kwargs['model'], 
                      mpause_model=kwargs['mpause_model'],
                      coord_sys=kwargs['coord_sys'])
    
    elif kwargs['obj'] == 'Neutralsheet':
        _neutralsheet(self, output, time=kwargs['time'], psi=kwargs['psi'], 
                      Rh=kwargs['Rh'], G=kwargs['G'], Lw=kwargs['Lw'], 
                      d=kwargs['d'], xlims=kwargs['xlims'], 
                      ylims=kwargs['ylims'], coord_sys=kwargs['coord_sys'],
                      model=kwargs['model'],
                      return_sheet=kwargs['return_sheet'])
        
    elif kwargs['obj'] == 'Plasmasheet':
        _plasmasheet(self, output, time=kwargs['time'], psi=kwargs['psi'], 
                      Rh=kwargs['Rh'], G=kwargs['G'], Lw=kwargs['Lw'], 
                      d=kwargs['d'], xlims=kwargs['xlims'], 
                      ylims=kwargs['ylims'], coord_sys=kwargs['coord_sys'],
                      model=kwargs['model'],
                      return_sheet=kwargs['return_sheet'])
    
    elif kwargs['obj'] == 'axis':
        _axis(self, output, time = kwargs['time'], val=kwargs['val'],
              coord_sys=kwargs['coord_sys'], lims=kwargs['lims'],
              tick_spacing=kwargs['label'], label=kwargs['label'])
    
    elif kwargs['obj'] == 'plasmapause':
        _plasmapause(self, output, time=kwargs['time'])
        
    elif kwargs['obj'] == 'latitude':
        _latitude_lines(self, time=kwargs['time'], coord_sys=kwargs['coord_sys'],
                        increment=kwargs['increment'], color=kwargs['color'])
        
    elif kwargs['obj'] == 'longitude':
        _longitude_lines(self, time=kwargs['time'], coord_sys=kwargs['coord_sys'],
                         increment=kwargs['increment'], color=kwargs['color'])
        
    
    
    
    
    
    
    
    
    
    
    
