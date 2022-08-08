# Execute using
#   magnetovis Curve_demo.py

# Demo 1
import magnetovis as mvs
mvs.Curve()
#mvs.PrintSourceDefaults('Curve')
mvs.SetTitle("Curve with default options")
#mvs.PrintPresentationDefaults('Curve', all=True)

# Demo 2
import magnetovis as mvs
mvs.CreateViewAndLayout()

skwargs = {
            "time": "2001-01-01",
            "coord_sys": "GSM",
            "Resolution": 5,
            "Closed": True,
            "point_function": "circle(radius=1.0, center=(0.0, 0.0, 0.0))"
        }

dkwargs = {
        "display": {
            "Representation": "Surface",
            "Opacity": 1.0,
            "AmbientColor": [1, 1, 0],
            "DiffuseColor": [1, 1, 0],
            "Visibility": 1
        },
        'coloring': {
            'colorBy': None
        }
}

curve = mvs.Curve(**skwargs)
mvs.SetPresentationProperties(source=curve, **dkwargs)
mvs.SetTitle("Curve using alt kwargs for point fn")

# Demo 3
import magnetovis as mvs
mvs.CreateViewAndLayout()

skwargs['Closed'] = False
skwargs['Resolution'] = 100
skwargs['point_function'] = "helix(radius=1.0, length=10, rounds=5)"

curve = mvs.Curve(**skwargs)
mvs.SetPresentationProperties(source=curve, **dkwargs)
mvs.SetTitle("Curve using alt point fn")


# Demo 4
import magnetovis as mvs
mvs.CreateViewAndLayout()

def _randpts(Npts):

	import numpy as np
	return  -0.5 + np.random.random_sample([Npts,3])

from magnetovis import functions as mvsfunctions
mvsfunctions._randpts = _randpts

skwargs = {
            "time": "2001-01-01",
            "coord_sys": "GSM",
            "Resolution": 100,
            "Closed": False,
            "point_function": "_randpts()"
        }

dkwargs = {
        "display": {
            "Representation": "Surface",
            "Opacity": 1.0,
            "AmbientColor": [1, 1, 0],
            "DiffuseColor": [1, 1, 0],
            "Visibility": 1
        },
        'tube': None,
        'coloring': {
            'colorBy': None
        }
}

curve = mvs.Curve(**skwargs)
mvs.SetPresentationProperties(source=curve, **dkwargs)
mvs.SetTitle("Points from user-defined function; no tube.")

# Demo #5
import magnetovis as mvs
mvs.CreateViewAndLayout()

def _parabola(Npts):

  import numpy as np
  xyz = np.zeros([Npts,3])

  xyz[:,1] = 40*np.linspace(-1,1,Npts)
  xyz[:,2] = xyz[:,1]**2/40

  return xyz 

from magnetovis import functions as mvsfunctions
mvsfunctions._parabola = _parabola

skwargs = {
            "time": "2001-01-01",
            "coord_sys": "GSM",
            "Resolution": 100,
            "Closed": False,
            "point_function": "_parabola()"
        }

dkwargs = {
        "display": {
            "Representation": "Surface",
            "Opacity": 1.0,
            "AmbientColor": [1, 1, 0],
            "DiffuseColor": [1, 1, 0],
            "Visibility": 1
        },
        'tube': {
            'source': {
                'Radius': 1.0
            }
        },
        'coloring': {
            'colorBy': ('POINTS', 'xyz', 'Z')
        }
}

mvs.Axis(direction="X")
mvs.Axis(direction="Y")
mvs.Axis(direction="Z")
curve = mvs.Curve(**skwargs)
mvs.SetPresentationProperties(source=curve, **dkwargs)
mvs.SetTitle("Parabola in Y-Z plane colored by Z")

# Color bar that appears by default has a minimum of 4.1e-3
# even though min of xyz >= 0. Not sure why this is. The max
# value is correct, however. The following resets
#import paraview.simple as pvs
import paraview.simple as pvs
curve1 = pvs.GetActiveSource()
renderView1 = pvs.GetActiveViewOrCreate('RenderView')
curve1Display = pvs.GetDisplayProperties(curve1, view=renderView1)
LUT = pvs.GetColorTransferFunction('xyz', curve1Display, separate=True)
LUT.RescaleTransferFunction(0.0, 40.0)
