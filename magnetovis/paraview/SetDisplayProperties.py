def SetDisplayProperties(programmableSource, renderView=None, displayArguments=None):

    import logging
    import paraview.simple as pvs

    logging.info("Called.")

    displayRepresentation = 'Surface'
    if displayArguments is not None:
        if 'displayRepresentation' in displayArguments:
            # TODO: Get this list dynamically in case it gets expanded.
            validRepresentations = [
                                    'Surface', '3D Glyphs', 'Feature Edges',
                                    'Outline', 'Point Gaussian', 'Points',
                                    'Surface With Edges', 'Wireframe', 'Volume'
                                 ]

            assert displayArguments['displayRepresentation'] in validRepresentations, \
                    "Invalid displayRepresentation ({}). displayRepresentation must be one of: {}" \
                       .format(displayProperties['displayRepresentation'],
                                 validRepresentations)

            displayRepresentation = displayArguments['displayRepresentation']

    showSource = True
    renderView = None
    if displayArguments is not None:
        if 'showSource' in displayArguments:
            showSource = displayArguments['showSource']
            del displayArguments['showSource']
        if 'renderView' in displayArguments:
            renderView = displayArguments['renderView']
            del displayArguments['renderView']

    if renderView is None:
        renderView = pvs.GetActiveViewOrCreate('RenderView')

    if displayArguments is None:
        displayArguments = {}

    #displayArguments['registrationName'] = programmableSource.GetLogName()
    #displayArguments['registrationName'] = self.registrationName

    # Create display properties object
    displayProperties = pvs.Show(programmableSource, renderView)
    displayProperties.Representation = displayRepresentation

    logging.info("Source object is a ParaView " + programmableSource.__class__.__name__)
    name = type(programmableSource).__name__
    if name.startswith("Magnetovis"):
        # Plugin
        name = name[len("Magnetovis"):] # Remove "Magnetovis" prefix
    else:
        # Programmable source
        name = programmableSource.GetProperty("__magnetovis_name__")

    logging.info("Source object is a Magnetovis " + name)
    import importlib
    
    object = importlib.import_module('magnetovis.Sources.' + name)
    if hasattr(object, 'SetDisplayProperties'):
        object.SetDisplayProperties(programmableSource,
                                    renderView=renderView,
                                    displayProperties=displayProperties,
                                    **displayArguments)

    # Update the view to ensure updated data information
    # TODO: Needed?
    renderView.Update()
    
    if showSource == False:
        pvs.Hide(programmableSource, renderView)
    
    return displayProperties
