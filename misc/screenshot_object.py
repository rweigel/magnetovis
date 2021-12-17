def screenshot_object(
                obj=None,
                renderView=None,
                camera=None,
                fileName=None,
                ImageResolution=[1800, 1220],
                UseGradientBackground=1,
                Background = [0.086, 0.36, 0.49],
                Background2 = [0.070, 0.071, 0.47],
                pAxes=False):
    """Take a screenshot of a single object."""


    """See misc/screenshots.py for links and a discussion on options for creating screenshots""" 

    import os
    import paraview.simple as pvs 

    Azimuth = 30
    Elevation = 30

    if not renderView:
        renderView = pvs.GetActiveViewOrCreate('RenderView')
    
    if not fileName:
        base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)))
        if not os.path.isdir(os.path.join(base_path, 'figures')):
            os.mkdir(os.path.join(base_path,'figures'))
        for name_id, pObject in pvs.GetSources().items():
            if pObject.__eq__(obj):
                fileName = name_id[0]
        fileName_full = os.path.join(base_path, 'figures', fileName + '.png')
        fileName_full = fileName_full.replace(' - ', '-').replace(' ', '_').replace(':', '')
    else:
        fileName_full = fileName

    # tempObjDisplay.SetScalarBarVisibility(tempRenderView, True)
    if not pAxes:
        renderView.OrientationAxesVisibility = 0

    if obj:
        # with this we don't need to  pass around objectDisplay variable        
        objDisplay = pvs.GetRepresentation(proxy=obj, view=renderView) 
        tempLayout = pvs.CreateLayout('Temp Layout')
        tempRenderView = pvs.CreateRenderView()
        pvs.AssignViewToLayout(view=tempRenderView, layout=tempLayout, hint=0)
        pvs.SetActiveView(tempRenderView)
        pvs.SetActiveSource(obj)
    
        # show data in view
        tempObjDisplay = pvs.Show(obj, tempRenderView)
        for prop in objDisplay.ListProperties():
            # print('\n')
            # print(property)
            # print(display.GetPropertyValue(property))
            # RepresentationTypesInfo gives a Runtime Error message. this is a list of strings
            # BlockColor and Block Opacity both give attribute error. they are blank {}
            # ColorArrayName produces TypeError: SetElement argument 2: string or None required. this gives [None, ''] might have to use color transfer function
            # OpacityArray produces TypeError: SetElement argument 2: string or None required. this gives ['POINTS', 'Normals']
            # SetScaleArray producecs TypeError: SetElement argument 2: string or None required. this gives ['POINTS', 'Normals']
    
            try:
                if prop == 'ColorArrayName': # or prop=='SetScaleArray' or prop=='OpacityArray'
                    tempObjDisplay.ColorArrayName = [objDisplay.ColorArrayName[0], str(objDisplay.ColorArrayName[1])] # objDisplay.GetPropertyValue(prop)[1]
                    # print('\nthis is inside the try colorArrayName: ', tempObjDisplay.ColorArrayName)
                    # tempObjDisplay.ColorArrayName[0] = objDisplay.ColorArrayName[0]
                    # print('\n\nStill inside but now trying to get points',tempObjDisplay.ColorArrayName,'\n\n')
                    # pvs.ColorBy(tempObjDisplay, tempObjDisplay.ColorArrayName)
                elif prop == 'OpacityArray':
                    tempObjDisplay.OpacityArray = objDisplay.GetPropertyValue(prop)[1]
                elif prop == 'SetScaleArray':
                    tempObjDisplay.SetScaleArray = objDisplay.GetPropertyValue(prop)[1]
                elif prop == 'BlockOpacity' or prop == 'BlockColor':
                    # print('{} Does not currently have a value'.format(prop))
                    if len(objDisplay.BlockOpacity) == 0:
                        pass 
                    if len(objDisplay.BlockColor) == 0:
                        pass
                elif prop == 'RepresentationTypesInfo':
                    pass 
                else:
                    tempObjDisplay.SetPropertyWithName(prop, objDisplay.GetPropertyValue(prop))
            except RuntimeError as err:
                print(prop)
                print('RunTimeError: {}'.format(err))
                print('Issue Copying: {}'.format(prop))
            except TypeError as err:
                print('TypeError: {}'.format(err))
                print('Issue Copying: {}'.format(prop))
            except AttributeError as err:
                print('AttributeError: {}'.format(err))
                print('Issue Copying: {}'.format(prop))

        tempRenderView.UseGradientBackground = UseGradientBackground
        tempRenderView.Background = Background
        tempRenderView.Background2 = Background2

        # Check to see if there is a need for a legend. Conclude legend is not
        # needed if the min value in the color array is the same as the max.
        color_array_name = tempObjDisplay.ColorArrayName
        if color_array_name[1] != '':
    
            smin, smax = obj.GetPointDataInformation()[color_array_name[1]].GetRange()
            if smin != smax:
                tempObjDisplay.SetScalarBarVisibility(tempRenderView, True)
                
        if not camera:
            tempRenderView.ResetCamera()
            tempCamera = pvs.GetActiveCamera()
            tempCamera.Azimuth(Azimuth)      # Horizontal rotation
            tempCamera.Elevation(Elevation)    # Vertical rotation
        
        tempRenderView.OrientationAxesVisibility = 0
        pvs.SaveScreenshot(fileName_full, tempRenderView, ImageResolution=ImageResolution)
    
        # Delete temporaries
        del tempObjDisplay
        del objDisplay
        pvs.Delete(tempRenderView)
        del tempRenderView
        pvs.RemoveLayout(tempLayout)
        del tempLayout

        pvs.SetActiveView(renderView)
        pvs.Show(proxy=obj, view=renderView)
        
    else: 
        assert fileName != None, 'fileName cannot be None when full_view is True'

        if not camera:
            renderView.ResetCamera()
            camera = pvs.GetActiveCamera()
            camera.Azimuth(Azimuth)      # Horizontal rotation
            camera.Elevation(Elevation)    # Vertical rotation
        
        pvs.SaveScreenshot(fileName_full, renderView, ImageResolution=ImageResolution)

    print("Wrote " + fileName_full)
