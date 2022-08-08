def SetColor(*args, proxy=None, representation=None, view=None, **kwargs):
  """Solid color a geometry or text representation

  This helper function can be used to reduce the amount of code needed
  to color a proxy with a Geometry, Grid, Ruler, or Text representation.

  For an object with a Geometry representation, use

  import paraview.simple as pvs
  import magnetovis as mvs
  s = pvs.Sphere()
  mvs.SetColor([0, 0, 1]) # Colors active proxy in active view and shows.
  # or
  mvs.SetColor('red') # See GetColorRGB() for list of named colors.

  instead of

    import paraview.simple as pvs
    s = pvs.Sphere()
    pvs.Show()
    view = pvs.GetActiveViewOrCreate('RenderView')
    rep = pvs.GetDisplayProperties(proxy=s, view=view)
    kwargs = {'DiffuseColor': [0, 0, 1], 'AmbientColor': [0, 0, 1]}
    pvs.Show(ColorArrayName=[None, ''], **kwargs)

  Although little code is need for coloring text, for consistency, one
  can use
    
    import paraview.simple as pvs
    import magnetovis as mvs
    t = pvs.Text(Text="The Text")
    mvs.SetColor([1, 0, 0])
    # or
    mvs.SetColor('red')

  instead of
  
    import paraview.simple as pvs
    t = pvs.Text(Text="The Text")
    pvs.Show(Color=[1, 0, 0])

  Also,
    import paraview.simple as pvs
    r = pvs.Text(Text="The Text")
    mvs.SetColor([1, 0, 0])
    # or
    mvs.SetColor('red')

"""
  import paraview.simple as pvs
  import magnetovis as mvs

  if len(args) == 0:
    Color = [0.5, 0.5, 0.5]
  else:
    Color = args[0]
    if isinstance(Color, str):
      Color = mvs.GetColorRGB(Color)

  if proxy is None:
    proxy = pvs.GetActiveSource()
  if view is None:
    view = pvs.GetActiveViewOrCreate('RenderView')
  if representation is None:
    representation = pvs.GetDisplayProperties(proxy=proxy, view=view)

  name = representation.__class__.__name__

  kwargs = kwargs.copy()
  if name.startswith('Geometry') or 'Grid' in name:
    if 'DiffuseColor' not in kwargs:
      kwargs['DiffuseColor'] = Color
    if 'AmbientColor' not in kwargs:
      kwargs['AmbientColor'] = Color
    pvs.SetProperties(proxy=representation, ColorArrayName=[None, ''], **kwargs)
  elif name == 'TextSourceRepresentation':
    kwargs['Color'] = Color
    pvs.SetProperties(proxy=representation, **kwargs)
  elif name == 'RulerSourceRepresentation':
    if 'AxisColor' not in kwargs:
      kwargs['AxisColor'] = Color
    kwargs['Color'] = Color
    pvs.SetProperties(proxy=representation, **kwargs)
  else:
    raise ValueError('Representation cannot be colored using SetColor.')

  pvs.HideUnusedScalarBars(view=view)