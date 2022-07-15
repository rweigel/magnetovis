def update_defaults(defaults, settings, form='list'):
  """Replace default VTK Properties"""

  import magnetovis as mvs
  mvs.logger.info("Called.")

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

  defaults = {**defaults, **list2dict(settings, defaults)}

  if form == 'dict':
    return defaults
  else:
    defaults_list = []
    for key, default in defaults.items():
      defaults_list.append("{}: {}".format(key, default))
    return defaults_list
