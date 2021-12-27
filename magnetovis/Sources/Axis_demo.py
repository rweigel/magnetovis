# Execute using
#   magnetovis --script=Axis_demo.py

import paraview.simple as pvs
import magnetovis as mvs

mvs.Axis()

'''
# Demo #1
'''

skwargs = {
            "time": "2001-01-01",
            "coord_sys": "GSM",
            "tube": True,
            "tubeAndCone": True,
            "tubeFilterSettings": ["Radius: 0.5", "Capping: 1"]
        }

dkwargs = {
            "display": {
                "Representation": "Surface",
                "Opacity": 1.0,
                "AmbientColor": [1, 1, 0],
                "DiffuseColor": [1, 1, 0]
            },

            "label":
                {
                    "source": {"Text": r"$\alpha^2$/β"},
                    "display": {
                        "FontSize": 24,
                        "Color": [1, 1, 0]
                    }
                }
        }


skwargs['direction'] = "Y"
skwargs['extent'] = [-40, 40]
yAxis = mvs.Axis(registrationName="α^2/β Axis", **skwargs)
mvs.SetDisplayProperties(source=yAxis, **dkwargs)

#print(mvs.GetDisplayDefaults('Axis'))
#print(mvs.GetSourceDefaults('Axis'))

skwargs['direction'] = "X"
skwargs['extent'] = [-40, 40]
xAxis = mvs.Axis(**skwargs)
#mvs.SetDisplayProperties(xAxis)

skwargs['direction'] = "Z"
skwargs['extent'] = [-40, 40]
zAxis = mvs.Axis(**skwargs)
#mvs.SetDisplayProperties(zAxis)

camera = mvs.SetCamera(viewType="isometric")

