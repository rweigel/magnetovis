# From this directory, execute
#   magnetovis --script=Curve_demo.py

import magnetovis as mvs

Npts = 30
sourceArguments = {
                    "coord_sys": "GSM",
                    "Npts": 4,
                    "closed": False,
                    "point_function": {"circle": {
                                                    "radius": 1.0,
                                                    "origin": (0.0, 0.0, 0.0),
                                                    "orientation": (0, 0, 1)
                                                }
                    },
                    "point_array_functions": {
                                                "position": 
                                                    {
                                                        "array_name": "point_positions",
                                                        "coord_sys": "GSM"
                                                    }
                    }
                }

displayArguments = {
                    "showSource": True,
                    "renderView": None
                }

registrationName = "Curve/{}/{}" \
                        .format(Npts, sourceArguments['coord_sys'])

MultiCurve = mvs.Curve(
                    registrationName=registrationName,
                    sourceArguments=sourceArguments,
                    renderSource=False,
                    displayArguments=displayArguments
                )

#print(Plane.programmableSource)
#print(Plane.displayProperties) # None b/c renderSource was False
#print(Plane.renderView) # None b/c renderSource was False#

displayArguments['showSource'] = True
displayArguments['displayRepresentation'] = "Surface"
MultiCurve.SetDisplayOptions(displayArguments)

# reset view to fit data
MultiCurve.renderView.ResetCamera()
