def PrintDisplayDefaults(mvsName, all=False):

  import pprint

  defaults = GetDisplayDefaults(mvsName, all=all)
  pp = pprint.PrettyPrinter(indent=2, sort_dicts=False) 
  pp.pprint(defaults)


def GetDisplayDefaults(mvsName, all=False):

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

  object = importlib.import_module('magnetovis.Sources.' + mvsName)

  if 'GetDisplayDefaults' in object.__dict__:
    # If function GetDisplayDefaults() in
    # magnetovis/Sources/{mvsName}.py file
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
  proxy = getattr(mvs, mvsName)()
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
  import paraview.simple as pvs
  PrintDisplayDefaults("Axis", all=True)
  PrintDisplayDefaults("Curve", all=True)
