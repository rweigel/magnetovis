def Script(time="2001-01-01", coord_sys="GSM", coord_sys_view=None,
            Resolution=90,
            Radius=1.0,
            Center=[0.0, 0.0, 0.0],
            Direction=[0.0, 0.0, 1.0],     
            point_array_functions=["xyz: position()"]):

  import magnetovis as mvs

  mvs.logger.info("Circle: Called.")

  kwargs = {
    "time": time,
    "coord_sys": coord_sys,
    "coord_sys_view": coord_sys_view,
    "Resolution": Resolution,
    "Closed": True,
    "point_function": f"circle(radius={Radius}, center={Center})",
    "point_array_functions": point_array_functions,
  }

  # TODO: Use vtkRegularPolygon
  mvs._Curve(**kwargs, _output=output)
  mvs._RotateUsingVectors(Vector2=Direction, _output=output)


def DefaultRegistrationName(**kwargs):

    import magnetovis as mvs

    Radius = mvs.util.trim_nums(kwargs['Radius'], 2, style='string')
    Center = mvs.util.trim_nums(kwargs['Center'], 2, style='string')
    Direction = mvs.util.trim_nums(kwargs['Direction'], 2, style='string')

    return f"Circle/Radius={Radius}/Center={Center}/Direction={Direction}"

