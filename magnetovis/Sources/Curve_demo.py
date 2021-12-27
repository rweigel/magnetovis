# From this directory, execute
#   magnetovis --script=Curve_demo.py

import magnetovis as mvs

kwargs = {
            "time": "2001-01-01",
            "coord_sys": "GSM",
            "Npts": 5,
            "closed": True,
            "point_function": "circle(radius=1.0, origin=(0.0, 0.0, 0.0), orientation=(0, 0, 1))"
        }

mvs.Curve(**kwargs)
