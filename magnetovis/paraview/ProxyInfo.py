def GetInfo(proxy, origin='client'):
    """Get information stored by SetInfo

    If origin='client', information is retrieved from magnetovis.__proxy_info.

    If origin='server', information is retrieved from output of proxy.
    Obtaining the information in this way requires all of the data to be
    copied from the server to the client.
    """

    if origin == 'client':
        import magnetovis
        proxy_id = hex(id(proxy))
        if hasattr(magnetovis, '__proxy_info'):
            if proxy_id in magnetovis.__proxy_info:
                return magnetovis.__proxy_info[proxy_id]
    else:
        import paraview
        sourceData = paraview.servermanager.Fetch(proxy)
        from vtk.numpy_interface import dataset_adapter as dsa
        sourceData = dsa.WrapDataObject(sourceData)
        keys = sourceData.GetFieldData().keys()
        values = sourceData.GetFieldData().values()
        info = {}
        import json
        for key_number in range(len(keys)):
            array = sourceData.GetFieldData()[key_number]
            if array.__vtkname__  == 'vtkStringArray':
                n = array.GetNumberOfValues()
                if n == 1:
                    try:
                        value = json.loads(array.GetValue(0))
                    except:
                        value = array.GetValue(0)
                else:
                    value = [array.GetValue(idx) for idx in range(array.GetNumberOfValues())]
            if array.__vtkname__  in ['vtkFloatArray', 'vtkIntArray']:
                n = array.GetNumberOfValues()
                if n == 1:
                    value = array.GetValue(0)
                else:
                    value = [array.GetValue(idx) for idx in range(array.GetNumberOfValues())]

            info[keys[key_number]] = value
        return info

    return None


def SetInfo(output, local_vars, include=None):
    """Store keyword arguments used for proxy.

    Information is stored in magnetivis.__proxy_info[id], where id
    is hex(id(proxy)) and proxy is the function returned by
    paraview.simple.GetActiveSource().

    Information is also stored as field data in the proxy output.    
    """
    import magnetovis as mvs

    import paraview.simple as pvs
    import magnetovis

    proxy = pvs.GetActiveSource()

    source_name = proxy.GetProperty('__magnetovis_name__')

    if source_name is None:
        return

    import importlib
    Script = importlib.import_module('magnetovis.Sources.' + source_name).Script

    # Get default keyword arguments
    ScriptKwargs = magnetovis.extract.extract_kwargs(Script)
    for key, val in local_vars.items():
        if key in ScriptKwargs:
            # Replace default with value used in script.
            if type(ScriptKwargs[key]) != type(val):
                mvs.logger.info("Type of {} in script differs from default. Using default value.".format(key))
            else:
                if ScriptKwargs[key] != val:
                    mvs.logger.info("Value of {} in script differs from default. Using value in script.".format(key))
                    ScriptKwargs[key] = val
        if include is not None and key in include:
            ScriptKwargs[key] = val

        if hasattr(val, '__vtkname__'):
            # Store keywords that start with the name of a vtk method and
            # end with "Settings" as a dict.
            vtkname = val.__vtkname__ + "Settings"
            if vtkname in ScriptKwargs:
                ScriptKwargs[vtkname] = magnetovis.vtk.get_settings(val, form='dict')

    registrationName = list(pvs.GetSources().keys())[list(pvs.GetSources().values()).index(pvs.GetActiveSource())][0]
    ScriptKwargs['registrationName'] = registrationName

    # Set field data
    magnetovis.vtk.set_arrays(output, field_data=ScriptKwargs)

    if not hasattr(magnetovis, '__proxy_info'):
        magnetovis.__proxy_info = {}

    # Delete ids that no longer exist in pipeline.
    # TODO?: Instead of 1000, use sys.getsizeof(magnetovis.__proxy_info)
    #        Probably not needed. Each source takes up far more memory
    #        than the metadata stored here.
    if len(magnetovis.__proxy_info) > 1000:
        active_proxys = list(pvs.GetSources().values())
        active_proxy_ids = []
        for active_proxy in active_proxys:
            active_proxy_ids.append(hex(id(active_proxy)))

        for stored_proxy_id in magnetovis.__proxy_info.copy():
            if stored_proxy_id not in active_proxy_ids:
                del magnetovis.__proxy_info[stored_proxy_id]

    proxy_id = hex(id(proxy))
    magnetovis.__proxy_info[proxy_id] = ScriptKwargs
