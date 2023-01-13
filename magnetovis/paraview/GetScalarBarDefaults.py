def GetScalarBarDefaults(color_by=None, colorTF=None):

  Title = ''
  ComponentTitle = ''
  if color_by is not None:
    Title = color_by[1]
    if len(color_by) == 3:
      ComponentTitle = ''
      component = color_by[2].lower()
      Title = f"{Title}$_{component}$"

  defaults = {
                'Title': Title,
                'ComponentTitle': ComponentTitle,
                'HorizontalTitle': 1,
                'TitleJustification': 'Centered',
                'Visibility': 1,
                'ScalarBarLength': 0.8,
            }

  categorical = False
  if colorTF is not None:
    categorical = colorTF.GetProperty('InterpretValuesAsCategories')

  if categorical is True:
    defaults['TextPosition'] = 'Ticks left/bottom, annotations right/top'
  else:
    defaults['TextPosition'] = 'Ticks right/top, annotations left/bottom'
    #defaults['AutomaticLabelFormat'] = 0
    #defaults['LabelFormat'] = '%.f'
    #defaults['AddRangeLabels'] = 0

  return defaults
