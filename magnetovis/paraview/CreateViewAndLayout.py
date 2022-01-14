def CreateViewAndLayout(name=None):

    import paraview.simple as pvs

    name = __GetUniqueLayoutName(name)
    pvs.SetActiveView(None)
    view = pvs.CreateView('RenderView')
    layout = pvs.CreateLayout(name=name)
    pvs.AssignViewToLayout(view=view, layout=layout)

    return view, layout

def __GetUniqueLayoutName(name):

    import paraview.simple as pvs

    layouts = list(pvs.GetLayouts().keys())
    usedNames = []
    for layout in layouts:
        usedNames.append(layout[0])

    if name is not None:
        if name in usedNames:
            raise ValueError("layout name '" + name + "' is used.")
        else:
            return name

    name = "Layout"
    if name + " #1" not in usedNames:
        name = name + " #1"
    else:
        k = 2
        while name + " #" + str(k) in usedNames:
            k = k + 1
        name = name + " #" + str(k)

    return name