def OutputDataSetType():

    return "vtkStructuredGrid"


def ScriptRequestInformation(self, dimensions=None):

    import magnetovis as mvs

    import magnetovis as mvs
    mvs.logger.info("T95CurrentSheet.ScriptRequestInformation Called.")

    if dimensions is None:
        import magnetovis as mvs
        function = "magnetovis.Sources.T95CurrentSheet.Script"
        dimensions = mvs.extract.extract_kwargs(function)['dimensions']

    dimensions.append(1)
    return mvs.Sources.GridData.ScriptRequestInformation(self, dimensions=dimensions)


def Script(time="2001-01-01T12:00:00", coord_sys='GSM', dimensions=[20, 20],
            psi=10., Rh=8., d=4., G=10., Lw=10.,
            point_function="linspace(starts=(-20., -15.), stops=(-4., 15.))",
            point_array_functions=["xyz: position()"]):

    import magnetovis as mvs
    mvs.logger.info("T95CurrentSheet.Script Called")

    assert isinstance(point_array_functions, list), "point_array_functions must be a list"
    assert isinstance(point_function, str), "point_function must be a str"
    assert len(dimensions) == 2, "Required: len(dimensions) == 2"

    import numpy as np
    import magnetovis as mvs
    import paraview.simple as pvs

    # Creates points by calling point_function with first argument of dimensions
    # an keyword arguments specified in point_function keyword argument of this
    # function (Script).
    xypoints = mvs.vtk.get_arrays(point_function, dimensions)
    points = mvs.functions.t95cs(xypoints, time=time, psi=psi, Rh=Rh, d=d, G=G, Lw=Lw)
    dimensions.append(1)

    if coord_sys != 'GSM':
        from hxform import hxform as hx
        assert time != None, 'If coord_sys in not GSM, time cannot be None'
        points = hx.transform(points, mvs.util.iso2ints(time), 'GSM', coord_sys, 'car', 'car')

    # Needed for UniformGrid, RectilinearGrid, and StructuredGrid.
    output.SetExtent([0, dimensions[0]-1, 0, dimensions[1]-1, 0, dimensions[2]-1])

    point_arrays = mvs.vtk.get_arrays(point_array_functions, points)
    mvs.vtk.set_points(output, points)
    mvs.vtk.set_arrays(output, point_data=point_arrays, include=["CellId"])
    mvs.ProxyInfo.SetInfo(pvs.GetActiveSource(), locals())


def DefaultRegistrationName(**kwargs):

    if kwargs['psi'] is None:
        arg = kwargs['time']
    else:
        arg = "$\psi$={}$^\circ$".format(kwargs['psi'])

    return "T95 Neutral Sheet/{}/{}".format(arg, kwargs['coord_sys'])


def GetDisplayDefaults():

    defaults = {
        'coloring': {
            'colorBy': ('POINTS', 'xyz', 'Z'),
            'scalarBar': {
                            'Title': "$Z$ [R$_E$]",
                            'ComponentTitle': '',
                            'HorizontalTitle': 1,
                            'Visibility': 1
                        }
            }
        }

    return defaults
