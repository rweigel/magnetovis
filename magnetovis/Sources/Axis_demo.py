# Execute using
#   magnetovis --script=Axis_demo.py

import paraview.simple as pvs

import magnetovis as mvs

kwargs = {
            "time": "2001-01-01",
            "coord_sys": "GSM",
            "tube": True,
            "tubeAndCone": True,
            "tubeFilterSettings": ["Radius: 0.5", "Capping: 1"]
        }

displayArguments = {
                        "label": {
                                'Text': r'$\alpha^2$/β',
                                'FontSize': 22,
                                'Color': [0, 0, 0],
                            },
                        "object": {
                            "Opacity": 1.0,
                            'AmbientColor': [1, 0, 0],
                            'DiffuseColor': [1, 0, 0]
                        }
                    }

kwargs['direction'] = "X"
kwargs['extent'] = [-40, 40]
xAxis = mvs.Axis(**kwargs)
mvs.SetDisplayProperties(xAxis, displayArguments=displayArguments)

kwargs['direction'] = "Y"
kwargs['extent'] = [-40, 40]
yAxis = mvs.Axis(**kwargs)
mvs.SetDisplayProperties(yAxis)

kwargs['direction'] = "Z"
kwargs['extent'] = [-40, 40]
zAxis = mvs.Axis(**kwargs)
mvs.SetDisplayProperties(zAxis)

camera = mvs.SetCamera(viewType="isometric")
