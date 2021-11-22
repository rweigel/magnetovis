def OutputDataSetType():

   # What is set in the drop-down menu for Output Data Set Type for a Programmable Source
   return "vtkPolyData"


def Script(Ntheta=10, Nphi=10):

    import vtk
    output = self.GetPolyDataOutput()
    sphereSource = vtk.vtkSphereSource()
    sphereSource.SetRadius(10)
    sphereSource.SetThetaResolution(Ntheta)
    sphereSource.SetPhiResolution(Nphi)
    sphereSource.LatLongTessellationOn()
    sphereSource.Update()

    # get poly data output from vtkSphereSource
    # output is vtkPolyData
    sphereSourceOutput = sphereSource.GetOutput()

    output = output.ShallowCopy(sphereSourceOutput)
    set_points(self, output, points)
    set_arrays(self, output, point_data=point_arrays)


def SetDisplayProperties(programmableSource, renderView=None, displayProperties=None, **displayArguments):

    import paraview.simple as pvs
    import magnetovis as mvs

    import magnetovis as mvs
    mvs.ColorByCellId(programmableSource, renderView=renderView, displayProperties=displayProperties)

    renderView.ResetCamera()

    pvs.SetActiveSource(programmableSource)

