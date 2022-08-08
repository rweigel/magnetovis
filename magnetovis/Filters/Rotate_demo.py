
# Demo 1
import paraview.simple as pvs
import magnetovis as mvs
a = mvs.Axis()
# Default is to rotate around Z
cR = mvs.Rotate(Input=a, angle=90) 
pvs.Show(cR)
pvs.ResetCamera()

# Demo 2
import paraview.simple as pvs
import magnetovis as mvs
mvs.CreateViewAndLayout()
a = mvs.Axis()
aR = mvs.Rotate(Input=a, angle=90, axis="Y")
pvs.Show(aR)
pvs.ResetCamera()

# Demo 3
import paraview.simple as pvs
import magnetovis as mvs
mvs.CreateViewAndLayout()
a = mvs.Axis()
aR = mvs.Rotate(Input=a, angle=89.999999, axis=[1, 1, 0])
pvs.Show(aR)
pvs.ResetCamera()
