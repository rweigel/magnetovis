def UniqueName(name=None, proxyType="source", default=None):

    import paraview.simple as pvs

    if proxyType == "source":
        usedNamesAndIds = list(pvs.GetSources().keys())

    if proxyType == "layout":
        usedNamesAndIds = list(pvs.GetLayouts().keys())
        # usedNamesAndIds has form of
        # [('Layout #1', '11632'), ('Layout #2', '40747')

    usedNames = []
    for usedNameAndId in usedNamesAndIds:
        usedNames.append(usedNameAndId[0])

    if name is None and default is not None:
        name = default
    if name is None:
        name = proxyType.capitalize()

    if name in usedNames:
        k = 2
        while name + " #" + str(k) in usedNames:
            k = k + 1
        name = name + " #" + str(k)

    return name
