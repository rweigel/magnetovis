def OutputDataSetType():

    import magnetovis as mvs
    mvs.logger.info("Called.")

    OutputDataSetType = mvs.extract.extract_kwargs("magnetovis.Sources.GridData.Script")['OutputDataSetType']

    return OutputDataSetType


def ScriptRequestInformation(self, dimensions=None):

    # Needed for UniformGrid, RectilinearGrid, and StructuredGrid. See
    #   https://discourse.paraview.org/t/problem-displaying-structured-grid-when-loading-from-programmable-source/3051/2
    # and comment above SetExtent call in the following function (Script).

    import magnetovis as mvs

    mvs.logger.info("Called.")

    if dimensions is None:
        import magnetovis
        dimensions = magnetovis.extract.extract_kwargs("magnetovis.Sources.GridData.Script")['dimensions']

    mvs.logger.info("dimensions = [{}, {}, {}]".format(dimensions[0], dimensions[1], dimensions[2]))
    executive = self.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    outInfo.Set(executive.WHOLE_EXTENT(), 0, dimensions[0]-1, 0, dimensions[1]-1, 0, dimensions[2]-1)

    return outInfo

def Script(time="2001-01-01T00:00:00", coord_sys="GSM", dimensions=[4, 4, 4],
            point_function="linspace(starts=(0., 0., 0.), stops=(1., 1., 1.))",
            point_array_functions=["xyz: position()"],
            cell_array_functions=["xyz: position()"],
            OutputDataSetType="vtkStructuredGrid",
            xoutput=None):

    # The keyword argument OutputDataSetType is not used explicitly here 
    # but is needed by CreateProgrammableSource(), which reads this
    # script to buid a Programmable Source.

    if xoutput is not None:
        output = xoutput

    import magnetovis as mvs
    mvs.logger.info("Called.")

    assert isinstance(point_function, str), "point_function must be a str" 
    assert isinstance(point_array_functions, list), "point_array_functions must be a list"
    assert isinstance(cell_array_functions, list), "cell_array_functions must be a list"

    import magnetovis as mvs

    # Get NumPy array by calling point_function with `arg[0]` of `dimensions`
    # and keyword arguments given in the point_function string.
    # NumPy array will have size=(np.prod(dimensions), 3)
    points = mvs.vtk.get_arrays(point_function, dimensions)

    if coord_sys != 'GSM':
        from hxform import hxform as hx
        assert time != None, 'If coord_sys in not GSM, time cannot be None'
        points = hx.transform(points, mvs.util.iso2ints(time), 'GSM', coord_sys, 'car', 'car')

    # The following is needed for OutputDataSetTypes of ImageData, RectilinearGrid,
    # and StructuredGrid. Extents are used in the VTK pipeline. See
    #   https://vtk.org/pipermail/vtkusers/2017-January/097628.html
    # and search for "WholeExtent" in
    #   https://gitlab.kitware.com/vtk/textbook/raw/master/VTKBook/VTKTextBook.pdf
    output.SetExtent([0, dimensions[0]-1, 0, dimensions[1]-1, 0, dimensions[2]-1])

    # Add points to the VTK object `output` after converting `points` to VTK arrays. 
    mvs.vtk.set_points(output, points, dimensions=dimensions)

    # Get Python list of NumPy arrays. Element `i` of list is return value
    # from a call to `point_array_functions[i]` with `arg[0]` of `points`
    # and keyword arguments given in point_array_functions[i].
    point_arrays = None
    if point_array_functions is not None:
        point_arrays = mvs.vtk.get_arrays(point_array_functions, points)

    cell_arrays = None
    if cell_array_functions is not None:
        centers = mvs.vtk.get_centers(output)
        cell_arrays = mvs.vtk.get_arrays(cell_array_functions, centers)

    # Add point data and cell data to `output`.
    mvs.vtk.set_arrays(output, point_data=point_arrays, cell_data=cell_arrays, include=["CellId", "PointId"])

    # Attach metadata to `output`. The metadata is the value of the
    # keyword variables.
    mvs.ProxyInfo.SetInfo(output, locals())


def DefaultRegistrationName(**kwargs):

    import magnetovis as mvs

    return "{}/{}/{}" \
                .format(kwargs['OutputDataSetType'], mvs.util.trim_iso(kwargs['time']), kwargs['coord_sys'])

