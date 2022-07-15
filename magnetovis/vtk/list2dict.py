def list2dict(settings, defaults):

  import magnetovis as mvs
  mvs.logger.info("Called.")

  if settings is None:
    return {}

  assert isinstance(defaults, dict), "defaults must be a dictionary"
  assert isinstance(settings, list), "settings must be a list"

  settings_dict = {}
  for setting in settings:
    key = setting.split(":")[0].strip()        
    val = setting.split(":")[1].strip()

    assert key in defaults, key + " is not a valid setting."
    default = defaults[key]

    if val == 'True':
      val = True
    elif val == 'False':
      val = False
    elif val == 'None':
      val = None
    elif isinstance(default, int):
      val = int(val)
    elif isinstance(default, float):
      val = float(val)
    elif isinstance(default, tuple):
      val = val[1:-1].split(",")
    else:
      raise NotImplementedError(f"Unrecognized value {val} for defaults[{key}]")

    if isinstance(val,list):
      if isinstance(default[0], float):
        val = tuple([float(v) for v in val])
      elif isinstance(default[0], int):
        val = tuple([int(v) for v in val])

    settings_dict[key] = val

  return settings_dict

