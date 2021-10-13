# From this directory, execute
#   magnetovis --script=Line_demo.py
# When executed results in the display of a line with n_pts-1 segments.

import magnetovis as mvs

sourceArguments = {
                    "n_pts": 2,
                    "length": 10
                }

displayArguments = {
                    "showSource": True,
                    "renderView": None,
                    "displayRepresentation": "Surface"
                }

Line = mvs.Line(
                    sourceName="Demo Line",
                    sourceArguments=sourceArguments,
                    renderSource=True,
                    displayArguments=displayArguments # Ignored if renderSource=False
                )

print(Line.programmableSource)
print(Line.displayProperties)   # None b/c renderSource was False
print(Line.renderView)          # None b/c renderSource was False
print(Line.displayArguments)
print(Line.sourceArguments)

displayArguments['showSource'] = True
displayArguments['displayRepresentation'] = "Point Gaussian"
Line.SetDisplayOptions(displayArguments)

print(Line.programmableSource)
print(Line.displayProperties)
print(Line.renderView)

import paraview.simple as pvs
pvs.SaveScreenshot('Line_demo.png', Line.renderView, ImageResolution=[1670, 1091])
print("Wrote Line_demo.png")