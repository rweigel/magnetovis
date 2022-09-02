def OutputDataSetType():

  return "vtkPolyData"


def Script(_output=None):

  if _output is not None:
    output = _output
    inputs = [_output]

  import vtk
  from vtk.util import numpy_support as vn
  import magfli as mf

  # Pull start points for tracing field lines from line source  
  line = inputs[1].VTKObject
  start_pts = vn.vtk_to_numpy(line.GetPoints().GetData())
  
  # Initialize field line tracing algorithm
  fl = mf.fieldlines_cartesian_unstructured_VTK(vtkData = inputs[0].VTKObject,
            Stop_Function = mf.trace_stop_earth, 
            tol = 1e-5, 
            grid_spacing = 0.01, 
            max_length = 100, 
            method_ode = 'RK23',
            method_interp = 'nearest',
            start_pts = None,
            direction = None,
            F_field = 'b',
            cell_centers = None)

  # We need to convert start_pts from np.array to list, which is what
  # set_start_points expects.
  # And we need to set the direction of the integration
  fl.set_start_points(start_pts.tolist(), mf.integrate_direction.both)

  # Setup multitrace for tracing field lines
  fl.trace_field_lines()

  fl.convert_to_vtk()

  output.ShallowCopy(fl.vtk_polydata)
