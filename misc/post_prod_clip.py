import paraview.simple as pvs

"""
This file will apply a clip filter to all objects in the pipeline browswer.
Only regions where y>-2 will be visible.

to use:
    1. have objects in the paraview pipeline browser
    2. open python shell in paraview and execute this script.
"""

renderView = pvs.GetActiveViewOrCreate('RenderView')

for name_id, pObject in pvs.GetSources().items():
    clip = pvs.Clip(Input=pObject)
    clip.ClipType= 'Plane'
    clip.Invert = 0
    # change the origin to [0,0,0] if you want to show y>0 regions
    clip.ClipType.Origin = [0,-2,0]
    clip.ClipType.Normal = [0,1,0]
    clipDisplay = pvs.Show(clip, renderView)
    
    pvs.Hide3DWidgets(proxy=clip.ClipType)
    pvs.Hide(pObject)
    
renderView.Update()


    

