def _source_output_data_type():

    # What is set in the drop-down menu for Output Data Set Type
    return "vtkStructuredGrid"


def _source_request_information(a=None, Nx=2, Ny=2, Nz=1):

    # What is entered in the Script (RequestInformation) box

    import vtk
    vtkInformationVector = vtk.vtkInformationVector()

    executive = self.GetExecutive()
    outInfo = executive.GetOutputInformation(0)

    vtkInformationVector.Append(outInfo)
    vtkDataSet = vtk.vtkDataSet.GetData(vtkInformationVector, 0)
    vtkDataSetDims = vtkDataSet.GetDimensions()
    print(vtkDataSetDims)
    
    outInfo.Set(executive.WHOLE_EXTENT(), 0, vtkDataSetDims[0]-1, 0, vtkDataSetDims[1]-1, 0, vtkDataSetDims[2]-1)


def _source(time="2001-01-01", normal="Z", extents=[[-40., 40.],[-40., 40.]], Nx=2, Ny=2, Nz=2, offset=0.0, coord_sys='GSM'):

    # What is entered in the Script box
    
    import vtk
    import numpy as np

    def structured_grid(output, points, F):

        # Convert 

        # https://discourse.paraview.org/t/problem-displaying-structured-grid-when-loading-from-programmable-source/3051/2
        import vtk
        from vtk.numpy_interface import dataset_adapter as dsa

        # Communication between "script" and "script (RequestInformation)"
        executive = self.GetExecutive()
        outInfo = executive.GetOutputInformation(0)
        exts = [executive.UPDATE_EXTENT().Get(outInfo, i) for i in range(6)]
        dims = [exts[1]+1, exts[3]+1, exts[5]+1]

        output.SetExtent(exts)

        pvtk = dsa.numpyTovtkDataArray(points)
        pts = vtk.vtkPoints()
        pts.Allocate(dims[0]*dims[1]*dims[2])
        pts.SetData(pvtk)
        output.SetPoints(pts)
        output.SetDimensions(2,2,1)
        for name, data in F.items():
            fvtk = dsa.numpyTovtkDataArray(data)
            fvtk.SetName(name)
            output.GetPointData().AddArray(fvtk)

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

    # Output is alread defined in script context.
    structured_grid(output, points, {}) 


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
