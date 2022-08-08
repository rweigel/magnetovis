
# Demo 1
import paraview.simple as pvs
import magnetovis as mvs
pvs.Sphere()
mvs.SetRepresentation('Surface With Edges')
mvs.SetColor(mvs.GetColorRGB('darkblue'), EdgeColor=mvs.GetColorRGB('gold'))
