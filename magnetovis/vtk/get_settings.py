def get_settings(vtkName, defaults=None, form='list'):
  """Get default values for VTK Set methods

  Example:
  --------
    >>> print(get_settings("vtkSphere"))
    >>> # ['Center: (0.0, 0.0, 0.0)', 'ObjectName: None', 'Radius: 0.5', 'Transform: None']
  """

  import types
  import vtk

  import magnetovis as mvs
  mvs.logger.info("Called.")

  if isinstance(vtkName, str):
    try:
      vtkObject = getattr(vtk, vtkName)()
      mvs.logger.info("Called with input = {}".format(vtkName))
    except:
      mvs.logger.error("Cannot get settings for " + vtkName)
      return {}
  else:
    mvs.logger.info("Called with input = {}".format(vtkName.__vtkname__))
    vtkObject = vtkName

  # Ideally there would be a way to get only native methods so this would not be
  # needed.
  ignores = [
             'SetAbortExecute',
             'SetDebug', 'SetDefaultExecutivePrototype',
             'SetExecutive', 'SetGlobalWarningDisplay', 'SetInformation', 
             'SetInputConnection', 'SetInputDataObject', 'SetMemkindDirectory',
             'SetProgressObserver', 'SetProgressShiftScale', 'SetProgressText',
             'SetReferenceCount', 'SetInputArrayToProcess', 'SetInputData',
             'SetOutput','SetProgress', 'ListProperties', 'SMProxy', 'add_attribute'
          ]

  settings = {}
  for option in dir(vtkObject):
    if option.startswith("Set"):
      if not option in ignores:
        option = option[3:]
        getfn = "Get" + option
        try:
          default = getattr(vtkObject, getfn)()
          if isinstance(default, (int, float, tuple, list)):
            settings[option] = default
          else:
            settings[option] = None
        except:
          settings[option] = False

  if defaults is not None:
    if isinstance(defaults, dict):
      for default in defaults:
        settings[default] = defaults[default]
    else:
      settings = mvs.vtk.update.update_defaults(settings, defaults, form='dict')

  if form == 'dict':
    return settings

  settings_list = []
  for setting_name, setting in settings.items():
    settings_list.append("{}: {}".format(setting_name, setting))

  if form == 'list':
    return settings_list
  else:
    for i in range(len(settings_list)):
      settings_list[i] = settings_list[i].replace("'", "\'")
    return "['" + "', '".join(settings_list) + "']"


if __name__ == "__main__":
  import magnetovis as mvs
  #print(get_settings("vtkAxis", form='dict'))
  print(get_settings("vtkSphere"))
  #print(mvs.vtk.list2dict(get_settings("vtkAxis"), get_settings("vtkAxis", form='dict')))
  if False:
    print(get_settings("vtkTubeFilter"))
    print(get_settings("vtkTubeFilter", defaults={"Radius": 100}))
    print(get_settings("vtkTubeFilter", defaults=["Radius: 100"]))

