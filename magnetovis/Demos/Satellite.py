# From this directory, execute
#   magnetovis --script=Satellite.py

import paraview.simple as pvs

import magnetovis as mvs

sourceArguments = {
                    "time_o": "2001-01-01T00:00:00",
                    "time_f": "2001-01-03T00:00:00",
                    "coord_sys": "GSM",
                    "satellite_id": 'geotail',
                    'tube_radius': 1.0
                }

displayArguments = {
                    "showSource": True,
                    "renderView": None,
                    "region_colors": {
                        'D_Msheath' : (230./255, 25./255,  75./255,  0.7), # red
                        'N_Msheath' : (245./255, 130./255, 48./255,  0.7), # orange
                        'D_Msphere' : (255./255, 255./255, 25./255,  0.7), # yellow
                        'N_Msphere' : (220./255, 190./255, 255./255, 0.7), # lavender
                        'D_Psphere' : (60./255,  180./255, 75./255,  0.7), # green
                        'N_Psphere' : (70./255,  240./255, 240./255, 0.7), # cyan
                        'Tail_Lobe' : (0,        130./255, 200./255, 0.7), # blue
                        'Plasma_Sh' : (145./255, 30./255,  180./255, 0.7), # purple
                        'HLB_Layer' : (240./255, 50./255,  230./255, 0.7), # magenta
                        'LLB_Layer' : (128./255, 128./255, 128./255, 0.7), # grey
                        'Intpl_Med' : (255./255, 255./255, 255./255, 0.7)  # white
                    },
                    "displayRepresentation": "Surface",
                    "opacity": None,
                    "ambientColor": None,
                    'diffuseColor': None
                }

Satellite = mvs.Satellite(
                    registrationName=sourceArguments['satellite_id'],
                    sourceArguments=sourceArguments,
                    renderSource=True,
                    displayArguments=displayArguments # Ignored if renderSource=False
                )


displayArguments['showSource'] = True
displayArguments['ambientColor'] = [1, 0, 0]
displayArguments['diffuseColor'] = [1, 0, 0]
Satellite.SetDisplayOptions(displayArguments)

# reset view to fit data
Satellite.renderView.ResetCamera()
