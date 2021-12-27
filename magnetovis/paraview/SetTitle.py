def SetTitle(*arg, source=None, view=None, registrationName=None, **kwargs):

    import paraview.simple as pvs
    import magnetovis as mvs

    mvs.logger.info("Called.")

    if len(arg) == 0:
        titleText = None
    else:
        titleText = arg[0]

    if source is None:
        source = pvs.GetActiveSource()

    sourceName = mvs.GetRegistrationName(source)
    if registrationName is None or registrationName == "":
        registrationName = "  Title for " + sourceName

    if titleText is None:
        titleText = sourceName

    textSource = pvs.Text(registrationName=registrationName, Text=titleText)
    
    if view is None:
        view = pvs.GetActiveViewOrCreate('RenderView')

    if 'display' in kwargs:
        pvs.Show(proxy=textSource, view=view, **kwargs['display'])
    else:
        pvs.Show(proxy=textSource, view=view)

    pvs.SetActiveSource(source)

    return textSource
