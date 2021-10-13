# From this directory, execute
#   magnetovis --script=Plane_demo.py

import magnetovis as mvs

sourceArguments = {
                    "time": "2001-01-01",
                    "normal": "Z",
                    "extents": [[-40,40],[-40,40]],
                    "coord_sys": "GSM"
                }

displayArguments = {
                    "showSource": True,
                    "renderView": None
                }

Plane = mvs.Plane(
                    sourceName="XY Plane",
                    sourceArguments=sourceArguments,
                    renderSource=True,
                    displayArguments=displayArguments
                )

#print(Plane.programmableSource)
#print(Plane.displayProperties) # None b/c renderSource was False
#print(Plane.renderView) # None b/c renderSource was False#
