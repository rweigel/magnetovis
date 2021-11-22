def ColorByCellId(programmableSource, renderView=None, displayProperties=None, **displayArguments):

    import paraview.simple as pvs

    import logging
    logging.info("called.")

    name = 'CellIds'
    n_cells = programmableSource.GetCellDataInformation().GetArray(name).GetNumberOfTuples()
    pvs.ColorBy(displayProperties, ('CELLS', name))

    logging.info(str(n_cells) + " cells")

    scalarBarVisibility = True
    if "scalarBarVisibility" in displayArguments:
        scalarBarVisibility = displayArguments['scalarBarVisibility']

    displayProperties.SetScalarBarVisibility(renderView, scalarBarVisibility)

    lookupTable = pvs.GetColorTransferFunction(name, displayProperties)
    lookupTable.AutomaticRescaleRangeMode = "Update on 'Apply'"

    lookupTable.NumberOfTableValues = n_cells
    colorBar = pvs.GetScalarBar(lookupTable, renderView)
    colorBar.HorizontalTitle = 1

    if (n_cells <= 8):
        # When the number of cells is small, extra tick labels appear
        # in legend that are not needed. We can't control the number of tick
        # labels, so here we switch to a categorical legend.
        # TODO: Use consistent coloring by getting the default colors
        # for a regular legend with n_cells colors and then use them
        # below for IndexedColors.
        lookupTable.InterpretValuesAsCategories = 1
        Annotations = ['0', '0',
                       '1', '1',
                       '2', '2',
                       '3', '3',
                       '4', '4',
                       '5', '5',
                       '6', '6',
                       '7', '7']
        lookupTable.Annotations = Annotations[0:2*n_cells]
        IndexedColors = [0.00, 0.50, 1.00,
                         1.00, 1.00, 0.00,
                         0.00, 1.00, 0.00,
                         0.00, 0.00, 1.00,
                         1.00, 1.00, 0.00,
                         1.00, 0.00, 1.00,
                         0.00, 1.00, 1.00,
                         0.63, 0.63, 1.00]
        lookupTable.IndexedColors = IndexedColors[0:3*n_cells]
        lookupTable.IndexedOpacities = n_cells*[1.0]
    else:
        # Force legend color squares to be centered on integers
        lookupTable.RescaleTransferFunction(-0.5, n_cells - 0.5)

        # Use integer labels
        colorBar.AutomaticLabelFormat = 0
        colorBar.LabelFormat = '%.f'
        colorBar.AddRangeLabels = 0