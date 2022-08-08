
# Demo 1
import paraview.simple as pvs
import magnetovis as mvs
earth = mvs.Earth(style="daynight")
pvs.Hide(earth)
earthT = mvs.Transform(x=[0, -1, 0], y=[1, 0, 0], Input=earth)
pvs.Show(earthT)
pvs.ResetCamera()

