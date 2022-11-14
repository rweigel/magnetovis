def SetColoring(*args, source=None, display=None, view=None, **kwargs):

    import magnetovis as mvs
    import paraview.simple as pvs

    import magnetovis as mvs
    mvs.logger.info("Called with args {}".format(args))
    mvs.logger.info("Called with kwargs {}".format(kwargs))

    if source is None:
        source = pvs.GetActiveSource()
    if view is None:
        view = pvs.GetActiveViewOrCreate('RenderView')
    if display is None:
        print(source)
        print(view)
        display = pvs.GetDisplayProperties(proxy=source, view=view)
        # TODO?: This will make object visible. If possible, reset to
        #        original visibility after call.

    kwargs = kwargs.copy()
    kwargs['value'] = None
    if len(args) != 0:
      kwargs['value'] = args[0]

    if kwargs['value'] is None:
      mvs.logger.info('No color_by given.')
      cellIdInfo = source.GetCellDataInformation().GetArray('CellId')
      if cellIdInfo is not None:
        mvs.logger.info('Found cell data with name CellId. Using.')
        kwargs['value'] = ('CELLS', 'CellId') 
      else:
        mvs.logger.info('No CellId array. Leaving color as default.')
        #mvs.SetColor(proxy=source, representation=display, view=view)
        return

    ctfkwargs = {}
    if 'colorTransferFunction' in kwargs:
      ctfkwargs = kwargs['colorTransferFunction']

    colorTransferFunctionProperties = \
        mvs.GetColorTransferFunctionDefaults(kwargs['value'], source=source, **ctfkwargs)

    if 'colorTransferFunction' in kwargs:
      # Override defaults
      colorTransferFunctionProperties = {
            **colorTransferFunctionProperties, 
            **kwargs['colorTransferFunction']
          }

    opacityTransferFunctionProperties = {}
    if 'opacityTransferFunction' in kwargs:
      # Override defaults
      opacityTransferFunctionProperties = {
            **opacityTransferFunctionProperties, 
            **kwargs['opacityTransferFunction']
          }

    preset = None
    if 'preset' in colorTransferFunctionProperties:
      preset = colorTransferFunctionProperties['preset']
      del colorTransferFunctionProperties['preset']

    separate = False
    if 'separate' in colorTransferFunctionProperties:
      separate = colorTransferFunctionProperties['separate']
      del colorTransferFunctionProperties['separate']

    _range = None
    if 'range' in colorTransferFunctionProperties:
      _range = colorTransferFunctionProperties['range']
      del colorTransferFunctionProperties['range']

    pvs.ColorBy(value=kwargs['value'], rep=display, separate=separate)

    # If this call is made before call to ColorBy, then we need to
    # call again prior to rescaling.
    colorTF = pvs.GetColorTransferFunction(\
                kwargs['value'][1], representation=display,\
                separate=separate, **colorTransferFunctionProperties)

    opacityTF = pvs.GetOpacityTransferFunction(\
                kwargs['value'][1], representation=display,\
                separate=separate, **opacityTransferFunctionProperties)

    if preset is not None:
      colorTF.ApplyPreset(preset)

    if False:
      # TODO.
      if kwargs['value'][1] == 'CELLS':
        r = source.CellData[kwargs['value'][1]]
      if kwargs['value'][1] == 'POINTS':
        r = source.CellData[kwargs['value'][1]]
      lims = [r.GetRange(0), r.GetRange(1), r.GetRange(2)]
      
      # Compute new limits using
      # colorTF.RescaleTransferFunction(0.0, 1.2)
      # Compute new tick values given number of colors or compute
      # number of colors given tick values.
      # Turn on annotations for min and max

    scalarBarPropertiesRequested = {}
    if 'scalarBar' in kwargs:
      scalarBarPropertiesRequested = kwargs['scalarBar']
      del kwargs['scalarBar']

    if _range is not None:
      colorTF.RescaleTransferFunction(*_range)
      opacityTF.RescaleTransferFunction(*_range)

    scalarBarProperties = mvs.GetScalarBarDefaults(kwargs['value'], colorTF=colorTF)
    # Override defaults
    scalarBarProperties = {**scalarBarProperties, **scalarBarPropertiesRequested}

    scalarBar = pvs.GetScalarBar(colorTF, view)

    # GetScalarBar does not have option to pass properties,
    # so must do via SetProperties (compare code for
    # GetColorTransferFunction with GetScalarBar in
    # https://kitware.github.io/paraview-docs/latest/python/_modules/paraview/simple.html
    pvs.SetProperties(proxy=scalarBar, **scalarBarProperties)

    mvs.logger.info("Calling pvs.HideScalarBarIfNotNeeded() and UpdateScalarBars().")
    pvs.HideScalarBarIfNotNeeded(colorTF, view=view)
    pvs.UpdateScalarBars(view=view)

    # See https://stackoverflow.com/a/63028935 for rescaling to visible range.
    mvs.logger.info("Calling pvs.RescaleTransferFunctionToDataRange().")
    # For explanation of False, True see
    # https://kitware.github.io/paraview-docs/latest/cxx/classvtkSMPVRepresentationProxy.html#a67200556fed6885f56753a450f2a2956
    # (False, True) is what is used when the rescale button is clicked in the GUI.
    display.RescaleTransferFunctionToDataRange(False, True)
    #display.SetScalarBarVisibility(view, True) 

    view.Update()

    return scalarBar, colorTF, opacityTF
