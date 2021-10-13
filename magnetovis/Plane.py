def OutputDataSetType():

    # What is set in the drop-down menu for Output Data Set Type for a Programmable Source
    return "vtkStructuredGrid"


def ScriptRequestInformation(self, Nx=2, Ny=2, Nz=1):

    # What is entered in the Script (RequestInformation) box for a Programmable Source
    executive = self.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    outInfo.Set(executive.WHOLE_EXTENT(), 0, Nx-1, 0, Ny-1, 0, Nz-1)


def Script(self, time="2001-01-01", normal="Z", extents=[[-40., 40.],[-40., 40.]], Nx=2, Ny=2, Nz=1, offset=0.0, coord_sys='GSM'):

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
    points = [[-40., -40.,   0.],[ 40., -40.,   0.],[-40.,  40.,   0.],[ 40.,  40.,   0.]]

    # output variable is defined in script context.
    structured_grid(self, output, points, {}) 


def _display(self, displayProperties, labels=True, opacity=.25):

    import paraview.simple as pvs

    displayProperties.Representation = 'Surface'
    displayProperties.Opacity = opacity

    #val = "XY"
    #color = [0, 1, 0.1]
    #scalar_data = 'Demo Plane'
    #scalar_data = '{} axes'.format(val)

    if False:
        lookupTable = pvs.GetColorTransferFunction('{} plane'.format(val))
        lookupTable.IndexedColors = color
        lookupTable.Annotations = ['0', val]
        lookupTable.InterpretValuesAsCategories = 1
        lookupTable.AnnotationsInitialized = 1

        displayProperties.LookupTable = lookupTable
        displayProperties.OpacityArray = ['POINTS', scalar_data]
        displayProperties.ColorArrayName = ['POINTS', scalar_data]
        #planeDisplay.SetScalarBarVisibility(renderView, True)

    return displayProperties
