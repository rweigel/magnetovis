import paraview.simple as pvs
import magnetovis as mvs
s = pvs.Sphere()
mvs.SetColor(Color=[0, 0, 1]) # Colors active proxy in active view and shows.

import paraview.simple as pvs
s = pvs.Sphere()
pvs.Show()
view = pvs.GetActiveViewOrCreate('RenderView')
rep = pvs.GetPresentationProperties(proxy=s, view=view)
kwargs = {'DiffuseColor': [0, 0, 1], 'AmbientColor': [0, 0, 1]}
pvs.SetProperties(ColorArrayName=[None, ''], **kwargs)
