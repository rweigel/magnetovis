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

    print(data)
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(1)
    colors.SetName(satellite_id + ' Spacecraft Region')
    region_dict = {}
    unique_regions = np.unique(data['Spacecraft_Region'])
    for i in range(len(unique_regions)):
        region_dict[unique_regions[i]] = int(i)

    for region in data['Spacecraft_Region']:
        if region_colors == None:
            colors.InsertNextTuple([0])
        else:
            colors.InsertNextTuple([region_dict[region]])
    output.GetPointData().AddArray(colors)

    output = output.ShallowCopy(pdo)

def Display(magnetovisAxis, magnetovisAxisDisplayProperties, magnetovisAxisRenderView, **displayArguments):

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

    if "displayRepresentation" in displayArguments:
        magnetovisAxisDisplayProperties.Representation = displayArguments['displayRepresentation']

    if "opacity" in displayArguments:
        if displayArguments["opacity"] is not None:
            magnetovisAxisDisplayProperties.Opacity = displayArguments['opacity']

    magnetovisAxisDisplayProperties.AmbientColor = [0.5, 0.5, 0.5]
    if "ambientColor" in displayArguments:
        if displayArguments["ambientColor"] is not None:
            magnetovisAxisDisplayProperties.AmbientColor = displayArguments["ambientColor"]

    magnetovisAxisDisplayProperties.DiffuseColor = [0.5, 0.5, 0.5]
    if "diffuseColor" in displayArguments:
        if displayArguments["diffuseColor"] is not None:
            magnetovisAxisDisplayProperties.DiffuseColor = displayArguments["diffuseColor"]

    return magnetovisAxisDisplayProperties

def _Display(self, displayArguments):
    self.displayProperties = Display(self.programmableSource, self.displayProperties, self.renderView, **displayArguments)
