def OutputDataSetType():

  return "vtkUnstructuredGrid"


def Script(file='http://mag.gmu.edu/git-data/swmfio/3d__var_2_e20190902-041000-000',
           time=None, coord_sys='GSM', tmpdir=None):

  # TOOD: Derive time from the contents of the file.

  import magnetovis as mvs

  mvs.logger.info("Called.")

  (dirname, fname, fext) = mvs.util.fileparts(file)

  if file.startswith("http"):
      for ext in ['.tree', '.info', '.out']:
        tmpfile = mvs.util.dlfile(dirname + "/" + fname + ext, tmpdir=tmpdir)
        (dirname, fname, fext) = mvs.util.fileparts(tmpfile)
  else:
      (dirname, fname, fext) = mvs.util.fileparts(file)

  import os
  vtkfile = os.path.join(dirname, fname, '.vtk')
  basename = os.path.join(dirname, fname)
  vtkfile = basename + '.vtk'
  if not os.path.exists(vtkfile):
      import swmfio # ParaView crashes on OS-X 10.15 Intel, but not OS-X 12.4 M1
      print("Creating vtk file using " + basename + ".{tree,info,out}")
      swmfio.write_vtk(basename)


  import vtk
  reader = vtk.vtkGenericDataObjectReader()
  reader.SetFileName(vtkfile)

  if False:
    # TODO: Based on the ReadAllScalarsOn() and ReadAllVectorsOn(), 
    # it would seem that only single vector or scalar could be read.
    # It may be useful to allow one to pass the variable to be read
    # as a kwarg to this function.
    # In Python, something like (Does not work)
    import vtk
    # https://github.com/Kitware/VTK/blob/master/IO/Legacy/vtkDataReader.cxx#L712
    reader = vtk.vtkGenericDataObjectReader()
    reader.SetFileName('/tmp/3d__var_2_e20190902-041000-000.vtk')
    reader.Update()
    ro = reader.GetOutput()
    numCells = ro.GetNumberOfCells()
    print(numCells) # 5896192

    # Segfault
    # reader.ReadCellData(ro, numCells)

    # A better solution is to use the code in vtk_export.py to build
    # a VTK object here. This will save the need to obviate the need
    # for an intermediate file.

  reader.ReadAllScalarsOn()
  reader.ReadAllVectorsOn()
  reader.ReadAllFieldsOn()
  reader.Update()
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
                          'DrawNanAnnotation': 1,
                          'ScalarBarLength': 0.8
                      }
      }
  }

  return defaults

