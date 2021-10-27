# From this directory, execute
#   magnetovis --script=Plane.py

import magnetovis as mvs

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

displayArguments['showSource'] = True
displayArguments['displayRepresentation'] = "Surface"
Plane.SetDisplayOptions(displayArguments)

# reset view to fit data
Plane.renderView.ResetCamera()
