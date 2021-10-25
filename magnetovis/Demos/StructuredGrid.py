# From this directory, execute
#   magnetovis --script=StructuredGrid_demo.py

import magnetovis as mvs

sourceArguments = {
                    "time": "2001-01-01",
                    "coord_sys": "GSM",
                    "point_array_functions": {"dipole": {"array_name": "B", "M": 1}},
                    "extents": [[-40,40],[-40,40],[-40,40]],
                    "Nx": 3,
                    "Ny": 3,
                    "Nz": 3
                }

displayArguments = {
                    "showSource": True,
                    "renderView": None
                }

registrationName = "Structured Grid/{}/{}/{}x{}x{}" \
                        .format(sourceArguments['time'],
                                sourceArguments['coord_sys'],
                                sourceArguments['Nx'],
                                sourceArguments['Ny'],
                                sourceArguments['Nz'])

StructuredGrid = mvs.StructuredGrid(
                    registrationName=registrationName,
                    sourceArguments=sourceArguments,
                    renderSource=True,
                    displayArguments=displayArguments
                )

displayArguments['showSource'] = True
displayArguments['displayRepresentation'] = "Surface"
StructuredGrid.SetDisplayOptions(displayArguments)

StructuredGrid.renderView.CameraPosition = [529., 282., 247.]
StructuredGrid.renderView.CameraViewUp = [-0.33, -0.19, 0.92]
