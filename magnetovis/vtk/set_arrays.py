def set_arrays(output, point_data=None, cell_data=None, field_data=None,
                include=None):

    import magnetovis as mvs
    mvs.logger.info("Called.")

    import vtk
    import numpy as np
    from vtk.util import numpy_support as nps
    from vtk.numpy_interface import dataset_adapter as dsa

    if isinstance(point_data, str):
        point_data = [point_data]

    if isinstance(cell_data, str):
        cell_data = [cell_data]

    if point_data is not None:
        for name, array in point_data.items():
            mvs.logger.info("Setting point_data array named " + name)
            vtkArray = dsa.numpyTovtkDataArray(array)
            vtkArray.SetName(name)
            output.GetPointData().AddArray(vtkArray)

    if cell_data is not None:
        for name, array in cell_data.items():
            mvs.logger.info("Setting cell_data array named " + name)
            vtkArray = dsa.numpyTovtkDataArray(array)
            vtkArray.SetName(name)
            output.GetCellData().AddArray(vtkArray)

    if field_data is not None:
        import json
        for name, array in field_data.items():
            mvs.logger.debug("Setting field_data element named " + name)
            mvs.logger.debug("Element value: " + str(array))
            vtkArray = None

            if array is None:
                array = "None"

            if array is False:
                array = "False"

            if array is True:
                array = "True"

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

    if include is not None:
        all = False
        if isinstance(include, str) and include == "all":
            all = True

        if all or "PointId" in include or "CellId" in include:
            vtkIdFilter = vtk.vtkIdFilter()
            if all or "PointId" in include:
                vtkIdFilter.SetPointIds(True)
                vtkIdFilter.SetPointIdsArrayName("PointId")
            if all or "CellId" in include:
                vtkIdFilter.SetCellIds(True)
                vtkIdFilter.SetCellIdsArrayName("CellId")
            if hasattr(output, "VTKObject"):
                vtkIdFilter.SetInputDataObject(output.VTKObject)
            else:
                vtkIdFilter.SetInputDataObject(output)
            vtkIdFilter.Update()
            output.DeepCopy(vtkIdFilter.GetOutput())

        # https://vtk.org/doc/nightly/html/classvtkCellSizeFilter.html
        if "CellVolume" or "CellLength" or "CellArea" or "CellVertexCount" in include:
            vtkCellSizeFilter = vtk.vtkCellSizeFilter()
            if hasattr(output, "VTKObject"):
                vtkCellSizeFilter.SetInputDataObject(output.VTKObject)
            else:
                vtkCellSizeFilter.SetInputDataObject(output)
            # Some are only applicable when input has certain types of cells.
            # A value of zero is when calculation is not applicable.
            # For a structured grid where one of the dimensions is 1
            # CellVolume and CellArea returned as 0.
            # TODO: Determine if cell type is such that they have a volume, area, or length.
            #       If structured grid where one of the dimensions is 1, area must be computed
            #       manually. If two dimensions are 1, length must be computed manually.
            if all or "CellVolume" in include:
                vtkCellSizeFilter.SetVolumeArrayName('CellVolume')
            else:
                vtkCellSizeFilter.ComputeVolumeOff()
            if all or "CellVertexCount" in include:
                vtkCellSizeFilter.SetVertexCountArrayName('CellVertexCount')
            else:
                vtkCellSizeFilter.ComputeVertexCountOff()
            if all or "CellLength" in include:
                vtkCellSizeFilter.SetLengthArrayName('CellLength')
            else:
                vtkCellSizeFilter.ComputeLengthOff()
            if all or "CellArea" in include:
                vtkCellSizeFilter.SetLengthArrayName('CellArea')
            else:
                vtkCellSizeFilter.ComputeAreaOff()
            vtkCellSizeFilter.ComputeSumOff()
            vtkCellSizeFilter.Update()
            output.DeepCopy(vtkCellSizeFilter.GetOutput())

        if all or "CellCenter" in include:
            vtkCellCenters = vtk.vtkCellCenters()
            if hasattr(output, "VTKObject"):
                vtkCellCenters.SetInputDataObject(output.VTKObject)
            else:
                vtkCellCenters.SetInputDataObject(output)
            vtkCellCenters.Update()
            cell_points = dsa.WrapDataObject(vtkCellCenters.GetOutput()).Points
            centers = nps.numpy_to_vtk(cell_points)
            centers.SetName('CellCenter')
            output.GetCellData().AddArray(centers)
