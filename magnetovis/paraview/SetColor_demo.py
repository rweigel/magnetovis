
# Demo 1
import paraview.simple as pvs
# Paraview solid coloring method
s = pvs.Sphere()
pvs.Show(ColorArrayName=[None, ''], DiffuseColor=[0, 0, 1], AmbientColor=[0, 0, 1])

# Demo 2
# Magnetovis solid coloring method
import paraview.simple as pvs
import magnetovis as mvs
mvs.CreateViewAndLayout()
pvs.Sphere()
mvs.SetColor([0, 0, 1]) # Colors active proxy in active view and shows.
# or
#mvs.SetColor('blue')

# Demo 3
import paraview.simple as pvs
import magnetovis as mvs
mvs.CreateViewAndLayout()
# Paraview coloring
pvs.Text(Text="The Text")
pvs.Show(Color=[1, 0, 0])

# Demo 4
import paraview.simple as pvs
import magnetovis as mvs
mvs.CreateViewAndLayout()
# Magnetovis coloring
pvs.Text(Text="The Text")
mvs.SetColor([1, 0, 0])
# or
#mvs.SetColor('red')

# Demo 5
import paraview.simple as pvs
import magnetovis as mvs
# ParaView coloring
mvs.CreateViewAndLayout()
pvs.Ruler()
pvs.Show(Color=[1, 0, 0], AxisColor=[0, 0, 1])

# Demo 6
# Magnetovis coloring
import paraview.simple as pvs
import magnetovis as mvs
mvs.CreateViewAndLayout()
pvs.Ruler()
mvs.SetColor([1, 0, 0], AxisColor=[0, 0, 1])

# Demo 7
# ParaView coloring
import paraview.simple as pvs
import magnetovis as mvs
mvs.CreateViewAndLayout()
source = pvs.Sphere()
view = pvs.GetActiveViewOrCreate('RenderView')
rep = pvs.GetDisplayProperties(proxy=source, view=view)
rep.SetRepresentationType('Surface With Edges')
pvs.Show(DiffuseColor=[0, 0, 1], AmbientColor=[0, 0, 1], EdgeColor=[0, 1, 1])

# Demo 8
# Magnetovis coloring
import paraview.simple as pvs
import magnetovis as mvs
mvs.CreateViewAndLayout()
pvs.Sphere()
mvs.SetRepresentation('Surface With Edges')
mvs.SetColor([0, 0, 1], EdgeColor=[0, 1, 1])
