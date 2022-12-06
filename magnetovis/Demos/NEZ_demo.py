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

  e_geo = np.cross(Z, z_geo)
  e_geo = e_geo/np.linalg.norm(e_geo)

  n_geo = np.cross(z_geo, e_geo)
  n_geo = n_geo/np.linalg.norm(n_geo)

  print(f"Unit vectors for Geographic N, E, and Z in {csys}:")
  print("North: ".format(n_geo))
  print("East:  ".format(e_geo))
  print("Z:     ".format(z_geo))

  return n_geo, e_geo, z_geo

def showaxis(pos, n_geo, e_geo, z_geo):

  def showlabel(dir,base,top):

    Label = pvs.Text(registrationName=dir+'_GEO Label', Text=dir+"$_{GEO}$")
    text1Display = pvs.Show(Label, pvs.GetActiveViewOrCreate('RenderView'), 'TextSourceRepresentation',
      TextPropMode='Flagpole Actor',BasePosition=base,TopPosition=top)

  north = pvs.Line(registrationName="N", Point1=pos, Point2=pos+n_geo)
  north_tube = pvs.Tube(north, Radius=0.02)
  mvs.SetColor('blue')
  pvs.Show(north_tube)
  showlabel('N',pos+n_geo,pos+1.05*n_geo)

  east = pvs.Line(registrationName="E", Point1=pos, Point2=pos+e_geo)
  east_tube = pvs.Tube(east, Radius=0.02)
  mvs.SetColor('green')
  pvs.Show(east_tube)
  showlabel('E',pos+e_geo,pos+e_geo+0.05*n_geo)

  up = pvs.Line(registrationName="Z", Point1=pos, Point2=pos+z_geo)
  up_tube = pvs.Tube(up, Radius=0.02)
  mvs.SetColor('red')
  pvs.Show(up_tube)
  showlabel('Z',pos+z_geo,pos+z_geo+0.05*n_geo)

  s = pvs.Sphere(Radius=0.05, Center=pos)
  pvs.Show(s)

# Demo 1
time = "2000-01-01T00:00:00"
pos = (1, 0, 0)
csys = "GEO"
n_geo, e_geo, z_geo = nez(time, pos, csys)

showaxis(pos, n_geo, e_geo, z_geo)
mvs.SetOrientationAxisLabel(Text="GEO")
mvs.Earth(coord_sys=csys)
mvs.LatLong(coord_sys=csys, coord_sys_view=csys)

# Demo 2
mvs.CreateViewAndLayout()

csys = "GSM"
time = "2000-01-01T00:00:00"
#pos = (1., 18.907, 72.815) # Geographic r, lat, long of Colaba
pos = (1., 60., 0.)
#pos = (1., 0, 0)
from hxform import hxform as hx
pos = hx.transform(np.array(pos), time, 'GEO', csys, ctype_in="sph", ctype_out="car", lib='cxform')
mvs.Earth(coord_sys=csys)
n_geo, e_geo, z_geo = nez(time, pos, csys)
showaxis(pos, n_geo, e_geo, z_geo)
mvs.SetOrientationAxisLabel(Text="GSM")
mvs.LatLong(coord_sys="GEO", coord_sys_view=csys)
