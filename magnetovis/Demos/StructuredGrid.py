# From this directory, execute
#   magnetovis --script=Plane_demo.py

import magnetovis as mvs

def field(points, M=7.788E22):
    import numpy as np
    r = np.linalg.norm(points, axis=1)
    B = np.zeros(points.shape)
    B[:,0] = 3*M*points[:,0]*points[:,2]/r**5 # Bx = 3*M*x*z/r^5
    B[:,1] = 3*M*points[:,1]*points[:,2]/r**5 # By = 3*M*y*z/r^5
    B[:,2] = M*(3*points[:,2]**2-r**2)/r**5   # Bz = M(3*z^2 - r^2)/r^5

    return B

mvs.dipole = field

sourceArguments = {
                    "time": "2001-01-01",
                    "normal": "Z",
                    "extents": [[-40,40],[-40,40],[0,0]],
                    "point_functions": {"dipole": 
                                            {
                                                "name": "dipole",
                                                "M": 7.788E22
                                            }
                                        },
                    "Nx": 2,
                    "Ny": 2,
                    "Nz": 1,                    
                    "offset": 0,
                    "coord_sys": "GSM"
                }

displayArguments = {
                    "showSource": True,
                    "renderView": None
                }

Plane = mvs.StructuredGrid(
                    registrationName="XY Plane",
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
