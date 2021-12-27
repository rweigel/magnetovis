def SetCamera(view=None, camera=None, source=None, viewType=None,
                Azimuth=45.0, Elevation=35.264, Roll=0.0):

    import paraview.simple as pvs

    import magnetovis as mvs
    mvs.logger.info("Called.")

    if view is None:
        view = pvs.GetActiveViewOrCreate('RenderView')

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

    if camera is None:
        camera = view.GetActiveCamera()

    view.CameraPosition = [(bounds[1]-bounds[0])*5, 0.5, 0.5]
    view.CameraFocalPoint = [0, 0, 0]
    view.CameraViewUp = [0, 0, 1]
    view.Update()

    # It seems that the following should work and it would 
    # make more sense to apply these settings to the camera
    # than to the view.
    # TODO: Figure out why.
    #camera.FocalPoint = [0, 0, 0]
    #camera.Position = [(bounds[1]-bounds[0])*5, 0.5, 0.5]
    #camera.ViewUp = [0, 0, 1]

    camera.Azimuth(Azimuth)
    camera.Elevation(Elevation)

    # Reset camera settings to include entire scene while
    # preserving orientation 
    view.ResetCamera()
    view.CenterOfRotation = [0, 0, 0]

    # Needed for pvbatch.
    view.StillRender()

    return camera
