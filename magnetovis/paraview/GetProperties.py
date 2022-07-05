def GetProperties(pvName, form='dict'):

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

   import magnetovis as mvs

   if isinstance(pvName, str):
      try:
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
      removeObject = False
      displayObject = object


   props = displayObject.ListProperties()
   settings = {}
   for prop in props:
      settings[prop] = displayObject.GetPropertyValue(prop)

   if removeObject:
      pvs.Delete(object)
      del object

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
   import paraview.simple as pvs
   import pprint
   print("Text")
   pprint.pprint(GetProperties("Text"))
   print("Sphere")
   pprint.pprint(GetProperties("Sphere"))
