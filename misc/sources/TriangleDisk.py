def OutputDataSetType():

    # What is set in the drop-down menu for Output Data Set Type for a Programmable Source
    return "vtkUnstructuredGrid"


def Script(time="2001-01-01", coord_sys='GSM',
            r=1, Nφ=4, φo=0, φf=360, closed=True,
            point_array_functions={"position": {}}):

    import vtk
    import numpy as np
    from magnetovis.vtk.set_arrays import set_arrays
    from magnetovis.vtk.set_points import set_points
    from magnetovis.vtk.get_arrays import get_arrays

    assert Nφ > 0, "Nφ > 0 is required"
    assert φf-φo <= 360, "φf-φo < 360 is required"
    if φf-φo == 360:
        assert Nφ > 2, "If φf-φo = 360, Nφ > 2 is required"
    assert r > 0, "r > 0 is required"
    assert φf - φo, "φf - φo <= 0 is required"

    dφ = (np.pi/180.)*(φf - φo)/Nφ

    if φf-φo < 360 and closed == True:
        # TODO: Warn
        closed = False

    if closed:
        points = np.zeros((Nφ+1, 3))
    else:
        points = np.zeros((Nφ+2, 3))

    for j in range(Nφ):
        x = r*np.cos(j*dφ)
        y = r*np.sin(j*dφ)
        points[j+1, 0] = x
        points[j+1, 1] = y

    if closed == False:
        j = j + 1
        x = r*np.cos(j*dφ)
        y = r*np.sin(j*dφ)
        points[j+1, 0] = x
        points[j+1, 1] = y

    output = self.GetUnstructuredGridOutput()
    output.Allocate(Nφ)

    for w in range(0, Nφ-1):
        triangle = vtk.vtkTriangle()
        triangle.GetPointIds().SetId(0, 0)
        triangle.GetPointIds().SetId(1, w+1)
        triangle.GetPointIds().SetId(2, w+2)
        output.InsertNextCell(triangle.GetCellType(), triangle.GetPointIds())

    # Last triangle
    w = w + 1
    triangle = vtk.vtkTriangle()
    triangle.GetPointIds().SetId(0, 0)
    triangle.GetPointIds().SetId(1, w+1)
    if closed:
        # Third point of last triangle connects to second point of first triangle
        triangle.GetPointIds().SetId(2, 1)
    else:
        # Third point of last triangle connects to added point
        triangle.GetPointIds().SetId(2, w+2)
    output.InsertNextCell(triangle.GetCellType(), triangle.GetPointIds())

    point_arrays = get_arrays(point_array_functions, points)

    set_points(output, points)
    set_arrays(output, point_data=point_arrays)


def SetDisplayProperties(programmableSource, renderView=None, displayProperties=None, **displayArguments):

    import logging
    import paraview.simple as pvs
    import magnetovis as mvs

    import magnetovis as mvs
    mvs.ColorByCellId(programmableSource, renderView=renderView, displayProperties=displayProperties)

    renderView.ResetCamera()

    pvs.SetActiveSource(programmableSource)
