def SetTitle(text=None, source=None, view=None, registrationName=None, **kwargs):
  """Set title for active or given view
    SetTitle()
        -> title is registrationName of active source,
           registrationName = '  Title for registrationName'
  
    SetTitle(text)
        -> title is text,
           registrationName = 'Title for view'

     SetTitle(text, source=source)
        -> title is text,
           registrationName = '  Title for registrationName'

     SetTitle(source=source)
        -> title is source registrationName,
           registrationName = '  Title for registrationName'
  """
  import paraview.simple as pvs
  import magnetovis as mvs

  mvs.logger.info("Called.")

  indent = ""
  if source is None:
    source = pvs.GetActiveSource()
  else:
    if source == pvs.GetActiveSource():
      indent = "  "

  if source is not None:
    sourceName = mvs.GetRegistrationName(source)
    if registrationName is None or registrationName == "":
      registrationName = indent + "Title for " + sourceName
    if text is None:
      text = sourceName

  if text is None:
    text = ""

  if view is None:
      view = pvs.GetActiveViewOrCreate('RenderView')

  if view.GetProperty('__magnetovis_title__') is None:
    mvs.logger.info("Creating new title source.")
    textSource = pvs.Text(registrationName=registrationName, Text=text)

    GetPropertyOriginal = view.GetProperty
    def GetProperty(property):
        if property == "__magnetovis_title__":
            return textSource
        else:
            return GetPropertyOriginal(property)

    view.GetProperty = GetProperty
  else:
    mvs.logger.info("Modifying existing title source.")
    textSource = view.GetProperty('__magnetovis_title__')
    textSource.Text = text

  if 'display' in kwargs:
      pvs.Show(proxy=textSource, view=view, **kwargs['display'])
  else:
      pvs.Show(proxy=textSource, view=view)

  if source is not None:
    pvs.SetActiveSource(source)

  return textSource

if __name__ == "__main__":

  import magnetovis as mvs
  t = mvs.SetTitle()
  assert t.GetProperty("Text") == ""

  mvs.ClearPipeline()
  t = mvs.SetTitle("ABC")
  assert t.GetProperty("Text") == "ABC"

  mvs.ClearPipeline()
  mvs.Axis(registrationName="Axis")
  t = mvs.SetTitle()
  assert t.GetProperty("Text") == "Axis"

  mvs.ClearPipeline()
  a = mvs.Axis(registrationName="Axis")
  t = mvs.SetTitle(source=a)
  assert t.GetProperty("Text") == "Axis"

  mvs.ClearPipeline()
  a1 = mvs.Axis(registrationName="Axis1")
  a2 = mvs.Axis(registrationName="Axis2")
  t = mvs.SetTitle(source=a1)
  assert t.GetProperty("Text") == "Axis1"
