def CreateProgrammableSource(sourceName, **kwargs):

    import importlib
    import paraview.simple as pvs
    from magnetovis import extract

    import magnetovis as mvs
    mvs.logger.info("Called. sourceName = " + sourceName)

    object = importlib.import_module('magnetovis.Sources.' + sourceName)

    pSource = pvs.ProgrammableSource()

    pSource.Script, kwargs = extract.extract_script(object.Script, kwargs)
    #kwargs = extract.extract_kwargs(object.Script, default_kwargs=kwargs)

    if hasattr(object, 'OutputDataSetType'):
        pSource.OutputDataSetType = object.OutputDataSetType()

    if 'OutputDataSetType' in kwargs:
        pSource.OutputDataSetType = kwargs['OutputDataSetType']

    if hasattr(object, 'ScriptRequestInformation'):
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
        return Properties

    GetPropertyOriginal = pSource.GetProperty
    def GetProperty(property):
        if property == "__magnetovis_name__":
            return sourceName
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
    mvs.SetDisplayProperties(pSource)

    mvs.logger.info("Finished.\n")

    return pSource
