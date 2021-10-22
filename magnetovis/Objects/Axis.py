# This program demonstrates how to use programmable source to create a
# VTK object that could not otherwise be created using paraview.simple.

def OutputDataSetType():

   # What is set in the drop-down menu for Output Data Set Type for a Programmable Source
   return "vtkPolyData"

def ScriptRequestInformation(self):

   # What is entered in the Script (RequestInformation) box for a Programmable Source
   pass

def Script(self, time="2001-01-01", extent=[-40., 40.], coord_sys='GSM', direction='X'):

    import vtk
    import numpy as np
    from magnetovis.structured_grid import structured_grid

    from hxform import hxform as hx

    assert isinstance(extent, list or tuple or np.ndarray), \
        'magnetovis.Axis(): Extent must be a list, tuple, or numpy.ndarray'

    extent = np.array(extent)

    assert extent[0] < extent[1], \
        'magnetovis.Axis(): Lower extent {} is larger than upper extent {}' \
            .format(extent[0], extent[1])

    if direction == 'X':
        points = np.array([[extent[0], 0.0, 0.0],[extent[1], 0.0, 0.0]])
    if direction == 'Y':
        points = np.array([[0.0, extent[0], 0.0],[0.0, extent[1], 0.0]])
    if direction == 'Z':
        points = np.array([[0.0, 0.0, extent[0]],[0.0, 0.0, extent[1]]])

    if coord_sys != 'GSM':
        assert time != None, 'magnetovis.Axis(): If coord_sys in not GSM, time cannot be None'
        points = hx.transform(points, time, 'GSM', coord_sys, 'car', 'car')

    vtkLineSource = vtk.vtkLineSource()
    vtkLineSource.SetPoint1(*points[0])
    vtkLineSource.SetPoint2(*points[1])
    vtkLineSource.SetResolution(1)
    vtkLineSource.Update()

    vtkTubeFilter = vtk.vtkTubeFilter()
    vtkTubeFilter.SetNumberOfSides(10)
    vtkTubeFilter.SetInputData(vtkLineSource.GetOutput())
    vtkTubeFilter.Update()
    vtkTubeFilterOutput = vtkTubeFilter.GetOutputDataObject(0)

    try:
        # Being executed in Programmable Source
        output = self.GetPolyDataOutput()
    except:
        # Being executed in Plugin
        from vtkmodules.vtkCommonDataModel import vtkPolyData
        output = vtkPolyData.GetData(outInfo, 0)

    output = output.ShallowCopy(vtkTubeFilterOutput)

def Display(magnetovisAxis, magnetovisAxisDisplayProperties, magnetovisAxisRenderView, **displayArguments):

    # Base this on code that is displayed by trace in ParaView GUI

    import paraview
    import paraview.simple as pvs

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
