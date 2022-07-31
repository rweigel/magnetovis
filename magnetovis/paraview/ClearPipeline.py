def ClearPipeline():

  import paraview.simple as pvs

  # TODO: Consider adding keyword of "hard", which does
  # Disconnect(); Connect();

  # GetSources() Gets Sources and Filters. ParaView sometimes
  # uses "Sources" to mean "Proxies in Pipeline Viewer".
  for s in pvs.GetSources().values():
    pvs.Delete(s)
    pvs.Delete(pvs.GetRepresentation(s)) # So that previously set colorbars are removed.

  # I see this suggested on ParaView lists. May possibly influence garbage collection.
  del s 
