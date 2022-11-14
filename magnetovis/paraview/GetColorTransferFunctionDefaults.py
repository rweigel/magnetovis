def GetColorTransferFunctionDefaults(color_by=None, source=None, **kwargs):

  # TODO?: Allow passing transfer function name and then set RGB points
  #        using return of GetTransferFunctions() (using vtk as here for 
  #        case when number of colors <=0 or by creating a TF here,
  #        using ApplyDefaults, and the extracting RGB points). It would
  #        be easier to use ApplyPreset as noted in mvs.SetColoring().

  import magnetovis as mvs
  mvs.logger.info("Called.")

  defaults = {
    'NumberOfTableValues': 32
  }

  if color_by is None:
    return defaults

  import paraview
  import paraview.simple as pvs
  if source is None:
    source = pvs.GetActiveSource()

  # Can this fetch be avoided? Seems like one would need to add
  # information calculated based on output and place as field data
  sourceData = paraview.servermanager.Fetch(source)
  if color_by[0] == 'CELLS':
    vtkData = sourceData.GetCellData().GetArray(color_by[1])
  elif color_by[0] == 'POINTS':
    vtkData = sourceData.GetPointData().GetArray(color_by[1])
  else:
    raise ValueError('First element of color_by must be POINTS or CELLS')

  from vtk.util import numpy_support
  data = numpy_support.vtk_to_numpy(vtkData)

  import numpy as np
  if len(color_by) == 2:
    if len(data.shape) == 1:
      u = np.unique(data)
    else:
      u = np.unique(np.linalg.norm(data, axis=1))

  if len(color_by) == 3:
    if color_by[2] == 'X':
        u = np.unique(data[:,0])
    elif color_by[2] == 'Y':
        u = np.unique(data[:,1])
    elif color_by[2] == 'Z':
        u = np.unique(data[:,2])
    elif color_by[2] == 'Magnitude':
        u = np.unique(np.linalg.norm(data, axis=2))
    else:
      raise NotImplementedError("Only components 'X', 'Y', 'Z', and 'Magnitude' implemented for second element of color_by.")
  
  n_unique = len(u)
  mvs.logger.info(f'Number of unique values in {color_by} = {n_unique}')
  defaults['NumberOfTableValues'] = min(n_unique, 32)

  categorizeIfFewUnique = 1
  if 'InterpretValuesAsCategories' in kwargs:
    if kwargs['InterpretValuesAsCategories'] == 0:
      categorizeIfFewUnique = False

  ntv = defaults['NumberOfTableValues']
  if ntv <= 8 and categorizeIfFewUnique == 1:
    u = np.flip(u)

    import vtk
    ctf = vtk.vtkColorTransferFunction()
    ctf.SetColorSpaceToHSV()
    ctf.SetColorSpaceToDiverging()
    ctf.AddRGBPoint(ntv-1, 0.23137254902, 0.298039215686, 0.752941176471)
    ctf.AddRGBPoint((ntv-1)/2, 0.865, 0.865, 0.865)
    ctf.AddRGBPoint(0, 0.705882352941, 0.0156862745098, 0.149019607843)

    defaults['InterpretValuesAsCategories'] = 1
    IndexedColors = []
    Annotations = []
    for i in range(ntv):
        Annotations.append(str(u[i]))
        Annotations.append(str(u[i]))
        rgb = ctf.GetColor(i)
        IndexedColors.append(rgb[0])
        IndexedColors.append(rgb[1])
        IndexedColors.append(rgb[2])
    defaults['Annotations'] = Annotations
    defaults['IndexedColors'] = IndexedColors
    defaults['IndexedOpacities'] = ntv*[1.0]

  mvs.logger.info(f"Returning {defaults}")

  return defaults