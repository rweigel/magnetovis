# This program demonstrates how to use programmable source to create a
# VTK object that could not otherwise be created using paraview.simple.

def OutputDataSetType():

   # What is set in the drop-down menu for Output Data Set Type for a Programmable Source
   return "vtkPolyData"

def ScriptRequestInformation(self):

   # What is entered in the Script (RequestInformation) box for a Programmable Source
   pass

def Script(self, time_o="2001-01-01", time_f="2001-01-02", satellite_id='ace', coord_sys='GSM', tube_radius=1.):

    import vtk
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
    data, meta = hapi(server, satellite_id, parameters, time_o, time_f, **opts)

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

def Display(source, display, renderView, **displayArguments):

    # Base this on code that is displayed by trace in ParaView GUI

    import paraview
    import paraview.simple as pvs
    import numpy as np

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
    if "region_colors" in displayArguments:
        for name in region_colors.keys():
            if name in displayArguments['region_colors']:
                region_colors[name] = displayArguments['region_colors'][name]

    id_names = ['D_Msheath', 'N_Msheath', 'D_Msphere', 'N_Msphere',
                'D_Psphere', 'N_Psphere', 'Tail_Lobe', 'Plasma_Sh',
                'HLB_Layer', 'LLB_Layer', 'Intpl_Med']



    LUT = pvs.GetColorTransferFunction('region_id')
    LUT.InterpretValuesAsCategories = 1
    LUT.AnnotationsInitialized = 1


    annotations = []
    index_colored_list = []
    for id, name in enumerate(id_names):
        annotations.append(str(id))
        annotations.append(name)
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
    display.SetScalarBarVisibility(renderView, True)

    #pvs.ColorBy(display, ('CELLS', 'region_id'))
    #lookupTable = pvs.GetColorTransferFunction('region_id')
    #lookupTable.NumberOfTableValues = len(id_names)

    if "displayRepresentation" in displayArguments:
        display.Representation = displayArguments['displayRepresentation']

    if "opacity" in displayArguments:
        if displayArguments["opacity"] is not None:
            display.Opacity = displayArguments['opacity']

    display.AmbientColor = [0.5, 0.5, 0.5]
    if "ambientColor" in displayArguments:
        if displayArguments["ambientColor"] is not None:
            display.AmbientColor = displayArguments["ambientColor"]

    display.DiffuseColor = [0.5, 0.5, 0.5]
    if "diffuseColor" in displayArguments:
        if displayArguments["diffuseColor"] is not None:
            display.DiffuseColor = displayArguments["diffuseColor"]

    return display

def _Display(self, displayArguments):
    self.displayProperties = Display(self.programmableSource, self.displayProperties, self.renderView, **displayArguments)
