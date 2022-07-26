def CreateProgrammableSource(sourceFile, **kwargs):

    import importlib
    import paraview.simple as pvs

    import magnetovis as mvs
    from magnetovis import extract

    def create_module(file_path):
        import os
        import types
        import importlib.machinery

        file_name = os.path.basename(os.path.splitext(file_path)[0])

        loader = importlib.machinery.SourceFileLoader(file_name, file_path)
        module = types.ModuleType(loader.name)
        loader.exec_module(module)
        return module

    module = create_module(sourceFile)
    sourceName = module.__name__


    # If registrationName is not a keyword for source, it will be removed
    # by the call to extract_script. So we need to get it here. Same for
    # setDisplayProperties.
    registrationName = None
    if 'registrationName' in kwargs:
        registrationName = kwargs['registrationName']
    setDisplayProperties = True
    if 'setDisplayProperties' in kwargs:
        setDisplayProperties = kwargs['setDisplayProperties']

    pSource = pvs.ProgrammableSource()

    if hasattr(module, 'GetSourceDefaults'):
        kwargs = module.GetSourceDefaults(extract.extract_kwargs(module.Script), kwargs)

    mvs.logger.info("Extracting script and kwarg defaults after replacing defaults with passed kwargs.")
    pSource.Script, kwargs = extract.extract_script(module.Script, kwargs)

    if hasattr(module, 'OutputDataSetType'):
        mvs.logger.info("Getting OutputDataSetType default.")
        default = module.OutputDataSetType()
        mvs.logger.info("Setting OutputDataSetType to " + default)
        pSource.OutputDataSetType = default
    else:
        if 'OutputDataSetType' in kwargs:
            mvs.logger.info("Setting OutputDataSetType passed as kwarg.")
            pSource.OutputDataSetType = kwargs['OutputDataSetType']

    if hasattr(module, 'ScriptRequestInformation'):
        mvs.logger.info("Extracting ScriptRequestInformation script.")
        pSource.ScriptRequestInformation, _ = extract.extract_script(module.ScriptRequestInformation, kwargs)

    # Add kwargs as properties to make pSource have options
    # that can be obtained with GetProperty() in the same way that a
    # plugin's menu options can be obtained with GetProperty().
    #Properties = pSource.ListProperties()
    Properties = []
    def ListProperties():
        for key in dict(kwargs):
            Properties.append(key)
        Properties.append("__magnetovis_name__")
        Properties.append("__magnetovis_children__")
        Properties.append("__magnetovis_module__")
        return Properties

    children = None
    GetPropertyOriginal = pSource.GetProperty
    def GetProperty(property):
        if property == "__magnetovis_name__":
            return sourceName
        if property == "__magnetovis_children__":
            return children
        if property == "__magnetovis_module__":
            return module
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
    #      if module.DefaultRegistrationName() found
    #         Use that name + " #1"
    #      else
    #         Use module name + " #1"
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
        if hasattr(module, 'DefaultRegistrationName'):
            registrationName = module.DefaultRegistrationName(**kwargs)

        #if registrationName + " #1" not in registrationNames:
        #    registrationName = registrationName + " #1"
        if registrationName in registrationNames:
            k = 2
            while registrationName + " #" + str(k) in registrationNames:
                k = k + 1
            registrationName = registrationName + " #" + str(k)

    pvs.RenameSource(registrationName, pSource)
    
    if setDisplayProperties == True:
        children = mvs.SetDisplayProperties(pSource)

    mvs.logger.info("Finished.\n")

    return pSource
