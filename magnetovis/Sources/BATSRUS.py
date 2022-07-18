def OutputDataSetType():

  return "vtkUnstructuredGrid"

def GetSourceDefaults(defaults, kwargs):
  """Update default kwargs for Script based on other kwargs"""

  assert 'file' in kwargs and kwargs['file'] is not None, "A file must be given"

  return kwargs

def Script(file=None, time=None, coord_sys='GSM', tmpdir=None):

  import magnetovis as mvs

  mvs.logger.info("Called.")

  mvs.logger.info("Reading " + file)
  import vtk
  reader = vtk.vtkGenericDataObjectReader()
  reader.SetFileName(file)
  reader.ReadAllScalarsOn()
  reader.ReadAllVectorsOn()
  reader.ReadAllFieldsOn()
  reader.Update()
  mvs.logger.info("Read " + file)
  output.ShallowCopy(reader.GetOutput())


def DefaultRegistrationName(**kwargs):

  import magnetovis as mvs
  
  (dirname, fname, fext) = mvs.util.fileparts(kwargs['file'])

  return "{}/{}/{}" \
              .format("BATSRUS", fname, kwargs['coord_sys'])

def GetDisplayDefaults():

  defaults = {
      'display': {
          "Representation": "Surface",
          'AmbientColor': [0.5, 0.5, 0.5],
          'DiffuseColor': [0.5, 0.5, 0.5]
      },
      'coloring': {
          'colorBy': ('CELLS', 'b'),
          'scalarBar': {
                          'Title': r"$\|\mathbf{B}\|$ [nT]",
                          'ComponentTitle': '',
                          'HorizontalTitle': 1,
                          'TitleJustification': 'Left',
                          'Visibility': 1,
                          'ScalarBarLength': 0.8
                      }
      }
  }

  return defaults

