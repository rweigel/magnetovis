# From this directory, execute
#   magnetovis --script=Line_demo.py
# When executed results in the display of a line with n_pts-1 segments.
import paraview.simple as pvs

import magnetovis as mvs

sourceArguments = {
                    "time": "2001-01-01",
                    "normal": "Z",
                    "extent": [-40,40],
                    "coord_sys": "GSM"
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

#print(Axis.programmableSource)
#print(Axis.displayProperties)   # None b/c renderSource was False
#print(Axis.renderView)          # None b/c renderSource was False
#print(Axis.displayArguments)
#print(Axis.sourceArguments)

displayArguments['showSource'] = True
displayArguments['ambientColor'] = [1, 0, 0]
displayArguments['diffuseColor'] = [1, 0, 0]
Axis.SetDisplayOptions(displayArguments)

#print(Axis.programmableSource)
#print(Axis.displayProperties)
#print(Axis.renderView)

