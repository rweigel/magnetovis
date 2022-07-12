def update_defaults(defaults, settings, form='list'):

  import magnetovis as mvs

  if isinstance(defaults, list) and isinstance(settings, list):

    defaults_dict = {}
    for default in defaults:
      key = default.split(":")[0].strip()        
      val = default.split(":")[1].lstrip().rstrip()
      defaults_dict[key] = val

    settings_dict = {}
    for setting in settings:
      key = setting.split(":")[0].strip()        
      val = setting.split(":")[1].lstrip().rstrip()
      settings_dict[key] = val

    defaults_dict = {**defaults_dict, **settings_dict}

    defaults_list = []
    for key in defaults_dict:
      defaults_list.append(key + ": " + defaults_dict[key])

    return defaults_list

  for setting in settings:

    key = setting.split(":")[0].strip()        
    val = setting.split(":")[1].lstrip().rstrip()

    assert key in defaults, key + " is not a valid setting."
    default = defaults[key]

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

    mvs.logger.info("Setting {} = {}".format(key, val))
    defaults[key] = val

  if form == 'dict':
    return defaults
  else:
    defaults_list = []
    for key, default in defaults.items():
      defaults_list.append("{}: {}".format(key, default))
    return defaults_list


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

   if isinstance(vtkName, str):
      try:
         vtkObject = getattr(vtk, vtkName)()
         mvs.logger.info("Called with input = {}".format(vtkName))
      except:
         mvs.logger.info("Cannot get settings for " + vtkName)
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
               'SetReferenceCount', 'SetInputArrayToProcess', 'SetInputData', 'SetOutput','SetProgress'
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

            #mvs.logger.info(option + " = " + str(settings[option]))

   if defaults is not None:
      if isinstance(defaults, dict):
         for default in defaults:
            settings[default] = defaults[default]
      else:
         settings = update_defaults(settings, defaults, form='dict')

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
   print(get_settings("vtkSphere"))
   print(get_settings("vtkTubeFilter"))
   print(get_settings("vtkTubeFilter", defaults={"Radius": 100}))
   print(get_settings("vtkTubeFilter", defaults=["Radius: 100"]))

