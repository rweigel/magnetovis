def GetDisplayDefaults(mvsName, all=False):

    import importlib
    object = importlib.import_module('magnetovis.Sources.' + mvsName)
    
    return object.GetDisplayDefaults(all=all)
