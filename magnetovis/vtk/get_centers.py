def get_centers(output):

    import vtk
    import numpy as np
    from vtk.util import numpy_support as nps
    from vtk.numpy_interface import dataset_adapter as dsa

    vtkCellCenters = vtk.vtkCellCenters()
    if hasattr(output, "VTKObject"):
        vtkCellCenters.SetInputDataObject(output.VTKObject)
    else:
        vtkCellCenters.SetInputDataObject(output)
    vtkCellCenters.Update()

    return dsa.WrapDataObject(vtkCellCenters.GetOutput()).Points
