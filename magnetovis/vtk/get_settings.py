def get_settings(vtkName, form='list'):
   """Get default values for VTK Set methods

    Example:
    --------
      >>> print(get_settings("vtkSphere"))
      >>> # {'SetCenter': (0.0, 0.0, 0.0), 'SetRadius': 0.5}
   """

   import logging
   import types
   import vtk

   if isinstance(vtkName, str):
      try:
         vtkObject = getattr(vtk, vtkName)()
      except:
         logging.info("Cannot get settings for " + vtkName)
         return {}
   else:
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

            #logging.info(option + " = " + str(settings[option]))

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


#import vtk
#print(get_settings("vtkSphere"))
#print(get_settings(vtk.vtkSphere()))
#print(get_settings("vtkTubeFilter"))
#print(get_settings("vtkUniformGrid"))
#print(get_settings("vtkRectilinearGrid"))
#print(get_settings("vtkStructuredGrid"))