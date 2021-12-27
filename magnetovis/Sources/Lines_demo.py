# From this directory, execute
#   magnetovis --script=Lines_demo.py

import magnetovis as mvs

kwargs = {
            "time": "2001-01-01",
            "coord_sys": "GSM",
            "Nlines": 3,
            "closed": True,
            "point_function": "circle(radius=1.0, origin=(0.0, 0.0, 0.0), orientation=(0, 0, 1))"
        }

mvs.Lines(**kwargs)
