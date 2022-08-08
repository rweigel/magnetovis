def Script(Vector1=[0.0, 0.0, 1.0], Vector2=[0.0, 0.0, 1.0], _output=None):

  import magnetovis as mvs

  mvs.logger.info("Orient: Called.")

  if _output is not None:
    output = _output
    inputs = [_output]

  if Vector1 == Vector2:
    mvs.logger.info("Orient: Vector1 == Vector2. No rotation needed.")
    return

  import numpy as np
  n1 = np.array(Vector1)
  n2 = np.array(Vector2)
  r1 = np.linalg.norm(n1)
  r2 = np.linalg.norm(n2)
  n1 = n1/r1
  n2 = n2/r2

  angle = (180./np.pi)*np.arccos(np.dot(n1, n2))
  axis = np.cross(n1, n2)
  mvs.logger.info(f"Orient: Vector1 = {Vector1}; Vector2 = {Vector2}=> Rotation by angle = {angle}° around axis = {axis}")
  mvs._Rotate(angle=angle, axis=axis, _output=output)

  if _output is None:
    mvs.ProxyInfo.SetInfo(output, locals())

def DefaultRegistrationName(**kwargs):

  import magnetovis as mvs

  v1 = mvs.util.trim_nums(kwargs['Vector1'], 3, style='string')
  v2 = mvs.util.trim_nums(kwargs['Vector2'], 3, style='string')

  return "{}/Vector1={}/Vector2={}".format("RotateUsingVectors", v1, v2)
