# From this directory, execute
#   magnetovis --script=Plane_demo.py

import magnetovis as mvs

time = (2015, 1, 1, 0, 0, 0)
csys = 'GEO'

mvs.earth(time, coord_sys=csys)

sourceArguments = {
                    "time": "2001-01-01",
                    "normal": "Z",
                    "extents": [[-40,40],[-40,40]],
                    "offset": 0,
                    "coord_sys": "GSM"
                }

displayArguments = {
                    "showSource": True,
                    "renderView": None,
                    "opacity": 0.25
                }

Plane = mvs.Plane(
                    registrationName="XY Plane/GSM/"+sourceArguments['time'],
                    sourceArguments=sourceArguments,
                    renderSource=True,
                    displayArguments=displayArguments
                )

#print(Plane.programmableSource)
#print(Plane.displayProperties) # None b/c renderSource was False
#print(Plane.renderView) # None b/c renderSource was False#

displayArguments['showSource'] = True
displayArguments['displayRepresentation'] = "Surface"
Plane.SetDisplayOptions(displayArguments)
