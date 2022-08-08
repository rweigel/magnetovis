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


def Script(time="2001-01-01T00:00:00", coord_sys='GSM',
            m=[0, 0, 1], k=1e-7, r_nan=1.0,
            dimensions=[20, 20, 20],
            point_function="linspace(starts=(-20., -10., -10.), stops=(20., 10., 10.))",
            point_array_functions=None,
            cell_array_functions=None,
            OutputDataSetType="vtkStructuredGrid"):

    import magnetovis as mvs
    mvs.logger.info("Called.")
    
    # This script builds a source by passing `output`, which is
    # in locals(), to GridData. GridData then modifies `output`.
    import importlib
    thisScript = importlib.import_module('magnetovis.Sources.Dipole')

    # Overwrite keyword arguments in GridData with the passed kwargs
    kwargs = mvs.extract.extract_kwargs(thisScript.Script, default_kwargs=locals())

    # TODO: Additional {point, cell}_array_functions can be passed.
    # Append and check that unique.
    field_fn = f"B: dipole(m={m}, k={k}, r_nan={r_nan})"
    kwargs['point_array_functions'] = [field_fn, "xyz: position()"]
    kwargs['cell_array_functions'] = [field_fn, "xyz: position()"]    
    del kwargs['m']
    del kwargs['k']
    del kwargs['r_nan']
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
                .format("Dipole", mvs.util.trim_iso(kwargs['time']), kwargs['coord_sys'])

