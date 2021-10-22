# From this directory, execute
#   magnetovis --script=Line_demo.py
# When executed results in the display of a line with n_pts-1 segments.
import paraview.simple as pvs
#pvs.Connect("localhost")
#[pvs.Delete(s) for s in pvs.GetSources().values()]
#pvs.ResetSession()

import magnetovis as mvs

sourceArguments = {
                    "time_o": "2001-01-01",
                    "time_f": "2001-01-02",
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

Satellite = mvs.Satellite(
                    registrationName="Satellite Trace",
                    sourceArguments=sourceArguments,
                    renderSource=True,
                    displayArguments=displayArguments # Ignored if renderSource=False
                )

print(Satellite.programmableSource)
print(Satellite.displayProperties)   # None b/c renderSource was False
print(Satellite.renderView)          # None b/c renderSource was False
print(Satellite.displayArguments)
print(Satellite.sourceArguments)

displayArguments['showSource'] = True
displayArguments['ambientColor'] = [1, 0, 0]
displayArguments['diffuseColor'] = [1, 0, 0]
Satellite.SetDisplayOptions(displayArguments)

print(Satellite.programmableSource)
print(Satellite.displayProperties)
print(Satellite.renderView)

#import paraview.simple as pvs
#pvs.SaveScreenshot('Axis_demo.png', Axis.renderView, ImageResolution=[1670, 1091])
#print("Wrote Axis_demo.png")