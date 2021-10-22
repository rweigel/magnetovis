# This program demonstrates how to use programmable source to create a
# VTK object that could not otherwise be created using paraview.simple.

def OutputDataSetType():

   # What is set in the drop-down menu for Output Data Set Type for a Programmable Source
   return "vtkPolyData"

def ScriptRequestInformation(self):

   # What is entered in the Script (RequestInformation) box for a Programmable Source
   pass

def Script(self, time_o="2001-01-01", time_f="2001-01-02", satellite_id='ace', coord_sys='GSM'):

    import vtk
    import numpy as np

    from hxform import hxform as hx
    from hapiclient import hapi
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
    opts       = {'logging': True, 'usecache': True}
    parameters = "X_{},Y_{},Z_{},Spacecraft_Region" \
                .format(coord_sys, coord_sys, coord_sys)
    data, meta = hapi(server, satellite_id, parameters, time_o, time_f, **opts)

    output.Allocate(len(data), 1)
    pts = vtk.vtkPoints()
    polyline = vtk.vtkPolyLine()
    polyline.GetPointIds().SetNumberOfIds(len(data['Spacecraft_Region']))

    for i in range(len(data['Spacecraft_Region'])):
        pts.InsertPoint(i,data['X_'+coord_sys][i], data['Y_'+coord_sys][i],
                          data['Z_'+coord_sys][i])
        polyline.GetPointIds().SetId(i,i)
    output.InsertNextCell(polyline.GetCellType(), polyline.GetPointIds())
    output.SetPoints(pts)

    vtk_region_id = vtk.vtkIntArray()
    vtk_region_id.SetNumberOfComponents(1)
    vtk_region_id.SetName(satellite_id + ' Spacecraft Region')

    for region in data['Spacecraft_Region']:
        if region_id == None:
            vtk_region_id.InsertNextTuple([0])
        else:
            vtk_region_id.InsertNextTuple([region_id[region.decode('UTF-8')]])
    output.GetPointData().AddArray(vtk_region_id)

def Display(source, display, renderView, **displayArguments):

    # Base this on code that is displayed by trace in ParaView GUI

    import paraview
    import paraview.simple as pvs

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
        for idx, name in enumerate(region_colors.items()):
            if name in displayArguments['region_colors']:
                region_colors[name] = displayArguments['region_colors'][name]

    id_names = ['D_Msheath', 'N_Msheath', 'D_Msphere', 'N_Msphere',
                'D_Psphere', 'N_Psphere', 'Tail_Lobe', 'Plasma_Sh',
                'HLB_Layer', 'LLB_Layer', 'Intpl_Med']


    if False:

        LUT = pvs.GetColorTransferFunction('region_id')
        LUT.InterpretValuesAsCategories = 1
        LUT.AnnotationsInitialized = 1


        for id in id_names:
            color = region_colors[id_names[id]][0:3]
            # Set color in lookup table
        annotations = []
        index_colored_list = []
        for id in range(len(id_names)):
            annotations.append(str(id))
            annotations.append(unique_regions[i])
            if kwargs['region_colors'] != None:
                index_colored_list.append(region_colors[id][0:3])
            else:
                index_colored_list.append(kwargs['color'][0:3])

        LUT.Annotations = annotations
        index_colored_list = np.array(index_colored_list).flatten()
        LUT.IndexedColors = index_colored_list

        programmableSourceDisplay.LookupTable = LUT
        programmableSourceDisplay.OpacityArray = ['POINTS', scalar_data]
        programmableSourceDisplay.ColorArrayName = ['POINTS', scalar_data]
        programmableSourceDisplay.SetScalarBarVisibility(renderView, True)

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
