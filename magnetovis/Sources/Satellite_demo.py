# From this directory, execute
#   magnetovis --script=Satellite.py

import magnetovis as mvs

kwargs = {
            "start": "2001-01-01T00:00:00",
            "stop": "2001-01-03T00:00:00",
            "coord_sys": "GSM",
            "id": "geotail"
        }
kwargs["registrationName"] = "{}/{}-{}/{}".format(kwargs['id'],
                                                  kwargs['start'],
                                                  kwargs['stop'],
                                                  kwargs['coord_sys'])
Satellite = mvs.Satellite(**kwargs)

displayArguments = {
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
                        }
                    }

displayProperties = mvs.SetDisplayProperties(Satellite, displayArguments=displayArguments)
