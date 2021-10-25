# From this directory, execute
#   magnetovis --script=PolyLine_demo.py

import magnetovis as mvs

sourceArguments = {
                    "time": "2001-01-01",
                    "coord_sys": "GSM",
                    "point_function": {
                                            "curve": 
                                                {   
                                                    "Npts": 6,
                                                    "coord_sys": "GSM"
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

registrationName = "MultiLine/{}/{}" \
                        .format(sourceArguments['time'],
                                sourceArguments['coord_sys'])

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
