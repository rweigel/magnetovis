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
        display = pvs.GetDisplayProperties(proxy=source, view=view)
        # TODO?: This will make object visible. If possible, reset to
        #        original visibility after call.

    kwargs = kwargs.copy()
    kwargs['value'] = None
    if len(args) != 0:
      kwargs['value'] = args[0]
    if 'separate' not in kwargs:
      kwargs['separate'] = True

    if kwargs['value'] is None:
      mvs.logger.info('No color_by given.')
      cellIdInfo = source.GetCellDataInformation().GetArray('CellId')
      if cellIdInfo is not None:
        mvs.logger.info('Found cell data with name CellId. Using.')
        kwargs['value'] = ('CELLS', 'CellId') 
      else:
        mvs.logger.info('No CellId array. Will give solid color.')
        mvs.SetColor(proxy=source, representation=display, view=view)
        return

    colorTransferFunctionProperties = \
        mvs.GetColorTransferFunctionDefaults(kwargs['value'], source=source)

    if 'colorTransferFunction' in kwargs:
      # Override defaults
      colorTransferFunctionProperties = {
            **colorTransferFunctionProperties, 
            **kwargs['colorTransferFunction']
          }
      del kwargs['colorTransferFunction']

    # TODO: Allow a parameter "TransferFunctionName" to be bassed
    #       and then apply after this line using colorTF.ApplyPreset.
    colorTF = pvs.GetColorTransferFunction(\
                kwargs['value'][1], representation=display,\
                separate=True, **colorTransferFunctionProperties)

    scalarBarPropertiesRequested = {}
    if 'scalarBar' in kwargs:
      scalarBarPropertiesRequested = kwargs['scalarBar']
      del kwargs['scalarBar']

    pvs.ColorBy(display, **kwargs)

    #colorTF.ApplyPreset()

    scalarBarProperties = mvs.GetScalarBarDefaults(kwargs['value'], colorTF=colorTF)
    # Override defaults
    scalarBarProperties = {**scalarBarProperties, **scalarBarPropertiesRequested}

    scalarBar = pvs.GetScalarBar(colorTF, view)

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

    # GetScalarBar does not have option to pass properties,
    # so must do via SetProperties (compare code for
    # GetColorTransferFunction with GetScalarBar in
    # https://kitware.github.io/paraview-docs/latest/python/_modules/paraview/simple.html
    pvs.SetProperties(proxy=scalarBar, **scalarBarProperties)

    mvs.logger.info("Calling pvs.HideScalarBarIfNotNeeded()")
    pvs.HideScalarBarIfNotNeeded(colorTF, view)

    # Hides unused scalar bars if they have HideScalarBarIfNotNeeded set.
    pvs.UpdateScalarBars(view=view)

    # RescaleTransferFunctionToDataRange is not available in display
    # until after the call to pvs.ColorBy. Needed?
    # display.RescaleTransferFunctionToDataRange()

    view.Update()

    return [colorTF, scalarBar]
