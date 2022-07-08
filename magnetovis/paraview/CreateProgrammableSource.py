def CreateProgrammableSource(sourceName, **kwargs):

    import importlib
    import paraview.simple as pvs
    from magnetovis import extract

    import magnetovis as mvs
    mvs.logger.info("Called. sourceName = " + sourceName)

    object = importlib.import_module('magnetovis.Sources.' + sourceName)

    pSource = pvs.ProgrammableSource()

    mvs.logger.info("Extracting script and kwarg defaults; replacing defaults with passed kwargs.")
    pSource.Script, kwargs = extract.extract_script(object.Script, kwargs)

    if hasattr(object, 'OutputDataSetType'):
        mvs.logger.info("Getting OutputDataSetType default.")
        default = object.OutputDataSetType()
        mvs.logger.info("Setting OutputDataSetType to " + default)
        pSource.OutputDataSetType = default
    else:
        if 'OutputDataSetType' in kwargs:
            mvs.logger.info("Setting OutputDataSetType passed as kwarg.")
            pSource.OutputDataSetType = kwargs['OutputDataSetType']

    if hasattr(object, 'ScriptRequestInformation'):
        mvs.logger.info("Extracting ScriptRequestInformation script.")
        pSource.ScriptRequestInformation, _ = extract.extract_script(object.ScriptRequestInformation, kwargs)

    registrationName = None
    if 'registrationName' in kwargs:
        registrationName = kwargs['registrationName']

    # Add kwargs as properties to make pSource have options
    # that can be obtained with GetProperty() in the same way that a
    # plugin's menu options can be obtained with GetProperty().
    Properties = pSource.ListProperties()
    def ListProperties():
        for key in dict(kwargs):
            Properties.append(key)
        Properties.append("__magnetovis_name__")
        Properties.append("__magnetovis_children__")
        return Properties

    children = None
    GetPropertyOriginal = pSource.GetProperty
    def GetProperty(property):
        if property == "__magnetovis_name__":
            return sourceName
        if property == "__magnetovis_children__":
            return children
        if property in kwargs:
            return kwargs[property]
        else:
            return GetPropertyOriginal(property)

    pSource.ListProperties = ListProperties
    pSource.GetProperty = GetProperty

    # TODO: Similar code exists in CreateViewAndLayout(). Combine.
    # Set a registration name using the following logic.
    # If registrationName
    #      Use it. If used, ValueError.
    #    else
    #      if object.DefaultRegistrationName() found
    #         Use that name + " #1"
    #      else
    #         Use object name + " #1"
    #      
    #      If name + " #1" already used, increment number until
    #      name + " #n" is unique.
    sources = list(pvs.GetSources().keys())
    registrationNames = []
    for source in sources:
        registrationNames.append(source[0])

    if registrationName is not None:
        # Requested registrationName
        if registrationName in registrationNames:
            raise ValueError("registration name '" + registrationName + "' is used.")
    else:
        registrationName = sourceName
        if hasattr(object, 'DefaultRegistrationName'):
            registrationName = object.DefaultRegistrationName(**kwargs)

        if registrationName + " #1" not in registrationNames:
            registrationName = registrationName + " #1"
        else:
            k = 2
            while registrationName + " #" + str(k) in registrationNames:
                k = k + 1
            registrationName = registrationName + " #" + str(k)

    pvs.RenameSource(registrationName, pSource)
    
    import magnetovis as mvs
    children = mvs.SetDisplayProperties(pSource)

    mvs.logger.info("Finished.\n")

    return pSource
