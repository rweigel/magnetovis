def SetDisplayProperties(source=None, view=None, **kwargs):

    import paraview.simple as pvs
    import magnetovis as mvs

    import magnetovis as mvs
    mvs.logger.info("Called.")

    if source is None:
        source = pvs.GetActiveSource()

    mvs.logger.info("Source object is a ParaView " + source.__class__.__name__)
    name = type(source).__name__
    if name.startswith("Magnetovis"):
        # Plugin
        name = name[len("Magnetovis"):] # Remove "Magnetovis" prefix
    else:
        # Programmable source
        name = source.GetProperty("__magnetovis_name__")
    mvs.logger.info("Source object is a Magnetovis " + name)

    sourceVisibility = True
    if 'sourceVisibility' in kwargs:
        sourceVisibility = kwargs['sourceVisibility']

    view = None
    if 'view' in kwargs:
        view = kwargs['view']
    if view is None:
        view = pvs.GetActiveViewOrCreate('RenderView')

    #logging.info("View settings: {}".format(mvs.GetSettings(view)))
    
    import importlib
    mvsObj = importlib.import_module('magnetovis.Sources.' + name)
    
    defaults = None
    displaySettings = {'Representation': 'Surface'}
    if hasattr(mvsObj, 'GetDisplayDefaults'):
        defaults = mvsObj.GetDisplayDefaults()
        if 'display' in defaults:
            displaySettings = {**displaySettings, **defaults['display']}
    if 'display' in kwargs:
        displaySettings = {**displaySettings, **kwargs['display']}
        del kwargs['display']

    mvs.logger.info("Calling Show()")
    display = pvs.Show(proxy=source, view=view, **displaySettings)
    #logging.info("Display settings: {}".format(mvs.GetSettings(display)))

    coloringSettings = {}
    if defaults is not None and 'coloring' in defaults:
        coloringSettings = defaults['coloring']
    if kwargs is not None and 'coloring' in kwargs:
        coloringSettings = {**coloringSettings, **kwargs['coloring']}

    mvs.SetColoring(source=source, view=view, display=display, **coloringSettings)

    # Hides unused scalar bars
    pvs.UpdateScalarBars(view=view)

    # This property is not available in display until after the call to pvs.ColorBy.
    display.RescaleTransferFunctionToDataRange = 0

    children = None
    if hasattr(mvsObj, 'SetDisplayProperties'):
        if hasattr(source, "__magnetovis_children"):
            for child in source.__magnetovis_children:
                pvs.Delete(child)

        children = mvsObj \
                    .SetDisplayProperties( \
                        source, view=view, display=display, **kwargs)

        if children is not None:
            if not isinstance(children, list):
                children = [children]
            source.add_attribute("__magnetovis_children", children)

        pvs.SetActiveSource(source)
    
    if sourceVisibility == False:
        pvs.Hide(source, view)

    camera = mvs.SetCamera(view=view, source=source, viewType="isometric")

    view.Update()

    return children