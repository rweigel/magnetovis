def OutputDataSetType():

  # What is set in the drop-down menu for Output Data Set Type for a Programmable Source
  return "vtkPolyData"

def GetSourceDefaults(defaults, kwargs):
    """Update default kwargs for Script based on other kwargs"""

    import magnetovis as mvs

    for key in defaults:
        if not key.startswith('vtk'):
            if key in kwargs:
                defaults[key] = kwargs[key]

    Radius = 0.01*(abs(defaults['extent'][1] - defaults['extent'][0]))
    defaults = mvs.vtk.update_if_needed(defaults, kwargs, 'vtkTubeFilter', key='Radius', val=Radius)

    defaults_dict = mvs.vtk.list2dict(defaults['vtkTubeFilter'], mvs.vtk.get_settings('vtkTubeFilter', form='dict'))

    Radius = 2.0*defaults_dict['Radius']
    defaults = mvs.vtk.update_if_needed(defaults, kwargs, 'vtkConeSource', key='Radius', val=Radius)
    defaults = mvs.vtk.update_if_needed(defaults, kwargs, 'vtkConeSource', key='Height', val=Radius)

    NumberOfSides = defaults_dict['NumberOfSides'] - 1    
    defaults = mvs.vtk.update_if_needed(defaults, kwargs, 'vtkConeSource', key='Resolution', val=NumberOfSides)

    return defaults


def Script(time="2001-01-01",
            coord_sys='GSM',
            extent=[-40., 40.],
            direction='X',
            tube=True,
            tubeAndCone=True,
            vtkTubeFilter=["Capping: 1", "NumberOfSides: 10"],
            vtkConeSource=["Capping: 1", "Angle: 45"]):

    import vtk
    import numpy as np
    import magnetovis as mvs

    mvs.logger.info("Called.")

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
      from hxform import hxform as hx
      assert time != None, 'magnetovis.Axis(): If coord_sys in not GSM, time cannot be None'
      points = hx.transform(points, time, 'GSM', coord_sys, 'car', 'car')

    vtkLineSource = vtk.vtkLineSource()
    vtkLineSource.SetPoint1(*points[0])
    vtkLineSource.SetPoint2(*points[1])
    vtkLineSource.SetResolution(1)
    vtkLineSource.Update()

    if tube == False or tubeAndCone == False:
      output.ShallowCopy(vtkLineSource.GetOutputDataObject(0))
      import paraview.simple as pvs
      mvs.ProxyInfo.SetInfo(pvs.GetActiveSource(), locals())
    else:

      """Tube"""

      vtkTubeFilterProxy = vtk.vtkTubeFilter()
      mvs.vtk.set_settings(vtkTubeFilterProxy, vtkTubeFilter)
      vtkTubeFilterProxy.SetInputData(vtkLineSource.GetOutput())
      vtkTubeFilterProxy.Update()

      if tube == True and tubeAndCone == False:
          output.ShallowCopy(vtkTubeFilterProxy.GetOutputDataObject(0))
          import paraview.simple as pvs
          mvs.ProxyInfo.SetInfo(pvs.GetActiveSource(), locals())
          return

      """Cone"""

      vtkConeSourceProxy = vtk.vtkConeSource()

      # Apply input settings
      mvs.vtk.set_settings(vtkConeSourceProxy, vtkConeSource)

      vtkConeSourceProxy.SetDirection(*points[1])

      # TODO?: Use vtkTranform to do the following translation.
      import math

      # Position of end of tube
      r = math.sqrt(points[1][0]**2 + points[1][1]**2 + points[1][2]**2)

      # Translate center by coneHeight/2 along tube
      coneCenter = []
      for i in range(3):
          coneCenter.append(points[1][i] + (vtkConeSourceProxy.GetHeight()/2.0)*points[1][i]/r)
      vtkConeSourceProxy.SetCenter(coneCenter)

      vtkConeSourceProxy.Update()


      """Combine tube and cone into single PolyData object"""
      combinedSources = vtk.vtkAppendPolyData()
      combinedSources.AddInputData(vtkTubeFilterProxy.GetOutput())
      combinedSources.AddInputData(vtkConeSourceProxy.GetOutput())
      combinedSources.Update()

      output.ShallowCopy(combinedSources.GetOutputDataObject(0))

      mvs.ProxyInfo.SetInfo(output, locals())


