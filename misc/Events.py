import paraview.simple as pvs

def UpdateDisplayOptions(caller, event):
    import paraview.simple as pvs

    print("Caller: ")
    print(caller)
    print("Event: ")
    print(event)
    # TODO: Figure out how to get source out of caller object (which is a SMSourceProxy).
    if True:
        source = pvs.GetActiveSource()
        renderView1 = pvs.GetActiveViewOrCreate('RenderView')
        sphere1Display = pvs.GetDisplayProperties(source, view=renderView1)
        sphere1Display.SetRepresentationType('Surface')
    #print(source)
    #source.RemoveObserver('UpdateInformationEvent')
    #mvs.SetDefaultDisplayProperties(pvs.GetActiveSource())


if False:
    from paraview import servermanager
    pxm = servermanager.ProxyManager()
    pxm.GetSelectionModel('ActiveSources').AddObserver("CurrentChangedEvent", UpdateDisplayOptions)
    #pxm.GetSelectionModel('ActiveSources').AddObserver("EndEvent", UpdateDisplayOptions)

if False:
	pxm = servermanager.vtkSMProxyManager.GetProxyManager()
	#https://github.com/Kitware/ParaView/blob/43519a5124f4b75670e4a1eed7d14c440f11ad4b/Wrapping/Python/paraview/simple.py#L2819
	pxm.AddObserver(pxm.ActiveSessionChanged, UpdateDisplayOptions)

sphere = pvs.Sphere()
sphere.AddObserver('UpdateInformationEvent', UpdateDisplayOptions)
pvs.Show(sphere)
