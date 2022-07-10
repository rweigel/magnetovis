import paraview.simple as pvs

# https://gitlab.kitware.com/paraview/paraview/-/issues/21459

# /Applications/ParaView-5.10.1.app/Contents/MacOS/paraview --script script.py
# xattr -d com.apple.quarantine /Applications/ParaView-master-5.10.1-1472-g92b14e0412.app
# /Applications/ParaView-master-5.10.1-1472-g92b14e0412.app/Contents/MacOS/paraview --script script.py

# /Applications/ParaView-5.10.1.app/Contents/bin/pvbatch script.py
# xattr -d com.apple.quarantine /Applications/ParaView-master-5.10.1-1472-g92b14e0412.app
# /Applications/ParaView-master-5.10.1-1472-g92b14e0412.app/Contents/bin/pvbatch script.py

try:
	__file__
	fname = 'pvbatch.png'
except:
	fname = 'gui.png'


# Determine image resolution to use by executing in GUI and inspecting the metadata.
ImageResolution = [1368, 684]
#FontScaling = "Do not scale fonts"
FontScaling = "Scale fonts proportionally"

view = pvs.GetActiveViewOrCreate('RenderView')
text = pvs.Text(Text=fname)
pvs.Show(text)

sphere = pvs.Sphere()
pvs.Show(sphere)

display = pvs.GetDisplayProperties(sphere, view=view)
pvs.ColorBy(display, ('POINTS', 'Normals', 'Magnitude'))
display.SetScalarBarVisibility(view, True)

pvs.SaveScreenshot(fname, view, FontScaling=FontScaling, ImageResolution=ImageResolution)
