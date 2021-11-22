def OutputDataSetType():

   # What is set in the drop-down menu for Output Data Set Type for a Programmable Source
   return "vtkPolyData"


def Script(time="2001-01-01", coord_sys='GSM', extent=[-40., 40.], direction='X',
            tube=True,
            tubeAndCone=True,
            vtkTubeFilterSettings=None,
            vtkConeSourceSettings=None):

    import vtk
    import numpy as np
    import magnetovis as mvs

    from hxform import hxform as hx

    import paraview.simple as pvs

    assert isinstance(extent, list or tuple or np.ndarray), \
        'magnetovis.Axis(): Extent must be a list, tuple, or numpy.ndarray'

    extent = np.array(extent)

    assert extent[0] < extent[1], \
        'magnetovis.Axis(): Lower extent {} is larger than upper extent {}' \
            .format(extent[0], extent[1])

    if direction == 'X':
        points = np.array([[extent[0], 0.0, 0.0],[extent[1], 0.0, 0.0]])
    if direction == 'Y':
        points = np.array([[0.0, extent[0], 0.0],[0.0, extent[1], 0.0]])
    if direction == 'Z':
        points = np.array([[0.0, 0.0, extent[0]],[0.0, 0.0, extent[1]]])

    if coord_sys != 'GSM':
        assert time != None, 'magnetovis.Axis(): If coord_sys in not GSM, time cannot be None'
        points = hx.transform(points, time, 'GSM', coord_sys, 'car', 'car')

    vtkLineSource = vtk.vtkLineSource()
    vtkLineSource.SetPoint1(*points[0])
    vtkLineSource.SetPoint2(*points[1])
    vtkLineSource.SetResolution(1)
    vtkLineSource.Update()

    if tube == False:
        output = output.ShallowCopy(vtkLineSource.GetOutputDataObject(0))
        mvs.ProxyInfo.SetInfo(pvs.GetActiveSource(), locals())
    else:
        numberOfSides = 20

        """Tube"""
        tubeRadius = 0.5

        vtkTubeFilter = vtk.vtkTubeFilter()

        # Set defaults
        vtkTubeFilter.SetNumberOfSides(numberOfSides)
        vtkTubeFilter.SetRadius(tubeRadius)

        # Apply input settings
        mvs.vtk.set_settings(vtkTubeFilter, vtkTubeFilterSettings)

        vtkTubeFilter.SetInputData(vtkLineSource.GetOutput())
        vtkTubeFilter.Update()

        if tube == True and tubeAndCone == False:
            output.ShallowCopy(vtkTubeFilter.GetOutputDataObject(0))
            mvs.ProxyInfo.SetInfo(pvs.GetActiveSource(), locals())
            return

        """Cone"""

        vtkConeSource = vtk.vtkConeSource()

        # Set defaults
        coneRadius = 2.0*vtkTubeFilter.GetRadius()
        coneHeight = coneRadius
        vtkConeSource.SetResolution(numberOfSides-1)
        vtkConeSource.SetAngle(45)
        vtkConeSource.SetDirection(*points[1])
        vtkConeSource.SetRadius(coneRadius)
        vtkConeSource.SetHeight(coneHeight)

        # TODO: Use vtkTranform to do the following translation.
        # TODO: Rotate the cone so base points align with tube end points.
        import math

        # Position of end of tube
        r = math.sqrt(points[1][0]**2 + points[1][1]**2 + points[1][2]**2)

        # Translate center by coneHeight/2 along tube
        coneCenter = []
        for i in range(3):
            coneCenter.append(points[1][i] + (coneHeight/2.0)*points[1][i]/r)
        vtkConeSource.SetCenter(coneCenter)

        # Apply input settings
        mvs.vtk.set_settings(vtkConeSource, vtkConeSourceSettings)
        vtkConeSource.Update()

        """Combine tube and cone into single PolyData object"""
        combinedSources = vtk.vtkAppendPolyData()
        combinedSources.AddInputData(vtkTubeFilter.GetOutput())
        combinedSources.AddInputData(vtkConeSource.GetOutput())
        combinedSources.Update()

        output.ShallowCopy(combinedSources.GetOutputDataObject(0))
        mvs.ProxyInfo.SetInfo(pvs.GetActiveSource(), locals())


def SetDisplayProperties(programmableSource, renderView=None, displayProperties=None,
                        **displayArguments):

    # Base this on code that is displayed by trace in ParaView GUI

    import paraview
    import paraview.simple as pvs
    import magnetovis

    renderView.ResetCamera()

    info = magnetovis.ProxyInfo.GetInfo(programmableSource)
    print(info)
    info = magnetovis.ProxyInfo.GetInfo(programmableSource, origin='server')
    print(info)

    direction = programmableSource.GetProperty('direction')
    extent = info['extent']
    if info['tubeAndCone']:
        # TODO: Use justification instead of 1.2 factor.
        extent[1] = extent[1] + 1.2*info['vtkConeSourceSettings']['Height']

    labelObject = pvs.Text()
    labelObject.Text = direction
    if 'label' in displayArguments:
        if 'Text' in displayArguments['label']:
            labelObject.Text = displayArguments['label']['Text']

    labelDisplayProperties = pvs.Show(labelObject, renderView, 'TextSourceRepresentation')

    labelDisplayProperties.TextPropMode = 'Billboard 3D Text'
    labelDisplayProperties.FontSize = 14

    displayProperties.AmbientColor = [0.5, 0.5, 0.5]
    displayProperties.DiffuseColor = [0.5, 0.5, 0.5]
    if direction == "X":
        labelDisplayProperties.BillboardPosition = [extent[1], 0, 0]
        displayProperties.AmbientColor = [1.0, 0.0, 0.0]
        displayProperties.DiffuseColor = [1.0, 0.0, 0.0]
    if direction == "Y":
        labelDisplayProperties.BillboardPosition = [0, extent[1], 0]
        displayProperties.AmbientColor = [1.0, 1.0, 0.0]
        displayProperties.DiffuseColor = [1.0, 1.0, 0.0]
    if direction == "Z":
        labelDisplayProperties.BillboardPosition = [0, 0, extent[1]]
        displayProperties.AmbientColor = [0.0, 1.0, 0.0]
        displayProperties.DiffuseColor = [0.0, 1.0, 0.0]


    # Override defaults
    if 'label' in displayArguments:
        for key, value in displayArguments['label'].items():
            if hasattr(labelDisplayProperties, key):            
                setattr(labelDisplayProperties, key, value)
            else:
                pass # TODO: Warn

    if 'object' in displayArguments:
        for key, value in displayArguments['object'].items():
            if hasattr(displayProperties, key):            
                setattr(displayProperties, key, value)
            else:
                pass # TODO: Warn

    return displayProperties
