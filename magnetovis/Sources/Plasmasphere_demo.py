# Execute using
#   magnetovis Plasmasphere_demo.py

# Demo 1
import magnetovis as mvs
mvs.Plasmasphere()
mvs.SetTitle('GCC88 Plasmasphere')

# Demo #2
import magnetovis as mvs
mvs.CreateViewAndLayout()
mvs.Earth(coord_sys='SM')

plasmasphere = mvs.Plasmasphere()

# Add slice
import paraview.simple as pvs
pvs.Hide(plasmasphere)

slice1 = pvs.Slice(registrationName=' y=0 slice', Input=plasmasphere)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.SliceOffsetValues = [0.0]
slice1.SliceType.Normal = [0.0, 1.0, 0.0]

renderView1 = pvs.GetActiveViewOrCreate('RenderView')
slice1Display = pvs.Show(slice1, renderView1, 'GeometryRepresentation')

# Show slice color bar
slice1Display.SetScalarBarVisibility(renderView1, True)
pvs.Hide3DWidgets(proxy=slice1.SliceType)

# Add countour
contour1 = pvs.Contour(registrationName=' 3.0 Contour', Input=slice1)
contour1.ContourBy = ['POINTS', 'H+ log density (cm^-3)']
contour1.Isosurfaces = [3.0]
contour1.PointMergeMethod = 'Uniform Binning'
pvs.Show(contour1)

mvs.SetCamera(viewType="+Y")

