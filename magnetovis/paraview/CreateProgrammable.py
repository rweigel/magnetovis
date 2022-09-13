def CreateProgrammable(scriptFile, ptype, **kwargs):

    import os
    import importlib
    import paraview.simple as pvs

    import magnetovis as mvs
    from magnetovis import extract

    mvs.logger.info("Called.")

    file_name = os.path.basename(os.path.splitext(scriptFile)[0])

    def create_module(file_path):
        import types
        import importlib.machinery
        loader = importlib.machinery.SourceFileLoader(file_name, file_path)
        module = types.ModuleType(loader.name)
        loader.exec_module(module)
        return module

    module = create_module(scriptFile)
    sourceName = module.__name__

    defaultRegistrationName = file_name
    registrationName = None
    if 'registrationName' in kwargs:
        registrationName = kwargs['registrationName']

    if ptype == "source":
        setPresentationProperties = True
        if 'setPresentationProperties' in kwargs:
            setPresentationProperties = kwargs['setPresentationProperties']
        setPresentationPropertiesOnShow = True
        if 'setPresentationPropertiesOnShow' in kwargs:
            setPresentationPropertiesOnShow = kwargs['setPresentationPropertiesOnShow']
        programmable = pvs.ProgrammableSource()
    else:
        programmable = pvs.ProgrammableFilter(Input=kwargs['Input'])

    mvs.logger.info("scriptFile = " + scriptFile)
    mvs.logger.info("ptype = " + ptype)

    mvs.logger.info("Adding observer for AnyEvent.")
    def AnySourceEvent(a, event):
        mvs.logger.info(f"Event {event} on {registrationName}.")
        programmable.SMProxy.RemoveObserver(cb_id_ase)
    cb_id_ase = programmable.SMProxy.AddObserver('AnyEvent', AnySourceEvent)

    if ptype == "source" and hasattr(module, 'GetSourceDefaults'):
        kwargs = module.GetSourceDefaults(extract.extract_kwargs(module.Script), kwargs)
    if ptype == "filter" and hasattr(module, 'GetFilterDefaults'):
        kwargs = module.GetSourceDefaults(extract.extract_kwargs(module.Script), kwargs)

    if registrationName is None and hasattr(module, 'DefaultRegistrationName'):
        _kwargs = extract.extract_kwargs(module.Script, default_kwargs=kwargs)
        registrationName = module.DefaultRegistrationName(**_kwargs)

    registrationName = mvs.UniqueName(name=registrationName, proxyType="source", default=defaultRegistrationName)
    pvs.RenameSource(registrationName, programmable)

    mvs.logger.info("Extracting script and kwarg defaults after replacing defaults with passed kwargs.")
    programmable.Script, kwargs = extract.extract_script(module.Script, kwargs)

    if 'output' in kwargs and kwargs['output'] is None or 'output' not in kwargs:
        programmable.Script += f"\nregistrationName='{registrationName}'\nimport magnetovis as mvs;mvs.ProxyInfo.SetInfo(output, locals())"

    if hasattr(module, 'OutputDataSetType'):
      mvs.logger.info("Getting OutputDataSetType default.")
      default = module.OutputDataSetType()
      mvs.logger.info("Setting OutputDataSetType to " + default)
      programmable.OutputDataSetType = default
    else:
      if 'OutputDataSetType' in kwargs:
        mvs.logger.info("Setting OutputDataSetType passed as kwarg.")
        programmable.OutputDataSetType = kwargs['OutputDataSetType']

    if ptype == "source" and hasattr(module, 'ScriptRequestInformation'):
      mvs.logger.info("Extracting ScriptRequestInformation script.")
      programmable.ScriptRequestInformation, _ = extract.extract_script(module.ScriptRequestInformation, kwargs)

    if ptype == "filter" and hasattr(module, 'RequestInformationScript'):
      # Note the difference in names (ScriptRequestInformation for source
      # and RequestInformationScript for filter)
      mvs.logger.info("Extracting RequestInformationScript script.")
      programmable.RequestInformationScript, _ = extract.extract_script(module.RequestInformationScript, kwargs)

    # Add kwargs as properties to make programmable have options
    # that can be obtained with GetProperty() in the same way that a
    # plugin's menu options can be obtained with GetProperty().
    #Properties = programmable.ListProperties()
    Properties = []
    def ListProperties():
      for key in dict(kwargs):
        Properties.append(key)
      Properties.append("__magnetovis_name__")
      Properties.append("__magnetovis_children__")
      Properties.append("__magnetovis_module__")
      return Properties

    children = None
    GetPropertyOriginal = programmable.GetProperty
    def GetProperty(property):
        if property == "__magnetovis_name__":
            return sourceName
        if property == "__magnetovis_children__":
            if hasattr(programmable, '__magnetovis_children__'):
                return programmable.__magnetovis_children__
            else:
                return None
        if property == "__magnetovis_module__":
            return module
        if property in kwargs:
            return kwargs[property]
        else:
            return GetPropertyOriginal(property)

    programmable.ListProperties = ListProperties
    programmable.GetProperty = GetProperty
    programmable.GetPropertyValue = GetProperty 
    # GetProperty and GetPropertyValue seem to be the same in ParaView sources,
    # so we set programmable.GetPropertyValue = GetProperty.
    # s = Sphere()
    # s.GetPropertyValue
    # <bound method Proxy.GetPropertyValue of <paraview.servermanager.Sphere object at 0x2abf04640>>
    # s.GetProperty
    # <bound method Proxy.GetProperty of <paraview.servermanager.Sphere object at 0x2abf04640>>

    if ptype == "source":
        if setPresentationProperties == True:
            mvs.SetPresentationProperties(source=programmable)
        else:
            # The following causes the display properties to be
            # set when the user clicks to show the source in the
            # pipeline or executes Show(). When a source is shown,
            # ParaView creates a representation for it (you will see
            # a change in the Display area of the Properties window)
            # and a StartEvent is then triggered on the view. In the
            # callback AnyViewEvent, a check is made to determine if
            # the source has a representation. If it does not have a
            # representation, then a request to Show the source has
            # not yet been made and so no action is taken.
            #
            # Note that this does not address the case where a source
            # is shown in multiple views. The magnetovis display
            # properties are only set on the view that was active
            # when the source was created.

            # TODO: Catch Hide() event. If associated source is a 
            # magnetovis source, hide its children.
            if setPresentationPropertiesOnShow == True:
              view = pvs.GetActiveViewOrCreate('RenderView')
              def ViewStartEvent(a,b):
                  from paraview import servermanager
                  rep = servermanager.GetRepresentation(programmable, view)
                  #mvs.logger.info("Event " + b + " on view for " + registrationName)
                  if rep is None:
                      #mvs.logger.info("No representation for " + registrationName)
                      return
                  mvs.logger.info(f"Call to SetPresentationProperties() triggered for {registrationName}")
                  view.SMProxy.RemoveObserver(cb_id_ae)
                  mvs.SetPresentationProperties(source=programmable)
              cb_id_ae = view.SMProxy.AddObserver('StartEvent', ViewStartEvent)

    mvs.logger.info("Finished.\n")

    return programmable
