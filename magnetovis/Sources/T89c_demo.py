import paraview.simple as pvs
import magnetovis as mvs

t89c = mvs.T89c(dimensions=[10, 10, 10])

if False:
	streamTracer1 = pvs.StreamTracer(registrationName='StreamTracer1', Input=t89c, SeedType='Line')
	streamTracer1.Vectors = ['POINTS', 'B']
	streamTracer1.MaximumStreamlineLength = 50.0

	# init the 'Line' selected for 'SeedType'
	streamTracer1.SeedType.Point1 = [-20.0, 0.0, 0.0]
	streamTracer1.SeedType.Point2 = [-10.0, 0.0, 0.0]
	streamTracer1.SeedType.Resolution = 10

	# set active source
	pvs.SetActiveSource(streamTracer1)

	# show data in view
	streamTracer1Display = pvs.Show(streamTracer1)


