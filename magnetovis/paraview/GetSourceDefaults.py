def PrintSourceDefaults(sourceName, all=False):

  import pprint

  defaults = GetSourceDefaults(sourceName, all=all)
  pp = pprint.PrettyPrinter(indent=2, sort_dicts=False) 
  pp.pprint(defaults)


def GetSourceDefaults(proxy, all=False):

  """
  Gets defaults for a Paraview or magnetovis source.
  """

  import magnetovis as mvs
  mvs.logger.info("Called.")

  is_magnetovis = False
  try:
    proxy = proxy(setPresentationProperties=False)
    is_magnetovis = True
  except:
    proxy = proxy()

  defaults = {}
  props = proxy.ListProperties()
  for prop in props:
    if not prop.startswith("__magnetovis"):
      defaults[prop] = proxy.GetPropertyValue(prop)

  if is_magnetovis == True and all == True:
    for default in defaults.keys():

      if not default.startswith('vtk'):
        continue

      defaults_vtk = mvs.vtk.get_settings(default)
      if defaults[default] is None:
        defaults[default] = defaults_vtk
      else:
        defaults[default] = mvs.vtk.update_defaults(defaults_vtk, defaults[default])

  import paraview.simple as pvs
  pvs.Delete(proxy)
  del proxy

  return defaults


if __name__ == "__main__":
  #PrintSourceDefaults("Sphere")
  #PrintSourceDefaults("Axis", all=False)
  import magnetovis as mvs
  PrintSourceDefaults(mvs.Axis)
  PrintSourceDefaults(mvs.Axis, all=True)
  #import paraview.simple as pvs
  #PrintSourceDefaults(pvs.Sphere, all=True)

if False:
  import pytest
  with pytest.raises(ValueError):
    PrintSourceDefaults("ShouldRaiseError")

if False:
  if 'Script' in source.__dict__:
    # If function Script() in
    # magnetovis/Sources/{mvsName}.py file
    defaults = extract.extract_kwargs(source.Script)

