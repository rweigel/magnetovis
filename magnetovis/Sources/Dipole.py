def OutputDataSetType():

    import magnetovis as mvs
    mvs.logger.info("Called.")

    import importlib
    OutputDataSetType = importlib.import_module('magnetovis.Sources.GridData').OutputDataSetType()

    #OutputDataSetType = mvs.extract.extract_kwargs("magnetovis.Sources.T89c.Script")['OutputDataSetType']

    return OutputDataSetType


def ScriptRequestInformation(self, dimensions=None):

    import magnetovis as mvs

    mvs.logger.info("Called.")

    import importlib
    outInfo = importlib.import_module('magnetovis.Sources.GridData').ScriptRequestInformation(self, dimensions=dimensions)

    if False:
	    if dimensions is None:
	        import magnetovis
	        dimensions = magnetovis.extract.extract_kwargs("magnetovis.Sources.GridData.Script")['dimensions']

	    mvs.logger.info("dimensions = [{}, {}, {}]".format(dimensions[0], dimensions[1], dimensions[2]))
	    executive = self.GetExecutive()
	    outInfo = executive.GetOutputInformation(0)
	    outInfo.Set(executive.WHOLE_EXTENT(), 0, dimensions[0]-1, 0, dimensions[1]-1, 0, dimensions[2]-1)


def Script(time="2001-01-01T00:00:00", coord_sys='GSM', dimensions=[20, 20, 20],
            point_function="linspace(starts=(-20., -10., -10.), stops=(20., 10., 10.))",
            point_array_functions=["B: dipole()", "xyz: position()"],
            cell_array_functions=["B: dipole()", "xyz: position()"],
            OutputDataSetType="vtkStructuredGrid"):

    import magnetovis as mvs
    mvs.logger.info("Called.")

    # This script builds a source by passing `output`, which is
    # in locals(), to GridData. GridData then modifies `output`.
    import importlib
    thisScript = importlib.import_module('magnetovis.Sources.T89c')

    # Over-write keyword arguments in GridData with the passed kwargs
    kwargs = mvs.extract.extract_kwargs(thisScript.Script, default_kwargs=locals())

    GridData = importlib.import_module('magnetovis.Sources.GridData')
    GridData.Script(**kwargs, xoutput=output)


def GetDisplayDefaults():

    defaults = {
        'display': {
            "Representation": "Surface",
            'AmbientColor': [0.5, 0.5, 0.5],
            'DiffuseColor': [0.5, 0.5, 0.5]
        },
        'coloring': {
            'colorBy': ('CELLS', 'B'),
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
                .format("Dipole", mvs.util.trim_iso(kwargs['time']), kwargs['coord_sys'])

