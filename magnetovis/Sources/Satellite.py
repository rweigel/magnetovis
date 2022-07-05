def OutputDataSetType():

   # What is set in the drop-down menu for Output Data Set Type for a Programmable Source
   return "vtkPolyData"


def Script(self, coord_sys='GSM', start="2001-01-01T00:00:00", stop="2001-01-03T00:00:00", id='geotail', tube_radius=1.):


    import vtk
    import magnetovis

    import numpy as np
    from itertools import groupby

    from hxform import hxform as hx
    from hapiclient import hapi
    from vtk.numpy_interface import dataset_adapter as dsa

    region_id = {
                  'D_Msheath' : 0,
                  'N_Msheath' : 1,
                  'D_Msphere' : 2,
                  'N_Msphere' : 3,
                  'D_Psphere' : 4,
                  'N_Psphere' : 5,
                  'Tail_Lobe' : 6,
                  'Plasma_Sh' : 7,
                  'HLB_Layer' : 8,
                  'LLB_Layer' : 9,
                  'Intpl_Med' : 10
                }

    try:
        # Being executed in Programmable Source
        output = self.GetPolyDataOutput()
    except:
        # Being executed in Plugin
        from vtkmodules.vtkCommonDataModel import vtkPolyData
        output = vtkPolyData.GetData(outInfo, 0)

    server     = 'http://hapi-server.org/servers/SSCWeb/hapi';
    opts       = {'logging': False, 'usecache': True}
    parameters = "X_{},Y_{},Z_{},Spacecraft_Region" \
                    .format(coord_sys, coord_sys, coord_sys)

    magnetovis.logger.info("Getting data.")
    data, meta = hapi(server, id, parameters, start, stop, **opts)

    points = np.column_stack([data['X_'+coord_sys], data['Y_'+coord_sys], data['Z_'+coord_sys]])
    pvtk = dsa.numpyTovtkDataArray(points)

    pts = vtk.vtkPoints()
    pts.Allocate(points.shape[0])
    pts.SetData(pvtk)
    output.Allocate(points.shape[0])
    output.SetPoints(pts)

    polyline = vtk.vtkPolyLine()
    vtk_region_id = vtk.vtkIntArray()
    vtk_region_id.SetNumberOfComponents(1)
    vtk_region_id.SetName('region_id')
    point_id = 0
    for region, group in groupby(data['Spacecraft_Region']):
        vtk_region_id.InsertNextTuple([region_id[region.decode('UTF-8')]])
        group = list(group)
        polyline.GetPointIds().SetNumberOfIds(len(group))
        for line_id in range(len(group)):
            polyline.GetPointIds().SetId(line_id, point_id)
            point_id += 1
        output.InsertNextCell(polyline.GetCellType(), polyline.GetPointIds())
    output.GetCellData().AddArray(vtk_region_id)

    if tube_radius:
        vtkTubeFilter = vtk.vtkTubeFilter()
        vtkTubeFilter.SetNumberOfSides(10)
        vtkTubeFilter.SetInputData(output)
        vtkTubeFilter.SetRadius(tube_radius)
        vtkTubeFilter.Update()
        vtkTubeFilterOutput = vtkTubeFilter.GetOutputDataObject(0)
        output = output.DeepCopy(vtkTubeFilterOutput)


def SetDisplayProperties(source, view=None, display=None, **kwargs):

    # Base this on code that is displayed by trace in ParaView GUI

    import paraview
    import paraview.simple as pvs
    import numpy as np

    from vtk.util import numpy_support

    region_colors = {
        'D_Msheath' : (230./255, 25./255,  75./255,  0.7), # red
        'N_Msheath' : (245./255, 130./255, 48./255,  0.7), # orange
        'D_Msphere' : (255./255, 255./255, 25./255,  0.7), # yellow
        'N_Msphere' : (220./255, 190./255, 255./255, 0.7), # lavender
        'D_Psphere' : (60./255,  180./255, 75./255,  0.7), # green
        'N_Psphere' : (70./255,  240./255, 240./255, 0.7), # cyan
        'Tail_Lobe' : (0,        130./255, 200./255, 0.7), # blue
        'Plasma_Sh' : (145./255, 30./255,  180./255, 0.7), # purple
        'HLB_Layer' : (240./255, 50./255,  230./255, 0.7), # magenta
        'LLB_Layer' : (128./255, 128./255, 128./255, 0.7), # grey
        'Intpl_Med' : (255./255, 255./255, 255./255, 0.7)  # white
    }

    # Over-ride default based on input
    if "region_colors" in kwargs:
        for name in region_colors.keys():
            if name in kwargs['region_colors']:
                region_colors[name] = kwargs['region_colors'][name]

    id_names = ['D_Msheath', 'N_Msheath', 'D_Msphere', 'N_Msphere',
                'D_Psphere', 'N_Psphere', 'Tail_Lobe', 'Plasma_Sh',
                'HLB_Layer', 'LLB_Layer', 'Intpl_Med']

    id_names_labels = [
                        "Dayside\nMagnetosheath",
                        "Dayside\nMagnetosheath",
                        "Nightside\nMagnetosheath",
                        "Dayside\nMagnetosphere",
                        "Nightside\nnMagnetosphere",
                        "Dayside\nPlasmasphere",
                        "Nightside\nPlasmasphere",
                        "Tail Lobe",
                        "Plasmasheet",
                        "High-Lat. Boundary\nLayer",
                        "Low-Lat. Boundary\nLayer",
                        "Interplanetary\nMedium"
                    ]

    sourceData = paraview.servermanager.Fetch(source)
    region_ids = sourceData.GetCellData().GetArray('region_id')
    region_ids = numpy_support.vtk_to_numpy(region_ids)
    region_ids = np.unique(region_ids)

    LUT = pvs.GetColorTransferFunction('region_id')
    LUT.InterpretValuesAsCategories = 1
    LUT.AnnotationsInitialized = 1

    annotations = []
    index_colored_list = []
    for id, name in enumerate(id_names):
        if np.any(region_ids == id) == False:
            continue
        annotations.append(str(id))
        annotations.append(id_names_labels[id])
        if region_colors != None:
            index_colored_list.append(region_colors[name][0:3])
        else:
            index_colored_list.append(region_colors[name][0:3])

    LUT.Annotations = annotations
    index_colored_list = np.array(index_colored_list).flatten()
    LUT.IndexedColors = index_colored_list

    display.LookupTable = LUT
    display.OpacityArray = ['CELLS', 'region_id']
    display.ColorArrayName = ['CELLS', 'region_id']
    display.SetScalarBarVisibility(view, True)

    LookupTableColorBar = pvs.GetScalarBar(LUT, view)
    LookupTableColorBar.Title = 'Satellite Region'
    LookupTableColorBar.ComponentTitle = ''

    if "displayRepresentation" in kwargs:
        display.Representation = kwargs['displayRepresentation']

    if "opacity" in kwargs:
        if kwargs["opacity"] is not None:
            display.Opacity = kwargs['opacity']

    display.AmbientColor = [0.5, 0.5, 0.5]
    if "ambientColor" in kwargs:
        if kwargs["ambientColor"] is not None:
            display.AmbientColor = kwargs["ambientColor"]

    display.DiffuseColor = [0.5, 0.5, 0.5]
    if "diffuseColor" in kwargs:
        if kwargs["diffuseColor"] is not None:
            display.DiffuseColor = kwargs["diffuseColor"]