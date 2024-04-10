

#, **scalarBarProperties)

mvs.Hide(cb) # cb has "Enabled" but does not do anything in script until image clicked.
mvs.HideColorBar(source=..., display=...)
mvs.ShowColorBar(source=..., display=...)

#colorTF = mvs.SetColorTransferFunction(('POINTS', 'xyz'), rep=, separate=, **options)
# cb = mvs.SetColorBar(color_by=..., proxy=..., display=..., view=..., setparate=..., color_tf=..., **scalarBarProperties)

mvs.ColorBar()

# mvs.ColorBy()
pvs.ColorBy(value=('POINTS', 'Normals'))

# cb = mvs.SetColorBar()
view = pvs.GetActiveViewOrCreate('RenderView')
scalarBar = pvs.GetScalarBar(colorTF, view)
pvs.SetProperties(proxy=scalarBar)#, **scalarBarProperties)

if False:
view = GetActiveViewOrCreate('RenderView')
display = GetDisplayProperties(g, view=view)

colorArrayName = display.GetProperty('ColorArrayName')
colorTF = mvs.SetColorTransferFunction(('POINTS', 'xyz'), rep=, separate=, **options)
mvs.SetColoring(colorArrayName, rep=..., separate=...)

scalarBar = mvs.SetColorBar(('POINTS', 'xyz'), colorTF, rep=rep, view=view, show=, **options)

#g = mvs.GridData(OutputDataSetType="vtkImageData")
[colorTF, scalarBar] = mvs.SetColoring(('POINTS', 'xyz'))
#Hide(ScalarBar)
#mvs.SetTitle("Dataset Type = vtkImageData")



if False:
display = GetDisplayProperties(g, view=view)

colorArrayName = display.GetProperty('ColorArrayName')

mvs.SetColoring(colorArrayName, rep=..., separate=...)

scalarBar = mvs.SetColorBar(('POINTS', 'xyz'), colorTF=colorTf, rep=rep, view=view, show=, **options)

#g = mvs.GridData(OutputDataSetType="vtkImageData")
[colorTF, scalarBar] = mvs.SetColoring(('POINTS', 'xyz'))
#Hide(ScalarBar)
#mvs.SetTitle("Dataset Type = vtkImageData")

