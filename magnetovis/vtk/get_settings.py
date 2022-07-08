def get_settings(vtkName, form='list'):
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

