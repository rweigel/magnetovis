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

    # If called more than once, need to delete existing children.
    children = source.GetProperty("__magnetovis_children__")
    if children is not None:
        for child in children:
            cname = list(child.keys())[0]
            mvs.logger.info("Deleting child " + cname)
            pvs.Delete(child[cname])
    else:
        mvs.logger.info("No children.")

    sourceVisibility = True
    if 'sourceVisibility' in kwargs:
        sourceVisibility = kwargs['sourceVisibility']

    view = None
    if 'view' in kwargs:
        view = kwargs['view']
    if view is None:
        view = pvs.GetActiveViewOrCreate('RenderView')
    
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
        kwargs['display'] = displaySettings

    mvs.logger.info("Calling Show()")
    display = pvs.Show(proxy=source, view=view, **displaySettings)

    coloringSettings = {}
    if defaults is not None and 'coloring' in defaults:
        coloringSettings = defaults['coloring']
    if kwargs is not None and 'coloring' in kwargs:
        coloringSettings = {**coloringSettings, **kwargs['coloring']}

    mvs.SetColoring(source=source, view=view, display=display, **coloringSettings)

    children = None
    if hasattr(mvsObj, 'SetDisplayProperties'):

        # Call the function magnetovis/Sources/{name}.py
        children = mvsObj \
                    .SetDisplayProperties( \
                        source, view=view, **kwargs)

        if children is not None:
            if not isinstance(children, list):
                children = [children]

        # Active source will be the last child. Set it back
        # to the main source.
        pvs.SetActiveSource(source)
    
    if sourceVisibility == False:
        pvs.Hide(source, view)

    camera = mvs.SetCamera(view=view, source=source, viewType="isometric")

    view.Update()

    return children