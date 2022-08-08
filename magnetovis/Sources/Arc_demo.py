
# Demo 1
import paraview.simple as pvs
import magnetovis as mvs
arc = mvs.Arc()
tube = pvs.Tube(arc)
pvs.Show(tube)

# Demo 2
import paraview.simple as pvs
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.Earth(coord_sys="GEO", coord_sys_view="GEO")
arc = mvs.Arc(Radisus=1.01, Direction=[0, 1, 0], StartPhi=-90, EndPhi=90)

color = [1.0, 0.0, 0.0]
tube = pvs.Tube(arc)
pvs.Show(tube, DiffuseColor=color)

text = pvs.Text(Text='Prime Meridian')
pvs.Show(text, TextPropMode='Billboard 3D Text', BillboardPosition=[0, 0, 1.05], Color=[1.0, 0.0, 0.0])

