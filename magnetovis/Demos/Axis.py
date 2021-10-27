# From this directory, execute
#   magnetovis --script=Axis.py

import paraview.simple as pvs

import magnetovis as mvs

sourceArguments = {
                    "time": "2001-01-01",
                    "extent": [-40., 40.],
                    "coord_sys": "GSM",
                    "direction": "X"
                }

displayArguments = {
                    "showSource": True,
                    "renderView": None,
                    "displayRepresentation": "Surface",
                    "opacity": None,
                    "ambientColor": None,
                    'diffuseColor': None
                }

Axis = mvs.Axis(
                    registrationName="Z-Axis",
                    sourceArguments=sourceArguments,
                    renderSource=True,
                    displayArguments=displayArguments # Ignored if renderSource=False
                )

displayArguments['showSource'] = True
displayArguments['ambientColor'] = [1, 0, 0]
displayArguments['diffuseColor'] = [1, 0, 0]
Axis.SetDisplayOptions(displayArguments)

# reset view to fit data
Axis.renderView.ResetCamera()
