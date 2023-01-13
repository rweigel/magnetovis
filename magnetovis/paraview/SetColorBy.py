def SetColorBy(color_by, proxy=None, display=None, view=None, **kwargs):

    import magnetovis as mvs
    import paraview.simple as pvs

    import magnetovis as mvs
    mvs.logger.info("Called with kwargs {}".format(kwargs))

    if proxy is None:
        proxy = pvs.GetActiveSource()
    if view is None:
        view = pvs.GetActiveViewOrCreate('RenderView')
    if display is None:
        display = pvs.GetPresentationProperties(proxy=proxy, view=view)
        # TODO: This will make object visible. If possible, reset to
        #       original visibility after call?

    kwargs = kwargs.copy()
    if 'separate' not in kwargs:
      kwargs['separate'] = True

    pvs.ColorBy(display, value=kwargs['colorBy'], **kwargs)

    colorTF = pvs.GetColorTransferFunction(color_by[1], representation=display, separate=kwargs['separate'])
