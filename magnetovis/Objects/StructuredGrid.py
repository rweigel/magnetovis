def OutputDataSetType():

    # What is set in the drop-down menu for Output Data Set Type for a Programmable Source
    return "vtkStructuredGrid"


def ScriptRequestInformation(self, Nx=2, Ny=2, Nz=2):

    # What is entered in the Script (RequestInformation) box for a Programmable Source

    # For vtkStructuredGrid this is needed. See
    # https://discourse.paraview.org/t/problem-displaying-structured-grid-when-loading-from-programmable-source/3051/2
    executive = self.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    outInfo.Set(executive.WHOLE_EXTENT(), 0, Nx-1, 0, Ny-1, 0, Nz-1)


def Script(self, time="2001-01-01", extents=[[-1.5, 1.5],[-1.5, 1.5],[-1.5, 1.5]], coord_sys='GSM', Nx=3, Ny=3, Nz=3, point_array_functions=None):

    # What is entered in the Script box for a Programmable Source
    
    import vtk
    import numpy as np
    from magnetovis.vtk.set_arrays import set_arrays
    from magnetovis.vtk.get_arrays import get_arrays

    from hxform import hxform as hx

    assert isinstance(extents, list or tuple or np.ndarray), \
        'magnetovis.StructuredGrid(): Extent must be a list, tuple, or numpy.ndarray'

    extents = np.array(extents)

    for i in range(2):
        assert extents[i,0] < extents[i,1], \
            'magnetovis.StructuredGrid(): Lower bound {} is larger than upper bound {} for extent[{}]' \
                .format(extents[i][0], extents[i][1], i)

    xax = np.linspace(extents[0,0],extents[0,1], Nx)
    yax = np.linspace(extents[1,0],extents[1,1], Ny)
    zax = np.linspace(extents[2,0],extents[2,1], Nz)
    Y, Z, X = np.meshgrid(yax, zax, xax)
    points = np.column_stack([X.flatten(), Y.flatten(), Z.flatten()])

    if coord_sys != 'GSM':
        assert time != None, 'magnetovis.StructuredGrid(): If coord_sys in not GSM, time cannot be None'
        points = hx.transform(points, time, 'GSM', coord_sys, 'car', 'car')

    point_data = get_arrays(point_array_functions, points)
    #cell_data = get_arrays(cell_array_functions, cell_centers)

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

    output = set_arrays(self, output, points, point_data=point_data)

def Display(source, display, renderView, **displayArguments):

    # Base this on code that is displayed by trace in ParaView GUI

    import paraview
    import paraview.simple as pvs

    name = 'cell_index'

    n_cells = source.GetCellDataInformation().GetArray(name).GetNumberOfTuples()

    if "displayRepresentation" in displayArguments:
        display.Representation = displayArguments['displayRepresentation']

    scalarBarVisibility = True
    if "scalarBarVisibility" in displayArguments:
        scalarBarVisibility = displayArguments['scalarBarVisibility']

    pvs.ColorBy(display, ('CELLS', name))
    lookupTable = pvs.GetColorTransferFunction(name)
    lookupTable.NumberOfTableValues = n_cells-1
    lookupTable.InterpretValuesAsCategories = 1

    display.SetScalarBarVisibility(renderView, scalarBarVisibility)

    return display


def _Display(self, displayArguments):
    self.displayProperties = Display(self.programmableSource, self.displayProperties, self.renderView, **displayArguments)
