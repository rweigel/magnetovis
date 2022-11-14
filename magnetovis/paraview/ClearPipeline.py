def ClearPipeline():

  import paraview.simple as pvs
  import magnetovis as mvs

  # Note that this does not clear all memory. It is useful
  # for a quick clearing of the pipeline, but when used in
  # a loop, memory usage will continously grow.
  # TODO: Consider adding keyword of "hard", which does
  # Disconnect(); Connect();

  # GetSources() Gets Sources and Filters. ParaView sometimes
  # uses "Sources" to mean "Proxies in Pipeline Viewer".

  s = None
  sources = pvs.GetSources().values()
  mvs.logger.info(f"Pipeline elements: {sources}")
  for s in sources:
    view = pvs.GetActiveView()
    if view is not None:
      pvs.Delete(pvs.GetRepresentation(s))
    pvs.Delete(s)
  del s 
  del sources

  l = None
  layouts = pvs.GetLayouts()
  mvs.logger.info(f"Layouts: {layouts}")
  for l in layouts.keys():
    layoutName = pvs.GetLayoutByName(l[0])
    pvs.RemoveLayout(layoutName)
  del l
  del layouts

  v = None
  views = pvs.GetViews()
  mvs.logger.info(f"Views: {views}")
  for v in views:
    pvs.Delete(v)
  del v
  del views

  # I see "del" of variables used as part of the Delete() process
  # suggested on ParaView lists and Python Trace output.
  # May possibly influence garbage collection.

  if True:
    renderView1 = pvs.CreateView('RenderView')
    layout1 = pvs.GetLayoutByName("Layout #1")
    if layout1:
      layout1.Reset() # If Layout #1 was previously split, it will still be split. This reset to no split.
    pvs.AssignViewToLayout(view=renderView1, layout=layout1, hint=0)