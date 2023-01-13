def OutputDataSetType():

    # What is set in the drop-down menu for Output Data Set Type for a Programmable Source
    return "vtkUnstructuredGrid"


def Script(time="2001-01-01", coord_sys='GSM',
            Nr=2, ro=0, rf=2,
            Nφ=4, φo=0, φf=360,
            closed=True,
            point_array_functions=None):

    # This script is to demonstrate the creation of an object
    # using VTK. This is a generalization of paraview.simple.Disk,
    # which only has options of ro and rf. (One could use
    # LinearExtrusion to achieve results similar to that in this
    # script).

    debug = False

    import vtk
    import numpy as np
    from magnetovis.vtk.set_arrays import set_arrays
    from magnetovis.vtk.set_points import set_points
    from magnetovis.vtk.get_arrays import get_arrays

    assert Nr > 0, "Nr > 0 is required"
    assert Nφ > 0, "Nφ > 0 is required"
    assert φf-φo <= 360, "φf-φo < 360 is required"
    if φf-φo == 360:
        assert Nφ > 2, "If φf-φo = 360, Nφ > 2 is required"
    assert rf - ro > 0, "rf - ro > 0 is required"
    assert φf - φo, "φf - φo <= 0 is required"

    dr = (rf - ro)/Nr
    dφ = (np.pi/180.)*(φf - φo)/Nφ

    if φf-φo < 360 and closed == True:
        import warnings
        warnings.warn("DifferentialDisk(): φf-φo < 360 and closed = True. Setting closed = False.")
        closed = False

    if closed:
        points = np.zeros((Nr*Nφ + 1, 3))
    else:
        points = np.zeros((Nr*(Nφ+1) + 1, 3))

    k = 0
    for j in range(Nφ):
        for i in range(0, Nr):
            k = k + 1
            x = (ro+(i+1)*dr)*np.cos(j*dφ)
            y = (ro+(i+1)*dr)*np.sin(j*dφ)
            points[k, 0] = x
            points[k, 1] = y

    if closed == False:
        i = i + 1
        j = j + 1
        for i in range(0, Nr):
            k = k + 1
            x = (ro+(i+1)*dr)*np.cos(j*dφ)
            y = (ro+(i+1)*dr)*np.sin(j*dφ)
            points[k, 0] = x
            points[k, 1] = y

    output.Allocate(Nφ + Nr*Nφ)

    k = 0
    for j in range(0, Nφ-1):
        triangle = vtk.vtkTriangle()
        p0 = 0
        p1 = 1+j*Nr
        p2 = 1+(j+1)*Nr
        triangle.GetPointIds().SetId(0, p0)
        triangle.GetPointIds().SetId(1, p1)
        triangle.GetPointIds().SetId(2, p2)
        if debug:
            print("Triangle; cell = {}; points = {} {} {}".format(k, p0, p1, p2))
        k = k + 1
        output.InsertNextCell(triangle.GetCellType(), triangle.GetPointIds())
        for i in range(0, Nr-1):
            quad = vtk.vtkQuad()
            p0 = 1 + i + j*Nr
            p1 = 2 + i + j*Nr
            p2 = 2 + i + Nr + j*Nr
            p3 = 1 + i + Nr + j*Nr
            quad.GetPointIds().SetId(0, p0)
            quad.GetPointIds().SetId(1, p1)
            quad.GetPointIds().SetId(2, p2)
            quad.GetPointIds().SetId(3, p3)
            if debug:
                print("Quad;     cell = {}; points = {} {} {} {}".format(k, p0, p1, p2, p3))
            k = k + 1
            output.InsertNextCell(quad.GetCellType(), quad.GetPointIds())

    if debug:
        print("\nLast φ (closed = " + str(closed) + "):")
    j = j + 1

    # Last triangle
    triangle = vtk.vtkTriangle()
    p0 = 0
    p1 = 1 + j*Nr
    if closed:
        # Third point of last triangle connects to second point of first triangle
        p2 = 1
    else:
        # Third point of last triangle connects to added point
        p2 = 1+(j+1)*Nr
    triangle.GetPointIds().SetId(0, p0)
    triangle.GetPointIds().SetId(1, p1)
    triangle.GetPointIds().SetId(2, p2)
    if debug:
        print("Triangle; cell = {}; points = {} {} {}".format(k, p0, p1, p2))
    k = k + 1
    output.InsertNextCell(triangle.GetCellType(), triangle.GetPointIds())

    # Last quads
    for i in range(0, Nr-1):
        quad = vtk.vtkQuad()
        p0 = 1 + i + j*Nr
        p1 = 2 + i + j*Nr
        p2 = 2 + i + Nr + j*Nr
        p3 = 1 + i + Nr + j*Nr
        if closed:
            p2 = 2 + i
            p3 = 1 + i
        else:
            p2 = 2 + i + Nr + j*Nr
            p3 = 1 + i + Nr + j*Nr
        quad.GetPointIds().SetId(0, p0)
        quad.GetPointIds().SetId(1, p1)
        quad.GetPointIds().SetId(2, p2)
        quad.GetPointIds().SetId(3, p3)
        if debug:
            print("Quad;     cell = {}; points = {} {} {} {}".format(k, p0, p1, p2, p3))
        k = k + 1
        output.InsertNextCell(quad.GetCellType(), quad.GetPointIds())

    point_arrays = get_arrays(point_array_functions, points)

    set_points(output, points)
    set_arrays(output, point_data=point_arrays, include=["CellId"])
