def PrintDisplayDefaults(mvsName, all=False):
    import pprint

    defaults = GetDisplayDefaults(mvsName, all=all)
    pp = pprint.PrettyPrinter(indent=2, sort_dicts=False) 
    pp.pprint(defaults)


def GetDisplayDefaults(mvsName, all=False):

    import importlib
    object = importlib.import_module('magnetovis.Sources.' + mvsName)

    if not 'GetDisplayDefaults' in object.__dict__:
        return None

    defaults = object.GetDisplayDefaults()
    if all == False:
        return defaults
    
    import paraview.simple as pvs
    import magnetovis as mvs

    # Display
    # See GetProperties() for a discussion on doing this
    # without putting an object in the pipeline.
    if not 'display' in defaults:
        defaults['display'] = {}

    object = getattr(mvs, 'Axis')()
    s = pvs.Show(proxy=object)
    for key in dir(s):
        if key.startswith('_') == False and not key in defaults['display']:
            defaults['display'][key] = s.GetPropertyValue(key)

    c = object.GetProperty('__magnetovis_children__')
    pvs.Delete(object)
    del object
    pvs.Delete(c[0])
    del c

    # View
    if not 'view' in defaults:
        defaults['view'] = {}

    v = pvs.GetActiveView()
    for key in dir(v):
        if key.startswith('_') == False and not key in defaults['view']:
            defaults['view'][key] = v.GetPropertyValue(key)

    # Could get from object.ListProperties()['__magnetovis_children__']
    for key in defaults:
        if 'sourceType' in defaults[key]:
            defaults[key] = mvs.GetProperties(defaults[key]['sourceType'])

    return defaults
