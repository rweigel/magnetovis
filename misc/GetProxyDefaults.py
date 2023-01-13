def GetProxyDefaults(pvName):

  # TODO: Is there a way to get properties without putting an object
  #       in the pipeline? See the following for a start.
  if False:
    # https://github.com/Kitware/ParaView/blob/master/Wrapping/Python/paraview/servermanager.py#L2801
    import paraview.servermanager as sm
    pxm = sm.ProxyManager()
    proto = pxm.GetPrototypeProxy('sources','TextSource')
    iter = sm.PropertyIterator(proto)
    properties = {}
    for prop in iter:
       key = iter.GetKey()
       n = prop.GetNumberOfElements()
       if n == 1:
          properties[key] = prop.GetElement(0)
       else:
          properties[key] = []
          for i in range(n):
             properties[key].append(prop.GetElement(i))
    print(properties)

  # https://github.com/Kitware/ParaView/blob/master/Wrapping/Python/paraview/servermanager.py#L408
  import types
  import paraview.simple as pvs
  import magnetovis as mvs

  mvs.logger.info("Called.")

  if isinstance(pvName, str):
      try:
        # Create object
        object = getattr(pvs, pvName)()
      except:
        mvs.logger.info("Cannot get properties for " + pvName)
        return
  else:
    object = pvName

  try:
    # object has outputs
    removeObject = True
    displayObject = pvs.Show(object)
  except:
    # object is a sink (no outputs). E.g., scalar bar and color transfer function.
    # TODO: Need example of this.
    removeObject = False
    displayObject = object

  props = displayObject.ListProperties()
  settings = {}
  for prop in props:
    settings[prop] = displayObject.GetPropertyValue(prop)

  if removeObject:
    pvs.Delete(object)
    del object

  return settings
