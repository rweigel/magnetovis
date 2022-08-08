def OutputDataSetType():

    import magnetovis as mvs
    mvs.logger.info("Called.")

    import importlib
    OutputDataSetType = importlib.import_module('magnetovis.Sources.GridData').OutputDataSetType()

    return OutputDataSetType


def ScriptRequestInformation(self, dimensions=None):

    import magnetovis as mvs

    mvs.logger.info("Called.")

    import importlib
    outInfo = importlib.import_module('magnetovis.Sources.GridData').ScriptRequestInformation(self, dimensions=dimensions)


def Script(time="2001-03-22T12:00:00", coord_sys='GSM', dimensions=[20, 20, 20],
            iopt=1, ps=None,
            point_function="linspace(starts=(-20., -10., -10.), stops=(20., 10., 10.))",
            point_array_functions=["B: t89c(iopt=0, ps=0.0)", "xyz: position()"],
            cell_array_functions=["B: t89c(iopt=0, ps=0.0)", "xyz: position()"],
            OutputDataSetType="vtkStructuredGrid"):

    import magnetovis as mvs
    mvs.logger.info("Called.")

    # TODO: The function used to generate the field is from
    # https://github.com/tsssss/geopack
    # This uses a native Python re-write of the Fortran code and
    # is much slower than native Fortran. A start of code that
    # wraps the native Fortran and does the looping in Fortran
    # is at https://github.com/rweigel/fastfield.
    # (SpacePy wraps the native Fortran, but the looping is done in Python,
    # which makes it significantly slower than doing the loop in Fortran.)

    # ut = Seconds since Unix time epoch start (1970-01-01)
    # ut = 59 => # 1970-01-01T00:00:59 UT

    import datetime
    time_ints = mvs.util.iso2ints(time)
    ut = (datetime.datetime(*time_ints[0:6])-datetime.datetime(1970,1,1)).total_seconds()    

    # This script builds a source by passing `output`, which is
    # in locals(), to GridData. GridData then modifies `output`.
    import importlib
    thisScript = importlib.import_module('magnetovis.Sources.T89c')

    # Overwrite keyword arguments in GridData with the passed kwargs
    kwargs = mvs.extract.extract_kwargs(thisScript.Script, default_kwargs=locals())

    # TODO: Additional {point, cell}_array_functions can be passed.
    # Append and check that unique.
    field_fn = f"B: t89c(ut={ut}, iopt={iopt}, ps={ps})"
    kwargs['point_array_functions'] = [field_fn, "xyz: position()"]
    kwargs['cell_array_functions'] = [field_fn, "xyz: position()"]
    del kwargs['iopt']
    del kwargs['ps']
    GridData = importlib.import_module('magnetovis.Sources.GridData')
    GridData.Script(**kwargs, xoutput=output)


def GetPresentationDefaults():

    defaults = {
        'display': {
            "Representation": "Surface",
            'AmbientColor': [0.5, 0.5, 0.5],
            'DiffuseColor': [0.5, 0.5, 0.5]
        },
        'coloring': {
            'colorBy': ('CELLS', 'B'),
            'scalarBar': {
                            'Title': r"$\|\mathbf{B}\|$ [nT]",
                            'ComponentTitle': '',
                            'HorizontalTitle': 1,
                            'TitleJustification': 'Left',
                            'Visibility': 1,
                            'DrawNanAnnotation': 1,
                            'ScalarBarLength': 0.8
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
                .format("T89c", mvs.util.trim_iso(kwargs['time']), kwargs['coord_sys'])

