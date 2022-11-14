# Demo 1
import paraview.simple as pvs
import magnetovis as mvs
import numpy as np

def nez(time, pos, csys):
  """Unit vectors in geographic north, east, and zenith dirs"""

  from hxform import hxform as hx

  # Geographic z axis in csys
  Z = hx.transform(np.array([0, 0, 1]), time, 'GEO', csys, lib='cxform')

  # zenith direction ("up")
  z_geo = pos/np.linalg.norm(pos)

  e_geo = np.cross(z_geo, Z)
  e_geo = e_geo/np.linalg.norm(e_geo)

  n_geo = np.cross(e_geo, z_geo)
  n_geo = n_geo/np.linalg.norm(n_geo)

  return n_geo, e_geo, z_geo

time = '2001-09-02T04:10:00' 
pos = (1., 18.907, 72.815)   # Geographic r, lat, long of Colaba
from hxform import hxform as hx
pos = hx.transform(np.array(pos), time, 'GEO', 'GSM', ctype_in="sph", ctype_out="car", lib='cxform')
pos = (1/np.sqrt(2), 0, 1/np.sqrt(2))
#pos = (1, 0, 0)

n_geo, e_geo, z_geo = nez(time, pos, "GEO")

print("Unit vectors for Geographic N, E, and Z in GSM:")
print(n_geo)
print(e_geo)
print(z_geo)

up = pvs.Line(registrationName="Z", Point1=pos, Point2=pos+z_geo)
up_tube = pvs.Tube(up, Radius=0.02)
mvs.SetColor('red')
pvs.Show(up_tube)

east = pvs.Line(registrationName="E", Point1=pos, Point2=pos+e_geo)
east_tube = pvs.Tube(east, Radius=0.02)
mvs.SetColor('green')
pvs.Show(east_tube)

north = pvs.Line(registrationName="N", Point1=pos, Point2=pos+n_geo)
north_tube = pvs.Tube(north, Radius=0.02)
mvs.SetColor('blue')
pvs.Show(north_tube)

mvs.SetOrientationAxisLabel(Text="GEO")
mvs.Earth(coord_sys="GEO", coord_sys_view="GEO")
mvs.LatLong(coord_sys="GEO", coord_sys_view="GEO")
mvs.SetTitle()

# GSM
#mvs.Earth(time=time, coord_sys="GSM")
#mvs.LatLong(time=time, coord_sys="GEO", phis=list(np.arange(0, 175, 5)), thetas=list(np.arange(-75, 75, 5)))
#s = pvs.Sphere(Radius=0.1, Center=pos)
#pvs.Show(s)

