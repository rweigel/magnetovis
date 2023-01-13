def GetRegistrationName(source=None):

    import paraview.simple as pvs

    if source is None:
        source = pvs.GetActiveSource()

    sources = pvs.GetSources()
    # https://public.kitware.com/pipermail/paraview/2017-January/038962.html
    return list(sources.keys())[list(sources.values()).index(source)][0]

