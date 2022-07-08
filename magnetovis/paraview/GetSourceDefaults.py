def PrintSourceDefaults(mvsName, all=False):

  import pprint

  defaults = GetSourceDefaults(mvsName, all=all)
  pp = pprint.PrettyPrinter(indent=2, sort_dicts=False) 
  #pp.pprint(defaults)


def GetSourceDefaults(sourceName, all=False):

  """
  Gets defaults for a Paraview or magnetovis source.
  """

  import importlib

  import magnetovis as mvs
  from magnetovis import extract

  mvs.logger.info("Called.")

  is_magnetovis = False
  is_paraview = False
  try:
    source = importlib.import_module('magnetovis.Sources.' + sourceName)
    is_magnetovis = True
  except:
    pass

  try:
    import paraview.simple as pvs
    source = getattr(pvs, sourceName)()
    is_paraview = True
  except:
    pass

  if is_magnetovis == False and is_paraview == False:
    raise ValueError(f'{sourceName} is not a magentovis or Paraview source.')

  defaults = {}
  if is_paraview:
    props = source.ListProperties()
    for prop in props:
      defaults[prop] = source.GetPropertyValue(prop)
    del source
  else:
    if 'Script' in source.__dict__:
      # If function Script() in
      # magnetovis/Sources/{mvsName}.py file
      defaults = extract.extract_kwargs(source.Script)
    else:
      return {}

    for default in defaults.keys():
      vtkName = ""
      if default.endswith('SourceSettings') or default.endswith('FilterSettings'):
        vtkName = default.replace('Settings','')

      if vtkName != "":
        from magnetovis.vtk import get_settings
        if defaults[default] is None:
          defaults[default] = get_settings(vtkName)
        else:
          if all == True:
            defaults_vtk = get_settings(vtkName, form='dict')
            from magnetovis.vtk.set_settings import update_defaults
            print(defaults[default])
            defaults[default] = update_defaults(defaults_vtk, defaults[default], form='list')

  return defaults


if __name__ == "__main__":
  PrintSourceDefaults("Sphere")
  PrintSourceDefaults("Axis", all=False)
  PrintSourceDefaults("Axis", all=True)
  import pytest
  with pytest.raises(ValueError):
    PrintSourceDefaults("ShouldRaiseError")
