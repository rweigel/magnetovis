def CreateViewAndLayout(name=None, viewType=None):
    
  # The types of ParaView views are Render View, Spreadsheet View, etc.
  # A layout is a tab in the ParaView GUI.
  # It seems possible to switch between view type in a given layout.
  # However, there does not seem to be a way to switch a view in a given
  # layout from that GUI. In addition, to have a new view, it seems
  # easy enough to just create a new layout with that view.
  import paraview.simple as pvs
  import magnetovis as mvs

  if viewType is None:
      viewType = 'RenderView'

  name = mvs.UniqueName(name=name, proxyType="layout")
  # If following line happens after two lines after it,
  # get problems with colorbars on previous layouts.
  layout = pvs.CreateLayout(name=name)
  pvs.SetActiveView(None)
  view = pvs.CreateView('RenderView')
  pvs.AssignViewToLayout(view=view, layout=layout)

  return view, layout

