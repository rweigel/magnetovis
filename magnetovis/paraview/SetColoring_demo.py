
# Demo 1
import paraview.simple as pvs
import magnetovis as mvs
mvs.ClearPipeline()
s = pvs.Sphere()
c = pvs.Calculator(Input=s)
c.ResultArrayName = 'XYZ'
c.Function = 'coordsX*iHat + coordsY*jHat'
mvs.SetColoring()

# Demo 2
import paraview.simple as pvs
import magnetovis as mvs
mvs.CreateViewAndLayout()
s = pvs.Sphere()
c = pvs.Calculator(Input=s)
c.ResultArrayName = 'XYZ'
c.Function = 'coordsX*iHat + coordsY*jHat + coordsZ*kHat'
mvs.SetColoring(('POINTS', 'XYZ', 'X'))

def HideScalarBar(sb=None, proxy=None, view=None, representation=None):

  if proxy is None:
      proxy = pvs.GetActiveSource()
  if view is None:
      view = pvs.GetActiveViewOrCreate('RenderView')
  if representation is None:
      representation = pvs.GetDisplayProperties(proxy=proxy, view=view)

  representation.SetScalarBarVisibility(view, False)

def ShowScalarBar(sb=None, proxy=None, view=None, representation=None):

  if proxy is None:
      proxy = pvs.GetActiveSource()
  if view is None:
      view = pvs.GetActiveViewOrCreate('RenderView')
  if representation is None:
      representation = pvs.GetDisplayProperties(proxy=proxy, view=view)

  representation.SetScalarBarVisibility(view, True)

# Demo 3
# If separate is not set to True, colorbar limits on previous layout changes!
import paraview.simple as pvs
import magnetovis as mvs
mvs.CreateViewAndLayout()
s = pvs.Sphere(Radius=1)
c = pvs.Calculator(Input=s)
c.ResultArrayName = 'XYZ'
c.Function = 'coordsX*iHat + coordsY*jHat + coordsZ*kHat'
colorTF = {"range": [-0.5, 0.5 ], "separate": True}
sb, ctf, otf = mvs.SetColoring(('POINTS', 'XYZ', 'X'), colorTransferFunction=colorTF)
#HideScalarBar()
#ShowScalarBar()

#print(mvs.GetSourceDefaults(ctf))
#print(mvs.GetSourceDefaults(sb))

def sphere(Radius=1, Center=[0, 0, 0], color_by=None, separate_tf=False, separate_cb=False):

  view = pvs.GetActiveViewOrCreate('RenderView')
  s = pvs.Sphere(Radius=Radius, Center=Center)
  c = pvs.Calculator(Input=s)
  c.ResultArrayName = 'XYZ'
  c.Function = 'coordsX*iHat + coordsY*jHat'

  # show data in view
  pvs.Show(c, view, 'GeometryRepresentation')

  display = pvs.GetDisplayProperties(c)
  display.SetRepresentationType('Surface')

  value = ('POINTS', 'XYZ', color_by)
  # GetColorTransferFunction() must go before ColorBy if modified.
  # separate = True in call to GetColorTransferFunction
  # causes TF to be created with a unique array name of
  # 'Separate' + ID + _value[0], where ID is unique id of active source.
  colorTF = pvs.GetColorTransferFunction(value[1], display, separate=separate_tf)

  # Allow input of _Range.
  #colorTF.RescaleTransferFunction(-1.0, 2.0)
  #colorTF.ApplyPreset('Black, Blue and White', True)

  # If separate=True, sets display.UseSeparateColorMap = True
  # Internally it seems that when a value is shown when
  # UseSeparateColorMap = True, the unique array name is looked
  # for when display.SetScalarColoring() is executed in ColorBy().
  pvs.ColorBy(rep=display, value=value, separate=separate_cb)

  # If separate=True in ColorBy, a new color bar is created even if
  # one exists for `value`.
  scalarBar = pvs.GetScalarBar(colorTF, view)
  scalarBar.ScalarBarLength = 0.9

  # We must set title and component title here if we do not want
  # to call pvs.UpdateScalarBars(view=view), reveals
  # colorbars that may have been previously hidden but also
  # changes the title and component title from "Name" and "Component"
  # to the value[1] and value[2].
  scalarBar.Title = 'X (left sphere) Y (right sphere)'
  scalarBar.ComponentTitle = ''

  # If this is not done, label is "Name Component" and colorbar stays
  # visisble after hiding.
  #pvs.UpdateScalarBars(view=view)

  return colorTF, scalarBar


if False:
  tf, sb = sphere(Radius=1, color_by='X', separate_cb=False, separate_tf=False)
  print(tf.ListProperties())
  print(sb.ListProperties())
  print(mvs.GetSourceDefaults(tf))
  print(mvs.GetSourceDefaults(sb))
  # Next call causes color_by to be set to 'Y' for first sphere.
  # This is unexpected b/c call to ColorBy when the following was
  # only passed the display of the second sphere.
  sphere(Radius=1, Center=[2, 1, 0], color_by='Y', separate_cb=False, separate_tf=False)

  mvs.CreateViewAndLayout()
  # Two colorbars shown and hiding first works
  sphere(Radius=1, color_by='X', separate_cb=True, separate_tf=True)
  HideScalarBar()
  sphere(Radius=1, Center=[2, 1, 0], color_by='Y', separate_cb=True, separate_tf=True)
