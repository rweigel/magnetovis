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


def Script(self, time="2001-01-01", extents=[[-40., 40.],[-40., 40.],[-40., 40.]], coord_sys='GSM', Nx=2, Ny=2, Nz=2, point_functions=None):

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


    xax = np.linspace(extents[0,0],extents[0,1], Nx)
    yax = np.linspace(extents[1,0],extents[1,1], Ny)
    zax = np.linspace(extents[2,0],extents[2,1], Nz)
    Y, Z, X = np.meshgrid(yax, zax, xax)
    points = np.column_stack([X.flatten(), Y.flatten(), Z.flatten()])

    point_data = {}
    if point_functions is not None:
        import magnetovis
        for function, kwargs in point_functions.items():
            if 'name' in kwargs:
                name = kwargs['name']
                del kwargs['name']
            else:
                name = function
            # TODO: Handle duplicate name case
            # Call the function
            data = getattr(magnetovis, function)(points, **kwargs)
            point_data[name] = data

    cell_data = {'cell_index': np.arange(np.max([1,(Nx-1)])*np.max([1,(Ny-1)])*np.max([1,(Nz-1)]))}

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

    scalar_data = data    

    output = structured_grid(self, output, points, point_data=point_data, cell_data=cell_data)

    return output, outInfo


def Display(magnetovisPlane, magnetovisPlaneDisplayProperties, magnetovisPlaneRenderView, **displayArguments):

    # Base this on code that is displayed by trace in ParaView GUI

    import paraview
    import paraview.simple as pvs

    name = 'cell_index'

    n_cells = magnetovisPlane.GetCellDataInformation().GetArray(name).GetNumberOfTuples()

    if "displayRepresentation" in displayArguments:
        magnetovisPlaneDisplayProperties.Representation = displayArguments['displayRepresentation']

    pvs.ColorBy(magnetovisPlaneDisplayProperties, ('CELLS', name))
    lookupTable = pvs.GetColorTransferFunction(name)
    lookupTable.NumberOfTableValues = n_cells

    return magnetovisPlaneDisplayProperties


def _Display(self, displayArguments):
    self.displayProperties = Display(self.programmableSource, self.displayProperties, self.renderView, **displayArguments)
