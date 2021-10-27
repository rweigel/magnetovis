# From this directory, execute
#   magnetovis --script=Lines_demo.py

import magnetovis as mvs

Npts = 10
closed = False
sourceArguments = {
                    "time": "2001-01-01",
                    "coord_sys": "GSM",
                    "Npts": Npts,
                    "closed": closed,
                    "point_function": {
                                        "circle": {
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

registrationName = "Circle using Lines Source/Npts={}/closed={}".format(Npts, closed)

MultiLine = mvs.MultiLine(
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
MultiLine.SetDisplayOptions(displayArguments)

# reset view to fit data
MultiLine.renderView.ResetCamera()
