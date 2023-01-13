def Script(x=[1, 0, 0], y=[0, 1, 0], z=[0, 0, 1], _output=None, _inputs=None):

    import magnetovis as mvs
    mvs.logger.info("Called.")

    if _output is not None:
        output = _output
        inputs = _inputs

    matrix = [*x, 0, *y, 0, *z, 0, 0, 0, 0, 1]

    import vtk
    transform = vtk.vtkTransform()
    transform.SetMatrix(matrix)
    mvs.logger.info("Tranform matrix = {}".format(transform.GetMatrix()))
    transformFilter = vtk.vtkTransformFilter()
    transformFilter.SetTransform(transform)
    transformFilter.SetInputDataObject(inputs[0].VTKObject)
    transformFilter.Update()

    output.ShallowCopy(transformFilter.GetOutputDataObject(0))

    #<paraview.vtk.numpy_interface.dataset_adapter.PointSet object at 0x14de43f70>
    #[<paraview.vtk.numpy_interface.dataset_adapter.PointSet object at 0x14de43fd0>]
    #<paraview.vtk.numpy_interface.dataset_adapter.PointSet object at 0x14de43f70>


def DefaultRegistrationName(**kwargs):

    import magnetovis as mvs

    x = mvs.util.trim_nums(kwargs['x'], 3, style='string')
    y = mvs.util.trim_nums(kwargs['y'], 3, style='string')
    z = mvs.util.trim_nums(kwargs['z'], 3, style='string')

    return "{}/x={}/y={}/z={}".format("Transform", x, y, z)
