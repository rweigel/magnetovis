def get_defaults(vtkName, debug=False):
   """Get default values for VTK Set methods

    Example:
    --------
      >>> print(get_defaults("vtkSphere"))
      >>> # {'SetCenter': (0.0, 0.0, 0.0), 'SetRadius': 0.5}
   """

   import types
   import vtk

   t = getattr(vtk, vtkName)()

   ignores = [
               'SetAbortExecute',
               'SetDebug', 'SetDefaultExecutivePrototype',
               'SetExecutive', 'SetGlobalWarningDisplay', 'SetInformation', 
               'SetInputConnection', 'SetInputDataObject', 'SetMemkindDirectory',
               'SetProgressObserver', 'SetProgressShiftScale', 'SetProgressText',
               'SetReferenceCount'
            ]

   defaults = {}
   for option in dir(t):
      if option.startswith("Set"):
         if not option in ignores:
            if debug is True:
               print(option)
            getfn = "Get" + option[3:]
            try:
               default = getattr(t, getfn)()
               if isinstance(default, (int, float, tuple, list)):
                  if debug is True:
                     print(" -- default = " + str(default))
                  defaults[option] = default
            except:
               if debug is True:
                  print(" -- default = None")
               defaults[option] = None

   return defaults