def SetColoring(source=None, display=None, view=None, **kwargs):

    import magnetovis as mvs
    import paraview.simple as pvs

    import magnetovis as mvs
    mvs.logger.info("Called with kwargs {}".format(kwargs))

    if source is None:
        source = pvs.GetActiveSource()
    if view is None:
        view = pvs.GetActiveViewOrCreate('RenderView')
    if display is None:
        display = pvs.GetDisplayProperties(proxy=source, view=view)

    mvs.logger.info("source = {}".format(source))
    mvs.logger.info("display = {}".format(display))

    if "colorBy" not in kwargs:
        ColorByCellId(source=source, display=display, view=view, **kwargs)
        return
    else:
        colorBy = kwargs['colorBy']
        if kwargs['colorBy'] is None:
            mvs.logger.info('coloring = None. Not coloring by an array.')
            try:
                # Will fail if colorBy was not previously set.
                pvs.ColorBy(display, None, separate=True)
            except:
                pass
            return

    #print(kwargs['colorBy'])
    mvs.logger.info("Calling pvs.ColorBy with display = {}".format(display))
    pvs.ColorBy(display, value=kwargs['colorBy'], separate=True)

    colorTFSettings = {}
    if 'colorTransferFunction' in kwargs:
        colorTFSettings = kwargs['colorTransferFunction'].copy()
    if not 'NumberOfTableValues' in colorTFSettings:
        # TODO: This should be stored externally
        colorTFSettings['NumberOfTableValues'] = 32

    colorTF = pvs.GetColorTransferFunction(colorBy[1], representation=display, separate=True, **colorTFSettings)

    scalarBar = pvs.GetScalarBar(colorTF, view)

    scalarBarSettings = {}
    if 'scalarBar' in kwargs:
        scalarBarSettings = kwargs['scalarBar']
    if not 'HorizontalTitle' in scalarBarSettings:
        # TODO: This setting should be stored externally
        scalarBarSettings['HorizontalTitle'] = 1

    # GetScalarBar does not have option to pass settings,
    # so must do it here.
    pvs.SetProperties(proxy=scalarBar, **scalarBarSettings)
    props = scalarBar.ListProperties()
    settings = {}
    for prop in props:
        settings[prop] = scalarBar.GetPropertyValue(prop)

    mvs.logger.info("Setting HideScalarBarIfNotNeeded")
    pvs.HideScalarBarIfNotNeeded(colorTF, view)

    # Hides unused scalar bars if HideScalarBarIfNotNeeded set.
    pvs.UpdateScalarBars(view=view)

    # This property is not available in display until after the call to pvs.ColorBy.
    # display.RescaleTransferFunctionToDataRange()

    view.Update()

def ColorByCellId(source=None, view=None, display=None, **displayArguments):

    import paraview.simple as pvs

    import magnetovis as mvs
    mvs.logger.info("Called.")

    name = 'CellId'
    cellIdInfo = source.GetCellDataInformation().GetArray(name)

    if cellIdInfo is None:
        mvs.logger.info('No CellId array. No coloring performed.')
        return
    else:
        n_cells = cellIdInfo.GetNumberOfTuples()

    pvs.ColorBy(rep=display, value=('CELLS', name), separate=True)

    mvs.logger.info(str(n_cells) + " cells")

    scalarBarVisibility = True
    if "scalarBarVisibility" in displayArguments:
        scalarBarVisibility = displayArguments['scalarBarVisibility']
    display.SetScalarBarVisibility(view, scalarBarVisibility)

    lookupTable = pvs.GetColorTransferFunction(name, display)
    lookupTable.AutomaticRescaleRangeMode = "Grow and update on 'Apply'"

    lookupTable.NumberOfTableValues = n_cells
    colorBar = pvs.GetScalarBar(lookupTable, view)
    colorBar.HorizontalTitle = 1
    colorBar.Title = "CellId"
    colorBar.ComponentTitle = ""

    if n_cells <= 8:
        # When the number of cells is small, extra tick labels appear
        # in legend that are not needed. We can't control the number of tick
        # labels, so here we switch to a categorical legend.

        # Make coloring consistent with default coloring when n_cells > 8.
        # Default is "Cool to Warm". RGB control points used are from
        # https://github.com/Kitware/ParaView/blob/master/Wrapping/Python/paraview/_colorMaps.py

        import vtk
        ctf = vtk.vtkColorTransferFunction()
        ctf.SetColorSpaceToHSV()
        ctf.SetColorSpaceToDiverging()
        ctf.AddRGBPoint(n_cells-1, 0.23137254902, 0.298039215686, 0.752941176471)
        ctf.AddRGBPoint((n_cells-1)/2, 0.865, 0.865, 0.865)
        ctf.AddRGBPoint(0, 0.705882352941, 0.0156862745098, 0.149019607843)

        lookupTable.InterpretValuesAsCategories = 1
        IndexedColors = []
        Annotations = []
        for i in range(n_cells):
            Annotations.append(str(n_cells-1-i))
            Annotations.append(str(n_cells-1-i))
            rgb = ctf.GetColor(i)
            IndexedColors.append(rgb[0])
            IndexedColors.append(rgb[1])
            IndexedColors.append(rgb[2])
        lookupTable.Annotations = Annotations
        lookupTable.IndexedColors = IndexedColors
        lookupTable.IndexedOpacities = n_cells*[1.0]
    else:
        lookupTable.InterpretValuesAsCategories = 0
        lookupTable.Annotations = []

        # Force legend color squares to be centered on integers
        #lookupTable.RescaleTransferFunction(-0.5, n_cells - 0.5)
        #print(dir(lookupTable))
        # Use integer labels
        colorBar.AutomaticLabelFormat = 0
        colorBar.LabelFormat = '%.f'
        colorBar.AddRangeLabels = 0

    #print("----Deleting")
    #print(colorBar)
    #pvs.Delete(colorBar)
    #del colorBar
