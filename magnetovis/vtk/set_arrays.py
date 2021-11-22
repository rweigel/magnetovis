def set_arrays(output, point_data=None, cell_data=None, field_data=None):

    import logging

    import vtk
    from vtk.numpy_interface import dataset_adapter as dsa

    if isinstance(point_data, str):
        point_data = [point_data]

    if isinstance(cell_data, str):
        cell_data = [point_data]

    if point_data is not None:
        for name, array in point_data.items():
            logging.info("set_arrays(): setting point_data array named " + name)
            vtkArray = dsa.numpyTovtkDataArray(array)
            vtkArray.SetName(name)
            output.GetPointData().AddArray(vtkArray)

    if cell_data is not None:
        for name, array in cell_data.items():
            logging.info("set_arrays(): setting cell_data array named " + name)
            vtkArray = dsa.numpyTovtkDataArray(array)
            vtkArray.SetName(name)
            output.GetCellData().AddArray(vtkArray)

    if field_data is not None:
        import json
        for name, array in field_data.items():
            logging.info("set_arrays(): setting field_data element named " + name)
            logging.info("set_arrays(): element: " + str(array))
            vtkArray = None
            if isinstance(array, str):
                vtkArray = vtk.vtkStringArray()
                vtkArray.SetNumberOfTuples(1)
                vtkArray.SetValue(0, array)
            if isinstance(array, int):
                vtkArray = vtk.vtkIntArray()
                vtkArray.SetNumberOfTuples(1)
                vtkArray.SetValue(0, array)
            if isinstance(array, float):
                vtkArray = vtk.vtkFloatArray()
                vtkArray.SetNumberOfTuples(1)
                vtkArray.SetValue(0, array)
            if isinstance(array, tuple) or isinstance(array, list):
                if isinstance(array[0], str):
                    vtkArray = vtk.vtkStringArray()
                    vtkArray.SetNumberOfComponents(1)
                    vtkArray.SetNumberOfTuples(len(array))
                    for i in range(len(array)):
                        vtkArray.SetValue(i, array[i])
                if isinstance(array[0], float):
                    vtkArray = vtk.vtkFloatArray()
                    vtkArray.SetNumberOfComponents(len(array))
                    vtkArray.InsertTuple(0, array)
                if isinstance(array[0], int):
                    vtkArray = vtk.vtkIntArray()
                    vtkArray.SetNumberOfComponents(len(array))
                    vtkArray.InsertTuple(0, array)

            if isinstance(array, dict):
                vtkArray = vtk.vtkStringArray()
                vtkArray.SetNumberOfTuples(1)
                vtkArray.SetValue(0, json.dumps(array))

            assert vtkArray is not None, 'Unrecognized data type. Field data must be str, int, float, tuple, list, or dict.'

            vtkArray.SetName(name)
            output.GetFieldData().AddArray(vtkArray)


    # Add special arrays
    # TODO: Use the filter CellSize and CellCenters
    import numpy as np
    Ncells = output.GetNumberOfCells()
    logging.info("set_arrays(): Ncells = " + str(Ncells))
    vtkArray = dsa.numpyTovtkDataArray(np.arange(Ncells))
    vtkArray.SetName('CellIds')
    output.GetCellData().AddArray(vtkArray)
