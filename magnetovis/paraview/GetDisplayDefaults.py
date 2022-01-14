def GetDisplayDefaults(mvsName, all=False):

    import importlib
    object = importlib.import_module('magnetovis.Sources.' + mvsName)
    
    defaults = object.GetDisplayDefaults()

    if all == False:
        return 
