import magnetovis as mvs
import paraview.simple as pvs

time = [2015,3,20,0,0,0] # time not used if coord_sys = GSM
coord_sys = 'GSM'
M=7.788E22
dipoleFieldSourceDisplay, renderView, dipoleFieldSource =  mvs.dipole_field(time, M, coord_sys)

# create a new 'Glyph'
glyph = pvs.Glyph(registrationName='-- Glyph', Input=dipoleFieldSource,
    GlyphType='Arrow')
glyph.OrientationArray = ['POINTS', 'B_field']
glyph.ScaleArray = ['POINTS', 'No scale array']

# show data in view
glyphDisplay = pvs.Show(glyph, renderView, 'GeometryRepresentation')
glyphDisplay.Opacity = 0.72

# center and position camera
renderView.CameraPosition = [0, -120, 0]
renderView.CameraFocalPoint = [0, 0.0, 0]
renderView.CameraViewUp = [0.0, 0.0, 1.0]

pvs.Hide(dipoleFieldSource, renderView)
renderView.Update()
