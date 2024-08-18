def nez(time, pos, csys):
  """Unit vectors in geographic north, east, and zenith dirs"""

  from hxform import hxform as hx

  # Geographic z axis in csys
  Z = hx.transform(np.array([0, 0, 1]), time, 'GEO', csys, lib='cxform')

  # zenith direction ("up")
  z_geo = pos/np.linalg.norm(pos)

  e_geo = np.cross(Z, z_geo)
  e_geo = e_geo/np.linalg.norm(e_geo)

  n_geo = np.cross(z_geo, e_geo)
  n_geo = n_geo/np.linalg.norm(n_geo)

  print(f"Unit vectors for Geographic N, E, and Z in {csys} at {time}:")
  print("North: {}".format(n_geo))
  print("East:  {}".format(e_geo))
  print("Z:     {}".format(z_geo))

  return n_geo, e_geo, z_geo

import numpy as np
time = "2000-01-01T12:00:00"
pos = (1, 0, 0)
csys = "GSM"
from hxform import hxform as hx
pos = (1., 0, 0)
nez(time, pos, csys)
