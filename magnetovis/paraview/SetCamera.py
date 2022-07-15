def SetCamera(view=None, source=None, viewType=None,
                Azimuth=0.0, Elevation=0.0, Dolly=0.0, Roll=0.0, Yaw=0.0, Zoom=1.5):

    import paraview.simple as pvs

    import magnetovis as mvs
    mvs.logger.info("Called.")

    if view is None:
        view = pvs.GetActiveViewOrCreate('RenderView')

    camera = view.GetActiveCamera() 

    # Azimuth, Elevation, etc. are defined at
    # https://vtk.org/doc/nightly/html/classvtkCamera.html

    if viewType == "isometric":
        Azimuth = 45.0
        Elevation = 35.264
        Dolly = 0.0
        Roll = 0.0
        Yaw = 0.0
        Zoom = 1.5

    if viewType in ["+X", "-X", "+Y", "-Y", "+Z", "-Z"]:
        Azimuth = 0
        Elevation = 0
        Dolly = 0.0
        Roll = 0.0
        Yaw = 0.0
        Zoom = 1.5
        if viewType == "+X":
            Azimuth = 0
        if viewType == "-X":
            Azimuth = 180
        if viewType == "+Y":
            Azimuth = 90
        if viewType == "-Y":
            Azimuth = 270
        if viewType == "+Z":
            Elevation = 90
        if viewType == "-Z":
            Elevation = 270

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

    # Ideally we would use 
    #   import paraview.simple as pvs
    #   pvs.SetProperties(proxy=camera, **cameraSettings)
    # This does not work b/c camera does not have a ListProperties method
    # (it seems like it should). Relevant code is at       
    # https://github.com/Kitware/ParaView/blob/master/Wrapping/Python/paraview/servermanager.py#L438

    xb = bounds[1]-bounds[0]
    yb = bounds[3]-bounds[2]
    zb = bounds[5]-bounds[4]

    camera.SetFocalPoint([0, 0, 0])
    camera.SetPosition([max(xb,yb,zb)*5, 0.5, 0.5])
    camera.SetViewUp([0, 0, 1])

    camera.Azimuth(Azimuth)
    camera.Dolly(Dolly)
    camera.Elevation(Elevation)
    camera.Roll(Roll)
    camera.Yaw(Yaw)
    camera.Zoom(Zoom)

    # Reset camera settings to include entire scene while
    # preserving orientation 
    view.ResetCamera()

    # TODO: Only set if origin is in volume.
    view.CenterOfRotation = [0, 0, 0]

    # Apply camera settings
    view.StillRender()

    return camera
