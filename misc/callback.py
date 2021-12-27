import paaraview.simple as pvs
sphere = pvs.Sphere()

def UpdateDisplayOptions(caller, event):
    import paraview.simple as pvs
    print("Event: " + event)
    print("Caller: " + caller)
    # TODO: Figure out how to get source out of caller object (which is a SMSourceProxy).
    source = pvs.GetActiveSource()
    print(source)
    #source.RemoveObserver('UpdateInformationEvent')
    #mvs.SetDefaultDisplayProperties(pvs.GetActiveSource())

sphere.AddObserver('UpdateInformationEvent', UpdateDisplayOptions)
