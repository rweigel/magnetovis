def OutputDataSetType():

    # What is set in the drop-down menu for Output Data Set Type for a Programmable Source
    return "vtkPolyData"

def ScriptRequestInformation(self):

    pass

def Script(self, time="2001-01-01", coord_sys='GSM', Npts=3, point_function=None, point_array_functions=None, cell_array_functions=None):

    # What is entered in the Script box for a Programmable Source
    
    import vtk
    import numpy as np

    from magnetovis.vtk.set_arrays import set_arrays
    from magnetovis.vtk.get_arrays import get_arrays
    from hxform import hxform as hx

    if point_function is None:
        Npoints = 6
        points = np.zeros((Npoints,3))
        points[:,0] = np.arange(Npoints)
        points[:,1] = np.zeros(Npoints)
        points[:,2] = np.zeros(Npoints)
    else:
        if (len(point_function) > 1):            
            pass # TODO: Error

        function_name = list(point_function.keys())[0]
        Npts = point_function[function_name]["Npts"]
        del point_function[function_name]["Npts"]
        points = get_arrays(point_function, Npts)[function_name]

    if coord_sys != 'GSM':
        assert time != None, 'magnetovis.StructuredGrid(): If coord_sys in not GSM, time cannot be None'
        points = hx.transform(points, time, 'GSM', coord_sys, 'car', 'car')

    point_data = get_arrays(point_array_functions, points)
    #cell_data = get_arrays(cell_array_functions, cell_centers)

    try:
      # Being executed in Programmable Source
      output = self.GetPolyDataOutput()
    except:
      # Being executed in Plugin
      from vtkmodules.vtkCommonDataModel import vtkPolyData
      output = vtkPolyData.GetData(outInfo, 0)

    Npts = points.shape[0]
    Nlines = Npts - 1

    vtkPoints = vtk.vtkPoints()
    points2 = np.zeros(((Npts-2)*2 + 2, 3))
    # Duplicate interior points
    for i in range(Nlines):
        points2[2*i, :] = points[i, :]
        points2[2*i+1, :] = points[i+1, :]

    output.Allocate(Nlines, 1)
    output.SetPoints(vtkPoints)

    vtkPolyLine = vtk.vtkPolyLine()
    for i in range(Nlines):
        vtkPolyLine.GetPointIds().SetNumberOfIds(2)
        vtkPolyLine.GetPointIds().SetId(0, 2*i) 
        vtkPolyLine.GetPointIds().SetId(1, 2*i+1)
        output.InsertNextCell(vtkPolyLine.GetCellType(), vtkPolyLine.GetPointIds())

    output = set_arrays(self, output, points2, point_data=point_data)

def Display(source, display, renderView, **displayArguments):

    # Base this on code that is displayed by trace in ParaView GUI

    import paraview
    import paraview.simple as pvs

    name = 'cell_index'

    n_cells = source.GetCellDataInformation().GetArray(name).GetNumberOfTuples()

    if "displayRepresentation" in displayArguments:
        display.Representation = displayArguments['displayRepresentation']

    scalarBarVisibility = True
    if "scalarBarVisibility" in displayArguments:
        scalarBarVisibility = displayArguments['scalarBarVisibility']

    pvs.ColorBy(display, ('CELLS', name))
    lookupTable = pvs.GetColorTransferFunction(name)
    lookupTable.NumberOfTableValues = n_cells-1
    lookupTable.InterpretValuesAsCategories = 1

    display.SetScalarBarVisibility(renderView, scalarBarVisibility)

    return display


def _Display(self, displayArguments):
    self.displayProperties = Display(self.programmableSource, self.displayProperties, self.renderView, **displayArguments)
