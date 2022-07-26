def OutputDataSetType():

    return "vtkPolyData"


def Script(time="2001-01-01T00:00:00", coord_sys='GSM', model='Fairfield71'):

  import magnetovis as mvs

  mvs.logger.info("Called.")

  points = mvs.functions.bowshock('Fairfield71')

  print(points)

  Npts = points.shape[0]

  vtkPolyLine = vtk.vtkPolyLine()
  vtkPolyLine.GetPointIds().SetNumberOfIds(Npts)
  for i in range(Npts):
    vtkPolyLine.GetPointIds().SetId(i, i) 

  output.Allocate(1, 1)
  output.InsertNextCell(vtkPolyLine.GetCellType(), vtkPolyLine.GetPointIds())

  mvs.vtk.set_points(output, points)


def DefaultRegistrationName(**kwargs):

    import magnetovis as mvs

    str_list = [kwargs['model'], mvs.util.trim_iso(kwargs['time']), kwargs['coord_sys']]

    return "Bowshock-{}/{}/{}".format(*str_list)

