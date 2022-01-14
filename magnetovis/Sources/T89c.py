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


def Script(time="2001-01-01T00:00:00", coord_sys='GSM', dimensions=[40, 2, 40],
            point_function="linspace(starts=(-20., -1., -10.), stops=(10., 1., 10.))",
            point_array_functions=["t89c: t89c()"],
            cell_array_functions=["xyz: position()"],
            OutputDataSetType="vtkStructuredGrid"):

    import magnetovis as mvs
    mvs.logger.info("Called.")

    # Note that OutputDataSetType is not used explicitly here but is needed
    # by CreateProgrammableSource().

    assert isinstance(point_function, str), "point_function must be a str" 
    assert isinstance(point_array_functions, list), "point_array_functions must be a list"
    assert isinstance(cell_array_functions, list), "cell_array_functions must be a list"

    import paraview.simple as pvs
    import magnetovis as mvs

    # Get NumPy array by calling point_function with `arg[0]` or `dimensions`.
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

    # Get Python list of NumPy arrays. Element `i` of list is return value
    # from a call to `point_array_functions[i]` with `arg[0]` of `points`.
    point_arrays = mvs.vtk.get_arrays(point_array_functions, points)

    # Add points to the VTK object `output` after converting `points` to VTK arrays. 
    mvs.vtk.set_points(output, points, dimensions=dimensions)

    # Add point data and cell data to `output`.
    mvs.vtk.set_arrays(output, point_data=point_arrays, include=["CellId", "PointId"])

    # Attach metadata to `output`. The metadata is the value of the
    # keyword variables.
    mvs.ProxyInfo.SetInfo(pvs.GetActiveSource(), locals())

def GetDisplayDefaults():

    defaults = {
        'display': {
            "Representation": "Surface",
            'AmbientColor': [0.5, 0.5, 0.5],
            'DiffuseColor': [0.5, 0.5, 0.5]
        },
        'coloring': {
            'colorBy': ('POINTS', 't89c'),
            'scalarBar': {
                            'Title': "$|\\mathbf{B}|$ [nT]",
                            'ComponentTitle': '',
                            'HorizontalTitle': 1,
                            'TitleJustification': 'Left',
                            'Visibility': 1,
                            'DrawNanAnnotation': 1,
                            'ScalarBarLength': 0.9
                        },
            'colorTransferFunction': {
                                        'UseLogScale': 1,
                                        'AutomaticRescaleRangeMode': 1,
                                        'AutomaticRescaleRangeMode': "Grow and update on 'Apply'",
                                        'NumberOfTableValues': 16
                                    }
        }
    }

    return defaults


def DefaultRegistrationName(**kwargs):

    import magnetovis as mvs

    return "{}/{}/{}" \
                .format(kwargs['OutputDataSetType'], mvs.util.trim_iso(kwargs['time']), kwargs['coord_sys'])

