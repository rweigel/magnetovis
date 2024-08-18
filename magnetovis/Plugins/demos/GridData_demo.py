# Demo 1
import paraview.simple as pvs
pvs.Text()
grid = pvs.MagnetovisGridData()
pvs.Show(grid, view=pvs.GetActiveView())
