def SetOrientationAxisLabel(Text=None, Position=None, FontSize=14, view=None):

  import paraview.simple as pvs
  import magnetovis as mvs

  if Text is None:
    Text = mvs.coord_sys_view # + r" [$\mathrm{R}_\mathrm{E}$]"

  if view is None:
      view = pvs.GetActiveViewOrCreate('RenderView')

  textSource = pvs.Text(Text=Text, registrationName='Orientation Axis Label')
  text2Display = pvs.Show(textSource, view, 'TextSourceRepresentation')
  text2Display.FontSize = FontSize

  if Position is None:
    text2Display.WindowLocation = 'Lower Left Corner'
  else:
    text2Display.Position = [0.05, 0.05]

  return textSource