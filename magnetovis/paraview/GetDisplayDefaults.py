def PrintDisplayDefaults(sourceName, all=False):

  import pprint
  import json
  defaults = GetDisplayDefaults(sourceName, all=all)
  pp = pprint.PrettyPrinter(indent=2, sort_dicts=False, width=200) 
  pp.pprint(defaults)
  #print(defaults)
  #print(json.dumps(defaults, indent=1))

def GetDisplayDefaults(sourceName, all=False):

  """
  Gets defaults for a magnetovis object by creating it.
  Object is deleted after creation. To avoid creation

  1. Could cache output. But Paraview defaults may change.
  2. If possible, use functions in
     https://github.com/Kitware/ParaView/blob/master/Wrapping/Python/paraview/servermanager.py
     to get defaults.
  """

  import paraview.simple as pvs
  import magnetovis as mvs

  mvs.logger.info("Called.")

  def convert_val(val):
    if hasattr(val,'GetData'):
      val = val.GetData()
    return val

  def keep_kv(key, val):
    keep = key != 'Input' and key.startswith('_') == False
    keep = keep and key.startswith('Get') == False
    keep = keep and not hasattr(val,'ListProperties')
    if False and keep:
      print(key)
      print(val)
      print(type(val))
      print(dir(val))
    return keep    

  is_magnetovis = False

  import types

  if isinstance(sourceName, types.FunctionType):
    # To support dynamically created sources not part of magnetovis.
    # See MySource.py.
    is_magnetovis = True
    object = sourceName
    proxy = sourceName()
  else:
    try:
      import importlib
      object = importlib.import_module('magnetovis.Sources.' + sourceName)
      is_magnetovis = True
      proxy = getattr(mvs, sourceName)()
    except:
      if hasattr(pvs, sourceName) == False:
        raise ValueError(sourceName + " is not a magnetovis or ParaView source.")

  if is_magnetovis == False:

    try:
      proxy = getattr(pvs, sourceName)()
    except:
      raise ValueError(sourceName + " is not a ParaView source (it may be a filter).")


    defaults = {'source': {}, 'display': {}}

    # TODO: Repeated code below
    lastView = pvs.GetActiveView()
    pvs.SetActiveView(None)
    view = pvs.CreateView('RenderView')
    s = pvs.Show(proxy=proxy, view=view)
    props = proxy.ListProperties()
    for prop in props:
      defaults['source'][prop] = proxy.GetPropertyValue(prop)

    for key in dir(s):
      val = s.GetPropertyValue(key)
      if keep_kv(key, val) and not key in defaults[name]['display']:
        defaults['display'][key] = convert_val(val)

    pvs.Delete(proxy)
    del proxy
    pvs.Delete(view)
    del view
    pvs.SetActiveView(lastView)

    return defaults


  if is_magnetovis and 'GetDisplayDefaults' in object.__dict__:
    # If function GetDisplayDefaults() in
    # magnetovis/Sources/{sourceName}.py file
    defaults = object.GetDisplayDefaults()
  else:
    defaults = {}

  if all == False:
    return defaults
    
  # Display
  if not 'display' in defaults:
    defaults['display'] = {}

  lastView = pvs.GetActiveView()
  pvs.SetActiveView(None)
  view = pvs.CreateView('RenderView')

  # Create proxy
  s = pvs.Show(proxy=proxy, view=view)
  for key in dir(s):
    val = s.GetPropertyValue(key)
    if keep_kv(key, val) and not key in defaults['display']:
      defaults['display'][key] = convert_val(val)

  children = proxy.GetProperty('__magnetovis_children__')
  if children is not None:
    for child in children:

      name = list(child.keys())[0]
      mvs.logger.info("Getting properties for {}".format(name))
      cproxy = child[name]
      props = proxy.ListProperties()
      mvs.logger.info("Properties = {}".format(props))

      if not name in defaults:
        defaults[name] = {}

      if not 'source' in defaults[name]:
        defaults[name]['source'] = {}

      if not 'display' in defaults[name]:
        defaults[name]['display'] = {}

      for key in props:
        val = cproxy.GetPropertyValue(key)
        if keep_kv(key, val):
          defaults[name]['source'][key] = convert_val(val)
          if all and key.startswith('vtk'):
            defaults[name]['source'][key] = mvs.vtk.get_settings(key)

      s = pvs.Show(proxy=cproxy, view=view)

      for key in dir(s):
        val = s.GetPropertyValue(key)
        if keep_kv(key, val) and not key in defaults[name]['display']:
          defaults[name]['display'][key] = convert_val(val)

      pvs.Delete(cproxy)
      del cproxy

  pvs.Delete(proxy)
  del proxy
  pvs.Delete(view)
  del view

  pvs.SetActiveView(lastView)

  return defaults

if __name__ == "__main__":
  #PrintDisplayDefaults("Text")
  #GetDisplayDefaults("Axis", all=True)
  #print(GetDisplayDefaults("Axis", all=True))
  PrintDisplayDefaults("Axis", all=True)
  #PrintDisplayDefaults("Curve", all=True)
