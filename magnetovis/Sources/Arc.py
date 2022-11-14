def Script(time="2001-01-01", coord_sys="GSM", coord_sys_view=None,
            Resolution=90,
            Radius=1.0,
            Center=[0.0, 0.0, 0.0],
            Direction=[0.0, 0.0, 1.0],
            StartPhi=0.0,
            EndPhi=90.0,            
            point_array_functions=["xyz: position()"]):

  import magnetovis as mvs

  mvs.logger.info("Arc: Called.")

  kwargs = {
    "Resolution": Resolution,
    "Closed": False,
    "time": time,
    "coord_sys": coord_sys,
    "coord_sys_view": coord_sys_view,
    "point_function": f"arc(radius={Radius}, center={Center}, start_phi={StartPhi}, end_phi={EndPhi})",
    "point_array_functions": point_array_functions,
    "_output": output
  }

  # TODO: Use vtkArcSource?
  mvs._Curve(**kwargs)
  mvs._RotateUsingVectors(Vector2=Direction, _output=output)


def DefaultRegistrationName(**kwargs):

    import magnetovis as mvs
    Radius = mvs.util.trim_nums(kwargs['Radius'], 2, style='string')
    Center = mvs.util.trim_nums(kwargs['Center'], 2, style='string')
    Direction = mvs.util.trim_nums(kwargs['Direction'], 2, style='string')
    StartPhi = mvs.util.trim_nums(kwargs['StartPhi'], 2, style='string')
    EndPhi = mvs.util.trim_nums(kwargs['EndPhi'], 2, style='string')

    return f"Arc/Radius={Radius}/Center={Center}/StartPhi={StartPhi}/EndPhi={EndPhi}/Direction={Direction}"