def DefaultRegistrationName(**kwargs):
    import magnetovis as mvs

    registrationName = "{}-Axis/{}/{}" \
                        .format(kwargs['direction'], mvs.util.trim_iso(kwargs['time']), kwargs['coord_sys'])

    return registrationName


def GetDisplayDefaults():

    defaults = {
        'display': {
            'Representation': 'Surface',
            'AmbientColor': [0.5, 0.5, 0.5],
            'DiffuseColor': [0.5, 0.5, 0.5]
        },
        'label': {
            'source': {},
            "display": {
                'FontSize': 24
            }
        } 
    }

    return defaults


def SetDisplayProperties(source, view=None, **kwargs):

    import paraview.simple as pvs
    import magnetovis as mvs

    info = mvs.ProxyInfo.GetInfo(source)
    mvs.logger.info("Source info: {}".format(info))
    mvs.logger.info("kwargs: {}".format(kwargs))

    direction = source.GetProperty('direction')

    # Default keyword arguments
    dkwargs = GetDisplayDefaults()

    # Display defaults that depend on parent source
    if direction == "X":
        dkwargs['display']['AmbientColor'] = [1.0, 0.0, 0.0]
        dkwargs['display']['DiffuseColor'] = [1.0, 0.0, 0.0]
    if direction == "Y":
        dkwargs['display']['AmbientColor'] = [1.0, 1.0, 0.0]
        dkwargs['display']['DiffuseColor'] = [1.0, 1.0, 0.0]
    if direction == "Z":
        dkwargs['display']['AmbientColor'] = [0.0, 1.0, 0.0]
        dkwargs['display']['DiffuseColor'] = [0.0, 1.0, 0.0]

    sourceDisplay = dkwargs['display']

    # Update defaults 
    if 'display' in kwargs:
        sourceDisplay = {**dkwargs['display'], **kwargs['display']}

    pvs.Show(source, view, **sourceDisplay)

    # Source defaults
    labelSettings = dkwargs['label']['source']

    # Source defaults that depend on parent source
    labelSettings['Text'] = direction
    labelSettings['registrationName'] = "  Label for " + info['registrationName']

    if 'label' in kwargs:
      if kwargs['label'] is None:
         return
      if 'source' in kwargs['label']:
         # Update defaults 
         labelSettings = {**labelSettings, **kwargs['label']['source']}

    # Create source
    labelSource = pvs.Text(**labelSettings)

    # Text Source Display Representation
    labelDisplay = dkwargs['label']['display']

    extent = info['extent']
    if info['tubeAndCone']:
        # TODO: Use justification instead of scale factor.
        extent[1] = extent[1] + 1.1*info['vtkConeSource']['Height']

    # Display defaults that depend on parent source
    if direction == "X":
        labelDisplay['BillboardPosition'] = [extent[1], 0, 0]
    if direction == "Y":
        labelDisplay['BillboardPosition'] = [0, extent[1], 0]
    if direction == "Z":
        labelDisplay['BillboardPosition'] = [0, 0, extent[1]]

    if info['coord_sys'] != 'GSM':
      from hxform import hxform as hx
      labelDisplay['BillboardPosition'] = hx.transform(labelDisplay['BillboardPosition'], info['time'], 'GSM', info['coord_sys'], 'car', 'car')

    # Update defaults 
    if 'label' in kwargs and 'display' in kwargs['label']:
        labelDisplay = {**labelDisplay, **kwargs['label']['display']}
    
    pvs.Show(labelSource, view, TextPropMode='Billboard 3D Text', **labelDisplay)

    return [{'label': labelSource}]
