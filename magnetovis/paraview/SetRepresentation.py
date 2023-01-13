def SetRepresentation(*args, proxy=None, representation=None, view=None, **kwargs):

  import paraview.simple as pvs

  if len(args) == 0:
    Representation = 'Surface With Edges'
  else:
    Representation = args[0]

  if proxy is None:
    proxy = pvs.GetActiveSource()
  if view is None:
    view = pvs.GetActiveViewOrCreate('RenderView')
  if representation is None:
    representation = pvs.GetDisplayProperties(proxy=proxy, view=view)

  representation.SetRepresentationType(Representation)
