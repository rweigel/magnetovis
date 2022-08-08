
# Demo 1
import paraview.simple as pvs
import magnetovis as mvs
pvs.Sphere()
mvs.SetRepresentation('Feature Edges')
mvs.SetCamera(viewType='isometric')

# Demo 2
import paraview.simple as pvs
import magnetovis as mvs
mvs.CreateViewAndLayout()
pvs.Sphere()
mvs.SetRepresentation('Outline')
mvs.SetCamera(viewType='isometric')

# Demo 3
import paraview.simple as pvs
import magnetovis as mvs
mvs.CreateViewAndLayout()
pvs.Sphere()
mvs.SetRepresentation('Point Gaussian')
mvs.SetCamera(viewType='isometric')

# Demo 4
import paraview.simple as pvs
import magnetovis as mvs
mvs.CreateViewAndLayout()
pvs.Sphere()
mvs.SetRepresentation('Points')
mvs.SetCamera(viewType='isometric')

# Demo 5
import paraview.simple as pvs
import magnetovis as mvs
mvs.CreateViewAndLayout()
pvs.Sphere()
mvs.SetRepresentation('Surface')
mvs.SetCamera(viewType='isometric')

# Demo 6
import paraview.simple as pvs
import magnetovis as mvs
mvs.CreateViewAndLayout()
pvs.Sphere()
mvs.SetRepresentation('Surface With Edges')
mvs.SetCamera(viewType='isometric')

# Demo 7
import paraview.simple as pvs
import magnetovis as mvs
mvs.CreateViewAndLayout()
pvs.Sphere()
mvs.SetRepresentation('Wireframe')
mvs.SetCamera(viewType='isometric')
