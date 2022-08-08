def ClearPipeline():

  import paraview.simple as pvs
  import magnetovis as mvs

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

  v = None
  views = pvs.GetRenderViews()
  mvs.logger.info(f"Render Views: {views}")
  for v in views:
    pvs.Delete(v)

  # I see this suggested on ParaView lists.
  # May possibly influence garbage collection.
  del s 
  del sources
  del v
  del views

  #mvs.CreateViewAndLayout()