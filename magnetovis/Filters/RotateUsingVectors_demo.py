
# Demo 1
import paraview.simple as pvs
import magnetovis as mvs
a = mvs.Axis()
# Vector1 rotated into Vector2 corresponds to a rotation of 45° around Z
cR = mvs.RotateUsingVectors(Input=a, Vector1=[1, 1, 0], Vector2=[0, 1, 0]) 
mvs.SetTitle()
pvs.Show(cR)
mvs.SetCamera(viewType="-Z")
