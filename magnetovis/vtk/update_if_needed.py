def update_if_needed(defaults, kwargs, vtkProxyName, key=None, val=None):
  """Replace default VTK Property value with a default"""

  import magnetovis as mvs

  defaults_dict = mvs.vtk.list2dict(defaults[vtkProxyName], mvs.vtk.get_settings(vtkProxyName, form='dict'))
  if vtkProxyName in kwargs:
      kwargs_dict = mvs.vtk.list2dict(kwargs[vtkProxyName], mvs.vtk.get_settings(vtkProxyName, form='dict'))
      print("yyy")
      print(kwargs_dict)
      print("yyy")
      if not key in kwargs_dict:
          # Update
          defaults_dict[key] = val
      else:
          # No update
          defaults_dict[key] = kwargs_dict[key]
  else:
      defaults_dict[key] = val

  defaults_list = []
  for key in defaults_dict:
      defaults_list.append(f"{key}: {defaults_dict[key]}")

  defaults[vtkProxyName] = defaults_list

  return defaults
