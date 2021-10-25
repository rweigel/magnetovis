def OutputDataSetType():

    # What is set in the drop-down menu for Output Data Set Type for a Programmable Source
    return "vtkStructuredGrid"


def ScriptRequestInformation(self, Nx=2, Ny=2, Nz=1):

    # What is entered in the Script (RequestInformation) box for a Programmable Source

    # For vtkStructuredGrid this is needed. See
    # https://discourse.paraview.org/t/problem-displaying-structured-grid-when-loading-from-programmable-source/3051/2
    executive = self.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    outInfo.Set(executive.WHOLE_EXTENT(), 0, Nx-1, 0, Ny-1, 0, Nz-1)


def Script(self, time="2001-01-01", normal="Z", extents=[[-40., 40.],[-40., 40.]], offset=0.0, coord_sys='GSM', Nx=2, Ny=2, Nz=1):

    # What is entered in the Script box for a Programmable Source

    import vtk
    import numpy as np
    from magnetovis.structured_grid import structured_grid

    from hxform import hxform as hx

    assert isinstance(extents, list or tuple or np.ndarray), \
        'magnetovis.Plane(): Extent must be a list, tuple, or numpy.ndarray'

    extents = np.array(extents)

    for i in range(2):
        assert extents[i,0] < extents[i,1], \
            'magnetovis.Plane(): Lower bound {} is larger than upper bound {} for extent[{}]' \
                .format(extents[i][0], extents[i][1], i)

    if coord_sys != 'GSM':
        assert time != None, 'magnetovis.Plane(): If coord_sys in not GSM, time cannot be None'
        extents = hx.transform(extents, time, 'GSM', coord_sys, 'car', 'car')

    points = [
                [extents[0,0], extents[1,0], offset],
                [extents[0,1], extents[1,0], offset],
                [extents[0,0], extents[1,1], offset],
                [extents[1,1], extents[1,1], offset]
            ]
    #points = [[-40., -40.,   0.],[ 40., -40.,   0.],[-40.,  40.,   0.],[ 40.,  40.,   0.]]
    points = np.array(points)

    try:
        # This needs to be in the try and not except, otherwise ParaView crashes.
        # Executed if script is executed in RequestData function of Plugin
        from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
        output = vtkStructuredGrid.GetData(outInfo, 0)
        output.SetExtent([0, Nx-1, 0, Ny-1, 0, Nz-1])
    except:
        # Executed if script is executed as progammable source
        executive = self.GetExecutive()
        outInfo = executive.GetOutputInformation(0)
        exts = [executive.UPDATE_EXTENT().Get(outInfo, i) for i in range(6)]
        dims = [exts[1]+1, exts[3]+1, exts[5]+1]
        output.SetExtent(exts)

    if normal == "X":
        scalar_data = [0, 0, 0, 0]
    if normal == "Y":
        scalar_data = [1, 1, 1, 1]
    if normal == "Z":
        scalar_data = [2, 2, 2, 2]

    output = structured_grid(self, output, points, {'scalar_data': scalar_data})


def Display(magnetovisPlane, magnetovisPlaneDisplayProperties, magnetovisPlaneRenderView, **displayArguments):

    # Base this on code that is displayed by trace in ParaView GUI

    import paraview
    import paraview.simple as pvs

    name = 'scalar_data'

    if "displayRepresentation" in displayArguments:
        magnetovisPlaneDisplayProperties.Representation = displayArguments['displayRepresentation']

    if "opacity" in displayArguments:
        magnetovisPlaneDisplayProperties.Opacity = displayArguments['opacity']

    sourceData = paraview.servermanager.Fetch(magnetovisPlane)
    scalar_data = sourceData.GetPointData().GetArray(name)

    if scalar_data.GetValue(0) == 0:
        color = [1, 0, 0]
        Annotations = ['0','X']
    if scalar_data.GetValue(0) == 1:
        color = [1, 1, 0]
        Annotations = ['1','Y']
    if scalar_data.GetValue(0) == 2:
        color = [0, 1, 0]
        Annotations = ['2','Z']

    lookupTable = pvs.GetColorTransferFunction(name)
    lookupTable.IndexedColors = color
    lookupTable.Annotations = Annotations
    lookupTable.InterpretValuesAsCategories = 1
    lookupTable.AnnotationsInitialized = 1
    magnetovisPlaneDisplayProperties.LookupTable = lookupTable
    magnetovisPlaneDisplayProperties.OpacityArray = ['POINTS', name]
    magnetovisPlaneDisplayProperties.ColorArrayName = ['POINTS', name]
    magnetovisPlaneDisplayProperties.SetScalarBarVisibility(magnetovisPlaneRenderView, False)

    return magnetovisPlaneDisplayProperties


def _Display(self, displayArguments):
    self.displayProperties = Display(self.programmableSource, self.displayProperties, self.renderView, **displayArguments)

