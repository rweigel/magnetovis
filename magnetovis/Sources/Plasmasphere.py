def OutputDataSetType():

    return "vtkUnstructuredGrid"


def Script(time="2001-01-01", coord_sys='SM', N=30, version=1):

    import vtk

    import magnetovis as mvs
    from magnetovis import functions as mvsfunctions
    if version == 1:
        points, cells, logDensity = mvsfunctions.plasmasphere(N=N)
    else:
        points, cells, logDensity = mvsfunctions.plasmasphere2(N=N)

    mvs.vtk.set_points(output, points)

    if coord_sys != 'SM':
        from hxform import hxform as hx
        assert time != None, 'If coord_sys in not SM, time cannot be None'
        points = hx.transform(points, mvs.util.iso2ints(time), 'SM', coord_sys, 'car', 'car')

    mvs.vtk.set_arrays(output, point_data={'H+ log density (cm^-3)': logDensity})

    output.Allocate(cells.shape[0],1)
    for row in range(cells.shape[0]):
        aHexahedron = vtk.vtkHexahedron()
        for col in range(cells.shape[1]):
            aHexahedron.GetPointIds().SetId(col, cells[row, col])
        output.InsertNextCell(aHexahedron.GetCellType(), aHexahedron.GetPointIds())


def DefaultRegistrationName(**kwargs):

    import magnetovis as mvs

    if kwargs['coord_sys'] == "SM":
        # Model is in SM and time independent so exclude time.
        return "{}/{}".format("GCC88 plasmasphere", kwargs['coord_sys'])
    else:
        # Orientation depends on time, so include it.
        return "{}/{}/{}" \
                    .format("GCC88 plasmasphere", mvs.util.trim_iso(kwargs['time']), kwargs['coord_sys'])

def GetDisplayDefaults():

    defaults = {
        'display': {
            "Representation": "Surface",
            'AmbientColor': [0.5, 0.5, 0.5],
            'DiffuseColor': [0.5, 0.5, 0.5]
        },
        'coloring': {
            'colorBy': ('POINTS', 'H+ log density (cm^-3)'),
            'scalarBar': {
                            'Title': r"H$^{+}$ log density [cm$^{-3}$]",
                            'ComponentTitle': '',
                            'HorizontalTitle': 0,
                            'Visibility': 1,
                            'ScalarBarLength': 0.8
                        },
            'colorTransferFunction': {
                                        'AutomaticRescaleRangeMode': 1,
                                        'AutomaticRescaleRangeMode': "Grow and update on 'Apply'",
                                        'NumberOfTableValues': 16
                                    }
        }
    }

    return defaults

