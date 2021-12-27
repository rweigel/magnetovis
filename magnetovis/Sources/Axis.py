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
        output.ShallowCopy(vtkLineSource.GetOutputDataObject(0))
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

        # TODO?: Use vtkTranform to do the following translation.
        import math

        # Position of end of tube
        r = math.sqrt(points[1][0]**2 + points[1][1]**2 + points[1][2]**2)

        # Translate center by coneHeight/2 along tube
        coneCenter = []
        for i in range(3):
            coneCenter.append(points[1][i] + (coneHeight/2.0)*points[1][i]/r)
        vtkConeSource.SetCenter(coneCenter)
        vtkConeSource.Update()

        # Apply input settings
        mvs.vtk.set_settings(vtkConeSource, vtkConeSourceSettings)

        """Combine tube and cone into single PolyData object"""
        combinedSources = vtk.vtkAppendPolyData()
        combinedSources.AddInputData(vtkTubeFilter.GetOutput())
        combinedSources.AddInputData(vtkConeSource.GetOutput())
        combinedSources.Update()

        output.ShallowCopy(combinedSources.GetOutputDataObject(0))
        mvs.ProxyInfo.SetInfo(pvs.GetActiveSource(), locals())


def DefaultRegistrationName(**kwargs):
    import magnetovis as mvs

    registrationName = "{}-Axis/{}/{}" \
                        .format(kwargs['direction'], mvs.util.trim_iso(kwargs['time']), kwargs['coord_sys'])

    return registrationName


def GetDisplayDefaults(all=False):

    defaults = {
        'display': {
            'Representation': 'Surface',
            'AmbientColor': [0.5, 0.5, 0.5],
            'DiffuseColor': [0.5, 0.5, 0.5]
        },
        'label': {
            "display": {
                'FontSize': 24
            }
        } 
    }

    return defaults


def SetDisplayProperties(source, view=None, display=None, **kwargs):

    # Base this on code that is displayed by trace in ParaView GUI

    import logging
    import paraview.simple as pvs
    import magnetovis

    info = magnetovis.ProxyInfo.GetInfo(source)
    magnetovis.logger.info("Source info: {}".format(info))

    direction = source.GetProperty('direction')

    extent = info['extent']
    if info['tubeAndCone']:
        # TODO: Use justification instead of 1.2 factor.
        extent[1] = extent[1] + 1.1*info['vtkConeSourceSettings']['Height']

    # Default keyword arguments
    dkwargs = GetDisplayDefaults()

    '''Display'''

    # Other defaults
    if direction == "X":
        display.AmbientColor = [1.0, 0.0, 0.0]
        display.DiffuseColor = [1.0, 0.0, 0.0]
    if direction == "Y":
        display.AmbientColor = [1.0, 1.0, 0.0]
        display.DiffuseColor = [1.0, 1.0, 0.0]
    if direction == "Z":
        display.AmbientColor = [0.0, 1.0, 0.0]
        display.DiffuseColor = [0.0, 1.0, 0.0]

    '''Text'''

    # Text Source
    textSourceSettings = {}
    # Defaults
    if 'label' in dkwargs and 'source' in dkwargs['label']:
        textSourceSettings = dkwargs['label']['source']
    # Other defaults
    textSourceSettings['Text'] = direction
    textSourceSettings['registrationName'] = "   Label for " + info['registrationName']
    # Update defaults 
    if 'label' in kwargs and 'source' in kwargs['label']:
        textSourceSettings = {**textSourceSettings, **kwargs['label']['source']}
    # Create source
    textSource = pvs.Text(**textSourceSettings)

    # Text Source Display Representation
    textDisplaySettings = {}
    # Defaults
    if 'label' in dkwargs and 'display' in dkwargs['label']:
        textDisplaySettings = dkwargs['label']['display']
    # Other defaults
    if direction == "X":
        textDisplaySettings['BillboardPosition'] = [extent[1], 0, 0]
    if direction == "Y":
        textDisplaySettings['BillboardPosition'] = [0, extent[1], 0]
    if direction == "Z":
        textDisplaySettings['BillboardPosition'] = [0, 0, extent[1]]
    # Update defaults 
    if 'label' in kwargs and 'display' in kwargs['label']:
        textDisplaySettings = {**textDisplaySettings, **kwargs['label']['display']}
    
    textRepresentation = pvs.Show(proxy=textSource,
                                    view=view,
                                    TextPropMode='Billboard 3D Text',
                                    **textDisplaySettings)


    return [textSource]
