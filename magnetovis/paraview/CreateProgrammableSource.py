def CreateProgrammableSource(sourceFile, ptype, **kwargs):

    import importlib
    import paraview.simple as pvs

    import magnetovis as mvs
    from magnetovis import extract

    mvs.logger.info("Called.")

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

    if ptype == "source":
        setDisplayProperties = True
        if 'setDisplayProperties' in kwargs:
            setDisplayProperties = kwargs['setDisplayProperties']
        pSource = pvs.ProgrammableSource()
    else:
        pSource = pvs.ProgrammableFilter()

    if False:
        def AnySourceEvent(a,b):
            mvs.logger.info("Event " + b + " on source.")
            pSource.SMProxy.RemoveObserver(cb_id_ase)
        cb_id_ase = pSource.SMProxy.AddObserver('AnyEvent', AnySourceEvent)

    if ptype == "source" and hasattr(module, 'GetSourceDefaults'):
        kwargs = module.GetSourceDefaults(extract.extract_kwargs(module.Script), kwargs)
    if ptype == "filter" and hasattr(module, 'GetFilterDefaults'):
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
            if hasattr(pSource, '__magnetovis_children__'):
                return pSource.__magnetovis_children__
            else:
                return None
        if property == "__magnetovis_module__":
            return module
        if property in kwargs:
            return kwargs[property]
        else:
            return GetPropertyOriginal(property)

    pSource.ListProperties = ListProperties
    pSource.GetProperty = GetProperty

    defaultRegistrationName = None
    if hasattr(module, 'DefaultRegistrationName'):
        defaultRegistrationName = module.DefaultRegistrationName(**kwargs)

    registrationName = mvs.UniqueName(name=registrationName, proxyType="source", default=defaultRegistrationName)
    pvs.RenameSource(registrationName, pSource)
    
    if ptype == "source":
        if setDisplayProperties == True:
            mvs.SetDisplayProperties(source=pSource)
        else:
            view = pvs.GetActiveViewOrCreate('RenderView')
            def AnyEvent(a,b):
                view.SMProxy.RemoveObserver(cb_id_ae)
                mvs.logger.info("Event " + b + " on view for " + registrationName)
                mvs.SetDisplayProperties(source=pSource)
            cb_id_ae = view.SMProxy.AddObserver('ModifiedEvent', AnyEvent)

    mvs.logger.info("Finished.\n")

    return pSource
