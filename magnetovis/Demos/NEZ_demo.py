# Demo 1
import paraview.simple as pvs
import magnetovis as mvs
import numpy as np

def nez(time, pos, csys):
  """Unit vectors in geographic north, east, and zenith dirs

    Given a cartesian position `pos` in `csys` at time `time`,
    returns the cartesian unit vectors for geographic north,
    east, and zenith in `csys`.

    Example:
      n_geo, e_geo, z_geo = nez("2010-01-01T00:00:00", (1, 0, 0), "GEO")
      print("North: {}".format(n_geo)) # North: [0. 0. 1.]
      print("East:  {}".format(e_geo)) # East:  [0. 1. 0.]
      print("Z:     {}".format(z_geo)) # Z:     [1. 0. 0.]
  """

  from hxform import hxform as hx

  # Geographic z axis in csys
  Z = hx.transform(np.array([0, 0, 1]), time, 'GEO', csys, lib='cxform')

  # zenith direction ("up")
  z_geo = pos/np.linalg.norm(pos)

  e_geo = np.cross(Z, z_geo)
  e_geo = e_geo/np.linalg.norm(e_geo)

  n_geo = np.cross(z_geo, e_geo)
  n_geo = n_geo/np.linalg.norm(n_geo)

  if False:
    print(f"Unit vectors for Geographic N, E, and Z at {pos} in {csys} at {time}:")
    print("North: {}".format(n_geo))
    print("East:  {}".format(e_geo))
    print("Z:     {}".format(z_geo))

  return n_geo, e_geo, z_geo

def showaxis(pos, n_geo, e_geo, z_geo, pos_label=""):

  def showlabel(dir,base,top):

    Label = pvs.Text(registrationName=dir+'_GEO Label', Text=dir+"$_{GEO}$")
    text1Display = pvs.Show(Label, pvs.GetActiveViewOrCreate('RenderView'), 'TextSourceRepresentation',
      TextPropMode='Flagpole Actor',BasePosition=base,TopPosition=top)

  north = pvs.Line(registrationName="  N_GEO Axis Line", Point1=pos, Point2=pos+n_geo)
  north_tube = pvs.Tube(north, registrationName="  N_GEO Axis Tube", Radius=0.02)
  mvs.SetColor('blue')
  pvs.Show(north_tube)
  showlabel('N', pos+n_geo, pos+1.05*n_geo)

  east = pvs.Line(registrationName="  E_GEO Axis Line", Point1=pos, Point2=pos+e_geo)
  east_tube = pvs.Tube(east, registrationName="  E_GEO Axis Tube", Radius=0.02)
  mvs.SetColor('green')
  pvs.Show(east_tube)
  showlabel('E', pos+e_geo, pos+e_geo+0.05*n_geo)

  up = pvs.Line(registrationName="  Z_GEO Axis Line", Point1=pos, Point2=pos+z_geo)
  up_tube = pvs.Tube(up, registrationName="  Z_GEO Axis Tube", Radius=0.02)
  mvs.SetColor('red')
  pvs.Show(up_tube)
  showlabel('Z', pos+z_geo, pos+z_geo+0.05*n_geo)

  s = pvs.Sphere(registrationName=pos_label, Radius=0.05, Center=pos)
  pvs.Show(s)

# Demo 1
time = "2010-01-01T00:00:00"
pos_GEO = (1, 0, 0)
csys = "GEO"
pos_GEO_label = f"$(r,\\lambda,\\phi)_{{GEO}}$={pos_GEO}"
from hxform import hxform as hx
pos = hx.transform(np.array(pos_GEO), time, 'GEO', csys, ctype_in="sph", ctype_out="car", lib='cxform')
n_geo, e_geo, z_geo = nez(time, pos_GEO, csys)

showaxis(pos_GEO, n_geo, e_geo, z_geo, pos_label=pos_GEO_label)
mvs.SetOrientationAxisLabel(Text="GEO")
mvs.Earth(time=time, coord_sys=csys)
mvs.SetTitle(f"{time} {pos_GEO_label}")
mvs.LatLong(coord_sys=csys, coord_sys_view=csys)

L = 10
skwargs = {
            "time": time,
            "coord_sys": "GEO",
            "coord_sys_view": "GEO",
            "Resolution": 20,
            "point_function": f"dipole_field_line(L={L})"
        }
curve = mvs.Curve(**skwargs)

import paraview
sourceData = paraview.servermanager.Fetch(curve)
points = sourceData.GetPointData().GetArray('xyz')
from vtk.util import numpy_support
points = numpy_support.vtk_to_numpy(points)

idx = np.argmax(points[:,2], axis=0)
print(idx)
lpos = points[idx,:]
print(lpos)
BasePosition=points[idx,:]
TopPosition=np.copy(points[idx,:])
TopPosition[2] = TopPosition[2] + 0.1

Label = pvs.Text(registrationName=f"L={L}", Text=f"L={L}")
text1Display = pvs.Show(Label, pvs.GetActiveViewOrCreate('RenderView'),
  'TextSourceRepresentation', TextPropMode='Flagpole Actor',
  BasePosition=BasePosition, TopPosition=TopPosition)

if False:
  # Demo 2
  mvs.CreateViewAndLayout()

  csys = "GSM"
  time = "2010-01-01T12:00:00"
  #pos = (1., 18.907, 72.815) # Geographic r, lat, long of Colaba
  #pos = (1., 60., 0.)
  pos_GEO = (1, 0, 0)
  mvs.SetTitle(f"{time} {pos_GEO_label}")

  from hxform import hxform as hx
  pos = hx.transform(np.array(pos_GEO), time, 'GEO', csys, ctype_in="sph", ctype_out="car", lib='cxform')
  n_geo, e_geo, z_geo = nez(time, pos, csys)

  mvs.Earth(time=time)
  mvs.SetTitle(f"{time} {pos_GEO_label}")
  showaxis(pos, n_geo, e_geo, z_geo, pos_label=pos_GEO_label)
  mvs.SetOrientationAxisLabel(Text="GSM")
  mvs.LatLong(time=time, coord_sys="GEO", coord_sys_view=csys)
