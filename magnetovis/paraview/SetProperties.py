def SetProperties(vtkObj, settings):

    import vtk
    import magnetovis as mvs

    if settings is None:
        return

    if isinstance(settings, str):
        settings = [settings]

    from magnetovis.vtk.get_settings import get_settings

    vtkName = vtkObj.__vtkname__
    defaults = get_settings(vtkName, form='dict')
    for setting in settings:

        key = setting.split(":")[0].strip()        
        val = setting.split(":")[1].lstrip().rstrip()

        assert key in defaults, key + " is not a valid setting of " + vtkName
        default = defaults[key]
        mvs.logger.info(vtkName + " default {} = {}".format(key, default))

        val_is_bool = False
        if val == 'True':
            val = True
            val_is_bool = True
        if val == 'False':
            val_is_bool = True
            val = False

        if isinstance(default, int) and val_is_bool == False:
            val = int(val)
        if isinstance(default, float):
            val = float(val)
        if isinstance(default, tuple):
            val = val[1:-1].split(",")
            if isinstance(default[0], float):
                val = tuple([float(v) for v in val])
            if isinstance(default[0], int):
                val = tuple([int(v) for v in val])

        mvs.logger.info(vtkName + " setting {} = {}".format(key, val))

        try:
            getattr(vtkObj, "Set" + key)() 
        except:
            try:
                getattr(vtkObj, "Set" + key)(val)
            except:
                mvs.logger.warning("Cannot evaluate vtk." + vtkName + "().Set" + key + "()")
                mvs.logger.warning("Cannot evaluate vtk." + vtkName + "().Set" + key + "(" + str(val) + ")")
                #logging.warning("Input is probably a vtk data type (e.g., vtkBitArray, vtkIdTypeArray, etc.)")

if False:
    import vtk
    from magnetovis.vtk.get_settings import get_settings

    vtkMethods = dir(vtk)
    vtkSources = []
    vtkFilters = []
    for vtkMethod in vtkMethods:
        if vtkMethod == "vtkSelectionSource":
            continue
        vtkObj = getattr(vtk, vtkMethod)
        if vtkMethod.endswith("Filter"):
            vtkFilters.append(vtkMethod)
        if vtkMethod.endswith("Source"):
            vtkSources.append(vtkMethod)

    #print(vtkFilters)
    #print(vtkSources)

    for vtkMethod in vtkFilters + vtkSources:
        print(80*"-")
        print(vtkMethod)
        print(80*"-")

        defaults_dict = get_settings(vtkMethod)
        defaults_list = []
        for key, val in defaults_dict.items():
            defaults_list.append(key + ": " + str(val))

        if len(defaults_list) > 0:
            vtkObj = getattr(vtk, vtkMethod)()
            set_settings(vtkObj, defaults_list)


    #import pprint
    #pp = pprint.PrettyPrinter(indent=2)
    #pp.pprint(dir(vtk.vtkSphereSource()))
    #print(vtk.vtkSphereSource())
    #pp.pprint(vtk.vtkSphereSource().IsA())
