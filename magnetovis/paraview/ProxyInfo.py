def GetInfo(proxy, origin='client'):

    #"_magnetovis__name__"

    import importlib 
    import magnetovis

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


def SetInfo(function, local_vars):

    import magnetovis

    name = function.GetProperty('__magnetovis_name__')

    import importlib
    Script = importlib.import_module('magnetovis.Sources.' + name).Script
    ScriptKwargs = magnetovis.extract.extract_kwargs(Script)
    for key, val in local_vars.items():
        if hasattr(val, '__vtkname__'):
            name = val.__vtkname__ + "Settings"
            if name in ScriptKwargs:
                ScriptKwargs[name] = magnetovis.vtk.get_settings(val, form='dict')

    import paraview.simple as pvs
    registrationName = list(pvs.GetSources().keys())[list(pvs.GetSources().values()).index(pvs.GetActiveSource())][0]
    ScriptKwargs['registrationName'] = registrationName

    #print(ScriptKwargs)

    magnetovis.vtk.set_arrays(local_vars['output'], field_data=ScriptKwargs)


    if not hasattr(magnetovis, '__proxy_info'):
        magnetovis.__proxy_info = {}

    # Delete ids that no longer exist in pipeline.
    # TODO?: Instead of 1000, use sys.getsizeof(magnetovis.__proxy_info)
    #        Probably not needed. Each source takes up far more memory
    #        than the metadata stored here.
    if len(magnetovis.__proxy_info) > 1000:
        import paraview.simple as pvs

        active_functions = list(pvs.GetSources().values())
        active_function_ids = []
        for active_function in active_functions:
            active_function_ids.append(hex(id(active_function)))

        for stored_function_id in magnetovis.__proxy_info.copy():
            if stored_function_id not in active_function_ids:
                del magnetovis.__proxy_info[stored_function_id]

    function_id = hex(id(function))
    magnetovis.__proxy_info[function_id] = ScriptKwargs
