def SetCamera(renderView=None, viewType=None, source=None):

    import paraview.simple as pvs

    if renderView is None:
        renderView = pvs.GetActiveViewOrCreate('RenderView')

    if viewType is None:
        viewType == "isometric"

    if source is None:
        sources = pvs.GetSources()
        # TODO: Ignore sources that are not visible. See
        # https://discourse.paraview.org/t/obtain-information-if-proxy-is-visible/2346/11?u=rweigel
        bounds = None
        for key, source in sources.items():
            source_bounds = source.GetDataInformation().GetBounds()
            if bounds is None:
                bounds = list(source_bounds)
            bounds[0] = min(bounds[0], source_bounds[0])
            bounds[1] = max(bounds[1], source_bounds[1])
            bounds[2] = min(bounds[2], source_bounds[2])
            bounds[3] = max(bounds[3], source_bounds[3])
            bounds[4] = min(bounds[4], source_bounds[4])
            bounds[5] = max(bounds[5], source_bounds[5])
    else:
        bounds = source.GetDataInformation().GetBounds()


    if viewType == "isometric":
        renderView.CameraPosition = [(bounds[1]-bounds[0])*5, 0.5, 0.5]
        renderView.Update()
        renderView.CameraFocalPoint = [0, 0, 0]
        renderView.CameraViewUp = [0, 0, 1]
        camera = renderView.GetActiveCamera()
        camera.Azimuth(45)
        camera.Elevation(35.264)
        renderView.ResetCamera()


    return camera
