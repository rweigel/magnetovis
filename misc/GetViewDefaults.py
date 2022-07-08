def GetViewDefaults():

  """Note used"""
  
  # View
  if not 'view' in defaults:
    defaults['view'] = {}

  v = pvs.GetActiveView()
  for key in dir(v):
    if key.startswith('_') == False and not key in defaults['view']:
      defaults['view'][key] = v.GetPropertyValue(key)

  # Colorbar, etc.
  for rep in defaults['view']['Representations']:
    pvs.Delete(rep)
