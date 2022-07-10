def PrintDisplayDefaults(sourceName, all=False):

  import pprint

  defaults = GetDisplayDefaults(sourceName, all=all)
  pp = pprint.PrettyPrinter(indent=2, sort_dicts=False) 
  pp.pprint(defaults)


def GetDisplayDefaults(sourceName, all=False):

  """
  Gets defaults for a magnetovis object by creating it.
  Object is deleted after creation. To avoid creation

  1. Could cache output. But Paraview defaults may change.
  2. If possible, use functions in
     https://github.com/Kitware/ParaView/blob/master/Wrapping/Python/paraview/servermanager.py
     to get defaults.
  """

  import importlib

  import paraview.simple as pvs
  import magnetovis as mvs

  mvs.logger.info("Called.")

  is_magnetovis = False
  try:
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
      if key.startswith('_') == False and key != 'Input':
        defaults['display'][key] = s.GetPropertyValue(key)

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
    if key.startswith('_') == False and not key in defaults['display']:
      defaults['display'][key] = s.GetPropertyValue(key)

  children = proxy.GetProperty('__magnetovis_children__')
  if children is not None:
    for child in children:
      name = list(child.keys())[0]
      cproxy = child[name]
      props = proxy.ListProperties()
      if not 'source' in defaults[name]:
        defaults[name]['source'] = {}
      for prop in props:
        if prop != 'Input':
          defaults[name]['source'][prop] = cproxy.GetPropertyValue(prop)

      s = pvs.Show(proxy=cproxy, view=view)
      for key in dir(s):
        if key.startswith('_') == False and not key in defaults[name]['display']:
          defaults[name]['display'][key] = s.GetPropertyValue(key)

      pvs.Delete(cproxy)
      del cproxy

  pvs.Delete(proxy)
  del proxy
  pvs.Delete(view)
  del view

  pvs.SetActiveView(lastView)

  return defaults


if __name__ == "__main__":
  PrintDisplayDefaults("Text")
  PrintDisplayDefaults("Axis", all=True)
  #PrintDisplayDefaults("Curve", all=True)
