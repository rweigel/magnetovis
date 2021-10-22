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
