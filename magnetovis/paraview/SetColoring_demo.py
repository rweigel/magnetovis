import magnetovis as mvs
source = mvs.GridData(OutputDataSetType="vtkImageData")
mvs.SetTitle("Dataset Type = vtkImageData")

ckwargs =  {
    'scalarBar': {
                    'Title': r"$" + name.replace("|","\|") + "$ [nT]",
                    'ComponentTitle': '',
                    'HorizontalTitle': 1,
                    'TitleJustification': 'Left',
                    'Visibility': 1,
                    'ScalarBarLength': 0.8
                },
    'colorTransferFunction': {
                                "separate": True,
                                "UseLogScale": False
                            }
}
mvs.SetColoring(('CELLS', 'CellId'), source=source, **ckwargs)
